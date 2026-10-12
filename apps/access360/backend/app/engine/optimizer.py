"""ACCESS OPTIMIZER: transparent screening comparison of electrification options for one settlement.

This is a screening tool. It uses annual energy and lifecycle costs, not hourly simulation, and its results must be
confirmed by a design study before any option is presented as deployable. Every cost is an explicit input.
Options that fail a technical gate are reported with the reason and are never ranked.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class Settlement(BaseModel):
    name: str
    households: int = Field(ge=0)
    businesses: int = Field(0, ge=0)
    productive_users: int = Field(0, ge=0, description="Mills, pumps, cold rooms and similar")
    institutions: int = Field(0, ge=0)
    anchor_present: bool = False
    anchor_kwh_month: float = Field(0.0, ge=0)
    household_kwh_month: float = Field(ge=0)
    business_kwh_month: float = Field(0.0, ge=0)
    productive_kwh_month: float = Field(0.0, ge=0)
    institution_kwh_month: float = Field(0.0, ge=0)
    household_income_month: float = Field(gt=0, description="LCY")
    distance_to_grid_km: float | None = Field(None, ge=0, description="None = unknown (grid options then fail their gate)")
    grid_has_capacity: bool | None = None
    grid_supply_hours: float = Field(12.0, ge=0, le=24)
    dispersed_household_share: float = Field(0.0, ge=0, le=1, description="Households too far from the centre for a network")


class OptionCosts(BaseModel):
    """All costs in LCY. Values must come from quotes, programme data or cited benchmarks."""

    discount_rate_pa: float
    horizon_years: int = 20
    # grid
    grid_densification_max_km: float = 1.0
    grid_extension_max_km: float = 30.0
    mv_line_per_km: float
    lv_network_per_connection: float
    grid_connection_per_connection: float
    grid_cost_of_supply_per_kwh: float
    grid_om_pct_capex: float = 0.02
    grid_kgco2_per_kwh: float = 0.0
    # mini grid
    pv_per_kwp: float
    battery_per_kwh: float
    battery_life_years: float = 8.0
    diesel_per_kw: float = 0.0
    diesel_fuel_per_kwh: float = 0.0
    diesel_kgco2_per_kwh: float = 0.8
    minigrid_network_per_connection: float
    minigrid_om_pct_capex: float = 0.03
    pv_yield_kwh_per_kwp_pa: float = 1500.0
    network_loss: float = 0.08
    battery_share_of_daily_energy: float = 0.6
    battery_depth_of_discharge: float = 0.8
    anchor_daytime_share: float = Field(0.8, ge=0, le=1, description="Share of anchor energy used in daylight, served directly by PV (option F)")
    hybrid_diesel_share: float = 0.15
    # solar home systems
    shs_cost_per_household: float
    shs_kwh_month_capacity: float
    shs_life_years: float = 5.0
    shs_om_pct_capex: float = 0.05
    # time to electrify, months
    months_densification: float = 6
    months_extension: float = 24
    months_minigrid: float = 12
    months_shs: float = 3
    # affordability policy (model policy threshold, not a standard)
    affordability_share_of_income: float = 0.10


class Weights(BaseModel):
    """Initial design weights, configurable. Not a validated scientific standard."""

    economic_cost: float = 0.25
    time: float = 0.15
    service_quality: float = 0.15
    subsidy_efficiency: float = 0.15
    financial_sustainability: float = 0.15
    environment: float = 0.05
    productive_use: float = 0.10


OPTIONS = {
    "A": "Grid densification",
    "B": "Grid extension",
    "C": "Solar PV mini grid with battery",
    "D": "Solar PV, battery and diesel back up mini grid",
    "E": "Standalone solar home systems",
    "F": "Anchor, business and community mini grid",
    "G": "Mini grid for the centre plus solar home systems for dispersed households",
}


def _pv_factor(r_pa: float, years: int) -> float:
    return sum(1 / (1 + r_pa) ** y for y in range(1, years + 1))


def compare(s: Settlement, c: OptionCosts, w: Weights = Weights()) -> dict:
    H = c.horizon_years
    af = _pv_factor(c.discount_rate_pa, H)
    conns_all = s.households + s.businesses + s.productive_users + s.institutions + (1 if s.anchor_present else 0)
    e_hh = s.households * s.household_kwh_month * 12
    e_bus = s.businesses * s.business_kwh_month * 12
    e_pu = s.productive_users * s.productive_kwh_month * 12
    e_inst = s.institutions * s.institution_kwh_month * 12
    e_anchor = s.anchor_kwh_month * 12 if s.anchor_present else 0.0
    e_total = e_hh + e_bus + e_pu + e_inst + e_anchor
    out = []

    def replacement_pv(cost: float, life: float) -> float:
        tot, k = 0.0, 1
        while life > 0 and k * life < H:
            tot += cost / (1 + c.discount_rate_pa) ** (k * life)
            k += 1
        return tot

    def minigrid(e_served: float, n_conn: int, diesel_share: float, daytime_kwh: float = 0.0) -> dict:
        gen = e_served / (1 - c.network_loss)
        pv_kwp = gen * (1 - diesel_share) / c.pv_yield_kwh_per_kwp_pa
        # energy used in daylight (anchor loads in option F) bypasses the battery
        stored = max(gen - daytime_kwh / (1 - c.network_loss), 0.0)
        batt = stored / 365 * c.battery_share_of_daily_energy * (1 - diesel_share) / c.battery_depth_of_discharge
        peak_kw = gen / 8760 / 0.35  # assumed load factor 35% for diesel sizing only
        diesel_kw = peak_kw if diesel_share > 0 else 0.0
        capex = (pv_kwp * c.pv_per_kwp + batt * c.battery_per_kwh + diesel_kw * c.diesel_per_kw
                 + n_conn * c.minigrid_network_per_connection)
        opex = capex * c.minigrid_om_pct_capex + gen * diesel_share * c.diesel_fuel_per_kwh
        pv_cost = capex + opex * af + replacement_pv(batt * c.battery_per_kwh, c.battery_life_years)
        co2 = gen * diesel_share * c.diesel_kgco2_per_kwh / 1000
        return dict(capex=capex, opex_pa=opex, pv_cost=pv_cost, co2_t_pa=co2, sizing=dict(pv_kwp=pv_kwp, battery_kwh=batt, diesel_kw=diesel_kw))

    for code, name in OPTIONS.items():
        gates: list[str] = []
        served = e_total
        n = conns_all
        tier = 0
        months = 0.0
        d = s.distance_to_grid_km
        res: dict = {}
        if code in ("A", "B"):
            if d is None:
                gates.append("Distance to the grid unknown")
            if s.grid_has_capacity is not True:
                gates.append("Grid capacity to serve the load not confirmed")
            if code == "A" and d is not None and d > c.grid_densification_max_km:
                gates.append(f"Settlement {d:.1f} km from the grid, beyond densification range ({c.grid_densification_max_km} km)")
            if code == "B" and d is not None and d > c.grid_extension_max_km:
                gates.append(f"Extension of {d:.1f} km beyond the configured maximum ({c.grid_extension_max_km} km)")
            km = (d or 0.0) if code == "B" else 0.0
            capex = km * c.mv_line_per_km + n * (c.lv_network_per_connection + c.grid_connection_per_connection)
            opex = capex * c.grid_om_pct_capex + e_total * c.grid_cost_of_supply_per_kwh
            res = dict(capex=capex, opex_pa=opex, pv_cost=capex + opex * af, co2_t_pa=e_total * c.grid_kgco2_per_kwh / 1000, sizing=dict(mv_km=km))
            tier = 5 if s.grid_supply_hours >= 23 else 4 if s.grid_supply_hours >= 16 else 3 if s.grid_supply_hours >= 8 else 2
            months = c.months_densification if code == "A" else c.months_extension
        elif code in ("C", "D"):
            res = minigrid(e_total, n, 0.0 if code == "C" else c.hybrid_diesel_share)
            tier = 3 if code == "C" else 4
            months = c.months_minigrid
        elif code == "F":
            if not s.anchor_present or s.anchor_kwh_month <= 0:
                gates.append("No anchor customer identified")
            res = minigrid(e_total, n, c.hybrid_diesel_share, daytime_kwh=e_anchor * c.anchor_daytime_share)
            tier = 4
            months = c.months_minigrid
        elif code == "E":
            hh_served = s.households * min(s.household_kwh_month, c.shs_kwh_month_capacity) * 12
            served = hh_served
            n = s.households
            if s.households == 0:
                gates.append("No households to serve")
            capex = s.households * c.shs_cost_per_household
            opex = capex * c.shs_om_pct_capex
            res = dict(capex=capex, opex_pa=opex, pv_cost=capex + opex * af + replacement_pv(capex, c.shs_life_years), co2_t_pa=0.0,
                       sizing=dict(systems=s.households))
            tier = 1 if c.shs_kwh_month_capacity < 6 else 2
            months = c.months_shs
        elif code == "G":
            if s.dispersed_household_share <= 0:
                gates.append("No dispersed households: option G equals option D")
            hh_d = int(round(s.households * s.dispersed_household_share))
            e_core = e_total - hh_d * s.household_kwh_month * 12
            mg = minigrid(e_core, n - hh_d, c.hybrid_diesel_share)
            shs_capex = hh_d * c.shs_cost_per_household
            shs_pv = shs_capex + shs_capex * c.shs_om_pct_capex * af + replacement_pv(shs_capex, c.shs_life_years)
            served = e_core + hh_d * min(s.household_kwh_month, c.shs_kwh_month_capacity) * 12
            res = dict(capex=mg["capex"] + shs_capex, opex_pa=mg["opex_pa"] + shs_capex * c.shs_om_pct_capex,
                       pv_cost=mg["pv_cost"] + shs_pv, co2_t_pa=mg["co2_t_pa"], sizing=dict(**mg["sizing"], shs=hh_d))
            tier = 3
            months = c.months_minigrid
        unserved = max(0.0, e_total - served)
        pv_energy = served * af
        lcoe = res["pv_cost"] / pv_energy if pv_energy > 0 else None
        afford_tariff = (c.affordability_share_of_income * s.household_income_month / s.household_kwh_month
                         if s.household_kwh_month > 0 else None)
        pv_rev_afford = (afford_tariff or 0.0) * served * af
        subsidy_pv = max(0.0, res["pv_cost"] - pv_rev_afford)
        hh_bill = (lcoe or 0.0) * min(s.household_kwh_month, c.shs_kwh_month_capacity if code == "E" else s.household_kwh_month)
        pu_served = 0.0 if code == "E" else (e_pu + e_anchor)
        out.append(dict(
            code=code, name=name, feasible=not gates, gates_failed=gates,
            capex=res["capex"], opex_pa=res["opex_pa"], replacement_included=True, pv_lifecycle_cost=res["pv_cost"],
            annual_demand_kwh=e_total, annual_supplied_kwh=served, unserved_share=unserved / e_total if e_total else None,
            connections=n, cost_per_connection=res["capex"] / n if n else None, lcoe=lcoe, service_tier=tier,
            household_bill_at_cost_month=hh_bill, bill_to_income=hh_bill / s.household_income_month,
            subsidy_requirement_pv=subsidy_pv, subsidy_per_connection=subsidy_pv / n if n else None,
            months_to_electrify=months, co2_t_pa=res["co2_t_pa"], financing_requirement=res["capex"],
            cost_recovery_ratio=(pv_rev_afford / res["pv_cost"]) if res["pv_cost"] > 0 else None,
            productive_use_share_served=(pu_served / (e_pu + e_anchor)) if (e_pu + e_anchor) > 0 else None,
            sizing=res["sizing"]))
    _score(out, w)
    return {"settlement": s.name, "options": out, **_recommend(out),
            "method_note": ("Screening comparison on annual energy and lifecycle cost. Not a substitute for an hourly design "
                            "study or a least-cost electrification plan. Weights are initial design assumptions.")}


OBJECTIVES = [  # key, direction (+1 higher is better), weight attribute
    ("pv_cost_per_kwh", -1, "economic_cost"),
    ("months_to_electrify", -1, "time"),
    ("service_tier", +1, "service_quality"),
    ("subsidy_per_connection", -1, "subsidy_efficiency"),
    ("cost_recovery_ratio", +1, "financial_sustainability"),
    ("co2_t_pa", -1, "environment"),
    ("productive_use_share_served", +1, "productive_use"),
]


def _obj_values(o: dict) -> dict:
    return {"pv_cost_per_kwh": o["lcoe"], "months_to_electrify": o["months_to_electrify"], "service_tier": o["service_tier"],
            "subsidy_per_connection": o["subsidy_per_connection"], "cost_recovery_ratio": o["cost_recovery_ratio"],
            "co2_t_pa": o["co2_t_pa"], "productive_use_share_served": o["productive_use_share_served"] or 0.0}


def _score(opts: list[dict], w: Weights) -> None:
    feas = [o for o in opts if o["feasible"] and o["lcoe"] is not None]
    for o in opts:
        o["objectives"] = _obj_values(o)
        o["score"] = None
    if not feas:
        return
    tot_w = sum(getattr(w, a) for _, _, a in OBJECTIVES)
    for key, sign, attr in OBJECTIVES:
        vals = [o["objectives"][key] for o in feas]
        lo, hi = min(vals), max(vals)
        for o in feas:
            v = o["objectives"][key]
            x = 0.5 if hi == lo else (v - lo) / (hi - lo)
            if sign < 0:
                x = 1 - x
            o.setdefault("score_parts", {})[key] = x * getattr(w, attr) / tot_w * 100
    for o in feas:
        o["score"] = sum(o["score_parts"].values())
    # Pareto front over the seven objectives
    for o in feas:
        dominated = False
        for q in feas:
            if q is o:
                continue
            better_or_eq = all((q["objectives"][k] * s >= o["objectives"][k] * s) for k, s, _ in OBJECTIVES)
            strictly = any((q["objectives"][k] * s > o["objectives"][k] * s) for k, s, _ in OBJECTIVES)
            if better_or_eq and strictly:
                dominated = True
                break
        o["pareto_efficient"] = not dominated
    for o in opts:
        o.setdefault("pareto_efficient", False)


def _recommend(opts: list[dict]) -> dict:
    feas = [o for o in opts if o["feasible"] and o["lcoe"] is not None]
    if not feas:
        return {"least_cost": None, "recommended": None,
                "explanation": "No option passed its technical gates. Complete the missing data (grid distance, capacity, anchor) and rerun."}
    least = min(feas, key=lambda o: o["lcoe"])
    rec = max(feas, key=lambda o: o["score"])
    why = [f"Least cost per kWh served: option {least['code']} ({least['name']})."]
    if rec["code"] != least["code"]:
        parts = sorted(rec["score_parts"].items(), key=lambda kv: -kv[1])[:3]
        why.append(f"Recommended option {rec['code']} ({rec['name']}) scores highest across the weighted objectives; "
                   f"its strongest objectives are {', '.join(k.replace('_', ' ') for k, _ in parts)}.")
    else:
        why.append("The least cost option also scores highest across the weighted objectives.")
    infeas = [o for o in opts if not o["feasible"]]
    if infeas:
        why.append("Excluded: " + "; ".join(f"{o['code']} ({', '.join(o['gates_failed'])})" for o in infeas) + ".")
    return {"least_cost": least["code"], "recommended": rec["code"], "explanation": " ".join(why)}


def demo_settlement() -> tuple[Settlement, OptionCosts]:
    """ILLUSTRATIVE: synthetic settlement and placeholder costs for demonstration only."""
    s = Settlement(name="Demo settlement (synthetic)", households=600, businesses=60, productive_users=10, institutions=3,
                   anchor_present=True, anchor_kwh_month=1500, household_kwh_month=9, business_kwh_month=45,
                   productive_kwh_month=250, institution_kwh_month=120, household_income_month=60000,
                   distance_to_grid_km=18, grid_has_capacity=True, grid_supply_hours=14, dispersed_household_share=0.15)
    c = OptionCosts(discount_rate_pa=0.10, mv_line_per_km=9_000_000, lv_network_per_connection=180_000,
                    grid_connection_per_connection=60_000, grid_cost_of_supply_per_kwh=150, pv_per_kwp=480_000,
                    battery_per_kwh=180_000, diesel_per_kw=250_000, diesel_fuel_per_kwh=420,
                    minigrid_network_per_connection=200_000, shs_cost_per_household=150_000, shs_kwh_month_capacity=6)
    return s, c

