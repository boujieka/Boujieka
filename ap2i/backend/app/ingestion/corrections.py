"""Systematic data corrections applied after each sync. Every correction is logged as a DataValidation note;
source records are never modified (they keep the original values)."""

from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.connectors.base import NULL_DATE_SENTINELS
from app.models import DataValidation, FinancingAgreement, Project, ResultsObservation, SourceObservation


def apply_corrections(db: Session, today: date | None = None) -> dict:
    today = today or date.today()
    out = {"future_actual_dates_cleared": 0, "placeholder_dates_cleared": 0}
    for p in db.scalars(select(Project).where((Project.actual_completion_date > today) | (Project.commissioning_date > today))):
        for attr in ("actual_completion_date", "commissioning_date"):
            v = getattr(p, attr)
            if v and v > today:
                db.add(DataValidation(project_id=p.id, rule="future_actual_date", severity="info",
                                      message=f"{attr}={v} is in the future and cannot be an actual date; cleared (source record unchanged)"))
                if attr == "actual_completion_date" and p.original_completion_date is None:
                    p.original_completion_date = v
                setattr(p, attr, None)
                out["future_actual_dates_cleared"] += 1
    # World Bank API `closingdate` is the CURRENT closing date. Earlier versions stored it as the original completion
    # date; clear it unless a supervision report (ISR) states the original closing date.
    out["wb_current_closing_cleared"] = 0
    rows = db.execute(select(Project, FinancingAgreement).join(FinancingAgreement, FinancingAgreement.project_id == Project.id).where(
        FinancingAgreement.source_identifier.op("~")(r"^P\d{6}$"), Project.original_completion_date.is_not(None),
        Project.original_completion_date == FinancingAgreement.closing_date_current)).all()
    for p, agr in rows:
        confirmed = db.scalar(select(SourceObservation.id).where(SourceObservation.project_id == p.id,
                                                                 SourceObservation.field == "original_closing_date",
                                                                 SourceObservation.value_date == p.original_completion_date))
        if confirmed:
            continue
        db.add(DataValidation(project_id=p.id, rule="wb_current_closing_not_original", severity="info",
                              message=f"original_completion_date={p.original_completion_date} came from the World Bank current closing date; "
                                      "cleared (kept as the financing's current closing date)"))
        p.original_completion_date = None
        out["wb_current_closing_cleared"] += 1
    for o in db.scalars(select(ResultsObservation).where(ResultsObservation.period_end.in_(NULL_DATE_SENTINELS))):
        o.period_end = None
        out["placeholder_dates_cleared"] += 1
    db.commit()
    return out
