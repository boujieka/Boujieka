"""Rule-based hourly dispatch for a FIXED configuration (transparent, physically constrained).

Used to (1) verify optimiser results under operating rules the LP cannot represent (diesel
minimum loading and unit commitment), (2) run fast sensitivity analyses without re-optimising,
and (3) simulate user-defined configurations.

Dispatch rules for each hour (load-following strategy):
1. PV serves the load first.
2. PV surplus charges the battery (power, SOC and efficiency limits); the rest is curtailed
   (no export assumed).
3. Remaining deficit: battery discharge, then dispatchable sources in merit order of marginal
   cost (biomass, grid when available, diesel).
   With a grid connection, a share of the usable battery capacity (``outage_reserve_fraction``)
   is held as an outage reserve: while the grid is up the battery only discharges energy above
   the reserve, and it recharges from the grid up to the reserve level; during outages the
   whole usable capacity is available.
4. Diesel units are committed in the minimum number covering the residual demand; if that
   demand is below the minimum loading of the committed units, they run at minimum loading and
   the surplus charges the battery or is reported as dumped energy (``diesel_excess``).
5. Anything still uncovered is unserved energy.
The battery is charged from PV surplus, from the grid only up to the outage reserve, and from
diesel only with minimum-load surplus; it never charges and discharges in the same hour.
"""

from __future__ import annotations

import math

import numpy as np

from src.optimization.system import SCENARIOS, Capacities, Profiles, ScenarioResult, SystemSpec, scenario_applicable, summarise


def simulate_dispatch(scenario_key: str, capacities: Capacities, spec: SystemSpec, profiles: Profiles) -> ScenarioResult:
    scenario = SCENARIOS[scenario_key]
    ok, reason = scenario_applicable(scenario, spec, profiles)
    if not ok:
        return ScenarioResult(scenario_key, "rule-based dispatch", False, "Not applicable", reason, capacities)
    techs = scenario.techs
    T = profiles.n
    load = profiles.load_kw
    caps = Capacities(**capacities.as_dict())
    if "pv" not in techs:
        caps.pv_kwp = 0.0
    if "battery" not in techs:
        caps.battery_kwh = caps.battery_kw = 0.0
    if "diesel" not in techs:
        caps.diesel_existing_kw = caps.diesel_new_kw = 0.0
    if "biomass" not in techs:
        caps.biomass_kw = 0.0

    pv_avail = (profiles.pv_per_kwp * caps.pv_kwp) if (profiles.pv_per_kwp is not None) else np.zeros(T)
    grid_avail = profiles.grid_available if ("grid" in techs and profiles.grid_available is not None) else np.zeros(T)
    grid_limit = (spec.grid.max_import_kw or math.inf) if ("grid" in techs and spec.grid) else 0.0

    b = spec.battery
    e_cap = caps.battery_kwh
    p_cap = caps.battery_kw
    eta_c = b.charge_efficiency if b else 1.0
    eta_d = b.discharge_efficiency if b else 1.0
    soc_lo = (b.soc_min if b else 0.0) * e_cap
    soc_hi = (b.soc_max if b else 0.0) * e_cap
    soc = 0.5 * (soc_lo + soc_hi)
    soc0 = soc
    has_grid = "grid" in techs and spec.grid is not None
    reserve = soc_lo + ((b.outage_reserve_fraction if b else 0.0) * (soc_hi - soc_lo) if has_grid else 0.0)

    d = spec.diesel
    d_cap = caps.diesel_total_kw
    unit = d.unit_kw if d else 1.0
    n_units = max(1, math.ceil(d_cap / unit - 1e-9)) if d_cap > 0 else 0
    min_load = d.min_loading if d else 0.0

    bm = spec.biomass
    bio_cap = caps.biomass_kw * (bm.availability if bm else 0.0)
    bio_budget = (bm.annual_energy_limit_kwh / profiles.weight) if (bm and caps.biomass_kw > 0) else 0.0

    # Merit order of dispatchable sources (cheapest first).
    order = []
    if caps.biomass_kw > 0 and bm:
        order.append(("biomass", bm.marginal_cost_per_kwh))
    if "grid" in techs and spec.grid:
        order.append(("grid", spec.grid.price_per_kwh))
    if d_cap > 0 and d:
        order.append(("diesel", d.marginal_cost_per_kwh))
    order.sort(key=lambda x: x[1])

    out = {k: np.zeros(T) for k in ("pv_used", "pv_curtailed", "charge", "discharge", "soc", "diesel", "diesel_excess", "biomass", "grid", "unserved")}
    for t in range(T):
        L = float(load[t])
        pv = float(pv_avail[t])
        pv_direct = min(pv, L)
        surplus = pv - pv_direct
        deficit = L - pv_direct
        charge = 0.0
        if surplus > 0 and e_cap > 0:
            charge = min(surplus, p_cap, max(soc_hi - soc, 0.0) / eta_c)
            soc += charge * eta_c
        out["pv_used"][t] = pv_direct + charge
        out["pv_curtailed"][t] = surplus - charge
        grid_up = has_grid and grid_avail[t] > 0.5
        floor = reserve if grid_up else soc_lo
        discharge = 0.0
        if deficit > 0 and e_cap > 0:
            discharge = min(deficit, p_cap, max(soc - floor, 0.0) * eta_d)
            soc -= discharge / eta_d
            deficit -= discharge
        grid_charge = 0.0
        if grid_up and e_cap > 0 and discharge == 0.0 and soc < reserve - 1e-9:
            grid_charge = min(p_cap - charge, (reserve - soc) / eta_c, grid_limit)
            grid_charge = max(grid_charge, 0.0)
            soc += grid_charge * eta_c
            charge += grid_charge
        for source, _ in order:
            if deficit <= 1e-9:
                break
            if source == "biomass":
                g = min(deficit, bio_cap, bio_budget)
                bio_budget -= g
                out["biomass"][t] = g
            elif source == "grid":
                g = min(deficit, max(grid_limit - grid_charge, 0.0)) if grid_up else 0.0
                out["grid"][t] = g
            else:
                need = min(deficit, d_cap)
                units_on = min(n_units, math.ceil(need / unit - 1e-9)) if need > 1e-9 else 0
                g = max(need, min_load * units_on * unit) if units_on else 0.0
                g = min(g, d_cap)
                excess = g - need
                if excess > 1e-9 and e_cap > 0 and charge == 0.0 and discharge == 0.0:
                    c2 = min(excess, p_cap, max(soc_hi - soc, 0.0) / eta_c)
                    soc += c2 * eta_c
                    charge += c2
                    excess -= c2
                out["diesel"][t] = g
                out["diesel_excess"][t] = max(excess, 0.0)
                g = need
            deficit -= g
        out["grid"][t] += grid_charge
        out["charge"][t] = charge
        out["discharge"][t] = discharge
        out["unserved"][t] = max(deficit, 0.0)
        out["soc"][t] = soc

    hourly = {"load": load.copy(), "pv_available": pv_avail, **out}
    res = summarise(scenario_key, "rule-based dispatch", "Simulated", caps, hourly, spec, profiles,
                    message="Rule-based load-following dispatch of a fixed configuration.")
    # The simulator does not enforce a cyclic SOC; report the residual using the true initial SOC.
    if e_cap > 0 and b:
        prev = np.concatenate(([soc0], out["soc"][:-1]))
        resid = out["soc"] - (prev + out["charge"] * eta_c - out["discharge"] / eta_d)
        res.diagnostics["battery_soc_residual_kwh"] = float(np.max(np.abs(resid)))
        res.diagnostics["battery_soc_change_kwh"] = float(out["soc"][-1] - soc0)
    return res
