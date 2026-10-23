"""Public, read-only data snapshot for the static AP²I portal (e.g. the Netlify site).

What it contains: only what an ANONYMOUS visitor of the API may already read. API-shaped files are produced by
calling the real API in-process without credentials (so tenant-private projects, plan-gated fields and the
Project Rescue diagnosis are never exported). The flat analytical tables (projects, agreements, flows) are built
with the same finance functions as the API (`agreement_position`, `FX.convert`) and restricted to the same
public project set.

Reconciliation: the per-year commitment and disbursement totals recomputed from the exported flow table are
compared with `compute_portfolio` (the annual-portfolio engine). The export fails if they differ.

Usage: python -m app.cli export-public-snapshot <outdir> [ISO3 ...]
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.finance.fx import FX
from app.finance.indicators import agreement_position
from app.finance.portfolio import compute_portfolio
from app.models import (
    Country,
    DataQualityAssessment,
    Disbursement,
    Document,
    FinancingAgreement,
    FinancingCommitment,
    ImplementationProgress,
    Project,
    ProjectAlert,
    ResultsIndicator,
    SourceConnector,
    SyncRun,
)

SNAPSHOT_VERSION = 1
LEVEL_ORDER = ["critical_attention", "high_attention", "watch", "information"]


def _j(v):
    if isinstance(v, Decimal):
        return str(v)
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    return v


def _dump(path: Path, data) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":"), default=_j)
    path.write_text(raw, encoding="utf-8")
    return len(raw)


def public_projects(db: Session, country_ids: list[int]) -> list[Project]:
    """Same visibility as an anonymous API call, without synthetic records."""
    return list(db.scalars(select(Project).where(
        Project.country_id.in_(country_ids), Project.merged_into_id.is_(None), Project.tenant_id.is_(None),
        Project.is_synthetic.is_(False)).options(
        selectinload(Project.agreements).selectinload(FinancingAgreement.partner),
        selectinload(Project.agreements).selectinload(FinancingAgreement.instrument),
        selectinload(Project.sector), selectinload(Project.region), selectinload(Project.country),
        selectinload(Project.locations)).order_by(Project.ap2i_id)).unique())


def build_tables(db: Session, projects: list[Project]) -> dict:
    fx = FX(db)
    ids = [p.id for p in projects]
    alerts: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for pid, level in db.execute(select(ProjectAlert.project_id, ProjectAlert.level).where(
            ProjectAlert.is_active.is_(True), ProjectAlert.project_id.in_(ids))):
        alerts[pid][level] += 1
    n_docs = dict(db.execute(select(Document.project_id, func.count()).where(Document.project_id.in_(ids)).group_by(Document.project_id)).all())
    n_results = dict(db.execute(select(ResultsIndicator.project_id, func.count()).where(
        ResultsIndicator.project_id.in_(ids)).group_by(ResultsIndicator.project_id)).all())
    latest_rating: dict[int, tuple] = {}
    for pid, rd, rating in db.execute(select(ImplementationProgress.project_id, ImplementationProgress.report_date,
                                             ImplementationProgress.rating).where(
            ImplementationProgress.project_id.in_(ids), ImplementationProgress.rating.is_not(None))):
        if pid not in latest_rating or (rd and latest_rating[pid][0] and rd > latest_rating[pid][0]):
            latest_rating[pid] = (rd, rating)
    dq = {d.project_id: d for d in db.scalars(select(DataQualityAssessment).where(
        DataQualityAssessment.project_id.in_(ids), DataQualityAssessment.is_current.is_(True)))}

    prows, arows = [], []
    agr_index: dict[int, int] = {}
    for p in projects:
        approvals = [a.approval_date for a in p.agreements if a.approval_date]
        approval = p.original_approval_date or (min(approvals) if approvals else None)
        closings = [a.closing_date_current for a in p.agreements if a.closing_date_current]
        al = alerts.get(p.id, {})
        q = dq.get(p.id)
        prows.append({
            "id": p.id, "ref": p.ap2i_id, "title": p.title, "country": p.country.iso3,
            "sector": p.sector.code if p.sector else None, "region": p.region.code if p.region else None,
            "status": p.status, "operational_status": p.operational_status, "verification": p.verification_status,
            "approval": approval, "start": p.implementation_start_date, "planned_end": p.original_completion_date,
            "revised_end": p.revised_completion_date, "actual_end": p.actual_completion_date,
            # same end-date rules as the backend: indicators (current planned end) and portfolio (incl. actual end)
            "current_end": p.revised_completion_date or p.original_completion_date or (max(closings) if closings else None),
            "portfolio_end": p.actual_completion_date or p.revised_completion_date or p.original_completion_date or (
                max(closings) if closings else None),
            "agency": p.executing_agency,
            "partners": sorted({a.partner.code for a in p.agreements if a.partner}),
            "instruments": sorted({a.instrument.code for a in p.agreements if a.instrument}),
            "alerts": {lv: al[lv] for lv in LEVEL_ORDER if al.get(lv)},
            "physical_progress": p.physical_progress_pct,
            "original_cost": p.original_estimated_cost, "revised_cost": p.revised_estimated_cost, "cost_currency": p.cost_currency,
            "documents": n_docs.get(p.id, 0), "results_indicators": n_results.get(p.id, 0),
            "latest_rating": {"date": latest_rating[p.id][0], "rating": latest_rating[p.id][1]} if p.id in latest_rating else None,
            "dq": {"completeness": q.completeness, "traceability": q.traceability, "timeliness": q.timeliness} if q else None,
            # Coordinates exactly as published by the source, with their precision; never generated.
            "locations": [{"lat": loc.latitude, "lon": loc.longitude, "precision": loc.precision, "place": loc.place_name}
                          for loc in p.locations if loc.latitude is not None and loc.longitude is not None],
            "last_source_update": p.last_source_update_at,
            "commissioning": p.commissioning_date, "status_source": p.status_source,
        })
        for a in p.agreements:
            pos = agreement_position(db, a)
            year = a.approval_date.year if a.approval_date else None
            conv = fx.convert(pos.committed, pos.currency, "USD", year) if pos.committed is not None and pos.currency else None
            agr_index[a.id] = len(arows)
            arows.append({
                "id": a.id, "project": p.id, "source_identifier": a.source_identifier,
                "partner": a.partner.code if a.partner else None,
                "instrument": a.instrument.code if a.instrument else None, "instrument_label": a.instrument_label,
                "approval": a.approval_date, "closing_original": a.closing_date_original, "closing_current": a.closing_date_current,
                "status": a.status, "currency": pos.currency,
                "amount_original": a.amount_original, "committed": pos.committed, "committed_basis": pos.committed_basis,
                "cancelled": pos.cancelled, "disbursed": pos.disbursed, "disbursed_basis": pos.disbursed_basis,
                "disbursed_as_of": pos.disbursed_as_of, "undisbursed": pos.undisbursed, "is_guarantee": pos.is_guarantee,
                "parent": a.parent_source_identifier,
                # USD equivalent of the commitment at the annual average rate of its approval year (methodology §FX);
                # null when the date or the rate is missing — never another year's rate.
                "committed_usd": conv.value if conv else None, "committed_usd_note": (conv.reason if conv and conv.value is None else
                                                                                       conv.source if conv else None),
                "source_record_id": a.source_record_id,
            })

    # Dated transactions: the series used for annual charts (same selection as the portfolio engine).
    agr_ids = list(agr_index)
    flows = {"kind": [], "agreement": [], "date": [], "year": [], "amount": [], "currency": [], "usd": [], "rate_source": []}
    sources = set()

    def add(kind, f, year):
        conv = fx.convert(f.amount, f.currency, "USD", year) if year else None
        flows["kind"].append(kind)
        flows["agreement"].append(f.agreement_id)
        flows["date"].append(_j(f.value_date))
        flows["year"].append(year)
        flows["amount"].append(str(f.amount))
        flows["currency"].append(f.currency)
        flows["usd"].append(str(conv.value) if conv and conv.value is not None else None)
        src = conv.source if conv and conv.value is not None and conv.source != "identity" else None
        flows["rate_source"].append(src)
        if src:
            sources.add(src)

    if agr_ids:
        for c in db.scalars(select(FinancingCommitment).where(FinancingCommitment.agreement_id.in_(agr_ids),
                                                               FinancingCommitment.is_counted.is_(True)).order_by(FinancingCommitment.id)):
            add("commitment", c, c.value_date.year if c.value_date else None)
        for d in db.scalars(select(Disbursement).where(Disbursement.agreement_id.in_(agr_ids),
                                                        Disbursement.is_counted.is_(True)).order_by(Disbursement.id)):
            add(d.flow_type, d, d.value_date.year if d.value_date else d.period_year)
    return {"projects": prows, "agreements": arows, "flows": flows, "rate_sources": sorted(sources)}


def reconcile(db: Session, iso3: str, tables: dict, first: int, last: int) -> dict:
    """Per-year totals from the exported flows must equal the portfolio engine's totals."""
    port = compute_portfolio(db, iso3, first, last)
    proj_country = {p["id"]: p["country"] for p in tables["projects"]}
    agr_project = {a["id"]: a["project"] for a in tables["agreements"]}
    f = tables["flows"]
    sums: dict[tuple, dict] = defaultdict(lambda: defaultdict(Decimal))
    for i in range(len(f["kind"])):
        if proj_country.get(agr_project.get(f["agreement"][i])) != iso3 or f["year"][i] is None:
            continue
        key = (f["kind"][i], f["year"][i])
        sums[key][f["currency"][i]] += Decimal(f["amount"][i])
        if f["usd"][i] is not None:
            sums[key]["__usd"] += Decimal(f["usd"][i])
    checks, ok = [], True
    for y in port.get("years", []):
        for kind, block in (("commitment", y["commitments"]), ("disbursement", y["disbursements"]), ("expenditure", y["expenditures"])):
            mine = sums.get((kind, y["year"]), {})
            by_cur = {k: str(v) for k, v in sorted(mine.items()) if k != "__usd"}
            usd = str(mine["__usd"].quantize(Decimal("0.01"))) if mine else None
            same = by_cur == block["by_currency"] and (usd == block["usd_equivalent"] or (not mine and block["usd_equivalent"] is None))
            ok = ok and same
            if not same:
                checks.append({"year": y["year"], "kind": kind, "snapshot": {"by_currency": by_cur, "usd": usd},
                               "portfolio": {"by_currency": block["by_currency"], "usd": block["usd_equivalent"]}})
    return {"country": iso3, "years": f"{first}-{last}", "ok": ok, "mismatches": checks,
            "method": "sum of exported counted transactions per year vs compute_portfolio()"}


def export_public_snapshot(db: Session, outdir: str | Path, countries: list[str] | None = None, first_year: int = 2011,
                           last_year: int = 2026, client=None) -> dict:
    from fastapi.testclient import TestClient

    from app.main import app

    out = Path(outdir)
    data = out / "data"
    api = client or TestClient(app)

    def get(path: str, **params):
        r = api.get("/api/v1" + path, params=params)
        r.raise_for_status()
        return r.json()

    iso3s = [c.upper() for c in (countries or [])] or sorted(db.scalars(select(Country.iso3).join(Project, Project.country_id == Country.id).where(
        Project.tenant_id.is_(None), Project.merged_into_id.is_(None)).distinct()))
    cids = [c.id for c in db.scalars(select(Country).where(Country.iso3.in_(iso3s)))]
    projects = public_projects(db, cids)
    tables = build_tables(db, projects)
    sizes = {}
    for name in ("projects", "agreements", "flows"):
        sizes[f"{name}.json"] = _dump(data / f"{name}.json", tables[name])
    ref = {"countries": get("/countries"), "sectors": get("/sectors"), "partners": get("/partners"),
           "instruments": get("/instruments"), "methodology": get("/methodology"), "alert_rules": get("/alerts/rules"),
           "rate_sources": tables["rate_sources"]}
    sizes["ref.json"] = _dump(data / "ref.json", ref)
    sizes["africa.json"] = _dump(data / "africa.json", get("/africa/overview"))
    alerts = get("/alerts", limit=1000)
    sizes["alerts.json"] = _dump(data / "alerts.json", alerts)
    sizes["data-quality.json"] = _dump(data / "data-quality.json", get("/data-quality"))
    recon = []
    for iso3 in iso3s:
        sizes[f"country-{iso3}.json"] = _dump(data / f"country-{iso3}.json", {
            "detail": get(f"/countries/{iso3}"), "dashboard": get(f"/countries/{iso3}/dashboard"),
            "portfolio": get(f"/countries/{iso3}/portfolio", year_from=first_year, year_to=last_year),
            "financing": get("/financing/summary", country=iso3), "data_quality": get("/data-quality", country=iso3)})
        recon.append(reconcile(db, iso3, tables, first_year, last_year))
    africa = json.loads((data / "africa.json").read_text(encoding="utf-8"))
    for iso3 in iso3s:
        # Total commitments (agreement positions, USD at approval-year rate) must equal the Africa overview figure.
        api_c = next((c for c in africa["countries"] if c["iso3"] == iso3), {})
        pids = {p["id"] for p in tables["projects"] if p["country"] == iso3}
        mine = sum((Decimal(a["committed_usd"]) for a in tables["agreements"] if a["project"] in pids and a["committed_usd"] is not None),
                   Decimal(0))
        api_v = api_c.get("commitments_usd")
        same = (api_v is None and not pids) or (api_v is not None and str(mine.quantize(Decimal("1"))) == api_v)
        recon.append({"country": iso3, "check": "commitments_usd (agreement positions) vs /africa/overview", "ok": same,
                      "snapshot": str(mine.quantize(Decimal("1"))), "api": api_v})
    if not all(r["ok"] for r in recon):
        raise RuntimeError(f"Snapshot does not reconcile with the portfolio engine: {recon}")
    for p in projects:
        detail = get(f"/projects/{p.ap2i_id}")
        detail["flows"] = get(f"/projects/{p.ap2i_id}/flows")
        _dump(data / "p" / f"{p.ap2i_id}.json", detail)
    syncs = []
    for c in db.scalars(select(SourceConnector).where(SourceConnector.enabled.is_(True)).order_by(SourceConnector.key)):
        last = db.scalar(select(SyncRun).where(SyncRun.connector_id == c.id, SyncRun.status == "success")
                         .order_by(SyncRun.finished_at.desc().nulls_last()).limit(1))
        syncs.append({"key": c.key, "name": c.name, "status": c.status,
                      "last_success": _j(last.finished_at) if last else None})
    meta = {
        "snapshot_version": SNAPSHOT_VERSION, "generated_at": datetime.now(timezone.utc).isoformat(),
        "countries": iso3s, "years": [first_year, last_year],
        "counts": {"projects": len(tables["projects"]), "agreements": len(tables["agreements"]),
                   "transactions": len(tables["flows"]["kind"]), "alerts": alerts["total"]},
        "latest_source_update": max((p["last_source_update"] for p in tables["projects"] if p["last_source_update"]), default=None),
        "connectors": syncs, "reconciliation": recon, "files": sizes,
        "scope": ("Public records only (what an anonymous API visitor can read). Connected sources only — not the complete "
                  "national public-investment portfolio. Read-only copy; the live application is the reference."),
    }
    meta["checksum"] = hashlib.sha256(json.dumps(tables, sort_keys=True, default=_j).encode()).hexdigest()
    _dump(data / "meta.json", meta)
    return {k: meta[k] for k in ("generated_at", "countries", "counts", "reconciliation")}
