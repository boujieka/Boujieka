"""Editable project assumptions (one JSON document per industrial site).

Every engine input a user can change lives here, grouped by module. Default values are generic
screening placeholders for *synthetic demonstration* and must be replaced with site data,
quotations and contract terms. Monetary values are in the project currency (XAF by default)
unless a field says otherwise.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class SiteData(BaseModel):
    latitude: float = Field(-4.27, ge=-90, le=90)
    longitude: float = Field(15.28, ge=-180, le=180)
    utc_offset_h: float = 1.0
    annual_consumption_kwh: float = Field(5_000_000, gt=0)
    declared_peak_kw: float | None = Field(None, gt=0)
    load_seed: int = 42


class DieselAssumptions(BaseModel):
    existing_kw: float = Field(1500, ge=0)
    n_units: int = Field(3, ge=1)
    sfc_l_per_kwh: float = Field(0.28, gt=0)
    fuel_price_per_l: float = Field(700, ge=0)
    fuel_transport_per_l: float = Field(0, ge=0)
    variable_om_per_kwh: float = Field(10, ge=0)
    fixed_om_per_year: float = Field(0, ge=0)
    overhaul_cost: float = Field(0, ge=0)
    overhaul_interval_hours: float = Field(20000, gt=0)
    replacement_capex_per_kw: float = Field(300_000, ge=0)
    new_capex_per_kw: float = Field(300_000, ge=0)
    allow_new_capacity: bool = True
    lifetime_years: float = Field(15, gt=0)
    availability: float = Field(0.95, gt=0, le=1)
    min_loading: float = Field(0.30, ge=0, lt=1)
    co2_kg_per_l: float = Field(2.68, ge=0)


class PVAssumptions(BaseModel):
    enabled: bool = True
    capex_per_kwp: float = Field(450_000, ge=0)
    opex_per_kwp_year: float = Field(6_000, ge=0)
    lifetime_years: int = Field(25, ge=1)
    max_kwp: float | None = Field(None, ge=0)
    performance_ratio_other: float = Field(0.88, gt=0, le=1)
    temp_coeff_per_c: float = Field(-0.004, le=0)
    inverter_efficiency: float = Field(0.97, gt=0, le=1)
    degradation_per_year: float = Field(0.005, ge=0)
    monthly_clearness: list[float] = Field(default_factory=lambda: [0.62, 0.64, 0.63, 0.62, 0.60, 0.55, 0.50, 0.50, 0.55, 0.58, 0.60, 0.61])
    resource_seed: int = 7


class BatteryAssumptions(BaseModel):
    enabled: bool = True
    capex_per_kwh: float = Field(220_000, ge=0)
    capex_per_kw: float = Field(60_000, ge=0)
    opex_per_kwh_year: float = Field(2_000, ge=0)
    calendar_life_years: float = Field(15, gt=0)
    cycle_life_efc: float = Field(6000, gt=0)
    charge_efficiency: float = Field(0.95, gt=0, le=1)
    discharge_efficiency: float = Field(0.95, gt=0, le=1)
    soc_min: float = Field(0.10, ge=0, lt=1)
    soc_max: float = Field(0.95, gt=0, le=1)
    max_kwh: float | None = Field(None, ge=0)
    replacement_cost_factor: float = Field(1.0, ge=0, description="Replacement cost / initial cost (real terms)")
    outage_reserve_fraction: float = Field(0.5, ge=0, le=1, description="Grid sites: usable capacity reserved for outages")


class BiomassAssumptions(BaseModel):
    enabled: bool = False
    biomass_type: str = "wood_residues"
    annual_availability_t: float = Field(0, ge=0)
    lhv_dry_mj_per_kg: float = Field(18.5, gt=0)
    moisture_content: float = Field(0.40, ge=0, lt=0.7)
    electrical_efficiency: float = Field(0.18, gt=0, lt=0.5)
    thermal_efficiency: float = Field(0.45, ge=0, lt=0.9)
    capex_per_kw: float = Field(2_200_000, ge=0)
    fixed_opex_per_kw_year: float = Field(70_000, ge=0)
    variable_opex_per_kwh: float = Field(15, ge=0)
    fuel_cost_per_t: float = Field(3_000, ge=0)
    fuel_preparation_cost_per_t: float = Field(2_000, ge=0)
    annual_operating_hours: float = Field(7000, gt=0, le=8760)
    availability: float = Field(0.85, gt=0, le=1)
    max_kw: float | None = Field(None, ge=0)
    heat_value_per_kwh_th: float = Field(0, ge=0)
    lifetime_years: float = Field(20, gt=0)


class GridAssumptions(BaseModel):
    enabled: bool = False
    existing_connection: bool = False
    distance_km: float = Field(0, ge=0)
    voltage_level: str = "MV"
    connection_fixed_cost: float = Field(0, ge=0)
    line_cost_per_km: float = Field(0, ge=0)
    energy_tariff_per_kwh: float = Field(0, ge=0)
    transmission_charge_per_kwh: float = Field(0, ge=0)
    distribution_charge_per_kwh: float = Field(0, ge=0)
    demand_charge_per_kw_month: float = Field(0, ge=0)
    fixed_charge_per_month: float = Field(0, ge=0)
    maintenance_cost_per_year: float = Field(0, ge=0)
    availability: float = Field(0.85, gt=0, le=1)
    average_outage_hours: float = Field(4, gt=0)
    max_import_kw: float | None = Field(None, gt=0)
    renewable_share: float = Field(0.0, ge=0, le=1)
    outage_seed: int = 11


class ReliabilityAssumptions(BaseModel):
    value_of_lost_load_per_kwh: float = Field(2_000, ge=0)
    max_unserved_fraction: float = Field(0.001, ge=0, le=1)


class FinanceAssumptions(BaseModel):
    discount_rate: float = Field(0.10, ge=0, lt=1)
    equity_discount_rate: float | None = Field(0.14, ge=0, lt=1)
    project_life_years: int = Field(20, ge=1, le=40)
    construction_years: int = Field(1, ge=1, le=5)
    inflation: float = Field(0.03, ge=-0.5, lt=1)
    energy_cost_escalation: float = Field(0.03, ge=-0.5, lt=1, description="Escalation of the avoided baseline cost")
    tax_rate: float = Field(0.28, ge=0, lt=1)
    depreciation_years: int = Field(10, ge=1)
    debt_share: float = Field(0.60, ge=0, le=0.95)
    interest_rate: float = Field(0.08, ge=0, lt=1)
    tenor_years: int = Field(8, ge=1)
    grace_years: int = Field(1, ge=0)
    repayment: Literal["annuity", "linear"] = "annuity"
    structure: str = "self_financing"
    equipment_currency: Literal["XAF", "EUR", "USD"] = "XAF"
    equipment_cost_share: float = Field(0.0, ge=0, le=1, description="Share of CAPEX priced in equipment_currency (for FX sensitivity)")
    ppa_tariff_per_kwh: float = Field(0, ge=0)
    eaas_fee_per_year: float = Field(0, ge=0)
    om_fee_per_year: float = Field(0, ge=0)
    lease_rate: float = Field(0.10, ge=0, lt=1)
    lease_term_years: int = Field(7, ge=1)


class ProjectAssumptions(BaseModel):
    currency: Literal["XAF", "EUR", "USD"] = "XAF"
    baseline_scenario: Literal["diesel_only", "grid_diesel"] = "diesel_only"
    site: SiteData = SiteData()
    diesel: DieselAssumptions = DieselAssumptions()
    pv: PVAssumptions = PVAssumptions()
    battery: BatteryAssumptions = BatteryAssumptions()
    biomass: BiomassAssumptions = BiomassAssumptions()
    grid: GridAssumptions = GridAssumptions()
    reliability: ReliabilityAssumptions = ReliabilityAssumptions()
    finance: FinanceAssumptions = FinanceAssumptions()
    is_synthetic: bool = True
    notes: str = ""
