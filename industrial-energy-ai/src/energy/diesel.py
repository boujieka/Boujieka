"""Module C - Diesel generation cost engine.

Three cost notions are kept strictly separate:

1. **Existing operating cost** - the cash cost of running the current fleet for one year:
   delivered fuel (price + transport) + variable maintenance + fixed O&M + overhauls pro-rated
   by running hours. Sunk capital is excluded. This is the baseline an alternative must beat
   when the generators are already paid for.
2. **Full economic cost** - operating cost + an annual capital charge on the replacement value
   of the fleet (capital recovery factor over the generator lifetime). This is the cost of
   *keeping* a diesel solution over the long run.
3. **Levelized generation cost (LCOE)** - present value of capital + all operating costs over the
   lifetime, with fuel and O&M escalation, divided by the present value of generation.
   With zero escalation it equals the full economic cost per kWh.

Fuel use is computed either from an average specific fuel consumption (SFC), from an electrical
efficiency and the fuel heating value, or - when an hourly dispatch profile is supplied - from a
linear fuel curve ``fuel[l/h] = a * P_online + b * P_out`` (the usual no-load + marginal form).
"""

from __future__ import annotations

import logging
import math

import numpy as np
from pydantic import BaseModel, Field, model_validator

from src.config import HOURS_PER_YEAR
from src.energy.defaults import default
from src.finance.common import crf, present_value

log = logging.getLogger(__name__)


class FuelCurve(BaseModel):
    """Linear fuel curve per unit: fuel (L/h) = no_load_l_per_h_per_kw * P_online_kW + marginal_l_per_kwh * P_out_kW."""

    no_load_l_per_h_per_kw: float = Field(ge=0)
    marginal_l_per_kwh: float = Field(gt=0)


class DieselInputs(BaseModel):
    installed_capacity_kw: float = Field(gt=0, description="Total installed (nameplate) capacity")
    n_units: int = Field(1, ge=1)
    annual_generation_kwh: float = Field(ge=0)
    specific_fuel_consumption_l_per_kwh: float | None = Field(None, gt=0)
    generator_efficiency: float | None = Field(None, gt=0, le=0.6)
    fuel_lhv_mj_per_l: float = Field(default("diesel_lhv_mj_per_l"), gt=0)
    fuel_curve: FuelCurve | None = None
    fuel_price_per_l: float = Field(ge=0)
    fuel_transport_per_l: float = Field(0.0, ge=0)
    variable_om_per_kwh: float = Field(0.0, ge=0, description="Maintenance proportional to energy")
    fixed_om_per_year: float = Field(0.0, ge=0)
    overhaul_cost: float = Field(0.0, ge=0, description="Cost of one major overhaul for the whole fleet")
    overhaul_interval_hours: float = Field(20000.0, gt=0)
    replacement_capex_per_kw: float = Field(0.0, ge=0, description="Replacement value of new generators")
    lifetime_years: float = Field(15.0, gt=0)
    discount_rate: float = Field(0.10, ge=0, lt=1)
    fuel_escalation: float = Field(0.0, ge=-0.5, lt=1, description="Annual change of fuel price for the LCOE")
    om_escalation: float = Field(0.0, ge=-0.5, lt=1)
    availability: float = Field(0.95, gt=0, le=1)
    min_loading_fraction: float = Field(default("diesel_min_loading"), ge=0, lt=1)
    operating_hours_per_year: float | None = Field(None, gt=0, le=HOURS_PER_YEAR)
    co2_kg_per_l: float = Field(default("diesel_co2_kg_per_l"), ge=0)
    currency: str = "XAF"

    @model_validator(mode="after")
    def _check_fuel_basis(self) -> "DieselInputs":
        if self.specific_fuel_consumption_l_per_kwh is None and self.generator_efficiency is None and self.fuel_curve is None:
            raise ValueError("Provide a specific fuel consumption, a generator efficiency or a fuel curve.")
        return self

    @property
    def unit_size_kw(self) -> float:
        return self.installed_capacity_kw / self.n_units

    def average_sfc(self) -> float:
        """Average L/kWh used when no hourly dispatch is available."""
        if self.specific_fuel_consumption_l_per_kwh is not None:
            return self.specific_fuel_consumption_l_per_kwh
        if self.generator_efficiency is not None:
            return 3.6 / (self.generator_efficiency * self.fuel_lhv_mj_per_l)
        # Fuel curve only: evaluate at the average loading while running.
        assert self.fuel_curve is not None
        hours = self.operating_hours_per_year or HOURS_PER_YEAR
        avg_load = self.annual_generation_kwh / hours if hours else 0.0
        if avg_load <= 0:
            return self.fuel_curve.marginal_l_per_kwh
        online = min(self.installed_capacity_kw, math.ceil(avg_load / self.unit_size_kw - 1e-9) * self.unit_size_kw)
        return (self.fuel_curve.no_load_l_per_h_per_kw * online + self.fuel_curve.marginal_l_per_kwh * avg_load) / avg_load


class DieselResults(BaseModel):
    annual_generation_kwh: float
    annual_fuel_l: float
    average_sfc_l_per_kwh: float
    fuel_cost: float
    fuel_transport_cost: float
    variable_om_cost: float
    fixed_om_cost: float
    overhaul_cost_annual: float
    existing_operating_cost: float
    annual_capital_charge: float
    full_economic_cost: float
    operating_cost_per_kwh: float
    economic_cost_per_kwh: float
    lcoe_per_kwh: float
    marginal_cost_per_kwh: float
    capacity_factor: float
    loading_while_running: float | None
    operating_hours: float
    co2_tonnes: float
    warnings: list[str]
    currency: str
    method: str


def hourly_fuel_from_dispatch(inputs: DieselInputs, dispatch_kw: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
    """Hourly fuel (L) and online capacity (kW) for a dispatch profile.

    Units are committed in the minimum number needed to cover each hour's output. Returns the
    number of hours where output is below the minimum loading of a single online unit.
    """
    p = np.clip(np.asarray(dispatch_kw, dtype=float), 0.0, None)
    unit = inputs.unit_size_kw
    units_on = np.where(p > 1e-9, np.ceil(p / unit - 1e-9), 0.0)
    units_on = np.minimum(units_on, inputs.n_units)
    online_kw = units_on * unit
    if inputs.fuel_curve is not None:
        fuel = inputs.fuel_curve.no_load_l_per_h_per_kw * online_kw + inputs.fuel_curve.marginal_l_per_kwh * p
    else:
        fuel = inputs.average_sfc() * p
    below_min = int(np.sum((p > 1e-9) & (p < inputs.min_loading_fraction * online_kw - 1e-9)))
    return fuel, online_kw, below_min


def calculate_diesel(inputs: DieselInputs, dispatch_kw: np.ndarray | None = None) -> DieselResults:
    """Compute the diesel baseline. If ``dispatch_kw`` (8,760 values) is given it overrides
    ``annual_generation_kwh`` and enables hourly fuel-curve and minimum-loading checks."""
    warnings: list[str] = []
    cap = inputs.installed_capacity_kw

    if dispatch_kw is not None:
        dispatch_kw = np.asarray(dispatch_kw, dtype=float)
        if np.any(dispatch_kw < -1e-9):
            raise ValueError("Diesel dispatch cannot be negative.")
        if np.any(dispatch_kw > cap * (1 + 1e-9)):
            raise ValueError("Diesel dispatch exceeds installed capacity.")
        fuel_h, _, below_min = hourly_fuel_from_dispatch(inputs, dispatch_kw)
        generation = float(dispatch_kw.sum())
        fuel_l = float(fuel_h.sum())
        op_hours = float(np.sum(dispatch_kw > 1e-9))
        method = "hourly dispatch + " + ("fuel curve" if inputs.fuel_curve else "average SFC")
        if below_min:
            warnings.append(f"{below_min} h below the minimum loading of the committed units ({inputs.min_loading_fraction:.0%}).")
    else:
        generation = inputs.annual_generation_kwh
        op_hours = inputs.operating_hours_per_year or (HOURS_PER_YEAR if generation > 0 else 0.0)
        fuel_l = generation * inputs.average_sfc()
        method = "annual energy x average SFC" if inputs.fuel_curve is None else "annual energy x fuel curve at average load"

    max_energy = cap * inputs.availability * HOURS_PER_YEAR
    if generation > max_energy * (1 + 1e-9):
        raise ValueError(
            f"Annual generation {generation:,.0f} kWh exceeds the available energy {max_energy:,.0f} kWh "
            f"(capacity x availability x {HOURS_PER_YEAR} h)."
        )

    sfc = fuel_l / generation if generation > 0 else inputs.average_sfc()
    loading = generation / (cap * op_hours) if op_hours > 0 else None
    if loading is not None and loading < inputs.min_loading_fraction and dispatch_kw is None:
        warnings.append(
            f"Average loading while running ({loading:.0%}) is below the minimum loading ({inputs.min_loading_fraction:.0%})."
        )
    if inputs.specific_fuel_consumption_l_per_kwh and not 0.2 <= inputs.specific_fuel_consumption_l_per_kwh <= 0.6:
        warnings.append("Specific fuel consumption outside the usual 0.20-0.60 L/kWh range: check units and data.")

    fuel_cost = fuel_l * inputs.fuel_price_per_l
    transport = fuel_l * inputs.fuel_transport_per_l
    var_om = generation * inputs.variable_om_per_kwh
    overhaul = inputs.overhaul_cost * op_hours / inputs.overhaul_interval_hours
    operating = fuel_cost + transport + var_om + inputs.fixed_om_per_year + overhaul

    capital = inputs.replacement_capex_per_kw * cap
    capital_charge = capital * crf(inputs.discount_rate, inputs.lifetime_years)
    economic = operating + capital_charge

    # LCOE with escalation over the lifetime (end-of-year convention, capital at year 0).
    years = int(math.ceil(inputs.lifetime_years))
    fuel_series = [(fuel_cost + transport) * (1 + inputs.fuel_escalation) ** y for y in range(years)]
    om_series = [(var_om + inputs.fixed_om_per_year + overhaul) * (1 + inputs.om_escalation) ** y for y in range(years)]
    pv_costs = capital + present_value([f + o for f, o in zip(fuel_series, om_series)], inputs.discount_rate)
    pv_energy = present_value([generation] * years, inputs.discount_rate)
    lcoe = pv_costs / pv_energy if pv_energy > 0 else float("nan")

    marginal = sfc * (inputs.fuel_price_per_l + inputs.fuel_transport_per_l) + inputs.variable_om_per_kwh

    return DieselResults(
        annual_generation_kwh=generation,
        annual_fuel_l=fuel_l,
        average_sfc_l_per_kwh=sfc,
        fuel_cost=fuel_cost,
        fuel_transport_cost=transport,
        variable_om_cost=var_om,
        fixed_om_cost=inputs.fixed_om_per_year,
        overhaul_cost_annual=overhaul,
        existing_operating_cost=operating,
        annual_capital_charge=capital_charge,
        full_economic_cost=economic,
        operating_cost_per_kwh=operating / generation if generation > 0 else float("nan"),
        economic_cost_per_kwh=economic / generation if generation > 0 else float("nan"),
        lcoe_per_kwh=lcoe,
        marginal_cost_per_kwh=marginal,
        capacity_factor=generation / (cap * HOURS_PER_YEAR),
        loading_while_running=loading,
        operating_hours=op_hours,
        co2_tonnes=fuel_l * inputs.co2_kg_per_l / 1000.0,
        warnings=warnings,
        currency=inputs.currency,
        method=method,
    )
