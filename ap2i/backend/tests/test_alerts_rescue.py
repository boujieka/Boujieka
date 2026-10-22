from datetime import date
from decimal import Decimal

from sqlalchemy import select

import app.models as m
from app.performance.alerts import run_alerts
from app.rescue.engine import FURTHER, create_plan, decide_action, update_progress


def test_alerts_generated_from_documented_rules(loaded):
    db = loaded
    run_alerts(db, today=date(2026, 6, 1))
    alerts = db.scalars(select(m.ProjectAlert).where(m.ProjectAlert.is_active.is_(True))).all()
    rules = {a.rule_code for a in alerts}
    # P900001: 10% disbursed with ~94% of 2018-03 -> 2025-12 elapsed; closing date passed while active.
    assert "LOW_DISBURSEMENT" in rules and "CLOSING_DATE_PASSED" in rules
    low = next(a for a in alerts if a.rule_code == "LOW_DISBURSEMENT")
    assert low.observed_value and low.threshold and low.source and low.recommended_verification and low.explanation
    assert low.level in ("high_attention", "critical_attention")
    for a in alerts:
        text = (a.explanation + a.recommended_verification).lower()
        assert "fraud" not in text and "corrupt" not in text


def test_alerts_idempotent_and_deactivate(loaded):
    db = loaded
    r1 = run_alerts(db, today=date(2026, 6, 1))
    r2 = run_alerts(db, today=date(2026, 6, 1))
    assert r2["alerts_created"] == 0 and r1["alerts_created"] > 0
    run_alerts(db, today=date(2019, 1, 1))  # earlier date: closing date not yet passed
    passed = db.scalars(select(m.ProjectAlert).where(m.ProjectAlert.rule_code == "CLOSING_DATE_PASSED")).all()
    assert passed and all(not a.is_active for a in passed)


def test_institution_threshold_override(loaded):
    db = loaded
    org = m.Organization(name="TEST ministry", is_tenant=True)
    db.add(org)
    db.flush()
    db.add(m.AlertThreshold(organization_id=org.id, rule_code="LOW_DISBURSEMENT", parameter="max_disbursement_ratio", value=Decimal("0.05")))
    db.commit()
    from app.performance.alerts import thresholds

    assert thresholds(db, org.id)[("LOW_DISBURSEMENT", "max_disbursement_ratio")] == Decimal("0.05")
    assert thresholds(db)[("LOW_DISBURSEMENT", "max_disbursement_ratio")] == Decimal("0.30")


def test_rescue_plan_is_evidence_based(loaded):
    db = loaded
    run_alerts(db, today=date(2026, 6, 1))
    p = db.scalar(select(m.Project).join(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "P900001"))
    plan = create_plan(db, p, None, None)
    db.commit()
    assert plan.actions
    for a in plan.actions:
        assert a.evidence and all(e["alert_id"].startswith("ALR-") and e["observed"] for e in a.evidence)
        assert a.contributing_factors == FURTHER  # no documented causes -> never invented
        assert a.estimated_timeframe is None and a.indicative_budget is None
        assert a.responsible_institution == "SYNTHETIC Ministry of Energy"
        assert a.approval_status == "proposed"
    action = plan.actions[0]
    try:
        update_progress(db, action, "in_progress", "x")
        raise AssertionError("unapproved actions must not progress")
    except ValueError:
        pass
    decide_action(db, action, "approved", user_id=None, changes={"estimated_timeframe": "3 months"})
    assert action.approval_status == "modified" and action.estimated_timeframe == "3 months"
    update_progress(db, action, "done", "Meeting held")
    assert action.implementation_status == "done" and "Meeting held" in action.progress_note


def test_rescue_without_alerts_says_further_investigation(db):
    p = m.Project(ap2i_id="AP2I-CMR-OTHER-999999", country_id=db.scalar(select(m.Country.id).where(m.Country.iso3 == "CMR")),
                  title="SYNTHETIC quiet project", status="active")
    db.add(p)
    db.commit()
    plan = create_plan(db, p, None, None)
    assert plan.actions == [] and FURTHER in plan.diagnosis["summary"]
