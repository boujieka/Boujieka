"""Optimiser and rule-based dispatch tests (small horizons for speed, plus one full-year run)."""

import numpy as np
import pytest

from src.optimization.dispatch import simulate_dispatch
from src.optimization.optimizer import optimise_scenario, recommend
from src.optimization.system import (
    BatteryTech,
    BiomassTech,
    Capacities,
    DieselTech,
    Economics,
    GridTech,
    Profiles,
    PVTech,
    SystemSpec,
)

TOL = 1e-5


def day_profiles(T=24, load=100.0):
    hours = np.arange(T) % 24
    pv = ((hours >= 6) & (hours < 18)).astype(float)
    return Profiles(np.full(T, load), pv, np.ones(T))


def spec(**kw):
    base = dict(
        pv=PVTech(capex_per_kwp=1000, lifetime_years=20),
        battery=BatteryTech(capex_per_kwh=500, capex_per_kw=100, calendar_life_years=10, cycle_life_efc=5000),
        diesel=DieselTech(existing_kw=150, unit_size_kw=50, new_capex_per_kw=500, fuel_price_per_l=1.0, sfc_l_per_kwh=0.3, min_loading=0.3),
        economics=Economics(discount_rate=0.08, project_life_years=20, value_of_lost_load_per_kwh=10.0, max_unserved_fraction=0.0),
    )
    base.update(kw)
    return SystemSpec(**base)


def assert_physics(res, s):
    d = res.diagnostics
    assert d["max_energy_balance_error_kw"] < TOL
    assert d["max_pv_split_error_kw"] < TOL
    if res.capacities.battery_kwh > 0:
        assert d["battery_soc_residual_kwh"] < 1e-4
        assert d["battery_simultaneous_hours"] == 0
        assert d["battery_soc_min_violation_kwh"] < 1e-4
        assert d["battery_soc_max_violation_kwh"] < 1e-4


def test_diesel_only_adds_missing_capacity():
    s = spec(diesel=DieselTech(existing_kw=50, unit_size_kw=50, new_capex_per_kw=500, fuel_price_per_l=1.0, sfc_l_per_kwh=0.3))
    r = optimise_scenario("diesel_only", s, day_profiles())
    assert r.status == "Optimal" and r.feasible
    assert r.capacities.diesel_new_kw == pytest.approx(50, abs=1e-6)
    assert r.metrics["unserved_fraction"] == pytest.approx(0)
    assert r.annual_energy["diesel"] == pytest.approx(100 * 8760)
    assert r.metrics["fuel_l"] == pytest.approx(0.3 * 100 * 8760)
    assert_physics(r, s)


def test_pv_sized_to_daytime_load_without_storage():
    r = optimise_scenario("pv_diesel", spec(), day_profiles())
    assert r.capacities.pv_kwp == pytest.approx(100, rel=1e-6)  # more PV would only be curtailed
    assert r.annual_energy["pv_curtailed"] == pytest.approx(0, abs=1e-3)
    assert r.annual_energy["diesel"] == pytest.approx(12 * 100 * 365)
    assert r.metrics["renewable_share"] == pytest.approx(0.5)


def test_storage_shifts_solar_and_respects_physics():
    s = spec(battery=BatteryTech(capex_per_kwh=100, capex_per_kw=20, calendar_life_years=10, cycle_life_efc=5000))
    r = optimise_scenario("pv_bess_diesel", s, day_profiles(T=72))
    assert r.feasible
    assert r.capacities.battery_kwh > 0
    assert r.metrics["renewable_share"] > 0.5
    assert_physics(r, s)


def test_capacity_limit_respected():
    s = spec(pv=PVTech(capex_per_kwp=1000, lifetime_years=20, max_kwp=40))
    r = optimise_scenario("pv_diesel", s, day_profiles())
    assert r.capacities.pv_kwp <= 40 + 1e-6


def test_fixed_capacity_is_enforced():
    s = spec(pv=PVTech(capex_per_kwp=1000, lifetime_years=20, fixed_kwp=75))
    r = optimise_scenario("pv_diesel", s, day_profiles())
    assert r.capacities.pv_kwp == pytest.approx(75)


def test_infeasibility_reported_clearly():
    s = spec(diesel=DieselTech(existing_kw=50, allow_new_capacity=False, fuel_price_per_l=1.0, sfc_l_per_kwh=0.3))
    r = optimise_scenario("diesel_only", s, day_profiles())
    assert not r.feasible
    assert r.status == "Infeasible"
    assert "reliability" in r.message


def test_not_applicable_when_technology_missing():
    r = optimise_scenario("grid_diesel", spec(), day_profiles())
    assert r.status == "Not applicable" and not r.feasible


def test_biomass_fuel_limit():
    s = spec(biomass=BiomassTech(capex_per_kw=10, marginal_cost_per_kwh=0.01, annual_energy_limit_kwh=100_000, availability=1.0))
    r = optimise_scenario("biomass_pv_diesel", s, day_profiles())
    assert r.annual_energy["biomass"] <= 100_000 + 1e-3
    assert r.annual_energy["biomass"] == pytest.approx(100_000, rel=1e-4)


def test_grid_outages_need_backup():
    T = 48
    prof = day_profiles(T)
    prof.grid_available = np.ones(T)
    prof.grid_available[20:24] = 0  # 4-hour outage each 2 days
    s = spec(grid=GridTech(price_per_kwh=0.05))
    r = optimise_scenario("grid_diesel", s, prof)
    assert r.feasible
    assert np.all(r.hourly["grid"][20:24] == 0)
    assert r.hourly["diesel"][20:24] == pytest.approx(np.full(4, 100.0))


def test_recommendation_lowest_cost_feasible():
    s = spec()
    res = {k: optimise_scenario(k, s, day_profiles()) for k in ("diesel_only", "pv_diesel")}
    best = recommend(res, 0.0)
    costs = {k: v.metrics["annual_cost"] for k, v in res.items()}
    assert best == min(costs, key=costs.get)


# ----------------------------------------------------------------------- rule-based dispatch


def test_dispatch_min_loading_and_balance():
    s = spec()
    prof = Profiles(np.array([10.0, 60.0, 140.0, 5.0] * 6), np.zeros(24), np.ones(24))
    r = simulate_dispatch("diesel_only", Capacities(diesel_existing_kw=150), s, prof)
    assert r.diagnostics["max_energy_balance_error_kw"] < TOL
    assert r.diagnostics["diesel_hours_below_min_loading"] == 0
    # 10 kW load with 50 kW units at 30 % minimum -> 15 kW generated, 5 kW dumped.
    assert r.hourly["diesel"][0] == pytest.approx(15.0)
    assert r.hourly["diesel_excess"][0] == pytest.approx(5.0)


def test_dispatch_battery_exclusive_and_bounded():
    s = spec()
    prof = day_profiles(T=96)
    r = simulate_dispatch("pv_bess_diesel", Capacities(pv_kwp=250, battery_kwh=600, battery_kw=150, diesel_existing_kw=150), s, prof)
    d = r.diagnostics
    assert d["max_energy_balance_error_kw"] < TOL
    assert d["battery_soc_residual_kwh"] < 1e-9
    assert d["battery_simultaneous_hours"] == 0
    assert r.hourly["soc"].min() >= 0.1 * 600 - 1e-9
    assert r.hourly["soc"].max() <= 0.95 * 600 + 1e-9
    assert r.hourly["charge"].max() <= 150 + 1e-9


def test_dispatch_grid_reserve_covers_outage():
    T = 48
    prof = Profiles(np.full(T, 100.0), np.zeros(T), np.ones(T))
    prof.grid_available[30:33] = 0
    s = spec(grid=GridTech(price_per_kwh=0.05),
             battery=BatteryTech(capex_per_kwh=500, soc_min=0.0, soc_max=1.0, charge_efficiency=1.0, discharge_efficiency=1.0,
                                 outage_reserve_fraction=1.0))
    r = simulate_dispatch("grid_pv_bess", Capacities(battery_kwh=400, battery_kw=100), s, prof)
    assert r.annual_energy["unserved"] == pytest.approx(0.0)
    assert r.diagnostics["max_energy_balance_error_kw"] < TOL


@pytest.mark.slow
def test_full_year_lp_is_optimal_and_reconciles():
    from src.assumptions import ProjectAssumptions
    from src.demo.case_studies import forestry
    from src.study import prepare_study

    case = forestry()
    study = prepare_study(ProjectAssumptions(**case["assumptions"]), case["sector"])
    assert study.profiles.n == 8760
    r = optimise_scenario("pv_bess_diesel", study.spec, study.profiles)
    assert r.status == "Optimal"
    assert_physics(r, study.spec)
    assert r.annual_energy["load"] == pytest.approx(case["annual_demand_kwh"], rel=1e-9)
    check = simulate_dispatch("pv_bess_diesel", r.capacities, study.spec, study.profiles)
    assert check.diagnostics["max_energy_balance_error_kw"] < TOL
    assert check.diagnostics["diesel_hours_below_min_loading"] == 0
