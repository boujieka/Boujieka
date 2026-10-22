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


def synthetic_isr_pdf() -> bytes:
    """A 2-page PDF laid out like a post-2024 ISR results table (coordinates taken from a real report)."""
    import pymupdf

    doc = pymupdf.open()

    def put(page, x, y, text, bold=False, size=11):
        page.insert_text((x, y + 10), text, fontsize=size, fontname="hebo" if bold else "helv")

    def header(page, y):
        for x, t in ((235, "Baseline"), (360, "Actual (Previous)"), (507, "Actual (Current)"), (656, "Closing Period")):
            put(page, x, y, t)
        put(page, 74, y + 10, "Indicator Name")
        for x, t in ((208, "Value"), (266, "Month/Year"), (353, "Value"), (427, "Date"), (498, "Value"), (572, "Date"),
                     (643, "Value"), (700, "Month/Year")):
            put(page, x, y + 17, t)

    p = doc.new_page(width=792, height=612)
    put(p, 87, 40, "SYNTHETIC Project (P900002)", size=10)
    put(p, 43, 140, "SYNTHETIC Component 1", bold=True)
    header(p, 160)
    # row 1: previous and current cells empty
    for x, t in ((187, "0.00"), (273, "Jun/2020"), (621, "26,000.00"), (706, "Sep/2027")):
        put(p, x, 214, t)
    put(p, 194, 233, "Comments on")
    put(p, 339, 233, "SYNTHETIC comment with 212 hectares")
    put(p, 42, 254, "SYNTHETIC direct beneficiaries")
    put(p, 42, 269, "(Number)")
    # row 2: all cells; name on the same line as the values
    put(p, 42, 324, "SYNTHETIC area irrigated")
    for x, t in ((187, "1,000.00"), (273, "Jun/2020"), (332, "0.00"), (410, "05-Apr-2024"), (477, "120.50"),
                 (555, "06-Dec-2024"), (621, "14,000.00"), (706, "Sep/2027")):
        put(p, x, 324, t)
    put(p, 42, 339, "(Hectare(Ha))")
    # row 3: a value in a date column -> the row is rejected, not shifted
    for x, t in ((187, "5.00"), (410, "7.00"), (621, "9.00")):
        put(p, x, 400, t)
    put(p, 42, 415, "SYNTHETIC misaligned row (Number)")
    # row 4: current actual dated after the report; name continues on the next page
    for x, t in ((187, "0.00"), (273, "Jun/2020"), (477, "3"), (555, "06-Dec-2025"), (621, "8.00"), (706, "Sep/2027")):
        put(p, x, 522, t)
    put(p, 22, 551, "Mar 04, 2025   Page 1 of 2", size=8)
    p2 = doc.new_page(width=792, height=612)
    put(p2, 87, 40, "SYNTHETIC Project (P900002)", size=10)
    put(p2, 68, 89, "SYNTHETIC stations installed (Number)")
    put(p2, 194, 120, "Comments on")
    for x, t in ((187, "2.00"), (273, "Jun/2020"), (621, "4.00"), (706, "Sep/2027")):
        put(p2, x, 300, t)
    put(p2, 42, 315, "SYNTHETIC long name")
    put(p2, 22, 551, "Mar 04, 2025   Page 2 of 3", size=8)
    p3 = doc.new_page(width=792, height=612)
    put(p3, 87, 40, "SYNTHETIC Project (P900002)", size=10)
    put(p3, 42, 89, "to the next page (Number)")
    out = doc.tobytes()
    doc.close()
    return out


def test_parse_isr_pdf_results():
    from app.connectors.wb_documents import parse_isr_pdf_results

    r = parse_isr_pdf_results(synthetic_isr_pdf())
    by = {i["name"]: i for i in r}
    assert set(by) == {"SYNTHETIC direct beneficiaries", "SYNTHETIC area irrigated", "SYNTHETIC stations installed",
                       "SYNTHETIC long name to the next page"}
    a = by["SYNTHETIC direct beneficiaries"]
    assert (a["unit"], a["baseline"], a["previous"], a["current"], a["target"]) == ("Number", "0.00", None, None, "26,000.00")
    assert a["baseline_date"] is None and a["baseline_period"] == "Jun/2020"  # no day invented
    b = by["SYNTHETIC area irrigated"]
    assert b["unit"] == "Hectare(Ha)" and (b["previous"], b["current"]) == ("0.00", "120.50")
    assert b["previous_date"] == date(2024, 4, 5) and b["current_date"] == date(2024, 12, 6)
    c = by["SYNTHETIC stations installed"]  # name read across the page break, without the running header
    assert c["current"] == "3" and c["current_date"] == date(2025, 12, 6)


def test_isr_pdf_table_is_read_when_text_has_no_values(loaded):
    import json

    db = loaded
    wds = {"documents": {"D1": {"id": "90000011", "docty": "Implementation Status and Results Report",
                                "docdt": "2025-03-04T00:00:00Z", "display_title": "SYNTHETIC ISR 2025", "lang": "English",
                                "pdfurl": "https://documents.example.test/isr2025.pdf",
                                "txturl": "https://documents.example.test/isr2025.txt"}}}
    text = b"Implementation Status & Results Report\nSeq No: 9\nIndicator Name\nSYNTHETIC direct beneficiaries\n"
    c = WorldBankDocumentsConnector(client=mock_client({
        "https://search.worldbank.org/api/v2/wds": (200, json.dumps(wds).encode(), "application/json"),
        "https://documents.example.test/isr2025.txt": (200, text, "text/plain"),
        "https://documents.example.test/isr2025.pdf": (200, synthetic_isr_pdf(), "application/pdf"),
    }))
    c.min_interval_seconds = 0
    run = run_sync(db, "worldbank_documents", connector=c, force=True)
    assert run.status == "success", str(run.errors)[:1500]
    p = db.scalar(select(m.Project).join(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "P900001"))
    ri = db.scalar(select(m.ResultsIndicator).where(m.ResultsIndicator.project_id == p.id,
                                                    m.ResultsIndicator.name == "SYNTHETIC area irrigated"))
    assert ri.baseline_value == Decimal("1000.00") and ri.target_value == Decimal("14000.00")
    vals = {o.period_end: o.value for o in db.scalars(select(m.ResultsObservation).where(m.ResultsObservation.indicator_id == ri.id))}
    assert vals == {date(2024, 4, 5): Decimal("0.00"), date(2024, 12, 6): Decimal("120.50")}
    st = db.scalar(select(m.ResultsIndicator).where(m.ResultsIndicator.project_id == p.id,
                                                    m.ResultsIndicator.name == "SYNTHETIC stations installed"))
    assert not db.scalars(select(m.ResultsObservation).where(m.ResultsObservation.indicator_id == st.id)).all()
    # (the mocked WDS returns this document for every project, so validations are checked without a project filter)
    msgs = dict(db.execute(select(m.DataValidation.rule, m.DataValidation.message)).all())
    assert "days after the report date 2025-03-04" in msgs["result_date_after_report"]
    assert "read from the PDF by word position (4 indicators" in msgs["document_partially_extracted"]
    cache = db.scalar(select(m.SourceObservation).where(m.SourceObservation.field == "isr_pdf_results"))
    assert cache is not None and cache.source_field.startswith("PDF results table, sha256 ")
    # second run: the PDF is not downloaded again
    c2 = WorldBankDocumentsConnector(client=mock_client({
        "https://search.worldbank.org/api/v2/wds": (200, json.dumps(wds).encode(), "application/json")}))
    c2.min_interval_seconds = 0
    run2 = run_sync(db, "worldbank_documents", connector=c2, force=True)
    assert run2.status == "success" and run2.records_failed == 0
    msgs = dict(db.execute(select(m.DataValidation.rule, m.DataValidation.message)).all())
    assert "read from the PDF by word position" in msgs["document_partially_extracted"]
    assert db.scalar(select(m.ResultsIndicator).where(m.ResultsIndicator.name == "SYNTHETIC area irrigated")) is not None
