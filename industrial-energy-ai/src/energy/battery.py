"""Module E - Battery energy storage (BESS) engine.

Operating model: hourly, energy-based, with mutually exclusive charge and discharge in each
hour (the rule-based simulator decides one mode per hour, so both can never be positive).

State of charge (kWh):
    SOC[t] = SOC[t-1] + charge[t] * eta_c - discharge[t] / eta_d
Constraints enforced every hour:
    0 <= charge, discharge <= P_max ;  SOC_min*E <= SOC <= SOC_max*E
Energy conservation is verified explicitly after every simulation (:func:`check_energy_balance`).

Degradation (screening model): capacity fades linearly with equivalent full cycles (EFC) and
calendar time until end-of-life (default 80 % of nominal capacity). The battery must be replaced
when either the calendar life or the cycle life is reached, whichever comes first.
EFC convention used here: annual discharged energy / nominal energy capacity.
"""

from __future__ import annotations

import math

import numpy as np
from pydantic import BaseModel, Field, model_validator

from src.energy.defaults import default


class BatteryInputs(BaseModel):
    energy_capacity_kwh: float = Field(ge=0)
    power_capacity_kw: float = Field(ge=0)
    round_trip_efficiency: float | None = Field(None, gt=0, le=1)
    charge_efficiency: float = Field(default("bess_charge_eff"), gt=0, le=1)
    discharge_efficiency: float = Field(default("bess_discharge_eff"), gt=0, le=1)
    soc_min: float = Field(default("bess_soc_min"), ge=0, lt=1)
    soc_max: float = Field(default("bess_soc_max"), gt=0, le=1)
    initial_soc: float = Field(0.5, ge=0, le=1)
    calendar_life_years: float = Field(15.0, gt=0)
    cycle_life_efc: float = Field(6000.0, gt=0)
    end_of_life_capacity: float = Field(0.80, gt=0, lt=1)
    capex_per_kwh: float = Field(0.0, ge=0)
    capex_per_kw: float = Field(0.0, ge=0)
    replacement_cost_per_kwh: float | None = Field(None, ge=0)
    opex_per_kwh_year: float = Field(0.0, ge=0)

    @model_validator(mode="after")
    def _consistency(self) -> "BatteryInputs":
        if self.soc_min >= self.soc_max:
            raise ValueError("soc_min must be lower than soc_max.")
        if self.round_trip_efficiency is not None:
            one_way = math.sqrt(self.round_trip_efficiency)
            object.__setattr__(self, "charge_efficiency", one_way)
            object.__setattr__(self, "discharge_efficiency", one_way)
        if not self.soc_min <= self.initial_soc <= self.soc_max:
            object.__setattr__(self, "initial_soc", min(max(self.initial_soc, self.soc_min), self.soc_max))
        return self

    @property
    def rte(self) -> float:
        return self.charge_efficiency * self.discharge_efficiency

    @property
    def usable_kwh(self) -> float:
        return self.energy_capacity_kwh * (self.soc_max - self.soc_min)

    @property
    def capex(self) -> float:
        return self.capex_per_kwh * self.energy_capacity_kwh + self.capex_per_kw * self.power_capacity_kw


class BatteryResults(BaseModel):
    charged_kwh: float
    discharged_kwh: float
    losses_kwh: float
    soc_change_kwh: float
    equivalent_full_cycles: float
    utilization: float
    simultaneous_hours: int
    max_balance_error_kwh: float
    replacement_interval_years: float
    replacement_driver: str
    capacity_after_year1_fraction: float


def simulate_battery(
    surplus_kw: np.ndarray,
    deficit_kw: np.ndarray,
    spec: BatteryInputs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Greedy hourly dispatch: charge from surplus, discharge to cover deficit.

    Returns hourly (charge_kw, discharge_kw, soc_kwh at end of hour).
    """
    surplus = np.clip(np.asarray(surplus_kw, dtype=float), 0, None)
    deficit = np.clip(np.asarray(deficit_kw, dtype=float), 0, None)
    n = surplus.size
    e = spec.energy_capacity_kwh
    p = spec.power_capacity_kw
    eta_c, eta_d = spec.charge_efficiency, spec.discharge_efficiency
    soc_lo, soc_hi = spec.soc_min * e, spec.soc_max * e
    charge = np.zeros(n)
    discharge = np.zeros(n)
    soc = np.zeros(n)
    s = spec.initial_soc * e
    if e <= 0 or p <= 0:
        soc[:] = s
        return charge, discharge, soc
    for t in range(n):
        if surplus[t] > 0:
            c = min(surplus[t], p, max(soc_hi - s, 0.0) / eta_c)
            charge[t] = c
            s += c * eta_c
        elif deficit[t] > 0:
            d = min(deficit[t], p, max(s - soc_lo, 0.0) * eta_d)
            discharge[t] = d
            s -= d / eta_d
        soc[t] = s
    return charge, discharge, soc


def check_energy_balance(charge: np.ndarray, discharge: np.ndarray, soc: np.ndarray, spec: BatteryInputs) -> float:
    """Maximum absolute hourly residual of the SOC equation (kWh)."""
    prev = np.concatenate(([spec.initial_soc * spec.energy_capacity_kwh], soc[:-1]))
    residual = soc - (prev + charge * spec.charge_efficiency - discharge / spec.discharge_efficiency)
    return float(np.max(np.abs(residual))) if residual.size else 0.0


def summarize_battery(charge: np.ndarray, discharge: np.ndarray, soc: np.ndarray, spec: BatteryInputs, hours_per_year: int = 8760) -> BatteryResults:
    e = spec.energy_capacity_kwh
    charged = float(charge.sum())
    discharged = float(discharge.sum())
    scale = hours_per_year / max(charge.size, 1)
    losses = charged * (1 - spec.charge_efficiency) + discharged * (1 / spec.discharge_efficiency - 1)
    soc_change = float(soc[-1] - spec.initial_soc * e) if soc.size else 0.0
    efc = discharged * scale / e if e > 0 else 0.0
    cycle_years = spec.cycle_life_efc / efc if efc > 0 else float("inf")
    if cycle_years < spec.calendar_life_years:
        interval, driver = cycle_years, "cycle life"
    else:
        interval, driver = spec.calendar_life_years, "calendar life"
    fade_per_year = (1 - spec.end_of_life_capacity) / interval if interval > 0 and math.isfinite(interval) else 0.0
    max_throughput = spec.power_capacity_kw * charge.size
    return BatteryResults(
        charged_kwh=charged,
        discharged_kwh=discharged,
        losses_kwh=losses,
        soc_change_kwh=soc_change,
        equivalent_full_cycles=efc,
        utilization=discharged / max_throughput if max_throughput > 0 else 0.0,
        simultaneous_hours=int(np.sum((charge > 1e-6) & (discharge > 1e-6))),
        max_balance_error_kwh=check_energy_balance(charge, discharge, soc, spec),
        replacement_interval_years=interval,
        replacement_driver=driver,
        capacity_after_year1_fraction=1 - fade_per_year,
    )


def replacement_years(interval_years: float, project_years: int) -> list[int]:
    """Operating years (1-based) in which the battery must be replaced within the project."""
    if not math.isfinite(interval_years) or interval_years <= 0:
        return []
    years: list[int] = []
    k = 1
    while True:
        y = int(math.ceil(k * interval_years - 1e-9))
        if y >= project_years:
            break
        years.append(y + 1 if y == 0 else y)
        k += 1
    return years
