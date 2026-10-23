"""Transparent financial and performance indicators (Master prompt §16, §19).

Every indicator returns: value, formula, inputs (with sources), as_of, limitations and the
missing inputs. A ratio is never computed when its denominator is missing or zero, and amounts
in different currencies are never added together without an explicit, dated conversion.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Contract,
    ContractAmendment,
    CounterpartFinancing,
    Disbursement,
    FinancingAgreement,
    FinancingCommitment,
    ImplementationProgress,
    Project,
)

FOUR = Decimal("0.0001")


@dataclass
class Indicator:
    code: str
    label: str
    value: Decimal | None
    unit: str
    formula: str
    inputs: list[dict] = field(default_factory=list)
    as_of: str | None = None
    limitations: list[str] = field(default_factory=list)
    missing_inputs: list[str] = field(default_factory=list)
    data_nature: str = "calculated"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["value"] = None if self.value is None else str(self.value)
        return d


def ratio(num: Decimal | None, den: Decimal | None) -> Decimal | None:
    if num is None or den is None or den == 0:
        return None
    return (Decimal(num) / Decimal(den)).quantize(FOUR, rounding=ROUND_HALF_EVEN)


@dataclass
class AgreementPosition:
    agreement_id: int
    partner: str | None
    source_identifier: str
    currency: str | None
    committed: Decimal | None
    committed_basis: str | None
    cancelled: Decimal
    disbursed: Decimal | None
    disbursed_basis: str | None
    disbursed_as_of: date | None
    undisbursed: Decimal | None
    expenditure: Decimal | None
    source_record_ids: list[int]
    is_guarantee: bool = False


def agreement_position(db: Session, agr: FinancingAgreement) -> AgreementPosition:
    commits = db.scalars(select(FinancingCommitment).where(FinancingCommitment.agreement_id == agr.id,
                                                           FinancingCommitment.is_counted.is_(True))).all()
    flows = db.scalars(select(Disbursement).where(Disbursement.agreement_id == agr.id, Disbursement.is_counted.is_(True))).all()
    srcs = sorted({x.source_record_id for x in [*commits, *flows] if x.source_record_id} | ({agr.source_record_id} if agr.source_record_id else set()))
    currency = agr.currency
    committed: Decimal | None = None
    basis = None
    cancelled = Decimal(0)
    same_cur_commits = [c for c in commits if currency is None or c.currency == currency]
    if same_cur_commits:
        currency = currency or same_cur_commits[0].currency
        committed = sum((c.amount for c in same_cur_commits), Decimal(0))
        cancelled = -sum((c.amount for c in same_cur_commits if c.amount < 0), Decimal(0))
        basis = "sum of counted commitment transactions (net of cancellations)"
    elif agr.amount_original is not None:
        excluded = db.scalar(select(FinancingCommitment.counting_note).where(
            FinancingCommitment.agreement_id == agr.id, FinancingCommitment.is_counted.is_(False)).limit(1))
        if excluded and not commits:
            # every commitment of this agreement was deliberately left out (e.g. EU decision envelope whose contracts
            # are counted): its headline amount must not come back through the fallback
            basis = f"not counted — {excluded}"
        else:
            committed = agr.amount_original
            basis = agr.amount_label
    if agr.reported_current_commitment is not None and currency == "USD" and agr.reported_cumulative_label:
        committed = agr.reported_current_commitment
        basis = "current commitment as published (" + agr.reported_cumulative_label + ")"

    disb_flows = [f for f in flows if f.flow_type == "disbursement" and (currency is None or f.currency == currency)]
    exp_flows = [f for f in flows if f.flow_type == "expenditure" and (currency is None or f.currency == currency)]
    disbursed = None
    d_basis = None
    d_asof = None
    if agr.reported_cumulative_disbursed is not None:
        disbursed = agr.reported_cumulative_disbursed
        d_basis = agr.reported_cumulative_label
        d_asof = agr.reported_cumulative_as_of
    elif disb_flows:
        disbursed = sum((f.amount for f in disb_flows), Decimal(0))
        d_basis = "sum of dated disbursement transactions"
        d_asof = max((f.value_date for f in disb_flows if f.value_date), default=None)
    undisbursed = agr.reported_undisbursed
    if undisbursed is None and committed is not None and disbursed is not None:
        undisbursed = committed - disbursed
    expenditure = sum((f.amount for f in exp_flows), Decimal(0)) if exp_flows else None
    is_guarantee = bool(agr.instrument and agr.instrument.code == "GUARANTEE")
    return AgreementPosition(agr.id, agr.partner.short_name if agr.partner else None, agr.source_identifier, currency,
                             committed, basis, cancelled, disbursed, d_basis, d_asof, undisbursed, expenditure, srcs, is_guarantee)


def project_financials(db: Session, project: Project, today: date | None = None) -> dict:
    today = today or date.today()
    agreements = db.scalars(select(FinancingAgreement).where(FinancingAgreement.project_id == project.id)).all()
    positions = [agreement_position(db, a) for a in agreements]
    by_cur: dict[str, dict[str, Decimal | None]] = defaultdict(lambda: {"committed": None, "disbursed": None, "cancelled": Decimal(0)})
    for p in positions:
        if not p.currency:
            continue
        slot = by_cur[p.currency]
        if p.committed is not None:
            slot["committed"] = (slot["committed"] or Decimal(0)) + p.committed
        if p.disbursed is not None:
            slot["disbursed"] = (slot["disbursed"] or Decimal(0)) + p.disbursed
        slot["cancelled"] += p.cancelled

    indicators: list[Indicator] = []
    # Disbursement rate per agreement (same currency by construction)
    for p in positions:
        if p.is_guarantee:
            indicators.append(Indicator(
                code="disbursement_rate", label=f"Disbursement rate — {p.partner or ''} {p.source_identifier}".strip(),
                value=None, unit="ratio", formula="not applicable",
                limitations=["Guarantee: amounts are disbursed only if the guarantee is called; a disbursement rate "
                             "is not meaningful."]))
            continue
        missing = []
        if p.committed is None:
            missing.append("commitment amount")
        if p.disbursed is None:
            missing.append("disbursed amount")
        indicators.append(Indicator(
            code="disbursement_rate", label=f"Disbursement rate — {p.partner or ''} {p.source_identifier}".strip(),
            value=ratio(p.disbursed, p.committed), unit="ratio",
            formula="cumulative disbursed / net commitment (same agreement, same currency)",
            inputs=[{"name": "disbursed", "value": _s(p.disbursed), "currency": p.currency, "basis": p.disbursed_basis},
                    {"name": "committed", "value": _s(p.committed), "currency": p.currency, "basis": p.committed_basis},
                    {"name": "source_record_ids", "value": p.source_record_ids}],
            as_of=p.disbursed_as_of.isoformat() if p.disbursed_as_of else None,
            limitations=["Published cumulative figures may be rounded (World Bank: US$ millions, 2 decimals)."]
            if p.disbursed_basis and "millions" in p.disbursed_basis else [],
            missing_inputs=missing,
        ))
    # Elapsed implementation time
    start = project.implementation_start_date or project.original_approval_date
    closings = [a.closing_date_current for a in agreements if a.closing_date_current]
    end = project.revised_completion_date or project.original_completion_date or (max(closings) if closings else None)
    elapsed = None
    if start and end and end > start:
        elapsed = ratio(Decimal((min(today, end) - start).days), Decimal((end - start).days))
    indicators.append(Indicator(
        code="elapsed_time_ratio", label="Share of planned implementation period elapsed", value=elapsed, unit="ratio",
        formula="(min(today, planned end) - start) / (planned end - start)",
        inputs=[{"name": "start", "value": _s(start)}, {"name": "planned_end", "value": _s(end)}, {"name": "today", "value": today.isoformat()}],
        as_of=today.isoformat(), missing_inputs=[n for n, v in (("start date", start), ("planned end date", end)) if v is None],
        limitations=["Uses the current planned end date published by the source, which may already include extensions."],
    ))
    # Schedule slippage
    slip = None
    if project.original_completion_date and project.revised_completion_date:
        slip = Decimal((project.revised_completion_date - project.original_completion_date).days)
    indicators.append(Indicator(
        code="schedule_slippage_days", label="Completion date slippage", value=slip, unit="days",
        formula="revised completion date - original completion date",
        missing_inputs=[n for n, v in (("original completion date", project.original_completion_date),
                                       ("revised completion date", project.revised_completion_date)) if v is None],
    ))
    # Cost overrun
    overrun = None
    if project.original_estimated_cost and project.revised_estimated_cost:
        overrun = ratio(project.revised_estimated_cost - project.original_estimated_cost, project.original_estimated_cost)
    indicators.append(Indicator(
        code="cost_overrun", label="Cost revision", value=overrun, unit="ratio",
        formula="(revised estimated cost - original estimated cost) / original estimated cost (same currency)",
        inputs=[{"name": "original", "value": _s(project.original_estimated_cost), "currency": project.cost_currency},
                {"name": "revised", "value": _s(project.revised_estimated_cost), "currency": project.cost_currency}],
        missing_inputs=[n for n, v in (("original estimated cost", project.original_estimated_cost),
                                       ("revised estimated cost", project.revised_estimated_cost)) if v is None],
    ))
    # Financing gap (only when cost and commitments share the cost currency)
    cost = project.revised_estimated_cost or project.original_estimated_cost
    gap = None
    gap_missing = []
    counterpart = db.scalars(select(CounterpartFinancing).where(CounterpartFinancing.project_id == project.id)).all()
    if cost is None:
        gap_missing.append("project cost estimate")
    elif project.cost_currency not in by_cur and not counterpart:
        gap_missing.append(f"commitments in {project.cost_currency}")
    else:
        committed_same = by_cur.get(project.cost_currency, {}).get("committed") or Decimal(0)
        cp = sum((c.amount for c in counterpart if c.amount is not None and c.currency == project.cost_currency), Decimal(0))
        gap = cost - committed_same - cp
    indicators.append(Indicator(
        code="financing_gap", label="Financing gap", value=gap, unit=project.cost_currency or "",
        formula="project cost - external commitments - counterpart financing (all in the cost currency)",
        missing_inputs=gap_missing,
        limitations=["Commitments in other currencies are not converted for this indicator."],
    ))
    # Contract amendment ratio
    contracts = db.scalars(select(Contract).where(Contract.project_id == project.id)).all()
    orig = sum((c.original_amount for c in contracts if c.original_amount is not None), Decimal(0)) if contracts else None
    amend_total = None
    amend_count = 0
    if contracts:
        amends = db.scalars(select(ContractAmendment).where(ContractAmendment.contract_id.in_([c.id for c in contracts]))).all()
        amend_count = len(amends)
        amend_total = sum((a.amount_change for a in amends if a.amount_change is not None), Decimal(0))
    indicators.append(Indicator(
        code="contract_amendment_ratio", label="Contract amendment ratio", value=ratio(amend_total, orig), unit="ratio",
        formula="sum of amendment amounts / sum of original contract amounts",
        inputs=[{"name": "amendments_count", "value": amend_count}],
        missing_inputs=[] if contracts else ["contract data"],
    ))
    # Physical vs financial progress
    latest = db.scalar(select(ImplementationProgress).where(ImplementationProgress.project_id == project.id)
                       .order_by(ImplementationProgress.report_date.desc()))
    phys = project.physical_progress_pct if project.physical_progress_pct is not None else (latest.physical_progress_pct if latest else None)
    fin_rates = [ratio(p.disbursed, p.committed) for p in positions if not p.is_guarantee]
    fin_rates = [r for r in fin_rates if r is not None]
    fin_pct = None
    if len(fin_rates) == 1:
        fin_pct = fin_rates[0] * 100
    elif len(by_cur) == 1:
        cur = next(iter(by_cur.values()))
        r = ratio(cur["disbursed"], cur["committed"])
        fin_pct = r * 100 if r is not None else None
    gap_pts = (phys - fin_pct).quantize(Decimal("0.01")) if phys is not None and fin_pct is not None else None
    indicators.append(Indicator(
        code="physical_financial_gap", label="Physical minus financial progress", value=gap_pts, unit="percentage points",
        formula="physical progress (%) - disbursement rate (%)",
        missing_inputs=[n for n, v in (("physical progress", phys), ("financial progress", fin_pct)) if v is None],
    ))

    return {
        "project_id": project.id,
        "agreements": [{**asdict(p), **{k: _s(getattr(p, k)) for k in ("committed", "cancelled", "disbursed", "undisbursed", "expenditure")},
                        "disbursed_as_of": _s(p.disbursed_as_of)} for p in positions],
        "totals_by_currency": {cur: {k: _s(v) for k, v in vals.items()} for cur, vals in by_cur.items()},
        "indicators": [i.to_dict() for i in indicators],
        "note": "Totals are per currency; currencies are never added together here.",
    }


def annual_flows(db: Session, project: Project) -> list[dict]:
    """Disbursements and commitments by calendar year and currency (dated transactions only)."""
    agreements = db.scalars(select(FinancingAgreement.id).where(FinancingAgreement.project_id == project.id)).all()
    if not agreements:
        return []
    out: dict[tuple[int, str, str], Decimal] = defaultdict(Decimal)
    for f in db.scalars(select(Disbursement).where(Disbursement.agreement_id.in_(agreements), Disbursement.is_counted.is_(True))):
        year = f.value_date.year if f.value_date else f.period_year
        if year:
            out[(year, f.currency, f.flow_type)] += f.amount
    for c in db.scalars(select(FinancingCommitment).where(FinancingCommitment.agreement_id.in_(agreements),
                                                          FinancingCommitment.is_counted.is_(True))):
        if c.value_date:
            out[(c.value_date.year, c.currency, "commitment")] += c.amount
    return [{"year": y, "currency": cur, "flow": flow, "amount": str(v)} for (y, cur, flow), v in sorted(out.items())]


def _s(v) -> str | None:
    if v is None:
        return None
    if isinstance(v, (Decimal, date)):
        return str(v) if isinstance(v, Decimal) else v.isoformat()
    return str(v)
