"""OCR of scanned BEAC notices: two independent tesseract passes, words with their boxes.

Every BEAC auction notice sampled is a page image (scanner output). Some PDFs carry a text layer
written by the scanner's own OCR; it is unreliable ("6,007o" for 6,00 %, "ls 000" for 15 000) and
is NEVER read here: pages are rasterised and re-OCRed.

Two passes, deliberately configured differently so that their errors are independent:

  pass "A"  pdftoppm 300 dpi greyscale → tesseract --psm 4 (single column of text of variable
            sizes), default global Otsu binarisation (thresholding_method=0).
  pass "B"  pdftoppm 400 dpi greyscale → tesseract --psm 3 (fully automatic page segmentation),
            Sauvola adaptive (local) binarisation (thresholding_method=2).

Both use the French+English LSTM models (`-l fra+eng --oem 1`). The checker (beac_check) stores a
value only when both passes read it identically. Each pass keeps its plain text and every word
with its bounding box (in pixels of that pass's raster) and confidence, so any stored value can be
traced to a crop of the page.

Results are cached as JSON next to the stored PDF (`<sha256>.ocr.json`), keyed by a configuration
signature: changing a pass configuration invalidates the cache.
"""

import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

LANG = "fra+eng"


@dataclass(frozen=True)
class PassConfig:
    name: str
    dpi: int
    psm: int
    thresholding_method: int  # tesseract: 0 = Otsu, 1 = Leptonica Otsu, 2 = Sauvola

    @property
    def signature(self) -> str:
        return f"{self.name}:dpi{self.dpi}:psm{self.psm}:thr{self.thresholding_method}:{LANG}:oem1"


PASSES = (
    PassConfig("A", dpi=300, psm=4, thresholding_method=0),
    PassConfig("B", dpi=400, psm=3, thresholding_method=2),
)
SIGNATURE = "|".join(p.signature for p in PASSES)


@dataclass
class Word:
    text: str
    left: int
    top: int
    width: int
    height: int
    conf: float
    block: int
    par: int
    line: int

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height


@dataclass
class Line:
    """One OCR line: words left to right, with the union box."""

    page: int  # 1-based
    index: int  # 0-based line number within the page (reading order of tesseract)
    words: list[Word]

    @property
    def text(self) -> str:
        return " ".join(w.text for w in self.words)

    @property
    def box(self) -> tuple[int, int, int, int]:
        return (min(w.left for w in self.words), min(w.top for w in self.words),
                max(w.right for w in self.words), max(w.bottom for w in self.words))


@dataclass
class PageOcr:
    page: int
    width: int
    height: int
    text: str
    words: list[Word] = field(default_factory=list)

    def lines(self) -> list[Line]:
        groups: dict[tuple[int, int, int], list[Word]] = {}
        for w in self.words:
            groups.setdefault((w.block, w.par, w.line), []).append(w)
        out = []
        for i, key in enumerate(sorted(groups, key=lambda k: (min(w.top for w in groups[k]), k))):
            out.append(Line(self.page, i, sorted(groups[key], key=lambda w: w.left)))
        return out


@dataclass
class PassResult:
    config: PassConfig
    pages: list[PageOcr]

    @property
    def text(self) -> str:
        return "\f".join(p.text for p in self.pages)

    def lines(self) -> list[Line]:
        return [ln for p in self.pages for ln in p.lines()]


@dataclass
class DocumentOcr:
    signature: str
    passes: dict[str, PassResult]
    page_count: int
    engine: str | None = None  # "tesseract 5.3.4" (recorded since; older caches: None)

    def to_json(self) -> str:
        return json.dumps({"signature": self.signature, "page_count": self.page_count, "engine": self.engine,
                           "passes": {k: {"config": asdict(v.config),
                                          "pages": [asdict(p) for p in v.pages]}
                                      for k, v in self.passes.items()}}, ensure_ascii=False)

    @classmethod
    def from_json(cls, s: str) -> "DocumentOcr":
        d = json.loads(s)
        passes = {}
        for k, v in d["passes"].items():
            pages = [PageOcr(p["page"], p["width"], p["height"], p["text"], [Word(**w) for w in p["words"]])
                     for p in v["pages"]]
            passes[k] = PassResult(PassConfig(**v["config"]), pages)
        return cls(d["signature"], passes, d["page_count"], d.get("engine"))


class OcrUnavailable(RuntimeError):
    pass


def tools_available() -> bool:
    return bool(shutil.which("pdftoppm") and shutil.which("tesseract"))


def rasterise(pdf: Path, dpi: int, out_dir: Path, first: int | None = None, last: int | None = None) -> list[Path]:
    """PDF pages → greyscale PNGs at `dpi`. Returns the page images in page order."""
    cmd = ["pdftoppm", "-r", str(dpi), "-gray", "-png"]
    if first:
        cmd += ["-f", str(first)]
    if last:
        cmd += ["-l", str(last)]
    prefix = out_dir / f"p{dpi}"
    subprocess.run([*cmd, str(pdf), str(prefix)], check=True, capture_output=True, timeout=300)
    return sorted(out_dir.glob(f"p{dpi}-*.png"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))


def _png_size(path: Path) -> tuple[int, int]:
    with open(path, "rb") as f:
        head = f.read(24)
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def _tesseract_tsv(image: Path, cfg: PassConfig) -> tuple[str, list[Word]]:
    cmd = ["tesseract", str(image), "stdout", "-l", LANG, "--oem", "1", "--psm", str(cfg.psm),
           "-c", f"thresholding_method={cfg.thresholding_method}", "-c", "preserve_interword_spaces=0",
           "tsv"]
    proc = subprocess.run(cmd, capture_output=True, timeout=600, env={**os.environ, "OMP_THREAD_LIMIT": "1"})
    if proc.returncode != 0:
        raise OcrUnavailable(proc.stderr.decode("utf-8", "replace")[:300])
    words: list[Word] = []
    rows = proc.stdout.decode("utf-8", "replace").splitlines()
    for row in rows[1:]:
        parts = row.split("\t")
        if len(parts) < 12 or parts[0] != "5" or not parts[11].strip():
            continue
        words.append(Word(text=parts[11].strip(), left=int(parts[6]), top=int(parts[7]),
                          width=int(parts[8]), height=int(parts[9]), conf=float(parts[10]),
                          block=int(parts[2]), par=int(parts[3]), line=int(parts[4])))
    # Plain text rebuilt from the TSV lines (identical words to what is stored as boxes).
    page = PageOcr(0, 0, 0, "", words)
    text = "\n".join(ln.text for ln in page.lines())
    return text, words


def ocr_pdf(pdf: Path, max_pages: int = 3) -> DocumentOcr:
    """Run both passes on the first `max_pages` pages of a PDF."""
    if not tools_available():
        raise OcrUnavailable("pdftoppm and tesseract are required")
    passes: dict[str, PassResult] = {}
    page_count = 0
    with tempfile.TemporaryDirectory() as tmp:
        for cfg in PASSES:
            images = rasterise(pdf, cfg.dpi, Path(tmp), last=max_pages)
            pages = []
            for i, img in enumerate(images, start=1):
                text, words = _tesseract_tsv(img, cfg)
                w, h = _png_size(img)
                pages.append(PageOcr(i, w, h, text, words))
            passes[cfg.name] = PassResult(cfg, pages)
            page_count = max(page_count, len(pages))
    version = subprocess.run(["tesseract", "--version"], capture_output=True, text=True).stdout.split("\n")[0]
    return DocumentOcr(SIGNATURE, passes, page_count, version.strip() or None)


def cached_ocr(pdf: Path, cache: Path | None = None, max_pages: int = 3) -> DocumentOcr:
    """OCR with a JSON cache next to the PDF (re-run when the pass configuration changed)."""
    cache = cache or pdf.with_suffix(".ocr.json")
    if cache.is_file():
        try:
            doc = DocumentOcr.from_json(cache.read_text(encoding="utf-8"))
            if doc.signature == SIGNATURE:
                return doc
        except (ValueError, KeyError, TypeError):
            pass
    doc = ocr_pdf(pdf, max_pages=max_pages)
    cache.write_text(doc.to_json(), encoding="utf-8")
    return doc


def crop_png(pdf: Path, page: int, box: tuple[int, int, int, int], dpi: int, out: Path,
             margin: int = 20) -> Path:
    """Render `box` (pixels at `dpi`) of a page to a PNG, for audit. Uses pdftoppm's crop."""
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0 - margin), max(0, y0 - margin)
    w, h = (x1 - x0) + 2 * margin, (y1 - y0) + 2 * margin
    prefix = out.with_suffix("")
    subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page), "-x", str(x0), "-y", str(y0),
                    "-W", str(w), "-H", str(h), "-png", "-singlefile", str(pdf), str(prefix)],
                   check=True, capture_output=True, timeout=120)
    return prefix.with_suffix(".png")
