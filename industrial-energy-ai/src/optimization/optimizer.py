"""Module H - Energy system optimisation (linear programme, PuLP + HiGHS).

Decision variables
------------------
Capacities: PV kWp (P_pv), battery energy E_b (kWh) and power P_b (kW), new diesel P_dn (kW),
biomass P_bio (kW), grid peak import G_pk (kW, for demand charges).
Hourly (t = 1..T): pv_u (PV used), pv_c (PV curtailed), ch, dis, soc, g_d (diesel), g_bio,
g_grid, us (unserved energy).

Objective - minimise the equivalent annual cost (EAC)
-----------------------------------------------------
    sum_k CRF(r, L_k) * CAPEX_k * Cap_k + FOM_k * Cap_k                     (capital + fixed O&M)
  + w * sum_t [ c_d g_d + c_bio g_bio + c_grid g_grid + c_wear dis + VOLL us ]
  + 12 * demand_charge * G_pk + grid fixed costs
with w = 8760 / T and c_wear = battery capex per kWh / cycle life (linear wear proxy).

Constraints
-----------
  pv_u + pv_c = P_pv * pv_per_kwp[t]                                         (PV availability)
  pv_u + dis + g_d + g_bio + g_grid + us = load[t] + ch                      (energy balance)
  soc[t] = soc[t-1] + eta_c ch - dis / eta_d ; soc[0-] = soc[T] (cyclic)      (storage dynamics)
  soc_min E_b <= soc <= soc_max E_b ; ch, dis <= P_b                          (storage limits)
  E_b / max_duration <= P_b <= E_b / min_duration                             (C-rate window)
  g_d <= P_d,existing + P_dn ; g_bio <= availability * P_bio
  w * sum g_bio <= biomass fuel-limited annual energy
  g_grid <= grid_available[t] * import limit ; g_grid <= G_pk
  w * sum us <= max_unserved_fraction * annual load                          (reliability)

Limitations (documented, also shown in the UI)
----------------------------------------------
* Linear model: diesel minimum loading, unit commitment and part-load fuel curves are not
  represented (they need binary variables). They are checked after the solve by the rule-based
  dispatch simulator, which reports violations and the resulting fuel use.
* Charge/discharge exclusivity is not imposed by binaries; with eta < 1 and a positive wear
  cost simultaneous operation is never optimal, and the result is checked hour by hour.
* Perfect foresight over the simulated year; one representative year; no load growth.
* The optimum is the global optimum of THIS linear formulation (LP is convex) when the solver
  reports "Optimal" - not of the real, non-linear system.
"""

from __future__ import annotations

import logging
import time

import numpy as np
import pulp

from src.finance.common import crf
from src.optimization.system import (
    SCENARIOS,
    Capacities,
    Profiles,
    ScenarioResult,
    SystemSpec,
    scenario_applicable,
    summarise,
)

log = logging.getLogger(__name__)


def _solver(time_limit: int, msg: bool = False):
    available = pulp.listSolvers(onlyAvailable=True)
    if "HiGHS" in available:
        return pulp.HiGHS(msg=msg, timeLimit=time_limit)
    if "HiGHS_CMD" in available:
        return pulp.HiGHS_CMD(msg=msg, timeLimit=time_limit)
    if "PULP_CBC_CMD" in available:
        return pulp.PULP_CBC_CMD(msg=msg, timeLimit=time_limit)
    raise RuntimeError("No LP solver available. Install 'highspy' (pip install highspy).")


def _bounds(fixed, lo, hi):
    if fixed is not None:
        return fixed, fixed
    return lo or 0.0, hi


def optimise_scenario(
    scenario_key: str,
    spec: SystemSpec,
    profiles: Profiles,
    time_limit: int = 300,
) -> ScenarioResult:
    scenario = SCENARIOS[scenario_key]
    ok, reason = scenario_applicable(scenario, spec, profiles)
    if not ok:
        return ScenarioResult(scenario_key, "LP optimisation", False, "Not applicable", reason, Capacities())

    techs = scenario.techs
    econ = spec.economics
    r = econ.discount_rate
    T = profiles.n
    w = profiles.weight
    load = profiles.load_kw
    hours = range(T)
    started = time.perf_counter()

    prob = pulp.LpProblem(f"iea_{scenario_key}", pulp.LpMinimize)
    var = lambda name, lo=None, hi=None: pulp.LpVariable(name, lowBound=lo, upBound=hi)  # noqa: E731
    obj = []
    zero = [0.0] * T

    # --- PV
    if "pv" in techs:
        pv = spec.pv
        lo, hi = _bounds(pv.fixed_kwp, pv.min_kwp, pv.max_kwp)
        P_pv = var("P_pv", lo, hi)
        pv_u = [var(f"pvu_{t}", 0) for t in hours]
        pv_c = [var(f"pvc_{t}", 0) for t in hours]
        k = profiles.pv_per_kwp
        for t in hours:
            prob += pv_u[t] + pv_c[t] == float(k[t]) * P_pv, f"pv_{t}"
        obj.append((crf(r, pv.lifetime_years) * pv.capex_per_kwp + pv.opex_per_kwp_year) * P_pv)
    else:
        P_pv, pv_u, pv_c = None, zero, zero

    # --- Battery
    if "battery" in techs:
        b = spec.battery
        lo_e, hi_e = _bounds(b.fixed_kwh, 0.0, b.max_kwh)
        E_b = var("E_b", lo_e, hi_e)
        P_b = var("P_b", b.fixed_kw if b.fixed_kw is not None else 0.0,
              b.fixed_kw if b.fixed_kw is not None else None)
        ch = [var(f"ch_{t}", 0) for t in hours]
        dis = [var(f"dis_{t}", 0) for t in hours]
        soc = [var(f"soc_{t}", 0) for t in hours]
        for t in hours:
            prev = soc[t - 1] if t > 0 else soc[T - 1]
            prob += soc[t] == prev + b.charge_efficiency * ch[t] - (1.0 / b.discharge_efficiency) * dis[t], f"soc_{t}"
            prob += soc[t] >= b.soc_min * E_b, f"socmin_{t}"
            prob += soc[t] <= b.soc_max * E_b, f"socmax_{t}"
            prob += ch[t] <= P_b, f"chmax_{t}"
            prob += dis[t] <= P_b, f"dismax_{t}"
        if b.fixed_kw is None:
            prob += P_b * b.max_duration_h >= E_b, "crate_low"
            prob += P_b * b.min_duration_h <= E_b, "crate_high"
        # Annualised on calendar life; cycle wear is priced per kWh discharged.
        obj.append((crf(r, b.calendar_life_years) * b.capex_per_kwh + b.opex_per_kwh_year) * E_b)
        obj.append(crf(r, b.calendar_life_years) * b.capex_per_kw * P_b)
        obj.append(w * b.wear_cost_per_kwh * pulp.lpSum(dis))
    else:
        E_b = P_b = None
        ch = dis = soc = zero

    # --- Diesel
    if "diesel" in techs:
        d = spec.diesel
        max_new = d.max_new_kw if d.allow_new_capacity else 0.0
        P_dn = var("P_dn", 0, max_new)
        g_d = [var(f"gd_{t}", 0) for t in hours]
        for t in hours:
            prob += g_d[t] <= d.existing_kw + P_dn, f"dcap_{t}"
        obj.append((crf(r, d.lifetime_years) * d.new_capex_per_kw + d.fixed_om_per_kw_year) * P_dn)
        obj.append(w * d.marginal_cost_per_kwh * pulp.lpSum(g_d))
    else:
        P_dn, g_d = None, zero

    # --- Biomass
    if "biomass" in techs:
        bm = spec.biomass
        lo, hi = _bounds(bm.fixed_kw, 0.0, bm.max_kw)
        P_bio = var("P_bio", lo, hi)
        g_bio = [var(f"gbio_{t}", 0) for t in hours]
        for t in hours:
            prob += g_bio[t] <= bm.availability * P_bio, f"biocap_{t}"
        prob += w * pulp.lpSum(g_bio) <= bm.annual_energy_limit_kwh, "biofuel"
        obj.append((crf(r, bm.lifetime_years) * bm.capex_per_kw + bm.fixed_opex_per_kw_year) * P_bio)
        obj.append(w * bm.marginal_cost_per_kwh * pulp.lpSum(g_bio))
    else:
        P_bio, g_bio = None, zero

    # --- Grid
    if "grid" in techs:
        g = spec.grid
        G_pk = var("G_pk", 0, g.max_import_kw)
        g_g = [var(f"gg_{t}", 0) for t in hours]
        avail = profiles.grid_available
        limit = g.max_import_kw if g.max_import_kw else float(load.max()) * 2 + 1.0
        for t in hours:
            prob += g_g[t] <= float(avail[t]) * limit, f"gavail_{t}"
            prob += g_g[t] <= G_pk, f"gpk_{t}"
        obj.append(w * g.price_per_kwh * pulp.lpSum(g_g))
        obj.append(12 * g.demand_charge_per_kw_month * G_pk)
    else:
        g_g = zero

    # --- Unserved energy and balance
    us = [var(f"us_{t}", 0, float(load[t])) for t in hours]
    voll = econ.value_of_lost_load_per_kwh
    if voll > 0:
        obj.append(w * voll * pulp.lpSum(us))
    prob += w * pulp.lpSum(us) <= econ.max_unserved_fraction * float(load.sum()) * w, "reliability"
    for t in hours:
        prob += pv_u[t] + dis[t] + g_d[t] + g_bio[t] + g_g[t] + us[t] == float(load[t]) + ch[t], f"bal_{t}"

    prob += pulp.lpSum(obj)
    build_s = time.perf_counter() - started
    status_code = prob.solve(_solver(time_limit))
    status = pulp.LpStatus[status_code]
    solve_s = time.perf_counter() - started - build_s
    log.info("Scenario %s: %s (build %.1fs, solve %.1fs, %d vars)", scenario_key, status, build_s, solve_s, len(prob.variables()))

    if status != "Optimal":
        msg = {
            "Infeasible": "No configuration satisfies the reliability constraint with the allowed capacities. "
                          "Relax the unserved-energy limit, allow new diesel capacity or raise capacity limits.",
            "Unbounded": "The problem is unbounded - check cost inputs (zero-cost technologies without limits).",
        }.get(status, f"Solver returned status '{status}' (time limit {time_limit}s may have been reached).")
        return ScenarioResult(scenario_key, "LP optimisation", False, status, msg, Capacities())

    def val(x) -> float:
        if x is None:
            return 0.0
        if isinstance(x, (int, float)):
            return float(x)
        v = x.value()
        return max(0.0, float(v)) if v is not None else 0.0  # clears solver noise such as -0.0

    def arr(xs) -> np.ndarray:
        return np.array([max(0.0, val(x)) for x in xs])

    caps = Capacities(
        pv_kwp=val(P_pv),
        battery_kwh=val(E_b),
        battery_kw=val(P_b),
        diesel_existing_kw=spec.diesel.existing_kw if ("diesel" in techs and spec.diesel) else 0.0,
        diesel_new_kw=val(P_dn),
        biomass_kw=val(P_bio),
    )
    k = profiles.pv_per_kwp if profiles.pv_per_kwp is not None else np.zeros(T)
    hourly = {
        "load": load.copy(),
        "pv_available": k * caps.pv_kwp,
        "pv_used": arr(pv_u),
        "pv_curtailed": arr(pv_c),
        "charge": arr(ch),
        "discharge": arr(dis),
        "soc": arr(soc),
        "diesel": arr(g_d),
        "diesel_excess": np.zeros(T),
        "biomass": arr(g_bio),
        "grid": arr(g_g),
        "unserved": arr(us),
    }
    result = summarise(scenario_key, "LP optimisation", "Optimal", caps, hourly, spec, profiles,
                       message="Optimal for the linear formulation (see limitations).")
    result.diagnostics["objective_eac"] = float(pulp.value(prob.objective))
    result.diagnostics["build_seconds"] = build_s
    result.diagnostics["solve_seconds"] = solve_s
    result.diagnostics["n_variables"] = float(len(prob.variables()))
    return result


def optimise_all(spec: SystemSpec, profiles: Profiles, scenarios: list[str] | None = None, time_limit: int = 300) -> dict[str, ScenarioResult]:
    keys = scenarios or list(SCENARIOS)
    return {k: optimise_scenario(k, spec, profiles, time_limit) for k in keys}


def recommend(results: dict[str, ScenarioResult], max_unserved_fraction: float | None = None) -> str | None:
    """Lowest equivalent annual cost among feasible scenarios (incl. unserved-energy penalty)."""
    candidates = []
    for key, res in results.items():
        if not res.feasible:
            continue
        if max_unserved_fraction is not None and res.metrics["unserved_fraction"] > max_unserved_fraction + 1e-9:
            continue
        candidates.append((res.metrics["annual_cost"] + res.metrics["unserved_penalty"], key))
    return min(candidates)[1] if candidates else None
