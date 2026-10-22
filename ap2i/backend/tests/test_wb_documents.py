from datetime import date
from decimal import Decimal

from conftest import FIXTURES, make_user, mock_client, token_for
from sqlalchemy import select

import app.models as m
from app.connectors.wb_documents import ICRR, WorldBankDocumentsConnector, parse_icr, parse_isr
from app.ingestion.pipeline import run_sync


def docs_connector():
    c = WorldBankDocumentsConnector(client=mock_client({
        "https://search.worldbank.org/api/v2/wds": (200, (FIXTURES / "wds_synthetic.json").read_bytes(), "application/json"),
        "https://documents.example.test/isr.txt": (200, (FIXTURES / "isr_synthetic.txt").read_bytes(), "text/plain"),
        "https://documents.example.test/icrr.txt": (200, (FIXTURES / "icrr_synthetic.txt").read_bytes(), "text/plain"),
    }))
    c.min_interval_seconds = 0
    return c


def test_parse_isr_synthetic():
    r = parse_isr((FIXTURES / "isr_synthetic.txt").read_text())
    assert r.sequence == "7"
    assert r.ratings["ip"] == {"previous": "Moderately Satisfactory", "current": "Moderately Unsatisfactory"}
    assert r.original_closing == date(2023, 12, 31) and r.revised_closing == date(2025, 12, 31)
    assert r.loans[0]["currency"] == "XDR" and r.loans[0]["pct_disbursed"] == Decimal("30")
    ind = r.indicators[0]
    assert ind["unit"] == "Number" and ind["current"] == "20,000.00" and ind["current_date"] == date(2024, 5, 31)
    assert r.progress_candidates[0]["value"] == Decimal("65")


def test_parse_icr_review():
    r = parse_icr((FIXTURES / "icrr_synthetic.txt").read_text(), ICRR)
    assert r.ratings["outcome"] == {"icr": "Satisfactory", "ieg": "Moderately Satisfactory"}


def test_documents_sync_persists_and_never_infers_progress(loaded, client):
    from app.performance.alerts import run_alerts

    db = loaded
    run = run_sync(db, "worldbank_documents", connector=docs_connector(), force=True)
    assert run.status == "success", str(run.errors)[:1500]
    p = db.scalar(select(m.Project).join(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "P900001"))
    docs = db.scalars(select(m.Document).where(m.Document.project_id == p.id, m.Document.doc_type.is_not(None))).all()
    assert {d.doc_type for d in docs} >= {"Implementation Status and Results Report", "Project Appraisal Document"}
    isr_doc = next(d for d in docs if d.doc_type.startswith("Implementation Status"))
    assert isr_doc.extracted_text and "ignore_previous" in isr_doc.injection_flags
    prog = db.scalar(select(m.ImplementationProgress).where(m.ImplementationProgress.project_id == p.id,
                                                            m.ImplementationProgress.document_id == isr_doc.id))
    assert prog.rating == "PDO=Moderately Satisfactory|IP=Moderately Unsatisfactory|Risk=High"
    assert prog.financial_progress_pct == Decimal("30") and prog.physical_progress_pct is None
    assert p.original_completion_date == date(2023, 12, 31) and p.revised_completion_date == date(2025, 12, 31)
    assert p.physical_progress_pct is None  # the 65% in the narrative is only a candidate
    obs = db.scalars(select(m.ResultsObservation).join(m.ResultsIndicator).where(m.ResultsIndicator.project_id == p.id,
                                                                                 m.ResultsObservation.period_end == date(2024, 5, 31))).all()
    assert any(o.value == Decimal("20000.00") for o in obs)
    assert "ICR Review" in (p.development_results or "")
    run_alerts(db, today=date(2024, 7, 1))
    rules = set(db.scalars(select(m.ProjectAlert.rule_code).where(m.ProjectAlert.project_id == p.id, m.ProjectAlert.is_active.is_(True))))
    assert "UNSATISFACTORY_RATING" in rules
    # reviewer confirms the candidate -> becomes physical progress (verified)
    make_user(db, "revdoc@example.org", ["data_reviewer"])
    h = token_for(client, "revdoc@example.org")
    cands = client.get("/api/v1/admin/progress-candidates", headers=h).json()
    assert cands and cands[0]["value_numeric"] == "65.0000"
    r = client.post(f"/api/v1/admin/progress-candidates/{cands[0]['id']}", headers=h, json={"decision": "accept"}).json()
    assert r["verification_status"] == "verified" and Decimal(r["project_physical_progress_pct"]) == 65
    # idempotent re-run: no new documents parsed
    run2 = run_sync(db, "worldbank_documents", connector=docs_connector(), force=True)
    assert run2.records_imported == 0 and run2.records_new == 0


def test_layout_variants():
    pad = " " * 25
    columnar = "\n".join([
        pad + "Indicator Name                                    Core Unit of Measure                      Baseline                         Current                          End Target",
        pad + "SYNTHETIC rural communities with                          Number               Value        0.00                             88448.00                         50000.00",
        pad + "land management plans                                                          Date         01-Mar-2008                      01-Mar-2012                      01-Mar-2012",
        pad + "SYNTHETIC people with water access                        Text                 Value        0                                                                 50000",
        pad + "                                                                               Date         04-Oct-2004                      19-May-2010                      30-Nov-2009",
    ])
    r = parse_isr(columnar)
    assert len(r.indicators) == 2
    a, b = r.indicators
    assert a["name"].startswith("SYNTHETIC rural communities with land management plans")
    assert (a["baseline"], a["current"], a["target"]) == ("0.00", "88448.00", "50000.00")
    assert b["current"] is None and b["target"] == "50000"  # an empty cell is not shifted
    ctl = " Progress towards achievement of PDO          \u0080Moderately Satisfactory        \u0080Moderately Unsatisfactory\r\n"
    assert parse_isr(ctl).ratings["pdo"]["current"] == "Moderately Unsatisfactory"
    icr = "KEY RATINGS\n\n     Outcome                                         Bank Performance                           M&E Quality\n" \
          "    Satisfactory                                     Satisfactory                               Substantial\n"
    from app.connectors.wb_documents import ICR

    assert parse_icr(icr, ICR).ratings == {"outcome": {"icr": "Satisfactory"}, "bank_performance": {"icr": "Satisfactory"},
                                           "me_quality": {"icr": "Substantial"}}
