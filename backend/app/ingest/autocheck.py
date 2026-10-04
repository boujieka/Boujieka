"""Automated second check of staged UMOA-Titres extractions, independent of the parser.

For every UNVERIFIED staged row this module:
  1. re-downloads the official PDF and compares its SHA-256 with the stored document (the
     publication must not have changed since extraction);
  2. extracts the text again with its own `pdftotext -layout` call (not the parser's);
  3. for every extracted field with a value, finds the field's label in that text, takes the line
     carrying the value (the label's line, or the next one when values are printed below), splits
     it into cells and checks that the cell named by the locator ("col i/n") holds the raw text;
  4. re-derives the stored value from the raw text with its own conversion rules (dates, French
     numbers, "millions de FCFA", percentages) and compares;
  5. runs row-level sanity checks (every extraction consistency check passed, ISIN prefix matches
     the country, allotted <= submitted, maturity after the auction date, yields in 0–30 %).

A row passes only if every check passes; anything doubtful stays in the queue for a person.
With --approve, passing rows are approved through the normal review path (app.ingest.queue),
so they are promoted and audited exactly like a manual approval, under the reviewer name given.

    python -m app.ingest.autocheck                       # dry run: report only
    python -m app.ingest.autocheck --approve --reviewer "…" --report out.json
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import engine
from app.ingest.queue import ReviewError, approve
from app.models import AuctionExtraction, SourceDocument
from app.models.enums import VerificationStatus

ISIN_COUNTRY = {"BJ": "BEN", "BF": "BFA", "CI": "CIV", "GW": "GNB", "ML": "MLI", "NE": "NER", "SN": "SEN", "TG": "TGO"}
LOCATOR_RE = re.compile(r"p(\d+):L(\d+) '(.*)'(?: col (\d+)/(\d+))?$")  # labels may contain apostrophes
# Fields whose stored value is not the raw text itself, with the rule to re-derive it.
DERIVED = {"instrument", "tenor_days"}
YIELD_FIELDS = ("weighted_average_yield", "marginal_rate", "weighted_average_rate")


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s.replace("’", "'")).strip()


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(" ", " ").replace(" ", " ")).strip()


def pdf_pages(content: bytes) -> list[list[str]]:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(content)
        f.flush()
        out = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", f.name, "-"],
                             capture_output=True, text=True, check=True).stdout
    return [page.split("\n") for page in out.split("\f")]


def derive(raw: str, field: dict) -> str | None:
    """Independent conversion of the printed text into the stored representation."""
    r = norm(raw)
    if m := re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", r):
        return date(int(m[3]), int(m[2]), int(m[1])).isoformat()
    if "millions" in r.lower():
        num = re.match(r"([\d ]+(?:,\d+)?)", r)
        if not num:
            return None
        return str(Decimal(num[1].replace(" ", "").replace(",", ".")) * 1_000_000)
    if r.endswith("%"):
        return str(Decimal(r[:-1].strip().replace(" ", "").replace(",", ".")))
    if re.fullmatch(r"[\d ]+(?:,\d+)?", r):
        return str(Decimal(r.replace(" ", "").replace(",", ".")))
    return r


def same(a: str, b: str) -> bool:
    try:
        return Decimal(a) == Decimal(b)
    except (InvalidOperation, TypeError):
        return norm(str(a)) == norm(str(b))


def _label_lines(pages: list[list[str]], locator: str) -> tuple[list[str], str]:
    """Candidate lines for a locator: each line carrying the label, and the line after it."""
    m = LOCATOR_RE.match(locator or "")
    if not m or int(m[1]) > len(pages):
        return [], ""
    lines, label = pages[int(m[1]) - 1], fold(m[3])
    out = []
    for i, line in enumerate(lines):
        if not label or label in fold(line):
            out += [line, lines[i + 1] if i + 1 < len(lines) else ""]
    return out, label


def column_of(locator: str) -> int:
    m = LOCATOR_RE.match(locator or "")  # noqa: E501
    return int(m[4]) if m and m[4] else 1


def in_order(line: str, raws: list[str]) -> bool:
    """True if every raw text appears in the line, left to right in the given order."""
    text, pos = norm(line), 0
    for raw in raws:
        i = text.find(norm(raw), pos)
        if i < 0:
            return False
        pos = i + len(norm(raw))
    return True


def placement_ok(pages: list[list[str]], locator: str, raw: str, siblings: list[tuple[int, str]]) -> tuple[bool, str]:
    """The raw text sits next to its label, and in the right column relative to the values the
    other securities of the same document have for this field (`siblings`: (column, raw))."""
    lines, label = _label_lines(pages, locator)
    if not lines:
        return False, f"label of {locator!r} not found"
    # Document-level values (no column) are shared by every security: only presence is checked.
    ordered = [r for _, r in sorted(set(siblings))] if siblings and " col " in locator else [raw]
    for line in lines:
        if norm(raw) in norm(line) and in_order(line, ordered):
            return True, "ok"
    if any(norm(raw) in norm(line) for line in lines):
        return False, f"'{raw}' is next to '{label}' but not in its column order {ordered}"
    return False, f"'{raw}' not found next to label '{label}'"


def check_row(ext: AuctionExtraction, pages: list[list[str]],
              siblings: dict[str, list[tuple[int, str]]] | None = None) -> list[str]:
    problems: list[str] = []
    if ext.parse_status != "complete":
        problems.append(f"parse_status={ext.parse_status}")
    for c in ext.checks or []:
        if not c.get("ok"):
            problems.append(f"failed check: {c.get('check')}: {c.get('detail')}")
    for name, f in (ext.fields or {}).items():
        if f.get("value") is None or name in DERIVED:
            continue
        raw = f.get("raw") or ""
        ok, why = placement_ok(pages, f.get("locator", ""), raw, (siblings or {}).get(name, []))
        if not ok:
            problems.append(f"{name}: {why}")
            continue
        if name in ("isin", "security_name", "auction_number", "tenor"):
            continue
        d = derive(raw, f)
        if d is not None and f.get("unit") == "percent" and "%" not in raw and not same(d, f["value"]):
            d = str(Decimal(d) * 100)  # ratio printed without % (e.g. 0,3328), stored as percent
        if d is None or not same(d, f["value"]):
            problems.append(f"{name}: stored {f['value']!r} but '{raw}' gives {d!r}")
    v = lambda n: (ext.fields.get(n) or {}).get("value")  # noqa: E731
    if ext.isin and ISIN_COUNTRY.get(ext.isin[:2]) != ext.country_iso3:
        problems.append(f"ISIN {ext.isin} does not match country {ext.country_iso3}")
    sub, alloc = v("amount_submitted"), v("amount_allocated")
    if sub is not None and alloc is not None and Decimal(alloc) > Decimal(sub):
        problems.append("allotted > submitted")
    mat = v("maturity_date")
    if mat and ext.auction_date and date.fromisoformat(mat) <= ext.auction_date:
        problems.append("maturity not after auction date")
    for n in YIELD_FIELDS:
        y = v(n)
        if y is not None and alloc not in (None, "0") and not (Decimal("0") < Decimal(y) <= Decimal("30")):
            # Bond auctions publish a price (around 100) in the marginal/average fields, not a rate.
            if not (ext.instrument == "OAT" and n != "weighted_average_yield" and Decimal("50") < Decimal(y) < Decimal("150")):
                problems.append(f"{n}={y} outside 0–30 %")
    return problems


def run(session: Session, do_approve: bool, reviewer: str | None, note: str | None) -> dict:
    rows = list(session.scalars(select(AuctionExtraction).where(
        AuctionExtraction.verification_status == VerificationStatus.UNVERIFIED).order_by(AuctionExtraction.extraction_id)))
    docs: dict[int, tuple[list[list[str]] | None, str | None]] = {}
    sibs: dict[int, dict[str, list[tuple[int, str]]]] = {}
    report = {"checked": 0, "passed": 0, "approved": 0, "held": [], "approve_errors": []}
    with httpx.Client(timeout=60, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (compatible; CartoucheAutocheck/1.0)"}) as client:
        for ext in rows:
            report["checked"] += 1
            doc: SourceDocument | None = ext.document
            if doc is None:
                report["held"].append({"id": ext.extraction_id, "problems": ["no source document"]})
                continue
            if doc.document_id not in docs:
                try:
                    content = client.get(doc.url).content
                    sha = hashlib.sha256(content).hexdigest()
                    docs[doc.document_id] = (pdf_pages(content), None) if sha == doc.content_sha256 else \
                        (None, f"live document changed (sha {sha[:12]} vs stored {str(doc.content_sha256)[:12]})")
                except Exception as e:  # network or PDF error: hold, never approve on doubt
                    docs[doc.document_id] = (None, f"re-download failed: {type(e).__name__}: {e}"[:200])
            pages, err = docs[doc.document_id]
            if doc.document_id not in sibs:
                sibs[doc.document_id] = {}
                for other in session.scalars(select(AuctionExtraction).where(
                        AuctionExtraction.source_document_id == doc.document_id)):
                    for n, f in (other.fields or {}).items():
                        if f.get("raw") and f.get("value") is not None:
                            sibs[doc.document_id].setdefault((f.get("locator") or "").split(" col ")[0] + "|" + n, []).append(
                                (column_of(f.get("locator", "")), f["raw"]))
            mine = {n: sibs[doc.document_id].get((f.get("locator") or "").split(" col ")[0] + "|" + n, [])
                    for n, f in (ext.fields or {}).items()}
            problems = [err] if err else check_row(ext, pages, mine)
            if problems:
                report["held"].append({"id": ext.extraction_id, "isin": ext.isin, "date": str(ext.auction_date),
                                       "problems": problems})
                continue
            report["passed"] += 1
            if do_approve:
                try:
                    with session.begin_nested():
                        approve(session, ext.extraction_id, reviewer, note)
                    report["approved"] += 1
                except ReviewError as e:
                    report["approve_errors"].append({"id": ext.extraction_id, "isin": ext.isin, "error": str(e)})
        if do_approve:
            session.commit()
    return report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--approve", action="store_true", help="approve rows that pass every check")
    p.add_argument("--reviewer", help="name recorded on approvals (required with --approve)")
    p.add_argument("--note", help="note recorded on each approval")
    p.add_argument("--report", type=Path, help="write the full report as JSON")
    args = p.parse_args(argv)
    if args.approve and not (args.reviewer and args.reviewer.strip()):
        p.error("--approve requires --reviewer")
    with Session(engine) as session:
        report = run(session, args.approve, args.reviewer, args.note)
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"checked {report['checked']} · passed {report['passed']} · approved {report['approved']} · "
          f"held {len(report['held'])} · approval errors {len(report['approve_errors'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
