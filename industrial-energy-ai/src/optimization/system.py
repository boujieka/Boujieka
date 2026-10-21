"""System definition shared by the optimiser, the rule-based dispatch simulator and the
financial model: technology parameters, hourly profiles, scenario definitions and the common
result structure (with energy-balance verification).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from pydantic import BaseModel, Field

from src.config import HOURS_PER_YEAR
from src.finance.common import crf

TECHS = ("pv", "battery", "diesel", "biomass", "grid")


class PVTech(BaseModel):
    capex_per_kwp: float = Field(0.0, ge=0)
    opex_per_kwp_year: float = Field(0.0, ge=0)
    lifetime_years: int = Field(25, ge=1)
    min_kwp: float = Field(0.0, ge=0)
    max_kwp: float | None = Field(None, ge=0, description="Roof/land limit; None = unconstrained")
    fixed_kwp: float | None = Field(None, ge=0, description="Force this size (no sizing)")


class BatteryTech(BaseModel):
    capex_per_kwh: float = Field(0.0, ge=0)
    capex_per_kw: float = Field(0.0, ge=0)
    opex_per_kwh_year: float = Field(0.0, ge=0)
    calendar_life_years: float = Field(15.0, gt=0)
    cycle_life_efc: float = Field(6000.0, gt=0)
    charge_efficiency: float = Field(0.95, gt=0, le=1)
    discharge_efficiency: float = Field(0.95, gt=0, le=1)
    soc_min: float = Field(0.10, ge=0, lt=1)
    soc_max: float = Field(0.95, gt=0, le=1)
    min_duration_h: float = Field(0.5, gt=0)
    max_duration_h: float = Field(8.0, gt=0)
    max_kwh: float | None = Field(None, ge=0)
    fixed_kwh: float | None = Field(None, ge=0)
    fixed_kw: float | None = Field(None, ge=0)
    outage_reserve_fraction: float = Field(0.5, ge=0, le=1, description="Rule-based dispatch with grid: share of usable capacity kept for outages and recharged from the grid")

    @property
    def wear_cost_per_kwh(self) -> float:
        """Linear cycle-wear proxy used by the optimiser: capex per kWh / cycle life."""
        return self.capex_per_kwh / self.cycle_life_efc


class DieselTech(BaseModel):
    existing_kw: float = Field(0.0, ge=0)
    unit_size_kw: float | None = Field(None, gt=0, description="Size of one genset; default = existing_kw or 500 kW")
    allow_new_capacity: bool = True
    max_new_kw: float | None = Field(None, ge=0)
    new_capex_per_kw: float = Field(0.0, ge=0)
    fixed_om_per_kw_year: float = Field(0.0, ge=0)
    fuel_price_per_l: float = Field(0.0, ge=0, description="Delivered price incl. transport")
    sfc_l_per_kwh: float = Field(0.28, gt=0)
    variable_om_per_kwh: float = Field(0.0, ge=0)
    lifetime_years: float = Field(15.0, gt=0)
    min_loading: float = Field(0.30, ge=0, lt=1)
    co2_kg_per_l: float = Field(2.68, ge=0)

    @property
    def marginal_cost_per_kwh(self) -> float:
        return self.sfc_l_per_kwh * self.fuel_price_per_l + self.variable_om_per_kwh

    @property
    def unit_kw(self) -> float:
        if self.unit_size_kw:
            return self.unit_size_kw
        return self.existing_kw if self.existing_kw > 0 else 500.0


class BiomassTech(BaseModel):
    capex_per_kw: float = Field(0.0, ge=0)
    fixed_opex_per_kw_year: float = Field(0.0, ge=0)
    marginal_cost_per_kwh: float = Field(0.0, ge=0, description="Fuel + preparation + variable O&M per kWh_e")
    annual_energy_limit_kwh: float = Field(0.0, ge=0, description="Fuel-limited annual electricity")
    availability: float = Field(0.90, gt=0, le=1)
    lifetime_years: float = Field(20.0, gt=0)
    max_kw: float | None = Field(None, ge=0)
    fixed_kw: float | None = Field(None, ge=0)


class GridTech(BaseModel):
    price_per_kwh: float = Field(0.0, ge=0, description="Energy + transmission + distribution")
    demand_charge_per_kw_month: float = Field(0.0, ge=0)
    fixed_cost_per_year: float = Field(0.0, ge=0, description="Fixed charges + line maintenance")
    connection_capex: float = Field(0.0, ge=0)
    lifetime_years: float = Field(25.0, gt=0)
    max_import_kw: float | None = Field(None, gt=0)
    renewable_share: float = Field(0.0, ge=0, le=1)


class Economics(BaseModel):
    discount_rate: float = Field(0.10, ge=0, lt=1)
    project_life_years: int = Field(20, ge=1, le=40)
    value_of_lost_load_per_kwh: float = Field(0.0, ge=0)
    max_unserved_fraction: float = Field(0.001, ge=0, le=1)
    currency: str = "XAF"


class SystemSpec(BaseModel):
    pv: PVTech | None = None
    battery: BatteryTech | None = None
    diesel: DieselTech | None = None
    biomass: BiomassTech | None = None
    grid: GridTech | None = None
    economics: Economics = Economics()


@dataclass
class Profiles:
    load_kw: np.ndarray
    pv_per_kwp: np.ndarray | None = None
    grid_available: np.ndarray | None = None
    load_is_synthetic: bool = True
    solar_is_synthetic: bool = True
    grid_is_synthetic: bool = True

    def __post_init__(self) -> None:
        self.load_kw = np.asarray(self.load_kw, dtype=float)
        n = self.load_kw.size
        for name in ("pv_per_kwp", "grid_available"):
            arr = getattr(self, name)
            if arr is not None:
                arr = np.asarray(arr, dtype=float)
                if arr.size != n:
                    raise ValueError(f"{name} has {arr.size} values; the load has {n}.")
                setattr(self, name, arr)

    @property
    def n(self) -> int:
        return int(self.load_kw.size)

    @property
    def weight(self) -> float:
        """Scaling of simulated hours to a full year (1.0 for an 8,760-hour run)."""
        return HOURS_PER_YEAR / self.n


@dataclass(frozen=True)
class Scenario:
    key: str
    label_fr: str
    label_en: str
    techs: frozenset[str]


SCENARIOS: dict[str, Scenario] = {
    s.key: s
    for s in [
        Scenario("diesel_only", "1. Diesel seul", "1. Diesel only", frozenset({"diesel"})),
        Scenario("pv_diesel", "2. PV + diesel", "2. Solar PV + diesel", frozenset({"pv", "diesel"})),
        Scenario("pv_bess_diesel", "3. PV + batterie + diesel", "3. Solar PV + BESS + diesel", frozenset({"pv", "battery", "diesel"})),
        Scenario("biomass_pv_diesel", "4. Biomasse + PV + diesel", "4. Biomass + solar PV + diesel", frozenset({"biomass", "pv", "diesel"})),
        Scenario("grid_diesel", "5. Réseau + secours diesel", "5. Grid + diesel backup", frozenset({"grid", "diesel"})),
        Scenario("grid_pv_bess", "6. Réseau + PV + batterie", "6. Grid + solar PV + BESS", frozenset({"grid", "pv", "battery"})),
        # Extension beyond the six required scenarios: the usual retrofit option for grid-connected sites.
        Scenario("grid_pv_bess_diesel", "7. Réseau + PV + batterie + secours diesel", "7. Grid + PV + BESS + diesel backup",
                 frozenset({"grid", "pv", "battery", "diesel"})),
    ]
}


def scenario_applicable(scenario: Scenario, spec: SystemSpec, profiles: Profiles) -> tuple[bool, str]:
    for tech in scenario.techs:
        if getattr(spec, tech) is None:
            return False, f"Technology '{tech}' is not configured for this site."
    if "pv" in scenario.techs and profiles.pv_per_kwp is None:
        return False, "No solar profile available."
    if "grid" in scenario.techs and profiles.grid_available is None:
        return False, "No grid availability profile available."
    if "biomass" in scenario.techs and spec.biomass is not None and spec.biomass.annual_energy_limit_kwh <= 0:
        return False, "No biomass resource configured."
    return True, ""


@dataclass
class Capacities:
    pv_kwp: float = 0.0
    battery_kwh: float = 0.0
    battery_kw: float = 0.0
    diesel_existing_kw: float = 0.0
    diesel_new_kw: float = 0.0
    biomass_kw: float = 0.0
    grid_kw: float = 0.0  # import capacity used (contract), informative

    @property
    def diesel_total_kw(self) -> float:
        return self.diesel_existing_kw + self.diesel_new_kw

    def as_dict(self) -> dict[str, float]:
        return {k: float(v) for k, v in self.__dict__.items()}


HOURLY_KEYS = ("load", "pv_available", "pv_used", "pv_curtailed", "charge", "discharge", "soc",
               "diesel", "diesel_excess", "biomass", "grid", "unserved")


@dataclass
class ScenarioResult:
    scenario: str
    method: str  # "LP optimisation" or "rule-based dispatch"
    feasible: bool
    status: str
    message: str
    capacities: Capacities
    hourly: dict[str, np.ndarray] = field(default_factory=dict)
    annual_energy: dict[str, float] = field(default_factory=dict)
    cost_breakdown: dict[str, float] = field(default_factory=dict)
    investment: dict[str, float] = field(default_factory=dict)
    metrics: dict[str, float] = field(default_factory=dict)
    diagnostics: dict[str, float] = field(default_factory=dict)
    replacements: dict[str, float] = field(default_factory=dict)  # replacement interval (years) per tech

    @property
    def total_investment(self) -> float:
        return float(sum(self.investment.values()))

    def to_summary(self) -> dict:
        return {
            "scenario": self.scenario,
            "method": self.method,
            "feasible": self.feasible,
            "status": self.status,
            "message": self.message,
            "capacities": self.capacities.as_dict(),
            "annual_energy": self.annual_energy,
            "cost_breakdown": self.cost_breakdown,
            "investment": self.investment,
            "metrics": self.metrics,
            "diagnostics": self.diagnostics,
            "replacements": self.replacements,
        }


def summarise(
    scenario_key: str,
    method: str,
    status: str,
    capacities: Capacities,
    hourly: dict[str, np.ndarray],
    spec: SystemSpec,
    profiles: Profiles,
    message: str = "",
) -> ScenarioResult:
    """Recompute every reported quantity from the hourly dispatch (single source of truth for
    both the LP and the rule-based simulator) and verify the energy balance."""
    w = profiles.weight
    econ = spec.economics
    r = econ.discount_rate
    techs = SCENARIOS[scenario_key].techs if scenario_key in SCENARIOS else frozenset(TECHS)
    h = {k: np.asarray(hourly.get(k, np.zeros(profiles.n)), dtype=float) for k in HOURLY_KEYS}

    annual = {k: float(h[k].sum() * w) for k in ("load", "pv_available", "pv_used", "pv_curtailed", "charge", "discharge",
                                                  "diesel", "diesel_excess", "biomass", "grid", "unserved")}
    served = annual["load"] - annual["unserved"]

    # Energy balance verification (per hour).
    supply = h["pv_used"] + h["discharge"] + h["diesel"] + h["biomass"] + h["grid"] + h["unserved"]
    demand = h["load"] + h["charge"] + h["diesel_excess"]
    balance_err = float(np.max(np.abs(supply - demand))) if profiles.n else 0.0
    pv_split_err = float(np.max(np.abs(h["pv_used"] + h["pv_curtailed"] - h["pv_available"]))) if profiles.n else 0.0

    cost: dict[str, float] = {}
    invest: dict[str, float] = {}
    repl: dict[str, float] = {}
    if capacities.pv_kwp > 0 and spec.pv:
        invest["pv"] = capacities.pv_kwp * spec.pv.capex_per_kwp
        cost["pv_capital"] = invest["pv"] * crf(r, spec.pv.lifetime_years)
        cost["pv_om"] = capacities.pv_kwp * spec.pv.opex_per_kwp_year
        repl["pv"] = float(spec.pv.lifetime_years)
    batt_diag = {}
    if capacities.battery_kwh > 0 and spec.battery:
        b = spec.battery
        invest["battery"] = capacities.battery_kwh * b.capex_per_kwh + capacities.battery_kw * b.capex_per_kw
        efc = annual["discharge"] / capacities.battery_kwh
        life = min(b.calendar_life_years, b.cycle_life_efc / efc if efc > 0 else math.inf)
        repl["battery"] = float(life)
        cost["battery_capital"] = invest["battery"] * crf(r, life)
        cost["battery_om"] = capacities.battery_kwh * b.opex_per_kwh_year
        prev = np.concatenate(([h["soc"][-1]], h["soc"][:-1]))  # cyclic
        soc_res = h["soc"] - (prev + h["charge"] * b.charge_efficiency - h["discharge"] / b.discharge_efficiency)
        batt_diag = {
            "battery_soc_residual_kwh": float(np.max(np.abs(soc_res))),
            "battery_efc_per_year": float(efc),
            "battery_simultaneous_hours": float(np.sum((h["charge"] > 1e-3) & (h["discharge"] > 1e-3))),
            "battery_soc_min_violation_kwh": float(max(0.0, np.max(b.soc_min * capacities.battery_kwh - h["soc"]))),
            "battery_soc_max_violation_kwh": float(max(0.0, np.max(h["soc"] - b.soc_max * capacities.battery_kwh))),
            "battery_losses_kwh": float(annual["charge"] * (1 - b.charge_efficiency) + annual["discharge"] * (1 / b.discharge_efficiency - 1)),
        }
    fuel_l = 0.0
    if "diesel" in techs and spec.diesel:
        d = spec.diesel
        diesel_out = annual["diesel"]  # total generator output, including any dumped excess
        fuel_l = diesel_out * d.sfc_l_per_kwh
        cost["diesel_fuel"] = fuel_l * d.fuel_price_per_l
        cost["diesel_variable_om"] = diesel_out * d.variable_om_per_kwh
        cost["diesel_fixed_om"] = capacities.diesel_total_kw * d.fixed_om_per_kw_year
        if capacities.diesel_new_kw > 0:
            invest["diesel_new"] = capacities.diesel_new_kw * d.new_capex_per_kw
            cost["diesel_new_capital"] = invest["diesel_new"] * crf(r, d.lifetime_years)
            repl["diesel"] = float(d.lifetime_years)
        unit = d.unit_kw
        units_on = np.where(h["diesel"] > 1e-6, np.ceil(h["diesel"] / unit - 1e-9), 0)
        below = (h["diesel"] > 1e-6) & (h["diesel"] < d.min_loading * units_on * unit - 1e-6)
        batt_diag["diesel_hours_below_min_loading"] = float(np.sum(below))
        batt_diag["diesel_running_hours"] = float(np.sum(h["diesel"] > 1e-6) * w)
    if capacities.biomass_kw > 0 and spec.biomass:
        bm = spec.biomass
        invest["biomass"] = capacities.biomass_kw * bm.capex_per_kw
        cost["biomass_capital"] = invest["biomass"] * crf(r, bm.lifetime_years)
        cost["biomass_fixed_om"] = capacities.biomass_kw * bm.fixed_opex_per_kw_year
        cost["biomass_fuel_and_variable"] = annual["biomass"] * bm.marginal_cost_per_kwh
        repl["biomass"] = float(bm.lifetime_years)
    if "grid" in techs and spec.grid:
        g = spec.grid
        peak_import = float(h["grid"].max()) if profiles.n else 0.0
        cost["grid_energy"] = annual["grid"] * g.price_per_kwh
        cost["grid_demand_charges"] = peak_import * g.demand_charge_per_kw_month * 12
        cost["grid_fixed"] = g.fixed_cost_per_year
        if g.connection_capex > 0:
            invest["grid_connection"] = g.connection_capex
            cost["grid_connection_capital"] = g.connection_capex * crf(r, g.lifetime_years)
        capacities.grid_kw = peak_import

    annual_cost = float(sum(cost.values()))
    capital_keys = [k for k in cost if k.endswith("_capital")]
    operating_cost = annual_cost - sum(cost[k] for k in capital_keys)
    # Renewable energy delivered to the load. Charging is attributed to PV first in each hour; the
    # share of battery discharge counted as renewable equals the annual PV share of charging
    # (charging from grid/diesel/biomass is conservatively counted as non-renewable).
    pv_to_charge = np.minimum(h["charge"], h["pv_used"])
    pv_direct = float((h["pv_used"] - pv_to_charge).sum() * w)
    pv_charge_share = float(pv_to_charge.sum() / h["charge"].sum()) if h["charge"].sum() > 0 else 0.0
    renewable = pv_direct + annual["discharge"] * pv_charge_share + annual["biomass"]
    if spec.grid and "grid" in techs:
        renewable += annual["grid"] * spec.grid.renewable_share
    re_share = max(0.0, renewable) / served if served > 0 else 0.0
    annuity = 1 / crf(r, econ.project_life_years)
    metrics = {
        "annual_cost": annual_cost,
        "annual_operating_cost": operating_cost,
        "annual_capital_cost": annual_cost - operating_cost,
        "lcoe_per_kwh": annual_cost / served if served > 0 else float("nan"),
        "lifecycle_cost_pv": annual_cost * annuity,
        "unserved_penalty": annual["unserved"] * econ.value_of_lost_load_per_kwh,
        "renewable_share": re_share,
        "unserved_fraction": annual["unserved"] / annual["load"] if annual["load"] > 0 else 0.0,
        "fuel_l": fuel_l,
        "co2_t": fuel_l * (spec.diesel.co2_kg_per_l if spec.diesel else 0.0) / 1000.0,
        "served_kwh": served,
        "pv_curtailment_share": annual["pv_curtailed"] / annual["pv_available"] if annual["pv_available"] > 0 else 0.0,
        "total_investment": float(sum(invest.values())),
    }
    diagnostics = {"max_energy_balance_error_kw": balance_err, "max_pv_split_error_kw": pv_split_err, **batt_diag}
    feasible = status.lower().startswith("optimal") or status.lower() == "simulated"
    return ScenarioResult(
        scenario=scenario_key,
        method=method,
        feasible=feasible,
        status=status,
        message=message,
        capacities=capacities,
        hourly=h,
        annual_energy=annual,
        cost_breakdown=cost,
        investment=invest,
        metrics=metrics,
        diagnostics=diagnostics,
        replacements=repl,
    )
