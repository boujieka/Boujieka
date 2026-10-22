from conftest import make_user, token_for
from sqlalchemy import select

import app.models as m


def _private_project(db, org_id):
    cid = db.scalar(select(m.Country.id).where(m.Country.iso3 == "CMR"))
    p = m.Project(ap2i_id="AP2I-CMR-HEALTH-990001", country_id=cid, title="SYNTHETIC confidential hospital", status="active", tenant_id=org_id)
    db.add(p)
    db.commit()
    return p


def test_tenant_isolation(client, db):
    org_a = m.Organization(name="TEST Ministry A", is_tenant=True)
    org_b = m.Organization(name="TEST DFI B", is_tenant=True)
    db.add_all([org_a, org_b])
    db.commit()
    p = _private_project(db, org_a.id)
    make_user(db, "a@example.org", ["government_analyst"], org_a.id, plan="institutional")
    make_user(db, "b@example.org", ["dfi_analyst"], org_b.id, plan="institutional")
    ha, hb = token_for(client, "a@example.org"), token_for(client, "b@example.org")
    assert client.get(f"/api/v1/projects/{p.ap2i_id}", headers=ha).status_code == 200
    assert client.get(f"/api/v1/projects/{p.ap2i_id}", headers=hb).status_code == 404
    assert client.get(f"/api/v1/projects/{p.ap2i_id}").status_code == 404
    titles_b = [x["title"] for x in client.get("/api/v1/projects", headers=hb).json()["items"]]
    assert "SYNTHETIC confidential hospital" not in titles_b
    titles_a = [x["title"] for x in client.get("/api/v1/projects", headers=ha).json()["items"]]
    assert "SYNTHETIC confidential hospital" in titles_a
    # Public map never counts private records
    cmr = next(c for c in client.get("/api/v1/africa/overview").json()["countries"] if c["iso3"] == "CMR")
    assert cmr["documented_projects"] is None


def test_role_based_authorization(client, db):
    make_user(db, "reg@example.org", ["registered_user"])
    make_user(db, "rev@example.org", ["data_reviewer"])
    make_user(db, "root@example.org", ["ap2i_super_admin"])
    hr, hv, hs = token_for(client, "reg@example.org"), token_for(client, "rev@example.org"), token_for(client, "root@example.org")
    assert client.get("/api/v1/admin/connectors", headers=hr).status_code == 403
    assert client.get("/api/v1/admin/connectors", headers=hv).status_code == 200
    assert client.patch("/api/v1/admin/connectors/worldbank_projects", headers=hv, json={"enabled": False}).status_code == 403
    assert client.patch("/api/v1/admin/connectors/worldbank_projects", headers=hs, json={"enabled": False}).status_code == 200
    assert client.patch("/api/v1/admin/connectors/kfw", headers=hs, json={"enabled": True}).status_code == 409
    assert client.patch("/api/v1/admin/connectors/worldbank_projects", headers=hs, json={"schedule_cron": "bad"}).status_code == 422
    assert client.get("/api/v1/admin/audit-logs", headers=hs).status_code == 200
    assert client.get("/api/v1/rescue/plans", headers=hr).status_code == 403  # plan feature required


def test_feature_gating_and_payments_not_active(client, db):
    make_user(db, "pay@example.org", ["registered_user"])
    h = token_for(client, "pay@example.org")
    r = client.post("/api/v1/billing/checkout", headers=h, json={"plan": "professional"})
    assert r.status_code == 402 and "not activated" in r.json()["detail"]["message"]
    assert client.get("/api/v1/saved-searches", headers=h).status_code == 403
    assert client.post("/api/v1/auth/api-keys", headers=h, json={"name": "x"}).status_code == 403


def test_enterprise_api_key(client, db):
    make_user(db, "ent@example.org", ["professional_subscriber"], plan="enterprise")
    h = token_for(client, "ent@example.org")
    key = client.post("/api/v1/auth/api-keys", headers=h, json={"name": "ci"}).json()["key"]
    assert client.get("/api/v1/auth/me", headers={"X-API-Key": key}).status_code == 200
    assert client.get("/api/v1/auth/me", headers={"X-API-Key": key + "x"}).status_code == 401
