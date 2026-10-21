"""Financial model tests: hand-checked values and reconciliation identities."""

import numpy as np
import numpy_financial as npf
import pytest

from src.finance.cashflow import FinanceInputs, run_finance
from src.finance.common import levelized_cost
from src.finance.structures import STRUCTURES, StructureInputs, break_even_ppa_tariff, client_cash_flows, developer_cash_flows


def simple(**kw):
    params = dict(capex=1000.0, construction_years=1, operating_years=10, revenue_year1=200.0, opex_year1=50.0,
                  revenue_escalation=0.0, inflation=0.0, tax_rate=0.0, discount_rate=0.10, energy_year1_kwh=100.0)
    params.update(kw)
    return FinanceInputs(**params)


def test_unlevered_no_tax_matches_numpy_financial():
    r = run_finance(simple())
    cf = np.array([-1000.0] + [150.0] * 10)
    assert np.allclose(r.project_cf, cf)
    assert r.irr_project == pytest.approx(npf.irr(cf))
    assert r.npv_project == pytest.approx(float(np.sum(cf / 1.1 ** np.arange(11))))
    assert r.payback_years == pytest.approx(1000 / 150)


def test_debt_does_not_change_unlevered_project_cash_flow():
    unlev = run_finance(simple(tax_rate=0.3))
    lev = run_finance(simple(tax_rate=0.3, debt_share=0.7, interest_rate=0.08, tenor_years=8, grace_years=1))
    assert np.allclose(unlev.project_cf, lev.project_cf)
    assert unlev.irr_project == pytest.approx(lev.irr_project)


def test_equity_reconciliation_identity():
    r = run_finance(simple(construction_years=2, tax_rate=0.3, debt_share=0.6, interest_rate=0.09,
                           tenor_years=7, grace_years=2, inflation=0.03, revenue_escalation=0.04,
                           replacements={5: 100.0}))
    lhs = np.array(r.equity_cf)
    rhs = np.array(r.project_cf) + np.array(r.debt_drawdown) - np.array(r.debt_service) + (
        np.array(r.tax_unlevered) - np.array(r.tax_levered))
    assert np.allclose(lhs, rhs)


def test_debt_fully_repaid_and_idc_capitalised():
    r = run_finance(simple(construction_years=2, debt_share=0.5, interest_rate=0.10, tenor_years=6, grace_years=1))
    assert r.idc[1] == pytest.approx(250 * 0.10)  # interest on year-0 drawdown during year 1
    assert r.debt_amount == pytest.approx(500 + 25)
    assert sum(r.principal) == pytest.approx(sum(r.debt_drawdown) + sum(r.idc))
    assert r.debt_balance_end[-1] == pytest.approx(0, abs=1e-6)
    assert r.total_financing_requirement == pytest.approx(1000 + 25)
    # Grace year: interest only.
    first_op = 2
    assert r.principal[first_op] == pytest.approx(0)
    assert r.interest[first_op] == pytest.approx(525 * 0.10)


def test_annuity_debt_service_constant_after_grace():
    r = run_finance(simple(debt_share=0.8, interest_rate=0.07, tenor_years=8, grace_years=0))
    ds = [x for x in r.debt_service if x > 0]
    assert np.allclose(ds, ds[0])
    assert ds[0] == pytest.approx(800 * 0.07 / (1 - 1.07 ** -8))


def test_linear_repayment():
    r = run_finance(simple(debt_share=0.5, interest_rate=0.05, tenor_years=5, repayment="linear"))
    principals = [p for p in r.principal if p > 0]
    assert np.allclose(principals, 100.0)


def test_dscr_and_llcr():
    r = run_finance(simple(debt_share=0.5, interest_rate=0.08, tenor_years=5))
    ds = 500 * 0.08 / (1 - 1.08 ** -5)
    assert r.min_dscr == pytest.approx(150 / ds)
    assert r.avg_dscr == pytest.approx(150 / ds)
    assert r.llcr == pytest.approx(sum(150 / 1.08 ** t for t in range(1, 6)) / 500)


def test_tax_with_depreciation_and_loss_carry_forward():
    r = run_finance(simple(tax_rate=0.25, depreciation_years=5, revenue_year1=100.0, opex_year1=0.0, operating_years=6))
    # Years 1-5: taxable 100-200 = -100 -> losses of 500 accumulated; year 6 taxable 100-500 < 0 -> no tax.
    assert sum(r.tax_unlevered) == pytest.approx(0.0)
    r2 = run_finance(simple(tax_rate=0.25, depreciation_years=2, revenue_year1=300.0, opex_year1=0.0, operating_years=4))
    # Dep 500/yr for 2 years: taxable -200, -200, 300, 300 -> tax in year 3 on (300-400)<0 -> 0, year 4 on (300-100)=200 -> 50
    assert r2.tax_unlevered[3] == pytest.approx(0.0)
    assert r2.tax_unlevered[4] == pytest.approx(50.0)


def test_inflation_and_replacements_nominal():
    r = run_finance(simple(inflation=0.05, replacements={4: 100.0}))
    assert r.opex[1] == pytest.approx(50.0)
    assert r.opex[2] == pytest.approx(52.5)
    assert r.replacements[4] == pytest.approx(100 * 1.05 ** 4)
    assert r.real_discount_rate == pytest.approx(1.10 / 1.05 - 1)


def test_lcoe_consistency():
    r = run_finance(simple())
    costs = np.array(r.capex) + np.array(r.opex) + np.array(r.replacements)
    assert r.lcoe_per_kwh == pytest.approx(levelized_cost(costs, r.energy_kwh, 0.10))
    # Hand check: (1000 + 50 * annuity) / (100 * annuity)
    ann = sum(1.1 ** -t for t in range(1, 11))
    assert r.lcoe_per_kwh == pytest.approx((1000 + 50 * ann) / (100 * ann))


def test_reproducible():
    a = run_finance(simple(debt_share=0.5, tax_rate=0.3, tenor_years=5))
    b = run_finance(simple(debt_share=0.5, tax_rate=0.3, tenor_years=5))
    assert a.model_dump() == b.model_dump()


def test_invalid_debt_terms():
    with pytest.raises(ValueError):
        simple(debt_share=0.5, tenor_years=12)
    with pytest.raises(ValueError):
        simple(debt_share=0.5, tenor_years=5, grace_years=5)


def test_no_irr_when_no_sign_change():
    r = run_finance(simple(revenue_year1=0.0))
    assert r.irr_project is None


def test_structures_responsibilities_complete():
    assert set(STRUCTURES) == {"self_financing", "epc_om", "corporate_ppa", "energy_as_a_service", "equipment_leasing", "developer_owned"}
    for s in STRUCTURES.values():
        assert s.investor and s.operator and len(s.risks) == 6


def test_structure_client_flows_and_break_even_tariff():
    inp = StructureInputs(capex=1000, annual_opex=20, baseline_annual_cost=300, annual_energy_kwh=1000, years=10,
                          discount_rate=0.1, escalation=0.0, ppa_tariff_per_kwh=0.2)
    sf = client_cash_flows("self_financing", inp)
    assert sf["client_cash_flow"][0] == -1000 and sf["annual_savings"][0] == pytest.approx(280)
    ppa = client_cash_flows("corporate_ppa", inp)
    assert ppa["upfront_investment"] == 0 and ppa["annual_savings"][0] == pytest.approx(300 - 200)
    tariff = break_even_ppa_tariff(inp, 0.12)
    dev = developer_cash_flows("corporate_ppa", inp.model_copy(update={"ppa_tariff_per_kwh": tariff}))
    assert dev["investor_irr"] == pytest.approx(0.12, abs=1e-6)
    lease = client_cash_flows("equipment_leasing", inp)
    assert len(lease["annual_payments"]) == 10
