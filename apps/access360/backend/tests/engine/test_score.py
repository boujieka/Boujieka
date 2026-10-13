import pytest

from app.engine.score import GATES, ScoreInputs, Weights, rank, score_project


def full(**over):
    base = dict(project_id="p", project_name="P", connections=2000, subsidy_per_connection_usd=0, dscr_min=1.5, months_to_power=6,
                productive_energy_share=1.0, household_share=1.0, underserved_area=True, readiness_done=6, readiness_required=6,
                gates={k: "met" for k in GATES})
    base.update(over)
    return ScoreInputs(**base)


def test_perfect_project_scores_100_and_is_eligible():
    r = score_project(full())
    assert r["score"] == pytest.approx(100.0)
    assert r["decision"] == "eligible" and not r["score_is_partial"]


def test_points_follow_weights_and_explanations_exist():
    r = score_project(full(connections=1000))  # half the access scale
    access = next(p for p in r["parts"] if p["criterion"] == "access_impact")
    assert access["points"] == pytest.approx(10.0)  # 0.5 x 20%
    assert all(p["explanation"] for p in r["parts"])


def test_failed_gate_overrides_a_high_score():
    gates = {k: "met" for k in GATES}
    gates["land_rights"] = "not_met"
    r = score_project(full(gates=gates))
    assert r["score"] == pytest.approx(100.0)
    assert r["decision"] == "excluded" and "Land rights" in r["decision_explanation"]
    ranked = rank([full(project_id="a", gates=gates), full(project_id="b", connections=10)])
    assert ranked[0]["project_id"] == "b" and ranked[0]["rank"] == 1
    assert ranked[1]["rank"] is None


def test_unknown_gate_means_review_and_missing_data_is_partial():
    r = score_project(ScoreInputs(project_id="x", project_name="X"))
    assert r["decision"] == "review_required"
    assert r["score_is_partial"] and r["score"] == 0.0
    assert any(p["explanation"].startswith("Data unavailable") for p in r["parts"])


def test_weights_are_configurable():
    w = Weights(access_impact=1, financial_efficiency=0, readiness=0, speed=0, productive_use=0, equity=0)
    assert score_project(full(connections=500), w)["score"] == pytest.approx(25.0)
