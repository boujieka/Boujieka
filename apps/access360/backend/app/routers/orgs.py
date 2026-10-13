from __future__ import annotations

import uuid
from collections import Counter
from datetime import date, timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from ..deps import Ctx, OrgCtx, org_ctx, superadmin
from ..models import Membership, Milestone, ModelRun, Organization, Project, User
from ..services.audit import audit

router = APIRouter(tags=["organisations"])


class MemberIn(BaseModel):
    email: EmailStr
    role: Literal["admin", "analyst", "viewer"]


class AccreditationIn(BaseModel):
    status: Literal["pending", "verified", "rejected"]
    note: str = ""


@router.get("/api/orgs/{org_id}/members")
def members(ctx: OrgCtx = Depends(org_ctx())):
    rows = ctx.session.execute(select(Membership, User).join(User, User.id == Membership.user_id)
                               .where(Membership.org_id == ctx.org.id)).all()
    return [{"user_id": str(u.id), "email": u.email, "full_name": u.full_name, "role": m.role, "mfa_enabled": u.mfa_enabled} for m, u in rows]


@router.post("/api/orgs/{org_id}/members", status_code=201)
def add_member(body: MemberIn, ctx: OrgCtx = Depends(org_ctx("admin", privileged=True))):
    u = ctx.session.execute(select(User).where(User.email == body.email.lower())).scalar_one_or_none()
    if u is None:
        raise HTTPException(404, "No account with this email: ask the person to register first")
    exists = ctx.session.execute(select(Membership).where(Membership.user_id == u.id, Membership.org_id == ctx.org.id)).scalar_one_or_none()
    if exists:
        exists.role = body.role
    else:
        ctx.session.add(Membership(user_id=u.id, org_id=ctx.org.id, role=body.role))
    audit(ctx.session, "member_set", "membership", u.id, org_id=ctx.org.id, user_id=ctx.user.id, role=body.role)
    return {"ok": True}


@router.get("/api/orgs/{org_id}/audit")
def audit_log(ctx: OrgCtx = Depends(org_ctx("admin"))):
    from ..models import AuditLog
    rows = ctx.session.execute(select(AuditLog).where(AuditLog.org_id == ctx.org.id).order_by(AuditLog.at.desc()).limit(200)).scalars().all()
    return [{"at": a.at.isoformat(), "action": a.action, "entity": a.entity, "entity_id": a.entity_id, "user_id": str(a.user_id) if a.user_id else None,
             "detail": a.detail} for a in rows]


@router.get("/api/orgs/{org_id}/dashboard")
def dashboard(ctx: OrgCtx = Depends(org_ctx())):
    s = ctx.session
    projects = s.execute(select(Project)).scalars().all()
    latest: dict[uuid.UUID, ModelRun] = {}
    for r in s.execute(select(ModelRun).order_by(ModelRun.created_at.desc())).scalars():
        latest.setdefault(r.project_id, r)
    # a project counts as demo if it is flagged demo or its latest run uses illustrative (synthetic) inputs
    is_demo = {p.id: p.is_demo or bool(latest.get(p.id) and latest[p.id].is_demo) for p in projects}
    real = [p for p in projects if not is_demo[p.id]]
    demo = [p for p in projects if is_demo[p.id]]

    def agg(ps):
        runs = [latest[p.id] for p in ps if p.id in latest]
        usable = [r for r in runs if r.status in ("validated", "warning")]
        return {
            "projects": len(ps),
            "projects_modelled": len(runs),
            "pipeline_capex_usd": sum(r.metrics.get("capex_total_usd") or 0 for r in usable),
            "planned_connections": sum(r.metrics.get("connections_target") or 0 for r in usable),
            "viability_gap_usd": sum(((r.metrics.get("viability_gap_pv") or 0) / r.inputs_snapshot["macro"]["fx_lcy_per_usd"]) for r in usable),
            "status_counts": dict(Counter(r.status for r in runs)),
            "stage_counts": dict(Counter(p.stage for p in ps)),
            "country_counts": dict(Counter(p.country for p in ps)),
        }

    soon = date.today() + timedelta(days=60)
    ms = s.execute(select(Milestone).where(Milestone.status != "done").order_by(Milestone.due_date.nulls_last())).scalars().all()
    names = {p.id: p.name for p in projects}
    alerts = []
    for p in projects:
        r = latest.get(p.id)
        if r is None:
            alerts.append({"level": "info", "project": p.name, "text": "Model not yet run"})
        elif r.status in ("failed_checks", "incomplete_inputs"):
            alerts.append({"level": "critical", "project": p.name, "text": f"Model status: {r.status.replace('_', ' ')}"})
        elif r.inputs_version != p.inputs_version:
            alerts.append({"level": "warning", "project": p.name, "text": "Inputs changed since the last run"})
    for m in ms:
        if m.due_date and m.due_date < date.today():
            alerts.append({"level": "warning", "project": names.get(m.project_id, ""), "text": f"Overdue: {m.title}"})
    return {"real": agg(real), "demo": agg(demo),
            "milestones": [{"project": names.get(m.project_id, ""), "title": m.title, "due_date": m.due_date.isoformat() if m.due_date else None,
                            "status": m.status, "due_soon": bool(m.due_date and m.due_date <= soon)} for m in ms[:10]],
            "alerts": alerts[:20],
            "note": "Real and synthetic demo data are counted separately and never added together."}


# ---------------------------------------------------------------- platform administration
@router.get("/api/admin/organizations")
def admin_orgs(ctx: Ctx = Depends(superadmin)):
    rows = ctx.session.execute(select(Organization).order_by(Organization.created_at.desc())).scalars().all()
    return [{"id": str(o.id), "name": o.name, "kind": o.kind, "accreditation_status": o.accreditation_status, "plan": o.plan,
             "is_demo": o.is_demo, "created_at": o.created_at.isoformat()} for o in rows]


@router.post("/api/admin/organizations/{org_id}/accreditation")
def set_accreditation(org_id: uuid.UUID, body: AccreditationIn, ctx: Ctx = Depends(superadmin)):
    o = ctx.session.get(Organization, org_id)
    if o is None:
        raise HTTPException(404, "Organisation not found")
    if o.kind != "accredited":
        raise HTTPException(400, "Only organisations registered as accredited organisations can be verified")
    o.accreditation_status = body.status
    audit(ctx.session, "accreditation", "organization", o.id, user_id=ctx.user.id, status=body.status, note=body.note)
    return {"id": str(o.id), "accreditation_status": o.accreditation_status}
