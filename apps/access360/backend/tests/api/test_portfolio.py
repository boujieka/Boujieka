import uuid

from app.engine.demo import demo_inputs
from tests.api.test_api import PW, make_project, new_client, org_id, register


def test_score_gates_and_portfolio_ranking(db_ready):
    c = new_client()
    u = register(c)
    oid = org_id(u)
    a = make_project(c, oid)
    b = make_project(c, oid)
    for pid in (a, b):
        assert c.post(f"/api/orgs/{oid}/projects/{pid}/runs").status_code == 201
    # model_checks is read only
    assert c.put(f"/api/orgs/{oid}/projects/{a}/gates", json={"gates": {"model_checks": "met"}}).status_code == 422
    met = {g: "met" for g in ("land_rights", "permits", "technical_feasibility", "environmental_social", "regulatory")}
    assert c.put(f"/api/orgs/{oid}/projects/{a}/gates", json={"gates": met, "underserved_area": True}).status_code == 200
    bad = {**met, "land_rights": "not_met"}
    assert c.put(f"/api/orgs/{oid}/projects/{b}/gates", json={"gates": bad, "underserved_area": True}).status_code == 200
    s = c.post(f"/api/orgs/{oid}/projects/{a}/score", json={}).json()
    assert s["decision"] == "eligible" and 0 < s["score"] <= 100
    assert s["sources"]["model_checks"].startswith("latest run status")
    f = c.post(f"/api/orgs/{oid}/portfolios", json={"name": "Pipeline 2027"}).json()["id"]
    for pid in (a, b):
        assert c.post(f"/api/orgs/{oid}/portfolios/{f}/projects", json={"project_id": pid}).status_code == 201
    an = c.post(f"/api/orgs/{oid}/portfolios/{f}/analysis", json={}).json()
    first, second = an["ranking"]
    assert first["project_id"] == a and first["rank"] == 1
    assert second["decision"] == "excluded" and second["rank"] is None
    # the runs use synthetic demo inputs, so both projects are totalled as demo, never as real
    assert an["totals_demo"]["projects"] == 2 and an["totals_real"]["projects"] == 0


def test_portfolio_is_tenant_isolated(db_ready):
    a, b = new_client(), new_client()
    ua, ub = register(a), register(b)
    f = a.post(f"/api/orgs/{org_id(ua)}/portfolios", json={"name": "Private"}).json()["id"]
    assert b.post(f"/api/orgs/{org_id(ub)}/portfolios/{f}/analysis", json={}).status_code == 404
    assert b.get(f"/api/orgs/{org_id(ub)}/portfolios").json() == []
    pid = make_project(a, org_id(ua))
    # cannot add another tenant's project to one's own portfolio
    g = b.post(f"/api/orgs/{org_id(ub)}/portfolios", json={"name": "Mine"}).json()["id"]
    assert b.post(f"/api/orgs/{org_id(ub)}/portfolios/{g}/projects", json={"project_id": pid}).status_code == 404
    _ = (uuid, demo_inputs, PW)


def test_gates_partial_update_and_project_returns_them(db_ready):
    c = new_client()
    u = register(c)
    oid = org_id(u)
    pid = make_project(c, oid)
    c.put(f"/api/orgs/{oid}/projects/{pid}/gates", json={"gates": {"permits": "met"}, "months_to_power": 9, "underserved_area": True})
    c.put(f"/api/orgs/{oid}/projects/{pid}/gates", json={"gates": {"land_rights": "met"}})
    p = c.get(f"/api/orgs/{oid}/projects/{pid}").json()
    assert p["gates"] == {"permits": "met", "land_rights": "met"}
    assert p["score_context"] == {"months_to_power": 9, "underserved_area": True}
