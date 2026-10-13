"""Project gates, Electrification Acceleration Score and portfolios (Phase 2)."""
from __future__ import annotations

import uuid
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
from sqlalchemy import select

from ..deps import OrgCtx, org_ctx
from ..engine.score import GATES, Scales, ScoreInputs, Weights, rank, score_project
from ..models import Milestone, ModelRun, Portfolio, PortfolioProject, Project
from ..services.audit import audit
from ..services.runs import clean

router = APIRouter(prefix="/api/orgs/{org_id}", tags=["portfolio and score"])

READINESS_CATEGORIES = ("feasibility", "esia", "land", "licence", "tariff", "financing")
PRODUCTIVE = ("commercial", "industrial", "agricultural", "anchor")
USER_GATES = tuple(k for k in GATES if k != "model_checks")  # the model gate is read from the latest run


class GatesIn(BaseModel):
    gates: dict[str, Literal["met", "not_met", "unknown"]] = Field(default_factory=dict)
    months_to_power: float | None = Field(None, ge=0, le=240, description="Months from today to first power, user estimate")
    underserved_area: bool | None = None


class PortfolioIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field("", max_length=2000)


class MemberIn(BaseModel):
    project_id: uuid.UUID


class ScoreQuery(BaseModel):
    weights: Weights = Weights()
    scales: Scales = Scales()


def _project(ctx: OrgCtx, pid: uuid.UUID) -> Project:
    p = ctx.session.get(Project, pid)
    if p is None or p.org_id != ctx.org.id:
        raise HTTPException(404, "Project not found")
    return p


def _latest(ctx: OrgCtx, pid: uuid.UUID) -> ModelRun | None:
    return ctx.session.execute(select(ModelRun).where(ModelRun.project_id == pid).order_by(ModelRun.created_at.desc()).limit(1)).scalar_one_or_none()


def score_inputs(ctx: OrgCtx, p: Project) -> tuple[ScoreInputs, dict]:
    """Build the score inputs from stored facts only; every derived value says where it comes from."""
    run = _latest(ctx, p.id)
    sources: dict[str, str] = {}
    gates = {k: (p.gates or {}).get(k, "unknown") for k in USER_GATES}
    if run is None:
        gates["model_checks"] = "unknown"
        sources["model_checks"] = "no model run yet"
    else:
        gates["model_checks"] = "met" if run.status in ("validated", "warning") else "not_met"
        sources["model_checks"] = f"latest run status: {run.status}"
    ctxs = p.score_context or {}
    si = dict(project_id=str(p.id), project_name=p.name, gates=gates, underserved_area=ctxs.get("underserved_area"))
    if run is not None:
        M = run.metrics
        fx = run.inputs_snapshot["macro"]["fx_lcy_per_usd"]
        si["connections"] = M.get("connections_target")
        si["subsidy_per_connection_usd"] = (M["subsidy_per_connection"] / fx) if M.get("subsidy_per_connection") is not None else None
        si["dscr_min"] = M.get("dscr_min")
        si["has_debt"] = bool(run.inputs_snapshot["financing"]["debt"])
        sources["financial"] = f"model run {str(run.id)[:8]} ({run.created_at.date().isoformat()})"
    if p.inputs:
        cust = p.inputs.get("customers", [])
        tot_e = sum(c["connections_target"] * c["kwh_per_connection_month"] for c in cust)
        prod_e = sum(c["connections_target"] * c["kwh_per_connection_month"] for c in cust if c["category"] in PRODUCTIVE)
        tot_n = sum(c["connections_target"] for c in cust)
        hh_n = sum(c["connections_target"] for c in cust if c["category"] == "household")
        si["productive_energy_share"] = prod_e / tot_e if tot_e > 0 else None
        si["household_share"] = hh_n / tot_n if tot_n > 0 else None
        sources["customer_mix"] = "project inputs at target connections and COD consumption"
    if ctxs.get("months_to_power") is not None:
        si["months_to_power"] = ctxs["months_to_power"]
        sources["months_to_power"] = "user estimate"
    elif p.inputs:
        si["months_to_power"] = p.inputs.get("construction_quarters", 0) * 3
        sources["months_to_power"] = "construction period from the model inputs only (development time before financial close not included)"
    done = {m.category for m in ctx.session.execute(select(Milestone).where(Milestone.project_id == p.id)).scalars() if m.status == "done"}
    si["readiness_done"] = len(done & set(READINESS_CATEGORIES))
    si["readiness_required"] = len(READINESS_CATEGORIES)
    sources["readiness"] = f"milestones marked done in categories: {', '.join(READINESS_CATEGORIES)}"
    return ScoreInputs(**si), sources


@router.put("/projects/{pid}/gates")
def put_gates(pid: uuid.UUID, body: GatesIn, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    p = _project(ctx, pid)
    bad = [k for k in body.gates if k not in USER_GATES]
    if bad:
        raise HTTPException(422, f"Unknown or read-only gates: {', '.join(bad)} (model_checks comes from the latest model run)")
    p.gates = {**(p.gates or {}), **body.gates}
    p.score_context = {**(p.score_context or {}), "months_to_power": body.months_to_power, "underserved_area": body.underserved_area}
    audit(ctx.session, "set_gates", "project", p.id, org_id=ctx.org.id, user_id=ctx.user.id, gates=body.gates)
    return {"gates": p.gates, "score_context": p.score_context}


@router.post("/projects/{pid}/score")
def project_score(pid: uuid.UUID, body: ScoreQuery = ScoreQuery(), ctx: OrgCtx = Depends(org_ctx())):
    p = _project(ctx, pid)
    si, sources = score_inputs(ctx, p)
    return clean({**score_project(si, body.weights, body.scales), "sources": sources, "is_demo": p.is_demo,
                  "readiness_categories": READINESS_CATEGORIES})


def _portfolio(ctx: OrgCtx, fid: uuid.UUID) -> Portfolio:
    f = ctx.session.get(Portfolio, fid)
    if f is None or f.org_id != ctx.org.id:
        raise HTTPException(404, "Portfolio not found")
    return f


@router.get("/portfolios")
def list_portfolios(ctx: OrgCtx = Depends(org_ctx())):
    rows = ctx.session.execute(select(Portfolio).order_by(Portfolio.created_at.desc())).scalars().all()
    out = []
    for f in rows:
        n = len(ctx.session.execute(select(PortfolioProject).where(PortfolioProject.portfolio_id == f.id)).scalars().all())
        out.append({"id": str(f.id), "name": f.name, "description": f.description, "projects": n, "created_at": f.created_at.isoformat()})
    return out


@router.post("/portfolios", status_code=201)
def create_portfolio(body: PortfolioIn, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    f = Portfolio(org_id=ctx.org.id, name=body.name, description=body.description, created_by=ctx.user.id)
    ctx.session.add(f)
    ctx.session.flush()
    audit(ctx.session, "create", "portfolio", f.id, org_id=ctx.org.id, user_id=ctx.user.id)
    return {"id": str(f.id), "name": f.name, "description": f.description}


@router.delete("/portfolios/{fid}", status_code=204)
def delete_portfolio(fid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx("admin"))):
    ctx.session.delete(_portfolio(ctx, fid))
    audit(ctx.session, "delete", "portfolio", fid, org_id=ctx.org.id, user_id=ctx.user.id)
    return Response(status_code=204)


@router.post("/portfolios/{fid}/projects", status_code=201)
def add_to_portfolio(fid: uuid.UUID, body: MemberIn, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    f = _portfolio(ctx, fid)
    p = _project(ctx, body.project_id)
    exists = ctx.session.execute(select(PortfolioProject).where(PortfolioProject.portfolio_id == f.id,
                                                                PortfolioProject.project_id == p.id)).scalar_one_or_none()
    if exists is None:
        ctx.session.add(PortfolioProject(org_id=ctx.org.id, portfolio_id=f.id, project_id=p.id))
    return {"ok": True}


@router.delete("/portfolios/{fid}/projects/{pid}", status_code=204)
def remove_from_portfolio(fid: uuid.UUID, pid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    _portfolio(ctx, fid)
    m = ctx.session.execute(select(PortfolioProject).where(PortfolioProject.portfolio_id == fid,
                                                           PortfolioProject.project_id == pid)).scalar_one_or_none()
    if m is not None:
        ctx.session.delete(m)
    return Response(status_code=204)


@router.post("/portfolios/{fid}/analysis")
def portfolio_analysis(fid: uuid.UUID, body: ScoreQuery = ScoreQuery(), ctx: OrgCtx = Depends(org_ctx())):
    """Ranking with the score and gates, and totals. Real and synthetic demo projects are totalled separately."""
    f = _portfolio(ctx, fid)
    pids = [m.project_id for m in ctx.session.execute(select(PortfolioProject).where(PortfolioProject.portfolio_id == f.id)).scalars()]
    projects = [_project(ctx, pid) for pid in pids]
    inputs, meta = [], {}
    for p in projects:
        si, sources = score_inputs(ctx, p)
        inputs.append(si)
        run = _latest(ctx, p.id)
        meta[str(p.id)] = {"is_demo": p.is_demo, "country": p.country, "stage": p.stage, "sources": sources,
                           "run_status": run.status if run else None,
                           "capex_usd": run.metrics.get("capex_total_usd") if run else None,
                           "connections": run.metrics.get("connections_target") if run else None,
                           "viability_gap_usd": ((run.metrics.get("viability_gap_pv") or 0) / run.inputs_snapshot["macro"]["fx_lcy_per_usd"]) if run else None,
                           "subsidy_usd": ((run.metrics.get("subsidy_total_nominal") or 0) / run.inputs_snapshot["macro"]["fx_lcy_per_usd"]) if run else None}
    ranked = rank(inputs, body.weights, body.scales)
    for r in ranked:
        r.update(meta[r["project_id"]])

    def totals(demo: bool) -> dict:
        rows = [r for r in ranked if r["is_demo"] == demo and r["run_status"] in ("validated", "warning")]
        return {"projects": len([r for r in ranked if r["is_demo"] == demo]), "modelled": len(rows),
                "capex_usd": sum(r["capex_usd"] or 0 for r in rows), "connections": sum(r["connections"] or 0 for r in rows),
                "viability_gap_usd": sum(r["viability_gap_usd"] or 0 for r in rows), "subsidy_usd": sum(r["subsidy_usd"] or 0 for r in rows),
                "eligible": len([r for r in ranked if r["is_demo"] == demo and r["decision"] == "eligible"]),
                "review_required": len([r for r in ranked if r["is_demo"] == demo and r["decision"] == "review_required"]),
                "excluded": len([r for r in ranked if r["is_demo"] == demo and r["decision"] == "excluded"])}

    return clean({"portfolio": {"id": str(f.id), "name": f.name, "description": f.description}, "ranking": ranked,
                  "totals_real": totals(False), "totals_demo": totals(True), "weights": body.weights.model_dump(),
                  "scales": body.scales.model_dump(),
                  "note": ("Totals use the latest model run of each project with status Validated or Warning. Real and synthetic "
                           "demo projects are never added together. Weights and scales are initial design assumptions.")})
