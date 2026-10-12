from __future__ import annotations

import hashlib
import uuid
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import select

from ..config import get_settings
from ..deps import OrgCtx, org_ctx
from ..engine.inputs import ProjectInputs, Provenance
from ..engine.sensitivity import minimum_capital_grant, sensitivity_table, tornado
from ..models import GeneratedDocument, Milestone, ModelRun, Project
from ..services.audit import audit
from ..services.exports import model_xlsx, teaser_pdf
from ..services.runs import clean, execute

router = APIRouter(prefix="/api/orgs/{org_id}", tags=["projects"])

STAGES = ("screening", "feasibility", "development", "financing", "construction", "operation")


class ProjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    country: str = Field(min_length=1, max_length=100)
    technology: str = "solar_battery_minigrid"
    stage: str = "screening"
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    geometry: dict | None = None


class MilestoneIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    category: str = "other"
    due_date: date | None = None
    status: str = Field("open", pattern="^(open|in_progress|done|blocked)$")
    owner_name: str | None = None


class SubsidyQuery(BaseModel):
    min_dscr: float | None = 1.3
    min_equity_irr: float | None = None
    max_grant: float | None = None


def project_out(p: Project, latest: ModelRun | None = None) -> dict:
    return {"id": str(p.id), "name": p.name, "country": p.country, "technology": p.technology, "stage": p.stage,
            "latitude": p.latitude, "longitude": p.longitude, "geometry": p.geometry, "is_demo": p.is_demo,
            "inputs_version": p.inputs_version, "has_inputs": p.inputs is not None,
            "updated_at": p.updated_at.isoformat(),
            "latest_run": run_summary(latest) if latest else None}


def run_summary(r: ModelRun) -> dict:
    M = r.metrics
    return {"id": str(r.id), "status": r.status, "created_at": r.created_at.isoformat(), "engine_version": r.engine_version,
            "inputs_version": r.inputs_version, "is_demo": r.is_demo,
            "key": {k: M.get(k) for k in ("capex_total_usd", "connections_target", "project_irr_post_subsidy", "equity_irr",
                                          "dscr_min", "lcoe_per_kwh_sold_usd", "viability_gap_per_connection")}}


def _project(ctx: OrgCtx, pid: uuid.UUID) -> Project:
    p = ctx.session.get(Project, pid)
    if p is None or p.org_id != ctx.org.id:
        raise HTTPException(404, "Project not found")
    return p


def _latest(ctx: OrgCtx, pid: uuid.UUID) -> ModelRun | None:
    return ctx.session.execute(select(ModelRun).where(ModelRun.project_id == pid).order_by(ModelRun.created_at.desc()).limit(1)).scalar_one_or_none()


def _inputs(p: Project) -> ProjectInputs:
    if p.inputs is None:
        raise HTTPException(409, "Enter the project inputs before running the model")
    try:
        return ProjectInputs.model_validate(p.inputs)
    except ValidationError as e:
        raise HTTPException(422, e.errors()) from e


@router.get("/projects")
def list_projects(ctx: OrgCtx = Depends(org_ctx())):
    rows = ctx.session.execute(select(Project).order_by(Project.updated_at.desc())).scalars().all()
    return [project_out(p, _latest(ctx, p.id)) for p in rows]


@router.post("/projects", status_code=201)
def create_project(body: ProjectIn, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    if body.stage not in STAGES:
        raise HTTPException(400, f"stage must be one of {', '.join(STAGES)}")
    p = Project(org_id=ctx.org.id, created_by=ctx.user.id, is_demo=ctx.org.is_demo, **body.model_dump())
    ctx.session.add(p)
    ctx.session.flush()
    audit(ctx.session, "create", "project", p.id, org_id=ctx.org.id, user_id=ctx.user.id)
    return project_out(p)


@router.get("/projects/{pid}")
def get_project(pid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx())):
    p = _project(ctx, pid)
    return {**project_out(p, _latest(ctx, pid)), "inputs": p.inputs}


@router.put("/projects/{pid}")
def update_project(pid: uuid.UUID, body: ProjectIn, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    p = _project(ctx, pid)
    if body.stage not in STAGES:
        raise HTTPException(400, f"stage must be one of {', '.join(STAGES)}")
    for k, v in body.model_dump().items():
        setattr(p, k, v)
    audit(ctx.session, "update", "project", p.id, org_id=ctx.org.id, user_id=ctx.user.id)
    return project_out(p, _latest(ctx, pid))


@router.delete("/projects/{pid}", status_code=204)
def delete_project(pid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx("admin"))):
    p = _project(ctx, pid)
    ctx.session.delete(p)
    audit(ctx.session, "delete", "project", pid, org_id=ctx.org.id, user_id=ctx.user.id)
    return Response(status_code=204)


@router.put("/projects/{pid}/inputs")
def put_inputs(pid: uuid.UUID, body: ProjectInputs, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    p = _project(ctx, pid)
    if p.is_demo or ctx.org.is_demo:
        body.provenance = Provenance.ILLUSTRATIVE  # demo projects can never be relabelled as real data
    p.inputs = body.model_dump(mode="json")
    p.inputs_version += 1
    audit(ctx.session, "update_inputs", "project", p.id, org_id=ctx.org.id, user_id=ctx.user.id, version=p.inputs_version)
    return {"inputs_version": p.inputs_version}


@router.post("/projects/{pid}/runs", status_code=201)
def create_run(pid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    p = _project(ctx, pid)
    pin = _inputs(p)
    out = execute(pin)
    r = ModelRun(org_id=ctx.org.id, project_id=p.id, inputs_version=p.inputs_version, inputs_snapshot=p.inputs,
                 created_by=ctx.user.id, is_demo=p.is_demo or pin.provenance.value == "illustrative",
                 **{k: out[k] for k in ("engine_version", "status", "metrics", "checks", "warnings", "missing_inputs", "annual",
                                        "sources_uses", "quarterly", "inputs_sha256")})
    ctx.session.add(r)
    ctx.session.flush()
    audit(ctx.session, "run_model", "model_run", r.id, org_id=ctx.org.id, user_id=ctx.user.id, status=r.status)
    return run_detail(r)


def run_detail(r: ModelRun) -> dict:
    return {**run_summary(r), "metrics": r.metrics, "checks": r.checks, "warnings": r.warnings, "missing_inputs": r.missing_inputs,
            "annual": r.annual, "sources_uses": r.sources_uses, "quarterly": r.quarterly, "inputs_sha256": r.inputs_sha256}


def _run(ctx: OrgCtx, pid: uuid.UUID, rid: uuid.UUID) -> ModelRun:
    r = ctx.session.get(ModelRun, rid)
    if r is None or r.project_id != pid or r.org_id != ctx.org.id:
        raise HTTPException(404, "Run not found")
    return r


@router.get("/projects/{pid}/runs")
def list_runs(pid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx())):
    _project(ctx, pid)
    rows = ctx.session.execute(select(ModelRun).where(ModelRun.project_id == pid).order_by(ModelRun.created_at.desc())).scalars().all()
    return [run_summary(r) for r in rows]


@router.get("/projects/{pid}/runs/{rid}")
def get_run(pid: uuid.UUID, rid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx())):
    return run_detail(_run(ctx, pid, rid))


@router.post("/projects/{pid}/sensitivity")
def sensitivity(pid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx())):
    pin = _inputs(_project(ctx, pid))
    rows = sensitivity_table(pin)
    return clean({"rows": rows, "tornado_npv": tornado(rows, "project_npv_post_subsidy"),
                  "tornado_equity_irr": tornado(rows, "equity_irr"),
                  "note": "Each case reruns the full engine on changed inputs; checks_passed shows its integrity checks."})


@router.post("/projects/{pid}/minimum-subsidy")
def min_subsidy(pid: uuid.UUID, body: SubsidyQuery, ctx: OrgCtx = Depends(org_ctx())):
    pin = _inputs(_project(ctx, pid))
    tol = max(1.0, sum(c.amount for c in pin.capex) * 1e-5)
    return clean(minimum_capital_grant(pin, min_dscr=body.min_dscr, min_equity_irr=body.min_equity_irr,
                                       max_grant=body.max_grant, tol=tol))


# ---------------------------------------------------------------- milestones
@router.get("/projects/{pid}/milestones")
def list_milestones(pid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx())):
    _project(ctx, pid)
    rows = ctx.session.execute(select(Milestone).where(Milestone.project_id == pid).order_by(Milestone.due_date.nulls_last())).scalars().all()
    return [milestone_out(m) for m in rows]


def milestone_out(m: Milestone) -> dict:
    return {"id": str(m.id), "title": m.title, "category": m.category, "due_date": m.due_date.isoformat() if m.due_date else None,
            "status": m.status, "owner_name": m.owner_name}


@router.post("/projects/{pid}/milestones", status_code=201)
def add_milestone(pid: uuid.UUID, body: MilestoneIn, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    _project(ctx, pid)
    m = Milestone(org_id=ctx.org.id, project_id=pid, **body.model_dump())
    ctx.session.add(m)
    ctx.session.flush()
    return milestone_out(m)


@router.put("/projects/{pid}/milestones/{mid}")
def update_milestone(pid: uuid.UUID, mid: uuid.UUID, body: MilestoneIn, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    m = ctx.session.get(Milestone, mid)
    if m is None or m.project_id != pid:
        raise HTTPException(404, "Milestone not found")
    for k, v in body.model_dump().items():
        setattr(m, k, v)
    return milestone_out(m)


# ---------------------------------------------------------------- exports
def _store(ctx: OrgCtx, p: Project, r: ModelRun, kind: str, data: bytes, ext: str) -> GeneratedDocument:
    root = Path(get_settings().storage_dir) / str(ctx.org.id)
    root.mkdir(parents=True, exist_ok=True)
    doc = GeneratedDocument(org_id=ctx.org.id, project_id=p.id, run_id=r.id, kind=kind, engine_version=r.engine_version,
                            inputs_sha256=r.inputs_sha256, file_sha256=hashlib.sha256(data).hexdigest(),
                            storage_key=f"{ctx.org.id}/{uuid.uuid4()}.{ext}", created_by=ctx.user.id)
    (Path(get_settings().storage_dir) / doc.storage_key).write_bytes(data)
    ctx.session.add(doc)
    audit(ctx.session, "generate_document", kind, r.id, org_id=ctx.org.id, user_id=ctx.user.id, sha256=doc.file_sha256)
    return doc


def _fname(p: Project, r: ModelRun, ext: str) -> str:
    safe = "".join(ch if ch.isalnum() else "_" for ch in p.name)[:60]
    return f"ACCESS360_{safe}_run{str(r.id)[:8]}.{ext}"


@router.get("/projects/{pid}/runs/{rid}/export.xlsx")
def export_xlsx(pid: uuid.UUID, rid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx())):
    p, r = _project(ctx, pid), _run(ctx, pid, rid)
    data = model_xlsx(p, r)
    _store(ctx, p, r, "model_xlsx", data, "xlsx")
    return Response(data, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": f'attachment; filename="{_fname(p, r, "xlsx")}"'})


@router.get("/projects/{pid}/runs/{rid}/teaser.pdf")
def export_teaser(pid: uuid.UUID, rid: uuid.UUID, ctx: OrgCtx = Depends(org_ctx())):
    p, r = _project(ctx, pid), _run(ctx, pid, rid)
    ms = ctx.session.execute(select(Milestone).where(Milestone.project_id == pid).order_by(Milestone.due_date.nulls_last())).scalars().all()
    data = teaser_pdf(p, r, ms)
    _store(ctx, p, r, "teaser_pdf", data, "pdf")
    return Response(data, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{_fname(p, r, "pdf")}"'})


@router.get("/documents")
def list_documents(ctx: OrgCtx = Depends(org_ctx())):
    rows = ctx.session.execute(select(GeneratedDocument).order_by(GeneratedDocument.created_at.desc()).limit(200)).scalars().all()
    return [{"id": str(d.id), "project_id": str(d.project_id), "run_id": str(d.run_id), "kind": d.kind, "engine_version": d.engine_version,
             "inputs_sha256": d.inputs_sha256, "file_sha256": d.file_sha256, "created_at": d.created_at.isoformat()} for d in rows]
