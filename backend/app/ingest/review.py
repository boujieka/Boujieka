"""Human verification queue (CLI).

    python -m app.ingest.review list [--status unverified|verified|rejected|all] [--country SEN]
    python -m app.ingest.review show <id>
    python -m app.ingest.review approve <id> [--reviewer NAME] [--note TEXT]
    python -m app.ingest.review reject <id> --reason TEXT [--reviewer NAME]

Before approving, open the document (`show` prints its URL and the local copy) and check each
value against it: `show` lists every field with the text it was read from and its location.
The reviewer name defaults to $ABI_REVIEWER, then the OS user. Every decision is recorded with
the reviewer and a UTC timestamp.
"""

import argparse
import getpass
import sys

from app.config import get_settings
from app.ingest.queue import ReviewError, approve, list_queue, reject
from app.models import AuctionExtraction, ExtractionReviewEvent
from app.models.enums import VerificationStatus

STATUSES = {"unverified": VerificationStatus.UNVERIFIED, "verified": VerificationStatus.VERIFIED,
            "rejected": VerificationStatus.REJECTED, "all": None}


def _reviewer(arg: str | None) -> str:
    return arg or get_settings().reviewer or getpass.getuser()


def _fmt(v) -> str:
    return "—" if v is None else str(v)


def print_list(session, status: str, country: str | None, limit: int) -> None:
    page = list_queue(session, STATUSES[status], country, limit=limit)
    print(f"{page.total} extraction(s) [{status}]" + (f" for {country}" if country else ""))
    print(f"{'id':>6}  {'status':<10} {'parse':<8} {'conf':>5}  {'ctry':<4} {'date':<10}  "
          f"{'instr':<5} {'isin':<12}  {'submitted':>15} {'allotted':>15} {'yield%':>7}")
    for e in page.items:
        f = e.fields or {}

        def v(n):
            return (f.get(n) or {}).get("value")

        print(f"{e.extraction_id:>6}  {e.verification_status.value:<10} {e.parse_status:<8} "
              f"{_fmt(e.confidence_score):>5}  {_fmt(e.country_iso3):<4} {_fmt(e.auction_date):<10}  "
              f"{_fmt(e.instrument):<5} {_fmt(e.isin):<12}  {_fmt(v('amount_submitted')):>15} "
              f"{_fmt(v('amount_allocated')):>15} {_fmt(v('weighted_average_yield')):>7}")


def print_show(session, extraction_id: int) -> None:
    e = session.get(AuctionExtraction, extraction_id)
    if e is None:
        raise ReviewError(f"extraction {extraction_id} not found")
    doc = e.document
    print(f"Extraction {e.extraction_id} — {e.verification_status.value.upper()} ({e.data_nature.value}); "
          f"parse {e.parse_status}; confidence {_fmt(e.confidence_score)}; extractor {e.extractor}")
    if doc:
        print(f"Document {doc.document_id}: {doc.title}\n  URL: {doc.url}\n  local copy: {doc.storage_path}"
              f"\n  sha256: {doc.content_sha256}\n  published: {_fmt(doc.publication_date)}; "
              f"retrieved: {_fmt(doc.retrieved_at)}")
    print("\nFields (value · read from · where · confidence):")
    for name, f in sorted((e.fields or {}).items()):
        unit = f" {f['unit']}" if f.get("unit") else ""
        note = f"  [{f['note']}]" if f.get("note") else ""
        print(f"  {name:<24} {_fmt(f.get('value'))}{unit}\n  {'':<24} ← {f.get('raw')!r} @ {f.get('locator')}"
              f" · {f.get('confidence')}{note}")
    if e.field_status:
        print("\nEmpty fields:")
        for name, st in sorted(e.field_status.items()):
            print(f"  {name:<24} {st}")
    print("\nOperation (all securities of the auction together):")
    for name, f in sorted((e.operation or {}).items()):
        print(f"  {name:<24} {f.get('value') if isinstance(f, dict) else f}")
    if e.checks:
        print("\nConsistency checks (CALCULATION):")
        for c in e.checks:
            print(f"  [{'ok' if c['ok'] else 'FAIL'}] {c['check']}: {c['detail']}")
    if e.warnings:
        print("\nWarnings:")
        for w in e.warnings:
            print(f"  - {w}")
    events = session.query(ExtractionReviewEvent).filter_by(extraction_id=e.extraction_id).all()
    if events:
        print("\nReview history:")
        for ev in events:
            print(f"  {ev.at.isoformat()} {ev.action} by {ev.reviewer}" + (f": {ev.reason}" if ev.reason else ""))


def main(argv: list[str] | None = None, session_factory=None) -> int:
    parser = argparse.ArgumentParser(description="Human verification queue for extracted auction data")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.add_argument("--status", choices=list(STATUSES), default="unverified")
    p.add_argument("--country")
    p.add_argument("--limit", type=int, default=100)
    p = sub.add_parser("show")
    p.add_argument("id", type=int)
    p = sub.add_parser("approve")
    p.add_argument("id", type=int)
    p.add_argument("--reviewer")
    p.add_argument("--note")
    p = sub.add_parser("reject")
    p.add_argument("id", type=int)
    p.add_argument("--reason", required=True)
    p.add_argument("--reviewer")
    args = parser.parse_args(argv)

    if session_factory is None:
        from app.db import SessionLocal as session_factory
    with session_factory() as session:
        try:
            if args.cmd == "list":
                print_list(session, args.status, args.country, args.limit)
            elif args.cmd == "show":
                print_show(session, args.id)
            elif args.cmd == "approve":
                a = approve(session, args.id, _reviewer(args.reviewer), args.note)
                session.commit()
                print(f"Approved extraction {args.id} → auction {a.auction_id} (VERIFIED)")
            elif args.cmd == "reject":
                reject(session, args.id, _reviewer(args.reviewer), args.reason)
                session.commit()
                print(f"Rejected extraction {args.id}")
        except ReviewError as e:
            session.rollback()
            print(f"error: {e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
