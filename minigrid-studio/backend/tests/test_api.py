"""API integration tests against a real PostgreSQL database.

Set MGS_TEST_DATABASE_URL (e.g. postgresql+psycopg://mgs:mgs@127.0.0.1:55432/mgs_test);
the tests drop and recreate the schema of that database with Alembic.
"""
import os
import uuid

import pytest

DB_URL = os.environ.get("MGS_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DB_URL, reason="MGS_TEST_DATABASE_URL not set")

PW = "correct horse battery staple"


@pytest.fixture(scope="module")
def client():
    os.environ["MGS_DATABASE_URL"] = DB_URL
    os.environ["MGS_ALLOW_SIGNUP"] = "true"
    os.environ["MGS_LOGIN_ATTEMPTS_PER_MINUTE"] = "5"
    from app.config import get_settings
    get_settings.cache_clear()
    from sqlalchemy import create_engine, text
    eng = create_engine(DB_URL)
    with eng.begin() as c:
        c.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public"))
    eng.dispose()
    from alembic import command
    from alembic.config import Config
    cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    cfg.set_main_option("script_location", os.path.join(os.path.dirname(__file__), "..", "alembic"))
    command.upgrade(cfg, "head")
    from app.db import reset_engine
    reset_engine()
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app) as c:
        yield c


def _signup(client, org):
    email = f"{uuid.uuid4().hex[:8]}@example.org"
    r = client.post("/api/v1/auth/signup", json={"organization": org, "email": email, "name": "Admin", "password": PW})
    assert r.status_code == 201, r.text
    tok = r.json()["access_token"]
    h = {"Authorization": f"Bearer {tok}"}
    org_id = client.get("/api/v1/auth/me", headers=h).json()["memberships"][0]["org_id"]
    return h, org_id, email


def _member(client, admin_h, org_id, role):
    email = f"{role}-{uuid.uuid4().hex[:6]}@example.org"
    r = client.post(f"/api/v1/orgs/{org_id}/members", headers=admin_h,
                    json={"email": email, "name": role, "password": PW, "role": role})
    assert r.status_code == 201, r.text
    tok = client.post("/api/v1/auth/login", json={"email": email, "password": PW}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}, r.json()["user_id"]


@pytest.fixture(scope="module")
def world(client):
    a_h, a_org, _ = _signup(client, "Org A")
    b_h, b_org, _ = _signup(client, "Org B")
    analyst, _ = _member(client, a_h, a_org, "analyst")
    reviewer, _ = _member(client, a_h, a_org, "reviewer")
    investor, _ = _member(client, a_h, a_org, "investor")
    p = client.post("/api/v1/projects", headers=analyst, json={"org_id": a_org, "name": "Portfolio 1", "country": "Fictitia"})
    assert p.status_code == 201, p.text
    return dict(a_h=a_h, a_org=a_org, b_h=b_h, b_org=b_org, analyst=analyst, reviewer=reviewer,
                investor=investor, project=p.json()["id"])


def test_health_and_engine_info(client):
    assert client.get("/health").json()["status"] == "ok"
    info = client.get("/api/v1/engine/info").json()
    assert info["deterministic"] and not info["uses_generative_ai"]
    names = [o["name"] for o in client.get("/api/v1/engine/options").json()]
    assert "cap_principal_at_balance" in names


def test_auth_required_and_bad_login(client):
    assert client.get("/api/v1/projects").status_code == 401
    assert client.get("/api/v1/projects", headers={"Authorization": "Bearer nope"}).status_code == 401
    assert client.post("/api/v1/auth/login", json={"email": "x@example.org", "password": "wrong-password!!"}).status_code == 401


def test_weak_password_rejected(client):
    r = client.post("/api/v1/auth/signup", json={"organization": "Weak", "email": "w@example.org", "name": "W",
                                                  "password": "short"})
    assert r.status_code == 422


def test_tenant_isolation(client, world):
    pid = world["project"]
    assert client.get(f"/api/v1/projects/{pid}", headers=world["b_h"]).status_code == 404
    assert client.get("/api/v1/projects", headers=world["b_h"]).json() == []
    r = client.post("/api/v1/projects", headers=world["b_h"], json={"org_id": world["a_org"], "name": "intrusion"})
    assert r.status_code == 404
    v = client.post(f"/api/v1/projects/{pid}/versions", headers=world["analyst"], json={"template": "demo_fictitious"}).json()
    assert client.get(f"/api/v1/versions/{v['id']}", headers=world["b_h"]).status_code == 404
    run = client.post(f"/api/v1/versions/{v['id']}/runs", headers=world["analyst"]).json()
    assert client.get(f"/api/v1/runs/{run['id']}", headers=world["b_h"]).status_code == 404
    assert client.get(f"/api/v1/orgs/{world['a_org']}/audit", headers=world["b_h"]).status_code == 404


def test_roles(client, world):
    assert client.post("/api/v1/projects", headers=world["investor"],
                       json={"org_id": world["a_org"], "name": "x"}).status_code == 403
    assert client.post("/api/v1/projects", headers=world["reviewer"],
                       json={"org_id": world["a_org"], "name": "x"}).status_code == 403
    assert client.post(f"/api/v1/orgs/{world['a_org']}/members", headers=world["analyst"],
                       json={"email": "z@example.org", "name": "z", "password": PW, "role": "admin"}).status_code == 403


def test_versions_runs_review_workflow(client, world):
    pid, an, rv, inv = world["project"], world["analyst"], world["reviewer"], world["investor"]
    v1 = client.post(f"/api/v1/projects/{pid}/versions", headers=an,
                     json={"scenario": "reference", "template": "crossboundary_reference"}).json()
    assert v1["version"] == 1 and v1["provenance"]["template"] == "crossboundary_reference"
    r1 = client.post(f"/api/v1/versions/{v1['id']}/runs", headers=an).json()
    assert r1["status"] == "reconciled-engine", r1["error"]
    assert abs(r1["result"]["kpis"]["project_irr"]["value"] - 0.12657422423362732) < 1e-8
    # revision by workbook cell: DSCR sizing (scenario S2)
    v2 = client.post(f"/api/v1/versions/{v1['id']}/revise", headers=an, json={"changes": {"Inputs!E302": "DSCR"}}).json()
    assert v2["version"] == 2 and v2["parent_id"] == v1["id"] and v2["content_hash"] != v1["content_hash"]
    r2 = client.post(f"/api/v1/versions/{v2['id']}/runs", headers=an).json()
    assert abs(r2["result"]["kpis"]["project_irr"]["value"] - 0.1269103426829644) < 1e-9
    # variant run is labelled as such
    v3 = client.post(f"/api/v1/versions/{v2['id']}/revise", headers=an,
                     json={"options": {"cap_principal_at_balance": True}}).json()
    r3 = client.post(f"/api/v1/versions/{v3['id']}/runs", headers=an).json()
    assert r3["status"] == "variant"
    # investors only see approved versions
    assert all(x["status"] == "approved" for x in client.get(f"/api/v1/projects/{pid}/versions", headers=inv).json())
    assert client.get(f"/api/v1/versions/{v2['id']}", headers=inv).status_code == 404
    # submit -> four-eyes review
    assert client.post(f"/api/v1/versions/{v2['id']}/submit", headers=an).json()["status"] == "submitted"
    assert client.post(f"/api/v1/versions/{v2['id']}/review", headers=an,
                       json={"decision": "approve"}).status_code == 403          # author cannot approve (and analyst role)
    ok = client.post(f"/api/v1/versions/{v2['id']}/review", headers=rv, json={"decision": "approve", "comment": "checked"})
    assert ok.json()["status"] == "approved"
    assert client.get(f"/api/v1/versions/{v2['id']}", headers=inv).status_code == 200
    # submitting without a run is refused
    v4 = client.post(f"/api/v1/versions/{v2['id']}/revise", headers=an, json={"changes": {"debt.tenor_years": 10}}).json()
    assert client.post(f"/api/v1/versions/{v4['id']}/submit", headers=an).status_code == 409
    # CSV export
    csv = client.get(f"/api/v1/runs/{r2['id']}/series.csv", headers=inv)
    assert csv.status_code == 200 and csv.text.startswith("series,label,unit,source,derived,2023")
    assert "Model!87" in csv.text


def test_invalid_inputs_rejected(client, world):
    pid, an = world["project"], world["analyst"]
    r = client.post(f"/api/v1/projects/{pid}/versions", headers=an,
                    json={"template": "demo_fictitious", "changes": {"debt.no_such_field": 1}})
    assert r.status_code == 422
    r = client.post(f"/api/v1/projects/{pid}/versions", headers=an,
                    json={"template": "demo_fictitious", "changes": {"reserves.dsra_months": 13}})
    assert r.status_code == 422 and "issues" in r.text
    r = client.post(f"/api/v1/projects/{pid}/versions", headers=an,
                    json={"template": "demo_fictitious", "options": {"bogus": True}})
    assert r.status_code == 422


def test_uploads_validated(client, world):
    pid, an = world["project"], world["analyst"]
    r = client.post(f"/api/v1/projects/{pid}/versions/import-xlsm", headers=an,
                    files={"file": ("evil.exe", b"MZ\x90\x00", "application/octet-stream")})
    assert r.status_code == 415
    r = client.post(f"/api/v1/projects/{pid}/versions/import-xlsm", headers=an,
                    files={"file": ("fake.xlsm", b"PK\x03\x04garbage", "application/vnd.ms-excel")})
    assert r.status_code == 422
    from .conftest import WORKBOOK
    if WORKBOOK.exists():
        r = client.post(f"/api/v1/projects/{pid}/versions/import-xlsm", headers=an,
                        files={"file": (WORKBOOK.name, WORKBOOK.read_bytes(), "application/vnd.ms-excel")})
        assert r.status_code == 201, r.text
        assert r.json()["provenance"]["sha256"].startswith("fe0ecb16")


def test_database_guarantees(client, world):
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import DBAPIError
    eng = create_engine(DB_URL)
    with eng.connect() as c:
        with pytest.raises(DBAPIError):
            c.execute(text("UPDATE scenario_versions SET assumptions = '{}'::jsonb"))
        c.rollback()
        with pytest.raises(DBAPIError):
            c.execute(text("DELETE FROM audit_events"))
        c.rollback()
        n = c.execute(text("SELECT count(*) FROM audit_events WHERE action = 'version.approve'")).scalar()
        assert n >= 1
        tokens = c.execute(text("SELECT token_hash FROM session_tokens LIMIT 1")).scalar()
        assert len(tokens) == 64      # only hashes are stored
    eng.dispose()


def test_audit_log_and_logout(client, world):
    log = client.get(f"/api/v1/orgs/{world['a_org']}/audit", headers=world["a_h"]).json()
    actions = {e["action"] for e in log}
    assert {"project.create", "version.create", "run.create", "member.add"} <= actions
    h, _, _ = _signup(client, "Org C")
    assert client.post("/api/v1/auth/logout", headers=h).status_code == 204
    assert client.get("/api/v1/auth/me", headers=h).status_code == 401


def test_login_rate_limited(client):
    codes = [client.post("/api/v1/auth/login", json={"email": "brute@example.org", "password": "x" * 12}).status_code
             for _ in range(7)]
    assert 429 in codes
