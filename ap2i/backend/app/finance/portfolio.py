"""Annual project portfolios (Master prompt §17).

Counting rules (METHODOLOGY_VERSION "1.0"), published on the methodology page:
  * A project is counted at most ONCE per category per year, whatever its number of financings.
  * approved(Y): the project's first approval date (project approval, else earliest financing
    approval) falls in Y. Additional financing does not create a new approved project.
  * active(Y): start <= 31 Dec Y and end >= 1 Jan Y, where start = implementation start or approval
    and end = actual completion, else current planned completion/closing. Projects lacking a start
    date are reported as "undated", never guessed into a year.
  * completed(Y): actual completion date in Y; if absent, a closed/completed project whose current
    closing date is in Y (flagged as "closing date used as completion proxy").
  * commissioned(Y): commissioning date in Y (only from documented observations).
  * suspended/cancelled(Y): only when the status change is dated in Y; otherwise "not determinable".
  * commitments(Y) / disbursements(Y) / expenditures(Y): sums of counted, dated transactions whose
    value date is in Y (transaction year, not publication year), per original currency, plus a
    USD conversion at the year-Y annual average rate where a rate exists.
  * Cumulative "disbursed to date" figures (e.g. World Bank) are NOT spread over years.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.finance.fx import FX
from app.models import (
    AnnualFinancialSnapshot,
    Country,
    Disbursement,
    FinancingAgreement,
    FinancingCommitment,
    Project,
    ProjectStatusHistory,
)

METHODOLOGY_VERSION = "1.0"


def _dates(p: Project) -> tuple[date | None, date | None, bool]:
    approval_candidates = [a.approval_date for a in p.agreements if a.approval_date]
    approval = p.original_approval_date or (min(approval_candidates) if approval_candidates else None)
    start = p.implementation_start_date or approval
    closing = [a.closing_date_current for a in p.agreements if a.closing_date_current]
    end = p.actual_completion_date or p.revised_completion_date or p.original_completion_date or (max(closing) if closing else None)
    return approval, start, bool(end)


def _end(p: Project) -> date | None:
    closing = [a.closing_date_current for a in p.agreements if a.closing_date_current]
    return p.actual_completion_date or p.revised_completion_date or p.original_completion_date or (max(closing) if closing else None)


def visible_projects_query(country_id: int, tenant_id: int | None = None, include_private: bool = False):
    q = select(Project).where(Project.country_id == country_id, Project.merged_into_id.is_(None), Project.is_synthetic.is_(False))
    if include_private and tenant_id is not None:
        q = q.where((Project.tenant_id.is_(None)) | (Project.tenant_id == tenant_id))
    else:
        q = q.where(Project.tenant_id.is_(None))
    return q


def compute_year(db: Session, country: Country, year: int, projects: list[Project], fx: FX,
                 partner_names: dict[int, str], sector_names: dict[int, str]) -> dict:
    y0, y1 = date(year, 1, 1), date(year, 12, 31)
    approved, active, completed, completed_proxy, commissioned, undated = [], [], [], [], [], []
    for p in projects:
        approval, start, _ = _dates(p)
        end = _end(p)
        if approval and approval.year == year:
            approved.append(p)
        if start is None:
            undated.append(p)
        elif start <= y1 and (end is None and p.status in ("active", "approved") or (end is not None and end >= y0)):
            active.append(p)
        if p.actual_completion_date and p.actual_completion_date.year == year:
            completed.append(p)
        elif p.actual_completion_date is None and p.status in ("closed", "completed") and end and end.year == year:
            completed_proxy.append(p)
        if p.commissioning_date and p.commissioning_date.year == year:
            commissioned.append(p)

    ids = [p.id for p in projects]
    hist = db.scalars(select(ProjectStatusHistory).where(ProjectStatusHistory.project_id.in_(ids),
                                                         ProjectStatusHistory.effective_date.is_not(None))).all() if ids else []
    suspended = sorted({h.project_id for h in hist if h.status == "suspended" and h.effective_date.year == year})
    cancelled = sorted({h.project_id for h in hist if h.status in ("cancelled", "dropped") and h.effective_date.year == year})

    agr_by_project = {p.id: p.agreements for p in projects}
    agr_ids = [a.id for ags in agr_by_project.values() for a in ags]
    agr_index = {a.id: (p, a) for p in projects for a in p.agreements}

    def flows(model, extra=None):
        if not agr_ids:
            return []
        in_year = (model.value_date >= y0) & (model.value_date <= y1)
        if model is Disbursement:
            in_year = in_year | (model.value_date.is_(None) & (model.period_year == year))
        q = select(model).where(model.agreement_id.in_(agr_ids), model.is_counted.is_(True), in_year)
        if extra is not None:
            q = q.where(extra)
        return db.scalars(q).all()

    def summarize(rows) -> dict:
        by_cur: dict[str, Decimal] = defaultdict(Decimal)
        usd = Decimal(0)
        usd_complete = True
        unconverted: dict[str, Decimal] = defaultdict(Decimal)
        rate_sources = set()
        by_sector: dict[str, Decimal] = defaultdict(Decimal)
        by_partner: dict[str, Decimal] = defaultdict(Decimal)
        projects_ids = set()
        for r in rows:
            by_cur[r.currency] += r.amount
            p, a = agr_index[r.agreement_id]
            projects_ids.add(p.id)
            conv = fx.convert(r.amount, r.currency, "USD", year)
            if conv.value is None:
                usd_complete = False
                unconverted[r.currency] += r.amount
            else:
                usd += conv.value
                if conv.source and conv.source != "identity":
                    rate_sources.add(conv.source)
                by_sector[sector_names.get(p.sector_id, "Unclassified")] += conv.value
                by_partner[partner_names.get(a.partner_id, "Unknown")] += conv.value
        return {
            "by_currency": {k: str(v) for k, v in sorted(by_cur.items())},
            "usd_equivalent": str(usd.quantize(Decimal("0.01"))) if rows else None,
            "usd_complete": usd_complete,
            "unconverted": {k: str(v) for k, v in unconverted.items()},
            "rate_sources": sorted(rate_sources),
            "usd_by_sector": {k: str(v.quantize(Decimal('0.01'))) for k, v in sorted(by_sector.items())},
            "usd_by_partner": {k: str(v.quantize(Decimal('0.01'))) for k, v in sorted(by_partner.items())},
            "transactions": len(rows),
            "projects": len(projects_ids),
            "transaction_ids": sorted(r.id for r in rows),
        }

    commitments = summarize(flows(FinancingCommitment))
    disbursements = summarize(flows(Disbursement, Disbursement.flow_type == "disbursement"))
    expenditures = summarize(flows(Disbursement, Disbursement.flow_type == "expenditure"))

    def breakdown(items: list[Project]) -> dict:
        by_sector: dict[str, int] = defaultdict(int)
        by_partner: dict[str, int] = defaultdict(int)
        by_ministry: dict[str, int] = defaultdict(int)
        by_region: dict[str, int] = defaultdict(int)
        by_instrument: dict[str, int] = defaultdict(int)
        for p in items:
            by_sector[sector_names.get(p.sector_id, "Unclassified")] += 1
            for name in sorted({partner_names.get(a.partner_id, "Unknown") for a in p.agreements}) or ["No financing record"]:
                by_partner[name] += 1
            by_ministry[(p.executing_agency or "Not reported")[:80]] += 1
            by_region[p.region.name_fr if p.region else "Not reported / national"] += 1
            for ins in sorted({a.instrument.name_en if a.instrument else (a.instrument_label or "Not reported") for a in p.agreements}) or ["No financing record"]:
                by_instrument[ins] += 1
        top = lambda d: dict(sorted(d.items(), key=lambda kv: (-kv[1], kv[0])))  # noqa: E731
        return {"by_sector": top(by_sector), "by_partner": top(by_partner), "by_ministry": dict(list(top(by_ministry).items())[:25]),
                "by_region": top(by_region), "by_instrument": top(by_instrument)}

    status_counts: dict[str, int] = defaultdict(int)
    for p in active:
        status_counts[p.status] += 1
    return {
        "country": country.iso3,
        "year": year,
        "methodology_version": METHODOLOGY_VERSION,
        "counts": {
            "approved": len(approved),
            "active": len(active),
            "completed": len(completed),
            "completed_closing_date_proxy": len(completed_proxy),
            "commissioned": len(commissioned),
            "suspended": len(suspended) if hist else None,
            "cancelled": len(cancelled) if hist else None,
            "undated_projects_excluded": len(undated),
        },
        "project_ids": {
            "approved": sorted(p.id for p in approved), "active": sorted(p.id for p in active),
            "completed": sorted(p.id for p in completed + completed_proxy), "commissioned": sorted(p.id for p in commissioned),
        },
        "commitments": commitments,
        "disbursements": disbursements,
        "expenditures": expenditures,
        "active_breakdown": breakdown(active),
        "approved_breakdown": breakdown(approved),
        "active_status_mix": dict(status_counts),
        "notes": [
            "Suspended/cancelled counts require dated status changes; null = not determinable from the sources." if not hist else "",
            "Operational performance requires documented operational-status observations; none are inferred.",
            "Cumulative 'disbursed to date' figures published without dates are not allocated to years.",
        ],
    }


def compute_portfolio(db: Session, country_iso3: str, first_year: int, last_year: int, tenant_id: int | None = None,
                      sector_id: int | None = None, partner_id: int | None = None) -> dict:
    country = db.scalar(select(Country).where(Country.iso3 == country_iso3.upper()))
    if country is None:
        raise ValueError(f"Unknown country {country_iso3}")
    q = visible_projects_query(country.id, tenant_id, include_private=tenant_id is not None).options(
        selectinload(Project.agreements).selectinload(FinancingAgreement.instrument), selectinload(Project.region))
    if sector_id:
        q = q.where(Project.sector_id == sector_id)
    projects = list(db.scalars(q).unique())
    if partner_id:
        projects = [p for p in projects if any(a.partner_id == partner_id for a in p.agreements)]
    from app.models import FinancingPartner, Sector

    partner_names = {p.id: p.short_name for p in db.scalars(select(FinancingPartner))}
    sector_names = {s.id: s.name_en for s in db.scalars(select(Sector))}
    fx = FX(db)
    if not projects:
        # No imported records: say so instead of showing a portfolio of zeros.
        return {"country": country.iso3, "first_year": first_year, "last_year": last_year, "has_data": False,
                "methodology_version": METHODOLOGY_VERSION, "projects_in_scope": 0,
                "filters": {"sector_id": sector_id, "partner_id": partner_id, "tenant_id": tenant_id}, "years": [],
                "coverage_note": "No project records have been imported for this selection. This is absence of data, "
                                 "not absence of investment."}
    years = [compute_year(db, country, y, projects, fx, partner_names, sector_names) for y in range(first_year, last_year + 1)]
    return {
        "country": country.iso3, "first_year": first_year, "last_year": last_year, "has_data": True,
        "methodology_version": METHODOLOGY_VERSION, "projects_in_scope": len(projects),
        "filters": {"sector_id": sector_id, "partner_id": partner_id, "tenant_id": tenant_id},
        "years": years,
        "coverage_note": ("Coverage is limited to the sources imported into AP²I (see /data-quality). It is NOT the "
                          "complete national public-investment portfolio."),
    }


def fingerprint(db: Session, country_id: int) -> str:
    """Hash of the inputs a snapshot depends on (project, agreement and flow state)."""
    parts = []
    for model, cols in ((Project, (Project.id, Project.updated_at, Project.status, Project.merged_into_id)),
                        (FinancingAgreement, (FinancingAgreement.id, FinancingAgreement.updated_at, FinancingAgreement.project_id))):
        q = select(*cols)
        if model is Project:
            q = q.where(Project.country_id == country_id)
        else:
            q = q.join(Project, Project.id == FinancingAgreement.project_id).where(Project.country_id == country_id)
        parts.append([tuple(str(x) for x in r) for r in db.execute(q.order_by(cols[0])).all()])
    for model in (FinancingCommitment, Disbursement):
        q = (select(func.count(model.id), func.coalesce(func.sum(model.amount), 0), func.max(model.id))
             .join(FinancingAgreement, FinancingAgreement.id == model.agreement_id)
             .join(Project, Project.id == FinancingAgreement.project_id)
             .where(Project.country_id == country_id, model.is_counted.is_(True)))
        parts.append([str(x) for x in db.execute(q).one()])
    return hashlib.sha256(json.dumps(parts, default=str).encode()).hexdigest()


def snapshot_portfolio(db: Session, country_iso3: str, first_year: int, last_year: int, note: str | None = None) -> list[AnnualFinancialSnapshot]:
    """Persist one snapshot per year; earlier snapshots are kept (is_current=False), never deleted."""
    country = db.scalar(select(Country).where(Country.iso3 == country_iso3.upper()))
    fp = fingerprint(db, country.id)
    portfolio = compute_portfolio(db, country_iso3, first_year, last_year)
    out = []
    for y in portfolio["years"]:
        current = db.scalar(select(AnnualFinancialSnapshot).where(
            AnnualFinancialSnapshot.country_id == country.id, AnnualFinancialSnapshot.year == y["year"],
            AnnualFinancialSnapshot.is_current.is_(True)))
        if current is not None and current.input_fingerprint == fp and current.methodology_version == METHODOLOGY_VERSION:
            out.append(current)
            continue
        if current is not None:
            current.is_current = False
        snap = AnnualFinancialSnapshot(country_id=country.id, year=y["year"], methodology_version=METHODOLOGY_VERSION,
                                       input_fingerprint=fp, payload=y, is_current=True, note=note)
        db.add(snap)
        out.append(snap)
    db.commit()
    return out
