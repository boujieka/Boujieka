"""Currency, Portfolio and Inputs-sheet calculations (everything that is not on
the annual timeline). Values are stored under their workbook cell reference
(``Currency!F33``, ``Portfolio!S14``, ``Inputs!E30``...) for reconciliation."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from . import excel as X
from .assumptions import Assumptions, MoneyInput
from .options import FAITHFUL, EngineOptions

COLS_AM = [chr(c) for c in range(ord("I"), ord("Z") + 1)] + [f"A{chr(c)}" for c in range(ord("A"), ord("M") + 1)]  # I..AM


@dataclass
class Prepared:
    """Scalars keyed by cell, tables keyed by Inputs row (list over columns I..)."""
    s: dict = field(default_factory=dict)
    tables: dict = field(default_factory=dict)

    def __getitem__(self, k):
        return self.s[k]


def _currency(a: Assumptions, p: Prepared) -> None:
    c = a.currency
    s = p.s
    s["Currency!F16"] = c.base_exchange_rate
    s["Currency!F11"] = c.effective_year
    s["Currency!F18"] = c.case
    # Exchange_rate = LOOKUP(F11, Inputs!I401:AM402): LCY per USD in the effective year
    years = p.tables["Inputs!401"]
    s["Currency!F14"] = X.lookup(c.effective_year, years, p.tables["Inputs!402"])
    fx = s["Currency!F14"]
    vat = a.tax.vat_rate  # Currency!G20
    s["Currency!G20"] = vat
    rows = {
        "mmra_starting_balance": 28, "all_in_cost_of_debt": 29, "capex_net_of_grant": 33,
        "grant_per_connection": 34, "battery_cost": 35, "transfer_fee": 36, "fixed_fee_per_grid": 39,
        "diesel_price": 40, "pv_price": 44, "battery_racking": 45, "battery_installation": 46,
        "battery_replacement_2023": 47, "inverter_price_2020": 48, "expansion_racking": 49,
        "expansion_logistics": 50, "bnef_battery_2030": 51, "inverter_2030": 52, "fee_per_customer": 55,
        "admin_costs": 56, "tariff": 59, "grid_arrival_tariff": 60, "amt_threshold": 63, "sizing_rounding": 64,
    }
    for name, row in rows.items():
        m: MoneyInput = getattr(c, name)
        if m.basis == "usd":
            h, i = m.value, m.value * fx
        elif m.basis == "usd_and_lcy":
            h, i = m.value, m.lcy_value
        else:  # lcy_contracted: K typed, L = K x base rate, I = L, H = I / exchange rate
            l = m.value * c.base_exchange_rate
            i, h = l, l / fx
        g = 0.0
        if m.vat == "capex":
            g = vat * (0 if a.tax.vat_capex == "Recoverable" else 1)
        elif m.vat == "opex":
            g = vat * (0 if a.tax.vat_opex == "Recoverable" else 1)
        s[f"Currency!H{row}"], s[f"Currency!I{row}"], s[f"Currency!G{row}"] = h, i, g
        s[f"Currency!F{row}"] = (h if c.case == 1 else i) * (1 + g)


def _portfolio(a: Assumptions, p: Prepared) -> None:
    s = p.s
    inherit = {
        "tariff": s["Currency!F59"], "capex_net_of_grant": s["Currency!F33"], "transfer_fee": s["Currency!F36"],
        "grant_per_connection": s["Currency!F34"], "battery_cost": s["Currency!F35"],
        "fixed_fee_per_grid": s["Currency!F39"], "fee_per_customer": s["Currency!F55"],
        "ratchet_share": a.opex.ratchet_share, "diesel_price": s["Currency!F40"],
    }
    lots = []
    for lot in a.lots:
        d = {k: (getattr(lot, k) if getattr(lot, k) is not None else v) for k, v in inherit.items()}
        f = lot.included
        grids, cpg = lot.grids * f, lot.connections_per_grid * f
        conns = lot.grids * lot.connections_per_grid * f
        lots.append({
            "grids": grids, "cpg": cpg, "conns": conns, "kwp": lot.kwp_per_grid * f,
            "people": lot.people_per_connection * f, "served": lot.grids * lot.connections_per_grid * lot.people_per_connection * f,
            "base": lot.baseline_kwh_month * f, "peak": lot.peak_kwh_month * f,
            "tariff": d["tariff"] * f, "capex": d["capex_net_of_grant"] * f, "fee": d["transfer_fee"] * f,
            "price": (d["capex_net_of_grant"] + d["transfer_fee"]) * f,
            "price_total": lot.grids * lot.connections_per_grid * d["capex_net_of_grant"] * f,
            "grant": d["grant_per_connection"] * f,
            "total_capex": (d["capex_net_of_grant"] + d["transfer_fee"] + d["grant_per_connection"]) * f,
            "w_per_conn": (lot.kwp_per_grid / lot.connections_per_grid * 1000 if lot.included == 1 else 0) * f,
            "module": lot.expansion_module_kw * f, "battery": d["battery_cost"] * f,
            "grid_fee": d["fixed_fee_per_grid"] * f, "cust_fee": d["fee_per_customer"] * f,
            "ratchet": d["ratchet_share"] * f, "diesel": d["diesel_price"] * f,
        })
    g = sum(l["grids"] for l in lots)
    n = sum(l["conns"] for l in lots)
    if g == 0 or n == 0:
        raise ValueError("Portfolio has no included grid or connection (#DIV/0! in Portfolio!S14)")

    def by_grids(k):
        return sum(l[k] * l["grids"] for l in lots) / g

    def by_conns(k):
        return sum(l[k] * l["conns"] for l in lots) / n

    s["Portfolio!S13"] = g
    s["Portfolio!S14"] = by_grids("cpg")
    s["Portfolio!S15"] = n
    s["Portfolio!S16"] = by_grids("kwp")
    s["Portfolio!S18"] = by_conns("people")
    s["Portfolio!S19"] = sum(l["served"] for l in lots)
    for row, k in ((22, "base"), (23, "peak"), (26, "tariff"), (29, "capex"), (30, "fee"), (31, "price"),
                   (34, "grant"), (35, "total_capex"), (37, "w_per_conn"), (40, "module"), (41, "battery"),
                   (45, "cust_fee"), (46, "ratchet"), (47, "diesel")):
        s[f"Portfolio!S{row}"] = by_conns(k)
    s["Portfolio!S32"] = sum(l["price_total"] for l in lots)
    # per-lot columns: E..J as typed or inherited, L..Q = E..J x included flag
    for lot, raw, ecol, lcol in zip(a.lots, lots, "EFGHIJ", "LMNOPQ"):
        f = lot.included
        e = {13: lot.grids, 14: lot.connections_per_grid, 15: lot.grids * lot.connections_per_grid,
             16: lot.kwp_per_grid, 18: lot.people_per_connection,
             19: lot.grids * lot.connections_per_grid * lot.people_per_connection,
             22: lot.baseline_kwh_month, 23: lot.peak_kwh_month, 40: lot.expansion_module_kw}
        for row, key in ((26, "tariff"), (29, "capex"), (30, "fee"), (31, "price"), (34, "grant"),
                         (35, "total_capex"), (37, "w_per_conn"), (41, "battery"), (44, "grid_fee"),
                         (45, "cust_fee"), (46, "ratchet"), (47, "diesel")):
            e[row] = raw[key] if f else None
        e[32] = lot.grids * lot.connections_per_grid * (raw["capex"] / f if f else 0)
        for row, val in e.items():
            if val is not None:
                s[f"Portfolio!{ecol}{row}"] = val
                s[f"Portfolio!{lcol}{row}"] = val * f
        s[f"Portfolio!{lcol}9"] = f
    s["Portfolio!S44"] = by_grids("grid_fee")
    p.lots = lots


def _tables(a: Assumptions, p: Prepared) -> None:
    """Calendar-year tables that the Currency sheet already needs (FX)."""
    y0 = X.year(X.to_serial(a.timing.model_start) + 1)
    years = [y0 + i for i in range(31)]  # Inputs!I393:AM393 (and 192, 198, 205, 401)
    for r in (192, 198, 205, 393, 401):
        p.tables[f"Inputs!{r}"] = years
    lcy = [a.currency.base_exchange_rate]  # Inputs!402
    for _ in range(30):
        lcy.append(lcy[-1] * (1 + a.macro.fx_depreciation))
    p.tables["Inputs!402"] = lcy
    p.tables["Inputs!403"] = [1.0] + [v / lcy[0] for v in lcy[1:]]  # I403 typed 1


def prepare(a: Assumptions, options: EngineOptions = FAITHFUL) -> Prepared:
    p = Prepared()
    p.options = options
    s = p.s
    _tables(a, p)
    _currency(a, p)
    _portfolio(a, p)
    # Currency!H67: equity-injection check cap = 1 % x USD capex x connections x grids
    s["Currency!H67"] = 0.01 * s["Currency!H33"] * s["Portfolio!S14"] * s["Portfolio!S13"]
    s["Currency!I67"] = s["Currency!H67"] * s["Currency!F14"]
    s["Currency!F67"] = s["Currency!H67"] if a.currency.case == 1 else s["Currency!I67"]
    s["Model!F281"] = s["Currency!F67"]
    t, tech, k = a.timing, a.technical, a.constants
    months, days, thousand = k.months_per_year, k.days_per_year, k.thousand
    s["Names!F12"], s["Names!F13"], s["Names!F17"] = days, months, thousand

    # --- portfolio sizing
    s["Inputs!E24"] = s["Portfolio!S13"]
    s["Inputs!E30"] = s["Portfolio!S14"]
    s["Inputs!E25"] = s["Inputs!E24"] * s["Inputs!E30"]
    s["Inputs!E26"] = s["Portfolio!S18"]
    s["Inputs!E27"] = s["Inputs!E26"] * s["Inputs!E25"]
    s["Inputs!E31"] = s["Portfolio!S35"]
    s["Inputs!E33"] = s["Inputs!E30"] * s["Inputs!E31"]
    s["Inputs!E38"] = s["Portfolio!S16"]  # = Dashboard!E9
    s["Inputs!E32"] = s["Inputs!E33"] / s["Inputs!E38"] / thousand
    s["Inputs!E39"] = tech.yield_kwh_per_kwp
    s["Inputs!E41"] = s["Inputs!E38"] * tech.yield_kwh_per_kwp / days
    s["Inputs!E43"] = s["Inputs!E38"] * tech.yield_kwh_per_kwp
    s["Inputs!E42"] = s["Inputs!E43"] / months
    s["Inputs!E45"] = s["Currency!F44"]
    s["Inputs!E46"] = s["Inputs!E45"] * s["Inputs!E38"] * thousand
    s["Inputs!E57"] = s["Inputs!E41"] * tech.night_battery_share
    s["Inputs!E59"] = s["Inputs!E57"] / tech.battery_discharge_limit
    s["Inputs!E63"] = s["Portfolio!S41"]
    s["Inputs!E60"] = s["Inputs!E63"] * s["Inputs!E59"]
    s["Inputs!E64"] = s["Currency!F45"]
    s["Inputs!E65"] = s["Inputs!E63"] - s["Inputs!E64"]
    s["Inputs!E67"] = s["Inputs!E59"] * s["Inputs!E63"]
    s["Inputs!E69"] = s["Portfolio!S41"]
    s["Inputs!E70"] = s["Currency!F45"]
    s["Inputs!E71"] = s["Currency!F46"]
    s["Inputs!E75"] = s["Currency!F48"]
    s["Inputs!E76"] = s["Inputs!E38"] * tech.inverter_sizing
    s["Inputs!E86"] = s["Portfolio!S47"]
    # --- expansion module
    s["Inputs!E106"] = s["Portfolio!S40"]
    s["Inputs!E107"] = s["Inputs!E106"] * tech.yield_kwh_per_kwp / days
    s["Inputs!E109"] = s["Inputs!E106"] * tech.yield_kwh_per_kwp
    s["Inputs!E108"] = s["Inputs!E109"] / months
    s["Inputs!E111"] = s["Inputs!E107"] * tech.night_battery_share
    s["Inputs!E112"] = s["Inputs!E111"] / tech.battery_discharge_limit
    s["Inputs!E114"] = s["Inputs!E106"] * tech.inverter_sizing
    s["Inputs!E117"] = s["Inputs!E106"] * s["Inputs!E45"] * thousand
    s["Inputs!E118"] = s["Inputs!E112"] * s["Inputs!E63"]
    s["Inputs!E119"] = s["Inputs!E75"] * s["Inputs!E114"] * thousand
    s["Inputs!E120"] = s["Currency!F49"]
    s["Inputs!E121"] = s["Currency!F50"]
    s["Inputs!E122"] = sum(s[f"Inputs!E{r}"] for r in range(117, 122))
    s["Inputs!E128"] = s["Portfolio!S31"]
    s["Inputs!E129"] = s["Inputs!E128"] * s["Inputs!E30"]
    s["Inputs!E131"] = s["Portfolio!S35"]
    s["Inputs!E132"] = s["Inputs!E131"] * s["Inputs!E30"]

    # --- build profile, Inputs!I134:N143 (construction years 1..6)
    e136 = s["Inputs!E24"]  # = Dashboard!E7
    s["Inputs!E136"] = e136
    prof = [0.0 if v is None else v for v in a.build.build_profile]
    inc, tot, rem = [], [], []
    prev_tot = 0.0  # H140 is empty
    for i in range(6):
        r141 = max(e136 - prev_tot, 0)
        r136 = min(X.xround(e136 * prof[i], 0), r141)
        prev_tot = prev_tot + r136
        rem.append(r141), inc.append(r136), tot.append(prev_tot)
    p.tables.update({"Inputs!134": [1, 2, 3, 4, 5, 6], "Inputs!136": inc, "Inputs!140": tot, "Inputs!141": rem,
                     "Inputs!137": [s["Inputs!E129"] * x for x in inc],
                     "Inputs!138": [s["Inputs!E132"] * x for x in inc],
                     "Inputs!143": [x * s["Inputs!E30"] for x in inc]})
    s["Inputs!G140"] = max(tot)
    s["Inputs!G141"] = s["Inputs!G140"] - s["Inputs!E24"]
    s["Inputs!E10"] = sum(1 for x in inc if x > 0)  # COUNTIF(I136:N136,">0")

    # --- dates
    con_start = X.to_serial(t.construction_start)
    s["Inputs!E6"] = X.to_serial(t.model_start)
    s["Inputs!E9"] = con_start
    s["Inputs!E11"] = X.eomonth(con_start, s["Inputs!E10"] * months - 1)
    s["Inputs!E14"] = t.project_duration_years
    if options.fix_ops_start:
        s["Inputs!E17"] = X.eomonth(con_start, t.project_duration_years * months - 1) + 1
    else:
        s["Inputs!E17"] = X.eomonth(con_start, t.project_duration_years * (months - 1)) + 1
    s["Inputs!E18"] = t.lifetime_years
    s["Inputs!E19"] = X.eomonth(s["Inputs!E11"], t.lifetime_years * months)

    # --- revenue ramp-up by grid, Inputs!I148:R157 (operations years 1..10)
    inc10 = inc + [0.0] * 4  # O136:R136 are empty
    ru = a.build.ramp_up
    r149 = [inc10[i] * ru[0] * a.build.ramp_discount for i in range(10)]
    r150 = [0.0] + [inc10[i - 1] * ru[1] for i in range(1, 10)]
    r151 = [0.0, 0.0] + [inc10[i - 2] * ru[2] for i in range(2, 10)]
    r152 = [0.0, 0.0, 0.0] + [sum(inc10[: i - 2]) * ru[3] for i in range(3, 10)]
    r154 = [r149[i] + r150[i] + r151[i] + r152[i] for i in range(10)]
    r156 = [1 if s["Inputs!G140"] == r154[i] else 0 for i in range(10)]
    r157, cum = [], 0
    for i in range(10):
        cum += r156[i]
        r157.append(1 if cum == 1 else 0)
    p.tables.update({"Inputs!148": list(range(1, 11)), "Inputs!149": r149, "Inputs!150": r150,
                     "Inputs!151": r151, "Inputs!152": r152, "Inputs!154": r154, "Inputs!156": r156,
                     "Inputs!157": r157})
    s["Inputs!E157"] = sum(y for y, f in zip(range(1, 11), r157) if f == 1)

    # --- demand, tariff, opex
    s["Inputs!E163"] = s["Portfolio!S22"]
    s["Inputs!E164"] = s["Inputs!E163"] * months
    s["Inputs!E162"] = s["Inputs!E164"] / days * thousand
    s["Inputs!E166"] = a.demand.growth_base + a.demand.growth_sensitivity
    s["Inputs!I170"] = s["Portfolio!S26"]
    s["Inputs!E170"] = s["Inputs!I170"] * (1 + a.demand.tariff_sensitivity)
    s["Inputs!E173"] = s["Portfolio!S44"]
    s["Inputs!E176"] = s["Portfolio!S45"]
    p.tables["Inputs!175"] = list(a.opex.fee_thresholds)
    p.tables["Inputs!176"] = [s["Inputs!E176"]] * 4
    s["Inputs!E179"] = s["Currency!F56"]

    # --- cost forecasts by calendar year (I..AM; decline until P = 2030, flat after)
    def decline(first, rate, p_override=None):
        out = [first]
        for i in range(1, 31):
            if i <= 6:
                out.append(out[-1] * (1 - rate))
            elif i == 7:
                out.append(out[-1] * (1 - rate) if p_override is None else p_override)
            else:
                out.append(out[-1])
        return out

    s["Inputs!E194"] = s["Currency!F44"]
    p.tables["Inputs!193"] = decline(s["Inputs!E194"], a.replacement.pv_cost_decline)
    s["Inputs!E202"] = s["Currency!F47"]
    p.tables["Inputs!199"] = decline(s["Inputs!E202"], a.replacement.battery_cost_decline)
    # E200 = -((U200/I200)^(1/(U198-I198)) - 1); U200 sits in the flat part = Currency!F51
    yrs = p.tables["Inputs!198"]
    s["Inputs!E200"] = -((s["Currency!F51"] / s["Inputs!E202"]) ** (1 / (yrs[12] - yrs[0])) - 1)
    p.tables["Inputs!200"] = decline(s["Inputs!E202"], s["Inputs!E200"], p_override=s["Currency!F51"])
    names = ["AssetCo Forecast", "BNEF New Energy Outlook 2018 forecast for Lithium-Ion batteries"]
    pick = X.lookup_text(a.replacement.battery_forecast, names, [0, 1])
    p.tables["Inputs!201"] = list(p.tables["Inputs!199"] if pick == 0 else p.tables["Inputs!200"])
    s["Inputs!E207"] = s["Currency!F48"]
    inv0 = s["Inputs!E207"] * (1 - a.replacement.inverter_cost_decline) ** (yrs[0] - a.replacement.inverter_reference_year)
    p.tables["Inputs!206"] = decline(inv0, a.replacement.inverter_cost_decline, p_override=s["Currency!F52"])

    # --- tax and depreciation rates
    tx = a.tax
    s["Inputs!E239"] = 1 / tx.book_life_initial
    s["Inputs!E242"] = a.replacement.battery_life
    s["Inputs!E243"] = 1 / s["Inputs!E242"]
    s["Inputs!E246"] = tx.book_life_initial
    s["Inputs!E247"] = 1 / s["Inputs!E246"]
    s["Inputs!E252"] = 1 / tx.tax_life_initial
    s["Inputs!E256"] = 1 / tx.tax_life_replacement
    s["Inputs!E259"] = tx.tax_life_initial
    s["Inputs!E260"] = 1 / s["Inputs!E259"]
    s["Inputs!E231"] = s["Currency!F63"]

    # --- funding (the parts that do not depend on the timeline results)
    s["Inputs!E270"] = s["Portfolio!S34"] * s["Inputs!E25"]
    s["Inputs!E283"] = 1 - a.funding.developer_stake
    s["Inputs!E288"] = 1 - a.funding.owner_equity_provision
    d = a.debt
    s["Inputs!L292"] = s["Currency!F64"]
    s["Inputs!L300"] = s["Currency!F64"]
    s["Inputs!G296"] = 1 - d.gearing
    s["Inputs!E297"] = a.pasted.funding * d.gearing
    s["Inputs!G297"] = a.pasted.funding * s["Inputs!G296"]
    s["Inputs!E304"] = (s["Inputs!E297"] if d.sizing_method == "Gearing" else a.pasted.dscr_limit) * d.debt_switch
    s["Inputs!E276"] = a.pasted.funding - s["Inputs!E304"]
    s["Inputs!E277"] = s["Inputs!E276"] - s["Inputs!E270"]
    s["Inputs!E279"] = s["Inputs!E277"]
    # interest tables: periods I..L
    p.tables["Inputs!313"] = [1, 2, 3, 4]
    p.tables["Inputs!314"] = list(d.margin_by_period) if d.margin_by_period else [d.margin] * 4
    p.tables["Inputs!315"] = list(d.fixed_rate_by_period) if d.fixed_rate_by_period else [s["Currency!F29"]] * 4
    s["Inputs!I310"] = s["Currency!F29"]
    s["Inputs!E321"] = d.commitment_fee_share * d.margin
    s["Inputs!G332"] = 0.5 if (d.debt_switch == 1 and d.gearing > 0 and d.drawdown == "Pari Passu") else 0.0
    r = a.refi
    s["Inputs!G340"] = 1 - r.gearing
    s["Inputs!E341"] = a.pasted.funding * r.gearing
    s["Inputs!G341"] = a.pasted.funding * s["Inputs!G340"]
    s["Inputs!G348"] = r.on
    s["Inputs!E348"] = (s["Inputs!E341"] if r.sizing_method == "Gearing" else a.pasted.refi_limit) * r.on
    p.tables["Inputs!353"] = [1, 2, 3, 4]
    p.tables["Inputs!354"] = [r.margin] * 4
    p.tables["Inputs!355"] = [s["Currency!F29"]] * 4
    s["Inputs!E361"] = r.commitment_fee_share * r.margin
    s["Inputs!E367"] = d.target_dscr
    res = a.reserves
    if res.dsra_months / months > 1:
        raise X.ExcelNA("Inputs!E375: DSRA provision above 12 months (#N/A)")
    s["Inputs!E375"] = res.dsra_months / months
    s["Inputs!E378"] = (s["Inputs!E11"] + con_start) / 2
    s["Inputs!E380"] = s["Inputs!E17"]
    s["Inputs!E386"] = s["Currency!F28"]

    # --- FX tables
    fx_rows = {1: p.tables["Inputs!402"], 2: p.tables["Inputs!403"]}
    r394 = fx_rows[a.macro.fx_case]
    s["Inputs!E397"] = a.currency.effective_year
    g397 = X.lookup(s["Inputs!E397"], p.tables["Inputs!393"], r394)
    r397 = [v / g397 for v in r394]
    r398 = [1 / v for v in r397]
    p.tables.update({"Inputs!394": r394, "Inputs!397": r397, "Inputs!398": r398,
                     "Inputs!399": [1 / v for v in r398]})

    # --- consumption profiles by operations year (I..AL = years 1..30, H432 = 0)
    e414 = None
    base, peak = s["Portfolio!S22"], s["Portfolio!S23"]
    e414 = (peak - base) / math.log(5)
    r414 = [base] + [e414 * math.log(y) + base for y in (2, 3, 4)] + [peak] * 26
    r416 = []
    for i in range(30):
        prev = r414[i - 1] if i > 0 else 0.0
        nxt = r414[i + 1] if i < 29 else 0.0
        r416.append(1 if (r414[i] == nxt and prev < r414[i]) else 0)
    g = s["Inputs!E166"]
    r420 = [(1 + g) ** i for i in range(30)]
    r421 = [s["Inputs!E163"] * x for x in r420]
    r425, prev = [], 0.0
    for i in range(30):
        prev = 1.0 if r416[i] == 1 else prev * (1 + a.demand.income_growth)
        r425.append(prev)
    r426 = [r414[i] if r425[i] == 0 else r414[i] * r425[i] for i in range(30)]
    cases = {1: r414, 2: r421, 3: r426}
    r433 = cases[a.demand.consumption_case]
    p.tables.update({"Inputs!414": r414, "Inputs!416": r416, "Inputs!420": r420, "Inputs!421": r421,
                     "Inputs!425": r425, "Inputs!426": r426, "Inputs!433": r433,
                     "Inputs!434": [v * months for v in r433], "Inputs!432": list(range(1, 31))})
    s["Inputs!E414"] = e414

    # --- grid arrival
    s["Inputs!E439"] = X.eomonth(s["Inputs!E11"], a.exit.years_before_grid_arrival * months) + 1
    s["Inputs!E441"] = s["Currency!F60"]
    return p
