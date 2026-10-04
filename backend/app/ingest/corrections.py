"""Owner decisions on held extractions, applied only with verified official evidence.

The strict checker (app.ingest.autocheck) is not involved and not relaxed. Each entry of the
versioned file `data/owner_corrections.json` names one staged extraction, the owner's decision it
relies on, and either:
  * `set`: field values to correct, each backed by an official document (URL + SHA-256 + the
    printed line). Before anything is written, the document is re-downloaded, its SHA-256 must
    match, every quoted fragment of the line must appear in its text (in order), and the corrected
    value must appear as printed;
  * `clear`: fields to empty with a status (`not_available` / `not_disclosed`) and a reason
    (e.g. a published 0,00 % yield the owner decided not to store);
  * `column`: a staging column to set (country_iso3), also evidence-backed.
Then the row is approved through `app.ingest.queue.approve` (same promotion, duplicate and
conflict guards as any approval), with the owner recorded as the deciding reviewer.
If any evidence check fails, nothing is changed on that row.

    python -m app.ingest.corrections            # dry run: verify evidence, report
    python -m app.ingest.corrections --apply
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import httpx
from sqlalchemy.orm import Session

from app.db import engine
from app.ingest.queue import ReviewError, approve
from app.models import AuctionExtraction
from app.models.enums import VerificationStatus

DATA_FILE = Path(__file__).resolve().parent / "data" / "owner_corrections.json"
REVIEWER = "Proprietaire (Boujieka) - decisions du 2026-10-04, preuves officielles verifiees par Claude"


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).replace(" ", " ").replace(" ", " ").replace("’", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def _text(content: bytes) -> str:
    if content[:4] != b"%PDF":
        return content.decode("utf-8", "replace")
    out = []
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(content)
        f.flush()
        for args in (["-layout"], []):
            out.append(subprocess.run(["pdftotext", *args, "-enc", "UTF-8", f.name, "-"],
                                      capture_output=True, text=True).stdout)
    return "\n".join(out)


def _fragments(line: str) -> list[str]:
    """Verbatim fragments of an evidence line as written by the investigators: '|' wrap markers are
    dropped; parentheses, '...', '…', ';', ' / ' and ': ' separate fragments. Each remaining
    fragment (4+ chars) must appear verbatim in the document, in order."""
    # Parenthesised parts are separators (they may be the investigator's annotation or printed text
    # such as "(en FCFA)"); the text on each side must still appear verbatim and in order.
    parts = re.split(r"\([^)]*\)|\.\.\.|…|;| / |: ", line.replace("|", ""))
    return [p.strip(" '\"") for p in parts if len(p.strip(" '\"")) >= 4]


def _printed_forms(value: str) -> list[str]:
    """How a stored value can appear in a French official document."""
    forms = {value}
    if m := re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", value):
        return [_norm(f"{m[3]}/{m[2]}/{m[1]}")]
    try:
        d = Decimal(value)
    except Exception:
        return [_norm(value)]
    s = format(d.normalize(), "f")
    ip, _, fp = s.partition(".")
    grouped = f"{int(ip):,}".replace(",", " ")
    for frac in {fp, fp.rstrip("0"), fp.ljust(2, "0")}:
        forms.add(grouped + ("," + frac if frac else ""))
        forms.add(ip + ("," + frac if frac else ""))
    return sorted({_norm(f) for f in forms})


class Evidence:
    def __init__(self) -> None:
        self.cache: dict[str, tuple[str, str]] = {}
        self.client = httpx.Client(timeout=60, follow_redirects=True,
                                   headers={"User-Agent": "Mozilla/5.0 (compatible; CartoucheCorrections/1.0)"})

    def check(self, ev: dict, value: str | None) -> str | None:
        """None if the evidence holds, else the reason it does not."""
        url = ev.get("url")
        if not url or not url.startswith("https://www.umoatitres.org/"):
            return f"evidence URL not on umoatitres.org: {url}"
        if url not in self.cache:
            try:
                content = self.client.get(url).content
            except Exception as e:  # network error: fail closed
                return f"download failed: {type(e).__name__}"
            self.cache[url] = (hashlib.sha256(content).hexdigest(), _norm(_text(content)))
        sha, text = self.cache[url]
        if sha != ev.get("sha256"):
            return f"SHA-256 mismatch for {url}"
        pos = 0
        for frag in _fragments(ev.get("line", "")):
            i = text.find(_norm(frag), pos)
            if i < 0:
                return f"fragment not found in document: {frag[:80]!r}"
            pos = i + 1
        if value is not None and not any(form in text for form in _printed_forms(value)):
            # A long amount wrapped over two lines ("2 509 480 00" / "0"): accept only an exact
            # digit sequence of 7+ digits found in the document with all whitespace removed.
            digits = re.sub(r"\D", "", value.split(".")[0])
            if not (len(digits) >= 7 and value.split(".")[-1].strip("0") == "" and digits in re.sub(r"\s", "", text)):
                return f"value {value!r} not printed in the document"
        return None


def apply(session: Session, entries: list[dict], do_apply: bool) -> dict:
    ev = Evidence()
    report = {"entries": len(entries), "verified": 0, "approved": 0, "failed": [], "approve_errors": []}
    now = datetime.now(timezone.utc).date().isoformat()
    for e in entries:
        ext = session.get(AuctionExtraction, e["extraction_id"])
        if ext is None or ext.verification_status != VerificationStatus.UNVERIFIED:
            report["failed"].append({"id": e["extraction_id"], "why": "not an unverified staged row"})
            continue
        if ext.isin != e["isin"] or str(ext.auction_date) != e["auction_date"]:
            report["failed"].append({"id": e["extraction_id"], "why": "ISIN/date do not match the staged row"})
            continue
        problems = [f"{name}: {why}" for name, p in {**e.get("set", {}), **e.get("column", {})}.items()
                    if (why := ev.check(p["evidence"], p["value"] if name != "country_iso3" else None))]
        if problems:
            report["failed"].append({"id": e["extraction_id"], "why": problems})
            continue
        report["verified"] += 1
        if not do_apply:
            continue
        try:
            with session.begin_nested():
                fields = dict(ext.fields or {})
                status = dict(ext.field_status or {})
                for name, p in e.get("set", {}).items():
                    old = (fields.get(name) or {}).get("value")
                    fields[name] = {**(fields.get(name) or {}), "value": p["value"], "raw": p["evidence"]["line"][:300],
                                    "locator": f"external:{p['evidence']['url']}", "confidence": 1.0,
                                    "note": f"Corrected {old!r} -> {p['value']!r} on {now} by owner decision "
                                            f"{e['decision']}; evidence {p['evidence']['url']} (sha256 {p['evidence']['sha256'][:12]})"}
                    status.pop(name, None)
                for name, p in e.get("clear", {}).items():
                    fields[name] = {**(fields.get(name) or {}), "value": None,
                                    "note": f"Cleared on {now} by owner decision {e['decision']}: {p['reason']}"}
                    status[name] = p["status"]
                for name, p in e.get("column", {}).items():
                    setattr(ext, name, p["value"])
                ext.fields, ext.field_status = fields, status
                session.flush()
                approve(session, ext.extraction_id, REVIEWER,
                        f"Owner decision {e['decision']}: {e.get('summary', '')}".strip())
            report["approved"] += 1
        except ReviewError as err:
            report["approve_errors"].append({"id": e["extraction_id"], "error": str(err)})
    if do_apply:
        session.commit()
    return report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--apply", action="store_true")
    p.add_argument("--file", type=Path, default=DATA_FILE)
    p.add_argument("--report", type=Path)
    args = p.parse_args(argv)
    entries = json.loads(args.file.read_text())["entries"]
    with Session(engine) as session:
        report = apply(session, entries, args.apply)
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"entries {report['entries']} · evidence verified {report['verified']} · approved {report['approved']} · "
          f"failed {len(report['failed'])} · approval errors {len(report['approve_errors'])}")
    for f in report["failed"]:
        print("FAILED", f)
    for f in report["approve_errors"]:
        print("APPROVE ERROR", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
