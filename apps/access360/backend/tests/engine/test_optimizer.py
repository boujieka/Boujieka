from app.engine.optimizer import Weights, compare, demo_settlement


def test_infeasible_options_are_never_ranked():
    s, c = demo_settlement()
    r = compare(s, c)
    for o in r["options"]:
        if not o["feasible"]:
            assert o["score"] is None and not o["pareto_efficient"] and o["gates_failed"]
    assert r["recommended"] in {o["code"] for o in r["options"] if o["feasible"]}
    assert r["least_cost"] in {o["code"] for o in r["options"] if o["feasible"]}


def test_unknown_grid_distance_blocks_grid_options():
    s, c = demo_settlement()
    s.distance_to_grid_km = None
    r = compare(s, c)
    grid = [o for o in r["options"] if o["code"] in ("A", "B")]
    assert all(not o["feasible"] for o in grid)


def test_least_cost_is_minimum_lcoe_among_feasible():
    s, c = demo_settlement()
    r = compare(s, c)
    feas = [o for o in r["options"] if o["feasible"]]
    assert r["least_cost"] == min(feas, key=lambda o: o["lcoe"])["code"]


def test_pareto_flags_dominated_options():
    s, c = demo_settlement()
    r = compare(s, c)
    feas = [o for o in r["options"] if o["feasible"]]
    assert any(o["pareto_efficient"] for o in feas)
    from app.engine.optimizer import OBJECTIVES
    for o in feas:
        if not o["pareto_efficient"]:
            assert any(all(q["objectives"][k] * sg >= o["objectives"][k] * sg for k, sg, _ in OBJECTIVES) and q is not o
                       for q in feas)


def test_anchor_option_needs_an_anchor_and_reduces_storage():
    s, c = demo_settlement()
    r = compare(s, c)
    d = next(o for o in r["options"] if o["code"] == "D")
    f = next(o for o in r["options"] if o["code"] == "F")
    assert f["sizing"]["battery_kwh"] < d["sizing"]["battery_kwh"]
    s.anchor_present = False
    r2 = compare(s, c)
    assert not next(o for o in r2["options"] if o["code"] == "F")["feasible"]


def test_weights_change_the_recommendation_not_the_costs():
    s, c = demo_settlement()
    a = compare(s, c)
    b = compare(s, c, Weights(economic_cost=0.0, time=1.0, service_quality=0, subsidy_efficiency=0, financial_sustainability=0,
                              environment=0, productive_use=0))
    assert [o["lcoe"] for o in a["options"]] == [o["lcoe"] for o in b["options"]]
    fastest = min((o for o in b["options"] if o["feasible"]), key=lambda o: o["months_to_electrify"])
    assert b["recommended"] == fastest["code"]
