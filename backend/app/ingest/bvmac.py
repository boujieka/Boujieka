"""BVMAC (Bourse des Valeurs Mobilières de l'Afrique Centrale): fetch the daily Bulletin officiel
de la cote (BOC) and stage its bond lines.

Official listing (checked 2026-10-04): https://www.bvm-ac.org/bulletin-officiel-de-la-cote-boc/
— one link per trading session, labelled "BOC Séance de cotation du <d> <mois> <yyyy>", pointing to
a text PDF (current pattern wp-content/uploads/YYYY/MM/BOC-YYYYMMDD.pdf; older
BOC-BVMAC-DD-MM-YY(YY).pdf and variants). The owner holds BVMAC's written authorisation to publish
these data free of charge (no resale); every stored row keeps its source attribution.

Pipeline: listing → select by session date (--since/--until/--limit) → polite download (one
request at a time, >= 1 s apart, User-Agent below) → SourceDocument (deduplicated by SHA-256,
bytes + -layout text in the document store) → app.ingest.bvmac_extract (parser "bvmac_boc/1")
→ staging table `bvmac_quote`, UNVERIFIED. Nothing is promoted here: app.ingest.bvmac_check runs
the strict checks and promotes.

    python -m app.ingest.bvmac --since 2024-01-01            # fetch + stage
    python -m app.ingest.bvmac --since 2024-01-01 --check    # … then run the strict checks
    python -m app.ingest.bvmac --reextract                   # re-parse stored documents (no network)

Idempotent: a URL already stored is not downloaded again (unless --refresh), identical bytes are
stored once, and re-extraction only rewrites rows that are still UNVERIFIED.
"""

import argparse
import hashlib
import html as htmllib
import re
import time
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingest.bvmac_extract import EXTRACTOR, REQUIRED_QUOTE_FIELDS, ParsedBoc, parse
from app.ingest.pdf import extract_text
from app.ingest.umoa import Fetched, save_document, store_bytes
from app.models import BvmacQuote, Source, SourceDocument
from app.models.enums import DataNature, SourceCategory, SourceStatus, VerificationStatus

SOURCE_NAME = "BVMAC — Bulletin officiel de la cote"
INSTITUTION = "BVMAC"  # Bourse des Valeurs Mobilières de l'Afrique Centrale (site/build.py maps it to CEMAC)
LISTING_URL = "https://www.bvm-ac.org/bulletin-officiel-de-la-cote-boc/"
USER_AGENT = "CartoucheIngest/1.0 (https://cartouche-africa.netlify.app)"
DOCUMENT_TYPE = "price_list"
REQUEST_PAUSE_SECONDS = 1.2  # >= 1 s between requests to the exchange's server
ATTRIBUTION = ("Source: BVMAC, Bulletin officiel de la cote. Published free of charge with the "
               "written authorisation of the BVMAC (no resale).")
MONTHS = {"janvier": 1, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7,
          "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11, "decembre": 12}


def http_get(url: str, timeout: float = 90, retries: int = 3) -> Fetched:
    """GET with retries for transient errors. Honours HTTPS_PROXY and SSL_CERT_FILE."""
    last = None
    for attempt in range(retries):
        try:
            r = httpx.get(url, timeout=timeout, follow_redirects=True, headers={"User-Agent": USER_AGENT})
            return Fetched(r.status_code, str(r.url), r.content, r.headers.get("content-type"))
        except httpx.HTTPError as e:
            last = f"{type(e).__name__}: {e}"[:300]
            time.sleep(3 * (attempt + 1))
    return Fetched(None, url, b"", None, last)


Fetcher = Callable[[str], Fetched]


# --------------------------------------------------------------------------- listing


@dataclass
class BocLink:
    url: str
    label: str
    session_date: date | None  # from the link label (cross-checked against the PDF header)


def _fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return " ".join("".join(c for c in s if not unicodedata.combining(c)).lower().split())


def label_date(label: str) -> date | None:
    """'BOC Séance de cotation du 01 octobre 2026' -> 2026-10-01 (None if not in that form)."""
    m = re.search(r"du\s+(\d{1,2})\s*(?:er)?\s+([a-z]+)\s+(\d{4})", _fold(label))
    if not m or m[2] not in MONTHS:
        return None
    try:
        return date(int(m[3]), MONTHS[m[2]], int(m[1]))
    except ValueError:
        return None


def parse_listing(html: str) -> tuple[list[BocLink], list[str]]:
    """BOC links of the listing page, and the hrefs skipped as malformed (never repaired)."""
    links, skipped, seen = [], [], set()
    for href, inner in re.findall(r'<a[^>]+href="([^"]+\.pdf)"[^>]*>(.*?)</a>', html, re.S | re.I):
        href = htmllib.unescape(href).strip()
        label = " ".join(htmllib.unescape(re.sub(r"<[^>]+>", "", inner)).split())
        if "BOC" not in href.upper() and "BOC" not in label.upper():
            continue
        if not re.match(r"^https://www\.bvm-ac\.org/wp-content/uploads/", href):
            skipped.append(href)
            continue
        if href in seen:
            continue
        seen.add(href)
        links.append(BocLink(href, label, label_date(label)))
    return links, skipped


# --------------------------------------------------------------------------- storage


def get_or_create_source(session: Session) -> Source:
    source = session.scalar(select(Source).where(Source.name == SOURCE_NAME))
    if source is None:
        source = Source(name=SOURCE_NAME, institution=INSTITUTION, category=SourceCategory.STOCK_EXCHANGE,
                        country_id=None, base_url=LISTING_URL, status=SourceStatus.ACTIVE,
                        crawl_config={"listing": LISTING_URL, "parser": EXTRACTOR, "zone": "CEMAC"},
                        notes=("Regional (CEMAC) stock exchange; daily official price list. " + ATTRIBUTION))
        session.add(source)
        session.flush()
    return source


def stage(session: Session, doc: SourceDocument, parsed: ParsedBoc, link_date: date | None,
          link_label: str | None) -> list[BvmacQuote]:
    """Write one UNVERIFIED staging row per bond line. Rows already decided on are not touched."""
    rows = []
    for isin, q in parsed.quotes.items():
        row = session.scalar(select(BvmacQuote).where(BvmacQuote.source_document_id == doc.document_id,
                                                      BvmacQuote.isin == isin))
        if row is not None and row.verification_status != VerificationStatus.UNVERIFIED:
            continue
        if row is None:
            row = BvmacQuote(source_document_id=doc.document_id, isin=isin)
            session.add(row)
        c = parsed.characteristics.get(isin)
        fields = {k: v.as_dict() for k, v in q.fields.items()}
        if c is not None:
            fields.update({f"char_{k}": v.as_dict() for k, v in c.fields.items()})
        if link_label is not None:
            fields["listing_label"] = {"value": link_date.isoformat() if link_date else None,
                                       "raw": link_label, "locator": f"listing {LISTING_URL}"}
        errors = list(q.errors) + [f"characteristics: {e}" for e in (c.errors if c else [])]
        if c is None:
            errors.append("characteristics: ISIN not found in the 'LIGNES OBLIGATAIRES' table")
        vt = q.v("volume_traded")
        row.extractor = EXTRACTOR
        row.session_date = parsed.session_date
        row.boc_number = parsed.boc_number
        row.mnemo = q.v("mnemo")
        row.section = q.section
        row.issuer_name = q.issuer
        row.security_name = q.name
        row.country_iso3 = q.country_iso3 or None
        complete = not q.errors and all(n in q.fields for n in REQUIRED_QUOTE_FIELDS) and q.issuer and q.name
        row.parse_status = "complete" if complete else "partial"
        row.traded = None if vt is None else vt > 0
        row.fields = fields
        row.raw_line = q.line
        row.errors = errors
        row.notes = "; ".join(q.notes) or None
        row.field_status = {}
        row.source_id = doc.source_id
        row.source_url = doc.url
        row.publication_date = parsed.session_date
        row.extracted_at = datetime.now(timezone.utc)
        row.data_nature = DataNature.FACT
        row.verification_status = VerificationStatus.UNVERIFIED
        row.is_synthetic = False
        row.confidence_score = Decimal("1") if complete else Decimal("0")
        row.provenance_notes = (f"Extracted by {EXTRACTOR} from '{doc.title}' ({doc.url}, sha256 "
                                f"{doc.content_sha256}). UNVERIFIED until app.ingest.bvmac_check passes. "
                                + ATTRIBUTION)
        rows.append(row)
    session.flush()
    return rows


def extract_document(session: Session, doc: SourceDocument, content: bytes,
                     link: BocLink | None = None) -> list[BvmacQuote]:
    pdf = extract_text(content)
    if not pdf.has_text:
        doc.extraction_status = "needs_ocr" if pdf.method != "none" else "failed"
        return []
    if doc.storage_path and doc.content_sha256:
        store_bytes(doc.content_sha256, content, Path(doc.storage_path).suffix, pdf.text)
    parsed = parse(pdf.text, "layout")
    if parsed.session_date:
        doc.publication_date = parsed.session_date
    if parsed.layout != EXTRACTOR:
        doc.extraction_status = "unsupported_layout"
        return []
    label = link.label if link else _stored_label(session, doc)
    ldate = link.session_date if link else label_date(label or "")
    rows = stage(session, doc, parsed, ldate, label)
    every = session.scalars(select(BvmacQuote).where(BvmacQuote.source_document_id == doc.document_id)).all()
    doc.extraction_status = "complete" if every and all(r.parse_status == "complete" for r in every) else (
        "partial" if every else "failed")
    return rows


def _stored_label(session: Session, doc: SourceDocument) -> str | None:
    """The listing label recorded at first extraction (re-extraction runs without the listing)."""
    row = session.scalar(select(BvmacQuote).where(BvmacQuote.source_document_id == doc.document_id).limit(1))
    return ((row.fields or {}).get("listing_label") or {}).get("raw") if row else None


# --------------------------------------------------------------------------- orchestration


def run(session: Session, since: date | None = None, until: date | None = None, limit: int | None = None,
        refresh: bool = False, fetch: Fetcher = http_get, pause: float = REQUEST_PAUSE_SECONDS,
        log: Callable[[str], None] = lambda _: None, commit: bool = False) -> dict:
    """Fetch the listing and the selected BOCs; store and stage them. With commit=True (the CLI)
    each document is committed as soon as it is staged, so an interrupted run keeps its work."""
    source = get_or_create_source(session)
    stats = {"links_listed": 0, "links_malformed": 0, "links_without_date": 0, "selected": 0,
             "skipped_known_url": 0, "downloaded": 0, "documents_new": 0, "duplicate_content": 0,
             "fetch_errors": 0, "rows_staged": 0, "documents_complete": 0, "documents_partial": 0,
             "documents_failed": 0, "documents_unsupported_layout": 0, "documents_needs_ocr": 0,
             "errors": []}
    now = datetime.now(timezone.utc)
    source.last_checked_at = now
    res = fetch(LISTING_URL)
    if res.status != 200 or not res.content:
        source.last_error = f"listing: {res.error or f'HTTP {res.status}'}"
        stats["errors"].append(source.last_error)
        return stats
    links, malformed = parse_listing(res.content.decode("utf-8", errors="replace"))
    stats["links_listed"], stats["links_malformed"] = len(links), len(malformed)
    stats["errors"] += [f"malformed link skipped: {h}" for h in malformed]
    undated = [lk for lk in links if lk.session_date is None]
    stats["links_without_date"] = len(undated)
    stats["errors"] += [f"no session date in label {lk.label!r}: {lk.url}" for lk in undated]
    links = [lk for lk in links if lk.session_date and (not since or lk.session_date >= since)
             and (not until or lk.session_date <= until)]
    links.sort(key=lambda lk: (lk.session_date, lk.url), reverse=True)
    links = links[:limit] if limit else links
    stats["selected"] = len(links)
    for lk in links:
        known = session.scalar(select(SourceDocument).where(SourceDocument.url == lk.url))
        if known is not None and not refresh:
            stats["skipped_known_url"] += 1
            continue
        time.sleep(pause)
        got = fetch(lk.url)
        if got.status != 200 or not got.content:
            stats["fetch_errors"] += 1
            stats["errors"].append(f"{lk.url}: {got.error or f'HTTP {got.status}'}")
            continue
        stats["downloaded"] += 1
        title = f"BVMAC — Bulletin officiel de la cote — séance du {lk.session_date.isoformat()}"
        doc, created = save_document(session, source, lk.url, got.content, got.content_type, title, DOCUMENT_TYPE)
        stats["documents_new"] += int(created)
        if not created and doc.url != lk.url:
            stats["duplicate_content"] += 1
            stats["errors"].append(f"{lk.url}: same bytes as {doc.url} (stored once)")
            continue
        try:
            with session.begin_nested():
                rows = extract_document(session, doc, got.content, lk)
        except Exception as e:  # a parser bug must not stop the run; keep the document
            doc.extraction_status = "failed"
            rows = []
            stats["errors"].append(f"{lk.url}: extraction error {type(e).__name__}: {e}"[:300])
        stats["rows_staged"] += len(rows)
        key = f"documents_{doc.extraction_status}"
        stats[key] = stats.get(key, 0) + 1
        log(f"{lk.session_date} {lk.url.rsplit('/', 1)[-1]}: {doc.extraction_status}, {len(rows)} bond line(s)")
        if commit:
            session.commit()
    source.last_success_at = now
    source.last_error = None
    session.flush()
    return stats


def reextract(session: Session, log: Callable[[str], None] = lambda _: None) -> dict:
    """Re-parse stored documents (after a parser change). No network. Decided rows are kept."""
    source = get_or_create_source(session)
    stats: dict = {"documents": 0, "rows": 0, "missing_file": 0}
    for doc in session.scalars(select(SourceDocument).where(SourceDocument.source_id == source.source_id)):
        path = Path(doc.storage_path or "")
        if not path.is_file():
            stats["missing_file"] += 1
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != doc.content_sha256:
            stats.setdefault("hash_mismatch", 0)
            stats["hash_mismatch"] += 1
            continue
        rows = extract_document(session, doc, path.read_bytes())
        stats["documents"] += 1
        stats["rows"] += len(rows)
        key = f"documents_{doc.extraction_status}"
        stats[key] = stats.get(key, 0) + 1
        log(f"{doc.title}: {doc.extraction_status}, {len(rows)} bond line(s)")
    return stats


def main() -> None:
    from app.db import SessionLocal

    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--since", type=date.fromisoformat, help="first session date (inclusive)")
    p.add_argument("--until", type=date.fromisoformat, help="last session date (inclusive)")
    p.add_argument("--limit", type=int, help="newest N sessions only")
    p.add_argument("--refresh", action="store_true", help="re-download URLs already stored")
    p.add_argument("--reextract", action="store_true", help="re-parse stored documents (no network)")
    p.add_argument("--check", action="store_true", help="then run app.ingest.bvmac_check (strict checks + promotion)")
    args = p.parse_args()
    with SessionLocal() as session:
        stats = reextract(session, log=print) if args.reextract else run(
            session, args.since, args.until, args.limit, args.refresh, log=print, commit=True)
        session.commit()
        errors = stats.pop("errors", [])
        for k, v in stats.items():
            print(f"{k}: {v}")
        for e in errors[:40]:
            print("note:", e)
        if args.check:
            from app.ingest import bvmac_check

            report = bvmac_check.run(session, log=print, commit=True)
            session.commit()
            print(bvmac_check.summary(report))


if __name__ == "__main__":
    main()
