"""Module F - Biomass cogeneration (PRELIMINARY SCREENING).

This module is a preliminary screening tool. Results must be validated with
equipment-specific performance data (boiler/turbine or gasifier/engine curves, fuel analysis)
before any investment decision.

Fuel energy (wet basis):
    LHV_wet [MJ/kg] = LHV_dry * (1 - M) - 2.443 * M      (M = moisture, wet basis)
Electricity is limited by both the fuel available and the installed capacity x operating hours:
    E_fuel_limited = biomass_energy * eta_el
    E_cap_limited  = P_installed * operating_hours * availability
    E_el           = min(E_fuel_limited, E_cap_limited)
Useful heat (CHP) = fuel energy actually burned x eta_th. Electricity and useful heat are always
reported separately; the electricity LCOE carries the full cost unless the user enters a value
for useful heat (heat credit).

Emissions: combustion CO2 from biomass is reported as *biogenic* and kept separate. Treating it
as carbon-neutral is an assumption valid only for sustainably sourced residues.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from src.config import HOURS_PER_YEAR
from src.energy.defaults import default
from src.finance.common import crf

# Indicative dry-basis LHVs for screening only (MJ/kg); replace with laboratory fuel analysis.
INDICATIVE_LHV_DRY = {
    "wood_residues": 18.5,
    "sawdust": 18.5,
    "palm_kernel_shells": 18.0,
    "palm_empty_fruit_bunches": 17.0,
    "rice_husks": 14.0,
    "bagasse": 17.0,
    "other": 16.0,
}
WOOD_BIOGENIC_CO2_KG_PER_GJ = 112.0  # IPCC 2006 default for wood/wood waste (biogenic, reported separately)


class BiomassInputs(BaseModel):
    biomass_type: str = "wood_residues"
    annual_availability_t: float = Field(ge=0, description="Wet tonnes per year available to the plant")
    lhv_dry_mj_per_kg: float = Field(gt=0, lt=30)
    moisture_content: float = Field(ge=0, lt=0.7, description="Wet basis fraction")
    electrical_efficiency: float = Field(gt=0, lt=0.5)
    thermal_efficiency: float = Field(0.0, ge=0, lt=0.9, description="Useful heat recovered (CHP); 0 for power only")
    installed_capacity_kw: float = Field(ge=0)
    annual_operating_hours: float = Field(7000, gt=0, le=HOURS_PER_YEAR)
    availability: float = Field(0.90, gt=0, le=1)
    capex_per_kw: float = Field(0.0, ge=0)
    fixed_opex_per_kw_year: float = Field(0.0, ge=0)
    variable_opex_per_kwh: float = Field(0.0, ge=0)
    fuel_cost_per_t: float = Field(0.0, ge=0, description="Purchase/collection cost per wet tonne")
    fuel_preparation_cost_per_t: float = Field(0.0, ge=0, description="Chipping, drying, handling per wet tonne")
    heat_value_per_kwh_th: float = Field(0.0, ge=0, description="Value of useful heat (avoided fuel); 0 = no credit")
    lifetime_years: float = Field(20, gt=0)
    discount_rate: float = Field(0.10, ge=0, lt=1)
    biogenic_co2_kg_per_gj: float = Field(WOOD_BIOGENIC_CO2_KG_PER_GJ, ge=0)


class BiomassResults(BaseModel):
    lhv_wet_mj_per_kg: float
    fuel_energy_available_kwh: float
    electricity_potential_fuel_limited_kwh: float
    electricity_potential_capacity_limited_kwh: float
    electricity_generation_kwh: float
    limiting_factor: str
    biomass_consumed_t: float
    fuel_energy_used_kwh: float
    useful_heat_kwh_th: float
    capacity_utilization: float
    capex: float
    annual_fuel_cost: float
    annual_opex: float
    annualized_capex: float
    annual_cost: float
    lcoe_per_kwh: float
    lcoe_net_of_heat_per_kwh: float
    biogenic_co2_t: float
    status: str = "PRELIMINARY SCREENING - validate with equipment-specific data"


def lhv_wet(lhv_dry: float, moisture: float) -> float:
    return lhv_dry * (1 - moisture) - default("water_latent_heat_mj_per_kg") * moisture


def calculate_biomass(inputs: BiomassInputs) -> BiomassResults:
    lhv = lhv_wet(inputs.lhv_dry_mj_per_kg, inputs.moisture_content)
    if lhv <= 0:
        raise ValueError("Moisture too high: wet-basis heating value is not positive.")
    fuel_kwh = inputs.annual_availability_t * 1000 * lhv / 3.6
    fuel_limited = fuel_kwh * inputs.electrical_efficiency
    cap_limited = inputs.installed_capacity_kw * inputs.annual_operating_hours * inputs.availability
    generation = min(fuel_limited, cap_limited)
    limiting = "fuel availability" if fuel_limited < cap_limited else "installed capacity / operating hours"
    fuel_used_kwh = generation / inputs.electrical_efficiency
    consumed_t = fuel_used_kwh * 3.6 / lhv / 1000
    heat = fuel_used_kwh * inputs.thermal_efficiency
    capex = inputs.capex_per_kw * inputs.installed_capacity_kw
    fuel_cost = consumed_t * (inputs.fuel_cost_per_t + inputs.fuel_preparation_cost_per_t)
    opex = inputs.fixed_opex_per_kw_year * inputs.installed_capacity_kw + inputs.variable_opex_per_kwh * generation
    ann_capex = capex * crf(inputs.discount_rate, inputs.lifetime_years)
    total = ann_capex + opex + fuel_cost
    lcoe = total / generation if generation > 0 else float("nan")
    heat_credit = heat * inputs.heat_value_per_kwh_th
    return BiomassResults(
        lhv_wet_mj_per_kg=lhv,
        fuel_energy_available_kwh=fuel_kwh,
        electricity_potential_fuel_limited_kwh=fuel_limited,
        electricity_potential_capacity_limited_kwh=cap_limited,
        electricity_generation_kwh=generation,
        limiting_factor=limiting,
        biomass_consumed_t=consumed_t,
        fuel_energy_used_kwh=fuel_used_kwh,
        useful_heat_kwh_th=heat,
        capacity_utilization=generation / (inputs.installed_capacity_kw * HOURS_PER_YEAR) if inputs.installed_capacity_kw else 0.0,
        capex=capex,
        annual_fuel_cost=fuel_cost,
        annual_opex=opex,
        annualized_capex=ann_capex,
        annual_cost=total,
        lcoe_per_kwh=lcoe,
        lcoe_net_of_heat_per_kwh=(total - heat_credit) / generation if generation > 0 else float("nan"),
        biogenic_co2_t=fuel_used_kwh * 3.6e-3 * inputs.biogenic_co2_kg_per_gj / 1000,
    )


def fuel_cost_per_kwh_el(inputs: BiomassInputs) -> float:
    """Marginal fuel + preparation + variable O&M cost per kWh of electricity (for dispatch/optimisation)."""
    lhv = lhv_wet(inputs.lhv_dry_mj_per_kg, inputs.moisture_content)
    t_per_kwh = 3.6 / (inputs.electrical_efficiency * lhv * 1000)
    return t_per_kwh * (inputs.fuel_cost_per_t + inputs.fuel_preparation_cost_per_t) + inputs.variable_opex_per_kwh
