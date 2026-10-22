"""AP²I Project Rescue (Master prompt §21).

Diagnosis and corrective-action drafting are EVIDENCE-BASED and rule-driven:
  * every proposed action is tied to one or more active alerts or documented indicators;
  * "likely contributing factors" are only stated when a source documents them; otherwise the
    text is exactly "Further investigation required.";
  * timeframes and budgets are never invented: they stay empty until a user sets them;
  * the responsible institution is the documented executing/implementing agency, else
    "To be determined";
  * AI-generated suggestions (optional, see app.assistant) are stored with origin="ai" and
    status "proposed" until a user approves, rejects or modifies them.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.finance.indicators import project_financials
from app.models import Document, Project, ProjectAlert, ProjectRisk, RecoveryAction, RecoveryPlan

FURTHER = "Further investigation required."
PRIORITY = {"critical_attention": "critical", "high_attention": "high", "watch": "medium", "information": "low"}

# Rule -> (problem template, recommended action, expected result, monitoring indicator, dependencies)
PLAYBOOK: dict[str, tuple[str, str, str, str, str | None]] = {
    "LOW_DISBURSEMENT": (
        "Disbursement is low relative to the time elapsed.",
        "Hold a disbursement review with the executing agency and the financing partner: reconcile the disbursement "
        "plan with the procurement plan, list contracts awaiting signature or payment, and agree a dated catch-up plan.",
        "An agreed, dated disbursement catch-up plan.",
        "Cumulative disbursement rate (quarterly) against the agreed plan.",
        "Availability of the latest procurement plan and disbursement forecast.",
    ),
    "CLOSING_DATE_PASSED": (
        "The project is reported active after its planned end date.",
        "Confirm the official closing date with the financing partner; if an extension was granted, obtain the amendment; "
        "if not, prepare closing actions (final disbursements, completion report).",
        "Closing date and status confirmed by an official document.",
        "Status and closing date as published by the financing partner.",
        None,
    ),
    "SCHEDULE_EXTENSION": (
        "The closing date has moved significantly later than planned.",
        "Review the documented reasons for the extension and check that the remaining work programme fits the new date.",
        "A realistic, documented completion schedule.",
        "Milestones achieved versus the revised schedule.",
        "Access to the restructuring paper or amendment.",
    ),
    "COST_REVISION": (
        "The estimated cost has been revised upward significantly.",
        "Obtain the cost revision justification and the updated financing plan; verify that the additional cost is financed.",
        "Revised cost justified and fully financed.",
        "Revised cost versus approved financing plan.",
        None,
    ),
    "REPEATED_AMENDMENTS": (
        "Contracts have been amended repeatedly.",
        "Review the amendments' cumulative effect on cost and schedule with the procurement authority.",
        "Amendment history reviewed; corrective measures agreed if needed.",
        "Number and value of amendments per contract.",
        None,
    ),
    "FINANCING_GAP": (
        "Recorded financing does not cover the estimated cost.",
        "Establish the complete financing plan (all partners, counterpart funds) and identify the unfunded components.",
        "Complete, documented financing plan.",
        "Financing gap in the cost currency.",
        None,
    ),
    "CANCELLATION": (
        "A significant part of the financing has been cancelled.",
        "Check what scope the cancellation removed and whether the expected outputs were revised accordingly.",
        "Outputs and targets aligned with the remaining financing.",
        "Remaining commitment and revised targets.",
        None,
    ),
    "PHYS_FIN_GAP": (
        "Physical and financial progress are inconsistent.",
        "Reconcile physical progress measurements with payment records for the same date (site report vs. payment ledger).",
        "Reconciled physical and financial progress.",
        "Gap between physical and financial progress (percentage points).",
        None,
    ),
    "COMPLETED_NOT_OPERATIONAL": (
        "Completed infrastructure is documented as not operational.",
        "Organise a joint site verification with the operator; identify the missing conditions for operation (staff, "
        "equipment, connection, operating budget) and assign each to an institution.",
        "Infrastructure in operation, or a dated plan to bring it into operation.",
        "Operational status confirmed by the operator.",
        "Identification of the operating entity.",
    ),
    "OPERATIONAL_STATUS_UNVERIFIED": (
        "The operational status of completed infrastructure is not documented.",
        "Obtain a dated operational-status statement from the operator or a site verification.",
        "Documented operational status.",
        "Operational status observation (date, source).",
        None,
    ),
    "MISSING_PROGRESS_REPORT": (
        "No recent implementation information is available.",
        "Request the latest implementation progress report from the executing agency or the financing partner.",
        "Up-to-date implementation information.",
        "Date of latest progress report.",
        None,
    ),
    "NO_DISBURSEMENT_DATA": (
        "Disbursement information is not published.",
        "Request disbursement data (cumulative and by year) from the financing partner or executing agency.",
        "Disbursement data available for monitoring.",
        "Availability of dated disbursement data.",
        None,
    ),
}


def _documented_factors(db: Session, project: Project) -> str:
    """Only causes documented in sources (project risks). Never AI-invented."""
    risks = db.scalars(select(ProjectRisk).where(ProjectRisk.project_id == project.id)).all()
    if not risks:
        return FURTHER
    return "Documented in sources: " + "; ".join(f"{r.category}: {r.description}" for r in risks[:5])


def diagnose(db: Session, project: Project) -> dict:
    alerts = db.scalars(select(ProjectAlert).where(ProjectAlert.project_id == project.id, ProjectAlert.is_active.is_(True))
                        .order_by(ProjectAlert.level)).all()
    fin = project_financials(db, project)
    docs = db.scalars(select(Document).where(Document.project_id == project.id)).all()
    sections = {
        "financial_gap_analysis": [i for i in fin["indicators"] if i["code"] in ("financing_gap", "disbursement_rate")],
        "schedule_analysis": [i for i in fin["indicators"] if i["code"] in ("elapsed_time_ratio", "schedule_slippage_days")],
        "contract_review": [i for i in fin["indicators"] if i["code"] == "contract_amendment_ratio"],
        "operational_readiness": {"operational_status": project.operational_status,
                                  "commissioning_date": project.commissioning_date.isoformat() if project.commissioning_date else None},
        "institutional_bottlenecks": FURTHER if not db.scalars(select(ProjectRisk).where(ProjectRisk.project_id == project.id)).first()
        else [r.description for r in db.scalars(select(ProjectRisk).where(ProjectRisk.project_id == project.id))],
    }
    return {
        "project": {"id": project.id, "ap2i_id": project.ap2i_id, "title": project.title, "status": project.status},
        "alerts": [{"id": a.id, "alert_id": a.public_id, "rule": a.rule_code, "level": a.level, "observed": a.observed_value,
                    "threshold": a.threshold, "source": a.source} for a in alerts],
        "sections": sections,
        "evidence_documents": [{"id": d.id, "title": d.title, "url": d.url} for d in docs[:20]],
        "method": "rules_v1 — deterministic rules on documented indicators; no causal inference",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def create_plan(db: Session, project: Project, user_id: int | None, tenant_id: int | None) -> RecoveryPlan:
    diag = diagnose(db, project)
    plan = RecoveryPlan(project_id=project.id, tenant_id=tenant_id, title=f"Recovery plan — {project.title[:200]}",
                        diagnosis=diag, status="draft", created_by=user_id)
    db.add(plan)
    db.flush()
    factors = _documented_factors(db, project)
    responsible = project.executing_agency or project.implementing_agency or "To be determined"
    alerts = db.scalars(select(ProjectAlert).where(ProjectAlert.project_id == project.id, ProjectAlert.is_active.is_(True))).all()
    by_rule: dict[str, list[ProjectAlert]] = {}
    for a in alerts:
        by_rule.setdefault(a.rule_code, []).append(a)
    for rule, items in by_rule.items():
        if rule not in PLAYBOOK:
            continue
        problem, action, result, indicator, deps = PLAYBOOK[rule]
        top = min(items, key=lambda a: ["critical_attention", "high_attention", "watch", "information"].index(a.level))
        db.add(RecoveryAction(
            plan_id=plan.id, problem=problem,
            evidence=[{"alert_id": a.public_id, "indicator": a.triggering_indicator, "observed": a.observed_value,
                       "threshold": a.threshold, "source": a.source, "source_record_ids": a.source_record_ids,
                       "as_of": a.as_of.isoformat()} for a in items],
            contributing_factors=factors, recommended_action=action, responsible_institution=responsible,
            priority=PRIORITY[top.level], estimated_timeframe=None, indicative_budget=None, dependencies=deps,
            expected_result=result, monitoring_indicator=indicator, origin="rule", data_nature="calculated",
            approval_status="proposed", implementation_status="not_started",
        ))
    if not by_rule:
        plan.diagnosis = {**diag, "summary": "No active alert: no corrective action proposed. " + FURTHER}
    db.flush()
    return plan


def decide_action(db: Session, action: RecoveryAction, decision: str, user_id: int, changes: dict | None = None) -> RecoveryAction:
    if decision not in ("approved", "rejected", "modified"):
        raise ValueError("decision must be approved, rejected or modified")
    editable = {"recommended_action", "responsible_institution", "priority", "estimated_timeframe", "indicative_budget",
                "budget_currency", "dependencies", "expected_result", "monitoring_indicator", "assigned_to", "due_date",
                "contributing_factors"}
    for k, v in (changes or {}).items():
        if k in editable:
            setattr(action, k, v)
    if changes and decision == "approved":
        decision = "modified"
    action.approval_status = decision
    action.decided_by = user_id
    action.decided_at = datetime.now(timezone.utc)
    if decision == "modified" and action.origin == "ai":
        action.data_nature = "calculated"  # human-validated
    db.flush()
    return action


def update_progress(db: Session, action: RecoveryAction, status: str, note: str | None, due: date | None = None) -> RecoveryAction:
    if status not in ("not_started", "in_progress", "blocked", "done", "cancelled"):
        raise ValueError("invalid implementation status")
    if action.approval_status not in ("approved", "modified"):
        raise ValueError("Only approved actions can be implemented")
    action.implementation_status = status
    if note:
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        action.progress_note = ((action.progress_note or "") + f"\n[{stamp}] {note}").strip()
    if due:
        action.due_date = due
    db.flush()
    return action


def plan_summary(plan: RecoveryPlan) -> dict:
    acts = plan.actions
    by_status: dict[str, int] = {}
    for a in acts:
        by_status[a.implementation_status] = by_status.get(a.implementation_status, 0) + 1
    approved = [a for a in acts if a.approval_status in ("approved", "modified")]
    done = [a for a in approved if a.implementation_status == "done"]
    return {"actions": len(acts), "approved": len(approved), "done": len(done), "by_status": by_status,
            "completion_rate": round(len(done) / len(approved), 3) if approved else None}
