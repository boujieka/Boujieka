"""Annual timeline calculations of the AssetCo model (Model, Debt, FinStat sheets).

Faithful reproduction of the reference workbook: each series is stored under
its workbook row (``Model!87`` = revenue) over the 69 timeline columns J..BZ
(calendar years 2023..2091 in the published case). ``totals`` holds the
column-I values the workbook keeps for some rows (row totals or anchors).

Calculation order (the workbook is acyclic once the macro-pasted values are
taken as inputs, see docs/formula_dependency_map.md):
  1. timeline flags and counters
  2. portfolio profile (construction, purchase, grids in service)
  3. operations: production, losses, consumption, diesel, expansion,
     battery and inverter replacement  (independent of financing)
  4. revenue, opex, working capital, VAT
  5. financing pass, year by year: uses, sources, senior and refinanced debt,
     depreciation, P&L, tax, cash waterfall down to CFADS, debt sculpting
  6. reserves pass, year by year: DSRA, MMRA, distributions
  7. returns, financial statements, dashboard outputs
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import excel as X
from .assumptions import Assumptions
from .options import FAITHFUL, EngineOptions
from .prepare import Prepared, prepare

T = 69  # timeline columns J..BZ
VERY_SMALL = 1e-7  # Names!F19


@dataclass
class Ledger:
    v: dict = field(default_factory=dict)       # "Model!87" -> [69 values]
    totals: dict = field(default_factory=dict)  # "Model!87" -> column I value
    s: dict = field(default_factory=dict)       # single cells, e.g. "Model!E375"

    def new(self, key: str, fill: float = 0.0) -> list:
        arr = [fill] * T
        self.v[key] = arr
        return arr

    def __getitem__(self, key: str) -> list:
        return self.v[key]


def _lookback(arr: list, t: int, width: int, col_i: float = 0.0) -> float:
    """SUM(OFFSET(<previous column>,0,0,1,-width)): columns t-width .. t-1;
    index -1 is column I (row total or empty)."""
    tot = 0.0
    for k in range(t - width, t):
        tot += col_i if k == -1 else (arr[k] if k >= 0 else 0.0)
    return tot


def _window(rows: list[list], t: int, width: int) -> float:
    """SUM(OFFSET(<current column>,0,0,len(rows),-width)): columns t-width+1 .. t."""
    return sum(r[k] for r in rows for k in range(t - width + 1, t + 1) if k >= 0)


def _fwd(arr: list, t: int, n: int) -> list:
    """Values of the next n columns that exist (cells beyond BZ are empty)."""
    return arr[t + 1: t + 1 + n]


def run_model(a: Assumptions, p: Prepared | None = None, options: EngineOptions = FAITHFUL) -> Ledger:
    p = p or prepare(a, options)
    opts = getattr(p, "options", options)
    S = p.s
    tb = p.tables
    L = Ledger()
    v = L.v
    months, days, thousand = S["Names!F13"], S["Names!F12"], S["Names!F17"]
    con_start, cons_end = S["Inputs!E9"], S["Inputs!E11"]
    ops_start, ops_end = S["Inputs!E17"], S["Inputs!E19"]
    case = S["Currency!F18"]

    # ------------------------------------------------------------ 1. timeline
    r4, r5 = L.new("Model!4"), L.new("Model!5")
    prev_end = S["Inputs!E6"]  # Model!I5
    for t in range(T):
        r4[t] = prev_end + 1
        r5[t] = X.eomonth(r4[t], months - 1)
        prev_end = r5[t]
    r6 = L.new("Model!6"); r7 = L.new("Model!7")
    r10 = L.new("Model!10"); r11 = L.new("Model!11"); r13 = L.new("Model!13"); r14 = L.new("Model!14")
    r15 = L.new("Model!15"); r16 = L.new("Model!16"); r17 = L.new("Model!17")
    r18 = L.new("Model!18"); r19 = L.new("Model!19"); r20 = L.new("Model!20")
    c6 = c7 = c18 = 0
    for t in range(T):
        r6[t] = 1 if (r4[t] >= con_start and r5[t] <= cons_end) else 0
        r7[t] = 1 if (r4[t] >= ops_start and r5[t] <= ops_end) else 0
        r10[t] = r5[t] - r4[t] + 1
        r11[t] = X.year(r4[t])
        c6 += r6[t]; c7 += r7[t]
        r13[t] = c6 * r6[t]
        r14[t] = c7 * r7[t]
        r15[t] = 1.0 if t == 0 else r15[t - 1] * (1 + a.macro.inflation)  # J15 typed 1
        r16[t] = X.lookup(r11[t], tb["Inputs!393"], tb["Inputs!398"])
        r17[t] = X.lookup(r11[t], tb["Inputs!393"], tb["Inputs!399"])
        r18[t] = 1 if (r4[t] >= con_start and r5[t] <= ops_end) else 0
        c18 += r18[t]
        r19[t] = c18 * r18[t]
        r20[t] = 1 if S["Inputs!E10"] == r13[t] else 0

    # ------------------------------------------------- 2. portfolio profile
    r175 = L.new("Model!175"); r176 = L.new("Model!176"); r179 = L.new("Model!179")
    r182 = L.new("Model!182"); r183 = L.new("Model!183"); r184 = L.new("Model!184")
    r185 = L.new("Model!185"); r187 = L.new("Model!187"); r188 = L.new("Model!188")
    for t in range(T):
        r175[t] = r13[t]
        r176[t] = 0 if r175[t] == 0 else X.lookup(r175[t], tb["Inputs!134"], tb["Inputs!136"])
    for t in range(T):
        r179[t] = r176[t - 1] if t > 0 else 0.0
        r183[t] = r179[t]
    L.totals["Model!183"] = sum(r183)
    for t in range(T):
        r182[t] = r185[t - 1] if t > 0 else 0.0
        r187[t] = min(r19[t], S["Inputs!E18"])
        w = int(r187[t])
        # J188 reads I183, the row total (workbook quirk, audit observation 8)
        r188[t] = 0.0 if w == 0 else _lookback(r183, t, w, L.totals["Model!183"])
        r184[t] = min(r188[t] - (r185[t - 1] if t > 0 else 0.0), 0)
        r185[t] = r182[t] + r183[t] + r184[t]
    r23 = L.new("Model!23"); r24 = L.new("Model!24"); r25 = L.new("Model!25")
    r26 = L.new("Model!26"); r27 = L.new("Model!27")
    for t in range(T):
        r23[t] = r185[t]
        r24[t] = 0 if r14[t] == 0 else X.lookup(r14[t], tb["Inputs!148"], tb["Inputs!154"])
        r25[t] = min(r23[t], r24[t])
        r26[t] = r25[t] * S["Inputs!E30"]
        r27[t] = (r23[t - 1] if t > 0 else 0.0) * S["Inputs!E30"]

    # --------------------------------------------------- consumption (pre-ops)
    r52 = L.new("Model!52"); r56 = L.new("Model!56"); r57 = L.new("Model!57")
    r59 = L.new("Model!59"); r60 = L.new("Model!60")
    keys432 = [0] + tb["Inputs!432"]
    vals433 = [0.0] + tb["Inputs!433"]  # H433 is empty
    for t in range(T):
        r52[t] = X.lookup(r14[t], keys432, vals433)
        r56[t] = r52[t]
        r57[t] = r56[t] * months
        r59[t] = r26[t]
        r60[t] = r57[t] * r59[t]
    L.totals["Model!60"] = sum(r60)

    # identical timeline headers on the Debt, FinStat and Graph sheets
    for sheet in ("Debt", "Graph sheet"):
        for r in (4, 5, 6, 7, 10, 11, 13, 14):
            L.v[f"{sheet}!{r}"] = list(L.v[f"Model!{r}"])
    L.v["Debt!16"], L.v["Debt!17"] = list(r18), list(r19)
    L.v["Debt!3"] = list(r19)   # =J17
    L.v["Model!3"] = list(r19)  # =J19
    for r_fs, r_m in ((4, 4), (5, 5), (7, 6), (8, 7)):
        L.v[f"FinStat!{r_fs}"] = list(L.v[f"Model!{r_m}"])
    L.options = opts
    _operations(a, S, tb, L)
    _revenue_opex(a, S, tb, L)
    _financing(a, S, tb, L)
    _reserves(a, S, tb, L)
    _returns(a, S, tb, L)
    _finstat(a, S, L)
    _dashboard(a, S, L)
    L.s.update({k: val for k, val in S.items()})
    return L


# ===================================================================== operations
def _operations(a: Assumptions, S: dict, tb: dict, L: Ledger) -> None:
    v = L.v
    months, days, thousand = S["Names!F13"], S["Names!F12"], S["Names!F17"]
    tech = a.technical
    r4, r5, r6, r7, r11 = v["Model!4"], v["Model!5"], v["Model!6"], v["Model!7"], v["Model!11"]
    r16, r17, r19, r23, r25, r26 = v["Model!16"], v["Model!17"], v["Model!19"], v["Model!23"], v["Model!25"], v["Model!26"]
    r60, r176 = v["Model!60"], v["Model!176"]
    case = S["Currency!F18"]
    module_kw = S["Inputs!E106"]
    names = {n: L.new(f"Model!{n}") for n in (
        30, 31, 33, 37, 40, 41, 43, 45, 46, 48, 49, 587, 590, 591, 592, 593, 594, 595, 598, 599, 600,
        604, 606, 608, 609, 610, 611, 613, 614, 616, 617, 618, 619, 621, 623, 626, 627, 628, 630, 633,
        634, 637, 638, 639, 642, 643, 644, 645, 646, 647, 649, 652, 653, 654, 655, 657, 661, 662, 663,
        666, 667, 668, 669, 670, 672, 673, 675, 676, 677, 680, 684, 685, 686, 688, 689, 691, 693, 695,
        698, 699, 700, 703, 705, 706, 707, 710, 711, 712, 715, 716, 717, 718, 721, 722, 725, 726, 727,
        728, 729, 731, 734, 735, 737, 738, 739, 742, 743, 744, 745, 746, 747, 749, 752, 753, 754, 755,
        758, 759, 760, 761, 762, 763, 765, 766, 769, 770, 771, 772, 775, 776)}
    m = names
    r15 = v["Model!15"]
    # rows 715/752: live flag from construction start to operations end
    c715 = 0
    for t in range(T):
        m[715][t] = 1 if (r4[t] >= S["Inputs!E9"] and r5[t] <= S["Inputs!E19"]) else 0
        m[752][t] = m[715][t]
        c715 += m[715][t]
        m[716][t] = c715 * m[715][t]
        m[753][t] = m[716][t]
        m[717][t] = r176[t]
        m[754][t] = r176[t]
    L.totals["Model!715"] = sum(m[715])
    L.totals["Model!752"] = sum(m[752])
    f718 = L.totals["Model!715"] - a.replacement.stop_before_end  # Model!F718
    L.s["Model!F718"] = f718
    L.s["Model!F755"] = L.totals["Model!752"] - a.replacement.stop_before_end
    for t in range(T):
        m[718][t] = (1 if f718 >= m[716][t] else 0) * m[715][t]
        m[755][t] = (1 if f718 >= m[716][t] else 0) * m[715][t]  # uses the battery rows (as the workbook)

    for t in range(T):
        prev = lambda r: m[r][t - 1] if t > 0 else 0.0  # noqa: E731
        m[587][t] = r19[t]
        # --- PV capacity at start of period
        m[590][t] = prev(595)
        m[591][t] = S["Inputs!E38"] * r176[t]
        m[594][t] = prev(600)
        m[30][t] = m[590][t]
        m[31][t] = m[30][t] / module_kw
        m[604][t] = m[590][t] * tech.yield_kwh_per_kwp * r7[t]
        m[33][t] = m[604][t]
        m[37][t] = -tech.self_consumption_kwh_day * m[31][t] * days * r7[t]
        m[40][t] = -tech.meter_consumption_kwh_day * r26[t] * days * r7[t]
        m[41][t] = m[40][t] * (1 + 1e-05)  # Model!E41: hard-coded factor (audit 3.2)
        m[43][t] = r60[t] * (-tech.distribution_losses)
        m[45][t] = m[43][t] + m[41][t] + m[37][t]
        m[46][t] = 0 if m[33][t] == 0 else m[45][t] / m[33][t]
        m[48][t] = m[33][t] + m[45][t]
        m[49][t] = 0 if m[31][t] == 0 else m[48][t] / m[31][t]
        # --- diesel per site
        m[661][t] = m[604][t]
        m[662][t] = X.xround(r25[t], 0)
        m[663][t] = 0 if m[662][t] == 0 else m[661][t] / m[662][t]
        m[666][t] = -m[37][t]
        m[667][t] = -m[41][t]
        m[668][t] = -m[43][t]
        m[669][t] = r60[t]
        m[670][t] = m[666][t] + m[667][t] + m[668][t] + m[669][t]
        m[672][t] = m[670][t] - m[669][t]
        m[673][t] = 0 if m[661][t] == 0 else m[672][t] / m[661][t]
        m[675][t] = m[590][t] / S["Inputs!E38"] * r7[t]
        m[676][t] = 0 if m[675][t] == 0 else m[670][t] / m[675][t]
        m[677][t] = 0 if m[662][t] == 0 else m[670][t] / m[662][t]
        m[680][t] = 0 if m[663][t] == 0 else m[677][t] / m[663][t]
        m[684][t] = (1 if tech.diesel_threshold < m[680][t] else 0) * r7[t]
        m[685][t] = tech.diesel_threshold * m[663][t]
        m[686][t] = (m[677][t] - m[685][t]) * m[684][t]
        m[688][t] = min(m[685][t], m[677][t]) * tech.diesel_share_below
        m[689][t] = m[686][t] * tech.diesel_share_above
        m[691][t] = m[688][t] + m[689][t]
        m[693][t] = m[691][t] / tech.diesel_kwh_per_litre
        m[695][t] = m[693][t] / tech.diesel_litres_per_hour
        m[698][t] = m[691][t] * m[662][t]
        m[699][t] = m[693][t] * m[662][t]
        m[700][t] = m[695][t] * m[662][t]
        m[703][t] = S["Inputs!E86"] * m[693][t]
        m[705][t] = (1 if case == 1 else r17[t]) * r7[t]
        m[706][t] = m[703][t] * m[705][t]
        m[707][t] = m[706][t] * m[662][t]
        m[710][t] = (0 if r23[t] == 0 else m[33][t] / r23[t]) * r7[t]
        m[711][t] = tech.max_diesel_share * m[710][t]
        m[712][t] = max(m[691][t] - m[711][t], 0)
        # --- expansion modules
        m[606][t] = 1 if (r7[t] == 1 and r6[t] == 0) else 0
        m[608][t] = m[48][t]
        m[609][t] = m[698][t]
        m[610][t] = -(r60[t + 1] if t + 1 < T else 0.0) * r7[t]
        m[611][t] = m[608][t] + m[609][t] + m[610][t]
        m[613][t] = min(0, m[611][t]) * m[606][t]
        m[614][t] = -X.roundup(m[613][t] / S["Inputs!E109"], 0)
        m[616][t] = m[712][t]
        m[617][t] = m[616][t] * r23[t] * r7[t]
        m[618][t] = m[49][t]
        m[619][t] = 0 if m[618][t] == 0 else X.roundup(m[617][t] / m[618][t], 0)
        m[621][t] = max(m[619][t], m[614][t])
        m[623][t] = m[621][t] * module_kw
        m[592][t] = m[623][t]
        m[595][t] = m[590][t] + m[591][t] + m[592][t] + m[593][t] + m[594][t]
        m[598][t] = min(m[587][t], a.timing.lifetime_years)
        w = int(m[598][t])
        m[599][t] = 0 if w == 0 else _window([m[591], m[592], m[593]], t, w)
        m[600][t] = -max((m[595][t] - m[599][t]) * r7[t], 0)
        # --- expansion capex
        m[626][t] = X.lookup(r11[t], tb["Inputs!192"], tb["Inputs!193"]) * r7[t]
        m[731][t] = X.lookup(r11[t], tb["Inputs!198"], tb["Inputs!201"])
        m[775][t] = X.lookup(r11[t], tb["Inputs!205"], tb["Inputs!206"])
        m[627][t] = m[731][t] * r7[t]
        m[628][t] = m[775][t] * r7[t]
        m[630][t] = (1 if case == 1 else r17[t]) * r7[t]
        m[633][t] = (1 if case == 2 else r16[t]) * r7[t]
        m[634][t] = r15[t] * r7[t]
        m[637][t] = m[626][t] * m[630][t]
        m[638][t] = m[627][t] * m[630][t]
        m[639][t] = m[628][t] * m[630][t]
        m[642][t] = module_kw * m[637][t] * thousand
        m[643][t] = S["Inputs!E112"] * m[638][t]
        m[644][t] = S["Inputs!E114"] * m[639][t] * thousand
        # racking row left empty in the workbook (audit observation); option adds it
        m[645][t] = S["Inputs!E120"] * m[630][t] * r7[t] if L.options.include_expansion_racking else 0.0
        m[646][t] = S["Inputs!E121"] * r7[t] * m[633][t] * m[634][t]
        m[647][t] = m[642][t] + m[643][t] + m[644][t] + m[645][t] + m[646][t]
        m[649][t] = m[647][t] * m[621][t]
        m[652][t] = m[608][t]
        m[653][t] = m[609][t]
        m[654][t] = -r60[t]
        m[655][t] = m[652][t] + m[653][t] + m[654][t]
        m[657][t] = m[655][t] >= 0
        # --- batteries
        m[721][t] = m[621][t]
        m[722][t] = S["Inputs!E112"] * m[721][t]
        m[725][t] = min(m[716][t], a.replacement.battery_life)
        m[729][t] = S["Inputs!E59"] * m[717][t] * r6[t]
        m[742][t] = prev(747)
        m[743][t] = S["Inputs!E59"] * m[717][t] * r6[t]
        m[744][t] = m[722][t]
        m[745][t] = prev(728) * r7[t]
        m[746][t] = prev(727) * r7[t]
        m[747][t] = m[742][t] + m[743][t] + m[744][t] + m[745][t] + m[746][t]
        w = int(m[725][t])
        m[726][t] = 0 if w == 0 else _window([m[743], m[744], m[745]], t, w)
        m[727][t] = -max((m[747][t] - m[726][t]) * r7[t], 0)
        m[728][t] = max((m[747][t] - m[726][t]) * r7[t], 0) * m[718][t]
        m[734][t] = (1 if case == 2 else r16[t]) * r7[t]
        m[735][t] = r15[t] * r7[t]
        m[737][t] = -m[731][t] * m[728][t] * m[630][t]
        m[738][t] = -S["Inputs!E71"] * m[728][t] * m[734][t] * m[735][t]
        m[739][t] = m[737][t] + m[738][t]
        m[749][t] = m[737][t] + m[738][t]
        # --- inverters
        m[758][t] = prev(763)
        m[759][t] = S["Inputs!E76"] * r6[t] * m[754][t]
        m[765][t] = m[621][t]
        m[766][t] = S["Inputs!E114"] * m[765][t]
        m[760][t] = m[766][t]
        m[761][t] = prev(772) * r7[t]
        m[762][t] = prev(771) * r7[t]
        m[763][t] = m[758][t] + m[759][t] + m[760][t] + m[761][t] + m[762][t]
        m[769][t] = min(m[716][t], a.replacement.inverter_life)
        w = int(m[769][t])
        m[770][t] = 0 if w == 0 else _window([m[759], m[760], m[761]], t, w)
        m[771][t] = -max((m[763][t] - m[770][t]) * r7[t], 0)
        m[772][t] = max((m[763][t] - m[770][t]) * r7[t], 0) * m[718][t]
        m[776][t] = -m[775][t] * m[772][t] * thousand * m[630][t]
    for r in (33, 37, 40, 41, 43, 45, 48, 49, 591, 592, 593, 594, 604, 608, 609, 610, 611, 613, 614, 616,
              617, 618, 649, 652, 653, 654, 655, 661, 666, 667, 668, 669, 670, 672, 686, 688, 689, 691,
              693, 695, 698, 699, 700, 703, 706, 707, 710, 712, 717, 718, 721, 722, 737, 738, 739, 746,
              749, 752, 754, 755, 762, 765, 766, 776):
        L.totals[f"Model!{r}"] = sum(m[r])
    L.s["Model!F693"] = X.average_nonzero(m[693])
    L.s["Model!F695"] = X.average_nonzero(m[695])
    L.s["Model!F703"] = X.average_nonzero(m[706])


# ================================================================= revenue & opex
def _revenue_opex(a: Assumptions, S: dict, tb: dict, L: Ledger) -> None:
    v = L.v
    months, days = S["Names!F13"], S["Names!F12"]
    case = S["Currency!F18"]
    r4, r6, r7, r14, r15, r16, r17 = (v[f"Model!{n}"] for n in (4, 6, 7, 14, 15, 16, 17))
    r23, r26, r52, r60, r185 = v["Model!23"], v["Model!26"], v["Model!52"], v["Model!60"], v["Model!185"]
    m = {n: L.new(f"Model!{n}") for n in (
        63, 65, 66, 67, 69, 72, 73, 75, 77, 79, 80, 83, 84, 85, 87, 89, 90, 92, 97, 98, 99, 100, 101,
        103, 104, 105, 106, 107, 109, 112, 113, 114, 116, 117, 119, 121, 122, 124, 125, 127, 128, 129,
        130, 132)}
    f73 = S["Inputs!E439"]
    for t in range(T):
        m[63][t] = 0 if r7[t] == 0 else S["Inputs!E170"]
        m[65][t] = (1 if case == 2 else r16[t]) * r7[t]
        m[83][t] = r15[t]
        m[66][t] = r7[t] * m[83][t]
        m[67][t] = m[63][t] * m[65][t] * m[66][t]
        m[69][t] = m[67][t]  # + row 68 (subsidy, empty)
        m[73][t] = r7[t] * (1 if r4[t] >= f73 else 0)
        m[72][t] = r7[t] - m[73][t]
        m[75][t] = m[69][t] * m[72][t] + m[73][t] * S["Inputs!E441"] * m[65][t] * m[66][t]
        m[77][t] = r60[t] * m[75][t]
        m[79][t] = r26[t]
        m[80][t] = (0 if m[79][t] == 0 else m[77][t] / m[79][t]) / months
        m[84][t] = r16[t]
        m[85][t] = m[83][t] * m[84][t]
        m[87][t] = m[77][t]
        m[89][t] = 0 if m[79][t] == 0 else m[87][t] / m[79][t]
        m[90][t] = m[89][t] / months
        m[92][t] = S["Inputs!E30"] * m[89][t]
        # OpCo base fee per grid
        m[97][t] = S["Inputs!E173"] * r7[t]
        m[98][t] = (1 if case == 2 else r16[t]) * r7[t]
        m[99][t] = m[83][t] * r7[t]
        m[100][t] = m[97][t] * m[98][t] * m[99][t]
        m[101][t] = -m[100][t] * r185[t]
        # fee per customer
        m[103][t] = X.lookup(r14[t], tb["Inputs!175"], tb["Inputs!176"]) * r7[t]
        m[104][t] = (1 if case == 2 else r16[t]) * r7[t]
        m[105][t] = m[83][t] * r7[t]
        m[106][t] = m[103][t] * m[104][t] * m[105][t]
        m[107][t] = -m[106][t] * r7[t] * m[79][t] * months
        m[109][t] = m[107][t] + m[101][t]
        # ratchet above P50 ARPU
        m[112][t] = m[90][t]
        m[113][t] = r52[t] * m[69][t]
        m[114][t] = max(m[112][t] - m[113][t], 0)
        m[116][t] = m[114][t] * m[79][t] * months
        m[117][t] = -a.opex.ratchet_share * m[116][t]
        m[119][t] = m[117][t]
        m[121][t] = m[119][t] + m[109][t]
        m[122][t] = 0 if r23[t] == 0 else m[121][t] / r23[t]
        m[124][t] = -v["Model!707"][t]
        m[125][t] = 0 if r23[t] == 0 else m[124][t] / r23[t]
        m[127][t] = -S["Inputs!E179"] * (1 if (r7[t] == 1 and r6[t] == 0) else 0)
        m[128][t] = (1 if case == 1 else r17[t]) * r7[t]
        m[129][t] = m[83][t] * r7[t]
        m[130][t] = m[127][t] * m[128][t] * m[129][t]
        m[132][t] = m[121][t] + m[124][t] + m[130][t]
    for r in (77, 87, 101, 107, 109, 116, 117, 119, 121, 122, 124, 125, 127, 130, 132):
        L.totals[f"Model!{r}"] = sum(m[r])
    L.s["Model!E103"] = sum(m[103][1:16]) / 15  # AVERAGE(K103:Y103)
    L.s["Inputs!N176"] = L.s["Model!E103"]
    L.s["Model!F56"] = X.average_nonzero(v["Model!56"])
    L.s["Model!F57"] = X.average_nonzero(v["Model!57"])
    L.s["Model!F63"] = X.average_nonzero(m[67])  # label F63 averages row 67
    L.s["Model!E89"] = X.average_nonzero(m[89])
    L.s["Model!E90"] = X.average_nonzero(m[90])
    L.s["Model!F122"] = X.average_nonzero(m[122])
    L.s["Model!F125"] = X.average_nonzero(m[125])

    # ---- working capital and VAT
    w = {n: L.new(f"Model!{n}") for n in (
        135, 137, 138, 139, 140, 142, 144, 145, 146, 147, 150, 153, 154, 155, 156, 158, 160, 161, 162,
        164, 165, 166, 167, 168, 170, 171, 191)}
    vat = a.tax.vat_rate
    for t in range(T):
        w[191][t] = v["Model!183"][t] * -S["Inputs!E129"]
    for t in range(T):
        prev = lambda r: w[r][t - 1] if t > 0 else 0.0  # noqa: E731
        last_ops = r7[t] == 1 and (r7[t + 1] if t + 1 < T else 0) == 0
        w[155][t] = vat * m[87][t]
        w[156][t] = m[132][t] * vat if a.tax.vat_opex == "Recoverable" else 0.0
        w[153][t] = w[191][t] * vat if a.tax.vat_capex == "Recoverable" else 0.0
        w[154][t] = 0.0  # filled once ongoing capex is known (_vat_and_operating_cash)
        w[135][t] = a.opex.receivable_days / days * (m[87][t] + w[155][t])
        w[137][t] = prev(140)
        w[138][t] = m[87][t] + w[155][t]
        w[139][t] = (w[137][t] + w[138][t]) if last_ops else (w[137][t] + w[138][t] - w[135][t])
        w[140][t] = w[137][t] + w[138][t] - w[139][t]
        w[142][t] = a.opex.payable_days / days * (m[132][t] + w[156][t])
        w[144][t] = prev(147)
        w[145][t] = m[132][t] + w[156][t]
        w[146][t] = (w[144][t] + w[145][t]) if last_ops else (w[144][t] + w[145][t] - w[142][t])
        w[147][t] = w[144][t] + w[145][t] - w[146][t]
        w[150][t] = (w[137][t] - w[140][t]) - (w[147][t] - w[144][t])
    L.totals["Model!191"] = sum(w[191])


def _vat_and_operating_cash(a: Assumptions, S: dict, L: Ledger) -> None:
    """VAT account and operating cash flow (needs ongoing capex, rows 271/274)."""
    v = L.v
    r7 = v["Model!7"]
    vat = a.tax.vat_rate
    days = S["Names!F12"]
    w = {n: v[f"Model!{n}"] for n in (153, 154, 155, 156, 158, 160, 161, 162, 164, 165, 166, 167, 168, 170, 171)}
    for t in range(T):
        w[154][t] = (v["Model!271"][t] + v["Model!274"][t]) * vat if a.tax.vat_capex == "Recoverable" else 0.0
    for t in range(T):
        last_ops = r7[t] == 1 and (r7[t + 1] if t + 1 < T else 0) == 0
        w[164][t] = w[168][t - 1] if t > 0 else 0.0
        w[158][t] = -w[156][t] - w[155][t]
        w[165][t] = -(w[153][t] + w[154][t])
        w[166][t] = w[158][t]
        term = a.tax.vat_term_days
        if last_ops:
            w[160][t] = 0.0
            w[161][t] = 0.0
            w[162][t] = w[164][t] + w[165][t] + w[166][t] - w[161][t]
        else:
            w[160][t] = term / days * (w[164][t] + w[158][t]) if w[164][t] > 0 else term / days * w[158][t]
            w[161][t] = w[160][t] if (w[164][t] + w[165][t] + w[158][t]) <= 0 else w[164][t] + w[158][t]
            w[162][t] = w[164][t] + w[158][t] - w[161][t]
        w[167][t] = w[162][t]
        w[168][t] = w[164][t] + w[165][t] + w[166][t] - w[167][t]
        w[170][t] = (v["Model!87"][t] + v["Model!132"][t] + w[155][t] + w[156][t] + v["Model!150"][t] + w[162][t])
        w[171][t] = 0 if v["Model!87"][t] == 0 else w[170][t] / v["Model!87"][t]
    for r in (135, 138, 139, 145, 146, 150, 153, 154, 155, 156, 158, 162, 165, 166, 167, 170):
        L.totals[f"Model!{r}"] = sum(v[f"Model!{r}"])


# ====================================================================== financing
def _financing(a: Assumptions, S: dict, tb: dict, L: Ledger) -> None:
    v = L.v
    d, r_, tx = a.debt, a.refi, a.tax
    months = S["Names!F13"]
    r4, r5, r6, r7, r11, r13, r14, r18, r19 = (v[f"Model!{n}"] for n in (4, 5, 6, 7, 11, 13, 14, 18, 19))
    # ---- ongoing capex (rows 269-276) and operating cash flow
    m = {n: L.new(f"Model!{n}") for n in (269, 270, 271, 274, 276)}
    for t in range(T):
        m[269][t] = v["Model!749"][t]
        m[270][t] = v["Model!776"][t]
        m[271][t] = m[269][t] + m[270][t]
        m[274][t] = -v["Model!649"][t]
    _vat_and_operating_cash(a, S, L)
    for t in range(T):
        m[276][t] = m[274][t] + m[271][t] + v["Model!154"][t]
    for r in (269, 270, 271, 274, 276):
        L.totals[f"Model!{r}"] = sum(m[r])

    # ---- Debt sheet flags (timeline identical to Model)
    D = {n: L.new(f"Debt!{n}") for n in (
        21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 38, 39, 40, 43, 45, 48, 52, 54, 55, 56, 58, 59, 60,
        65, 66, 68, 69, 70, 71, 74, 75, 76, 77, 81, 82, 83, 86, 88, 90, 94, 96, 97, 98, 100, 101, 102,
        107, 108, 116, 120, 124, 125, 152)}
    # Inputs!I325: start of operations year 1 (SUMIF on Model row 14)
    i325 = sum(r4[t] for t in range(T) if r14[t] == d.repayment_start_ops_year)
    j325 = X.eomonth(i325, d.tenor_years * months - 1)
    j326 = X.eomonth(i325, d.grace_years * months - 1)
    S["Inputs!I325"], S["Inputs!J325"], S["Inputs!I326"], S["Inputs!J326"] = i325, j325, i325, j326
    debt_on = (0 if d.gearing == 0 else 1) * d.debt_switch
    opts = L.options
    base_years = list(a.macro.base_rate_years)
    if opts.fix_base_rate_lookup:
        base_years = [int(str(y).rstrip("+")) if isinstance(y, str) else y for y in base_years]
    for t in range(T):
        D[21][t] = (1 if (r4[t] >= i325 and r5[t] <= j325) else 0) * debt_on
        D[22][t] = (1 if (r4[t] >= i325 and r5[t] <= j326) else 0) * debt_on
        D[23][t] = D[21][t] - D[22][t]
    c21 = 0
    for t in range(T):
        D[24][t] = sum(D[23][t:]) * D[23][t]
        c21 += D[21][t]
        D[25][t] = c21 * D[21][t]
        D[65][t] = (1 if r_.tenor_year == D[25][t] else 0) * r_.on
        D[66][t] = (D[65][t - 1] if t > 0 else 0) * r4[t]
    L.totals["Debt!21"] = sum(D[21])
    i364 = sum(D[66])  # Debt!I66 -> Inputs!I364
    j364 = X.eomonth(i364, r_.tenor_years * months - 1)
    S["Inputs!I364"], S["Inputs!J364"] = i364, j364
    e75 = i364 - 1
    c69 = 0
    for t in range(T):
        D[68][t] = 1 if (r4[t] >= i364 and r5[t] <= j364) else 0
        D[69][t] = D[68][t]
    for t in range(T):
        D[70][t] = sum(D[69][t:]) * D[69][t]
        c69 += D[69][t]
        D[71][t] = c69 * D[69][t]
        D[26][t] = D[65][t]
        D[27][t] = D[68][t]
        # interest rates
        D[38][t] = X.lookup(r11[t], base_years, a.macro.base_rates) * D[21][t]
        D[39][t] = 0 if D[21][t] == 0 else X.lookup(D[25][t], tb["Inputs!313"], tb["Inputs!314"])
        D[40][t] = D[38][t] + D[39][t]
        # Debt!43 looks up the tenor flag (always period 1), not the year in tenor (audit)
        key43 = D[25][t] if opts.fix_fixed_rate_by_year else D[21][t]
        D[43][t] = 0 if D[21][t] == 0 else X.lookup(key43, tb["Inputs!313"], tb["Inputs!315"])
        D[45][t] = D[40][t] if d.rate_choice == "Floating" else D[43][t]
        D[81][t] = X.lookup(r11[t], base_years, a.macro.base_rates) * D[68][t]
        D[82][t] = 0 if D[68][t] == 0 else X.lookup(D[71][t], tb["Inputs!353"], tb["Inputs!354"])
        D[83][t] = D[81][t] + D[82][t]
        D[86][t] = 0 if D[68][t] == 0 else X.lookup(D[71][t], tb["Inputs!353"], tb["Inputs!355"])
        D[88][t] = D[83][t] if r_.rate_choice == "Floating" else D[86][t]
        D[52][t] = D[23][t]
        D[56][t] = d.target_dscr * D[52][t]
        D[94][t] = D[69][t]
        D[98][t] = S["Inputs!E367"] * D[94][t]
        # MMRA flags
        D[107][t] = D[21][t] * a.reserves.mmra_on
        D[124][t] = (1 if S["Inputs!E10"] == r14[t] else 0) * debt_on
        D[125][t] = D[124][t] * S["Inputs!E386"]
        D[116][t] = D[125][t]
    for t in range(T):
        D[108][t] = 1 if (D[107][t] == 1 and (D[107][t + 1] if t + 1 < T else 0) == 0) else 0
        D[152][t] = S["Inputs!E386"] * D[108][t]
        D[120][t] = -D[152][t]

    # ---- DSRA initial funding flag (Debt!168) and funding (Debt!194)
    DS = {n: L.new(f"Debt!{n}") for n in (157, 168, 194)}
    f168 = S["Inputs!E380"]
    for t in range(T):
        DS[157][t] = D[21][t] * a.reserves.dsra_on
        DS[168][t] = (1 if (r4[t] <= f168 <= r5[t]) else 0) * debt_on
        DS[194][t] = a.pasted.dsra_initial * DS[168][t]

    # ---- Model funding rows
    F = {n: L.new(f"Model!{n}") for n in (
        192, 193, 196, 199, 200, 201, 202, 203, 204, 207, 208, 209, 210, 211, 215, 216, 219, 220, 223,
        224, 226, 227, 230, 231, 232, 234, 235, 238, 239, 240, 242, 245, 246, 247, 248, 249, 251, 254,
        255, 256, 258, 262, 264, 265, 278, 281, 282, 284, 285, 287, 288, 290, 291, 368, 408)}
    r183, r191 = v["Model!183"], v["Model!191"]
    e219 = 1 - S["Inputs!G332"]
    S["Model!E219"] = e219
    e234, e242, e251 = S["Inputs!E270"], S["Inputs!E279"], S["Inputs!E304"]
    e256 = i325
    for t in range(T):
        F[196][t] = 1 if r183[t] > 0 else 0
        F[254][t] = S["Inputs!I310"] * r6[t]
        F[256][t] = 1 if r4[t] == e256 else 0
        F[258][t] = d.arrangement_fee * F[256][t] * S["Inputs!E304"]
        F[201][t] = -F[258][t]
        F[192][t] = F[201][t]
        F[193][t] = r191[t] + F[192][t]
        F[199][t] = r191[t] + v["Model!153"][t]
        F[202][t] = -DS[194][t]
        F[203][t] = -D[125][t]
        F[408][t] = r14[t]
        F[368][t] = (1 if F[408][t] <= a.funding.irr_period else 0) * r18[t] * r7[t]

    # ---- depreciation & tax rows
    T_ = {n: L.new(f"Model!{n}") for n in (
        458, 461, 462, 464, 468, 469, 470, 472, 473, 474, 476, 478, 479, 481, 484, 485, 486, 487, 488,
        490, 491, 493, 496, 497, 498, 499, 502, 505, 506, 509, 510, 514, 515, 516, 517, 519, 520, 523,
        524, 525, 526, 528, 529, 532, 533, 534, 535, 537, 538, 540, 543, 544, 545, 546, 551, 552, 553,
        554, 556, 557, 560, 561, 562, 563, 565, 566, 569, 570, 571, 572, 574, 575, 577, 580, 581, 582, 583)}
    FS = {n: L.new(f"FinStat!{n}") for n in (12, 13, 14, 16, 17, 18, 20, 21, 22, 23, 25, 26, 28)}
    c7 = 0
    for t in range(T):
        T_[458][t] = (1 if tx.holiday_years < r14[t] else 0) * r7[t]
        T_[509][t] = r18[t]
        T_[510][t] = r19[t]
        T_[505][t] = v["Model!87"][t]
        c7 += r7[t]
        T_[490][t] = min(c7, tx.nol_years)
        T_[524][t] = -m[274][t] - m[271][t]
        T_[561][t] = -m[274][t] - m[271][t]
        T_[552][t] = -r191[t]
        T_[519][t] = min(T_[510][t], tx.book_life_initial)
        T_[528][t] = min(T_[510][t], S["Inputs!E242"])
        T_[537][t] = min(T_[510][t], S["Inputs!E246"])
        T_[556][t] = min(T_[510][t], tx.tax_life_initial)
        T_[565][t] = min(T_[510][t], tx.tax_life_replacement)
        T_[574][t] = min(T_[510][t], S["Inputs!E259"])

    # ---- year-by-year financing pass
    for t in range(T):
        prev = lambda rows, r: rows[r][t - 1] if t > 0 else 0.0  # noqa: E731
        # uses
        F[245][t] = prev(F, 249)
        F[255][t] = F[245][t] * F[254][t]
        F[200][t] = -F[255][t]
        F[204][t] = F[199][t] + F[200][t] + F[201][t] + F[202][t] + F[203][t]
        # grant
        F[230][t] = prev(F, 232)
        F[234][t] = (e234 - F[230][t]) * F[196][t]
        F[215][t] = min(-F[204][t] * a.funding.grant_drawdown_rate, F[234][t])
        F[231][t] = F[215][t]
        F[232][t] = F[230][t] + F[231][t]
        F[216][t] = F[204][t] + F[215][t]
        # owner equity (pari passu share)
        F[238][t] = prev(F, 240)
        F[242][t] = (e242 - F[238][t]) * F[196][t]
        F[219][t] = min(F[242][t], -e219 * F[216][t])
        F[239][t] = F[219][t]
        F[240][t] = F[238][t] + F[239][t]
        F[220][t] = F[216][t] + F[219][t]
        # senior debt
        F[251][t] = (e251 - F[245][t]) * F[196][t]
        F[223][t] = min(-F[220][t], F[251][t])
        F[224][t] = F[220][t] + F[223][t]
        F[226][t] = -F[224][t]
        F[227][t] = F[224][t] + F[226][t]
        F[207][t], F[208][t], F[209][t], F[210][t] = F[215][t], F[219][t], F[223][t], F[226][t]
        F[211][t] = F[207][t] + F[208][t] + F[209][t] + F[210][t]
        F[246][t] = F[223][t]
        F[235][t] = S["Inputs!E30"] * v["Model!23"][t]
        # Debt account
        D[30][t] = prev(D, 34)
        D[31][t] = F[246][t]
        D[48][t] = D[45][t] * (D[30][t] + D[31][t])
        # refinanced debt
        D[74][t] = prev(D, 77)
        D[75][t] = S["Inputs!E348"] if e75 == r5[t] else 0.0
        D[90][t] = D[74][t] * D[88][t]
        # depreciation (book)
        T_[515][t] = -F[193][t]
        T_[533][t] = F[255][t]
        T_[540][t] = F[255][t]
        T_[570][t] = F[255][t]
        T_[577][t] = F[255][t]
        for (bf, add, dep, cf, lb, base_rate) in ((514, 515, 516, 517, 519, S["Inputs!E239"]),
                                                  (523, 524, 525, 526, 528, S["Inputs!E243"]),
                                                  (532, 533, 534, 535, 537, S["Inputs!E247"]),
                                                  (551, 552, 553, 554, 556, S["Inputs!E252"]),
                                                  (560, 561, 562, 563, 565, S["Inputs!E256"]),
                                                  (569, 570, 571, 572, 574, S["Inputs!E260"])):
            T_[bf][t] = prev(T_, cf)
            w = int(T_[lb][t])
            base = 0.0 if w == 0 else _lookback(T_[add], t, w)
            T_[lb + 1][t] = base
            T_[dep][t] = -base * base_rate
            T_[cf][t] = T_[bf][t] + T_[add][t] + T_[dep][t]
        T_[543][t] = T_[514][t] + T_[523][t] + T_[532][t]
        T_[544][t] = T_[515][t] + T_[524][t] + T_[533][t]
        T_[545][t] = T_[516][t] + T_[525][t] + T_[534][t]
        T_[546][t] = T_[543][t] + T_[544][t] + T_[545][t]
        T_[580][t] = T_[551][t] + T_[560][t] + T_[569][t]
        T_[581][t] = T_[552][t] + T_[561][t] + T_[570][t]
        T_[582][t] = T_[553][t] + T_[562][t] + T_[571][t]
        T_[583][t] = T_[580][t] + T_[581][t] + T_[582][t]
        # P&L to EBT
        FS[12][t] = v["Model!87"][t]
        FS[13][t] = v["Model!132"][t]
        FS[14][t] = FS[12][t] + FS[13][t]
        FS[16][t] = T_[545][t]
        FS[17][t] = FS[14][t] + FS[16][t]
        FS[18][t] = 0 if FS[12][t] == 0 else FS[17][t] / FS[12][t]
        FS[20][t] = -D[48][t]
        FS[21][t] = -D[90][t]
        FS[23][t] = FS[20][t] + FS[21][t] + FS[22][t] + FS[17][t]
        # tax
        T_[461][t] = FS[23][t]
        T_[462][t] = max(T_[461][t], 0)
        T_[464][t] = -T_[462][t] * tx.corporate_rate
        T_[468][t] = FS[23][t]
        T_[469][t] = -T_[545][t]
        T_[470][t] = T_[468][t] + T_[469][t]
        T_[472][t] = T_[582][t]
        x = -tx.capital_allowance_limit * T_[470][t]
        T_[473][t] = 0 if x >= 0 else x
        T_[474][t] = max(T_[473][t], T_[472][t])
        T_[476][t] = T_[470][t] + T_[474][t]
        # NOLs
        w = int(T_[490][t])
        if w and t - w <= -1:  # would read the row total (conditional cycle, audit section 4)
            raise ValueError("Model!491 would read its own row total (operations start in the first column)")
        T_[491][t] = 0.0 if w == 0 else _lookback(T_[485], t, w)
        T_[484][t] = min(prev(T_, 488), T_[491][t])
        T_[485][t] = -min(T_[476][t], 0)
        T_[486][t] = min(T_[491][t] - prev(T_, 488), 0)
        T_[487][t] = -min(max(T_[476][t], 0), T_[484][t])
        T_[488][t] = T_[484][t] + T_[485][t] + T_[486][t] + T_[487][t]
        T_[478][t] = T_[487][t]
        T_[479][t] = max(T_[476][t] + T_[478][t], 0)
        T_[481][t] = (-T_[479][t] * tx.corporate_rate) * T_[458][t]
        T_[493][t] = -T_[488][t] * tx.corporate_rate
        T_[496][t] = prev(T_, 499)
        T_[497][t] = -T_[464][t]
        T_[498][t] = T_[481][t]
        T_[499][t] = T_[496][t] + T_[497][t] + T_[498][t]
        T_[502][t] = (1 if T_[481][t] >= S["Inputs!E231"] else 0) * r7[t]
        T_[506][t] = (-tx.minimum_tax * T_[505][t] * T_[502][t]) * T_[458][t]
        FS[25][t] = T_[464][t]
        FS[26][t] = T_[506][t]
        FS[28][t] = FS[23][t] + FS[25][t] + FS[26][t]
        # cash waterfall to CFADS
        F[262][t] = v["Model!170"][t]
        F[264][t] = F[262][t] + F[204][t] + F[211][t]
        F[265][t] = F[264][t]
        F[278][t] = F[265][t] + m[276][t]
        F[284][t] = T_[506][t]
        F[285][t] = T_[481][t]
        F[281][t] = -min(F[278][t] + F[285][t], 0) * F[368][t]
        F[282][t] = F[278][t] + F[281][t]
        F[287][t] = min(F[285][t], F[284][t])
        F[288][t] = F[282][t] + F[287][t]
        F[290][t] = -D[120][t]
        F[291][t] = F[288][t] + F[290][t]
        # senior debt sculpting and repayment
        D[54][t] = F[291][t]
        D[55][t] = D[54][t] * D[23][t]
        D[58][t] = 0 if D[52][t] == 0 else D[55][t] / D[56][t]
        D[59][t] = -D[52][t] * D[48][t]
        D[60][t] = max(D[58][t] + D[59][t], 0)
        D[32][t] = -D[30][t] if D[24][t] == 1 else -D[60][t] * (D[23][t] - D[27][t])
        if opts.cap_principal_at_balance:
            D[32][t] = max(D[32][t], -(D[30][t] + D[31][t]))
        D[33][t] = -(D[30][t] + D[31][t] + D[32][t]) * D[26][t]
        D[34][t] = D[30][t] + D[31][t] + D[32][t] + D[33][t]
        F[247][t] = D[32][t]
        F[248][t] = D[33][t]
        F[249][t] = F[245][t] + F[246][t] + F[247][t] + F[248][t]
        # refinanced debt sculpting
        D[96][t] = F[291][t]
        D[97][t] = D[96][t] * D[69][t]
        D[100][t] = 0 if D[94][t] == 0 else D[97][t] / D[98][t]
        D[101][t] = -D[94][t] * D[90][t]
        D[102][t] = D[100][t] + D[101][t]
        D[76][t] = -min(D[102][t], D[74][t])
        D[77][t] = D[74][t] + D[75][t] + D[76][t]

    for k in (192, 193, 199, 200, 201, 202, 203, 204, 207, 208, 209, 210, 211, 215, 216, 219, 220, 223,
              224, 226, 227, 231, 239, 246, 247, 248, 255, 258, 262, 264, 265, 278, 281, 282, 284, 285,
              287, 288, 290, 291, 368):
        L.totals[f"Model!{k}"] = sum(F[k])
    for k in (461, 462, 464, 468, 469, 470, 472, 473, 474, 476, 478, 479, 481, 485, 486, 487, 497,
              498, 505, 506, 516, 525, 534, 540, 544, 545, 553, 562, 571, 577, 581, 582):
        L.totals[f"Model!{k}"] = sum(T_[k])
    for k in (515, 524, 533, 552, 561, 570):
        L.s[f"Model!H{k}"] = sum(T_[k])
    for k in (12, 13, 14, 16, 17, 20, 21, 22, 23, 25, 26, 28):
        L.totals[f"FinStat!{k}"] = sum(FS[k])
    for k in (21, 31, 32, 33, 48, 52, 54, 55, 58, 59, 60, 66, 75, 76, 90, 94, 96, 97, 100, 101, 102,
              116, 120, 125, 152):
        L.totals[f"Debt!{k}"] = sum(D[k])
    L.totals["Debt!194"] = sum(DS[194])
    L.totals["Debt!78"] = L.totals["Debt!75"] + L.totals["Debt!76"]
    L.s["Debt!H35"] = L.totals["Debt!31"] + L.totals["Debt!32"]
    L.totals["Debt!35"] = L.totals["Debt!33"] + L.s["Debt!H35"]
    # macro inputs computed from the results
    S["Inputs!E292"] = -L.totals["Model!204"]          # Funding_calculated
    S["Inputs!E300"] = L.totals["Debt!60"]             # DSCR_calculated
    S["Inputs!E344"] = L.totals["Debt!102"]            # Refi_Calculated
    S["Inputs!E305"] = L.totals["Model!246"]
    S["Inputs!E349"] = L.totals["Model!246"]
    S["Inputs!E280"] = L.totals["Model!210"]


# ======================================================================= reserves
def _reserves(a: Assumptions, S: dict, tb: dict, L: Ledger) -> None:
    v = L.v
    D = v
    r7 = v["Model!7"]
    res = a.reserves
    R = {n: L.new(f"Debt!{n}") for n in (
        111, 112, 115, 117, 118, 119, 121, 128, 129, 130, 132, 133, 136, 139, 140, 142, 143, 144, 145,
        148, 149, 150, 160, 161, 162, 165, 169, 172, 173, 174, 175, 176, 179, 180, 181, 184, 185, 186,
        187, 188, 190, 193, 195, 196, 197, 198, 200, 203, 204)}
    M = {n: L.new(f"Model!{n}") for n in (
        296, 297, 300, 301, 305, 306, 307, 310, 311, 312, 314, 317, 318, 319, 322, 323, 324, 326, 329,
        330, 332, 333, 335, 336, 341, 342, 344, 345, 346, 347, 349, 352, 353, 354, 405)}
    d21, d32, d48, d157 = D["Debt!21"], D["Debt!32"], D["Debt!48"], D["Debt!157"]
    for t in range(T):
        R[160][t] = -d32[t]
        R[161][t] = d48[t]
        R[162][t] = R[160][t] + R[161][t]
        R[136][t] = -v["Model!269"][t]
        # the MMRA switch multiplies the minimum balance in the first column only (workbook)
        R[139][t] = S["Inputs!E386"] * d21[t] * (res.mmra_on if t == 0 else 1)
        R[128][t] = v["Model!265"][t]
        R[129][t] = -v["Model!271"][t] if t == 0 else v["Model!271"][t]
        R[130][t] = min(R[128][t] + R[129][t], 0)
    f165 = 1  # Debt!F165 periods of debt service in the target
    for t in range(T):
        R[165][t] = sum(_fwd(R[162], t, f165)) * d157[t] * S["Inputs!E375"]
        R[140][t] = sum(_fwd(R[136], t, int(res.mmra_years))) * res.mmra_on
        R[142][t] = max(R[139][t], R[140][t]) * v["Debt!107"][t]
        R[169][t] = v["Debt!168"][t] * R[165][t]
        R[179][t] = R[165][t]
        R[184][t] = R[165][t]
        R[203][t] = res.dsra_deposit_rate * d157[t]
    L.totals["Debt!165"] = max(R[165])
    S["Debt!F169"] = sum(R[169])
    S["Inputs!E371"] = S["Debt!F169"]                   # DSRA_Copy
    diff = S["Inputs!E371"] - a.pasted.dsra_initial
    S["Inputs!E373"] = min(diff, X.xround(diff, -5))

    for t in range(T):
        prev = lambda rows, r: rows[r][t - 1] if t > 0 else 0.0  # noqa: E731
        # DSRA interest and release for shortfall
        R[193][t] = prev(R, 198)
        R[204][t] = R[203][t] * max(0, R[193][t])
        M[296][t] = R[204][t]
        M[297][t] = v["Model!291"][t] + M[296][t]
        R[172][t] = M[297][t]
        R[173][t] = R[162][t]
        R[174][t] = max(0, min(R[173][t], R[173][t] - R[172][t]))
        R[175][t] = 0 if R[174][t] == 0 else R[193][t] + v["Debt!194"][t]
        R[176][t] = min(R[174][t], R[175][t])
        M[300][t] = R[176][t]
        M[301][t] = M[297][t] + M[300][t]
        M[305][t] = -d48[t]
        M[306][t] = d32[t]
        M[307][t] = M[305][t] + M[306][t]
        M[310][t] = -v["Debt!90"][t]
        M[311][t] = v["Debt!76"][t]
        M[312][t] = M[310][t] + M[311][t]
        M[314][t] = M[301][t] + M[307][t] + M[312][t]
        # DSRA top-up and release of excess
        R[190][t] = M[314][t]
        R[195][t] = -R[176][t]
        R[185][t] = R[193][t] + v["Debt!194"][t]
        R[186][t] = max(0, R[184][t] - R[185][t])
        R[187][t] = 0 if R[186][t] == 0 else max(0, R[190][t])
        R[188][t] = min(R[186][t], R[187][t])
        R[196][t] = R[188][t]
        R[180][t] = (R[193][t] + v["Debt!194"][t] + R[195][t] + R[196][t]) * d157[t]
        R[181][t] = max(0, R[180][t] - R[179][t])
        R[197][t] = -R[181][t]
        R[198][t] = R[193][t] + v["Debt!194"][t] + R[195][t] + R[196][t] + R[197][t]
        R[200][t] = 1 if R[180][t] < R[179][t] else 0
        M[317][t] = -R[196][t]
        M[318][t] = -R[197][t]
        M[319][t] = M[314][t] + M[317][t] + M[318][t]
        M[322][t] = v["Debt!33"][t]
        M[323][t] = v["Debt!75"][t]
        M[324][t] = M[322][t] + M[323][t]
        M[326][t] = M[319][t] + M[324][t]
        # MMRA
        R[115][t] = prev(R, 121)
        R[132][t] = R[115][t]
        R[133][t] = min(R[132][t], R[130][t])
        R[117][t] = -R[133][t]
        R[148][t] = R[115][t] + v["Debt!116"][t] + R[117][t]
        R[149][t] = 1 if R[148][t] > R[142][t] else 0
        R[150][t] = R[149][t] * (R[148][t] - R[142][t])
        R[119][t] = -R[150][t]
        R[111][t] = R[117][t] + R[119][t]
        M[329][t] = -R[111][t]
        M[330][t] = M[326][t] + M[329][t]
        R[144][t] = M[330][t]
        R[143][t] = max(R[142][t] - R[115][t], 0)
        R[145][t] = max(min(R[143][t], R[144][t]), 0)
        R[118][t] = R[145][t]
        R[112][t] = R[118][t]
        R[121][t] = R[115][t] + v["Debt!116"][t] + R[117][t] + R[118][t] + R[119][t] + v["Debt!120"][t]
        M[332][t] = -R[112][t]
        M[333][t] = M[330][t] + M[332][t]
        M[335][t] = -min(M[333][t], 0) * v["Model!368"][t]
        M[336][t] = M[333][t] + M[335][t]

    # exit and distributions
    r14 = v["Model!14"]
    exit_year = a.exit.exit_ops_year
    for t in range(T):
        M[341][t] = r7[t] * (1 if exit_year == r14[t] else 0)
        M[342][t] = r7[t] * (1 if exit_year >= r14[t] else 0)
        M[344][t] = M[336][t]
    for t in range(T):
        M[345][t] = X.npv(a.exit.exit_wacc, _fwd(M[344], t, int(a.exit.exit_lookforward_years)))
        M[346][t] = M[345][t] * M[341][t]
        M[347][t] = M[342][t] * (M[346][t] + M[344][t])
        M[349][t] = M[347][t] * a.tax.dividend_wht
        M[405][t] = M[347][t] - M[349][t]
        M[352][t] = M[354][t - 1] if t > 0 else 0.0
        M[353][t] = M[347][t] - M[349][t] - M[405][t]
        M[354][t] = M[352][t] + M[353][t]
    L.s["Debt!I122"] = sum(v["Debt!116"]) + sum(R[117]) + sum(R[118]) + sum(R[119]) + sum(v["Debt!120"])
    L.s["Debt!V122"] = R[115][12] + v["Debt!120"][12]  # column V hard-coded in the workbook check
    for k in (111, 112, 117, 118, 119, 128, 129, 130, 132, 133, 136, 143, 144, 145, 148, 150, 160, 161,
              162, 169, 174, 176, 181, 186, 187, 188, 190, 195, 196, 197, 200, 204):
        L.totals[f"Debt!{k}"] = sum(R[k])
    for k in (296, 297, 300, 301, 305, 306, 307, 310, 311, 312, 314, 317, 318, 319, 322, 323, 324,
              326, 329, 330, 332, 333, 335, 336, 344, 345, 346, 347, 349, 353, 405):
        L.totals[f"Model!{k}"] = sum(M[k])
    # sizing deltas (Inputs!J292, J300, J344) and checks
    _sizing_state(a, S)


def _sizing_state(a: Assumptions, S: dict) -> None:
    pst = a.pasted
    l292 = S["Inputs!L292"]
    d = pst.funding - S["Inputs!E292"]
    S["Inputs!I292"] = S["Inputs!E292"]
    S["Inputs!J292"] = min(d, X.xround(d, -int(l292)))
    S["Inputs!K292"] = 0 if pst.funding == 0 else (S["Inputs!E292"] - pst.funding) / pst.funding
    S["Inputs!N292"] = 0 - S["Inputs!J292"]
    l300 = S["Inputs!L300"]
    d = S["Inputs!E300"] - pst.dscr_limit
    j300 = min(d, X.xround(d, -int(l300)))
    S["Inputs!J300"] = j300
    S["Inputs!I300"] = pst.dscr_limit + j300 if (j300 < 0 and j300 > -10 ** l300) else pst.dscr_limit + 0.5 * j300
    S["Inputs!K300"] = 0 if pst.dscr_limit == 0 else (S["Inputs!E300"] - pst.dscr_limit) / pst.dscr_limit
    S["Inputs!N300"] = (0 - j300) * a.debt.debt_switch * (1 - a.refi.on)
    l344 = a.refi.sizing_rounding
    d = S["Inputs!E344"] - pst.refi_limit
    j344 = min(d, X.xround(d, -int(l344)))
    S["Inputs!J344"] = j344
    S["Inputs!I344"] = pst.refi_limit + j344 if (j344 < 0 and j344 > -10 ** l344) else pst.refi_limit + 0.5 * j344
    S["Inputs!N344"] = (0 - j344) * a.refi.on


# ======================================================================== returns
def _returns(a: Assumptions, S: dict, tb: dict, L: Ledger) -> None:
    v = L.v
    r5, r7, r14, r18 = v["Model!5"], v["Model!7"], v["Model!14"], v["Model!18"]
    dates = [S["Inputs!E6"]] + list(r5)  # I5:BZ5
    M = {n: L.new(f"Model!{n}") for n in (
        358, 359, 360, 361, 362, 363, 364, 365, 367, 369, 370, 371, 372, 377, 378, 381, 382, 383, 384,
        386, 387, 388, 397, 399, 400, 402, 406, 409, 410, 416, 417, 422, 423, 424, 426, 427, 428, 429,
        431, 432, 433, 439, 440, 444, 445, 446, 449, 450, 451, 452, 453, 454)}
    fund = a.funding
    for t in range(T):
        M[358][t] = v["Model!199"][t]
        M[359][t] = v["Model!231"][t]
        M[360][t] = v["Model!87"][t] + v["Model!155"][t]
        M[361][t] = v["Model!132"][t] + v["Model!156"][t]
        M[362][t] = v["Model!150"][t]
        M[363][t] = v["Model!276"][t]
        M[364][t] = v["Model!285"][t] + v["Model!162"][t]
        M[365][t] = sum(M[r][t] for r in range(358, 365))
        M[367][t] = r14[t]
        M[369][t] = M[365][t] * v["Model!368"][t]
        M[370][t] = 1 if S["Currency!F18"] == 1 else X.lookup(v["Model!11"][t], tb["Inputs!401"], tb["Inputs!402"])
        M[371][t] = M[369][t] / M[370][t]
        M[381][t] = M[365][t]
        M[382][t] = -M[358][t]
        M[383][t] = v["Model!231"][t]
        M[384][t] = M[381][t] + M[382][t] + M[383][t]
        M[386][t] = r14[t]
        M[387][t] = (1 if v["Model!408"][t] < fund.irr_period else 0) * r18[t]
        M[388][t] = M[384][t] * M[387][t]
        M[397][t] = -v["Model!219"][t]
        M[399][t] = -v["Model!226"][t]
        M[400][t] = -v["Model!281"][t] - v["Model!335"][t]
        M[402][t] = M[397][t] + M[399][t] + M[400][t]
        M[406][t] = M[402][t] + v["Model!405"][t]
        M[409][t] = (1 if v["Model!408"][t] <= fund.irr_period else 0) * r18[t] * r7[t]
        M[410][t] = M[406][t] * M[409][t]
        M[416][t] = v["Model!215"][t]
        M[417][t] = M[410][t] - M[416][t]
        M[422][t] = fund.owner_equity_provision * M[397][t]
        M[423][t] = fund.owner_equity_provision * M[399][t]
        M[424][t] = fund.owner_equity_provision * M[400][t]
        M[426][t] = M[422][t] + M[423][t] + M[424][t]
        M[427][t] = S["Inputs!E283"] * v["Model!405"][t]
        M[428][t] = M[426][t] + M[427][t]
        M[431][t] = r14[t]
        M[432][t] = (1 if M[431][t] <= fund.irr_period else 0) * r18[t] * r7[t]
        M[433][t] = M[428][t] * M[432][t]
        M[439][t] = v["Model!215"][t]
        M[440][t] = M[433][t] - M[439][t]
        M[444][t] = -v["Model!121"][t]
        M[445][t] = v["Model!405"][t] * fund.developer_stake
        M[446][t] = M[444][t] + M[445][t]
        M[449][t] = M[454][t - 1] if t > 0 else 0.0
        M[450][t] = v["Model!208"][t]
        M[451][t] = v["Model!210"][t]
        M[452][t] = v["Model!281"][t] + v["Model!335"][t]
        M[453][t] = v["Model!215"][t]
        M[454][t] = M[449][t] + M[450][t] + M[451][t] + M[452][t] + M[453][t]
    for t in range(T):
        M[372][t] = X.iferror(lambda: X.irr(M[371][: t + 1]), 0.0)
        M[429][t] = X.iferror(lambda: X.irr(M[428][: t + 1]), 0.0)
        M[377][t] = X.iferror(lambda: (1 if M[372][t] > 0 else 0) * r7[t], 0)
        M[378][t] = r7[t] * (1 - M[377][t])
    for k in (358, 359, 360, 361, 362, 363, 364, 365, 368, 377, 378, 381, 382, 383, 384, 387, 397, 399,
              400, 402, 405, 409, 416, 422, 423, 424, 426, 427, 432, 439, 444, 445, 446, 450, 451, 452, 453):
        L.totals[f"Model!{k}"] = sum(v[f"Model!{k}"])
    for k in (371, 372, 388, 406, 410, 417, 428, 433, 440):
        L.totals[f"Model!{k}"] = -VERY_SMALL  # column I anchor of the IRR series
    L.s["Model!H369"] = sum(M[369])
    L.s["Model!H388"] = sum(M[388])
    L.s["Model!H406"] = sum(M[406])
    L.s["Model!H410"] = sum(M[410])
    L.s["Model!H417"] = sum(M[417])
    L.s["Model!H428"] = sum(M[428])
    L.s["Model!H433"] = sum(M[433])
    L.s["Model!H440"] = sum(M[440])
    xs = lambda row: [-VERY_SMALL] + list(M[row])  # noqa: E731  (I..BZ)
    L.s["Model!E375"] = X.xirr(xs(371), dates)
    L.s["Model!E376"] = X.xnpv(fund.wacc, M[369], r5)
    L.s["Model!E392"] = X.xnpv(fund.wacc, M[388], r5)
    L.s["Model!E394"] = L.s["Model!E392"] / S["Inputs!E25"]
    L.s["Model!E413"] = X.xirr(xs(410), dates)
    L.s["Model!E418"] = X.xirr(xs(417), dates)
    L.s["Model!E436"] = X.xirr(xs(433), dates)
    L.s["Model!E441"] = X.xirr(xs(440), dates)
    L.s["Model!E281"] = 1 if L.totals["Model!281"] > S["Model!F281"] else 0
    L.s["Model!E335"] = 1 if L.totals["Model!335"] > S["Model!F281"] else 0
    L.s["Model!E337"] = L.s["Model!E335"] + L.s["Model!E281"]


# ====================================================================== finstat
def _finstat(a: Assumptions, S: dict, L: Ledger) -> None:
    v = L.v
    FS = v
    N = {n: L.new(f"FinStat!{n}") for n in (
        30, 31, 32, 34, 35, 39, 40, 41, 42, 43, 44, 48, 50, 53, 54, 55, 57, 58, 60, 63, 64, 65, 67, 68,
        73, 74, 75, 76, 77, 79, 80, 82, 83, 85, 86, 87, 88, 89, 90, 91, 92, 93, 95, 96, 98, 99, 100, 102,
        103, 104, 106, 107, 109, 110, 112, 114, 115, 116, 118, 119, 120, 122, 123, 124, 126, 127, 129,
        130, 131, 132, 134, 135)}
    M = lambda r: v[f"Model!{r}"]  # noqa: E731
    pairs = {73: None, 74: None, 75: 150, 76: 162, 79: 199, 82: 287, 85: 200, 86: 201, 87: 202, 88: 203,
             89: 207, 90: 208, 91: 209, 92: 210, 95: 276, 98: 281, 99: 290, 102: 296, 103: 300, 106: 305,
             107: 306, 109: 310, 110: 311, 114: 317, 115: 318, 118: 322, 119: 323, 122: 329, 123: 332,
             126: 335, 129: 346}
    for t in range(T):
        N[30][t] = -M(349)[t]
        N[31][t] = -M(405)[t]
        N[32][t] = FS["FinStat!28"][t] + N[30][t] + N[31][t]
        N[34][t] = N[35][t - 1] if t > 0 else 0.0
        N[35][t] = N[34][t] + N[32][t]
        for r, src in pairs.items():
            if src:
                N[r][t] = M(src)[t]
        N[73][t] = M(87)[t] + M(155)[t]
        N[74][t] = M(132)[t] + M(156)[t]
        N[77][t] = N[73][t] + N[74][t] + N[75][t] + N[76][t]
        N[80][t] = N[77][t] + N[79][t]
        N[83][t] = N[80][t] + N[82][t]
        N[93][t] = N[83][t] + sum(N[r][t] for r in range(85, 93))
        N[96][t] = N[93][t] + N[95][t]
        N[100][t] = N[96][t] + N[98][t] + N[99][t]
        N[104][t] = N[100][t] + N[102][t] + N[103][t]
        N[112][t] = N[104][t] + N[106][t] + N[107][t] + N[109][t] + N[110][t]
        N[116][t] = N[112][t] + N[114][t] + N[115][t]
        N[120][t] = N[116][t] + N[118][t] + N[119][t]
        N[124][t] = N[120][t] + N[122][t] + N[123][t]
        N[127][t] = N[124][t] + N[126][t]
        N[130][t] = -M(349)[t]
        N[131][t] = -M(405)[t]
        N[132][t] = N[127][t] + N[129][t] + N[130][t] + N[131][t]
        N[134][t] = N[135][t - 1] if t > 0 else 0.0
        N[135][t] = N[134][t] + N[132][t]
        # balance sheet
        N[39][t] = N[135][t]
        N[40][t] = M(140)[t]
        N[41][t] = M(168)[t]
        N[42][t] = v["Debt!121"][t]
        N[43][t] = v["Debt!198"][t]
        N[44][t] = N[39][t] + N[40][t] + N[41][t] + N[42][t] + N[43][t]
        N[48][t] = M(546)[t]
        N[50][t] = N[48][t]
        N[53][t] = -M(499)[t]
        N[54][t] = M(147)[t]
        N[55][t] = -M(249)[t]
        N[57][t] = -v["Debt!77"][t]
        N[58][t] = N[53][t] + N[54][t] + N[55][t] + N[57][t]
        N[60][t] = N[44][t] + N[50][t] + N[58][t]
        N[63][t] = M(454)[t]
        N[64][t] = N[35][t]
        N[65][t] = N[63][t] + N[64][t]
        N[67][t] = X.xround(N[60][t] - N[65][t], 3)
    for t in range(1, T):
        N[68][t] = N[67][t] - N[68][t - 1]  # FinStat!K68 = K67 - J68
    for k in (30, 31, 32, 73, 74, 75, 76, 77, 79, 80, 82, 83, 85, 86, 87, 88, 89, 90, 91, 92, 93, 95, 96,
              98, 99, 100, 102, 103, 104, 106, 107, 109, 110, 112, 114, 115, 116, 118, 119, 120, 122,
              123, 124, 126, 127, 129, 130, 131, 132, 67, 68):
        L.totals[f"FinStat!{k}"] = sum(N[k])
    L.s["FinStat!I69"] = L.totals["FinStat!67"] * L.totals["FinStat!68"]


# ==================================================================== dashboard
def _dashboard(a: Assumptions, S: dict, L: Ledger) -> None:
    s, tot = L.s, L.totals
    s["Dashboard!E36"] = s["Model!E375"]
    s["Dashboard!G36"] = tot["Model!378"]
    s["Dashboard!E41"] = S["Inputs!E305"]
    s["Dashboard!E42"] = S["Inputs!E270"]
    s["Dashboard!E43"] = S["Inputs!E279"]
    s["Dashboard!E44"] = S["Inputs!E292"]
    for r, row in ((50, 199), (51, 200), (52, 201), (53, 202), (54, 203), (55, 204)):
        s[f"Dashboard!E{r}"] = -tot[f"Model!{row}"]
    s["Dashboard!K34"] = s.get("Model!E90", 0.0)
    s["Dashboard!K35"] = s["Model!F56"]
    s["Dashboard!K36"] = s["Model!F63"]
    s["Dashboard!K39"] = S["Inputs!E27"]
    s["Dashboard!K42"] = s["FinStat!I69"]
    s["Dashboard!K43"] = 0 if S["Inputs!E279"] > 0 else 1
    s["Dashboard!K44"] = tot["Debt!35"]
    s["Dashboard!K45"] = S["Inputs!N292"]
    s["Dashboard!K46"] = S["Inputs!N300"]
    s["Dashboard!K47"] = tot["Debt!78"]
    s["Dashboard!K48"] = S["Inputs!N344"]
    s["Dashboard!K49"] = tot["Model!210"]
    s["Dashboard!K50"] = s["Model!E337"]
    s["Dashboard!K51"] = S["Inputs!G141"]
    s["Dashboard!K52"] = s["Debt!V122"]
    s["Dashboard!K53"] = S["Inputs!E373"]
    s["Dashboard!K55"] = sum(s[f"Dashboard!K{r}"] for r in range(42, 54))
