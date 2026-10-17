import pytest

from lcoe import crf, lcoe, wacc


def test_crf_matches_closed_form_lcoe():
    # Sans dégradation ni indexation, LCOE = (CAPEX x CRF + OPEX) / E.
    for r in (0.04, 0.08, 0.12):
        expected = (50e6 * crf(r, 25) + 750e3) / 90_000
        assert lcoe(50e6, 750e3, 90_000, r, 25) == pytest.approx(expected)


@pytest.mark.parametrize("rate,expected", [
    (0.04, 43.9), (0.06, 51.8), (0.08, 60.4), (0.10, 69.5), (0.12, 79.2), (0.14, 89.2),
])
def test_proposal_illustrative_table(rate, expected):
    # La proposition affiche 69,6 / 79,3 / 89,3 pour 10 / 12 / 14 % : écart d'arrondi de 0,1.
    assert lcoe(50e6, 750e3, 90_000, rate, 25) == pytest.approx(expected, abs=0.06)


def test_zero_rate():
    assert crf(0, 25) == pytest.approx(1 / 25)


def test_wacc():
    assert wacc(0.7, 0.08, 0.15) == pytest.approx(0.101)
    assert wacc(0.7, 0.08, 0.15, tax_rate=0.25) == pytest.approx(0.087)


from lcoe import (captive_cashflows, diesel_cost_mwh, irr, minigrid_cost_of_service,
                  minigrid_subsidy, npv, simple_payback)


def test_irr_roundtrip():
    flows = [-100, 30, 30, 30, 30, 30]
    assert npv(irr(flows), flows) == pytest.approx(0, abs=1e-6)


def test_diesel_cost():
    # 1,2 USD/l x 0,27 l/kWh = 324 USD/MWh de carburant, + 20 USD/MWh d'O&M.
    assert diesel_cost_mwh(1.2, 0.27, 20) == pytest.approx(344)


def test_captive_payback_and_flows():
    flows = captive_cashflows(1e6, 20e3, 1500, 300, 3)
    assert flows == pytest.approx([-1e6, 430e3, 430e3, 430e3])
    assert simple_payback(1e6, 430e3) == pytest.approx(2.3256, rel=1e-4)
    assert simple_payback(1e6, 0) == float("inf")


def test_minigrid_cost_decomposition_and_subsidy():
    r, n = 0.10, 20
    cos = minigrid_cost_of_service(400e3, 200e3, 15e3, 10e3, 250, 0.2, r, n)
    sold = 200
    assert cos["total"] == pytest.approx(cos["production"] + cos["distribution"] + cos["commercial"])
    assert cos["distribution"] == pytest.approx(200e3 * crf(r, n) / sold)
    sub = minigrid_subsidy(cos["total"], 250, sold, r, n)
    # Avec cette subvention retirée du CAPEX, le coût complet égale le tarif.
    after = minigrid_cost_of_service(400e3 - sub, 200e3, 15e3, 10e3, 250, 0.2, r, n)
    assert after["total"] == pytest.approx(250)
    assert minigrid_subsidy(100, 250, sold, r, n) == 0
