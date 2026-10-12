"""Deterministic tests of the ACCESS FINANCE engine: hand-checkable cases, reconciliations and fault injection."""
from __future__ import annotations

from datetime import date

import numpy as np
import numpy_financial as npf
import pytest

from app.engine.checks import ModelStatus, integrity_checks, status
from app.engine.demo import demo_inputs
from app.engine.finance import annuity_payment, irr, npv, q_rate
from app.engine.inputs import (CapexItem, CustomerClass, DebtTranche, Financing, GrantMilestone, GridArrival, Macro, Opex,
                               ProjectInputs, Review, Subsidies, Technical)
from app.engine.model import run_model
from app.engine.sensitivity import minimum_capital_grant, sensitivity_table, standard_cases, run_case, tornado


def simple(**over) -> ProjectInputs:
    """One customer class, flat prices, no tax, no debt, no subsidy: every number can be checked by hand."""
    base = dict(
        project_name="Unit test", country="Test", currency="XTS", financial_close=date(2027, 1, 1),
        construction_quarters=2, operating_years=10,
        technical=Technical(pv_kwp=10, battery_kwh=0, deliverable_energy_kwh_pa=1_000_000, technical_loss=0.0, commercial_loss=0.0),
        customers=[CustomerClass(name="H", category="household", connections_target=100, ramp_quarters=1,
                                 kwh_per_connection_month=10, tariff_per_kwh=100)],
        capex=[CapexItem(name="Plant", category="generation", amount=1_000_000, asset_life_years=10)],
        opex=Opex(fixed_pa=100_000, collection_efficiency=1.0),
        macro=Macro(fx_lcy_per_usd=1.0, discount_rate_pa=0.10),
    )
    base.update(over)
    return ProjectInputs(**base)


def all_pass(r) -> bool:
    return all(c.passed for c in integrity_checks(r))


# ---------------------------------------------------------------- hand calculations
def test_revenue_opex_and_project_irr_by_hand():
    r = run_model(simple())
    C = r.C
    # 100 connections x 10 kWh x 3 months x 100 LCY = 300,000 a quarter; opex 25,000 a quarter
    assert r.s("revenue")[C] == pytest.approx(300_000)
    assert r.s("opex")[C] == pytest.approx(25_000)
    assert r.s("ebitda")[C] == pytest.approx(275_000)
    flows = np.array([-500_000, -500_000] + [275_000] * 40)
    assert np.allclose(r.s("project_cf_pre_subsidy"), flows)
    expected = (1 + npf.irr(flows)) ** 4 - 1
    assert r.metrics["project_irr_pre_subsidy"] == pytest.approx(expected, rel=1e-9)
    assert r.metrics["cost_per_connection"] == pytest.approx(10_000)
    assert all_pass(r)


def test_depreciation_straight_line_from_cod():
    r = run_model(simple())
    dep = r.s("depreciation")
    assert dep[:2].sum() == 0
    assert dep[2] == pytest.approx(1_000_000 / 40)
    assert dep.sum() == pytest.approx(1_000_000)


def test_irr_and_npv_helpers_match_numpy_financial():
    rng = np.random.default_rng(7)
    for _ in range(20):
        cf = np.concatenate([[-rng.uniform(100, 1000)], rng.uniform(-50, 300, 30)])
        mine, ref = irr(cf), npf.irr(cf)
        if ref is not None and np.isfinite(ref) and -0.5 < ref < 1:
            assert mine == pytest.approx(ref, abs=1e-9)
            assert npv(mine, cf) == pytest.approx(0.0, abs=1e-6)
    assert irr(np.array([1.0, 2.0])) is None


def test_lcy_annuity_schedule():
    p = simple(financing=Financing(debt=[DebtTranche(name="L", share_of_capex=0.5, rate_pa=0.12, tenor_years=5)], dsra_quarters=0),
               subsidies=Subsidies())
    r = run_model(p)
    tr = r.tranches[0]
    C = r.C
    bal_cod = tr["balance"][C - 1]
    assert bal_cod == pytest.approx(500_000)
    pay = annuity_payment(bal_cod, q_rate(0.12), 20)
    ds = tr["interest"][C:C + 20] + tr["principal"][C:C + 20]
    assert np.allclose(ds, pay)
    assert tr["balance"][C + 19] == pytest.approx(0.0, abs=1e-6)
    assert tr["interest"][C] == pytest.approx(bal_cod * q_rate(0.12))
    assert all_pass(r)


def test_usd_debt_translation_and_fx_loss():
    p = simple(macro=Macro(fx_lcy_per_usd=100.0, fx_depreciation_pa=0.10, discount_rate_pa=0.1),
               financing=Financing(debt=[DebtTranche(name="U", currency="USD", share_of_capex=0.5, rate_pa=0.05, tenor_years=5)]))
    r = run_model(p)
    tr = r.tranches[0]
    fx = r.s("fx")
    assert fx[4] == pytest.approx(100.0 * 1.10)
    usd_bal = tr["balance"] / fx
    open_usd = np.concatenate([[0.0], usd_bal[:-1]])
    assert np.allclose(tr["fx_loss"][1:], open_usd[1:] * np.diff(fx))
    assert tr["fx_loss"].sum() > 0
    assert all_pass(r)


def test_usd_capex_converted_at_spend_rate():
    p = simple(capex=[CapexItem(name="PV", category="generation", amount=1000, currency="USD", asset_life_years=10)],
               macro=Macro(fx_lcy_per_usd=500.0, fx_depreciation_pa=0.2, discount_rate_pa=0.1))
    r = run_model(p)
    fx = r.s("fx")
    assert r.s("capex")[0] == pytest.approx(500 * fx[0])
    assert r.s("capex")[1] == pytest.approx(500 * fx[1])


def test_battery_replacement_schedule_and_reserve():
    p = demo_inputs()
    r = run_model(p)
    repl = r.s("battery_replacement")
    idx = list(np.nonzero(repl)[0])
    assert idx == [r.C + 32, r.C + 64]  # 8 year life, 20 operating years
    items = r.s("replacement_capex") - repl
    assert list(np.nonzero(items)[0]) == [r.C + 40]  # genset and meters (10 years), replaced once
    t = idx[0]
    exp = 300 * 220 * (1 - 0.03) ** 8 * r.s("fx")[t]
    assert repl[t] == pytest.approx(exp)
    mra = r.s("mra")
    assert mra[t - 1] == pytest.approx(repl[t])
    assert mra[t] == pytest.approx(0.0, abs=1e-6)


def test_rbf_lag_and_cap():
    p = simple(subsidies=Subsidies(rbf_per_connection=1000, rbf_verification_lag_quarters=3, rbf_cap=60_000))
    r = run_model(p)
    rbf = r.s("rbf_receipts")
    C = r.C
    assert rbf[:C + 3].sum() == 0
    assert rbf[C + 3] == pytest.approx(60_000)  # 100 connections x 1,000 capped at 60,000
    assert rbf.sum() == pytest.approx(60_000)


def test_capital_grant_milestones_and_deferred_income():
    p = simple(subsidies=Subsidies(capital_grant=400_000, grant_milestones=[GrantMilestone(quarter=0, share=0.25),
                                                                           GrantMilestone(quarter=6, share=0.75)]))
    r = run_model(p)
    g = r.s("grant_receipts")
    assert g[0] == pytest.approx(100_000) and g[6] == pytest.approx(300_000)
    assert r.s("grant_income").sum() == pytest.approx(400_000)
    assert r.s("deferred_grant")[-1] == pytest.approx(0.0, abs=1e-6)
    assert all_pass(r)


def test_subsidy_delay_raises_liquidity_need():
    base = demo_inputs()
    late = base.model_copy(deep=True)
    for ms in late.subsidies.grant_milestones:
        ms.quarter += 4 if ms.quarter >= late.construction_quarters else 0
    late.subsidies.rbf_verification_lag_quarters += 4
    a, b = run_model(base), run_model(late)
    assert b.metrics["equity_peak"] >= a.metrics["equity_peak"] - 1e-6
    assert all_pass(b)


def test_negative_operating_cash_is_met_by_equity_support():
    p = simple(opex=Opex(fixed_pa=2_000_000, collection_efficiency=1.0))  # opex above revenue
    r = run_model(p)
    assert r.metrics["equity_support_total"] > 0
    assert np.min(r.s("cash")) >= -1e-6
    assert all_pass(r)


def test_dscr_annual_definition():
    r = run_model(demo_inputs())
    C = r.C
    for y in range(4):
        cf = r.s("cfads")[C + 4 * y:C + 4 * y + 4].sum()
        ds = r.s("debt_service")[C + 4 * y:C + 4 * y + 4].sum()
        assert r.annual["dscr"][y] == pytest.approx(cf / ds)
    assert r.metrics["dscr_min"] == pytest.approx(min(d for d in r.annual["dscr"] if d == d))


def test_capacity_limits_supply():
    p = simple(technical=Technical(pv_kwp=1, battery_kwh=0, deliverable_energy_kwh_pa=6_000, technical_loss=0.0, commercial_loss=0.0))
    r = run_model(p)
    assert r.s("supplied_kwh")[r.C] == pytest.approx(1_500)
    assert r.s("unserved_kwh")[r.C] == pytest.approx(3_000 - 1_500)


# ---------------------------------------------------------------- reconciliation across many configurations
@pytest.mark.parametrize("treatment", ["interconnect", "asset_transfer", "stranded"])
def test_grid_arrival_treatments_reconcile(treatment):
    p = demo_inputs()
    p.grid_arrival = GridArrival(enabled=True, operating_year=7, treatment=treatment, compensation_pct_nbv=0.6,
                                 tariff_factor_after=0.7, demand_factor_after=1.2, regulatory_source="unit test")
    r = run_model(p)
    assert all_pass(r), [c for c in integrity_checks(r) if not c.passed]
    if treatment != "interconnect":
        ta = r.C + 24
        assert r.s("revenue")[ta:].sum() == 0
        assert r.s("debt_balance")[ta] == pytest.approx(0.0, abs=1e-6)
        assert r.s("nbv")[ta] == pytest.approx(0.0, abs=1e-6)


def test_every_sensitivity_case_reconciles_and_moves_the_right_way():
    rows = sensitivity_table(demo_inputs())
    assert all(r["checks_passed"] for r in rows)
    by = {r["case"]: r for r in rows}
    assert by["CAPEX +10%"]["project_irr_post_subsidy"] < by["Base case"]["project_irr_post_subsidy"] < by["CAPEX -10%"]["project_irr_post_subsidy"]
    assert by["Tariff -10%"]["project_npv_post_subsidy"] < by["Base case"]["project_npv_post_subsidy"] < by["Tariff +10%"]["project_npv_post_subsidy"]
    assert by["Collection -10pp"]["project_npv_post_subsidy"] < by["Base case"]["project_npv_post_subsidy"]
    t = tornado(rows)
    assert t[0]["swing"] >= t[-1]["swing"]


def test_minimum_grant_solver_meets_threshold():
    res = minimum_capital_grant(demo_inputs(), min_dscr=1.3, tol=10_000)
    assert res["feasible"]
    assert res["dscr_min"] >= 1.3
    below = run_model(demo_inputs(), capital_grant_override=res["grant"] - 50_000)
    assert below.metrics["dscr_min"] < 1.3


# ---------------------------------------------------------------- status rules
def test_status_never_validated_without_review():
    r = run_model(simple())
    st, checks, warns, miss = status(r)
    assert not miss and all(c.passed for c in checks)
    assert st == ModelStatus.WARNING
    reviewed = simple(review=Review(reviewed_by="Analyst A", reviewed_on=date(2027, 1, 1)))
    st2, *_ = status(run_model(reviewed))
    assert st2 == ModelStatus.VALIDATED


def test_demo_is_never_validated():
    p = demo_inputs()
    p.review = Review(reviewed_by="X", reviewed_on=date(2027, 1, 1))
    st, *_ = status(run_model(p))
    assert st != ModelStatus.VALIDATED


def test_incomplete_inputs_status():
    p = simple(customers=[CustomerClass(name="H", category="household", connections_target=100, kwh_per_connection_month=10, tariff_per_kwh=0)])
    st, *_ , miss = status(run_model(p))
    assert st == ModelStatus.INCOMPLETE_INPUTS and miss


# ---------------------------------------------------------------- fault injection: each planted error must be caught
FAULTS = {
    "BS": lambda S: S["cash"].__setitem__(10, S["cash"][10] + 1_000.0),
    "CASH": lambda S: S["net_cash_flow"].__setitem__(12, S["net_cash_flow"][12] + 1_000.0),
    "FA": lambda S: S["depreciation"].__setitem__(9, S["depreciation"][9] + 1_000.0),
    "GRANT": lambda S: S["grant_income"].__setitem__(9, S["grant_income"][9] + 1_000.0),
    "DSRA": lambda S: S["dsra"].__setitem__(5, S["dsra"][5] + 1_000.0),
    "MRA": lambda S: S["mra"].__setitem__(33, -1_000.0),
    "NEGCASH": lambda S: S["cash"].__setitem__(20, -5_000.0),
    "ENERGY": lambda S: S["supplied_kwh"].__setitem__(8, S["supplied_kwh"][8] + 10.0),
    "COLL": lambda S: S["collections"].__setitem__(8, S["revenue"][8] + 10.0),
    "RBFVER": lambda S: S["rbf_receipts"].__setitem__(3, 1e9),
}


@pytest.mark.parametrize("code", sorted(FAULTS))
def test_fault_injection_is_detected(code):
    r = run_model(demo_inputs())
    assert all_pass(r)
    FAULTS[code](r.series)
    failed = {c.code for c in integrity_checks(r) if not c.passed}
    assert code in failed, f"planted fault {code} not detected; failed: {failed}"


def test_fault_debt_roll_forward_detected():
    r = run_model(demo_inputs())
    r.tranches[0]["principal"][12] += 1_000.0
    failed = {c.code for c in integrity_checks(r) if not c.passed}
    assert any(f.startswith("DEBT:") for f in failed)


def test_fault_sources_uses_detected():
    r = run_model(demo_inputs())
    r.sources_uses["equity"] += 1_000.0
    r.sources_uses["sources_total"] += 1_000.0
    assert "SU" in {c.code for c in integrity_checks(r) if not c.passed}


def test_all_standard_cases_have_names_and_groups():
    names = [n for _, n, _ in standard_cases()]
    assert len(names) == len(set(names)) and len(names) >= 18
    r = run_case(demo_inputs(), standard_cases()[0][2])
    assert all_pass(r)


# ---------------------------------------------------------------- regressions from the independent review (F01 to F15)
def test_f01_pre_subsidy_metrics_do_not_depend_on_tariff_support():
    a = demo_inputs()
    b = demo_inputs()
    b.subsidies.tariff_support_per_kwh = 150
    b.subsidies.tariff_support_years = 10
    ra, rb = run_model(a), run_model(b)
    assert np.allclose(ra.s("project_cf_pre_subsidy"), rb.s("project_cf_pre_subsidy"))
    assert ra.metrics["viability_gap_pv"] == pytest.approx(rb.metrics["viability_gap_pv"])
    assert rb.metrics["project_npv_post_subsidy"] > ra.metrics["project_npv_post_subsidy"]


def test_f02_solver_finds_zero_and_interior_answers_with_irr_targets():
    zero = minimum_capital_grant(demo_inputs(), min_dscr=None, min_equity_irr=0.01, tol=10_000)
    assert zero["feasible"] and zero["grant"] == 0.0
    mid = minimum_capital_grant(demo_inputs(), min_dscr=None, min_equity_irr=0.15, tol=10_000)
    assert mid["feasible"] and 0 < mid["grant"] < 286_000_000 and mid["equity_irr"] >= 0.15
    assert run_model(demo_inputs(), capital_grant_override=mid["grant"] - 50_000).metrics["equity_irr"] < 0.15


def test_f03_short_life_items_are_replaced_and_depreciated_over_their_life():
    r = run_model(demo_inputs())
    items = r.s("replacement_capex") - r.s("battery_replacement")
    assert items[r.C + 40] > 0 and items.sum() == pytest.approx(items[r.C + 40])
    with pytest.raises(Exception):  # storage life must equal the battery life
        p = demo_inputs().model_dump()
        p["technical"]["battery_life_years"] = 12
        ProjectInputs.model_validate(p)


def test_f04_construction_tax_is_in_sources_and_uses():
    p = demo_inputs()
    p.macro.fx_depreciation_pa = -0.10  # LCY appreciation: FX gain on USD debt during construction
    r = run_model(p)
    assert r.sources_uses["tax_during_construction"] > 0
    assert all_pass(r)


def test_f05_and_f14_invalid_timings_are_rejected():
    base = demo_inputs().model_dump()
    for path, value in ((("subsidies", "grant_milestones", 1, "quarter"), 500), (("subsidies", "grant_milestones", 0, "quarter"), -3),
                        (("financing", "debt", 0, "grace_quarters"), 40), (("financing", "debt", 1, "tenor_years"), 25),
                        (("technical", "battery_life_years"), 0.1)):
        d = demo_inputs().model_dump()
        node = d
        for k in path[:-1]:
            node = node[k]
        node[path[-1]] = value
        with pytest.raises(Exception):
            ProjectInputs.model_validate(d)
    assert base  # the unchanged demo stays valid
    ProjectInputs.model_validate(base)


def test_f05_grant_lost_to_closure_is_reported():
    p = demo_inputs()
    p.subsidies.grant_milestones = [GrantMilestone(quarter=0, share=0.5), GrantMilestone(quarter=40, share=0.5)]
    p.grid_arrival = GridArrival(enabled=True, operating_year=5, treatment="stranded", regulatory_source="unit test")
    r = run_model(p)
    assert r.metrics["capital_grant_undisbursed"] == pytest.approx(50_000_000)
    st, checks, warns, _ = status(r)
    assert "W_GRANT" in {w.code for w in warns}


def test_f07_closure_quarter_is_not_scheduled_debt_service():
    p = demo_inputs()
    p.grid_arrival = GridArrival(enabled=True, operating_year=8, treatment="asset_transfer", compensation_pct_nbv=0.6,
                                 regulatory_source="unit test")
    r = run_model(p)
    ta = r.C + 28
    assert r.s("debt_service")[ta] == 0.0 and r.s("prepayment")[ta] > 0
    assert r.metrics["dscr_min"] > 0
    assert r.metrics["closure_cover"] is not None
    assert all_pass(r)


def test_f11_minimum_cash_is_funded_before_cod():
    r = run_model(demo_inputs())
    assert r.s("cash")[r.C - 1] == pytest.approx(5_000_000)
    assert r.sources_uses["cash_at_cod"] == pytest.approx(5_000_000)


def test_f12_residual_disposal_releases_the_deferred_grant():
    p = demo_inputs()
    p.operating_years = 15
    p.residual_value_pct_nbv = 0.5
    r = run_model(ProjectInputs.model_validate(p.model_dump()))
    assert r.s("deferred_grant")[-1] == pytest.approx(0.0, abs=1e-6)
    assert all_pass(r)
