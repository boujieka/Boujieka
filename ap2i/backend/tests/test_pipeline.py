from decimal import Decimal

from conftest import iati_connector, wb_connector
from sqlalchemy import func, select

import app.models as m
from app.ingestion.pipeline import run_sync


def test_ingestion_persists_with_provenance(loaded):
    db = loaded
    p = db.scalar(select(m.Project).join(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "P900001"))
    assert p.ap2i_id.startswith("AP2I-CMR-ENERGY-")
    links = db.scalars(select(m.ProjectSourceLink).where(m.ProjectSourceLink.project_id == p.id)).all()
    assert {lk.link_type for lk in links} >= {"primary", "deterministic_match"}
    for lk in links:
        sr = db.get(m.SourceRecord, lk.source_record_id)
        assert sr.payload_sha256 and sr.retrieved_at and sr.source_url
    obs = db.scalars(select(m.SourceObservation).where(m.SourceObservation.project_id == p.id)).all()
    assert any(o.field == "original_approval_date" for o in obs)


def test_additional_financing_attaches_to_parent_project(loaded):
    db = loaded
    p = db.scalar(select(m.Project).join(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "P900001"))
    ids = {a.source_identifier for a in p.agreements}
    assert {"P900001", "P900002"} <= ids
    assert db.scalar(select(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "P900002")).project_id == p.id


def test_world_bank_iati_does_not_double_count(loaded):
    db = loaded
    agr = db.scalar(select(m.FinancingAgreement).where(m.FinancingAgreement.source_identifier == "P900001"))
    assert db.scalar(select(func.count(m.FinancingAgreement.id)).where(
        m.FinancingAgreement.source_identifier.in_(("P900001", "44000-P900001")))) == 1
    counted = db.scalars(select(m.FinancingCommitment).where(m.FinancingCommitment.agreement_id == agr.id,
                                                             m.FinancingCommitment.is_counted.is_(True))).all()
    assert sum(c.amount for c in counted) == Decimal("100000000")
    assert len(db.scalars(select(m.FinancingCommitment).where(m.FinancingCommitment.agreement_id == agr.id)).all()) == 2


def test_afd_parent_child_single_project(loaded):
    db = loaded
    parent = db.scalar(select(m.Project).join(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "TEST-FR-3-CCM0001"))
    child_owner = db.scalar(select(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "TEST-FR-3-CCM000101"))
    assert child_owner.project_id == parent.id
    agrs = db.scalars(select(m.FinancingAgreement).where(m.FinancingAgreement.project_id == parent.id)).all()
    assert [a.source_identifier for a in agrs] == ["TEST-FR-3-CCM000101"]
    assert parent.region is not None and parent.region.code == "CM-NO"  # "Garoua, Nord"


def test_resync_is_idempotent(loaded):
    db = loaded
    before = (db.scalar(select(func.count(m.Project.id))), db.scalar(select(func.count(m.Disbursement.id))),
              db.scalar(select(func.count(m.SourceRecord.id))))
    run = run_sync(db, "iati_generic", connector=iati_connector(), force=True)
    run2 = run_sync(db, "worldbank_projects", connector=wb_connector(), force=True)
    after = (db.scalar(select(func.count(m.Project.id))), db.scalar(select(func.count(m.Disbursement.id))),
             db.scalar(select(func.count(m.SourceRecord.id))))
    assert before == after
    assert run.records_unchanged == 4 and run2.records_unchanged == 3


def test_changed_record_creates_new_version_and_keeps_old(loaded):
    import json

    from conftest import FIXTURES, mock_client

    from app.connectors.worldbank import WorldBankProjectsConnector

    db = loaded
    data = json.loads((FIXTURES / "wb_projects_synthetic.json").read_text())
    data["projects"]["P900001"]["disbursement"] = ["20.00"]
    data["projects"]["P900001"]["available"] = ["80.00"]
    c = WorldBankProjectsConnector(client=mock_client({"https://search.worldbank.org": (200, json.dumps(data).encode(), "application/json")}))
    c.min_interval_seconds = 0
    run_sync(db, "worldbank_projects", connector=c, force=True)
    versions = db.scalars(select(m.SourceRecord).join(m.SourceConnector).where(
        m.SourceConnector.key == "worldbank_projects", m.SourceRecord.source_identifier == "P900001")).all()
    assert len(versions) == 2 and sum(v.is_latest for v in versions) == 1
    agr = db.scalar(select(m.FinancingAgreement).where(m.FinancingAgreement.source_identifier == "P900001"))
    assert agr.reported_cumulative_disbursed == Decimal("20000000")


def test_failed_sync_is_logged(db):
    import httpx

    from app.connectors.worldbank import WorldBankProjectsConnector

    c = WorldBankProjectsConnector(client=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(403))))
    c.min_interval_seconds = 0
    run = run_sync(db, "worldbank_projects", connector=c, force=True)
    conn = db.scalar(select(m.SourceConnector).where(m.SourceConnector.key == "worldbank_projects"))
    assert run.status == "failed" and "failed" in run.log
    assert conn.last_failure_at is not None and conn.last_error and conn.status != "operational"
    assert db.scalar(select(func.count(m.Notification.id)).where(m.Notification.kind == "sync_failed")) == 1


def test_connector_marked_operational_only_after_persisting_records(loaded):
    conn = loaded.scalar(select(m.SourceConnector).where(m.SourceConnector.key == "worldbank_projects"))
    assert conn.status == "operational" and "records" in conn.status_evidence


def test_prompt_injection_text_is_flagged_not_obeyed(loaded):
    db = loaded
    v = db.scalars(select(m.DataValidation).where(m.DataValidation.rule == "prompt_injection_pattern")).all()
    assert v and "ignore_previous" in v[0].message


def test_missing_values_stay_null(loaded):
    p = loaded.scalar(select(m.Project).join(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "P900003"))
    assert p.status == "dropped" and p.original_estimated_cost is None and p.physical_progress_pct is None
    agr = p.agreements[0]
    assert agr.amount_original is None and agr.reported_cumulative_disbursed is None


def test_corrections_clear_future_actual_dates(db):
    from datetime import date

    from app.ingestion.corrections import apply_corrections

    cid = db.scalar(select(m.Country.id).where(m.Country.iso3 == "CMR"))
    p = m.Project(ap2i_id="AP2I-CMR-OTHER-990100", country_id=cid, title="SYNTHETIC", status="active",
                  actual_completion_date=date(2030, 6, 30))
    db.add(p)
    db.commit()
    out = apply_corrections(db, today=date(2026, 1, 1))
    assert out["future_actual_dates_cleared"] == 1
    db.refresh(p)
    assert p.actual_completion_date is None and p.original_completion_date == date(2030, 6, 30)
    assert db.scalar(select(m.DataValidation).where(m.DataValidation.rule == "future_actual_date"))
    ind = m.ResultsIndicator(project_id=p.id, name="SYNTHETIC indicator")
    db.add(ind)
    db.flush()
    obs = m.ResultsObservation(indicator_id=ind.id, value=5, period_end=date(2029, 6, 29))
    db.add(obs)
    db.commit()
    out = apply_corrections(db, today=date(2026, 1, 1))
    db.refresh(obs)
    assert out["future_result_dates_cleared"] == 1 and obs.period_end is None and obs.value == 5


def test_corrections_identical_repeats_and_eu_decision(db):
    from datetime import date
    from decimal import Decimal

    from app.finance.indicators import agreement_position
    from app.ingestion.corrections import apply_corrections

    cid = db.scalar(select(m.Country.id).where(m.Country.iso3 == "CMR"))
    p = m.Project(ap2i_id="AP2I-CMR-OTHER-990200", country_id=cid, title="SYNTHETIC", status="active")
    q = m.Project(ap2i_id="AP2I-CMR-OTHER-990201", country_id=cid, title="SYNTHETIC EU", status="active")
    db.add_all([p, q])
    db.flush()
    loan = m.FinancingAgreement(project_id=p.id, source_identifier="SYN-LOAN", currency="EUR", amount_original=Decimal(50))
    dec = m.FinancingAgreement(project_id=q.id, source_identifier="XI-IATI-EC_INTPA-2016-ACT-D-1", currency="EUR", amount_original=Decimal(30))
    con = m.FinancingAgreement(project_id=q.id, source_identifier="XI-IATI-EC_INTPA-2016-PCC-1", currency="EUR", amount_original=Decimal(30))
    db.add_all([loan, dec, con])
    db.flush()
    for i in range(3):  # the same commitment published three times (the importer labels repeats "additional")
        db.add(m.FinancingCommitment(agreement_id=loan.id, commitment_type="original" if i == 0 else "additional", amount=Decimal(50), currency="EUR",
                                     value_date=date(2018, 11, 8), transaction_key=f"k{i}"))
    db.add(m.Disbursement(agreement_id=loan.id, amount=Decimal(5), currency="EUR", value_date=date(2019, 1, 1), transaction_key="d1"))
    db.add(m.Disbursement(agreement_id=loan.id, amount=Decimal(5), currency="EUR", value_date=date(2019, 2, 1), transaction_key="d2"))
    for a in (dec, con):
        db.add(m.FinancingCommitment(agreement_id=a.id, commitment_type="original", amount=Decimal(30), currency="EUR",
                                     value_date=date(2016, 5, 1), transaction_key="c"))
    db.commit()
    out = apply_corrections(db, today=date(2026, 1, 1))
    assert out["duplicate_commitments_not_counted"] == 2 and out["duplicate_flows_not_counted"] == 0
    assert out["eu_decision_commitments_not_counted"] == 1
    assert agreement_position(db, loan).committed == Decimal(50)
    assert agreement_position(db, dec).committed is None  # the envelope does not come back through amount_original
    assert agreement_position(db, con).committed == Decimal(30)
    assert apply_corrections(db, today=date(2026, 1, 1))["duplicate_commitments_not_counted"] == 0  # idempotent
