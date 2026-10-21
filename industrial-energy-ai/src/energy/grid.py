"""Module G - Grid connection analysis.

The grid is NOT assumed to be reliable. Availability and outage duration are explicit,
configurable assumptions. For hourly simulation a synthetic outage calendar is generated from
them (seeded, reproducible, labelled SYNTHETIC); replace it with recorded outage logs when
available.

Effective supply cost per kWh =
    (annualised connection CAPEX + line maintenance + energy procurement + demand/fixed charges
     + backup generation cost during outages) / energy demand
"""

from __future__ import annotations

import numpy as np
from pydantic import BaseModel, Field

from src.config import HOURS_PER_YEAR
from src.finance.common import crf


class GridInputs(BaseModel):
    distance_km: float = Field(0.0, ge=0)
    voltage_level: str = "MV"
    connection_fixed_cost: float = Field(0.0, ge=0, description="Substation / metering / fees")
    line_cost_per_km: float = Field(0.0, ge=0)
    connection_capex_override: float | None = Field(None, ge=0)
    energy_tariff_per_kwh: float = Field(ge=0)
    transmission_charge_per_kwh: float = Field(0.0, ge=0)
    distribution_charge_per_kwh: float = Field(0.0, ge=0)
    demand_charge_per_kw_month: float = Field(0.0, ge=0)
    fixed_charge_per_month: float = Field(0.0, ge=0)
    max_import_kw: float | None = Field(None, gt=0, description="Contracted capacity")
    availability: float = Field(0.90, gt=0, le=1, description="Share of hours with grid supply")
    average_outage_hours: float = Field(4.0, gt=0, le=240)
    backup_required: bool = True
    maintenance_cost_per_year: float = Field(0.0, ge=0)
    lifetime_years: float = Field(25, gt=0)
    discount_rate: float = Field(0.10, ge=0, lt=1)
    renewable_share: float = Field(0.0, ge=0, le=1, description="Renewable content of grid supply (user-provided; default 0, not assumed)")
    outage_seed: int = 11

    @property
    def connection_capex(self) -> float:
        if self.connection_capex_override is not None:
            return self.connection_capex_override
        return self.connection_fixed_cost + self.line_cost_per_km * self.distance_km

    @property
    def energy_price_per_kwh(self) -> float:
        return self.energy_tariff_per_kwh + self.transmission_charge_per_kwh + self.distribution_charge_per_kwh


def outage_profile(inputs: GridInputs, n_hours: int = HOURS_PER_YEAR) -> np.ndarray:
    """SYNTHETIC hourly availability (1 = grid available, 0 = outage) matching the configured
    availability and average outage duration."""
    avail = np.ones(n_hours)
    outage_hours = int(round((1 - inputs.availability) * n_hours))
    if outage_hours <= 0:
        return avail
    duration = max(1, int(round(inputs.average_outage_hours)))
    rng = np.random.default_rng(inputs.outage_seed)
    remaining = outage_hours
    attempts = 0
    while remaining > 0 and attempts < 100_000:
        attempts += 1
        start = int(rng.integers(0, n_hours))
        length = min(duration, remaining)
        window = avail[start:start + length]
        if window.size < length or window.min() < 1:
            continue
        avail[start:start + length] = 0
        remaining -= length
    return avail


class GridResults(BaseModel):
    connection_capex: float
    annualized_connection_capex: float
    grid_energy_kwh: float
    backup_energy_kwh: float
    unserved_without_backup_kwh: float
    energy_procurement_cost: float
    demand_and_fixed_charges: float
    backup_cost: float
    maintenance_cost: float
    annual_total_cost: float
    effective_cost_per_kwh: float
    outage_hours: int
    peak_import_kw: float
    import_limited_kwh: float
    is_synthetic_outages: bool = True


def analyse_grid(
    inputs: GridInputs,
    load_kw: np.ndarray,
    backup_marginal_cost_per_kwh: float = 0.0,
    backup_fixed_cost_per_year: float = 0.0,
    availability_profile: np.ndarray | None = None,
) -> GridResults:
    load = np.asarray(load_kw, dtype=float)
    avail = outage_profile(inputs, load.size) if availability_profile is None else np.asarray(availability_profile, dtype=float)
    cap = inputs.max_import_kw if inputs.max_import_kw else float("inf")
    grid_kw = np.minimum(load, cap) * avail
    shortfall = load - grid_kw
    outage_short = float((load * (1 - avail)).sum())
    import_limited = float(shortfall.sum()) - outage_short
    grid_kwh = float(grid_kw.sum())
    backup_kwh = float(shortfall.sum()) if inputs.backup_required else 0.0
    unserved = 0.0 if inputs.backup_required else float(shortfall.sum())
    procurement = grid_kwh * inputs.energy_price_per_kwh
    peak = float(grid_kw.max()) if grid_kw.size else 0.0
    charges = inputs.demand_charge_per_kw_month * peak * 12 + inputs.fixed_charge_per_month * 12
    backup_cost = backup_kwh * backup_marginal_cost_per_kwh + (backup_fixed_cost_per_year if inputs.backup_required else 0.0)
    ann_capex = inputs.connection_capex * crf(inputs.discount_rate, inputs.lifetime_years)
    total = ann_capex + inputs.maintenance_cost_per_year + procurement + charges + backup_cost
    demand = float(load.sum())
    return GridResults(
        connection_capex=inputs.connection_capex,
        annualized_connection_capex=ann_capex,
        grid_energy_kwh=grid_kwh,
        backup_energy_kwh=backup_kwh,
        unserved_without_backup_kwh=unserved,
        energy_procurement_cost=procurement,
        demand_and_fixed_charges=charges,
        backup_cost=backup_cost,
        maintenance_cost=inputs.maintenance_cost_per_year,
        annual_total_cost=total,
        effective_cost_per_kwh=total / demand if demand > 0 else float("nan"),
        outage_hours=int((avail < 0.5).sum()),
        peak_import_kw=peak,
        import_limited_kwh=import_limited,
        is_synthetic_outages=availability_profile is None,
    )
