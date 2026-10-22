"""Early-warning system (Master prompt §20).

Each rule is documented, uses configurable thresholds (AlertThreshold; organization overrides
the AP²I default) and produces alerts that carry the observed value, threshold, source and a
recommended VERIFICATION. Alerts are signals for verification — they never assert fraud,
corruption or mismanagement.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import select, update
from sqlalchemy.orm import Session, selectinload

from app.finance.indicators import agreement_position, ratio
from app.models import (
    AlertThreshold,
    Contract,
    ContractAmendment,
    FinancingAgreement,
    ImplementationProgress,
    Project,
    ProjectAlert,
    ProjectSourceLink,
    Sector,
    SourceRecord,
)

INFRA_SECTORS = {"ENERGY", "TRANSPORT", "WATER", "HEALTH", "EDUCATION", "DIGITAL", "URBAN", "HOUSING"}

RULES: dict[str, dict] = {
    "LOW_DISBURSEMENT": {"label": "Low disbursement relative to time elapsed", "indicator": "disbursement_rate"},
    "CLOSING_DATE_PASSED": {"label": "Planned closing date passed while reported active", "indicator": "planned_end_date"},
    "SCHEDULE_EXTENSION": {"label": "Major extension of the closing date", "indicator": "closing_date_extension_months"},
    "COST_REVISION": {"label": "Significant cost revision", "indicator": "cost_revision_ratio"},
    "REPEATED_AMENDMENTS": {"label": "Repeated contract amendments", "indicator": "contract_amendments_count"},
    "FINANCING_GAP": {"label": "Financing gap", "indicator": "financing_gap_ratio"},
    "CANCELLATION": {"label": "Significant cancellation of financing", "indicator": "cancelled_share"},
    "PHYS_FIN_GAP": {"label": "Physical and financial progress inconsistent", "indicator": "physical_minus_financial_points"},
    "COMPLETED_NOT_OPERATIONAL": {"label": "Completed but reported non-operational", "indicator": "operational_status"},
    "OPERATIONAL_STATUS_UNVERIFIED": {"label": "Completed infrastructure with unverified operational status", "indicator": "operational_status"},
    "MISSING_PROGRESS_REPORT": {"label": "No recent implementation information", "indicator": "months_since_last_source_update"},
    "NO_DISBURSEMENT_DATA": {"label": "Disbursement information not published", "indicator": "disbursed_amount"},
}


@dataclass
class Finding:
    rule: str
    level: str
    observed: str
    threshold: str
    explanation: str
    verification: str
    source: str
    source_record_ids: list[int]
    discriminator: str = ""


def thresholds(db: Session, organization_id: int | None = None) -> dict[tuple[str, str], Decimal]:
    out = {(t.rule_code, t.parameter): t.value for t in db.scalars(select(AlertThreshold).where(AlertThreshold.organization_id.is_(None)))}
    if organization_id:
        for t in db.scalars(select(AlertThreshold).where(AlertThreshold.organization_id == organization_id)):
            out[(t.rule_code, t.parameter)] = t.value
    return out


def _months(a: date, b: date) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)


def evaluate_project(db: Session, p: Project, thr: dict, today: date) -> list[Finding]:
    f: list[Finding] = []
    sector_code = p.sector.code if p.sector else None
    srcs = sorted(db.scalars(select(ProjectSourceLink.source_record_id).where(ProjectSourceLink.project_id == p.id,
                                                                              ProjectSourceLink.active.is_(True))))
    start = p.implementation_start_date or p.original_approval_date
    closing_dates = [a.closing_date_current for a in p.agreements if a.closing_date_current]
    planned_end = p.revised_completion_date or p.original_completion_date or (max(closing_dates) if closing_dates else None)
    active = p.status in ("active", "approved")

    positions = [(a, agreement_position(db, a)) for a in p.agreements]
    elapsed = None
    if start and planned_end and planned_end > start:
        elapsed = ratio(Decimal((min(today, planned_end) - start).days), Decimal((planned_end - start).days))

    # LOW_DISBURSEMENT
    if active and elapsed is not None:
        max_r, min_e = thr[("LOW_DISBURSEMENT", "max_disbursement_ratio")], thr[("LOW_DISBURSEMENT", "min_elapsed_ratio")]
        for a, pos in positions:
            r = ratio(pos.disbursed, pos.committed)
            if r is None or elapsed < min_e or r > max_r:
                continue
            level = "critical_attention" if (r < max_r / 2 and elapsed >= Decimal("0.75")) else "high_attention"
            f.append(Finding(
                "LOW_DISBURSEMENT", level,
                f"{(r * 100):.1f}% disbursed ({pos.disbursed} / {pos.committed} {pos.currency}) with {(elapsed * 100):.0f}% of the planned period elapsed",
                f"disbursement ≤ {(max_r * 100):.0f}% when ≥ {(min_e * 100):.0f}% of the period has elapsed",
                "The financing has disbursed little relative to the time elapsed since start. This can reflect late "
                "effectiveness, procurement delays, front-loaded preparation or a disbursement profile weighted to later years.",
                "Check the latest implementation status report and disbursement schedule with the executing agency and the "
                "financing partner; confirm effectiveness date and pending procurement.",
                pos.disbursed_basis or "", pos.source_record_ids, discriminator=a.source_identifier))
    # CLOSING_DATE_PASSED
    grace = int(thr[("CLOSING_DATE_PASSED", "grace_days")])
    if active and planned_end and (today - planned_end).days > grace:
        months = _months(planned_end, today)
        f.append(Finding(
            "CLOSING_DATE_PASSED", "high_attention" if months >= 12 else "watch",
            f"Planned end {planned_end.isoformat()} passed {months} month(s) ago; status reported '{p.status}'",
            f"planned end date + {grace} days",
            "The source still reports the project as active after its planned end date. The source may not have been "
            "updated, or an extension may not be published yet.",
            "Verify with the financing partner whether the closing date was extended or the project closed.",
            "planned end / closing date as published", srcs))
    # SCHEDULE_EXTENSION
    min_ext = int(thr[("SCHEDULE_EXTENSION", "min_extension_months")])
    for a in p.agreements:
        if a.closing_date_original and a.closing_date_current and a.closing_date_current > a.closing_date_original:
            ext = _months(a.closing_date_original, a.closing_date_current)
            if ext >= min_ext:
                f.append(Finding(
                    "SCHEDULE_EXTENSION", "watch", f"Current/actual closing date {ext} months later than originally planned ({a.closing_date_original} → {a.closing_date_current})",
                    f"≥ {min_ext} months", "The current or actual closing date is significantly later than the originally planned one.",
                    "Review the restructuring paper or amendment that documents the extension and its reasons.",
                    a.source_identifier, srcs, discriminator=a.source_identifier))
    # COST_REVISION
    max_cost = thr[("COST_REVISION", "max_ratio")]
    if p.original_estimated_cost and p.revised_estimated_cost and p.original_estimated_cost > 0:
        r = ratio(p.revised_estimated_cost, p.original_estimated_cost)
        if r is not None and r > max_cost:
            f.append(Finding(
                "COST_REVISION", "high_attention", f"Revised cost = {r:.2f} × original ({p.revised_estimated_cost} vs {p.original_estimated_cost} {p.cost_currency})",
                f"> {max_cost} × original", "The estimated cost has been revised upward. Revisions can reflect scope changes, "
                "price increases, currency movements or design changes.",
                "Obtain the documented justification of the revision (amendment, restructuring paper).", "project cost observations", srcs))
    # REPEATED_AMENDMENTS
    contracts = db.scalars(select(Contract.id).where(Contract.project_id == p.id)).all()
    if contracts:
        n = len(db.scalars(select(ContractAmendment.id).where(ContractAmendment.contract_id.in_(contracts))).all())
        if n >= int(thr[("REPEATED_AMENDMENTS", "min_count")]):
            f.append(Finding("REPEATED_AMENDMENTS", "watch", f"{n} contract amendments", f"≥ {int(thr[('REPEATED_AMENDMENTS', 'min_count')])}",
                             "Several amendments have been recorded on this project's contracts.",
                             "Review the amendments' purposes and cumulative effect on cost and schedule.", "contract records", srcs))
    # CANCELLATION
    min_c = thr[("CANCELLATION", "min_cancelled_ratio")]
    for a, pos in positions:
        gross = None
        cancelled = None
        basis = ""
        if a.amount_original and a.reported_current_commitment is not None and a.currency == "USD":
            gross, cancelled = a.amount_original, a.amount_original - a.reported_current_commitment
            basis = "original commitment vs current commitment as published"
        elif pos.cancelled and pos.committed is not None:
            gross, cancelled = pos.committed + pos.cancelled, pos.cancelled
            basis = "negative commitment transactions"
        r = ratio(cancelled, gross)
        if r is not None and r >= min_c:
            f.append(Finding("CANCELLATION", "watch", f"{(r * 100):.1f}% of the original commitment no longer committed ({cancelled} {pos.currency})",
                             f"≥ {(min_c * 100):.0f}%", "Part of the financing has been cancelled or reduced. Cancellations may "
                             "follow restructuring, savings or reallocation.",
                             "Check the restructuring or cancellation notice and whether the scope was reduced accordingly.",
                             basis, pos.source_record_ids, discriminator=a.source_identifier))
    # FINANCING_GAP
    cost = p.revised_estimated_cost or p.original_estimated_cost
    if cost and p.cost_currency:
        same = [pos.committed for _, pos in positions if pos.currency == p.cost_currency and pos.committed is not None]
        if same:
            gap = cost - sum(same, Decimal(0))
            r = ratio(gap, cost)
            if r is not None and r >= thr[("FINANCING_GAP", "min_gap_ratio")]:
                f.append(Finding("FINANCING_GAP", "watch", f"Gap {gap} {p.cost_currency} ({(r * 100):.1f}% of cost)",
                                 f"≥ {(thr[('FINANCING_GAP', 'min_gap_ratio')] * 100):.0f}% of cost",
                                 "Recorded commitments (same currency) do not cover the estimated cost. Other financing "
                                 "(counterpart, other currencies) may exist but is not recorded.",
                                 "Confirm the full financing plan with the executing agency.", "cost and commitments", srcs))
    # PHYS_FIN_GAP
    if p.physical_progress_pct is not None:
        rates = [ratio(pos.disbursed, pos.committed) for _, pos in positions]
        rates = [r for r in rates if r is not None]
        if len(rates) == 1:
            gap_pts = p.physical_progress_pct - rates[0] * 100
            if abs(gap_pts) > thr[("PHYS_FIN_GAP", "max_gap_points")]:
                f.append(Finding("PHYS_FIN_GAP", "watch", f"Physical {p.physical_progress_pct}% vs financial {(rates[0] * 100):.1f}%",
                                 f"|gap| > {thr[('PHYS_FIN_GAP', 'max_gap_points')]} points",
                                 "Physical and financial progress diverge. Advances, retention, unpaid works or reporting lags can explain this.",
                                 "Compare the latest physical progress report with payment records for the same date.",
                                 "physical progress observation and disbursement data", srcs))
    # COMPLETED_NOT_OPERATIONAL / OPERATIONAL_STATUS_UNVERIFIED
    finished = p.status in ("completed", "closed")
    if finished and p.operational_status in ("not_operational",):
        f.append(Finding("COMPLETED_NOT_OPERATIONAL", "critical_attention", "Operational status: not operational", "operational",
                         "A completed project is documented as not operational.",
                         "Field verification of the asset and of the operating entity's capacity and budget.", "operational status observation", srcs))
    elif finished and sector_code in INFRA_SECTORS and p.operational_status == "unknown":
        end = p.actual_completion_date or planned_end
        if end and end.year >= 2011:
            f.append(Finding("OPERATIONAL_STATUS_UNVERIFIED", "information", "Operational status: unknown", "documented operational status",
                             "No source documents whether the infrastructure delivered by this completed project is in operation.",
                             "Obtain an operational status statement (operator report, site visit, completion report).",
                             "absence of operational-status observation", srcs))
    # MISSING_PROGRESS_REPORT (based on the latest source update date stated by the sources)
    if active:
        max_age = int(thr[("MISSING_PROGRESS_REPORT", "max_age_months")])
        last_progress = db.scalar(select(ImplementationProgress.report_date).where(ImplementationProgress.project_id == p.id)
                                  .order_by(ImplementationProgress.report_date.desc()))
        stated = []
        if srcs:
            for v in db.scalars(select(SourceRecord.source_last_updated).where(SourceRecord.id.in_(srcs))):
                if v:
                    try:
                        stated.append(date.fromisoformat(str(v)[:10]))
                    except ValueError:
                        pass
        latest = max([d for d in [last_progress, *stated] if d], default=None)
        if latest is None or _months(latest, today) > max_age:
            f.append(Finding("MISSING_PROGRESS_REPORT", "information",
                             f"Latest dated source update: {latest.isoformat() if latest else 'none'}", f"≤ {max_age} months",
                             "No implementation information dated within the threshold is available for this active project.",
                             "Request the latest implementation progress report.", "source update dates", srcs))
    # NO_DISBURSEMENT_DATA
    if active and positions and all(pos.disbursed is None for _, pos in positions):
        f.append(Finding("NO_DISBURSEMENT_DATA", "information", "No disbursement figure published", "any disbursement figure",
                         "None of the imported sources publishes disbursements for this active project.",
                         "Request disbursement data from the financing partner or the executing agency.", "financing records", srcs))
    return f


def run_alerts(db: Session, country_id: int | None = None, organization_id: int | None = None, today: date | None = None) -> dict:
    today = today or date.today()
    thr = thresholds(db, organization_id)
    q = select(Project).where(Project.merged_into_id.is_(None)).options(
        selectinload(Project.agreements).selectinload(FinancingAgreement.partner), selectinload(Project.sector))
    if country_id:
        q = q.where(Project.country_id == country_id)
    projects = db.scalars(q).all()
    seen_keys: set[str] = set()
    created = 0
    for p in projects:
        for fnd in evaluate_project(db, p, thr, today):
            key = hashlib.sha256(f"{fnd.rule}|{p.id}|{fnd.discriminator}|{fnd.observed}".encode()).hexdigest()
            seen_keys.add(key)
            existing = db.scalar(select(ProjectAlert).where(ProjectAlert.alert_key == key))
            if existing:
                existing.is_active = True
                continue
            db.add(ProjectAlert(alert_key=key, project_id=p.id, rule_code=fnd.rule, level=fnd.level,
                                triggering_indicator=RULES[fnd.rule]["indicator"], observed_value=fnd.observed,
                                threshold=fnd.threshold, source=fnd.source, source_record_ids=fnd.source_record_ids,
                                as_of=today, explanation=fnd.explanation, recommended_verification=fnd.verification))
            created += 1
    # Alerts whose condition no longer holds become inactive (kept for history).
    ids = [p.id for p in projects]
    stale = 0
    if ids:
        for a in db.scalars(select(ProjectAlert).where(ProjectAlert.project_id.in_(ids), ProjectAlert.is_active.is_(True))):
            if a.alert_key not in seen_keys:
                a.is_active = False
                stale += 1
    db.commit()
    return {"projects_evaluated": len(projects), "alerts_created": created, "alerts_deactivated": stale,
            "evaluated_at": datetime.now(timezone.utc).isoformat()}


__all__ = ["run_alerts", "evaluate_project", "RULES", "thresholds", "update", "Sector"]
