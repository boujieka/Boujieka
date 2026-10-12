import pytest

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


def test_anchor_option_needs_an_anchor_and_costs_like_d():
    """F differs from D by its anchor contract, not its engineering: same cost, but it needs an anchor (review F17)."""
    s, c = demo_settlement()
    r = compare(s, c)
    d = next(o for o in r["options"] if o["code"] == "D")
    f = next(o for o in r["options"] if o["code"] == "F")
    assert f["sizing"]["battery_kwh"] == d["sizing"]["battery_kwh"] and f["pv_lifecycle_cost"] == d["pv_lifecycle_cost"]
    s.anchor_present = False
    r2 = compare(s, c)
    assert not next(o for o in r2["options"] if o["code"] == "F")["feasible"]


def test_partial_service_options_are_gated():
    """An option serving only households cannot win by leaving most demand unserved (review F08)."""
    s, c = demo_settlement()
    c.shs_cost_per_household = 40_000
    r = compare(s, c)
    e = next(o for o in r["options"] if o["code"] == "E")
    assert not e["feasible"] and any("unserved" in g for g in e["gates_failed"])
    assert r["least_cost"] != "E" and r["recommended"] != "E"


def test_revenue_uses_class_tariffs_and_affordability_cap():
    """Revenue = served kWh by class x class tariff, household tariff capped by affordability (review F09)."""
    s, c = demo_settlement()
    s.household_kwh_month = 1  # tiny use: the affordability cap must not inflate revenue
    r = compare(s, c)
    d = next(o for o in r["options"] if o["code"] == "D")
    from app.engine.optimizer import _pv_factor
    af = _pv_factor(c.discount_rate_pa, c.horizon_years)
    rev = (s.households * 1 * 12 * min(c.tariff_household_per_kwh, 0.1 * s.household_income_month / 1)
           + s.businesses * s.business_kwh_month * 12 * c.tariff_business_per_kwh
           + s.productive_users * s.productive_kwh_month * 12 * c.tariff_productive_per_kwh
           + s.institutions * s.institution_kwh_month * 12 * c.tariff_institution_per_kwh
           + s.anchor_kwh_month * 12 * c.tariff_anchor_per_kwh)
    assert d["cost_recovery_ratio"] == pytest.approx(rev * af / d["pv_lifecycle_cost"])
    assert d["cost_recovery_ratio"] < 5


def test_zero_cost_option_does_not_crash():
    s, c = demo_settlement()
    c.shs_cost_per_household = 0.0
    c.max_unserved_share = 1.0
    compare(s, c)  # review F16: must not raise


def test_weights_change_the_recommendation_not_the_costs():
    s, c = demo_settlement()
    a = compare(s, c)
    b = compare(s, c, Weights(economic_cost=0.0, time=1.0, service_quality=0, subsidy_efficiency=0, financial_sustainability=0,
                              environment=0, productive_use=0))
    assert [o["lcoe"] for o in a["options"]] == [o["lcoe"] for o in b["options"]]
    fastest = min((o for o in b["options"] if o["feasible"]), key=lambda o: o["months_to_electrify"])
    assert b["recommended"] == fastest["code"]
