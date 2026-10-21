"""Study pipeline: turns a project's assumptions into engine inputs and runs the engines.

Data flow (all deterministic and reproducible from the stored assumptions):

    assumptions + load profile + solar resource
        -> Module C diesel baseline (existing fleet, hourly)
        -> SystemSpec + Profiles
        -> baseline scenario (rule-based dispatch of the EXISTING system, no new investment)
        -> LP optimisation per scenario (sizing + dispatch)
        -> rule-based verification of each optimised configuration (min loading, unit commitment)
        -> financial model on the verified configuration vs the baseline

The verified (rule-based) results are the ones used for finance, sensitivity and reports, so
that operating constraints the LP cannot represent are reflected in the reported numbers.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field

import numpy as np

from src.assumptions import ProjectAssumptions
from src.energy.battery import replacement_years
from src.energy.biomass import BiomassInputs, calculate_biomass, fuel_cost_per_kwh_el
from src.energy.diesel import DieselInputs, DieselResults, calculate_diesel
from src.energy.grid import GridInputs, outage_profile
from src.energy.load_profiles import LoadProfile, synthetic_load_profile
from src.energy.solar import PVInputs, SolarResource, pv_output_per_kwp, synthetic_solar_resource
from src.finance.cashflow import FinanceInputs, FinanceResults, run_finance
from src.finance.structures import STRUCTURES, StructureInputs, client_cash_flows, developer_cash_flows
from src.optimization.dispatch import simulate_dispatch
from src.optimization.optimizer import optimise_scenario, recommend
from src.optimization.system import (
    SCENARIOS,
    BatteryTech,
    BiomassTech,
    Capacities,
    DieselTech,
    Economics,
    GridTech,
    Profiles,
    PVTech,
    ScenarioResult,
    SystemSpec,
)

log = logging.getLogger(__name__)


# ------------------------------------------------------------------------------ inputs

def build_load_profile(a: ProjectAssumptions, sector: str, stored: dict | None = None) -> LoadProfile:
    if stored:
        return LoadProfile.from_dict(stored)
    return synthetic_load_profile(sector, a.site.annual_consumption_kwh, seed=a.site.load_seed)


def build_solar_resource(a: ProjectAssumptions, stored: dict | None = None) -> SolarResource:
    if stored:
        return SolarResource(np.asarray(stored["ghi_w_m2"], float), np.asarray(stored["ambient_c"], float),
                             bool(stored.get("is_synthetic", False)), stored.get("source", "stored"), stored.get("assumptions", []))
    return synthetic_solar_resource(a.site.latitude, a.site.longitude, a.site.utc_offset_h,
                                    tuple(a.pv.monthly_clearness), seed=a.pv.resource_seed)


def pv_inputs(a: ProjectAssumptions, capacity_kwp: float = 1.0) -> PVInputs:
    return PVInputs(capacity_kwp=capacity_kwp, performance_ratio_other=a.pv.performance_ratio_other,
                    temp_coeff_per_c=a.pv.temp_coeff_per_c, inverter_efficiency=a.pv.inverter_efficiency,
                    degradation_per_year=a.pv.degradation_per_year, capex_per_kwp=a.pv.capex_per_kwp,
                    opex_per_kwp_year=a.pv.opex_per_kwp_year, lifetime_years=a.pv.lifetime_years,
                    discount_rate=a.finance.discount_rate)


def diesel_inputs(a: ProjectAssumptions) -> DieselInputs:
    d = a.diesel
    return DieselInputs(
        installed_capacity_kw=max(d.existing_kw, 1e-6), n_units=d.n_units, annual_generation_kwh=0.0,
        specific_fuel_consumption_l_per_kwh=d.sfc_l_per_kwh, fuel_price_per_l=d.fuel_price_per_l,
        fuel_transport_per_l=d.fuel_transport_per_l, variable_om_per_kwh=d.variable_om_per_kwh,
        fixed_om_per_year=d.fixed_om_per_year, overhaul_cost=d.overhaul_cost, overhaul_interval_hours=d.overhaul_interval_hours,
        replacement_capex_per_kw=d.replacement_capex_per_kw, lifetime_years=d.lifetime_years,
        discount_rate=a.finance.discount_rate, availability=d.availability, min_loading_fraction=d.min_loading,
        co2_kg_per_l=d.co2_kg_per_l, currency=a.currency,
    )


def diesel_baseline(a: ProjectAssumptions, load_kw: np.ndarray, dispatch_kw: np.ndarray | None = None) -> tuple[DieselResults, float]:
    """Module C on the existing fleet. Returns (results, unserved kWh when the fleet cannot meet the load)."""
    inp = diesel_inputs(a)
    dispatch = np.minimum(load_kw, a.diesel.existing_kw) if dispatch_kw is None else dispatch_kw
    unserved = float((load_kw - dispatch).clip(min=0).sum()) if dispatch_kw is None else 0.0
    gen = float(dispatch.sum())
    max_energy = a.diesel.existing_kw * a.diesel.availability * 8760
    if gen > max_energy:
        # Availability limits annual energy; report rather than fail.
        inp = inp.model_copy(update={"availability": min(1.0, gen / (a.diesel.existing_kw * 8760) + 1e-9)})
    return calculate_diesel(inp, dispatch), unserved


def biomass_inputs(a: ProjectAssumptions, capacity_kw: float) -> BiomassInputs:
    b = a.biomass
    return BiomassInputs(biomass_type=b.biomass_type, annual_availability_t=b.annual_availability_t, lhv_dry_mj_per_kg=b.lhv_dry_mj_per_kg,
                         moisture_content=b.moisture_content, electrical_efficiency=b.electrical_efficiency,
                         thermal_efficiency=b.thermal_efficiency, installed_capacity_kw=capacity_kw,
                         annual_operating_hours=b.annual_operating_hours, availability=b.availability, capex_per_kw=b.capex_per_kw,
                         fixed_opex_per_kw_year=b.fixed_opex_per_kw_year, variable_opex_per_kwh=b.variable_opex_per_kwh,
                         fuel_cost_per_t=b.fuel_cost_per_t, fuel_preparation_cost_per_t=b.fuel_preparation_cost_per_t,
                         heat_value_per_kwh_th=b.heat_value_per_kwh_th, lifetime_years=b.lifetime_years,
                         discount_rate=a.finance.discount_rate)


def grid_inputs(a: ProjectAssumptions) -> GridInputs:
    g = a.grid
    return GridInputs(distance_km=g.distance_km, voltage_level=g.voltage_level,
                      connection_fixed_cost=0 if g.existing_connection else g.connection_fixed_cost,
                      line_cost_per_km=0 if g.existing_connection else g.line_cost_per_km,
                      energy_tariff_per_kwh=g.energy_tariff_per_kwh, transmission_charge_per_kwh=g.transmission_charge_per_kwh,
                      distribution_charge_per_kwh=g.distribution_charge_per_kwh, demand_charge_per_kw_month=g.demand_charge_per_kw_month,
                      fixed_charge_per_month=g.fixed_charge_per_month, max_import_kw=g.max_import_kw, availability=g.availability,
                      average_outage_hours=g.average_outage_hours, maintenance_cost_per_year=g.maintenance_cost_per_year,
                      discount_rate=a.finance.discount_rate, renewable_share=g.renewable_share, outage_seed=g.outage_seed)


@dataclass
class StudyInputs:
    assumptions: ProjectAssumptions
    load: LoadProfile
    solar: SolarResource
    spec: SystemSpec
    profiles: Profiles
    diesel_baseline: DieselResults
    diesel_baseline_unserved_kwh: float
    notes: list[str] = field(default_factory=list)


def build_spec(a: ProjectAssumptions, load_kw: np.ndarray, capex_multiplier: float = 1.0, life_multiplier: float = 1.0) -> tuple[SystemSpec, list[str]]:
    notes: list[str] = []
    d = a.diesel
    base, _ = diesel_baseline(a, load_kw)
    overhaul_per_kwh = base.overhaul_cost_annual / base.annual_generation_kwh if base.annual_generation_kwh > 0 else 0.0
    if overhaul_per_kwh:
        notes.append(f"Diesel overhauls converted to {overhaul_per_kwh:.2f} {a.currency}/kWh using the baseline operating pattern.")
    diesel = DieselTech(
        existing_kw=d.existing_kw, unit_size_kw=(d.existing_kw / d.n_units) if d.existing_kw > 0 else None,
        allow_new_capacity=d.allow_new_capacity, new_capex_per_kw=d.new_capex_per_kw * capex_multiplier,
        fixed_om_per_kw_year=(d.fixed_om_per_year / d.existing_kw) if d.existing_kw > 0 else 0.0,
        fuel_price_per_l=d.fuel_price_per_l + d.fuel_transport_per_l, sfc_l_per_kwh=d.sfc_l_per_kwh,
        variable_om_per_kwh=d.variable_om_per_kwh + overhaul_per_kwh, lifetime_years=d.lifetime_years * life_multiplier,
        min_loading=d.min_loading, co2_kg_per_l=d.co2_kg_per_l,
    )
    pv = PVTech(capex_per_kwp=a.pv.capex_per_kwp * capex_multiplier, opex_per_kwp_year=a.pv.opex_per_kwp_year,
                lifetime_years=max(1, int(round(a.pv.lifetime_years * life_multiplier))), max_kwp=a.pv.max_kwp) if a.pv.enabled else None
    b = a.battery
    battery = BatteryTech(capex_per_kwh=b.capex_per_kwh * capex_multiplier, capex_per_kw=b.capex_per_kw * capex_multiplier,
                          opex_per_kwh_year=b.opex_per_kwh_year, calendar_life_years=b.calendar_life_years * life_multiplier,
                          cycle_life_efc=b.cycle_life_efc, charge_efficiency=b.charge_efficiency, discharge_efficiency=b.discharge_efficiency,
                          soc_min=b.soc_min, soc_max=b.soc_max, max_kwh=b.max_kwh,
                          outage_reserve_fraction=b.outage_reserve_fraction) if b.enabled else None
    biomass = None
    if a.biomass.enabled and a.biomass.annual_availability_t > 0:
        bi = biomass_inputs(a, capacity_kw=1e9)  # capacity-free run gives the fuel-limited potential
        pot = calculate_biomass(bi)
        biomass = BiomassTech(capex_per_kw=a.biomass.capex_per_kw * capex_multiplier, fixed_opex_per_kw_year=a.biomass.fixed_opex_per_kw_year,
                              marginal_cost_per_kwh=fuel_cost_per_kwh_el(bi), annual_energy_limit_kwh=pot.electricity_potential_fuel_limited_kwh,
                              availability=a.biomass.availability, lifetime_years=a.biomass.lifetime_years * life_multiplier, max_kw=a.biomass.max_kw)
    grid = None
    if a.grid.enabled:
        gi = grid_inputs(a)
        grid = GridTech(price_per_kwh=gi.energy_price_per_kwh, demand_charge_per_kw_month=gi.demand_charge_per_kw_month,
                        fixed_cost_per_year=gi.fixed_charge_per_month * 12 + gi.maintenance_cost_per_year,
                        connection_capex=gi.connection_capex, max_import_kw=gi.max_import_kw, renewable_share=gi.renewable_share)
    econ = Economics(discount_rate=a.finance.discount_rate, project_life_years=a.finance.project_life_years,
                     value_of_lost_load_per_kwh=a.reliability.value_of_lost_load_per_kwh,
                     max_unserved_fraction=a.reliability.max_unserved_fraction, currency=a.currency)
    return SystemSpec(pv=pv, battery=battery, diesel=diesel, biomass=biomass, grid=grid, economics=econ), notes


def prepare_study(a: ProjectAssumptions, sector: str, stored_load: dict | None = None, stored_solar: dict | None = None,
                  load_scale: float = 1.0, capex_multiplier: float = 1.0, life_multiplier: float = 1.0) -> StudyInputs:
    load = build_load_profile(a, sector, stored_load)
    if load_scale != 1.0:
        load = LoadProfile(load.values_kw * load_scale, load.is_synthetic, load.source, load.assumptions + [f"Scaled x{load_scale:g}"], load.filled_mask)
    solar = build_solar_resource(a, stored_solar)
    spec, notes = build_spec(a, load.values_kw, capex_multiplier, life_multiplier)
    k = pv_output_per_kwp(solar, pv_inputs(a)) if a.pv.enabled else None
    grid_av = outage_profile(grid_inputs(a)) if a.grid.enabled else None
    profiles = Profiles(load.values_kw, k, grid_av, load.is_synthetic, solar.is_synthetic, True)
    base, unserved = diesel_baseline(a, load.values_kw)
    if unserved > 0:
        notes.append(f"Existing diesel capacity cannot meet the peak load: {unserved:,.0f} kWh/yr would be unserved with diesel alone.")
    return StudyInputs(a, load, solar, spec, profiles, base, unserved, notes)


# ------------------------------------------------------------------------------ runs

def existing_capacities(a: ProjectAssumptions) -> Capacities:
    return Capacities(diesel_existing_kw=a.diesel.existing_kw)


def run_baseline(study: StudyInputs) -> ScenarioResult:
    a = study.assumptions
    return simulate_dispatch(a.baseline_scenario, existing_capacities(a), study.spec, study.profiles)


def run_scenarios(study: StudyInputs, keys: list[str] | None = None, time_limit: int = 300) -> dict[str, dict[str, ScenarioResult]]:
    out: dict[str, dict[str, ScenarioResult]] = {}
    for key in keys or list(SCENARIOS):
        lp = optimise_scenario(key, study.spec, study.profiles, time_limit)
        check = simulate_dispatch(key, lp.capacities, study.spec, study.profiles) if lp.feasible else lp
        out[key] = {"lp": lp, "check": check}
    return out


def recommended_scenario(results: dict[str, dict[str, ScenarioResult]], max_unserved_fraction: float) -> str | None:
    return recommend({k: v["check"] for k, v in results.items()}, max_unserved_fraction)


def replacement_schedule(a: ProjectAssumptions, result: ScenarioResult) -> dict[int, float]:
    """Operating year -> replacement cost (year-0 money) within the project life."""
    life = a.finance.project_life_years
    sched: dict[int, float] = {}
    for tech, interval in result.replacements.items():
        cost_key = {"diesel": "diesel_new"}.get(tech, tech)
        base_cost = result.investment.get(cost_key, 0.0)
        if tech == "battery":
            base_cost *= a.battery.replacement_cost_factor
        for y in replacement_years(interval, life):
            sched[y] = sched.get(y, 0.0) + base_cost
    return sched


def finance_inputs(a: ProjectAssumptions, result: ScenarioResult, baseline: ScenarioResult, capex_multiplier: float = 1.0) -> FinanceInputs:
    f = a.finance
    return FinanceInputs(
        capex=result.total_investment, construction_years=f.construction_years, operating_years=f.project_life_years,
        revenue_year1=baseline.metrics["annual_operating_cost"], opex_year1=result.metrics["annual_operating_cost"],
        revenue_escalation=f.energy_cost_escalation, inflation=f.inflation, replacements=replacement_schedule(a, result),
        energy_year1_kwh=result.metrics["served_kwh"], tax_rate=f.tax_rate, depreciation_years=f.depreciation_years,
        debt_share=f.debt_share, interest_rate=f.interest_rate, tenor_years=min(f.tenor_years, f.project_life_years),
        grace_years=min(f.grace_years, max(0, min(f.tenor_years, f.project_life_years) - 1)), repayment=f.repayment,
        discount_rate=f.discount_rate, equity_discount_rate=f.equity_discount_rate, currency=a.currency,
    )


def financial_analysis(a: ProjectAssumptions, result: ScenarioResult, baseline: ScenarioResult) -> FinanceResults:
    return run_finance(finance_inputs(a, result, baseline))


def structure_comparison(a: ProjectAssumptions, result: ScenarioResult, baseline: ScenarioResult) -> list[dict]:
    f = a.finance
    inp = StructureInputs(
        capex=result.total_investment, annual_opex=result.metrics["annual_operating_cost"],
        baseline_annual_cost=baseline.metrics["annual_operating_cost"], annual_energy_kwh=max(result.metrics["served_kwh"], 1.0),
        years=f.project_life_years, discount_rate=f.discount_rate, escalation=f.inflation, om_fee_per_year=f.om_fee_per_year,
        ppa_tariff_per_kwh=f.ppa_tariff_per_kwh, eaas_fee_per_year=f.eaas_fee_per_year, lease_rate=f.lease_rate,
        lease_term_years=min(f.lease_term_years, f.project_life_years),
    )
    rows = []
    for key, s in STRUCTURES.items():
        client = client_cash_flows(key, inp)
        dev = developer_cash_flows(key, inp)
        needs_terms = (key in ("corporate_ppa", "developer_owned") and f.ppa_tariff_per_kwh <= 0) or (key == "energy_as_a_service" and f.eaas_fee_per_year <= 0)
        rows.append({
            "key": key, "label_fr": s.label_fr, "label_en": s.label_en, "investor": s.investor, "operator": s.operator,
            "risks": s.risks, "payment_basis": s.payment_basis,
            "client_npv": None if needs_terms else client["client_npv"],
            "client_upfront": client["upfront_investment"],
            "investor_irr": None if (dev is None or needs_terms) else dev["investor_irr"],
            "terms_missing": needs_terms,
        })
    return rows


def key_metrics(fin: FinanceResults, result: ScenarioResult, baseline: ScenarioResult) -> dict[str, float | None]:
    return {
        "npv_project": fin.npv_project,
        "irr_project": fin.irr_project,
        "irr_equity": fin.irr_equity,
        "lcoe_per_kwh": fin.lcoe_per_kwh,
        "min_dscr": fin.min_dscr,
        "payback_years": fin.payback_years,
        "annual_savings": baseline.metrics["annual_operating_cost"] - result.metrics["annual_operating_cost"],
        "investment": result.total_investment,
        "fuel_savings_l": baseline.metrics["fuel_l"] - result.metrics["fuel_l"],
        "renewable_share": result.metrics["renewable_share"],
    }


def is_finite(x) -> bool:
    return x is not None and isinstance(x, (int, float)) and math.isfinite(x)
