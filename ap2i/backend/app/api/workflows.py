"""Project Rescue, Intelligence Assistant, reports, private portfolios, uploads, billing, saved searches."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.serial import j, row
from app.assistant.service import answer
from app.commerce.payments import PaymentsNotActivated, get_payment_provider
from app.config import get_settings
from app.connectors.base import SyncParams
from app.connectors.manual import (
    BUDGET_COLUMNS,
    PROJECT_COLUMNS,
    REQUIRED_BUDGET,
    ManualUploadConnector,
    UploadValidationError,
    read_table,
    validate_project_rows,
)
from app.db import get_db
from app.ingestion.pipeline import run_sync
from app.models import (
    AIAssessment,
    BudgetAllocation,
    Country,
    Notification,
    Plan,
    Project,
    RecoveryAction,
    RecoveryPlan,
    Report,
    SavedSearch,
    SourceConnector,
    SourceRecord,
    Subscription,
)
from app.reports.generator import REPORT_TYPES, generate
from app.rescue.engine import create_plan, decide_action, diagnose, plan_summary, update_progress
from app.security.deps import Principal, audit, get_principal, require, require_feature, require_user, tenant_filter, visible_project_or_404

router = APIRouter(tags=["workflows"])


# --- Project Rescue -----------------------------------------------------------------------------------

@router.get("/rescue/projects/{ref}/diagnosis")
def rescue_diagnosis(ref: str, principal: Principal = Depends(require_feature("project_rescue")), db: Session = Depends(get_db)):
    return diagnose(db, visible_project_or_404(db, ref, principal))


class PlanIn(BaseModel):
    project: str
    private: bool = True


def _plan_or_404(db: Session, plan_id: int, principal: Principal) -> RecoveryPlan:
    plan = db.scalar(select(RecoveryPlan).where(RecoveryPlan.id == plan_id, tenant_filter(RecoveryPlan, principal)))
    if plan is None:
        raise HTTPException(404, "Plan not found")
    return plan


def plan_out(db: Session, plan: RecoveryPlan) -> dict:
    p = db.get(Project, plan.project_id)
    return {**row(plan, ["id", "title", "status", "method", "created_at", "updated_at", "approved_at", "diagnosis"]),
            "project": {"id": p.id, "ap2i_id": p.ap2i_id, "title": p.title}, "private": plan.tenant_id is not None,
            "summary": plan_summary(plan),
            "actions": [{**row(a, ["id", "problem", "evidence", "contributing_factors", "recommended_action", "responsible_institution",
                                   "priority", "estimated_timeframe", "indicative_budget", "budget_currency", "dependencies",
                                   "expected_result", "monitoring_indicator", "origin", "data_nature", "approval_status",
                                   "implementation_status", "assigned_to", "due_date", "progress_note", "decided_at"])}
                        for a in plan.actions]}


@router.post("/rescue/plans", status_code=201)
def rescue_create(body: PlanIn, request: Request, principal: Principal = Depends(require_feature("project_rescue")),
                  db: Session = Depends(get_db)):
    if not principal.can("rescue:use"):
        raise HTTPException(403, "Missing permission: rescue:use")
    project = visible_project_or_404(db, body.project, principal)
    tenant = principal.organization_id if body.private else None
    if body.private and tenant is None:
        raise HTTPException(400, "Private plans need an organization workspace")
    plan = create_plan(db, project, principal.user.id, tenant)
    audit(db, request, "rescue.plan_created", principal, "recovery_plan", plan.id)
    db.commit()
    return plan_out(db, plan)


@router.get("/rescue/plans")
def rescue_list(principal: Principal = Depends(require_feature("project_rescue")), db: Session = Depends(get_db)):
    plans = db.scalars(select(RecoveryPlan).where(tenant_filter(RecoveryPlan, principal)).order_by(RecoveryPlan.updated_at.desc())).all()
    return [{"id": pl.id, "title": pl.title, "status": pl.status, "project_id": pl.project_id, "updated_at": j(pl.updated_at),
             "summary": plan_summary(pl)} for pl in plans]


@router.get("/rescue/plans/{plan_id}")
def rescue_get(plan_id: int, principal: Principal = Depends(require_feature("project_rescue")), db: Session = Depends(get_db)):
    return plan_out(db, _plan_or_404(db, plan_id, principal))


class DecisionIn(BaseModel):
    decision: str = Field(pattern="^(approved|rejected|modified)$")
    changes: dict = Field(default_factory=dict)


@router.post("/rescue/actions/{action_id}/decision")
def rescue_decide(action_id: int, body: DecisionIn, request: Request, principal: Principal = Depends(require_feature("project_rescue")),
                  db: Session = Depends(get_db)):
    action = db.get(RecoveryAction, action_id)
    if action is None:
        raise HTTPException(404, "Not found")
    _plan_or_404(db, action.plan_id, principal)
    changes = dict(body.changes)
    if "indicative_budget" in changes and changes["indicative_budget"] not in (None, ""):
        changes["indicative_budget"] = Decimal(str(changes["indicative_budget"]))
    if changes.get("due_date"):
        changes["due_date"] = date.fromisoformat(changes["due_date"])
    decide_action(db, action, body.decision, principal.user.id, changes)
    audit(db, request, "rescue.action_decision", principal, "recovery_action", action.id, {"decision": body.decision})
    db.commit()
    return row(action, ["id", "approval_status", "implementation_status", "recommended_action", "estimated_timeframe", "indicative_budget"])


class ProgressIn(BaseModel):
    status: str
    note: str | None = Field(None, max_length=2000)
    due_date: date | None = None


@router.post("/rescue/actions/{action_id}/progress")
def rescue_progress(action_id: int, body: ProgressIn, request: Request, principal: Principal = Depends(require_feature("project_rescue")),
                    db: Session = Depends(get_db)):
    action = db.get(RecoveryAction, action_id)
    if action is None:
        raise HTTPException(404, "Not found")
    plan = _plan_or_404(db, action.plan_id, principal)
    try:
        update_progress(db, action, body.status, body.note, body.due_date)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from None
    if all(a.implementation_status in ("done", "cancelled") for a in plan.actions if a.approval_status in ("approved", "modified")):
        plan.status = "completed" if any(a.approval_status in ("approved", "modified") for a in plan.actions) else plan.status
    elif plan.status == "draft":
        plan.status = "in_progress"
    audit(db, request, "rescue.action_progress", principal, "recovery_action", action.id, {"status": body.status})
    db.commit()
    return row(action, ["id", "implementation_status", "progress_note", "due_date"])


@router.get("/rescue/dashboard")
def rescue_dashboard(principal: Principal = Depends(require_feature("project_rescue")), db: Session = Depends(get_db)):
    plans = db.scalars(select(RecoveryPlan).where(tenant_filter(RecoveryPlan, principal))).all()
    actions = [a for p in plans for a in p.actions]
    by = lambda attr: {k: sum(1 for a in actions if getattr(a, attr) == k) for k in sorted({getattr(a, attr) for a in actions})}  # noqa: E731
    overdue = [a.id for a in actions if a.due_date and a.due_date < date.today() and a.implementation_status not in ("done", "cancelled")]
    return {"plans": len(plans), "actions": len(actions), "by_approval": by("approval_status"), "by_implementation": by("implementation_status"),
            "by_priority": by("priority"), "overdue_action_ids": overdue}


# --- Intelligence Assistant ---------------------------------------------------------------------------

class AskIn(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    country: str | None = None


@router.post("/assistant/ask")
def assistant_ask(body: AskIn, request: Request, principal: Principal = Depends(require("assistant:use")), db: Session = Depends(get_db)):
    ans = answer(db, body.question, tenant_filter(Project, principal), (body.country or get_settings().default_country).upper())
    out = ans.to_dict()
    db.add(AIAssessment(user_id=principal.user.id, tenant_id=principal.organization_id, kind="assistant_answer", provider=ans.provider,
                        question=body.question, output={"parsed": out["parsed"], "facts_count": len(ans.facts),
                                                        "narrative": ans.narrative}, citations=ans.citations[:100],
                        grounding_check=ans.grounding))
    audit(db, request, "assistant.ask", principal, detail={"intent": out["parsed"]["intent"]})
    db.commit()
    return out


# --- Reports --------------------------------------------------------------------------------------------

class ReportIn(BaseModel):
    report_type: str
    format: str = Field("pdf", pattern="^(pdf|xlsx|csv)$")
    country: str | None = None
    year_from: int | None = Field(None, ge=1960, le=2100)
    year_to: int | None = Field(None, ge=1960, le=2100)
    sector: str | None = None
    partner: str | None = None


@router.get("/reports/types")
def report_types():
    return [{"code": k, "title": v} for k, v in REPORT_TYPES.items()]


@router.post("/reports")
def create_report(body: ReportIn, request: Request, principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    if body.report_type not in REPORT_TYPES:
        raise HTTPException(422, "Unknown report type")
    if body.format != "csv" and not principal.has_feature("exports"):
        raise HTTPException(403, "PDF and Excel reports require a plan with exports")
    if body.report_type == "project_rescue" and not principal.has_feature("project_rescue"):
        raise HTTPException(403, "Project Rescue reports require an institutional plan")
    params = body.model_dump(exclude={"report_type", "format"}, exclude_none=True)
    try:
        rep, content, mime = generate(db, body.report_type, body.format, params, principal, principal.user.id, principal.organization_id)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None
    audit(db, request, "report.generated", principal, "report", rep.report_uid)
    db.commit()
    return Response(content, media_type=mime, headers={
        "Content-Disposition": f'attachment; filename="{rep.report_uid}.{body.format}"', "X-Report-Id": rep.report_uid})


@router.get("/reports")
def list_reports(principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    q = select(Report).where(Report.generated_by == principal.user.id).order_by(Report.generated_at.desc()).limit(100)
    return [row(r, ["report_uid", "report_type", "title", "fmt", "period", "generated_at", "sha256", "size_bytes"]) for r in db.scalars(q)]


# --- Uploads (documented official-data import workflow) ------------------------------------------------

@router.get("/uploads/templates")
def upload_templates():
    return {"projects": {"columns": PROJECT_COLUMNS, "required": ["country_iso3", "source_project_id", "title", "source_url", "reporting_date"]},
            "budget_lines": {"columns": BUDGET_COLUMNS, "required": REQUIRED_BUDGET},
            "rules": ["Every row must reproduce an official document cited in source_url/source_document.",
                      "Amounts in their original currency; dates YYYY-MM-DD; empty = not available (never 0 for unknown).",
                      "Budget appropriations are not commitments or disbursements and are stored separately."]}


def _check_upload(file: UploadFile, content: bytes) -> None:
    if len(content) > get_settings().upload_max_bytes:
        raise HTTPException(413, "File too large")
    name = (file.filename or "").lower()
    if not name.endswith((".csv", ".xlsx")):
        raise HTTPException(415, "Only .csv and .xlsx files are accepted")
    if name.endswith(".xlsx") and not content.startswith(b"PK"):
        raise HTTPException(415, "Not a valid .xlsx file")
    if name.endswith(".csv") and b"\x00" in content[:4096]:
        raise HTTPException(415, "Binary content in CSV")


@router.post("/uploads/projects")
async def upload_projects(request: Request, file: UploadFile = File(...), private: bool = Form(False),
                          principal: Principal = Depends(require("data:contribute")), db: Session = Depends(get_db)):
    content = await file.read()
    _check_upload(file, content)
    try:
        rows = read_table(content, file.filename or "upload.csv")
    except UploadValidationError as exc:
        raise HTTPException(422, exc.errors) from None
    except (UnicodeDecodeError, ValueError):
        raise HTTPException(422, "File could not be read as UTF-8 CSV or XLSX") from None
    errors = validate_project_rows(rows)
    known = {c for c in db.scalars(select(Country.iso3))}
    errors += [{"row": i, "field": "country_iso3", "error": "unknown country"} for i, r in enumerate(rows, 2)
               if r.get("country_iso3") and r["country_iso3"].upper() not in known]
    if errors:
        return {"imported": 0, "errors": errors[:500], "message": "Nothing imported: correct the listed rows."}
    tenant = principal.organization_id if private else None
    if private and tenant is None:
        raise HTTPException(400, "Private imports need an organization workspace")
    if not private and not principal.can("data:review"):
        # Public data from contributors stays private until a reviewer publishes it.
        tenant = principal.organization_id
    connector = ManualUploadConnector(rows=rows, uploaded_by=principal.user.email)
    run = run_sync(db, "manual_upload", trigger="manual", connector=connector, tenant_id=tenant, force=True,
                   params=SyncParams(countries=sorted({r["country_iso3"].upper() for r in rows})))
    audit(db, request, "upload.projects", principal, "sync_run", run.id, {"rows": len(rows), "private": tenant is not None})
    db.commit()
    return {"run_id": run.id, "status": run.status, "imported": run.records_imported, "review": run.records_review,
            "failed": run.records_failed, "errors": run.errors, "visibility": "private" if tenant else "public"}


@router.post("/uploads/budget-lines")
async def upload_budget(request: Request, file: UploadFile = File(...), principal: Principal = Depends(require("data:contribute")),
                        db: Session = Depends(get_db)):
    from app.connectors.base import parse_date, parse_decimal
    import hashlib
    import json

    content = await file.read()
    _check_upload(file, content)
    rows = read_table(content, file.filename or "budget.csv")
    errors = []
    countries = {c.iso3: c for c in db.scalars(select(Country))}
    for i, r in enumerate(rows, 2):
        for c in REQUIRED_BUDGET:
            if not r.get(c):
                errors.append({"row": i, "field": c, "error": "required"})
        if r.get("country_iso3", "").upper() not in countries:
            errors.append({"row": i, "field": "country_iso3", "error": "unknown country"})
        for c in ("approved_appropriation", "revised_appropriation", "commitment", "payment"):
            if r.get(c) and parse_decimal(r[c]) is None:
                errors.append({"row": i, "field": c, "error": "not a number"})
        if r.get("reporting_date") and parse_date(r["reporting_date"]) is None:
            errors.append({"row": i, "field": "reporting_date", "error": "date must be YYYY-MM-DD"})
        if r.get("budget_year") and not r["budget_year"].isdigit():
            errors.append({"row": i, "field": "budget_year", "error": "must be a year"})
    if errors:
        return {"imported": 0, "errors": errors[:500]}
    conn = db.scalar(select(SourceConnector).where(SourceConnector.key == "manual_upload"))
    n = 0
    for r in rows:
        payload = {**r, "_uploaded_by": principal.user.email}
        sha = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        ident = f"budget:{r['country_iso3'].upper()}:{r['budget_year']}:{r['budget_line_code']}"
        if db.scalar(select(SourceRecord).where(SourceRecord.connector_id == conn.id, SourceRecord.payload_sha256 == sha,
                                                SourceRecord.source_identifier == ident)):
            continue
        src = SourceRecord(connector_id=conn.id, source_identifier=ident, record_type="budget_line", country_iso3=r["country_iso3"].upper(),
                           payload=payload, payload_sha256=sha, source_url=r.get("source_url"), source_last_updated=r.get("reporting_date"),
                           processing_status="imported", tenant_id=principal.organization_id if not principal.can("data:review") else None)
        db.add(src)
        db.flush()
        db.add(BudgetAllocation(
            country_id=countries[r["country_iso3"].upper()].id, budget_year=int(r["budget_year"]), budget_line_code=r["budget_line_code"],
            project_identifier=r.get("project_identifier") or None, project_label=r.get("project_label") or None,
            administrative_classification=r.get("administrative_classification") or None,
            program_classification=r.get("program_classification") or None, funding_source=r.get("funding_source") or None,
            funding_type=r.get("funding_type") or "unknown", currency=r["currency"].upper(),
            approved_appropriation=parse_decimal(r.get("approved_appropriation")), revised_appropriation=parse_decimal(r.get("revised_appropriation")),
            commitment=parse_decimal(r.get("commitment")), payment=parse_decimal(r.get("payment")), source_record_id=src.id))
        n += 1
    audit(db, request, "upload.budget_lines", principal, detail={"rows": n})
    db.commit()
    return {"imported": n, "errors": []}


@router.get("/budget")
def budget_lines(country: str = "CMR", year: int | None = None, db: Session = Depends(get_db)):
    c = db.scalar(select(Country).where(Country.iso3 == country.upper()))
    if c is None:
        raise HTTPException(404, "Unknown country")
    q = select(BudgetAllocation).join(SourceRecord, SourceRecord.id == BudgetAllocation.source_record_id).where(
        BudgetAllocation.country_id == c.id, SourceRecord.tenant_id.is_(None))
    if year:
        q = q.where(BudgetAllocation.budget_year == year)
    items = []
    for b in db.scalars(q.order_by(BudgetAllocation.budget_year, BudgetAllocation.budget_line_code)):
        d = row(b, ["budget_year", "budget_line_code", "project_identifier", "project_label", "administrative_classification",
                    "program_classification", "funding_source", "funding_type", "currency", "approved_appropriation",
                    "revised_appropriation", "commitment", "payment", "source_record_id"])
        base = b.revised_appropriation if b.revised_appropriation is not None else b.approved_appropriation
        d["execution_rate"] = str((b.payment / base).quantize(Decimal("0.0001"))) if b.payment is not None and base else None
        d["execution_rate_formula"] = "payment / (revised appropriation, else approved appropriation)"
        items.append(d)
    return {"items": items, "note": "Budget appropriations are not financing commitments or disbursements."}


# --- Billing & saved searches & notifications --------------------------------------------------------------

@router.get("/plans")
def plans(db: Session = Depends(get_db)):
    return [{**row(p, ["code", "name_en", "name_fr", "price_amount", "price_currency", "billing_period", "features"]),
             "price_note": "On request" if p.price_amount is None else None}
            for p in db.scalars(select(Plan).where(Plan.is_public.is_(True)).order_by(Plan.sort_order))]


class SubscribeIn(BaseModel):
    plan: str


@router.post("/billing/checkout")
def checkout(body: SubscribeIn, principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    plan = db.scalar(select(Plan).where(Plan.code == body.plan))
    if plan is None:
        raise HTTPException(404, "Unknown plan")
    try:
        provider = get_payment_provider()
        provider.create_checkout(0, plan.price_amount or Decimal(0), plan.price_currency or "EUR", principal.user.email)
    except PaymentsNotActivated as exc:
        sub = Subscription(plan_id=plan.id, user_id=principal.user.id, organization_id=principal.organization_id, status="pending_payment")
        db.add(sub)
        db.add(Notification(kind="subscription_request", title=f"Subscription request: {plan.code}",
                            body=f"{principal.user.email} requested the {plan.code} plan", link="/admin/subscriptions"))
        db.commit()
        raise HTTPException(402, {"message": str(exc), "subscription_request_id": sub.id}) from None
    raise HTTPException(501, "Unreachable")


class SavedSearchIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    query: dict


@router.get("/saved-searches")
def saved_list(principal: Principal = Depends(require_feature("saved_searches")), db: Session = Depends(get_db)):
    return [row(s, ["id", "name", "query", "created_at"]) for s in db.scalars(select(SavedSearch).where(SavedSearch.user_id == principal.user.id))]


@router.post("/saved-searches", status_code=201)
def saved_create(body: SavedSearchIn, principal: Principal = Depends(require_feature("saved_searches")), db: Session = Depends(get_db)):
    s = SavedSearch(user_id=principal.user.id, name=body.name, query=body.query)
    db.add(s)
    db.commit()
    return row(s, ["id", "name", "query", "created_at"])


@router.delete("/saved-searches/{sid}")
def saved_delete(sid: int, principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    s = db.get(SavedSearch, sid)
    if s is None or s.user_id != principal.user.id:
        raise HTTPException(404, "Not found")
    db.delete(s)
    db.commit()
    return {"status": "deleted"}


@router.get("/notifications")
def notifications(principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    q = select(Notification).where((Notification.user_id == principal.user.id) |
                                   ((Notification.user_id.is_(None)) & principal.can("admin:all")))
    return [row(n, ["id", "kind", "title", "body", "link", "read_at", "created_at"]) for n in db.scalars(q.order_by(Notification.created_at.desc()).limit(100))]


__all__ = ["router", "func", "get_principal"]
