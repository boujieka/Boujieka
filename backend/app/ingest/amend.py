"""Refine verified auctions whose result report printed a ROUNDED value (category B only).

Input: the versioned record data/announcement_cross_check.json written by
app.ingest.announcements. Each refinement names an auction (ISIN, date, type), a field, the value
stored from the result report, the exact value printed in the official results announcement of
the same operation, and the evidence. Before anything is written, for each refinement:

  * the auction exists, is VERIFIED and non-synthetic, and its source document is the result
    report named in the record (same URL and SHA-256);
  * the result report's bytes (document store, or a re-download) have that SHA-256 and its text
    prints the rounded value the record quotes (`report_raw`);
  * the announcement is re-downloaded: its SHA-256 equals the record's and, when the database
    already holds it as a SourceDocument, that document's hash; the quoted table line is printed
    in its text and contains the exact value (`announcement_raw`), which equals `proposed`;
  * the rounding relation is re-checked: the stored value equals the exact value rounded to the
    precision the report printed;
  * the stored value is still the one the record saw (`stored`).

If any check fails, that refinement is not applied (fail closed). Category C discrepancies in the
same file are never touched. data_nature stays FACT and verification_status VERIFIED. A note is
appended to provenance_notes. Idempotent: an auction already carrying the exact value and the
note is skipped.

    python -m app.ingest.amend               # dry run: verify evidence, report
    python -m app.ingest.amend --apply
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingest.announcements import (
    AMOUNT_FIELDS,
    DATA_FILE,
    DOCUMENT_TYPE,
    FIELDS,
    PoliteFetcher,
    _fold,
    classify,
    document_text,
    french_number,
    split_values,
    unit_of,
)
from app.ingest.umoa import get_source, save_document
from app.models import Auction, Security, SourceDocument
from app.models.enums import AuctionType, DataNature, VerificationStatus


def _flat(s: str) -> str:
    return re.sub(r"\s+", " ", _fold(s))


def _digits_only(s: str) -> str:
    return re.sub(r"\s", "", _fold(s))


def note_for(r: dict, today: str) -> str:
    return (f"{r['field']} refined from {r['stored']} to {r['proposed']} on {today}: exact figure printed in "
            f"{r['announcement_url']} (sha256 {r['announcement_sha256']}); the result report printed the "
            f"rounded value '{r['report_raw']}'")


def _marker(r: dict) -> str:
    """Date-independent part of the note, used to detect an earlier application."""
    return f"{r['field']} refined from {r['stored']} to {r['proposed']} on "


class Evidence:
    def __init__(self, fetch=None) -> None:
        self.fetch = fetch or PoliteFetcher()
        self.cache: dict[str, tuple[bytes | None, str | None]] = {}

    def get(self, url: str) -> tuple[bytes | None, str | None]:
        """(bytes, error). Always downloaded again (never from a cache on disk)."""
        if url not in self.cache:
            try:
                got = self.fetch(url, use_cache=False) if isinstance(self.fetch, PoliteFetcher) else self.fetch(url)
            except Exception as e:  # network error: fail closed
                self.cache[url] = (None, f"download failed: {type(e).__name__}")
            else:
                ok = got.status == 200 and got.content
                self.cache[url] = (got.content if ok else None, None if ok else f"download failed: {got.error or got.status}")
        return self.cache[url]


def verify(session: Session, r: dict, ev: Evidence) -> tuple[Auction | None, str | None, bytes | None]:
    """(auction, None, announcement bytes) when every check holds, else (auction?, reason, None)."""
    if r.get("field") not in FIELDS:
        return None, f"field {r.get('field')!r} cannot be refined", None
    auction = session.scalar(
        select(Auction).join(Security).where(
            Security.isin == r["isin"], Auction.auction_date == date.fromisoformat(r["auction_date"]),
            Auction.auction_type == AuctionType(r["auction_type"])))
    if auction is None:
        return None, "auction not found", None
    if auction.is_synthetic or auction.verification_status != VerificationStatus.VERIFIED \
            or auction.data_nature != DataNature.FACT:
        return auction, "auction is not a verified non-synthetic FACT", None
    report = session.get(SourceDocument, auction.source_document_id) if auction.source_document_id else None
    if report is None or report.url != r["report_url"] or report.content_sha256 != r["report_sha256"]:
        return auction, "the auction's source document is not the result report of the record", None
    # The report prints the rounded value quoted in the record.
    content = None
    if report.storage_path and Path(report.storage_path).is_file():
        content = Path(report.storage_path).read_bytes()
    if content is None or hashlib.sha256(content).hexdigest() != report.content_sha256:
        content, err = ev.get(report.url)
        if content is None:
            return auction, f"result report: {err}", None
    if hashlib.sha256(content).hexdigest() != r["report_sha256"]:
        return auction, "result report SHA-256 mismatch", None
    rtext = document_text(content)
    if not r.get("report_raw") or _flat(r["report_raw"].split(" millions")[0].split("%")[0]) not in _flat(rtext):
        return auction, f"rounded value {r.get('report_raw')!r} not printed in the result report", None
    # The announcement, downloaded again.
    if not r["announcement_url"].startswith("https://www.umoatitres.org/"):
        return auction, "announcement URL not on umoatitres.org", None
    ann_bytes, err = ev.get(r["announcement_url"])
    if ann_bytes is None:
        return auction, f"announcement: {err}", None
    sha = hashlib.sha256(ann_bytes).hexdigest()
    if sha != r["announcement_sha256"]:
        return auction, "announcement SHA-256 differs from the record", None
    stored_doc = session.scalar(select(SourceDocument).where(SourceDocument.content_sha256 == sha))
    if stored_doc is not None and stored_doc.url != r["announcement_url"]:
        return auction, f"announcement bytes stored under another URL ({stored_doc.url})", None
    same_url = session.scalars(select(SourceDocument).where(SourceDocument.url == r["announcement_url"],
                                                            SourceDocument.document_type == DOCUMENT_TYPE)).all()
    if any(d.content_sha256 != sha for d in same_url):
        return auction, "announcement SHA-256 differs from the stored SourceDocument", None
    atext = document_text(ann_bytes)
    line = r.get("announcement_line") or ""
    if not line or _flat(line) not in _flat(atext):
        return auction, "quoted announcement line not printed in the announcement", None
    raw = r.get("announcement_raw") or ""
    label_end = re.search(r"(?<![A-Za-z(])[\d-]", line)
    cells, ok = split_values(line[label_end.start():]) if label_end else ([], False)
    if not ok or raw not in cells:
        return auction, f"exact value {raw!r} is not a cell of the quoted line", None
    is_amount = r["field"] in AMOUNT_FIELDS
    exact = french_number(raw)
    if exact is None:
        return auction, f"exact value {raw!r} is not a number", None
    if is_amount:
        exact *= unit_of(line.split(raw)[0])
    if exact != Decimal(r["proposed"]):
        return auction, f"announcement prints {exact} but the record proposes {r['proposed']}", None
    # Current value and the rounding relation.
    current = getattr(auction, r["field"])
    current = None if current is None else Decimal(current)
    if current == exact and _marker(r) in (auction.provenance_notes or ""):
        return auction, "already applied", None
    if current != Decimal(r["stored"]):
        return auction, f"stored value is now {current}, not {r['stored']} as recorded", None
    cat, why = classify(current, r["report_raw"], exact, raw, is_amount)
    if cat != "B":
        return auction, f"rounding relation does not hold ({cat}: {why})", None
    return auction, None, ann_bytes


def apply(session: Session, data: dict, do_apply: bool, fetch=None, today: str | None = None,
          commit: bool = True) -> dict:
    today = today or datetime.now(timezone.utc).date().isoformat()
    ev = Evidence(fetch)
    report = {"refinements": len(data.get("refinements", [])), "verified": 0, "applied": 0,
              "already_applied": 0, "failed": [], "discrepancies_untouched": len(data.get("discrepancies", []))}
    source = None
    for r in data.get("refinements", []):
        auction, why, ann_bytes = verify(session, r, ev)
        key = f"{r.get('isin')} {r.get('auction_date')} {r.get('field')}"
        if why == "already applied":
            report["already_applied"] += 1
            continue
        if why:
            report["failed"].append({"refinement": key, "why": why})
            continue
        report["verified"] += 1
        if not do_apply:
            continue
        if session.scalar(select(SourceDocument).where(
                SourceDocument.content_sha256 == r["announcement_sha256"])) is None:
            source = source or get_source(session)
            save_document(session, source, r["announcement_url"], ann_bytes, "application/pdf",
                          "UMOA-Titres — Annonce des résultats (cross-check)", DOCUMENT_TYPE)
        setattr(auction, r["field"], Decimal(r["proposed"]))
        note = note_for(r, today)
        auction.provenance_notes = f"{auction.provenance_notes} {note}." if auction.provenance_notes else f"{note}."
        session.flush()
        report["applied"] += 1
    if do_apply and commit:
        session.commit()
    return report


def main(argv: list[str] | None = None) -> int:
    from app.db import SessionLocal

    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--apply", action="store_true")
    p.add_argument("--file", type=Path, default=DATA_FILE)
    p.add_argument("--report", type=Path)
    args = p.parse_args(argv)
    data = json.loads(args.file.read_text())
    with SessionLocal() as session:
        report = apply(session, data, args.apply)
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(f"refinements {report['refinements']} · evidence verified {report['verified']} · applied {report['applied']} · "
          f"already applied {report['already_applied']} · failed {len(report['failed'])} · "
          f"discrepancies left untouched {report['discrepancies_untouched']}" + ("" if args.apply else " (dry run)"))
    for f in report["failed"]:
        print("FAILED", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
