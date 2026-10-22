from datetime import date

from conftest import make_user, token_for
from sqlalchemy import select

import app.models as m


def test_health_and_openapi(client):
    assert client.get("/api/v1/health").json()["status"] == "ok"
    spec = client.get("/openapi.json").json()
    assert "/api/v1/projects" in spec["paths"] and "/api/v1/assistant/ask" in spec["paths"]


def test_security_headers(client):
    r = client.get("/api/v1/health")
    assert r.headers["x-content-type-options"] == "nosniff" and r.headers["x-frame-options"] == "DENY"
    assert "default-src 'none'" in r.headers["content-security-policy"]


def test_countries_and_map_show_coverage_separately(loaded, client):
    cs = client.get("/api/v1/countries").json()
    assert len(cs) == 54
    cmr = next(c for c in cs if c["iso3"] == "CMR")
    sen = next(c for c in cs if c["iso3"] == "SEN")
    assert cmr["documented_projects"] > 0 and cmr["is_active"]
    assert sen["documented_projects"] == 0 and sen["data_coverage"] == "no_project_data"
    ov = {c["iso3"]: c for c in client.get("/api/v1/africa/overview").json()["countries"]}
    assert ov["SEN"]["documented_projects"] is None and ov["SEN"]["commitments_usd"] is None  # never fabricated zeros
    assert ov["CMR"]["documented_projects"] >= 4


def test_project_registry_search_and_detail(loaded, client):
    r = client.get("/api/v1/projects", params={"country": "CMR", "q": "electrification"}).json()
    assert r["total"] == 1
    item = r["items"][0]
    assert item["committed_by_currency"] == {"USD": "150000000.0000"}  # original 100M + additional financing 50M
    d = client.get(f"/api/v1/projects/{item['ap2i_id']}").json()
    assert {a["source_identifier"] for a in d["agreements"]} >= {"P900001", "P900002"}
    assert d["sources"] and all(s["url"] for s in d["sources"])
    assert d["financials"]["indicators"]
    assert d["observations"] is None  # field-level provenance requires a detailed plan
    assert client.get("/api/v1/projects/AP2I-CMR-NOPE-000000").status_code == 404
    r2 = client.get("/api/v1/projects", params={"partner": "AFD"}).json()
    assert r2["total"] == 1


def test_detail_with_professional_plan_shows_observations(loaded, client, db):
    make_user(db, "pro@example.org", ["professional_subscriber"], plan="professional")
    h = token_for(client, "pro@example.org")
    pid = client.get("/api/v1/projects", params={"q": "electrification"}).json()["items"][0]["ap2i_id"]
    d = client.get(f"/api/v1/projects/{pid}", headers=h).json()
    assert d["observations"] and all("source_record_id" in o for o in d["observations"])
    src = d["sources"][0]["record_id"]
    assert client.get(f"/api/v1/sources/{src}", headers=h).json()["payload"]


def test_portfolio_and_dashboards(loaded, client):
    pf = client.get("/api/v1/countries/CMR/portfolio", params={"year_from": 2011, "year_to": 2026}).json()
    assert len(pf["years"]) == 16 and "NOT the complete" in pf["coverage_note"]
    dash = client.get("/api/v1/countries/CMR/dashboard").json()
    assert dash["documented_projects"] >= 4 and "data_gaps" in dash
    sec = client.get("/api/v1/sectors/ENERGY/summary", params={"country": "CMR"}).json()
    assert sec["projects"] == 1 and len(sec["indicators"]) == 6
    fin = client.get("/api/v1/financing/summary", params={"country": "CMR"}).json()
    assert "USD" in fin["totals_by_currency"] and "EUR" in fin["totals_by_currency"]
    assert client.get("/api/v1/countries/CMR/portfolio", params={"year_from": 2020, "year_to": 2000}).status_code == 422


def test_alerts_endpoint_and_review(loaded, client, db):
    from app.performance.alerts import run_alerts

    run_alerts(db, today=date(2026, 6, 1))
    r = client.get("/api/v1/alerts", params={"country": "CMR"}).json()
    assert r["total"] > 0 and "not indicate fraud" in r["disclaimer"]
    make_user(db, "rev2@example.org", ["data_reviewer"])
    h = token_for(client, "rev2@example.org")
    aid = r["items"][0]["id"]
    assert client.post(f"/api/v1/admin/alerts/{aid}/review", headers=h, json={"review_status": "acknowledged"}).status_code == 200
    assert client.get("/api/v1/alerts/rules").json()


def test_csv_export(loaded, client, db):
    make_user(db, "exp@example.org", ["registered_user"])
    h = token_for(client, "exp@example.org")
    assert client.get("/api/v1/projects/export.csv").status_code == 401
    r = client.get("/api/v1/projects/export.csv", headers=h, params={"country": "CMR"})
    assert r.status_code == 200 and "ap2i_id" in r.text and "P900001" in r.text and "source_url" in r.text


def test_explorer_and_methodology(loaded, client):
    t = client.get("/api/v1/explorer/transactions", params={"flow": "disbursement", "country": "CMR"}).json()
    assert t["total"] >= 4 and all(i["source_record_id"] for i in t["items"])
    meth = client.get("/api/v1/methodology").json()
    assert "annual" in meth["portfolio"].lower()


def test_admin_review_merge_and_reverse(loaded, client, db):
    from app.ingestion.resolution import generate_candidates

    make_user(db, "rv@example.org", ["data_reviewer"])
    h = token_for(client, "rv@example.org")
    a = db.scalar(select(m.Project).join(m.ProjectIdentifier).where(m.ProjectIdentifier.identifier == "P900001"))
    cid = a.country_id
    b = m.Project(ap2i_id="AP2I-CMR-ENERGY-990009", country_id=cid, title="SYNTHETIC Rural Electrification Project phase", status="active",
                  original_approval_date=date(2018, 4, 1))
    db.add(b)
    db.flush()
    db.add(m.FinancingAgreement(project_id=b.id, partner_id=db.scalar(select(m.FinancingPartner.id).where(m.FinancingPartner.code == "AFDB")),
                                source_identifier="TEST-AFDB-1"))
    db.commit()
    generate_candidates(db, [b.id])
    db.commit()
    cands = client.get("/api/v1/admin/matches", headers=h).json()
    assert cands
    r = client.post(f"/api/v1/admin/matches/{cands[0]['id']}", headers=h, json={"decision": "accept", "survivor": "a"}).json()
    assert r["status"] == "accepted" and r["merge_id"]
    assert client.post(f"/api/v1/admin/merges/{r['merge_id']}/reverse", headers=h).status_code == 200
    db.expire_all()
    assert db.get(m.Project, b.id).merged_into_id is None


def test_admin_manual_sync_endpoint_logs_failure(client, db, monkeypatch):
    import httpx

    from app.connectors import worldbank

    make_user(db, "root2@example.org", ["ap2i_super_admin"])
    h = token_for(client, "root2@example.org")
    real = worldbank.WorldBankProjectsConnector.__init__

    def fake_init(self, config=None, client=None):
        real(self, config, client=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(403))))
        self.min_interval_seconds = 0

    monkeypatch.setattr(worldbank.WorldBankProjectsConnector, "__init__", fake_init)
    r = client.post("/api/v1/admin/connectors/worldbank_projects/sync", headers=h).json()
    assert r["status"] == "failed"
    runs = client.get("/api/v1/admin/sync-runs", headers=h).json()
    assert runs[0]["status"] == "failed"
