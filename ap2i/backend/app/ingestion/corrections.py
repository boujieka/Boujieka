"""Systematic data corrections applied after each sync. Every correction is logged as a DataValidation note;
source records are never modified (they keep the original values)."""

from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.connectors.base import NULL_DATE_SENTINELS
from app.models import (
    DataValidation,
    Disbursement,
    FinancingAgreement,
    FinancingCommitment,
    Project,
    ResultsIndicator,
    ResultsObservation,
    SourceObservation,
)


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
    # An observed (actual) result cannot be dated in the future: IATI dates it by the end of a still-open period.
    out["future_result_dates_cleared"] = 0
    future = db.execute(select(ResultsObservation, ResultsIndicator.project_id).join(
        ResultsIndicator, ResultsIndicator.id == ResultsObservation.indicator_id).where(ResultsObservation.period_end > today)).all()
    per_project: dict[int, int] = {}
    for o, pid in future:
        o.period_end = None
        per_project[pid] = per_project.get(pid, 0) + 1
        out["future_result_dates_cleared"] += 1
    for pid, n in per_project.items():
        db.add(DataValidation(project_id=pid, rule="future_result_date", severity="info",
                              message=f"{n} results value(s) were dated by the end of a reporting period after {today}; the value "
                                      "is kept without a date (measurement date not given by the source)"))
    for o in db.scalars(select(ResultsObservation).where(ResultsObservation.period_end.in_(NULL_DATE_SENTINELS))):
        o.period_end = None
        out["placeholder_dates_cleared"] += 1
    out.update(dedupe_identical_transactions(db))
    out.update(eu_decision_vs_contract(db))
    db.commit()
    return out


DUP_NOTE = "Identical repeat of transaction #{keep} in the source file (same date, amount and currency); counted once"


def dedupe_identical_transactions(db: Session) -> dict:
    """Some publishers repeat the same transaction several times in one file, with only the reference changed (e.g. one
    EIB loan of EUR 50M published as 17 identical EUR 50M commitments on the same date; AfDB quarterly totals published
    three times). Identical counted rows of one agreement (same kind, date, amount, currency) are counted once; the
    repeats stay stored with `is_counted=False` and a note, and a DataValidation is recorded for review."""
    out = {"duplicate_commitments_not_counted": 0, "duplicate_flows_not_counted": 0}
    # the commitment "type" is not part of the key: the importer labels the first commitment of an agreement "original"
    # and the following ones "additional", so identical repeats would otherwise differ by that label only
    for model, key_cols, label in ((FinancingCommitment, (), "duplicate_commitments_not_counted"),
                                   (Disbursement, (Disbursement.flow_type,), "duplicate_flows_not_counted")):
        groups = db.execute(select(model.agreement_id, *key_cols, model.value_date, model.amount, model.currency,
                                   func.min(model.id), func.count()).where(model.is_counted.is_(True), model.value_date.is_not(None))
                            .group_by(model.agreement_id, *key_cols, model.value_date, model.amount, model.currency)
                            .having(func.count() > 1)).all()
        for g in groups:
            agreement_id, value_date, amount, currency, keep = g[0], g[-5], g[-4], g[-3], g[-2]
            rows = db.scalars(select(model).where(model.agreement_id == agreement_id, model.is_counted.is_(True),
                                                  model.value_date == value_date, model.amount == amount, model.currency == currency,
                                                  *(c == g[1 + i] for i, c in enumerate(key_cols)), model.id != keep)).all()
            for r in rows:
                r.is_counted = False
                r.counting_note = DUP_NOTE.format(keep=keep)
                out[label] += 1
            agr = db.get(FinancingAgreement, agreement_id)
            db.add(DataValidation(project_id=agr.project_id, source_record_id=agr.source_record_id, rule="duplicate_transaction",
                                  severity="warning", message=f"{agr.source_identifier}: {len(rows) + 1} identical transactions "
                                  f"({value_date}, {amount} {currency}) in the source; counted once"))
    return out


EU_DECISION = r"^XI-IATI-EC_INTPA-.*-ACT-"


def eu_decision_vs_contract(db: Session) -> dict:
    """EU (DG INTPA) publishes a financing decision (`…-ACT-…`) and the contracts that implement it (`…-PC/PCC-…`). When
    both are attached to one project, counting both commitments double-counts the same money: the contracts (legal
    commitments, which also carry the disbursements) are counted, the decision envelope is not."""
    out = {"eu_decision_commitments_not_counted": 0}
    decisions = db.scalars(select(FinancingAgreement).where(FinancingAgreement.source_identifier.op("~")(EU_DECISION))).all()
    for d in decisions:
        contracts = db.scalars(select(FinancingAgreement.id).where(
            FinancingAgreement.project_id == d.project_id, FinancingAgreement.id != d.id,
            FinancingAgreement.source_identifier.like("XI-IATI-EC_INTPA-%"),
            ~FinancingAgreement.source_identifier.op("~")(EU_DECISION))).all()
        if not contracts or not db.scalar(select(func.count(FinancingCommitment.id)).where(
                FinancingCommitment.agreement_id.in_(contracts), FinancingCommitment.is_counted.is_(True))):
            continue
        rows = db.scalars(select(FinancingCommitment).where(FinancingCommitment.agreement_id == d.id,
                                                            FinancingCommitment.is_counted.is_(True))).all()
        for r in rows:
            r.is_counted = False
            r.counting_note = "EU financing decision envelope: the implementing contracts of the same project are counted instead"
            out["eu_decision_commitments_not_counted"] += 1
        if rows:
            db.add(DataValidation(project_id=d.project_id, source_record_id=d.source_record_id, rule="eu_decision_not_counted",
                                  severity="info", message=f"{d.source_identifier}: decision-level commitment not counted; "
                                  f"{len(contracts)} contract(s) of the same project counted"))
    return out
