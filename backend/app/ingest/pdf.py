"""PDF → text, layout preserved.

Primary: poppler's `pdftotext -layout` (keeps table columns aligned, which the column-based
parsers rely on). Fallback: `pypdf` if installed (no layout, so table parsing degrades to
partial). OCR is NOT attempted automatically: if a PDF has no text layer the document is
marked `needs_ocr` and left for a human, because OCR digits are not reliable enough to enter
the verification queue unflagged.
"""

import shutil
import subprocess
import tempfile
from dataclasses import dataclass

MIN_TEXT_CHARS = 40  # below this, the PDF is treated as having no text layer (scanned)


@dataclass
class PdfText:
    text: str  # pages separated by form feed (\f)
    method: str  # "pdftotext-layout" | "pypdf" | "none"
    error: str | None = None

    @property
    def pages(self) -> list[str]:
        return self.text.split("\f")

    @property
    def has_text(self) -> bool:
        return len(self.text.strip()) >= MIN_TEXT_CHARS


def pdftotext_available() -> bool:
    return shutil.which("pdftotext") is not None


def extract_text(data: bytes, timeout: float = 60) -> PdfText:
    if pdftotext_available():
        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(data)
            f.flush()
            proc = subprocess.run(
                ["pdftotext", "-layout", "-enc", "UTF-8", f.name, "-"],
                capture_output=True,
                timeout=timeout,
            )
        if proc.returncode == 0:
            return PdfText(proc.stdout.decode("utf-8", errors="replace"), "pdftotext-layout")
        error = proc.stderr.decode("utf-8", errors="replace")[:300]
    else:
        error = "pdftotext not installed"
    try:
        import io

        from pypdf import PdfReader  # optional dependency
    except ImportError:
        return PdfText("", "none", error)
    try:
        reader = PdfReader(io.BytesIO(data))
        return PdfText("\f".join(p.extract_text() or "" for p in reader.pages), "pypdf")
    except Exception as e:  # malformed PDF
        return PdfText("", "none", f"{error}; pypdf: {type(e).__name__}: {e}"[:300])
