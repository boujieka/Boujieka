"""UMOA-Titres (WAEMU regional public-securities agency): fetch auction result reports.

Official pages (checked 2026-10-04):
  * listing  https://www.umoatitres.org/fr/emissions/  ("Annonces et résultats"): one table row
    per security of every completed operation ("Émissions réalisées"), each linking to the
    operation page /fr/emission/<slug>/.
  * operation page: characteristics, results summary and the operation's documents, each under
    a heading: "Avis d'appel d'offres", "Termes et conditions", "Note d'information",
    "Note de pré-émission", "Annonce", "Compte rendu".
  * The **"Compte rendu"** PDF (compte rendu d'adjudication) is the official result report;
    it is the document this module stores and extracts.

Run:
    python -m app.ingest.umoa --since 2026-07-01            # fetch + extract, newest first
    python -m app.ingest.umoa --limit 20 --refresh          # re-download known URLs too
    python -m app.ingest.umoa --reextract                   # re-parse stored documents (no network)

Idempotent: a URL already stored is not downloaded again (unless --refresh), identical bytes
are never stored twice (SHA-256), and re-extraction updates only rows still UNVERIFIED.
"""

import argparse
import hashlib
import html as htmllib
import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.ingest.pdf import extract_text
from app.ingest.umoa_extract import EXTRACTOR, ParsedDocument, parse_compte_rendu
from app.models import AuctionExtraction, Source, SourceDocument
from app.models.enums import DataNature, VerificationStatus
from app.watch.sources import USER_AGENT

SOURCE_NAME = "UMOA-Titres — auction calendar and results"
LISTING_URL = "https://www.umoatitres.org/fr/emissions/"
RESULT_LABEL = "compte rendu"
DOCUMENT_TYPES = {
    "compte rendu": "auction_result",
    "annonce": "result_announcement",
    "avis d'appel d'offres": "auction_notice",
    "termes et conditions": "terms_and_conditions",
    "note d'information": "information_note",
    "note de pre-emission": "pre_issue_note",
}
DATE_RE = re.compile(r"(\d{2})/(\d{2})/(\d{4})")
REQUEST_PAUSE_SECONDS = 0.5  # be polite to a public institution's server


@dataclass
class Fetched:
    status: int | None
    url: str
    content: bytes
    content_type: str | None
    error: str | None = None


def http_get(url: str, timeout: float = 60, retries: int = 3) -> Fetched:
    """GET with retries for transient errors. Honours HTTPS_PROXY and SSL_CERT_FILE."""
    last = None
    for attempt in range(retries):
        try:
            r = httpx.get(url, timeout=timeout, follow_redirects=True, headers={"User-Agent": USER_AGENT})
            return Fetched(r.status_code, str(r.url), r.content, r.headers.get("content-type"))
        except httpx.HTTPError as e:
            last = f"{type(e).__name__}: {e}"[:300]
            time.sleep(2 * (attempt + 1))
    return Fetched(None, url, b"", None, last)


Fetcher = Callable[[str], Fetched]


# --------------------------------------------------------------------------- page parsing


@dataclass
class Operation:
    """One completed auction operation as listed on the official listing page."""

    url: str
    issuer: str
    operation_date: date | None
    instruments: list[str] = field(default_factory=list)


@dataclass
class DocumentLink:
    label: str
    url: str
    document_type: str


def _fold(text: str) -> str:
    import unicodedata

    text = text.replace("’", "'").replace("\xa0", " ")
    text = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    return " ".join(text.split()).lower()


def _date(text: str) -> date | None:
    m = DATE_RE.search(text)
    if not m:
        return None
    try:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None


class _TableParser(HTMLParser):
    """Rows (cell texts + links) of the table with the given id."""

    def __init__(self, table_id: str) -> None:
        super().__init__(convert_charrefs=True)
        self.table_id = table_id
        self.depth = 0  # >0 while inside the target table
        self.rows: list[tuple[list[str], list[str]]] = []
        self._cells: list[str] | None = None
        self._links: list[str] = []
        self._cell: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            if self.depth:
                self.depth += 1
            elif a.get("id") == self.table_id:
                self.depth = 1
        if not self.depth:
            return
        if tag == "tr":
            self._cells, self._links = [], []
        elif tag == "td" and self._cells is not None:
            self._cell = []
        elif tag == "br" and self._cell is not None:
            self._cell.append(" | ")
        elif tag == "a" and self._cells is not None and a.get("href"):
            self._links.append(a["href"])

    def handle_endtag(self, tag):
        if not self.depth:
            return
        if tag == "td" and self._cell is not None and self._cells is not None:
            self._cells.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._cells is not None:
            if self._cells:
                self.rows.append((self._cells, self._links))
            self._cells = None
        elif tag == "table":
            self.depth -= 1

    def handle_data(self, data):
        if self.depth and self._cell is not None:
            self._cell.append(data)


def parse_listing(html: str, base_url: str = LISTING_URL) -> list[Operation]:
    """Completed operations from the "Émissions réalisées" table, one per operation page."""
    p = _TableParser("emission-hub-passees-par")
    p.feed(html)
    ops: dict[str, Operation] = {}
    for cells, links in p.rows:
        url = next((urljoin(base_url, h) for h in links if "/emission/" in h), None)
        if url is None or len(cells) < 6:
            continue
        op = ops.get(url)
        if op is None:
            issuer = cells[0].split(" | ")[0].strip()
            op = ops[url] = Operation(url=url, issuer=issuer, operation_date=_date(cells[3]))
        if cells[1] and cells[1] not in op.instruments:
            op.instruments.append(cells[1])
    return list(ops.values())


def parse_operation_page(html: str, base_url: str) -> list[DocumentLink]:
    """Document links of an operation page, labelled by the heading above each button."""
    out: list[DocumentLink] = []
    label = None
    for m in re.finditer(r"<h3[^>]*>(.*?)</h3>|href=['\"]([^'\"]+\.pdf)['\"]", html, re.S | re.I):
        if m.group(1) is not None:
            label = _fold(htmllib.unescape(re.sub(r"<[^>]+>", "", m.group(1))))
        elif label in DOCUMENT_TYPES:
            out.append(DocumentLink(label, urljoin(base_url, m.group(2)), DOCUMENT_TYPES[label]))
    return out


# --------------------------------------------------------------------------- storage


def get_source(session: Session) -> Source:
    source = session.scalar(select(Source).where(Source.name == SOURCE_NAME))
    if source is None:
        raise RuntimeError(f"Source {SOURCE_NAME!r} not found: run `python -m app.seed.load` first")
    return source


def store_bytes(sha: str, content: bytes, suffix: str, text: str | None = None) -> str:
    """Write to the document store (content-addressed). Returns the stored path."""
    root = Path(get_settings().document_store_dir)
    folder = root / sha[:2]
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{sha}{suffix}"
    if not path.exists():
        path.write_bytes(content)
    if text is not None:
        (folder / f"{sha}.txt").write_text(text, encoding="utf-8")
    return str(path)


def save_document(
    session: Session,
    source: Source,
    url: str,
    content: bytes,
    content_type: str | None,
    title: str,
    document_type: str,
    retrieved_at: datetime | None = None,
) -> tuple[SourceDocument, bool]:
    """Store a retrieved document once per content hash. Returns (document, created)."""
    sha = hashlib.sha256(content).hexdigest()
    existing = session.scalar(select(SourceDocument).where(SourceDocument.content_sha256 == sha))
    if existing is not None:
        return existing, False
    suffix = ".pdf" if content[:5] == b"%PDF-" else ".bin"
    doc = SourceDocument(
        source_id=source.source_id,
        url=url,
        title=title[:512],
        document_type=document_type,
        retrieved_at=retrieved_at or datetime.now(timezone.utc),
        content_sha256=sha,
        mime_type=(content_type or "").split(";")[0] or None,
        storage_path=store_bytes(sha, content, suffix),
        extraction_status="not_started",
        is_synthetic=False,
    )
    session.add(doc)
    session.flush()
    return doc, True


# --------------------------------------------------------------------------- extraction → staging


def extract_document(session: Session, doc: SourceDocument, content: bytes) -> list[AuctionExtraction]:
    """Parse one result report into staging rows (UNVERIFIED). Reviewed rows are never touched."""
    pdf = extract_text(content)
    if not pdf.has_text:
        doc.extraction_status = "needs_ocr" if pdf.method != "none" else "failed"
        return []
    if doc.storage_path:
        store_bytes(doc.content_sha256 or "", content, Path(doc.storage_path).suffix, pdf.text)
    parsed = parse_compte_rendu(pdf.text)
    if not parsed.tranches:
        doc.extraction_status = "failed"
        return []
    if parsed.publication_date:
        doc.publication_date = parsed.publication_date
    rows = [_upsert_extraction(session, doc, parsed, t) for t in parsed.tranches]
    doc.extraction_status = (
        "complete" if all(t.parse_status == "complete" for t in parsed.tranches) else "partial"
    )
    session.flush()
    return [r for r in rows if r is not None]


def _upsert_extraction(session: Session, doc: SourceDocument, parsed: ParsedDocument, t) -> AuctionExtraction | None:
    row = session.scalar(
        select(AuctionExtraction).where(
            AuctionExtraction.source_document_id == doc.document_id,
            AuctionExtraction.tranche_key == t.tranche_key,
        )
    )
    if row is not None and row.verification_status != VerificationStatus.UNVERIFIED:
        return None  # a human already decided on this row; keep it as reviewed
    if row is None:
        row = AuctionExtraction(source_document_id=doc.document_id, tranche_key=t.tranche_key)
        session.add(row)
    auction_date = t.value("auction_date")
    row.extractor = EXTRACTOR
    row.parse_status = t.parse_status
    country = (t.operation or parsed.operation).get("country_iso3")
    row.country_iso3 = country.value if country else None
    row.isin = t.value("isin")
    row.instrument = t.value("instrument")
    row.auction_date = date.fromisoformat(auction_date) if auction_date else None
    row.fields = {k: f.as_dict() for k, f in t.fields.items()}
    row.field_status = dict(t.field_status)
    op = t.operation or parsed.operation
    row.operation = {"layout": parsed.layout, "operation_kind": t.kind,
                     "tranche_count": t.operation_tranches,
                     **{k: f.as_dict() for k, f in op.items()}}
    row.warnings = list(parsed.warnings) + list(t.errors)
    row.checks = list(parsed.checks)
    row.source_id = doc.source_id
    row.source_url = doc.url
    row.publication_date = doc.publication_date
    row.extracted_at = datetime.now(timezone.utc)
    row.data_nature = DataNature.FACT
    row.verification_status = VerificationStatus.UNVERIFIED
    row.is_synthetic = False
    row.confidence_score = Decimal(str(t.confidence))
    row.provenance_notes = (
        f"Extracted by {EXTRACTOR} from '{doc.title}'. UNVERIFIED: awaiting human review."
    )
    return row


# --------------------------------------------------------------------------- orchestration


def run(
    session: Session,
    since: date | None = None,
    until: date | None = None,
    limit: int | None = None,
    refresh: bool = False,
    fetch: Fetcher = http_get,
    pause: float = REQUEST_PAUSE_SECONDS,
    log: Callable[[str], None] = lambda _: None,
) -> dict:
    """Fetch the listing, then each operation's result report; store and extract."""
    source = get_source(session)
    stats = {"operations_listed": 0, "operations_selected": 0, "operations_without_result": 0,
             "documents_found": 0, "documents_downloaded": 0, "documents_new": 0,
             "documents_skipped_known_url": 0, "fetch_errors": 0, "extractions": 0,
             "documents_complete": 0, "documents_partial": 0, "documents_failed": 0,
             "documents_needs_ocr": 0, "errors": []}
    now = datetime.now(timezone.utc)
    source.last_checked_at = now
    res = fetch(LISTING_URL)
    if res.status != 200 or not res.content:
        source.last_error = f"listing: {res.error or f'HTTP {res.status}'}"
        stats["errors"].append(source.last_error)
        return stats
    ops = parse_listing(res.content.decode("utf-8", errors="replace"), res.url)
    stats["operations_listed"] = len(ops)
    ops = [o for o in ops if o.operation_date and (not since or o.operation_date >= since)
           and (not until or o.operation_date <= until)]
    ops.sort(key=lambda o: (o.operation_date, o.url), reverse=True)
    ops = ops[:limit] if limit else ops
    stats["operations_selected"] = len(ops)

    for op in ops:
        time.sleep(pause)
        page = fetch(op.url)
        if page.status != 200:
            stats["fetch_errors"] += 1
            stats["errors"].append(f"{op.url}: {page.error or f'HTTP {page.status}'}")
            continue
        links = [d for d in parse_operation_page(page.content.decode("utf-8", errors="replace"), page.url)
                 if d.label == RESULT_LABEL]
        if not links:
            stats["operations_without_result"] += 1
            continue
        for link in links:
            stats["documents_found"] += 1
            known = session.scalar(select(SourceDocument).where(SourceDocument.url == link.url))
            if known is not None and not refresh:
                stats["documents_skipped_known_url"] += 1
                continue
            time.sleep(pause)
            got = fetch(link.url)
            if got.status != 200 or not got.content:
                stats["fetch_errors"] += 1
                stats["errors"].append(f"{link.url}: {got.error or f'HTTP {got.status}'}")
                continue
            stats["documents_downloaded"] += 1
            title = f"UMOA-Titres — Compte rendu d'adjudication — {op.issuer} — {op.operation_date}"
            doc, created = save_document(session, source, link.url, got.content, got.content_type,
                                         title, link.document_type)
            stats["documents_new"] += int(created)
            if created or refresh:
                try:
                    with session.begin_nested():
                        rows = extract_document(session, doc, got.content)
                except Exception as e:  # a parser bug must not stop the run; keep the document
                    doc.extraction_status = "failed"
                    rows = []
                    stats["errors"].append(f"{link.url}: extraction error {type(e).__name__}: {e}"[:300])
                stats["extractions"] += len(rows)
                key = f"documents_{doc.extraction_status}"
                if key in stats:
                    stats[key] += 1
                log(f"{op.operation_date} {op.issuer}: {doc.extraction_status}, {len(rows)} tranche(s)")
    source.last_success_at = now
    source.last_error = None
    session.flush()
    return stats


def reextract(session: Session, log: Callable[[str], None] = lambda _: None) -> dict:
    """Re-run extraction on stored documents (after a parser change). No network access.
    Rows a reviewer already decided on are left untouched."""
    source = get_source(session)
    stats = {"documents": 0, "extractions": 0, "missing_file": 0}
    docs = session.scalars(select(SourceDocument).where(
        SourceDocument.source_id == source.source_id,
        SourceDocument.document_type == "auction_result")).all()
    for doc in docs:
        path = Path(doc.storage_path or "")
        if not path.is_file():
            stats["missing_file"] += 1
            continue
        rows = extract_document(session, doc, path.read_bytes())
        stats["documents"] += 1
        stats["extractions"] += len(rows)
        key = f"documents_{doc.extraction_status}"
        stats[key] = stats.get(key, 0) + 1
        log(f"{doc.title}: {doc.extraction_status}, {len(rows)} tranche(s)")
    return stats


def main() -> None:
    from app.db import SessionLocal

    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--since", type=date.fromisoformat)
    parser.add_argument("--until", type=date.fromisoformat)
    parser.add_argument("--limit", type=int, help="newest N operations only")
    parser.add_argument("--refresh", action="store_true", help="re-download URLs already stored")
    parser.add_argument("--reextract", action="store_true",
                        help="re-parse documents already stored (no network); for parser upgrades")
    args = parser.parse_args()
    with SessionLocal() as session:
        if args.reextract:
            stats = reextract(session, log=print)
        else:
            stats = run(session, args.since, args.until, args.limit, args.refresh, log=print)
        session.commit()
    errors = stats.pop("errors", [])
    for k, v in stats.items():
        print(f"{k}: {v}")
    for e in errors[:20]:
        print("error:", e)


if __name__ == "__main__":
    main()
