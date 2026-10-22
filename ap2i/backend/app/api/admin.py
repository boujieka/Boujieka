"""Administration panel API (Master prompt §29): connectors, imports, review, users, organizations, audit."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.serial import j, row
from app.config import get_settings
from app.connectors.base import ConnectorError
from app.db import get_db
from app.ingestion.resolution import merge_projects, reverse_merge
from app.models import (
    AlertThreshold,
    AppSetting,
    AuditLog,
    Country,
    DataValidation,
    MatchCandidate,
    Organization,
    Plan,
    Project,
    ProjectAlert,
    ProjectMerge,
    RoleDef,
    SourceConnector,
    SourceRecord,
    Subscription,
    SyncRun,
    User,
    UserRole,
)
from app.reference.catalog import P_ADMIN_ALL, P_ADMIN_ORG, P_REVIEW
from app.reference.seed import sync_active_countries
from app.security.deps import Principal, audit, require
from app.tasks import cron

router = APIRouter(prefix="/admin", tags=["admin"])
ADMIN = require(P_ADMIN_ALL)
REVIEW = require(P_REVIEW)


# --- connectors & synchronisation ----------------------------------------------------------------------

def connector_out(db: Session, c: SourceConnector) -> dict:
    stored = db.scalar(select(func.count(SourceRecord.id)).where(SourceRecord.connector_id == c.id, SourceRecord.is_latest.is_(True)))
    review = db.scalar(select(func.count(SourceRecord.id)).where(SourceRecord.connector_id == c.id, SourceRecord.processing_status == "review"))
    last = db.scalar(select(SyncRun).where(SyncRun.connector_id == c.id).order_by(SyncRun.started_at.desc()))
    return {**row(c, ["id", "key", "name", "tier", "enabled", "status", "status_evidence", "access_method", "base_url", "documentation_url",
                      "usage_terms", "update_frequency", "config", "schedule_cron", "last_success_at", "last_failure_at", "last_error",
                      "notes"]),
            "records_stored": stored, "records_requiring_review": review,
            "last_run": row(last, ["id", "status", "trigger", "started_at", "finished_at", "records_retrieved", "records_imported",
                                   "records_review", "records_failed"]) if last else None}


@router.get("/connectors")
def connectors(principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    return [connector_out(db, c) for c in db.scalars(select(SourceConnector).order_by(SourceConnector.tier, SourceConnector.key))]


class ConnectorPatch(BaseModel):
    enabled: bool | None = None
    schedule_cron: str | None = None
    countries: list[str] | None = None
    date_from: str | None = None
    date_to: str | None = None
    limit: int | None = Field(None, ge=1, le=100000)
    notes: str | None = None


@router.patch("/connectors/{key}")
def patch_connector(key: str, body: ConnectorPatch, request: Request, principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    c = db.scalar(select(SourceConnector).where(SourceConnector.key == key))
    if c is None:
        raise HTTPException(404, "Unknown connector")
    if body.enabled and c.status == "not_implemented":
        raise HTTPException(409, "This connector has no implementation and cannot be enabled")
    if body.schedule_cron is not None:
        if body.schedule_cron:
            try:
                cron.parse(body.schedule_cron)
            except ValueError as exc:
                raise HTTPException(422, f"Invalid cron: {exc}") from None
        c.schedule_cron = body.schedule_cron or None
    cfg = dict(c.config or {})
    if body.countries is not None:
        valid = set(db.scalars(select(Country.iso3)))
        bad = [x for x in body.countries if x.upper() not in valid]
        if bad:
            raise HTTPException(422, f"Unknown countries {bad}")
        cfg["countries"] = [x.upper() for x in body.countries]
        cfg["follow_active_countries"] = False
    for k in ("date_from", "date_to", "limit"):
        v = getattr(body, k)
        if v is not None:
            cfg[k] = v
    c.config = cfg
    if body.enabled is not None:
        c.enabled = body.enabled
    if body.notes is not None:
        c.notes = body.notes
    audit(db, request, "admin.connector_updated", principal, "connector", key, body.model_dump(exclude_none=True))
    db.commit()
    return connector_out(db, c)


@router.post("/connectors/{key}/sync")
def trigger_sync(key: str, request: Request, background: bool = False, principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    c = db.scalar(select(SourceConnector).where(SourceConnector.key == key))
    if c is None:
        raise HTTPException(404, "Unknown connector")
    if c.key == "manual_upload":
        raise HTTPException(409, "Use the upload endpoints for the manual import workflow")
    audit(db, request, "admin.sync_triggered", principal, "connector", key, {"background": background})
    db.commit()
    if background:
        from app.tasks.celery_app import sync_connector_task

        res = sync_connector_task.delay(key, "manual")
        return {"queued": True, "task_id": res.id}
    from app.tasks.jobs import sync_connector

    try:
        return sync_connector(key, "manual")
    except ConnectorError as exc:
        raise HTTPException(502, str(exc)) from None


@router.get("/sync-runs")
def sync_runs(connector: str | None = None, limit: int = 50, principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    q = select(SyncRun).join(SourceConnector, SourceConnector.id == SyncRun.connector_id)
    if connector:
        q = q.where(SourceConnector.key == connector)
    return [{**row(r, ["id", "trigger", "status", "started_at", "finished_at", "params", "records_retrieved", "records_new",
                       "records_unchanged", "records_imported", "records_review", "records_failed"]), "connector": r.connector.key}
            for r in db.scalars(q.order_by(SyncRun.started_at.desc()).limit(min(limit, 500)))]


@router.get("/sync-runs/{run_id}")
def sync_run(run_id: int, principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    r = db.get(SyncRun, run_id)
    if r is None:
        raise HTTPException(404, "Not found")
    return {**row(r, ["id", "trigger", "status", "started_at", "finished_at", "params", "records_retrieved", "records_new",
                      "records_unchanged", "records_imported", "records_review", "records_failed", "errors", "log"]), "connector": r.connector.key}


# --- import review ----------------------------------------------------------------------------------------

@router.get("/review/records")
def review_records(status: str = "review", connector: str | None = None, limit: int = 100, offset: int = 0,
                   principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    q = select(SourceRecord).where(SourceRecord.processing_status == status)
    if connector:
        q = q.join(SourceConnector).where(SourceConnector.key == connector)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    items = []
    for s in db.scalars(q.order_by(SourceRecord.retrieved_at.desc()).offset(offset).limit(min(limit, 500))):
        issues = db.scalars(select(DataValidation).where(DataValidation.source_record_id == s.id)).all()
        items.append({**row(s, ["id", "source_identifier", "record_type", "country_iso3", "source_url", "retrieved_at", "processing_status",
                                "processing_note", "verification_status"]), "connector": s.connector.key,
                      "issues": [row(i, ["id", "rule", "severity", "message", "status"]) for i in issues]})
    return {"total": total, "items": items}


class RecordDecision(BaseModel):
    decision: str = Field(pattern="^(verified|rejected)$")
    note: str | None = None


@router.post("/review/records/{record_id}")
def decide_record(record_id: int, body: RecordDecision, request: Request, principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    s = db.get(SourceRecord, record_id)
    if s is None:
        raise HTTPException(404, "Not found")
    s.verification_status = body.decision
    if body.decision == "rejected":
        s.processing_status = "rejected"
    for i in db.scalars(select(DataValidation).where(DataValidation.source_record_id == s.id, DataValidation.status == "open")):
        i.status = "resolved" if body.decision == "verified" else "rejected"
        i.resolved_by, i.resolved_at = principal.user.id, datetime.now(timezone.utc)
    audit(db, request, "review.record_decision", principal, "source_record", record_id, body.model_dump())
    db.commit()
    return {"id": s.id, "verification_status": s.verification_status}


class ProjectVerify(BaseModel):
    status: str = Field(pattern="^(verified|needs_review|rejected|unverified)$")
    note: str | None = None
    operational_status: str | None = Field(None, pattern="^(operational|partially_operational|not_operational|unknown)$")


@router.post("/projects/{project_id}/verification")
def verify_project(project_id: int, body: ProjectVerify, request: Request, principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    p = db.get(Project, project_id)
    if p is None:
        raise HTTPException(404, "Not found")
    p.verification_status = body.status
    if body.status == "verified":
        p.last_verified_at = datetime.now(timezone.utc)
    audit(db, request, "review.project_verification", principal, "project", p.ap2i_id, body.model_dump())
    db.commit()
    return {"ap2i_id": p.ap2i_id, "verification_status": p.verification_status}


# --- duplicates & merges -----------------------------------------------------------------------------------

@router.get("/matches")
def matches(status: str = "pending", principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    out = []
    for m in db.scalars(select(MatchCandidate).where(MatchCandidate.status == status).order_by(MatchCandidate.score.desc()).limit(500)):
        a, b = db.get(Project, m.project_a_id), db.get(Project, m.project_b_id)
        def brief(p):
            return {"id": p.id, "ap2i_id": p.ap2i_id, "title": p.title, "status": p.status, "approval": j(p.original_approval_date),
                    "partners": sorted({ag.partner.short_name for ag in p.agreements if ag.partner}),
                    "executing_agency": p.executing_agency}
        out.append({**row(m, ["id", "score", "features", "relation", "status", "created_at", "review_note"]), "a": brief(a), "b": brief(b)})
    return out


class MatchDecision(BaseModel):
    decision: str = Field(pattern="^(accept|reject)$")
    survivor: str = Field("a", pattern="^(a|b)$")
    note: str | None = None


@router.post("/matches/{match_id}")
def decide_match(match_id: int, body: MatchDecision, request: Request, principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    m = db.get(MatchCandidate, match_id)
    if m is None or m.status != "pending":
        raise HTTPException(404, "Pending candidate not found")
    m.reviewed_by, m.reviewed_at, m.review_note = principal.user.id, datetime.now(timezone.utc), body.note
    merge = None
    if body.decision == "accept":
        survivor, merged = (m.project_a_id, m.project_b_id) if body.survivor == "a" else (m.project_b_id, m.project_a_id)
        try:
            merge = merge_projects(db, survivor, merged, principal.user.id, body.note or f"Accepted match candidate {m.id}", m.id)
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from None
        m.status = "accepted"
    else:
        m.status = "rejected"
    audit(db, request, "review.match_decision", principal, "match_candidate", m.id, body.model_dump())
    db.commit()
    return {"id": m.id, "status": m.status, "merge_id": merge.id if merge else None}


@router.get("/merges")
def merges(principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    return [row(mg, ["id", "survivor_id", "merged_id", "merged_by", "merged_at", "reason", "reversed_at", "reversed_by", "match_candidate_id"])
            for mg in db.scalars(select(ProjectMerge).order_by(ProjectMerge.merged_at.desc()))]


@router.post("/merges/{merge_id}/reverse")
def reverse(merge_id: int, request: Request, principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    try:
        mg = reverse_merge(db, merge_id, principal.user.id)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None
    audit(db, request, "review.merge_reversed", principal, "project_merge", merge_id)
    db.commit()
    return {"id": mg.id, "reversed_at": j(mg.reversed_at)}


class AlertReview(BaseModel):
    review_status: str = Field(pattern="^(open|acknowledged|confirmed|dismissed|resolved)$")
    note: str | None = Field(None, max_length=2000)


@router.post("/alerts/{alert_id}/review")
def review_alert(alert_id: int, body: AlertReview, request: Request, principal: Principal = Depends(REVIEW), db: Session = Depends(get_db)):
    a = db.get(ProjectAlert, alert_id)
    if a is None:
        raise HTTPException(404, "Not found")
    a.review_status, a.review_note = body.review_status, body.note
    a.reviewed_by, a.reviewed_at = principal.user.id, datetime.now(timezone.utc)
    audit(db, request, "review.alert", principal, "alert", a.public_id, body.model_dump())
    db.commit()
    return {"alert_id": a.public_id, "review_status": a.review_status}


class ThresholdIn(BaseModel):
    rule_code: str
    parameter: str
    value: str


@router.put("/thresholds")
def set_threshold(body: ThresholdIn, request: Request, principal: Principal = Depends(require(P_ADMIN_ORG)), db: Session = Depends(get_db)):
    """Institution-specific thresholds (organization scope); super admins set AP²I defaults with org=None."""
    from decimal import Decimal, InvalidOperation

    try:
        value = Decimal(body.value)
    except InvalidOperation:
        raise HTTPException(422, "value must be a number") from None
    org = None if principal.is_super_admin and not principal.organization_id else principal.organization_id
    default = db.scalar(select(AlertThreshold).where(AlertThreshold.organization_id.is_(None), AlertThreshold.rule_code == body.rule_code,
                                                     AlertThreshold.parameter == body.parameter))
    if default is None:
        raise HTTPException(404, "Unknown rule/parameter")
    t = db.scalar(select(AlertThreshold).where(AlertThreshold.organization_id == org if org else AlertThreshold.organization_id.is_(None),
                                               AlertThreshold.rule_code == body.rule_code, AlertThreshold.parameter == body.parameter))
    if t is None:
        t = AlertThreshold(organization_id=org, rule_code=body.rule_code, parameter=body.parameter, value=value)
        db.add(t)
    t.value = value
    audit(db, request, "admin.threshold_set", principal, "threshold", f"{body.rule_code}.{body.parameter}", body.model_dump())
    db.commit()
    return {"organization_id": org, "rule_code": t.rule_code, "parameter": t.parameter, "value": str(t.value)}


# --- users, organizations, subscriptions ---------------------------------------------------------------------

@router.get("/users")
def users(principal: Principal = Depends(require(P_ADMIN_ORG)), db: Session = Depends(get_db)):
    q = select(User)
    if not principal.is_super_admin:
        q = q.where(User.organization_id == principal.organization_id)
    return [{**row(u, ["id", "email", "full_name", "organization_id", "is_active", "email_verified_at", "mfa_enabled", "last_login_at", "created_at"]),
             "roles": [r.role.code for r in u.roles]} for u in db.scalars(q.order_by(User.id))]


class RolesIn(BaseModel):
    roles: list[str]
    is_active: bool | None = None
    organization_id: int | None = None


@router.put("/users/{user_id}/roles")
def set_roles(user_id: int, body: RolesIn, request: Request, principal: Principal = Depends(require(P_ADMIN_ORG)), db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if u is None or (not principal.is_super_admin and u.organization_id != principal.organization_id):
        raise HTTPException(404, "Not found")
    roles = {r.code: r for r in db.scalars(select(RoleDef))}
    unknown = [r for r in body.roles if r not in roles]
    if unknown:
        raise HTTPException(422, f"Unknown roles {unknown}")
    if not principal.is_super_admin and "ap2i_super_admin" in body.roles:
        raise HTTPException(403, "Only super administrators can grant this role")
    for ur in list(u.roles):
        db.delete(ur)
    db.flush()
    for code in body.roles:
        db.add(UserRole(user_id=u.id, role_id=roles[code].id, organization_id=u.organization_id))
    if body.is_active is not None:
        u.is_active = body.is_active
    if body.organization_id is not None and principal.is_super_admin:
        u.organization_id = body.organization_id
    u.token_version += 1
    audit(db, request, "admin.user_roles", principal, "user", u.id, body.model_dump())
    db.commit()
    return {"id": u.id, "roles": body.roles}


class OrgIn(BaseModel):
    name: str = Field(min_length=2, max_length=250)
    short_name: str | None = None
    org_type: str = "institution"
    is_tenant: bool = True
    country_iso3: str | None = None


@router.get("/organizations")
def orgs(principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    return [row(o, ["id", "name", "short_name", "org_type", "is_tenant", "iati_ref", "created_at"]) for o in db.scalars(select(Organization).order_by(Organization.id))]


@router.post("/organizations", status_code=201)
def create_org(body: OrgIn, request: Request, principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    country_id = db.scalar(select(Country.id).where(Country.iso3 == body.country_iso3.upper())) if body.country_iso3 else None
    o = Organization(name=body.name, short_name=body.short_name, org_type=body.org_type, is_tenant=body.is_tenant, country_id=country_id)
    db.add(o)
    audit(db, request, "admin.org_created", principal, "organization", body.name)
    db.commit()
    return row(o, ["id", "name", "short_name", "org_type", "is_tenant"])


class GrantIn(BaseModel):
    plan: str
    user_id: int | None = None
    organization_id: int | None = None
    ends_on: str | None = None
    seats: int | None = None


@router.post("/subscriptions", status_code=201)
def grant_subscription(body: GrantIn, request: Request, principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    from datetime import date

    plan = db.scalar(select(Plan).where(Plan.code == body.plan))
    if plan is None or (body.user_id is None and body.organization_id is None):
        raise HTTPException(422, "plan and user_id or organization_id required")
    s = Subscription(plan_id=plan.id, user_id=body.user_id, organization_id=body.organization_id, status="active",
                     starts_on=date.today(), ends_on=date.fromisoformat(body.ends_on) if body.ends_on else None, seats=body.seats)
    db.add(s)
    audit(db, request, "admin.subscription_granted", principal, "subscription", body.plan, body.model_dump())
    db.commit()
    return {"id": s.id, "plan": plan.code, "status": s.status}


@router.get("/subscriptions")
def list_subscriptions(principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    return [{**row(s, ["id", "user_id", "organization_id", "status", "starts_on", "ends_on", "seats", "created_at"]), "plan": s.plan.code}
            for s in db.scalars(select(Subscription).order_by(Subscription.id.desc()))]


# --- countries (activation is configuration) ---------------------------------------------------------------------

@router.post("/countries/sync-activation")
def sync_activation(request: Request, principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    active = sync_active_countries(db)
    audit(db, request, "admin.countries_activation_synced", principal, detail={"active": active})
    db.commit()
    return {"active_countries": active, "source": "AP2I_ACTIVE_COUNTRIES"}


# --- settings, audit, system ---------------------------------------------------------------------------------------

class SettingIn(BaseModel):
    value: dict


@router.get("/settings")
def get_settings_api(principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    s = get_settings()
    stored = {x.key: x.value for x in db.scalars(select(AppSetting))}
    return {"stored": stored, "runtime": {"environment": s.environment, "active_countries": s.active_countries,
                                          "llm_provider": s.llm_provider, "llm_model": s.llm_model, "llm_configured": bool(s.llm_api_key),
                                          "payment_provider": s.payment_provider, "email_backend": s.email_backend,
                                          "iati_official_api_key_configured": bool(s.iati_api_key)}}


@router.put("/settings/{key}")
def put_setting(key: str, body: SettingIn, request: Request, principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    if key not in ("ai", "rescue", "reports", "ui"):
        raise HTTPException(422, "Unknown setting group")
    if any(k.lower() in ("api_key", "secret", "password", "token") for k in body.value):
        raise HTTPException(422, "Secrets must be provided through environment variables, not stored settings")
    s = db.get(AppSetting, key) or AppSetting(key=key, value={})
    s.value, s.updated_by = body.value, principal.user.id
    db.add(s)
    audit(db, request, "admin.setting", principal, "setting", key)
    db.commit()
    return {"key": key, "value": s.value}


@router.get("/audit-logs")
def audit_logs(limit: int = 200, action: str | None = None, principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    q = select(AuditLog)
    if action:
        q = q.where(AuditLog.action == action)
    return [row(a, ["id", "at", "user_id", "organization_id", "action", "entity_type", "entity_id", "method", "path", "status_code",
                    "ip_truncated", "detail"]) for a in db.scalars(q.order_by(AuditLog.id.desc()).limit(min(limit, 1000)))]


@router.get("/system")
def system(principal: Principal = Depends(ADMIN), db: Session = Depends(get_db)):
    from sqlalchemy import text

    db_ok = db.execute(text("SELECT 1")).scalar() == 1
    redis_ok = None
    try:
        import redis

        redis_ok = bool(redis.Redis.from_url(get_settings().redis_url, socket_timeout=2).ping())
    except Exception:  # noqa: BLE001
        redis_ok = False
    postgis = None
    if db.bind.dialect.name == "postgresql":
        postgis = db.execute(text("SELECT extversion FROM pg_extension WHERE extname='postgis'")).scalar()
    return {"database": db_ok, "redis": redis_ok, "postgis_version": postgis,
            "running_syncs": db.scalar(select(func.count(SyncRun.id)).where(SyncRun.status == "running")),
            "failed_runs_7d": db.scalar(select(func.count(SyncRun.id)).where(SyncRun.status == "failed"))}
