"""Data quality framework (Master prompt §28) and per-project completeness."""

from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    DataQualityAssessment,
    DataValidation,
    Disbursement,
    FinancingAgreement,
    MatchCandidate,
    Project,
    ProjectSourceLink,
    SourceConnector,
    SourceObservation,
    SourceRecord,
    SyncRun,
)

KEY_FIELDS = [
    ("title", "Title"), ("description", "Description"), ("objectives", "Objectives"), ("sector_id", "Sector"),
    ("executing_agency", "Executing agency"), ("original_approval_date", "Approval date"),
    ("implementation_start_date", "Start date"), ("original_completion_date", "Planned completion date"),
    ("original_estimated_cost", "Estimated cost"), ("physical_progress_pct", "Physical progress"),
    ("region_id", "Region"),
]
SOURCE_RELIABILITY = {"wb_project": 1.0, "iati_activity": 0.9, "upload_project_row": 0.7}


def assess_project(db: Session, p: Project, today: date | None = None) -> DataQualityAssessment:
    today = today or date.today()
    missing = [label for attr, label in KEY_FIELDS if getattr(p, attr) in (None, "")]
    if p.operational_status == "unknown":
        missing.append("Operational status")
    agreements = db.scalars(select(FinancingAgreement).where(FinancingAgreement.project_id == p.id)).all()
    if not agreements:
        missing.append("Financing information")
    elif all(a.amount_original is None and a.reported_current_commitment is None for a in agreements):
        missing.append("Financing amount")
    has_disb = any(a.reported_cumulative_disbursed is not None for a in agreements) or (
        bool(agreements) and db.scalar(select(func.count(Disbursement.id)).where(Disbursement.agreement_id.in_([a.id for a in agreements]))) > 0)
    if not has_disb:
        missing.append("Disbursements")
    total = len(KEY_FIELDS) + 3
    completeness = round(1 - len(missing) / total, 3)

    links = db.scalars(select(ProjectSourceLink).where(ProjectSourceLink.project_id == p.id, ProjectSourceLink.active.is_(True))).all()
    observed_fields = set(db.scalars(select(SourceObservation.field).where(SourceObservation.project_id == p.id)))
    set_fields = [attr for attr, _ in KEY_FIELDS if getattr(p, attr) not in (None, "")]
    traceable = [a for a in set_fields if a in observed_fields or a in ("title", "sector_id", "region_id")]
    traceability = round(len(traceable) / len(set_fields), 3) if set_fields else 0.0
    if not links:
        traceability = 0.0

    stated = []
    types = []
    for sr in db.scalars(select(SourceRecord).where(SourceRecord.id.in_([lk.source_record_id for lk in links]))):
        types.append(sr.record_type)
        if sr.source_last_updated:
            try:
                stated.append(date.fromisoformat(str(sr.source_last_updated)[:10]))
            except ValueError:
                pass
    timeliness = None
    if stated:
        age_m = (today - max(stated)).days / 30.44
        timeliness = round(max(0.0, 1 - age_m / 24), 3)
    reliability = round(max((SOURCE_RELIABILITY.get(t, 0.5) for t in types), default=0.0), 3)
    dup = db.scalar(select(func.count(MatchCandidate.id)).where(
        MatchCandidate.status == "pending", (MatchCandidate.project_a_id == p.id) | (MatchCandidate.project_b_id == p.id)))
    open_issues = db.scalar(select(func.count(DataValidation.id)).where(DataValidation.project_id == p.id,
                                                                        DataValidation.severity.in_(("error", "warning")),
                                                                        DataValidation.status == "open"))
    consistency = round(max(0.0, 1 - 0.2 * open_issues), 3)
    for old in db.scalars(select(DataQualityAssessment).where(DataQualityAssessment.project_id == p.id,
                                                              DataQualityAssessment.is_current.is_(True))):
        old.is_current = False
    dqa = DataQualityAssessment(project_id=p.id, completeness=completeness, timeliness=timeliness, traceability=traceability,
                                consistency=consistency, source_reliability=reliability, duplicate_risk=1.0 if dup else 0.0,
                                missing_fields=missing, detail={"sources": len(links), "open_validation_issues": open_issues})
    db.add(dqa)
    return dqa


def assess_all(db: Session, country_id: int | None = None) -> int:
    q = select(Project).where(Project.merged_into_id.is_(None))
    if country_id:
        q = q.where(Project.country_id == country_id)
    n = 0
    for p in db.scalars(q):
        assess_project(db, p)
        n += 1
    db.commit()
    return n


def dashboard(db: Session, country_id: int | None = None) -> dict:
    pq = select(Project).where(Project.merged_into_id.is_(None), Project.tenant_id.is_(None))
    if country_id:
        pq = pq.where(Project.country_id == country_id)
    projects = db.scalars(pq).all()
    ids = [p.id for p in projects]
    by_verif: dict[str, int] = {}
    for p in projects:
        by_verif[p.verification_status] = by_verif.get(p.verification_status, 0) + 1
    current = db.scalars(select(DataQualityAssessment).where(DataQualityAssessment.is_current.is_(True),
                                                             DataQualityAssessment.project_id.in_(ids))).all() if ids else []
    missing_counts: dict[str, int] = {}
    for d in current:
        for m in d.missing_fields:
            missing_counts[m] = missing_counts.get(m, 0) + 1
    outdated = sum(1 for d in current if d.timeliness is not None and d.timeliness == 0)
    connectors = []
    for c in db.scalars(select(SourceConnector).order_by(SourceConnector.tier, SourceConnector.key)):
        last = db.scalar(select(SyncRun).where(SyncRun.connector_id == c.id).order_by(SyncRun.started_at.desc()))
        stored = db.scalar(select(func.count(SourceRecord.id)).where(SourceRecord.connector_id == c.id, SourceRecord.is_latest.is_(True)))
        connectors.append({
            "key": c.key, "name": c.name, "tier": c.tier, "enabled": c.enabled, "status": c.status,
            "last_success_at": c.last_success_at.isoformat() if c.last_success_at else None,
            "last_failure_at": c.last_failure_at.isoformat() if c.last_failure_at else None,
            "last_error": c.last_error, "records_stored": stored,
            "last_run": None if last is None else {"id": last.id, "status": last.status, "retrieved": last.records_retrieved,
                                                   "imported": last.records_imported, "review": last.records_review,
                                                   "failed": last.records_failed,
                                                   "finished_at": last.finished_at.isoformat() if last.finished_at else None},
        })
    failed_imports = db.scalar(select(func.count(SourceRecord.id)).where(SourceRecord.processing_status == "failed"))
    review_records = db.scalar(select(func.count(SourceRecord.id)).where(SourceRecord.processing_status == "review"))
    pending_dups = db.scalar(select(func.count(MatchCandidate.id)).where(MatchCandidate.status == "pending"))
    def avg(attr):
        vals = [getattr(d, attr) for d in current if getattr(d, attr) is not None]
        return round(sum(vals) / len(vals), 3) if vals else None
    return {
        "projects": len(projects),
        "verification": by_verif,
        "verified_records": by_verif.get("verified", 0),
        "unverified_records": by_verif.get("unverified", 0),
        "records_requiring_review": review_records,
        "missing_information": dict(sorted(missing_counts.items(), key=lambda kv: -kv[1])),
        "outdated_observations": outdated,
        "potential_duplicates": pending_dups,
        "failed_imports": failed_imports,
        "average_scores": {k: avg(k) for k in ("completeness", "timeliness", "traceability", "consistency", "source_reliability")},
        "connectors": connectors,
        "assessed_at": datetime.now(timezone.utc).isoformat(),
        "coverage_warning": "These figures describe the records imported into AP²I, not the complete national investment portfolio.",
    }
