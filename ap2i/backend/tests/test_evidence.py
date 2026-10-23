from datetime import date
from decimal import Decimal

from sqlalchemy import select

import app.models as m
from app.ingestion.evidence import apply_groups, import_evidence


def _setup(db):
    cid = db.scalar(select(m.Country.id).where(m.Country.iso3 == "CMR"))
    a = m.Project(ap2i_id="AP2I-CMR-ENERGY-990300", country_id=cid, title="SYNTHETIC hydropower plant (guarantee)", status="active")
    b = m.Project(ap2i_id="AP2I-CMR-ENERGY-990301", country_id=cid, title="SYNTHETIC hydropower plant (loan)", status="completed")
    db.add_all([a, b])
    db.flush()
    loan = m.FinancingAgreement(project_id=b.id, source_identifier="SYN-LOAN-1", currency="EUR", amount_original=Decimal(50))
    db.add(loan)
    db.commit()
    return a, b, loan


def rec(**kw):
    base = {"ap2i_id": "AP2I-CMR-ENERGY-990300", "agreement": None, "field": "operational_status", "value": "operational",
            "currency": None, "as_of": "2025-03-01", "source_url": "https://example.org/synthetic-operator-page",
            "source_publisher": "SYNTHETIC operator", "source_type": "operator_official", "published": "2025-03-02",
            "quote": "SYNTHETIC: the plant is in full commercial operation since March 2025.", "retrieved_at": "2026-10-23T08:00:00Z",
            "confidence": "high - operator statement"}
    base.update(kw)
    return base


def test_evidence_applies_official_facts_only(db, client):
    a, b, loan = _setup(db)
    out = import_evidence(db, [
        rec(),
        rec(field="commissioning_date", value="2025-03-01"),
        rec(field="operational_status", value="operational", source_type="press", source_publisher="press: SYNTHETIC news",
            ap2i_id="AP2I-CMR-ENERGY-990301"),
        rec(ap2i_id="AP2I-CMR-ENERGY-990301", field="disbursed_amount", value="50000000", currency="EUR", agreement="SYN-LOAN-1",
            source_type="donor_official", source_publisher="SYNTHETIC bank"),
        rec(field="other", quote=""),  # rejected: no quote
        rec(ap2i_id="AP2I-CMR-ENERGY-000000"),  # rejected: unknown project
    ], today=date(2026, 10, 23))
    db.commit()
    assert (out["stored"], out["rejected"], out["review"]) == (4, 2, 1)
    db.refresh(a), db.refresh(b), db.refresh(loan)
    assert a.operational_status == "operational" and a.commissioning_date == date(2025, 3, 1)
    assert b.operational_status == "unknown"  # press only: stored for review, field unchanged
    assert loan.reported_cumulative_disbursed == Decimal("50000000") and "SYNTHETIC bank" in loan.reported_cumulative_label
    again = import_evidence(db, [rec()], today=date(2026, 10, 23))
    assert again["already_stored"] == 1 and again["stored"] == 0  # idempotent
    db.commit()
    d = client.get("/api/v1/projects/AP2I-CMR-ENERGY-990300").json()
    ev = {e["field"]: e for e in d["documented_evidence"]}
    assert ev["operational_status"]["quote"].startswith("SYNTHETIC") and ev["operational_status"]["source_url"].startswith("https://")


def test_groups_merge_high_confidence_only(db):
    a, b, _ = _setup(db)
    ev = [{"source_url": "https://example.org/cofinancing", "quote": "SYNTHETIC co-financed by A and B"}]
    out = apply_groups(db, [{"group_name": "SYN low", "members": [a.ap2i_id, b.ap2i_id], "lead_member": a.ap2i_id, "evidence": ev,
                             "confidence": "medium"}])
    assert out["merged"] == 0
    out = apply_groups(db, [{"group_name": "SYN plant", "members": [a.ap2i_id, b.ap2i_id], "lead_member": a.ap2i_id, "evidence": ev,
                             "confidence": "high - same asset"}])
    db.commit()
    db.refresh(b)
    assert out["merged"] == 1 and b.merged_into_id == a.id
    assert db.scalar(select(m.FinancingAgreement.project_id).where(m.FinancingAgreement.source_identifier == "SYN-LOAN-1")) == a.id
