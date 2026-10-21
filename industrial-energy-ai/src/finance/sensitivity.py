"""Sensitivity analysis on a FIXED technical configuration.

The installed capacities of the selected scenario are held constant; for every parameter
change the hourly dispatch (rule-based) of both the selected configuration and the baseline is
re-simulated and the financial model is re-run. Re-optimising the sizing for each variation is
deliberately not done (it would mix sizing and parameter effects and take minutes per point).

Parameters are varied by multipliers on their base value (``1.0`` = base case).
"""

from __future__ import annotations

import logging
import math
from collections.abc import Callable

from scipy.optimize import brentq

from src.assumptions import ProjectAssumptions
from src.optimization.dispatch import simulate_dispatch
from src.optimization.system import Capacities
from src.study import existing_capacities, financial_analysis, key_metrics, prepare_study

log = logging.getLogger(__name__)

PARAMETERS: dict[str, dict] = {
    "diesel_price": {"fr": "Prix du gazole", "en": "Diesel price"},
    "demand": {"fr": "Demande d'électricité", "en": "Electricity demand"},
    "solar_capex": {"fr": "CAPEX solaire", "en": "Solar CAPEX"},
    "battery_capex": {"fr": "CAPEX batterie", "en": "Battery CAPEX"},
    "grid_tariff": {"fr": "Tarif réseau", "en": "Grid tariff"},
    "discount_rate": {"fr": "Taux d'actualisation", "en": "Discount rate"},
    "interest_rate": {"fr": "Taux d'intérêt", "en": "Interest rate"},
    "exchange_rate": {"fr": "Taux de change (équipements)", "en": "Exchange rate (equipment)"},
    "equipment_lifetime": {"fr": "Durée de vie des équipements", "en": "Equipment lifetime"},
    "biomass_availability": {"fr": "Disponibilité de la biomasse", "en": "Biomass availability"},
}

DEFAULT_SCENARIOS: dict[str, dict[str, float]] = {
    "base": {p: 1.0 for p in PARAMETERS},
    "optimistic": {"diesel_price": 1.20, "demand": 1.0, "solar_capex": 0.85, "battery_capex": 0.80, "grid_tariff": 1.10,
                   "discount_rate": 0.90, "interest_rate": 0.90, "exchange_rate": 0.95, "equipment_lifetime": 1.10, "biomass_availability": 1.10},
    "conservative": {"diesel_price": 0.80, "demand": 0.90, "solar_capex": 1.20, "battery_capex": 1.25, "grid_tariff": 0.90,
                     "discount_rate": 1.15, "interest_rate": 1.20, "exchange_rate": 1.10, "equipment_lifetime": 0.85, "biomass_availability": 0.80},
}


def apply_multipliers(a: ProjectAssumptions, m: dict[str, float]) -> tuple[ProjectAssumptions, dict]:
    """Return modified assumptions plus pipeline-level factors (load scale, capex and life multipliers)."""
    x = a.model_copy(deep=True)
    g = lambda k: float(m.get(k, 1.0))  # noqa: E731
    x.diesel.fuel_price_per_l *= g("diesel_price")
    x.diesel.fuel_transport_per_l *= g("diesel_price")
    x.pv.capex_per_kwp *= g("solar_capex")
    x.battery.capex_per_kwh *= g("battery_capex")
    x.battery.capex_per_kw *= g("battery_capex")
    x.grid.energy_tariff_per_kwh *= g("grid_tariff")
    x.finance.discount_rate = min(0.99, x.finance.discount_rate * g("discount_rate"))
    if x.finance.equity_discount_rate is not None:
        x.finance.equity_discount_rate = min(0.99, x.finance.equity_discount_rate * g("discount_rate"))
    x.finance.interest_rate = min(0.99, x.finance.interest_rate * g("interest_rate"))
    x.biomass.annual_availability_t *= g("biomass_availability")
    share = a.finance.equipment_cost_share if a.finance.equipment_currency != a.currency else 0.0
    capex_mult = 1.0 + share * (g("exchange_rate") - 1.0)
    return x, {"load_scale": g("demand"), "capex_multiplier": capex_mult, "life_multiplier": g("equipment_lifetime")}


def evaluate(a: ProjectAssumptions, sector: str, scenario_key: str, capacities: Capacities,
             multipliers: dict[str, float] | None = None, stored_load: dict | None = None, stored_solar: dict | None = None) -> dict:
    x, factors = apply_multipliers(a, multipliers or {})
    study = prepare_study(x, sector, stored_load, stored_solar, **factors)
    res = simulate_dispatch(scenario_key, capacities, study.spec, study.profiles)
    base = simulate_dispatch(x.baseline_scenario, existing_capacities(x), study.spec, study.profiles)
    fin = financial_analysis(x, res, base)
    return key_metrics(fin, res, base)


def tornado(a: ProjectAssumptions, sector: str, scenario_key: str, capacities: Capacities, metric: str = "npv_project",
            low: float = 0.8, high: float = 1.2, parameters: list[str] | None = None, **stored) -> dict:
    base_val = evaluate(a, sector, scenario_key, capacities, None, **stored)[metric]
    rows = []
    for p in parameters or list(PARAMETERS):
        lo = evaluate(a, sector, scenario_key, capacities, {p: low}, **stored)[metric]
        hi = evaluate(a, sector, scenario_key, capacities, {p: high}, **stored)[metric]
        swing = abs((hi or 0.0) - (lo or 0.0)) if lo is not None and hi is not None else float("nan")
        rows.append({"parameter": p, "low_multiplier": low, "high_multiplier": high, "low": lo, "high": hi, "swing": swing})
    rows.sort(key=lambda r: -(r["swing"] if math.isfinite(r["swing"]) else -1))
    return {"metric": metric, "base": base_val, "rows": rows}


def scenario_table(a: ProjectAssumptions, sector: str, scenario_key: str, capacities: Capacities,
                   scenarios: dict[str, dict[str, float]] | None = None, **stored) -> dict[str, dict]:
    return {name: {"multipliers": m, "metrics": evaluate(a, sector, scenario_key, capacities, m, **stored)}
            for name, m in (scenarios or DEFAULT_SCENARIOS).items()}


def break_even(a: ProjectAssumptions, sector: str, scenario_key: str, capacities: Capacities, parameter: str = "diesel_price",
               metric: str = "npv_project", target: float = 0.0, lo: float = 0.1, hi: float = 5.0, **stored) -> float | None:
    """Multiplier of ``parameter`` at which ``metric`` equals ``target`` (None if not bracketed)."""
    f: Callable[[float], float] = lambda m: (evaluate(a, sector, scenario_key, capacities, {parameter: m}, **stored)[metric] or 0.0) - target  # noqa: E731
    f_lo, f_hi = f(lo), f(hi)
    if f_lo == 0:
        return lo
    if f_lo * f_hi > 0:
        return None
    return float(brentq(f, lo, hi, xtol=1e-4))


def matrix(a: ProjectAssumptions, sector: str, scenario_key: str, capacities: Capacities, p_row: str, p_col: str,
           values_row: list[float], values_col: list[float], metric: str = "npv_project", **stored) -> dict:
    grid = [[evaluate(a, sector, scenario_key, capacities, {p_row: r, p_col: c}, **stored)[metric] for c in values_col] for r in values_row]
    return {"row_parameter": p_row, "col_parameter": p_col, "rows": values_row, "cols": values_col, "values": grid, "metric": metric}
