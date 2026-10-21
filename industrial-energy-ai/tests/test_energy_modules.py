"""Unit tests for load profiles, data validation, solar, battery, biomass and grid engines."""

import numpy as np
import pandas as pd
import pytest

from src.energy.battery import BatteryInputs, replacement_years, simulate_battery, summarize_battery
from src.energy.biomass import BiomassInputs, calculate_biomass, lhv_wet
from src.energy.data_validation import check_fuel_consistency, extract_bill_candidates, standardise_hourly_profile
from src.energy.grid import GridInputs, analyse_grid, outage_profile
from src.energy.load_profiles import SECTORS, synthetic_load_profile
from src.energy.solar import PVInputs, resource_from_arrays, simulate_pv, solar_cos_zenith, synthetic_solar_resource

# ---------------------------------------------------------------- load profiles


@pytest.mark.parametrize("sector", sorted(SECTORS))
def test_synthetic_profile_scaled_and_labelled(sector):
    p = synthetic_load_profile(sector, 5_000_000)
    assert p.values_kw.size == 8760
    assert p.annual_kwh == pytest.approx(5_000_000)
    assert p.is_synthetic and "SYNTHETIC" in p.source
    assert np.all(p.values_kw > 0)


def test_synthetic_profile_reproducible():
    a = synthetic_load_profile("cement", 1e6, seed=3).values_kw
    b = synthetic_load_profile("cement", 1e6, seed=3).values_kw
    assert np.array_equal(a, b)


# ---------------------------------------------------------------- data validation


def _hourly_df(values, start="2024-01-01"):
    idx = pd.date_range(start, periods=len(values), freq="h")
    return pd.DataFrame({"timestamp": idx, "kw": values})


def test_full_year_clean_data_is_grade_a():
    vals = 500 + 100 * np.sin(np.arange(8760) / 24 * 2 * np.pi)
    prof, rep = standardise_hourly_profile(_hourly_df(vals, "2023-01-01"), "timestamp", "kw")
    assert prof is not None and not prof.is_synthetic
    assert rep.coverage == pytest.approx(1.0)
    assert rep.quality_score == "A"
    assert prof.annual_kwh == pytest.approx(vals.sum())


def test_leap_year_feb29_removed():
    vals = np.full(8784, 100.0)
    prof, rep = standardise_hourly_profile(_hourly_df(vals, "2024-01-01"), "timestamp", "kw")
    assert prof.values_kw.size == 8760
    assert rep.coverage == pytest.approx(1.0)


def test_detects_missing_negative_duplicates_and_gaps():
    vals = np.full(8760, 200.0)
    df = _hourly_df(vals, "2023-01-01")
    df.loc[10, "kw"] = np.nan
    df.loc[20, "kw"] = -5
    df = pd.concat([df, df.iloc[[30]]])  # duplicate timestamp
    df = df.drop(index=range(1000, 1100))  # 100 h gap
    prof, rep = standardise_hourly_profile(df, "timestamp", "kw")
    codes = rep.codes()
    assert {"missing_values", "negative_consumption", "duplicate_timestamps", "incomplete_year",
            "timestamp_unsorted", "timestamp_irregular"} <= codes
    assert prof is not None
    assert prof.filled_mask.sum() >= 100
    assert np.all(prof.values_kw >= 0)
    assert prof.values_kw[1050] == pytest.approx(200.0)


def test_subhourly_energy_converted_to_power():
    idx = pd.date_range("2023-01-01", periods=8760 * 4, freq="15min")
    df = pd.DataFrame({"t": idx, "kwh": np.full(idx.size, 25.0)})  # 25 kWh per 15 min = 100 kW
    prof, rep = standardise_hourly_profile(df, "t", "kwh", unit="kW", quantity="energy")
    assert prof.values_kw.mean() == pytest.approx(100.0)


def test_unit_error_detected_against_declared_peak():
    vals = np.full(8760, 500_000.0)  # watts entered as kW
    prof, rep = standardise_hourly_profile(_hourly_df(vals, "2023-01-01"), "timestamp", "kw", declared_peak_kw=600)
    assert "unit_suspect" in rep.codes() and rep.has_errors


def test_daily_data_rejected():
    df = pd.DataFrame({"t": pd.date_range("2023-01-01", periods=365, freq="D"), "kw": 10.0})
    prof, rep = standardise_hourly_profile(df, "t", "kw")
    assert prof is None and "resolution_too_coarse" in rep.codes()


def test_fuel_consistency_checks():
    assert check_fuel_consistency(1_000_000, 1_000_000)[0].code == "fuel_conflict"  # 1 L/kWh
    assert check_fuel_consistency(280_000, 1_000_000) == []
    codes = {i.code for i in check_fuel_consistency(None, 10_000_000, 1000)}
    assert "capacity_factor_impossible" in codes


def test_bill_candidates_extraction():
    text = "Consommation : 12 450 kWh\nMontant TTC : 1 234 567 FCFA"
    c = extract_bill_candidates(text)
    assert 12450.0 in c["kwh"] and 1234567.0 in c["amount_xaf"]


# ---------------------------------------------------------------- solar


def test_solar_geometry_no_sun_at_night():
    cosz = solar_cos_zenith(-4.27, 15.28, 1.0)  # Brazzaville
    hours = np.arange(8760) % 24
    assert cosz[hours == 0].max() == 0
    assert cosz[hours == 12].mean() > 0.7


def test_pv_hand_check_constant_irradiance():
    res = resource_from_arrays(np.full(8760, 1000.0), np.full(8760, 25.0 - (45 - 20) / 800 * 1000))  # T_cell = 25 °C
    inputs = PVInputs(capacity_kwp=100, performance_ratio_other=0.9, inverter_efficiency=0.95, dc_ac_ratio=1.0)
    gen, r = simulate_pv(res, inputs)
    assert gen[0] == pytest.approx(100 * 0.9 * 0.95)
    assert r.annual_generation_kwh == pytest.approx(100 * 0.9 * 0.95 * 8760)


def test_pv_temperature_derating_and_clipping():
    res = resource_from_arrays(np.full(8760, 1000.0), np.full(8760, 40.0))
    hot, _ = simulate_pv(res, PVInputs(capacity_kwp=1))
    cold, _ = simulate_pv(resource_from_arrays(np.full(8760, 1000.0), np.full(8760, 0.0)), PVInputs(capacity_kwp=1))
    assert hot[0] < cold[0]
    clipped, _ = simulate_pv(resource_from_arrays(np.full(8760, 1000.0), np.full(8760, 0.0)), PVInputs(capacity_kwp=1, dc_ac_ratio=1.3))
    assert clipped.max() <= 1 / 1.3 + 1e-12


def test_pv_self_consumption_and_curtailment_balance():
    res = synthetic_solar_resource(-4.27, 15.28)
    load = np.full(8760, 50.0)
    gen, r = simulate_pv(res, PVInputs(capacity_kwp=200, capex_per_kwp=500_000, discount_rate=0.1), load)
    assert r.self_consumed_kwh + r.curtailed_kwh == pytest.approx(r.annual_generation_kwh)
    assert 0.08 < r.capacity_factor < 0.25  # plausible range for the illustrative tropical resource
    assert r.lcoe_per_kwh > 0
    assert res.is_synthetic


def test_irradiance_validation():
    with pytest.raises(ValueError):
        resource_from_arrays(np.zeros(100))
    with pytest.raises(ValueError):
        resource_from_arrays(np.full(8760, 2000.0))


# ---------------------------------------------------------------- battery


def _spec(**kw):
    params = dict(energy_capacity_kwh=1000, power_capacity_kw=250, charge_efficiency=0.95, discharge_efficiency=0.95,
                  soc_min=0.1, soc_max=0.9, initial_soc=0.5)
    params.update(kw)
    return BatteryInputs(**params)


def test_battery_constraints_and_energy_conservation():
    rng = np.random.default_rng(0)
    net = rng.normal(0, 300, 8760)
    spec = _spec()
    ch, dis, soc = simulate_battery(np.clip(net, 0, None), np.clip(-net, 0, None), spec)
    assert ch.max() <= 250 + 1e-9 and dis.max() <= 250 + 1e-9
    assert soc.min() >= 100 - 1e-6 and soc.max() <= 900 + 1e-6
    s = summarize_battery(ch, dis, soc, spec)
    assert s.simultaneous_hours == 0
    assert s.max_balance_error_kwh < 1e-9
    # Global conservation: energy in x eta_c - energy out / eta_d = delta SOC
    assert ch.sum() * 0.95 - dis.sum() / 0.95 == pytest.approx(s.soc_change_kwh, abs=1e-6)
    assert s.losses_kwh == pytest.approx(ch.sum() * 0.05 + dis.sum() * (1 / 0.95 - 1))


def test_round_trip_efficiency_split():
    spec = _spec(round_trip_efficiency=0.81)
    assert spec.charge_efficiency == pytest.approx(0.9) and spec.rte == pytest.approx(0.81)


def test_battery_full_charge_then_discharge_hand_case():
    spec = _spec(initial_soc=0.1)
    surplus = np.zeros(10); deficit = np.zeros(10)
    surplus[:5] = 1000  # limited by power 250 kW and headroom 800 kWh
    deficit[5:] = 1000
    ch, dis, soc = simulate_battery(surplus, deficit, spec)
    assert soc[4] == pytest.approx(900)  # 800 kWh stored
    assert ch.sum() == pytest.approx(800 / 0.95)
    assert dis.sum() == pytest.approx(800 * 0.95)
    assert soc[-1] == pytest.approx(100)


def test_invalid_soc_window_rejected():
    with pytest.raises(ValueError):
        _spec(soc_min=0.9, soc_max=0.5)


def test_replacement_schedule():
    assert replacement_years(8, 20) == [8, 16]
    assert replacement_years(float("inf"), 20) == []
    assert replacement_years(25, 20) == []


def test_cycle_driven_replacement():
    spec = _spec(cycle_life_efc=1000, calendar_life_years=15)
    ch = np.zeros(8760); dis = np.zeros(8760)
    dis[:365] = 1000 * 1.0  # 365 EFC/year (nominal 1000 kWh)
    s = summarize_battery(ch, dis, np.full(8760, 500.0), spec)
    assert s.equivalent_full_cycles == pytest.approx(365)
    assert s.replacement_driver == "cycle life"
    assert s.replacement_interval_years == pytest.approx(1000 / 365)


# ---------------------------------------------------------------- biomass


def test_lhv_moisture_correction():
    assert lhv_wet(18.5, 0.0) == pytest.approx(18.5)
    assert lhv_wet(18.5, 0.4) == pytest.approx(18.5 * 0.6 - 2.443 * 0.4)


def test_biomass_fuel_limited_hand_case():
    inp = BiomassInputs(annual_availability_t=10_000, lhv_dry_mj_per_kg=18.0, moisture_content=0.0,
                        electrical_efficiency=0.20, thermal_efficiency=0.5, installed_capacity_kw=5000,
                        annual_operating_hours=8000, availability=1.0, fuel_cost_per_t=5000)
    r = calculate_biomass(inp)
    fuel_kwh = 10_000 * 1000 * 18 / 3.6  # 50 GWh
    assert r.fuel_energy_available_kwh == pytest.approx(fuel_kwh)
    assert r.electricity_generation_kwh == pytest.approx(fuel_kwh * 0.2)  # 10 GWh < 40 GWh capacity-limited
    assert r.limiting_factor == "fuel availability"
    assert r.useful_heat_kwh_th == pytest.approx(fuel_kwh * 0.5)
    assert r.biomass_consumed_t == pytest.approx(10_000)
    assert r.annual_fuel_cost == pytest.approx(50_000_000)


def test_biomass_capacity_limited_and_electricity_separate_from_heat():
    inp = BiomassInputs(annual_availability_t=100_000, lhv_dry_mj_per_kg=18.0, moisture_content=0.3,
                        electrical_efficiency=0.2, thermal_efficiency=0.4, installed_capacity_kw=1000,
                        annual_operating_hours=7000, availability=0.9)
    r = calculate_biomass(inp)
    assert r.electricity_generation_kwh == pytest.approx(1000 * 7000 * 0.9)
    assert r.limiting_factor.startswith("installed capacity")
    assert r.useful_heat_kwh_th == pytest.approx(r.fuel_energy_used_kwh * 0.4)
    assert r.biomass_consumed_t < 100_000


# ---------------------------------------------------------------- grid


def test_outage_profile_matches_availability():
    inp = GridInputs(energy_tariff_per_kwh=100, availability=0.9, average_outage_hours=4)
    avail = outage_profile(inp)
    assert (1 - avail.mean()) == pytest.approx(0.1, abs=1 / 8760)


def test_grid_costs_hand_case():
    load = np.full(8760, 100.0)
    inp = GridInputs(energy_tariff_per_kwh=100, transmission_charge_per_kwh=5, distribution_charge_per_kwh=5,
                     availability=1.0, distance_km=10, line_cost_per_km=1_000_000, connection_fixed_cost=5_000_000,
                     discount_rate=0.0, lifetime_years=10, fixed_charge_per_month=1000)
    r = analyse_grid(inp, load)
    assert r.connection_capex == pytest.approx(15_000_000)
    assert r.annualized_connection_capex == pytest.approx(1_500_000)
    assert r.energy_procurement_cost == pytest.approx(876_000 * 110)
    assert r.backup_energy_kwh == 0
    assert r.annual_total_cost == pytest.approx(1_500_000 + 876_000 * 110 + 12_000)


def test_grid_outages_require_backup():
    load = np.full(8760, 100.0)
    inp = GridInputs(energy_tariff_per_kwh=100, availability=0.8, average_outage_hours=6)
    r = analyse_grid(inp, load, backup_marginal_cost_per_kwh=300)
    assert r.grid_energy_kwh + r.backup_energy_kwh == pytest.approx(load.sum())
    assert r.backup_cost == pytest.approx(r.backup_energy_kwh * 300)
    no_backup = analyse_grid(inp.model_copy(update={"backup_required": False}), load)
    assert no_backup.unserved_without_backup_kwh == pytest.approx(r.backup_energy_kwh)
