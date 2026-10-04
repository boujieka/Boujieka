"""One-off maintenance: recompute `security.tenor_days` as the ORIGINAL tenor (app.ingest.tenor).

Securities used to take tenor_days from the first extraction approved for their ISIN, which for a
reopening or a buyback is the remaining maturity ("7 jours"), not the original tenor. This command
re-applies the evidence rule to every verified, non-synthetic security, from its verified staging
rows, and prints a before/after report. Dry run by default; --apply writes and commits. Each
changed row gets a dated provenance note naming its evidence. Only tenor_days, field_status
["tenor_days"] and provenance_notes are touched. Idempotent: a second run changes nothing.

    python -m app.ingest.fix_tenors                    # dry run
    python -m app.ingest.fix_tenors --apply [--report out.json]
"""

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingest.tenor import NOT_AVAILABLE, apply_decision, original_tenor, security_evidence
from app.models import Security
from app.models.enums import VerificationStatus


def run(session: Session, apply: bool, today: date | None = None) -> dict:
    today = today or date.today()
    report: dict = {"checked": 0, "changed": 0, "rules": Counter(), "conflicts": [], "changes": [],
                    "incomplete_evidence": [], "unchanged_null": 0}
    securities = session.scalars(select(Security).where(
        Security.is_synthetic.is_(False), Security.verification_status == VerificationStatus.VERIFIED,
        Security.isin.is_not(None)).order_by(Security.isin)).all()
    for sec in securities:
        report["checked"] += 1
        evidence, known, complete = security_evidence(session, sec)
        decision = original_tenor(evidence, known)
        report["rules"][decision.rule] += 1
        if not complete:
            # Some promoted auctions have no staging row here: the evidence is partial, so only
            # an original issue may overwrite a value.
            report["incomplete_evidence"].append(sec.isin)
            if decision.rule != "original_issue":
                continue
        if decision.conflict:
            report["conflicts"].append({"isin": sec.isin, "days": decision.days, "conflict": decision.conflict})
        before = sec.tenor_days
        if apply:
            changed = apply_decision(sec, decision, today)
        else:
            changed = not (before == decision.days and
                           (sec.field_status or {}).get("tenor_days") == (NOT_AVAILABLE if decision.days is None else None))
        if changed:
            report["changed"] += 1
            report["changes"].append({"isin": sec.isin, "instrument": sec.instrument_type.value,
                                      "before": before, "after": decision.days, "rule": decision.rule,
                                      "note": decision.note})
    if apply:
        session.commit()
    report["rules"] = dict(report["rules"])
    return report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--apply", action="store_true", help="write the corrections (default: dry run)")
    p.add_argument("--report", type=Path, help="write the full report as JSON")
    args = p.parse_args(argv)
    from app.db import engine

    with Session(engine) as session:
        report = run(session, args.apply)
    for c in report["changes"]:
        print(f"{c['isin']}  {c['instrument']:<14} {str(c['before']):>5} -> {str(c['after']):<5} "
              f"[{c['rule']}] {c['note']}")
    for c in report["conflicts"]:
        print(f"CONFLICT {c['isin']}: {c['conflict']}")
    by = Counter((c["before"], c["after"]) for c in report["changes"])
    print(f"{'APPLIED' if args.apply else 'DRY RUN'}: checked {report['checked']} · "
          f"{'changed' if args.apply else 'would change'} {report['changed']} · rules {report['rules']} · conflicts {len(report['conflicts'])} · "
          f"partial evidence {len(report['incomplete_evidence'])} · distinct before->after {len(by)}")
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
