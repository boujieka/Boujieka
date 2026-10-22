"""Read API: reference data, Africa map, projects, portfolios, sectors, financing, alerts, explorer."""

from __future__ import annotations

import csv
import io
from collections import defaultdict
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.api.serial import j, project_summary, row
from app.config import get_settings
from app.db import get_db
from app.finance.fx import FX
from app.finance.indicators import agreement_position, annual_flows, project_financials
from app.finance.portfolio import compute_portfolio, visible_projects_query
from app.models import (
    AdminRegion,
    AnnualFinancialSnapshot,
    Country,
    CountryDataSource,
    DataQualityAssessment,
    DataValidation,
    Disbursement,
    Document,
    ExchangeRate,
    FinancingAgreement,
    FinancingCommitment,
    FinancingInstrument,
    FinancingPartner,
    ImplementationProgress,
    MatchCandidate,
    Project,
    ProjectAlert,
    ProjectAlias,
    ProjectIdentifier,
    ProjectLocation,
    ProjectSourceLink,
    ProjectStatusHistory,
    ResultsIndicator,
    ResultsObservation,
    Sector,
    SectorIndicator,
    SourceConnector,
    SourceObservation,
    SourceRecord,
)
from app.performance.alerts import RULES, thresholds
from app.performance.quality import dashboard as dq_dashboard
from app.security.deps import Principal, get_principal, require_user, tenant_filter, visible_project_or_404

router = APIRouter(tags=["data"])


def _country(db: Session, iso3: str) -> Country:
    c = db.scalar(select(Country).where(Country.iso3 == iso3.upper()))
    if c is None:
        raise HTTPException(404, "Unknown country")
    return c


# --- reference ----------------------------------------------------------------------------------

@router.get("/countries")
def countries(db: Session = Depends(get_db)):
    counts = dict(db.execute(select(Project.country_id, func.count(Project.id)).where(
        Project.merged_into_id.is_(None), Project.tenant_id.is_(None)).group_by(Project.country_id)).all())
    out = []
    for c in db.scalars(select(Country).order_by(Country.name_en)):
        out.append({**row(c, ["iso2", "iso3", "iso_numeric", "name_en", "name_fr", "region", "subregion", "currency",
                              "official_languages", "is_active", "reference_status"]),
                    "documented_projects": counts.get(c.id, 0),
                    "data_coverage": "connected_sources" if counts.get(c.id) else "no_project_data"})
    return out


@router.get("/countries/{iso3}")
def country_detail(iso3: str, db: Session = Depends(get_db)):
    c = _country(db, iso3)
    return {**row(c, ["iso2", "iso3", "iso_numeric", "name_en", "name_fr", "region", "subregion", "currency", "official_languages",
                      "is_active", "reporting_config", "reference_status", "reference_note"]),
            "admin_divisions": [row(r, ["code", "name_en", "name_fr", "level", "division_type"])
                                for r in db.scalars(select(AdminRegion).where(AdminRegion.country_id == c.id).order_by(AdminRegion.code))],
            "data_sources": [row(s, ["name", "institution", "category", "url", "access_method", "reachability", "last_checked_at", "notes"])
                             for s in db.scalars(select(CountryDataSource).where(CountryDataSource.country_id == c.id))]}


@router.get("/sectors")
def sectors(db: Session = Depends(get_db)):
    out = []
    for s in db.scalars(select(Sector).options(selectinload(Sector.indicators)).order_by(Sector.sort_order)):
        out.append({**row(s, ["id", "code", "name_en", "name_fr"]),
                    "indicators": [row(i, ["code", "name_en", "name_fr", "unit", "kind"]) for i in s.indicators]})
    return out


@router.get("/partners")
def partners(db: Session = Depends(get_db)):
    conns = {c.key: c for c in db.scalars(select(SourceConnector))}
    out = []
    for p in db.scalars(select(FinancingPartner).order_by(FinancingPartner.tier, FinancingPartner.code)):
        c = conns.get(p.connector_key or "")
        out.append({**row(p, ["id", "code", "name", "short_name", "partner_type", "tier", "iati_org_refs", "website", "notes"]),
                    "connector": {"key": c.key, "status": c.status, "enabled": c.enabled} if c else None})
    return out


@router.get("/instruments")
def instruments(db: Session = Depends(get_db)):
    return [row(i, ["code", "name_en", "name_fr"]) for i in db.scalars(select(FinancingInstrument))]


# --- Africa map ----------------------------------------------------------------------------------

@router.get("/africa/overview")
def africa_overview(year: int | None = None, sector: str | None = None, partner: str | None = None, instrument: str | None = None,
                    status: str | None = None, verification: str | None = None, db: Session = Depends(get_db)):
    """One row per country. Countries without imported records get null statistics (never zeros)."""
    q = select(Project).where(Project.merged_into_id.is_(None), Project.tenant_id.is_(None), Project.is_synthetic.is_(False)).options(
        selectinload(Project.agreements).selectinload(FinancingAgreement.instrument), selectinload(Project.sector))
    if sector:
        q = q.join(Sector, Sector.id == Project.sector_id).where(Sector.code == sector)
    if status:
        q = q.where(Project.status == status)
    if verification:
        q = q.where(Project.verification_status == verification)
    projects = list(db.scalars(q).unique())
    pid = db.scalar(select(FinancingPartner.id).where(FinancingPartner.code == partner.upper())) if partner else None
    if pid:
        projects = [p for p in projects if any(a.partner_id == pid for a in p.agreements)]
    if instrument:
        projects = [p for p in projects if any(a.instrument and a.instrument.code == instrument for a in p.agreements)]
    if year:
        def in_year(p):
            ds = [a.approval_date for a in p.agreements if a.approval_date]
            start = p.implementation_start_date or p.original_approval_date or (min(ds) if ds else None)
            ends = [a.closing_date_current for a in p.agreements if a.closing_date_current]
            end = p.actual_completion_date or p.original_completion_date or (max(ends) if ends else None)
            return start is not None and start.year <= year and (end is None or end.year >= year)
        projects = [p for p in projects if in_year(p)]
    alerts = set(db.scalars(select(ProjectAlert.project_id).where(ProjectAlert.is_active.is_(True),
                                                                  ProjectAlert.level.in_(("high_attention", "critical_attention")))))
    by_country: dict[int, list[Project]] = defaultdict(list)
    for p in projects:
        by_country[p.country_id].append(p)
    fx = FX(db)
    out = []
    for c in db.scalars(select(Country).order_by(Country.name_en)):
        items = by_country.get(c.id, [])
        last = db.scalar(select(func.max(Project.last_source_update_at)).where(Project.country_id == c.id)) if items else None
        entry = {"iso3": c.iso3, "iso2": c.iso2, "iso_numeric": c.iso_numeric, "name_en": c.name_en, "name_fr": c.name_fr,
                 "is_active": c.is_active, "has_data": bool(items)}
        if not items:
            entry.update({k: None for k in ("documented_projects", "commitments_usd", "commitments_by_currency", "disbursements_usd",
                                            "under_implementation", "completed", "operational", "requiring_attention", "last_update")})
            entry["data_coverage"] = "No project records imported"
        else:
            commits: dict[str, Decimal] = defaultdict(Decimal)
            disb: dict[str, Decimal] = defaultdict(Decimal)
            usd_c = usd_d = Decimal(0)
            unconv = 0
            for p in items:
                for a in p.agreements:
                    pos = agreement_position(db, a)
                    if pos.committed is not None and pos.currency:
                        commits[pos.currency] += pos.committed
                        yr = (a.approval_date or p.original_approval_date or date.today()).year
                        cv = fx.convert(pos.committed, pos.currency, "USD", yr)
                        usd_c += cv.value or 0
                        unconv += cv.value is None
                    if pos.disbursed is not None and pos.currency:
                        disb[pos.currency] += pos.disbursed
            entry.update({
                "documented_projects": len(items),
                "commitments_by_currency": {k: str(v) for k, v in commits.items()},
                "commitments_usd": str(usd_c.quantize(Decimal("1"))),
                "commitments_usd_note": "Each agreement converted at the annual average rate of its approval year; "
                                        f"{unconv} agreement(s) could not be converted (rate missing).",
                "disbursements_by_currency": {k: str(v) for k, v in disb.items()},
                "under_implementation": sum(1 for p in items if p.status == "active"),
                "completed": sum(1 for p in items if p.status in ("completed", "closed")),
                "operational": sum(1 for p in items if p.operational_status == "operational"),
                "operational_unknown": sum(1 for p in items if p.status in ("completed", "closed") and p.operational_status == "unknown"),
                "requiring_attention": sum(1 for p in items if p.id in alerts),
                "last_update": j(last),
                "data_coverage": "Connected sources only (see data quality page)",
            })
        out.append(entry)
    return {"countries": out, "filters": {"year": year, "sector": sector, "partner": partner, "instrument": instrument,
                                          "status": status, "verification": verification}}


# --- projects --------------------------------------------------------------------------------------

def _project_filter_query(db: Session, principal: Principal, country: str | None, sector: str | None, partner: str | None,
                          status: str | None, year_from: int | None, year_to: int | None, q: str | None, region: str | None,
                          verification: str | None, has_alerts: bool | None):
    stmt = select(Project).where(Project.merged_into_id.is_(None), tenant_filter(Project, principal))
    if country:
        stmt = stmt.where(Project.country_id == _country(db, country).id)
    if sector:
        stmt = stmt.join(Sector, Sector.id == Project.sector_id).where(Sector.code == sector)
    if status:
        stmt = stmt.where(Project.status.in_(status.split(",")))
    if verification:
        stmt = stmt.where(Project.verification_status == verification)
    if region:
        stmt = stmt.join(AdminRegion, AdminRegion.id == Project.region_id).where(AdminRegion.code == region)
    if partner:
        sub = select(FinancingAgreement.project_id).join(FinancingPartner, FinancingPartner.id == FinancingAgreement.partner_id).where(
            FinancingPartner.code == partner.upper())
        stmt = stmt.where(Project.id.in_(sub))
    if year_from or year_to:
        appr = func.coalesce(Project.original_approval_date, select(func.min(FinancingAgreement.approval_date)).where(
            FinancingAgreement.project_id == Project.id).scalar_subquery())
        if year_from:
            stmt = stmt.where(appr >= date(year_from, 1, 1))
        if year_to:
            stmt = stmt.where(appr <= date(year_to, 12, 31))
    if q:
        like = f"%{q.strip()[:100]}%"
        stmt = stmt.where(or_(Project.title.ilike(like), Project.ap2i_id.ilike(like), Project.executing_agency.ilike(like),
                              Project.id.in_(select(ProjectAlias.project_id).where(ProjectAlias.alias.ilike(like))),
                              Project.id.in_(select(FinancingAgreement.project_id).where(FinancingAgreement.source_identifier.ilike(like)))))
    if has_alerts:
        stmt = stmt.where(Project.id.in_(select(ProjectAlert.project_id).where(ProjectAlert.is_active.is_(True))))
    return stmt


@router.get("/projects")
def list_projects(country: str | None = None, sector: str | None = None, partner: str | None = None, status: str | None = None,
                  year_from: int | None = None, year_to: int | None = None, q: str | None = None, region: str | None = None,
                  verification: str | None = None, has_alerts: bool | None = None, sort: str = "ap2i_id",
                  limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0),
                  principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    stmt = _project_filter_query(db, principal, country, sector, partner, status, year_from, year_to, q, region, verification, has_alerts)
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    order = {"ap2i_id": Project.ap2i_id, "approval": Project.original_approval_date.desc().nulls_last(),
             "title": Project.title, "updated": Project.last_source_update_at.desc().nulls_last()}.get(sort, Project.ap2i_id)
    items = db.scalars(stmt.options(selectinload(Project.agreements).selectinload(FinancingAgreement.partner),
                                    selectinload(Project.sector), selectinload(Project.region), selectinload(Project.country))
                       .order_by(order).offset(offset).limit(limit)).unique().all()
    alert_counts = dict(db.execute(select(ProjectAlert.project_id, func.count()).where(
        ProjectAlert.is_active.is_(True), ProjectAlert.project_id.in_([p.id for p in items])).group_by(ProjectAlert.project_id)).all())
    out = []
    for p in items:
        d = project_summary(p)
        d["active_alerts"] = alert_counts.get(p.id, 0)
        cur: dict[str, Decimal] = defaultdict(Decimal)
        for a in p.agreements:
            pos = agreement_position(db, a)
            if pos.committed is not None and pos.currency:
                cur[pos.currency] += pos.committed
        d["committed_by_currency"] = {k: str(v) for k, v in cur.items()}
        out.append(d)
    return {"total": total, "limit": limit, "offset": offset, "items": out}


@router.get("/projects/export.csv")
def export_projects(request: Request, country: str | None = None, sector: str | None = None, partner: str | None = None,
                    status: str | None = None, year_from: int | None = None, year_to: int | None = None, q: str | None = None,
                    principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    """CSV export of the project registry (one row per financing agreement). Registered users: 1,000 rows;
    plans with the `exports` feature: unlimited."""
    from app.security.deps import audit

    stmt = _project_filter_query(db, principal, country, sector, partner, status, year_from, year_to, q, None, None, None)
    cap = None if principal.has_feature("exports") else 1000
    projects = db.scalars(stmt.options(selectinload(Project.agreements).selectinload(FinancingAgreement.partner),
                                       selectinload(Project.sector), selectinload(Project.country)).order_by(Project.ap2i_id)).unique().all()
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["# AP²I project export", f"generated {date.today().isoformat()}", "connected sources only — not complete national coverage"])
    w.writerow(["ap2i_id", "country", "title", "sector", "status", "operational_status", "verification_status", "approval_date",
                "start_date", "planned_end", "actual_end", "executing_agency", "partner", "source_identifier", "currency",
                "committed", "committed_basis", "disbursed", "disbursed_as_of", "disbursed_basis", "source_url"])
    n = 0
    for p in projects:
        for a in p.agreements or [None]:
            pos = agreement_position(db, a) if a else None
            src = db.get(SourceRecord, a.source_record_id) if a and a.source_record_id else None
            w.writerow([p.ap2i_id, p.country.iso3, p.title, p.sector.code if p.sector else "", p.status, p.operational_status,
                        p.verification_status, j(p.original_approval_date) or "", j(p.implementation_start_date) or "",
                        j(p.original_completion_date) or "", j(p.actual_completion_date) or "", p.executing_agency or "",
                        a.partner.short_name if a and a.partner else "", a.source_identifier if a else "",
                        pos.currency if pos else "", j(pos.committed) if pos else "", pos.committed_basis if pos else "",
                        j(pos.disbursed) if pos else "", j(pos.disbursed_as_of) if pos else "", pos.disbursed_basis if pos else "",
                        src.source_url if src else ""])
            n += 1
            if cap and n >= cap:
                break
        if cap and n >= cap:
            w.writerow([f"# truncated at {cap} rows — the Professional plan includes full exports"])
            break
    audit(db, request, "export.projects_csv", principal, detail={"rows": n})
    db.commit()
    return StreamingResponse(iter([buf.getvalue().encode("utf-8-sig")]), media_type="text/csv",
                             headers={"Content-Disposition": 'attachment; filename="ap2i_projects.csv"'})


@router.get("/projects/{ref}")
def project_detail(ref: str, principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    p = visible_project_or_404(db, ref, principal)
    detailed = principal.can("read:detail")
    d = project_summary(p)
    d.update(row(p, ["description", "objectives", "title_language", "funding_type", "supervising_ministry", "implementing_agency",
                     "project_owner", "original_estimated_cost", "revised_estimated_cost", "cost_currency", "revised_completion_date",
                     "commissioning_date", "physical_progress_pct", "physical_progress_date", "expected_beneficiaries",
                     "actual_beneficiaries", "development_results", "status_source", "last_verified_at", "created_at"]))
    d["aliases"] = [{"alias": a.alias, "language": a.language} for a in p.aliases]
    d["identifiers"] = [{"scheme": s, "identifier": i} for s, i in db.execute(
        select(ProjectIdentifier.scheme, ProjectIdentifier.identifier).where(ProjectIdentifier.project_id == p.id)).all()]
    fin = project_financials(db, p)
    agreements = []
    for a in db.scalars(select(FinancingAgreement).where(FinancingAgreement.project_id == p.id).options(
            selectinload(FinancingAgreement.partner), selectinload(FinancingAgreement.instrument))):
        src = db.get(SourceRecord, a.source_record_id) if a.source_record_id else None
        agreements.append({**row(a, ["id", "source_identifier", "name", "instrument_label", "approval_date", "signature_date",
                                     "closing_date_original", "closing_date_current", "status", "currency", "amount_original",
                                     "amount_label", "reported_current_commitment", "reported_cumulative_disbursed",
                                     "reported_undisbursed", "reported_cumulative_as_of", "reported_cumulative_label",
                                     "parent_source_identifier", "data_nature", "verification_status"]),
                           "partner": {"code": a.partner.code, "name": a.partner.short_name} if a.partner else None,
                           "instrument": a.instrument.name_en if a.instrument else None,
                           "source": {"record_id": src.id, "url": src.source_url, "connector": src.connector.key,
                                      "retrieved_at": j(src.retrieved_at)} if src else None,
                           "commitments": [row(c, ["commitment_type", "amount", "currency", "value_date", "is_counted", "counting_note",
                                                   "source_record_id"]) for c in a.commitments],
                           "flows_count": len(a.disbursements)})
    d["agreements"] = agreements
    d["financials"] = fin
    d["annual_flows"] = annual_flows(db, p)
    links = db.scalars(select(ProjectSourceLink).where(ProjectSourceLink.project_id == p.id, ProjectSourceLink.active.is_(True))).all()
    d["sources"] = []
    for lk in links:
        sr = db.get(SourceRecord, lk.source_record_id)
        d["sources"].append({"record_id": sr.id, "connector": sr.connector.key, "connector_name": sr.connector.name,
                             "source_identifier": sr.source_identifier, "url": sr.source_url, "retrieved_at": j(sr.retrieved_at),
                             "source_last_updated": sr.source_last_updated, "link_type": lk.link_type, "match_rule": lk.match_rule,
                             "is_latest": sr.is_latest})
    d["documents"] = [row(x, ["id", "title", "doc_type", "url", "language", "published_date"]) for x in
                      db.scalars(select(Document).where(Document.project_id == p.id).order_by(Document.published_date.desc().nulls_last()))]
    d["locations"] = [{**row(x, ["place_name", "latitude", "longitude", "precision"]),
                       "region": x.region_id} for x in db.scalars(select(ProjectLocation).where(ProjectLocation.project_id == p.id))]
    d["status_history"] = [row(h, ["status", "previous_status", "effective_date", "recorded_at", "note", "source_record_id"])
                           for h in db.scalars(select(ProjectStatusHistory).where(ProjectStatusHistory.project_id == p.id)
                                               .order_by(ProjectStatusHistory.recorded_at))]
    d["alerts"] = [{**row(a, ["id", "rule_code", "level", "triggering_indicator", "observed_value", "threshold", "source",
                              "source_record_ids", "as_of", "explanation", "recommended_verification", "review_status"]),
                    "alert_id": a.public_id} for a in db.scalars(select(ProjectAlert).where(ProjectAlert.project_id == p.id,
                                                                                            ProjectAlert.is_active.is_(True)))]
    results = []
    for ind in db.scalars(select(ResultsIndicator).where(ResultsIndicator.project_id == p.id)):
        obs = db.scalars(select(ResultsObservation).where(ResultsObservation.indicator_id == ind.id)).all()
        results.append({**row(ind, ["name", "unit", "measure", "baseline_value", "target_value", "target_date"]),
                        "observations": [row(o, ["value", "value_text", "period_end", "data_nature"]) for o in obs]})
    d["results"] = results
    d["implementation_progress"] = [row(x, ["report_date", "physical_progress_pct", "financial_progress_pct", "narrative", "rating"])
                                    for x in db.scalars(select(ImplementationProgress).where(ImplementationProgress.project_id == p.id))]
    dqa = db.scalar(select(DataQualityAssessment).where(DataQualityAssessment.project_id == p.id, DataQualityAssessment.is_current.is_(True)))
    d["data_quality"] = row(dqa, ["completeness", "timeliness", "traceability", "consistency", "source_reliability", "duplicate_risk",
                                  "missing_fields", "assessed_at"]) if dqa else None
    d["validation_issues"] = [row(v, ["rule", "severity", "message", "status"]) for v in
                              db.scalars(select(DataValidation).where(DataValidation.project_id == p.id))]
    d["pending_match_candidates"] = db.scalar(select(func.count(MatchCandidate.id)).where(
        MatchCandidate.status == "pending", or_(MatchCandidate.project_a_id == p.id, MatchCandidate.project_b_id == p.id)))
    if detailed:
        d["observations"] = [row(o, ["field", "source_field", "value_text", "value_numeric", "value_date", "currency", "reporting_date",
                                     "extracted_at", "data_nature", "verification_status", "source_record_id"])
                             for o in db.scalars(select(SourceObservation).where(SourceObservation.project_id == p.id)
                                                 .order_by(SourceObservation.field).limit(500))]
    else:
        d["observations"] = None
        d["observations_note"] = "Field-level provenance is available on Professional and institutional plans."
    return d


@router.get("/projects/{ref}/flows")
def project_flows(ref: str, principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    p = visible_project_or_404(db, ref, principal)
    ag = {a.id: a for a in db.scalars(select(FinancingAgreement).where(FinancingAgreement.project_id == p.id))}
    out = []
    for f in db.scalars(select(Disbursement).where(Disbursement.agreement_id.in_(ag)).order_by(Disbursement.value_date)):
        out.append({**row(f, ["flow_type", "amount", "currency", "value_date", "is_counted", "source_record_id", "data_nature"]),
                    "agreement": ag[f.agreement_id].source_identifier})
    return out


@router.get("/sources/{record_id}")
def source_record(record_id: int, principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    sr = db.get(SourceRecord, record_id)
    if sr is None or (sr.tenant_id is not None and not (principal.is_super_admin or principal.organization_id == sr.tenant_id)):
        raise HTTPException(404, "Not found")
    d = row(sr, ["id", "source_identifier", "record_type", "country_iso3", "payload_format", "payload_sha256", "source_url",
                 "source_last_updated", "retrieved_at", "is_latest", "processing_status", "processing_note", "verification_status"])
    d["connector"] = {"key": sr.connector.key, "name": sr.connector.name, "usage_terms": sr.connector.usage_terms}
    if principal.can("read:detail"):
        d["payload"] = sr.payload
        d["raw_text"] = sr.raw_text[:200000] if sr.raw_text else None
    else:
        d["payload_note"] = "The verbatim source record is available on Professional and institutional plans."
    return d


# --- portfolios & dashboards ----------------------------------------------------------------------

@router.get("/countries/{iso3}/portfolio")
def portfolio(iso3: str, year_from: int = 2011, year_to: int = 2026, sector: str | None = None, partner: str | None = None,
              principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    if year_to - year_from > 40 or year_from > year_to:
        raise HTTPException(422, "Invalid year range")
    sector_id = db.scalar(select(Sector.id).where(Sector.code == sector)) if sector else None
    partner_id = db.scalar(select(FinancingPartner.id).where(FinancingPartner.code == partner.upper())) if partner else None
    tenant = principal.organization_id if principal.can("tenant:read") else None
    return compute_portfolio(db, iso3, year_from, year_to, tenant_id=tenant, sector_id=sector_id, partner_id=partner_id)


@router.get("/countries/{iso3}/portfolio/snapshots")
def portfolio_snapshots(iso3: str, year: int | None = None, include_superseded: bool = False, db: Session = Depends(get_db)):
    c = _country(db, iso3)
    q = select(AnnualFinancialSnapshot).where(AnnualFinancialSnapshot.country_id == c.id)
    if year:
        q = q.where(AnnualFinancialSnapshot.year == year)
    if not include_superseded:
        q = q.where(AnnualFinancialSnapshot.is_current.is_(True))
    return [{**row(s, ["id", "year", "computed_at", "methodology_version", "input_fingerprint", "is_current", "note"]),
             "counts": s.payload.get("counts"), "commitments_usd": s.payload.get("commitments", {}).get("usd_equivalent"),
             "disbursements_usd": s.payload.get("disbursements", {}).get("usd_equivalent")}
            for s in db.scalars(q.order_by(AnnualFinancialSnapshot.year, AnnualFinancialSnapshot.computed_at))]


@router.get("/snapshots/{snapshot_id}")
def snapshot(snapshot_id: int, db: Session = Depends(get_db)):
    s = db.get(AnnualFinancialSnapshot, snapshot_id)
    if s is None:
        raise HTTPException(404, "Not found")
    return row(s, ["id", "year", "computed_at", "methodology_version", "input_fingerprint", "is_current", "note", "payload"])


@router.get("/countries/{iso3}/dashboard")
def country_dashboard(iso3: str, principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    c = _country(db, iso3)
    base = visible_projects_query(c.id).options(selectinload(Project.agreements).selectinload(FinancingAgreement.partner),
                                                selectinload(Project.sector))
    projects = list(db.scalars(base).unique())
    by_status: dict[str, int] = defaultdict(int)
    by_sector: dict[str, dict] = {}
    by_partner: dict[str, dict] = {}
    fx = FX(db)
    for p in projects:
        by_status[p.status] += 1
        sk = p.sector.code if p.sector else "UNCLASSIFIED"
        s = by_sector.setdefault(sk, {"code": sk, "name_en": p.sector.name_en if p.sector else "Unclassified",
                                      "name_fr": p.sector.name_fr if p.sector else "Non classé", "projects": 0,
                                      "active": 0, "committed_usd": Decimal(0)})
        s["projects"] += 1
        s["active"] += p.status == "active"
        for a in p.agreements:
            pos = agreement_position(db, a)
            pk = a.partner.short_name if a.partner else "Unknown"
            pe = by_partner.setdefault(pk, {"partner": pk, "code": a.partner.code if a.partner else None, "agreements": 0,
                                            "committed_by_currency": defaultdict(Decimal), "disbursed_by_currency": defaultdict(Decimal),
                                            "committed_usd": Decimal(0)})
            pe["agreements"] += 1
            if pos.committed is not None and pos.currency:
                pe["committed_by_currency"][pos.currency] += pos.committed
                yr = (a.approval_date or p.original_approval_date or date.today()).year
                cv = fx.convert(pos.committed, pos.currency, "USD", yr).value
                if cv is not None:
                    pe["committed_usd"] += cv
                    s["committed_usd"] += cv
            if pos.disbursed is not None and pos.currency:
                pe["disbursed_by_currency"][pos.currency] += pos.disbursed
    alerts = db.execute(select(ProjectAlert.level, func.count()).join(Project, Project.id == ProjectAlert.project_id).where(
        Project.country_id == c.id, ProjectAlert.is_active.is_(True), Project.tenant_id.is_(None)).group_by(ProjectAlert.level)).all()
    for v in by_partner.values():
        v["committed_by_currency"] = {k: str(x) for k, x in v["committed_by_currency"].items()}
        v["disbursed_by_currency"] = {k: str(x) for k, x in v["disbursed_by_currency"].items()}
        v["committed_usd"] = str(v["committed_usd"].quantize(Decimal("1")))
    for v in by_sector.values():
        v["committed_usd"] = str(v["committed_usd"].quantize(Decimal("1")))
    dq = dq_dashboard(db, c.id)
    return {
        "country": {"iso3": c.iso3, "name_en": c.name_en, "name_fr": c.name_fr, "currency": c.currency, "is_active": c.is_active},
        "documented_projects": len(projects), "by_status": dict(by_status),
        "by_sector": sorted(by_sector.values(), key=lambda x: -x["projects"]),
        "by_partner": sorted(by_partner.values(), key=lambda x: -x["agreements"]),
        "alerts_by_level": dict(alerts),
        "data_gaps": dq["missing_information"], "average_quality": dq["average_scores"],
        "usd_method": "agreement commitments converted at the annual average rate of their approval year",
        "coverage_warning": dq["coverage_warning"],
    }


@router.get("/sectors/{code}/summary")
def sector_summary(code: str, country: str | None = None, db: Session = Depends(get_db)):
    s = db.scalar(select(Sector).where(Sector.code == code.upper()))
    if s is None:
        raise HTTPException(404, "Unknown sector")
    iso3 = (country or get_settings().default_country).upper()
    c = _country(db, iso3)
    projects = list(db.scalars(visible_projects_query(c.id).where(Project.sector_id == s.id).options(
        selectinload(Project.agreements).selectinload(FinancingAgreement.partner), selectinload(Project.sector))).unique())
    indicators = db.scalars(select(SectorIndicator).where(SectorIndicator.sector_id == s.id)).all()
    linked = db.scalar(select(func.count(ResultsIndicator.id)).where(ResultsIndicator.sector_indicator_id.in_([i.id for i in indicators]))) if indicators else 0
    by_status: dict[str, int] = defaultdict(int)
    for p in projects:
        by_status[p.status] += 1
    pf = compute_portfolio(db, iso3, 2011, 2026, sector_id=s.id)
    return {"sector": row(s, ["code", "name_en", "name_fr"]), "country": iso3, "projects": len(projects), "by_status": dict(by_status),
            "indicators": [row(i, ["code", "name_en", "name_fr", "unit", "kind"]) for i in indicators],
            "indicator_observations_linked": linked,
            "indicator_note": "Sector indicators are populated only from documented results observations; none are inferred.",
            "annual": [{"year": y["year"], "approved": y["counts"]["approved"], "active": y["counts"]["active"],
                        "commitments_usd": y["commitments"]["usd_equivalent"], "disbursements_usd": y["disbursements"]["usd_equivalent"],
                        "usd_complete": y["commitments"]["usd_complete"] and y["disbursements"]["usd_complete"]} for y in pf["years"]],
            "project_list": [project_summary(p) for p in projects[:300]]}


@router.get("/financing/summary")
def financing_summary(country: str | None = None, db: Session = Depends(get_db)):
    c = _country(db, country or get_settings().default_country)
    projects = list(db.scalars(visible_projects_query(c.id).options(
        selectinload(Project.agreements).selectinload(FinancingAgreement.partner),
        selectinload(Project.agreements).selectinload(FinancingAgreement.instrument))).unique())
    by_instrument: dict[str, dict] = {}
    totals: dict[str, dict] = defaultdict(lambda: {"committed": Decimal(0), "disbursed": Decimal(0), "undisbursed": Decimal(0),
                                                   "agreements_with_disbursement": 0, "agreements": 0})
    for p in projects:
        for a in p.agreements:
            pos = agreement_position(db, a)
            ins = a.instrument.name_en if a.instrument else (a.instrument_label or "Not reported")
            e = by_instrument.setdefault(ins, {"instrument": ins, "agreements": 0, "committed_by_currency": defaultdict(Decimal)})
            e["agreements"] += 1
            if pos.currency:
                t = totals[pos.currency]
                t["agreements"] += 1
                if pos.committed is not None:
                    e["committed_by_currency"][pos.currency] += pos.committed
                    t["committed"] += pos.committed
                if pos.disbursed is not None:
                    t["disbursed"] += pos.disbursed
                    t["agreements_with_disbursement"] += 1
                if pos.undisbursed is not None:
                    t["undisbursed"] += pos.undisbursed
    for e in by_instrument.values():
        e["committed_by_currency"] = {k: str(v) for k, v in e["committed_by_currency"].items()}
    return {"country": c.iso3, "by_instrument": sorted(by_instrument.values(), key=lambda x: -x["agreements"]),
            "totals_by_currency": {k: {kk: (str(vv) if isinstance(vv, Decimal) else vv) for kk, vv in v.items()} for k, v in totals.items()},
            "distinctions": {"commitment": "financing committed by partners (approval / commitment transactions)",
                             "disbursement": "funds paid out by partners", "budget_appropriation": "national budget credits (separate table)",
                             "expenditure": "spending reported by implementers", "contract_payment": "payments under contracts"},
            "note": "Currencies are never summed together on this page."}


@router.get("/exchange-rates")
def exchange_rates(currency: str | None = None, db: Session = Depends(get_db)):
    q = select(ExchangeRate)
    if currency:
        q = q.where(or_(ExchangeRate.base_currency == currency.upper(), ExchangeRate.quote_currency == currency.upper()))
    return [row(r, ["base_currency", "quote_currency", "rate", "period", "period_type", "source", "source_url", "retrieved_at"])
            for r in db.scalars(q.order_by(ExchangeRate.base_currency, ExchangeRate.quote_currency, ExchangeRate.period))]


# --- alerts --------------------------------------------------------------------------------------------

@router.get("/alerts")
def alerts(country: str | None = None, level: str | None = None, rule: str | None = None, partner: str | None = None,
           review_status: str | None = None, limit: int = Query(100, le=1000), offset: int = 0,
           principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    q = select(ProjectAlert, Project).join(Project, Project.id == ProjectAlert.project_id).where(
        ProjectAlert.is_active.is_(True), Project.merged_into_id.is_(None), tenant_filter(Project, principal))
    if country:
        q = q.where(Project.country_id == _country(db, country).id)
    if level:
        q = q.where(ProjectAlert.level.in_(level.split(",")))
    if rule:
        q = q.where(ProjectAlert.rule_code == rule)
    if review_status:
        q = q.where(ProjectAlert.review_status == review_status)
    if partner:
        q = q.where(Project.id.in_(select(FinancingAgreement.project_id).join(FinancingPartner).where(FinancingPartner.code == partner.upper())))
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    order = {"critical_attention": 0, "high_attention": 1, "watch": 2, "information": 3}
    rows = db.execute(q.order_by(ProjectAlert.id).offset(offset).limit(limit)).all()
    items = [{**row(a, ["id", "rule_code", "level", "triggering_indicator", "observed_value", "threshold", "source", "source_record_ids",
                        "as_of", "explanation", "recommended_verification", "review_status", "review_note"]),
              "alert_id": a.public_id, "project": {"id": p.id, "ap2i_id": p.ap2i_id, "title": p.title}} for a, p in rows]
    items.sort(key=lambda x: order.get(x["level"], 9))
    summary = dict(db.execute(select(ProjectAlert.level, func.count()).join(Project, Project.id == ProjectAlert.project_id).where(
        ProjectAlert.is_active.is_(True), tenant_filter(Project, principal)).group_by(ProjectAlert.level)).all())
    return {"total": total, "items": items, "summary_by_level": summary,
            "disclaimer": "Alerts are signals requiring verification. They do not indicate fraud or corruption."}


@router.get("/alerts/rules")
def alert_rules(principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    thr = thresholds(db, principal.organization_id)
    return [{"code": code, **meta, "thresholds": {param: str(v) for (r, param), v in thr.items() if r == code}} for code, meta in RULES.items()]


# --- data quality & methodology ----------------------------------------------------------------------

@router.get("/data-quality")
def data_quality(country: str | None = None, db: Session = Depends(get_db)):
    c = _country(db, country) if country else None
    return dq_dashboard(db, c.id if c else None)


@router.get("/methodology")
def methodology():
    from app.finance import fx, portfolio
    from app.ingestion import resolution
    from app.performance import alerts as al

    return {
        "data_principles": ["Every record keeps its original source record, hash, URL and retrieval date.",
                            "Missing values are shown as missing, never as zero.",
                            "Officially reported, verified, calculated, estimated and AI-generated information are labelled separately.",
                            "Synthetic data is refused in production."],
        "portfolio": portfolio.__doc__, "exchange_rates": fx.__doc__, "entity_resolution": resolution.__doc__,
        "early_warning": al.__doc__,
        "coverage": "AP²I coverage is limited to connected sources and uploaded official documents. It is not the complete "
                    "public investment portfolio of any country.",
    }


@router.get("/explorer/transactions")
def explorer_transactions(country: str | None = None, flow: str = Query("disbursement", pattern="^(commitment|disbursement|expenditure)$"),
                          partner: str | None = None, year: int | None = None, currency: str | None = None,
                          limit: int = Query(200, le=2000), offset: int = 0,
                          principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    model = FinancingCommitment if flow == "commitment" else Disbursement
    q = (select(model, FinancingAgreement, Project).join(FinancingAgreement, FinancingAgreement.id == model.agreement_id)
         .join(Project, Project.id == FinancingAgreement.project_id)
         .where(Project.merged_into_id.is_(None), tenant_filter(Project, principal), model.is_counted.is_(True)))
    if flow != "commitment":
        q = q.where(Disbursement.flow_type == flow)
    if country:
        q = q.where(Project.country_id == _country(db, country).id)
    if partner:
        q = q.join(FinancingPartner, FinancingPartner.id == FinancingAgreement.partner_id).where(FinancingPartner.code == partner.upper())
    if year:
        q = q.where(model.value_date >= date(year, 1, 1), model.value_date <= date(year, 12, 31))
    if currency:
        q = q.where(model.currency == currency.upper())
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    items = []
    for m, a, p in db.execute(q.order_by(model.value_date.desc().nulls_last(), model.id).offset(offset).limit(limit)).all():
        items.append({"id": m.id, "flow": flow, "amount": j(m.amount), "currency": m.currency, "value_date": j(m.value_date),
                      "agreement": a.source_identifier, "partner_id": a.partner_id, "project": {"id": p.id, "ap2i_id": p.ap2i_id, "title": p.title},
                      "source_record_id": m.source_record_id, "data_nature": m.data_nature})
    return {"total": total, "items": items}
