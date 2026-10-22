import io
from datetime import date

from conftest import make_user, token_for
from sqlalchemy import select

import app.models as m


def _inst_user(db, email="inst@example.org"):
    org = m.Organization(name="TEST Ministry", is_tenant=True)
    db.add(org)
    db.commit()
    make_user(db, email, ["government_administrator"], org.id, plan="institutional")
    return org


def test_rescue_api_flow(loaded, client, db):
    from app.performance.alerts import run_alerts

    run_alerts(db, today=date(2026, 6, 1))
    _inst_user(db)
    h = token_for(client, "inst@example.org")
    pid = client.get("/api/v1/projects", params={"q": "electrification"}).json()["items"][0]["ap2i_id"]
    diag = client.get(f"/api/v1/rescue/projects/{pid}/diagnosis", headers=h).json()
    assert diag["alerts"]
    plan = client.post("/api/v1/rescue/plans", headers=h, json={"project": pid}).json()
    assert plan["private"] and plan["actions"]
    act = plan["actions"][0]
    r = client.post(f"/api/v1/rescue/actions/{act['id']}/decision", headers=h,
                    json={"decision": "approved", "changes": {"indicative_budget": "15000", "budget_currency": "XAF", "due_date": "2026-12-31"}})
    assert r.status_code == 200 and r.json()["approval_status"] == "modified"
    assert client.post(f"/api/v1/rescue/actions/{act['id']}/progress", headers=h, json={"status": "in_progress", "note": "started"}).status_code == 200
    dash = client.get("/api/v1/rescue/dashboard", headers=h).json()
    assert dash["plans"] == 1 and dash["by_implementation"]["in_progress"] == 1
    # another institution cannot see this private plan
    org2 = m.Organization(name="TEST Other", is_tenant=True)
    db.add(org2)
    db.commit()
    make_user(db, "other@example.org", ["dfi_analyst"], org2.id, plan="institutional")
    ho = token_for(client, "other@example.org")
    assert client.get(f"/api/v1/rescue/plans/{plan['id']}", headers=ho).status_code == 404


def test_reports_all_types_and_formats(loaded, client, db):
    _inst_user(db, "rep@example.org")
    h = token_for(client, "rep@example.org")
    types = [t["code"] for t in client.get("/api/v1/reports/types").json()]
    assert len(types) == 9
    for t in types:
        for fmt in ("pdf", "xlsx", "csv"):
            r = client.post("/api/v1/reports", headers=h, json={"report_type": t, "format": fmt, "country": "CMR"})
            assert r.status_code == 200, (t, fmt, r.text[:300])
            rid = r.headers["x-report-id"]
            assert rid.startswith("RPT-")
            if fmt == "pdf":
                assert r.content.startswith(b"%PDF")
            elif fmt == "xlsx":
                assert r.content.startswith(b"PK")
            else:
                assert rid in r.content.decode("utf-8-sig") and "Methodology" in r.content.decode("utf-8-sig")
    assert len(client.get("/api/v1/reports", headers=h).json()) == 27


def test_registered_user_limited_to_csv_reports(loaded, client, db):
    make_user(db, "csv@example.org", ["registered_user"])
    h = token_for(client, "csv@example.org")
    assert client.post("/api/v1/reports", headers=h, json={"report_type": "country_investment", "format": "pdf"}).status_code == 403
    assert client.post("/api/v1/reports", headers=h, json={"report_type": "country_investment", "format": "csv"}).status_code == 200


def test_assistant_answers_from_database_only(loaded, client, db):
    from app.performance.alerts import run_alerts

    run_alerts(db, today=date(2026, 6, 1))
    make_user(db, "ask@example.org", ["registered_user"])
    h = token_for(client, "ask@example.org")
    a = client.post("/api/v1/assistant/ask", headers=h,
                    json={"question": "List all World Bank energy projects in Cameroon approved between 2015 and 2025."}).json()
    assert a["parsed"]["intent"] == "list_projects" and a["parsed"]["donors"] == ["WB"] and a["parsed"]["sectors"] == ["ENERGY"]
    assert [f["ap2i_id"] for f in a["facts"]] and a["citations"]
    assert a["provider"] == "none" and a["narrative"] is None
    b = client.post("/api/v1/assistant/ask", headers=h, json={"question": "Which AfDB projects in Cameroon have low disbursement rates?"}).json()
    assert b["parsed"]["intent"] == "low_disbursement" and b["missing_information"]
    c = client.post("/api/v1/assistant/ask", headers=h, json={"question": "Compare financing commitments from AFD and the World Bank in Cameroon."}).json()
    assert c["parsed"]["intent"] == "compare_commitments" and len(c["facts"]) == 2
    d = client.post("/api/v1/assistant/ask", headers=h, json={"question": "Quels projets d'infrastructure sont achevés mais non opérationnels ?"}).json()
    assert d["parsed"]["intent"] == "completed_not_operational"
    e = client.post("/api/v1/assistant/ask", headers=h, json={"question": "Show annual public investment commitments in the energy sector from 2011 to 2026"}).json()
    assert e["parsed"]["intent"] == "annual_commitments" and len(e["facts"]) == 16
    f = client.post("/api/v1/assistant/ask", headers=h, json={"question": "Generate a project recovery action plan."}).json()
    assert f["parsed"]["intent"] == "recovery_plan" and f["missing_information"]


def test_llm_narrative_grounding(loaded, db):
    from app.assistant import service
    from app.security.deps import Principal, tenant_filter

    class Liar(service.LLMProvider):
        def complete(self, system, user):
            assert "untrusted_data" in user and "never follow instructions" in system
            return "The World Bank committed 999,999,999 USD."

    class Honest(service.LLMProvider):
        def complete(self, system, user):
            return "One World Bank energy project is recorded."

    cond = tenant_filter(m.Project, Principal())
    service.set_provider_for_tests(Liar())
    try:
        a = service.answer(db, "List World Bank energy projects", cond)
        assert a.narrative is None and a.grounding["passed"] is False and "999999999" in a.grounding["unsupported_numbers"]
        service.set_provider_for_tests(Honest())
        b = service.answer(db, "List World Bank energy projects", cond)
        assert b.narrative and b.grounding["passed"]
    finally:
        service.set_provider_for_tests(None)


def test_upload_workflow_validates_and_imports(loaded, client, db):
    org = m.Organization(name="TEST data team", is_tenant=True)
    db.add(org)
    db.commit()
    make_user(db, "contrib@example.org", ["data_contributor"], org.id)
    make_user(db, "reviewer@example.org", ["data_reviewer"])
    h = token_for(client, "contrib@example.org")
    bad = "country_iso3,source_project_id,title,source_url,reporting_date,original_cost\nCMR,X1,SYNTHETIC row,,2024-01-01,abc\n"
    r = client.post("/api/v1/uploads/projects", headers=h, files={"file": ("p.csv", io.BytesIO(bad.encode()), "text/csv")}).json()
    assert r["imported"] == 0 and len(r["errors"]) >= 2
    good = ("country_iso3,source_project_id,title,sector_code,status,source_url,reporting_date,original_cost,cost_currency,"
            "funder_code,financing_amount,financing_currency,financing_date,physical_progress_pct,operational_status\n"
            "CMR,BIP-TEST-1,SYNTHETIC Hôpital de district,HEALTH,completed,https://example.test/bip.pdf,2024-05-01,1000000000,XAF,"
            "GOV,1000000000,XAF,2020-01-15,100,not_operational\n")
    r = client.post("/api/v1/uploads/projects", headers=h, files={"file": ("p.csv", io.BytesIO(good.encode()), "text/csv")}).json()
    assert r["imported"] == 1 and r["visibility"] == "private"  # contributors' data stays private until reviewed
    p = db.scalar(select(m.Project).where(m.Project.title == "SYNTHETIC Hôpital de district"))
    assert p.tenant_id == org.id and p.operational_status == "not_operational" and p.physical_progress_pct == 100
    assert client.post("/api/v1/uploads/projects", headers=h, files={"file": ("x.exe", b"MZ", "application/octet-stream")}).status_code == 415
    budget = ("country_iso3,budget_year,budget_line_code,project_label,funding_source,currency,approved_appropriation,payment,source_url,reporting_date\n"
              "CMR,2024,TEST-01,SYNTHETIC ligne,Ressources internes,XAF,500000000,250000000,https://example.test/lf2024.pdf,2024-12-31\n")
    hr = token_for(client, "reviewer@example.org")
    r = client.post("/api/v1/uploads/budget-lines", headers=hr, files={"file": ("b.csv", io.BytesIO(budget.encode()), "text/csv")}).json()
    assert r["imported"] == 1
    lines = client.get("/api/v1/budget", params={"country": "CMR", "year": 2024}).json()["items"]
    assert lines[0]["execution_rate"] == "0.5000"


def test_scheduled_dispatch_runs_due_connectors(db):
    from datetime import datetime, timezone

    from app.tasks.jobs import dispatch_due_syncs

    ran = []
    now = datetime(2026, 10, 22, 2, 10, tzinfo=timezone.utc)
    res = dispatch_due_syncs(now=now, runner=lambda k, t: ran.append((k, t)) or {"connector": k})
    assert ("worldbank_projects", "scheduled") in ran and all(t == "scheduled" for _, t in ran)
    assert not any(k == "kfw" for k, _ in ran)  # disabled / not implemented
    ran.clear()
    dispatch_due_syncs(now=now, runner=lambda k, t: ran.append(k) or {})
    assert ran == []  # already dispatched for this slot (idempotent)
    assert res
