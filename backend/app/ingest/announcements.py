"""Cross-check verified auctions against the official results announcement of the same operation.

Many UMOA-Titres result reports ("Compte rendu d'adjudication") print amounts rounded to whole
millions (or to 0,01 million) and prices to two decimals, while the results announcement of the
same operation ("Annonce au Marché des Titres Publics", the "Annonce" document of the operation
page https://www.umoatitres.org/fr/emission/<slug>/) prints the exact amounts in FCFA. This module
finds that announcement for every verified non-synthetic auction, stores it (document store +
SourceDocument, document_type "auction_results_announcement", SHA-256), parses its per-security
table and classifies every comparable field:

  A  identical (same value);
  A2 consistent, the announcement is COARSER (it prints the stored value rounded): nothing to do;
  B  ROUNDING: the stored value equals the announcement value rounded to the precision the report
     printed (proved on the raw report text) -> the exact announcement value is proposed;
  C  DISCREPANCY: anything else -> flagged for a human, never changed;
  D  not printed in the announcement (or not stored).

Columns are mapped to securities only when unambiguous: the announcement prints ISINs, or its
instrument/tenor headers equal, in order and without repeated labels, the report's tranche
labels. Otherwise the auctions of that operation are "unmapped" and nothing is compared.

Nothing here writes to the auction table: category B proposals (with their evidence) are written
to data/announcement_cross_check.json and applied by app.ingest.amend after re-verification.

    python -m app.ingest.announcements --report /path/cross_check_report.json [--cache DIR]
"""

import argparse
import hashlib
import json
import re
import sys
import time
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from pathlib import Path

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingest.pdf import extract_text
from app.ingest.umoa import (
    LISTING_URL,
    Fetched,
    parse_listing,
    parse_operation_page,
    save_document,
    get_source,
)
from app.models import Auction, AuctionExtraction, SourceDocument
from app.models.enums import VerificationStatus
from app.watch.sources import USER_AGENT

DOCUMENT_TYPE = "auction_results_announcement"
DATA_FILE = Path(__file__).resolve().parent / "data" / "announcement_cross_check.json"
ANNOUNCE_LABEL = "annonce"
REPORT_LABEL = "compte rendu"
PAUSE_SECONDS = 0.5


# --------------------------------------------------------------------------- polite fetching


class PoliteFetcher:
    """GET with a pause between network requests, retries with backoff on errors and 5xx/429,
    and an optional on-disk cache (so a re-run of the campaign does not hit the server again)."""

    def __init__(self, cache_dir: Path | None = None, pause: float = PAUSE_SECONDS, retries: int = 4) -> None:
        self.cache_dir = cache_dir
        self.pause = pause
        self.retries = retries
        self.requests = 0
        self.client = httpx.Client(timeout=60, follow_redirects=True, headers={"User-Agent": USER_AGENT})

    def _cache_path(self, url: str) -> Path | None:
        if self.cache_dir is None:
            return None
        return self.cache_dir / hashlib.sha256(url.encode()).hexdigest()

    def __call__(self, url: str, use_cache: bool = True) -> Fetched:
        cp = self._cache_path(url)
        if use_cache and cp is not None and cp.exists():
            meta = json.loads(cp.with_suffix(".json").read_text())
            return Fetched(meta["status"], meta["url"], cp.read_bytes(), meta.get("content_type"))
        last = None
        for attempt in range(self.retries):
            time.sleep(self.pause if attempt == 0 else 2 ** attempt)
            self.requests += 1
            try:
                r = self.client.get(url)
            except httpx.HTTPError as e:
                last = Fetched(None, url, b"", None, f"{type(e).__name__}: {e}"[:300])
                continue
            last = Fetched(r.status_code, str(r.url), r.content, r.headers.get("content-type"))
            if r.status_code in (429, 500, 502, 503, 504):
                continue
            break
        if cp is not None and last is not None and last.status == 200:
            cp.parent.mkdir(parents=True, exist_ok=True)
            cp.write_bytes(last.content)
            cp.with_suffix(".json").write_text(json.dumps(
                {"status": last.status, "url": last.url, "content_type": last.content_type}))
        return last


Fetcher = Callable[[str], Fetched]


# --------------------------------------------------------------------------- numbers


def _fold(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).replace("’", "'").replace("\xa0", " ").replace(" ", " ")
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def french_number(tok: str) -> Decimal | None:
    """'39 907 270 000' -> 39907270000; '96,2654%' -> 96.2654; '-' / '' -> None."""
    t = re.sub(r"[\s \xa0]", "", tok).rstrip("%")
    if not re.fullmatch(r"\d+(,\d+)?", t):
        return None
    return Decimal(t.replace(",", "."))


def decimals_of(raw: str) -> int | None:
    """Decimals printed in the first number of a raw report cell ('4 431,25 millions' -> 2)."""
    m = re.search(r"\d+(?:[  \xa0]\d{3})*(?:,(\d+))?", raw or "")
    if not m:
        return None
    return len(m.group(1)) if m.group(1) else 0


def split_values(rest: str) -> tuple[list[str], bool]:
    """Split the value part of a table row into cells. Returns (cells, unique).

    Thousands are separated by single spaces and columns by one or more spaces, so a 3-digit group
    could either continue a number or start the next one. Groups are joined greedily (a group
    continues the previous number iff it has exactly 3 integer digits and the previous group has no
    decimal part / '%'); the greedy split has the fewest cells, so it is the only possible split
    when its length equals the number of columns. The caller checks that (fail closed otherwise).
    A '-' cell is kept as '-' (nothing printed)."""
    cells: list[str] = []
    ok = True
    for chunk in re.split(r"\s{2,}", rest.strip()):
        prev_closed = True
        for part in chunk.split():
            if part in ("-", "–"):
                cells.append("-")
                prev_closed = True
                continue
            if not re.fullmatch(r"\d+(,\d+)?%?", part):
                ok = False
                cells.append(part)
                prev_closed = True
                continue
            intdigits = len(part.split(",")[0].rstrip("%"))
            if not prev_closed and intdigits == 3:
                cells[-1] += " " + part
            else:
                cells.append(part)
            prev_closed = "," in part or part.endswith("%")
    return cells, ok


# --------------------------------------------------------------------------- announcement parsing

ISIN_RE = re.compile(r"\b[A-Z]{2}[A-Z0-9]{9}\d\b")
HEADER_RE = re.compile(r"\b(BAT|OAT)\s*[-–]?\s*(\d+(?:,\d+)?)\s*(ans?|mois|jours?|semaines?)\b", re.I)
TITLE_RE = re.compile(r"^(resultats? (de l'emission|de l'emission simultanee|du rachat|global)|"
                      r"resultat global|emission simultanee|emission|rachat de titres|rachat)\b")


def field_of(label: str) -> str | None:
    """Field read from a table row, from its folded label (None: row not compared)."""
    f = _fold(label)
    if not f or f.startswith(("dont onc", "montant net", "taux de couverture", "taux d'absorption", "taux de rendement")):
        return None
    if "nombre de participants" in f:
        return "number_of_participants"
    if "nombre de soumissions" in f:
        return "number_of_bids"
    if "rendement moyen" in f:
        return "weighted_average_yield"
    if "marginal" in f:
        return "marginal"
    if "moyen pondere" in f:
        return "weighted_average"
    if "retenu" in f and ("montant" in f or "soumissions" in f):
        return "amount_allocated"
    if "montant" in f and "soumissions" in f:
        return "amount_submitted"
    return None


def norm_label(text: str) -> str | None:
    """Comparable column label: 'OAT - 2 ans' == 'OAT 2 ans' == 'oat-2 an'."""
    m = HEADER_RE.search(text)
    if not m:
        return None
    unit = m.group(3).lower()
    unit = {"an": "ans", "jour": "jours", "semaine": "semaines"}.get(unit, unit)
    return f"{m.group(1).upper()} - {m.group(2)} {unit}"


@dataclass
class Cell:
    value: Decimal | None
    raw: str
    line: str


@dataclass
class Block:
    """One results table: its kind (issue | buyback | global), its column headers, its rows."""

    kind: str
    labels: list[str] = field(default_factory=list)
    isins: list[str] = field(default_factory=list)
    rows: dict[str, list[Cell]] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    @property
    def columns(self) -> int:
        return len(self.isins) or len(self.labels) or 1


@dataclass
class Announcement:
    blocks: list[Block] = field(default_factory=list)

    @property
    def errors(self) -> list[str]:
        return [e for b in self.blocks for e in b.errors]


def _header(line: str) -> tuple[list[str], list[str], str] | None:
    """(labels, isins, leftover) when the line is a column-header row."""
    isins = ISIN_RE.findall(line)
    labels = [norm_label(m.group(0)) for m in HEADER_RE.finditer(line)]
    if not isins and not labels:
        return None
    left = ISIN_RE.sub(" ", HEADER_RE.sub(" ", line))
    left = _fold(left)
    if re.search(r"\d", left.replace("2024", "").replace("2025", "").replace("2026", "")) or len(left) > 60:
        return None
    if isins and labels and len(isins) != len(labels):
        return None
    return [x for x in labels if x], isins, left


def _kind(title: str, current: str) -> str:
    f = _fold(title)
    if "global" in f:
        return "global"
    if "rachat" in f:
        return "buyback"
    if "emission" in f or "resultats" in f:
        return "issue"
    return current


Word = tuple[float, float, str]  # xMin, xMax, text


def pdf_word_lines(content: bytes) -> list[list[Word]]:
    """Words of each printed line (pdftotext -bbox), left to right. Empty for a non-PDF."""
    if content[:4] != b"%PDF":
        return []
    import html as htmllib
    import subprocess
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(content)
        f.flush()
        out = subprocess.run(["pdftotext", "-bbox", "-enc", "UTF-8", f.name, "-"], capture_output=True,
                             timeout=60).stdout.decode("utf-8", "replace")
    lines: dict[tuple[int, float], list[Word]] = {}
    page = 0
    for m in re.finditer(r'<page |<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="[\d.]+">([^<]*)</word>', out):
        if m.group(0).startswith("<page"):
            page += 1
            continue
        key = (page, round(float(m.group(2)), 1))
        lines.setdefault(key, []).append((float(m.group(1)), float(m.group(3)), htmllib.unescape(m.group(4))))
    return [sorted(ws) for _, ws in sorted(lines.items())]


def split_by_geometry(rest: str, ncols: int, word_lines: list[list[Word]]) -> list[str] | None:
    """Cells of a row whose text alone is ambiguous ('5 988 000 000 193 667 000 000'), from the
    printed positions of its words: thousands separators are narrow gaps, column boundaries wide
    ones. Accepted only when every printed line carrying these words splits the same way into
    `ncols` cells, with every column gap at least twice as wide as every thousands gap."""
    tokens = rest.split()
    if not tokens or not word_lines:
        return None
    splits = set()
    for ws in word_lines:
        texts = [w[2] for w in ws]
        n = len(tokens)
        if len(texts) < n or texts[-n:] != tokens:
            continue
        seg = ws[-n:]
        gaps = [seg[i + 1][0] - seg[i][1] for i in range(n - 1)]
        if len(gaps) < ncols - 1 or ncols < 2:
            return None
        order = sorted(range(len(gaps)), key=lambda i: gaps[i], reverse=True)
        wide = sorted(order[:ncols - 1])
        narrow = [gaps[i] for i in order[ncols - 1:]]
        if narrow and min(gaps[i] for i in wide) < 2 * max(narrow):
            return None
        cells, start = [], 0
        for i in wide:
            cells.append(" ".join(tokens[start:i + 1]))
            start = i + 1
        cells.append(" ".join(tokens[start:]))
        # Each cell must itself be a well-formed French number (thousands groups of 3 digits).
        if not all(re.fullmatch(r"\d{1,3}( \d{3})*(,\d+)?%?|-", c) for c in cells):
            return None
        splits.add(tuple(cells))
    return list(next(iter(splits))) if len(splits) == 1 else None


def parse_announcement(text: str, word_lines: list[list[Word]] | None = None) -> Announcement:
    """Results tables of an 'Annonce au MTP' (pdftotext -layout text).

    The document is cut into blocks at section titles ('RESULTAT GLOBAL', 'Résultats de
    l'émission', 'Résultats du rachat', 'Rachat', 'Emission simultanée') and at column-header rows
    (instrument/tenor labels such as 'OAT - 2 ans', or ISINs). A data row is kept only when its
    values split into exactly one cell per column (see split_values); otherwise the row is recorded
    in the block's errors and not read: nothing is guessed."""
    ann = Announcement()
    block: Block | None = None
    kind = "issue"
    pending_label: str | None = None
    for raw_line in text.replace("\f", "\n").splitlines():
        line = raw_line.rstrip()
        f = _fold(line)
        if not f:
            continue
        if f.startswith(("umoa-titres remercie", "fait a dakar")):
            block = None
            pending_label = None
            continue
        head = _header(line)
        if head is not None:
            labels, isins, left = head
            kind = _kind(left, kind) if left else kind
            if kind == "global":
                kind = "issue"
            block = Block(kind, labels, isins)
            ann.blocks.append(block)
            pending_label = None
            continue
        if len(f) < 70 and TITLE_RE.match(f) and not re.search(r"\d{3}", f):
            kind = _kind(f, kind)
            block = Block(kind)
            ann.blocks.append(block)
            pending_label = None
            continue
        if block is None:
            continue
        m = re.search(r"(?<![A-Za-z(])[\d-]", line)
        label, rest = (line[:m.start()], line[m.start():]) if m else (line, "")
        if pending_label is not None and not _fold(label):
            label = pending_label  # values printed on the line below a wrapped label
        key = field_of(label)
        if key is None:
            pending_label = None
            continue
        if not rest.strip():
            pending_label = label  # label without values: they may follow on the next line
            continue
        pending_label = None
        if key in block.rows:
            continue
        cells, ok = split_values(rest)
        if ok and len(cells) < block.columns and word_lines:
            geo = split_by_geometry(rest, block.columns, word_lines)
            if geo is not None:
                cells = geo
        if not ok or len(cells) != block.columns:
            block.errors.append(f"{block.kind}/{key}: {len(cells)} cell(s) for {block.columns} column(s): {line.strip()[:200]}")
            continue
        block.rows[key] = [Cell(french_number(c) if c != "-" else None, c, line.strip()) for c in cells]
    ann.blocks = [b for b in ann.blocks if b.rows or b.errors]
    return ann


# --------------------------------------------------------------------------- discovery


@dataclass
class OperationDocs:
    page_url: str
    report_urls: list[str]
    announcement_urls: list[str]


def discover(report_urls: set[str], dates: set[date], fetch: Fetcher,
             log: Callable[[str], None] = lambda _: None) -> tuple[dict[str, OperationDocs], dict]:
    """Operation pages (from the official listing) whose 'Compte rendu' is one of `report_urls`.
    Only listed operations dated on one of `dates` are opened."""
    stats = {"operations_listed": 0, "operation_pages_opened": 0, "page_errors": []}
    res = fetch(LISTING_URL)
    if res.status != 200:
        raise RuntimeError(f"listing: {res.error or res.status}")
    ops = parse_listing(res.content.decode("utf-8", "replace"), res.url)
    stats["operations_listed"] = len(ops)
    found: dict[str, OperationDocs] = {}
    for op in sorted((o for o in ops if o.operation_date in dates), key=lambda o: (o.operation_date, o.url)):
        page = fetch(op.url)
        stats["operation_pages_opened"] += 1
        if page.status != 200:
            stats["page_errors"].append(f"{op.url}: {page.error or page.status}")
            continue
        links = parse_operation_page(page.content.decode("utf-8", "replace"), page.url)
        reports = [d.url for d in links if d.label == REPORT_LABEL]
        anns = [d.url for d in links if d.label == ANNOUNCE_LABEL]
        docs = OperationDocs(op.url, reports, anns)
        for r in reports:
            if r in report_urls:
                found[r] = docs
        log(f"{op.operation_date} {op.url}: {len(reports)} report(s), {len(anns)} announcement(s)")
    return found, stats


# --------------------------------------------------------------------------- classification

# auction column -> (announcement row, staging field holding the report's printed value, instrument)
FIELDS: dict[str, tuple[str, str, str | None]] = {
    "amount_submitted": ("amount_submitted", "amount_submitted", None),
    "amount_allocated": ("amount_allocated", "amount_allocated", None),
    "cutoff_yield": ("marginal", "marginal_rate", "BAT"),  # bills: marginal rate
    "average_price": ("weighted_average", "weighted_average_price", "OAT"),  # bonds: average price
    "weighted_average_yield": ("weighted_average_yield", "weighted_average_yield", None),
    "number_of_bidders": ("number_of_participants", "number_of_participants", None),
}
AMOUNT_FIELDS = {"amount_submitted", "amount_allocated"}


def unit_of(raw: str) -> Decimal:
    """FCFA per printed unit of a raw amount cell ('4 431,25 millions de F CFA' -> 10^6)."""
    f = _fold(raw)
    if "milliard" in f:
        return Decimal(10) ** 9
    if "million" in f:
        return Decimal(10) ** 6
    return Decimal(1)


def printed_step(raw: str, is_amount: bool) -> Decimal | None:
    """Smallest step the report could print: 10^6 for '29 936 millions', 0,01 for '98,45%'."""
    d = decimals_of(raw)
    if d is None:
        return None
    return (unit_of(raw) if is_amount else Decimal(1)) * Decimal(10) ** -d


def round_to(value: Decimal, step: Decimal, mode: str = ROUND_HALF_UP) -> Decimal:
    return (value / step).quantize(Decimal(1), rounding=mode) * step


def classify(stored: Decimal | None, report_raw: str | None, ann: Decimal | None, ann_raw: str | None,
             is_amount: bool) -> tuple[str, str]:
    """(category, explanation). See the module docstring for the categories."""
    if stored is None:
        return "D", "not stored"
    if ann is None:
        return "D", "not printed in the announcement"
    if ann == stored:
        return "A", "identical"
    step = printed_step(report_raw or "", is_amount)
    if step is not None and ann != stored:
        for mode in (ROUND_HALF_UP, ROUND_HALF_EVEN):
            if round_to(ann, step, mode) == stored and ann % step != 0:
                how = "half-up" if mode == ROUND_HALF_UP else "half-even"
                return "B", (f"report printed {report_raw!r} (step {step.normalize():f}); "
                             f"announcement {ann_raw!r} rounded {how} to that step = stored {stored.normalize():f}")
    if not is_amount and ann_raw:
        ad = decimals_of(ann_raw)
        rd = decimals_of(report_raw or "")
        if ad is not None and rd is not None and ad < rd:
            for mode in (ROUND_HALF_UP, ROUND_HALF_EVEN):
                if round_to(stored, Decimal(10) ** -ad, mode) == ann:
                    how = "half-up" if mode == ROUND_HALF_UP else "half-even"
                    return "A2", f"announcement {ann_raw!r} is the stored value rounded {how} to {ad} decimals (coarser)"
    return "C", f"stored {stored.normalize():f} (report {report_raw!r}) vs announcement {ann_raw!r}"


def announcement_value(cell: "Cell", row_line: str, is_amount: bool) -> Decimal | None:
    if cell.value is None:
        return None
    if not is_amount:
        return cell.value
    label = _fold(row_line.split(cell.raw)[0]) if cell.raw in row_line else _fold(row_line)
    return cell.value * unit_of(label)


# --------------------------------------------------------------------------- mapping


@dataclass
class Tranche:
    """One column of the result report (all staged rows of the document, reviewed or not)."""

    isin: str | None
    kind: str
    label: str | None
    order: tuple[int, int, int]
    extraction: AuctionExtraction


def _order(ext: AuctionExtraction) -> tuple[int, int, int]:
    loc = ((ext.fields or {}).get("isin") or {}).get("locator") or ""
    m = re.match(r"p(\d+):L(\d+)", loc)
    c = re.search(r"col (\d+)/", loc)
    return (int(m.group(1)) if m else 0, int(m.group(2)) if m else 0, int(c.group(1)) if c else 1)


def report_tranches(session: Session, document_id: int) -> list[Tranche]:
    out = []
    for ext in session.scalars(select(AuctionExtraction).where(AuctionExtraction.source_document_id == document_id)):
        if ext.verification_status == VerificationStatus.REJECTED and not ext.isin:
            continue
        f = ext.fields or {}
        tenor = (f.get("tenor") or {}).get("raw") or ""
        kind = (ext.operation or {}).get("operation_kind") or "issue"
        out.append(Tranche(ext.isin, kind, norm_label(f"{ext.instrument or ''} {tenor}"), _order(ext), ext))
    return sorted(out, key=lambda t: t.order)


def map_columns(ann: Announcement, tranches: list[Tranche]) -> tuple[dict[str, tuple[Block, int, str]], dict[str, str]]:
    """ISIN -> (block, column index, method), and ISIN -> reason for the unmapped ones."""
    mapped: dict[str, tuple[Block, int, str]] = {}
    unmapped: dict[str, str] = {}
    for kind in ("issue", "buyback"):
        reps = [t for t in tranches if t.kind == kind]
        if not reps:
            continue
        blocks = [b for b in ann.blocks if b.kind == kind]
        by_isin = {}
        for b in blocks:
            for i, isin in enumerate(b.isins):
                by_isin.setdefault(isin, []).append((b, i))
        labelled = [b for b in blocks if b.labels and not b.isins]
        bare = [b for b in blocks if not b.labels and not b.isins]
        why = None
        method = "header"
        positional: list[tuple[Block, int]] = []
        if labelled:
            ann_labels = [x for b in labelled for x in b.labels]
            rep_labels = [t.label for t in reps]
            positional = [(b, i) for b in labelled for i in range(len(b.labels))]
            if None in rep_labels:
                why = "report tenor label unreadable"
            elif len(set(ann_labels)) != len(ann_labels) or len(set(rep_labels)) != len(rep_labels):
                why = f"repeated instrument/tenor header {ann_labels}: column order not provable"
            elif sorted(ann_labels) != sorted(rep_labels):
                why = f"announcement headers {ann_labels} differ from report tranches {rep_labels}"
            elif ann_labels != rep_labels:
                # Same distinct labels in another order: each label names exactly one column.
                at = {lab: p for lab, p in zip(ann_labels, positional)}
                positional = [at[lab] for lab in rep_labels]
                method = "header (same distinct labels, other order)"
        for pos, t in enumerate(reps):
            if t.isin is None:
                continue
            hits = by_isin.get(t.isin, [])
            if len(hits) == 1:
                mapped[t.isin] = (hits[0][0], hits[0][1], "isin")
            elif len(hits) > 1:
                unmapped[t.isin] = "ISIN printed in several columns"
            elif labelled:
                if why is None:
                    mapped[t.isin] = (positional[pos][0], positional[pos][1], method)
                else:
                    unmapped[t.isin] = why
            elif len(bare) == 1 and len(reps) == 1 and not by_isin:
                mapped[t.isin] = (bare[0], 0, "single")
            else:
                unmapped[t.isin] = (f"no unambiguous {kind} column (blocks: "
                                    f"{len(blocks)}, report {kind} tranches: {len(reps)})")
    return mapped, unmapped


# --------------------------------------------------------------------------- campaign


def read_announcement(content: bytes) -> tuple[str, Announcement]:
    """(text, parsed tables) of an announcement document (PDF, or UTF-8 text for fixtures)."""
    text = document_text(content)
    return text, parse_announcement(text, pdf_word_lines(content))


def is_result_report(text: str) -> bool:
    """A 'Compte rendu' uploaded under the 'Annonce' heading is not an announcement."""
    head = _fold(text[:1500])
    return "compte rendu" in head and "annonce" not in head


def document_text(content: bytes) -> str:
    """pdftotext -layout text of a PDF; a plain-text document (test fixtures) is read as UTF-8."""
    if content[:4] != b"%PDF":
        return content.decode("utf-8", "replace")
    return extract_text(content).text


def compare_auction(auction: Auction, ext: AuctionExtraction, block: Block, col: int) -> dict:
    out = {}
    f = ext.fields or {}
    for name, (row, staged, instrument) in FIELDS.items():
        if instrument and ext.instrument != instrument:
            continue
        is_amount = name in AMOUNT_FIELDS
        stored = getattr(auction, name)
        stored = None if stored is None else Decimal(stored)
        sf = f.get(staged) or {}
        report_raw = sf.get("raw")
        cell = (block.rows.get(row) or [None] * block.columns)[col]
        rec = {"stored": None if stored is None else f"{stored.normalize():f}", "report_raw": report_raw,
               "announcement_raw": cell.raw if cell else None, "announcement_line": cell.line if cell else None}
        if stored is not None and sf.get("value") is not None and name != "number_of_bidders" \
                and not (name == "average_price" and sf.get("unit") == "XOF_per_unit") \
                and Decimal(sf["value"]) != stored:
            cat, why = "D", f"stored value differs from the report reading {sf['value']!r}: not comparable"
        elif name == "average_price" and sf.get("unit") == "XOF_per_unit":
            cat, why = "D", "report price printed in FCFA per unit (converted): not compared"
        else:
            ann = announcement_value(cell, cell.line, is_amount) if cell else None
            cat, why = classify(stored, report_raw, ann, cell.raw if cell else None, is_amount)
            if cat == "B":
                rec["proposed"] = f"{ann.normalize():f}"
            if ann is not None:
                rec["announcement_value"] = f"{ann.normalize():f}"
        rec["category"], rec["why"] = cat, why
        out[name] = rec
    return out


def run(session: Session, fetch: Fetcher, log: Callable[[str], None] = lambda _: None,
        store: bool = True) -> dict:
    """Cross-check every verified non-synthetic auction. Stores the announcements (SourceDocument
    + document store) when `store`; never writes to the auction table."""
    rows = session.execute(
        select(Auction, AuctionExtraction, SourceDocument)
        .join(AuctionExtraction, AuctionExtraction.promoted_auction_id == Auction.auction_id)
        .join(SourceDocument, SourceDocument.document_id == Auction.source_document_id)
        .where(Auction.is_synthetic.is_(False), Auction.verification_status == VerificationStatus.VERIFIED)
        .order_by(Auction.auction_date, Auction.auction_id)).all()
    report_urls = {d.url for _, _, d in rows}
    report_shas = set(session.scalars(select(SourceDocument.content_sha256).where(
        SourceDocument.document_type != DOCUMENT_TYPE)))
    found, dstats = discover(report_urls, {a.auction_date for a, _, _ in rows}, fetch, log)
    source = get_source(session) if store else None
    parsed: dict[str, tuple[Announcement | None, str | None, str | None]] = {}
    tranches_cache: dict[int, list[Tranche]] = {}
    results = []
    stats = {"auctions": len(rows), "report_documents": len(report_urls),
             "operations_found": len({o.page_url for o in found.values()}),
             "reports_without_operation_page": len(report_urls - set(found)),
             "operations_without_announcement": len({o.page_url for o in found.values() if not o.announcement_urls}),
             "announcements_downloaded": 0, "announcements_unparsed": 0,
             "announcement_links_serving_a_report": 0,
             "auctions_mapped": 0, "auctions_unmapped": 0, "auctions_without_announcement": 0,
             "operation_pages_opened": dstats["operation_pages_opened"], "page_errors": dstats["page_errors"]}
    for auction, ext, doc in rows:
        base = {"auction_id": auction.auction_id, "isin": auction.security.isin,
                "auction_date": auction.auction_date.isoformat(), "auction_type": auction.auction_type.value,
                "instrument": ext.instrument, "report_url": doc.url, "report_sha256": doc.content_sha256}
        op = found.get(doc.url)
        if op is None or not op.announcement_urls:
            stats["auctions_without_announcement"] += 1
            results.append({**base, "status": "no_announcement",
                            "operation_page": op.page_url if op else None})
            continue
        base["operation_page"] = op.page_url
        if doc.document_id not in tranches_cache:
            tranches_cache[doc.document_id] = report_tranches(session, doc.document_id)
        tranches = tranches_cache[doc.document_id]
        best = None
        for url in op.announcement_urls:
            if url not in parsed:
                got = fetch(url)
                if got.status != 200 or not got.content:
                    parsed[url] = (None, None, f"download failed: {got.error or got.status}")
                    continue
                stats["announcements_downloaded"] += 1
                sha = hashlib.sha256(got.content).hexdigest()
                text, ann = read_announcement(got.content)
                if len(text.strip()) < 40:
                    parsed[url] = (None, sha, "no text layer")
                    stats["announcements_unparsed"] += 1
                    continue
                if is_result_report(text) or sha in report_shas:
                    parsed[url] = (None, sha, "the 'Annonce' link serves a result report, not an announcement")
                    stats["announcement_links_serving_a_report"] += 1
                    continue
                if store:
                    sd, _ = save_document(session, source, url, got.content, got.content_type,
                                          f"UMOA-Titres — Annonce des résultats — {op.page_url.rstrip('/').rsplit('/', 1)[-1]}",
                                          DOCUMENT_TYPE)
                    if sd.url != url:
                        log(f"note: {url} has the bytes of document {sd.document_id} ({sd.url})")
                parsed[url] = (ann, sha, None if ann.blocks else "no results table recognised")
                if not ann.blocks:
                    stats["announcements_unparsed"] += 1
            ann, sha, err = parsed[url]
            if ann is None or not ann.blocks:
                best = best or {"announcement_url": url, "announcement_sha256": sha, "why": err}
                continue
            mapped, unmapped = map_columns(ann, tranches)
            if auction.security.isin in mapped:
                block, col, method = mapped[auction.security.isin]
                best = {"announcement_url": url, "announcement_sha256": sha, "mapping": method,
                        "column": col, "block_kind": block.kind,
                        "fields": compare_auction(auction, ext, block, col)}
                break
            best = {"announcement_url": url, "announcement_sha256": sha,
                    "why": unmapped.get(auction.security.isin, "security not in the announcement"),
                    "parse_errors": ann.errors[:5]}
        if best and "fields" in best:
            stats["auctions_mapped"] += 1
            results.append({**base, "status": "mapped", **best})
        else:
            stats["auctions_unmapped"] += 1
            results.append({**base, "status": "unmapped", **(best or {})})
    counts: dict[str, dict[str, int]] = {}
    for r in results:
        for name, rec in (r.get("fields") or {}).items():
            counts.setdefault(name, {"A": 0, "A2": 0, "B": 0, "C": 0, "D": 0})[rec["category"]] += 1
    stats["categories"] = counts
    stats["announcements"] = {u: {"sha256": s, "error": e, "blocks": len(a.blocks) if a else 0}
                              for u, (a, s, e) in parsed.items()}
    return {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "stats": stats, "auctions": results}


def proposals(report: dict) -> dict:
    """The versioned record: category B refinements (to apply) and category C discrepancies (for
    a human), each with its evidence."""
    ref, disc = [], []
    for r in report["auctions"]:
        for name, rec in (r.get("fields") or {}).items():
            if rec["category"] not in ("B", "C"):
                continue
            item = {"isin": r["isin"], "auction_date": r["auction_date"], "auction_type": r["auction_type"],
                    "field": name, "stored": rec["stored"], "report_url": r["report_url"],
                    "report_sha256": r["report_sha256"], "report_raw": rec["report_raw"],
                    "announcement_url": r["announcement_url"], "announcement_sha256": r["announcement_sha256"],
                    "announcement_raw": rec["announcement_raw"], "announcement_line": rec["announcement_line"],
                    "mapping": r["mapping"], "why": rec["why"]}
            if rec["category"] == "B":
                ref.append({**item, "proposed": rec["proposed"]})
            else:
                disc.append({**item, "announcement_value": rec.get("announcement_value"), "status": "flagged_for_human"})
    return {"description": "Cross-check of verified auctions against the official results announcements "
                           "(app.ingest.announcements). 'refinements' (category B: the report printed a rounded "
                           "value, the announcement the exact one) are applied by app.ingest.amend after "
                           "re-verification; 'discrepancies' (category C) are never changed automatically.",
            "generated_at": report["generated_at"], "stats": {k: v for k, v in report["stats"].items()
                                                               if k not in ("announcements", "page_errors")},
            "refinements": ref, "discrepancies": disc}


def main(argv: list[str] | None = None) -> int:
    from app.db import SessionLocal

    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--report", type=Path, required=True, help="full JSON report (every auction, every field)")
    p.add_argument("--data", type=Path, default=DATA_FILE, help="versioned record of B and C items")
    p.add_argument("--cache", type=Path, help="HTTP cache directory (re-runs do not hit the server)")
    p.add_argument("--no-store", action="store_true", help="do not store announcements as SourceDocument")
    args = p.parse_args(argv)
    fetch = PoliteFetcher(args.cache)
    with SessionLocal() as session:
        report = run(session, fetch, log=print, store=not args.no_store)
        session.commit()
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=1))
    args.data.write_text(json.dumps(proposals(report), ensure_ascii=False, indent=1) + "\n")
    s = report["stats"]
    print(json.dumps({k: v for k, v in s.items() if k not in ("announcements", "page_errors")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
