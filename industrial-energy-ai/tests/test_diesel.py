import numpy as np
import pytest

from src.energy.diesel import DieselInputs, FuelCurve, calculate_diesel
from src.finance.common import crf


def base_inputs(**overrides):
    params = dict(
        installed_capacity_kw=1000,
        n_units=2,
        annual_generation_kwh=4_000_000,
        specific_fuel_consumption_l_per_kwh=0.30,
        fuel_price_per_l=700,
        fuel_transport_per_l=50,
        variable_om_per_kwh=10,
        fixed_om_per_year=20_000_000,
        overhaul_cost=30_000_000,
        overhaul_interval_hours=20_000,
        replacement_capex_per_kw=500_000,
        lifetime_years=15,
        discount_rate=0.10,
        operating_hours_per_year=8760,
    )
    params.update(overrides)
    return DieselInputs(**params)


def test_hand_calculated_costs():
    r = calculate_diesel(base_inputs())
    assert r.annual_fuel_l == pytest.approx(1_200_000)
    assert r.fuel_cost == pytest.approx(840_000_000)
    assert r.fuel_transport_cost == pytest.approx(60_000_000)
    assert r.variable_om_cost == pytest.approx(40_000_000)
    assert r.overhaul_cost_annual == pytest.approx(30_000_000 * 8760 / 20_000)
    expected_operating = 840e6 + 60e6 + 40e6 + 20e6 + 13.14e6
    assert r.existing_operating_cost == pytest.approx(expected_operating)
    expected_charge = 500e6 * crf(0.10, 15)
    assert r.annual_capital_charge == pytest.approx(expected_charge)
    assert r.full_economic_cost == pytest.approx(expected_operating + expected_charge)
    assert r.operating_cost_per_kwh == pytest.approx(expected_operating / 4e6)


def test_three_cost_notions_are_ordered_and_lcoe_equals_economic_without_escalation():
    r = calculate_diesel(base_inputs())
    assert r.operating_cost_per_kwh < r.economic_cost_per_kwh
    assert r.lcoe_per_kwh == pytest.approx(r.economic_cost_per_kwh, rel=1e-9)


def test_fuel_escalation_raises_lcoe_above_economic_cost():
    r = calculate_diesel(base_inputs(fuel_escalation=0.05))
    assert r.lcoe_per_kwh > r.economic_cost_per_kwh


def test_crf_known_value():
    assert crf(0.10, 15) == pytest.approx(0.1314738, rel=1e-6)
    assert crf(0.0, 10) == pytest.approx(0.1)


def test_efficiency_based_sfc():
    r = calculate_diesel(base_inputs(specific_fuel_consumption_l_per_kwh=None, generator_efficiency=0.35, fuel_lhv_mj_per_l=35.9))
    assert r.average_sfc_l_per_kwh == pytest.approx(3.6 / (0.35 * 35.9))


def test_capacity_factor_and_emissions():
    r = calculate_diesel(base_inputs())
    assert r.capacity_factor == pytest.approx(4e6 / (1000 * 8760))
    assert r.co2_tonnes == pytest.approx(1_200_000 * 2.68 / 1000)


def test_generation_above_available_energy_is_rejected():
    with pytest.raises(ValueError, match="exceeds the available energy"):
        calculate_diesel(base_inputs(annual_generation_kwh=9_000_000, availability=0.95))


def test_missing_fuel_basis_rejected():
    with pytest.raises(ValueError):
        DieselInputs(installed_capacity_kw=100, annual_generation_kwh=1, fuel_price_per_l=1)


def test_negative_inputs_rejected():
    with pytest.raises(ValueError):
        base_inputs(fuel_price_per_l=-1)


def test_hourly_fuel_curve_and_unit_commitment():
    inputs = base_inputs(fuel_curve=FuelCurve(no_load_l_per_h_per_kw=0.08, marginal_l_per_kwh=0.25))
    dispatch = np.full(8760, 600.0)  # needs both 500 kW units online
    r = calculate_diesel(inputs, dispatch)
    assert r.annual_generation_kwh == pytest.approx(600 * 8760)
    assert r.annual_fuel_l == pytest.approx((0.08 * 1000 + 0.25 * 600) * 8760)
    assert r.warnings == []


def test_min_loading_violation_detected_hourly():
    inputs = base_inputs(fuel_curve=FuelCurve(no_load_l_per_h_per_kw=0.08, marginal_l_per_kwh=0.25))
    dispatch = np.zeros(8760)
    dispatch[:100] = 100.0  # one 500 kW unit at 20 % < 30 % minimum
    r = calculate_diesel(inputs, dispatch)
    assert any("100 h below the minimum loading" in w for w in r.warnings)
    assert r.operating_hours == 100


def test_dispatch_above_capacity_rejected():
    with pytest.raises(ValueError):
        calculate_diesel(base_inputs(), np.full(8760, 1500.0))


def test_part_load_curve_raises_average_sfc():
    curve = FuelCurve(no_load_l_per_h_per_kw=0.08, marginal_l_per_kwh=0.25)
    high = calculate_diesel(base_inputs(fuel_curve=curve), np.full(8760, 950.0))
    low = calculate_diesel(base_inputs(fuel_curve=curve), np.full(8760, 400.0))
    assert low.average_sfc_l_per_kwh > high.average_sfc_l_per_kwh
