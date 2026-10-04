"""
BANKABLE HYDRO — Integrated Hydropower Project & Power-System Bankability Model
Builder script: generates model/Bankable_Hydro_Model.xlsx with live Excel formulas.

Design notes
- Annual model, 40 periods (t=1..40), first period = model start year.
- All money in USD million (USDm) nominal unless labelled "real 2026".
- Formulas are written as templates and resolved at the end, so sheets can
  reference each other regardless of build order:
    {name}      -> absolute reference to a scalar cell
    [name]      -> same-column cell of a time-series row
    [name@p]    -> previous-column cell of a time-series row
    [name@n]    -> next-column cell of a time-series row
    [RNG:name]  -> full absolute time-series range of a row
    [C:name]    -> total/summary cell (column C) of a time-series row
    #T#         -> period index t of the current column
- No macros, no circular references, no data tables. Scenario/structure
  snapshots are produced by tools/run_snapshots.py (LibreOffice headless).
"""
import re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L, column_index_from_string as CI
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.comments import Comment
from openpyxl.chart import LineChart, BarChart, Reference

OUT = "model/Bankable_Hydro_Model.xlsx"
N = 40
C0 = 5  # column E = t1
TCOLS = [L(C0 + i) for i in range(N)]
FIRSTC, LASTC = TCOLS[0], TCOLS[-1]

ARIAL = "Arial"
F_BASE = Font(name=ARIAL, size=10)
F_INPUT = Font(name=ARIAL, size=10, color="0000FF")
F_LINK = Font(name=ARIAL, size=10, color="008000")
F_CALC = Font(name=ARIAL, size=10, color="000000")
F_BOLD = Font(name=ARIAL, size=10, bold=True)
F_TITLE = Font(name=ARIAL, size=14, bold=True, color="FFFFFF")
F_SUB = Font(name=ARIAL, size=10, italic=True, color="FFFFFF")
F_SEC = Font(name=ARIAL, size=10, bold=True, color="1F3864")
F_HDR = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
FILL_TITLE = PatternFill("solid", fgColor="1F3864")
FILL_SEC = PatternFill("solid", fgColor="D9E1F2")
FILL_HDR = PatternFill("solid", fgColor="2F5597")
FILL_KEY = PatternFill("solid", fgColor="FFFF00")
FILL_INPUT = PatternFill("solid", fgColor="FFF2CC")
FILL_OUT = PatternFill("solid", fgColor="E2EFDA")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)

FMT = {
    "m": '#,##0.0;(#,##0.0);"-"',
    "m0": '#,##0;(#,##0);"-"',
    "gwh": '#,##0;(#,##0);"-"',
    "mw": '#,##0.0;(#,##0.0);"-"',
    "pct": '0.0%;(0.0%);"-"',
    "pct2": '0.00%;(0.00%);"-"',
    "x": '0.00"x";(0.00"x");"-"',
    "yr": '0',
    "int": '0;(0);"-"',
    "n2": '#,##0.00;(#,##0.00);"-"',
    "n3": '0.000',
    "usd": '#,##0.00;(#,##0.00);"-"',
    "txt": '@',
    "flag": '0;(0);"-"',
}

wb = Workbook()
wb.remove(wb.active)
wb.properties.creator = "Bankable Hydro"
wb.properties.lastModifiedBy = "Bankable Hydro"
wb.properties.title = "Bankable Hydro Integrated Bankability Model"
SHEETS = [
    "00_README", "01_CONTROL_PANEL", "01A_DEVELOPMENT", "02_PROJECT_INPUTS", "03_HYDROLOGY", "04_GENERATION",
    "05_PLANT_CAPEX", "05A_CONTRACTING", "06_CONSTRUCTION", "07_OPEX", "08_TRANSMISSION", "09_GRID", "10_DEMAND",
    "11_OFFTAKER", "12_UTILITY", "13_REGULATION", "14_PPA", "15_TARIFF", "16_REVENUE",
    "17_PROJECT_FINANCE", "17A_STRUCTURES", "18_DEBT", "19_EQUITY", "20_CASH_FLOW", "21_TAX",
    "22_GOVERNMENT_SUPPORT", "23_GUARANTEES", "24_CONTINGENT_LIABILITIES", "25_FISCAL_IMPACT",
    "26_DEBT_SUSTAINABILITY", "27_SCENARIOS", "28_SENSITIVITY", "29_RISK_ALLOCATION",
    "30_BANKABILITY", "30A_CLOSE_READINESS", "31_CASE_STUDY", "32_DASHBOARD", "33_CHECKS",
]
WS = {s: wb.create_sheet(s) for s in SHEETS}

REF = {}      # scalar name -> "'Sheet'!$C$r"
TSROW = {}    # ts name -> (sheet, row)
PENDING = []  # (ws, coord, template, col, t)


def q(sheet):
    return f"'{sheet}'"


def title(ws, text, sub, ts=False):
    ws.sheet_view.showGridLines = False
    last = LASTC if ts else "J"
    for c in range(1, CI(last) + 1):
        ws.cell(1, c).fill = FILL_TITLE
        ws.cell(2, c).fill = FILL_TITLE
    ws["A1"] = text
    ws["A1"].font = F_TITLE
    ws["A2"] = sub
    ws["A2"].font = F_SUB
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 4 if ts else 60
    if ts:
        for c in TCOLS:
            ws.column_dimensions[c].width = 10.5
        ws.freeze_panes = "E6"


def section(ws, r, text, ts=False):
    last = LASTC if ts else "J"
    for c in range(1, CI(last) + 1):
        ws.cell(r, c).fill = FILL_SEC
    ws.cell(r, 1, text).font = F_SEC


def put(ws, coord, template, fmt=None, t=None, col=None, font=None):
    PENDING.append((ws, coord, template, col, t, fmt, font))


def inp(ws, r, name, label, val, unit="", note="", fmt=None, key=False):
    ws.cell(r, 1, label).font = F_BASE
    ws.cell(r, 2, unit).font = F_BASE
    c = ws.cell(r, 3, val)
    c.font = F_INPUT
    c.fill = FILL_KEY if key else FILL_INPUT
    c.border = BOX
    if fmt:
        c.number_format = FMT[fmt]
    if note:
        ws.cell(r, 4, note).font = Font(name=ARIAL, size=9, italic=True, color="595959")
    if name:
        assert name not in REF, name
        REF[name] = f"{q(ws.title)}!$C${r}"


def calc(ws, r, name, label, template, unit="", fmt=None, note="", out=False):
    ws.cell(r, 1, label).font = F_BOLD if out else F_BASE
    ws.cell(r, 2, unit).font = F_BASE
    put(ws, f"C{r}", template, fmt)
    if out:
        ws.cell(r, 3).fill = FILL_OUT
    ws.cell(r, 3).border = BOX
    if note:
        ws.cell(r, 4, note).font = Font(name=ARIAL, size=9, italic=True, color="595959")
    if name:
        assert name not in REF, name
        REF[name] = f"{q(ws.title)}!$C${r}"


def ts(ws, r, name, label, unit, template, fmt="m", total=None, bold=False):
    ws.cell(r, 1, label).font = F_BOLD if bold else F_BASE
    ws.cell(r, 2, unit).font = F_BASE
    assert name not in TSROW, name
    TSROW[name] = (ws.title, r)
    for i, c in enumerate(TCOLS):
        tpl = template(i + 1) if callable(template) else template
        put(ws, f"{c}{r}", tpl, fmt, t=i + 1, col=c)
    if total == "sum":
        put(ws, f"C{r}", f"=SUM([RNG:{name}])", fmt)
    elif total == "max":
        put(ws, f"C{r}", f"=MAX([RNG:{name}])", fmt)
    elif total == "min":
        put(ws, f"C{r}", f"=MIN([RNG:{name}])", fmt)
    elif total:
        put(ws, f"C{r}", total, fmt)
    if bold:
        for c in TCOLS:
            ws[f"{c}{r}"].font = F_BOLD


def ts_header(ws, r=4):
    ws.cell(r, 1, "Calendar year").font = F_BOLD
    ws.cell(r + 1, 1, "Operating year (0 = construction/post-concession)").font = F_BASE
    ws.cell(r, 3, "Total / key").font = F_BOLD
    for c in TCOLS:
        if ws.title == "06_CONSTRUCTION":
            continue
        put(ws, f"{c}{r}", "=[year]", "yr", col=c)
        put(ws, f"{c}{r+1}", "=[opyr]", "int", col=c)
        ws[f"{c}{r}"].fill = FILL_HDR
    for cc in range(1, 4):
        ws.cell(r, cc).fill = FILL_SEC


def note(ws, r, text, col=1):
    ws.cell(r, col, text).font = Font(name=ARIAL, size=9, italic=True, color="595959")


def resolve(tpl, col, t):
    def scal(m):
        n = m.group(1)
        if n not in REF:
            raise KeyError(f"Unknown scalar {n} in {tpl}")
        return REF[n]

    def tsr(m):
        body = m.group(1)
        if body.startswith("RNG:"):
            n = body[4:]
            s, r = TSROW[n]
            return f"{q(s)}!${FIRSTC}${r}:${LASTC}${r}"
        if body.startswith("C:"):
            n = body[2:]
            s, r = TSROW[n]
            return f"{q(s)}!$C${r}"
        n, _, mod = body.partition("@")
        if n not in TSROW:
            raise KeyError(f"Unknown ts {n} in {tpl}")
        s, r = TSROW[n]
        cc = col
        if mod == "p":
            cc = L(CI(col) - 1)
        elif mod == "n":
            cc = L(CI(col) + 1)
        return f"{q(s)}!{cc}{r}"

    out = re.sub(r"\{(\w+)\}", scal, tpl)
    out = re.sub(r"\[([A-Za-z0-9_:@]+)\]", tsr, out)
    if t is not None:
        out = out.replace("#T#", str(t))
    return out


def finalize():
    for ws, coord, tpl, col, t, fmt, font in PENDING:
        f = resolve(tpl, col, t) if isinstance(tpl, str) else tpl
        cell = ws[coord]
        cell.value = f
        if font is not None:
            cell.font = font
        elif isinstance(f, str) and re.fullmatch(r"='[^']+'![$A-Z]+[$0-9]+", f) and f"'{ws.title}'" not in f:
            cell.font = F_LINK
        elif cell.font is None or not cell.font.bold:
            cell.font = F_CALC
        if fmt:
            cell.number_format = FMT[fmt]


def dv_list(ws, rng, options):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(rng)


# ===================================================================================
# 01 CONTROL PANEL
# ===================================================================================
ws = WS["01_CONTROL_PANEL"]
title(ws, "01 CONTROL PANEL — Scenario, structure and case selection",
      "Blue = input. Yellow = key lever. Every stress toggle can be combined with any other.")
r = 4
section(ws, r, "A. CASE & GENERATION SELECTION"); r += 1
inp(ws, r, "case", "Model case (1=Base, 2=Low, 3=High)", 1, "1-3", "Case multipliers in 27_SCENARIOS", "int", True); r += 1
inp(ws, r, "gen_case", "Generation case for cash flows (1=P50, 2=P75, 3=P90)", 1, "1-3", "Equity / sponsor case usually P50", "int", True); r += 1
inp(ws, r, "lender_case", "Lender sizing generation case (1=P50, 2=P75, 3=P90 one-year, 4=P90 ten-year)", 4, "1-4", "Lenders typically size debt on a P90 (one-year) case — verify with lenders' technical adviser", "int", True); r += 1
section(ws, r, "B. TRANSACTION STRUCTURE"); r += 1
inp(ws, r, "structure", "Financing / PPP structure (1-5, see 17A_STRUCTURES)", 2, "1-5", "1 Public | 2 IPP | 3 PPP | 4 Hybrid | 5 Blended finance", "int", True); r += 1
calc(ws, r, "structure_name", "Selected structure", "={str_name}", "", None); r += 1
inp(ws, r, "debt_mode", "Debt sizing mode (1=sculpted in-model, 2=locked amounts)", 1, "1-2", "Use 2 to stress a FIXED debt package (paste base-case amounts in 18_DEBT)", "int", True); r += 1
inp(ws, r, "backstop", "Government budget backstop of utility PPA shortfall (1=yes, 0=no)", 1, "0/1", "1: shortfall becomes a fiscal cost. 0: shortfall becomes a guarantee call or IPP arrears", "int", True); r += 1
inp(ws, r, "bs_share", "Share of the shortfall the budget backstop covers", 1.0, "%", "Remainder goes to the PPA guarantee, then to arrears", "pct"); r += 1
section(ws, r, "C. STRESS TOGGLES (1 = ON). Parameters in 27_SCENARIOS"); r += 1
for nm, lab in [("st_drought", "Drought case"), ("st_capex", "CAPEX overrun"), ("st_delay", "Construction delay"),
                ("st_demand", "Low demand"), ("st_offtaker", "Offtaker stress"), ("st_fx", "FX depreciation"),
                ("st_rate", "High interest rate"), ("st_trans", "Transmission delay"), ("st_climate", "Climate trend on flows")]:
    inp(ws, r, nm, lab, 0, "0/1", "", "int", True); r += 1
section(ws, r, "D. SENSITIVITY FLEXES (applied on top of case & stresses)"); r += 1
inp(ws, r, "fx_capex", "CAPEX flex", 0.0, "%", "e.g. 0.10 = +10%", "pct"); r += 1
inp(ws, r, "fx_gen", "Generation (flow) flex", 0.0, "%", "", "pct"); r += 1
inp(ws, r, "fx_tariff", "PPA tariff flex", 0.0, "%", "", "pct"); r += 1
inp(ws, r, "fx_opex", "OPEX flex", 0.0, "%", "", "pct"); r += 1
inp(ws, r, "fx_rate", "Commercial interest rate flex (absolute)", 0.0, "%", "e.g. 0.01 = +100 bps", "pct2"); r += 1
section(ws, r, "E. ACTIVE SCENARIO READ-OUT"); r += 1
calc(ws, r, None, "Active stress count", "=SUM({st_drought},{st_capex},{st_delay},{st_demand},{st_offtaker},{st_fx},{st_rate},{st_trans},{st_climate})", "#", "int"); r += 1
calc(ws, r, None, "Project IRR (post-tax, unlevered)", "={kpi_pirr}", "%", "pct", out=True); r += 1
calc(ws, r, None, "Private equity IRR", "={kpi_eirr}", "%", "pct", out=True); r += 1
calc(ws, r, None, "Minimum DSCR (actual case)", "={kpi_min_dscr}", "x", "x", out=True); r += 1
calc(ws, r, None, "Financing gap", "={fin_gap}", "USDm", "m", out=True); r += 1
calc(ws, r, None, "Fiscal NPV to government (negative = net cost)", "={fis_npv}", "USDm", "m", out=True); r += 1
calc(ws, r, None, "Consolidated fiscal NPV incl. state utility", "={fis_npv_cons}", "USDm", "m", out=True); r += 1
calc(ws, r, None, "Developer IRR (success path)", "={dev_irr}", "%", "pct", out=True); r += 1
calc(ws, r, None, "Financial close decision (23 gates)", "={fc_decision}", "", None, out=True); r += 1
calc(ws, r, None, "Overall bankability verdict", "={bk_overall}", "", None, out=True); r += 1
calc(ws, r, None, "Model integrity checks", "={chk_all}", "", None, out=True); r += 1
for nm in ["case", "gen_case", "lender_case"]:
    pass
dv = DataValidation(type="whole", operator="between", formula1="1", formula2="4"); ws.add_data_validation(dv)
dv.add("C5:C7")
dv5 = DataValidation(type="whole", operator="between", formula1="1", formula2="5"); ws.add_data_validation(dv5); dv5.add("C9")
dvb = DataValidation(type="whole", operator="between", formula1="0", formula2="1"); ws.add_data_validation(dvb)
dvb.add("C12"); dvb.add("C15:C23")
dv2 = DataValidation(type="whole", operator="between", formula1="1", formula2="2"); ws.add_data_validation(dv2); dv2.add("C11")

# ===================================================================================
# 02 PROJECT INPUTS
# ===================================================================================
ws = WS["02_PROJECT_INPUTS"]
title(ws, "02 PROJECT INPUTS — Fictional reference project: Kasiri River Hydro (60 MW private IPP)",
      "All data FICTIONAL, constructed for training. Not based on any confidential project data.")
r = 4
section(ws, r, "A. PROJECT IDENTITY"); r += 1
inp(ws, r, "proj_name", "Project name", "Kasiri River Hydro (KRH)", "", "Fictional 60 MW private IPP"); r += 1
inp(ws, r, "country", "Country", "Republic of Navaria", "", "Fictional sub-Saharan African country"); r += 1
inp(ws, r, "river", "River / basin", "Kasiri River", "", "Fictional; bimodal tropical regime, steep catchment"); r += 1
inp(ws, r, "scheme", "Scheme type", "Run-of-river with small daily pondage", "", ""); r += 1
section(ws, r, "B. TIMING"); r += 1
inp(ws, r, "start_year", "Model start / financial close year (t=1)", 2027, "year", "", "yr", True); r += 1
inp(ws, r, "base_year", "Price base year for real inputs", 2026, "year", "All 'real' inputs in 2026 USD", "yr"); r += 1
inp(ws, r, "cons_years", "Base construction period", 3, "years", "IFC 2015: up to about 4 years for larger hydro; SSA small hydro observed 19-29 months [hydro_development_evidence]", "int", True); r += 1
inp(ws, r, "ops_years", "Concession / PPA operating term", 25, "years", "PPA 20 years plus an assumed 5-year extension at the same tariff (assumption)", "int", True); r += 1
section(ws, r, "C. PLANT"); r += 1
inp(ws, r, "inst_mw", "Installed capacity", 60, "MW", "3 x 20 MW Francis units (fictional)", "mw", True); r += 1
inp(ws, r, "units", "Number of units", 3, "#", "", "int"); r += 1
section(ws, r, "D. MACRO (USD model with local-currency utility)"); r += 1
inp(ws, r, "us_cpi", "US CPI (USD indexation)", 0.02, "% p.a.", "Assumption", "pct"); r += 1
inp(ws, r, "lc_cpi", "Local CPI (Navarian lira, NVL)", 0.08, "% p.a.", "Assumption", "pct"); r += 1
inp(ws, r, "fx0", "FX rate in base year", 20.0, "NVL/USD", "Fictional", "n2"); r += 1
inp(ws, r, "fx_dep", "Base-case nominal depreciation of NVL vs USD", 0.06, "% p.a.", "Roughly inflation differential (PPP) — assumption", "pct", True); r += 1
inp(ws, r, "capex_esc", "CAPEX escalation during construction", 0.025, "% p.a.", "", "pct"); r += 1
inp(ws, r, "disc_rate", "Project discount rate (nominal USD) for NPV/LCOE", 0.10, "%", "Assumption; replace with sponsor WACC", "pct", True); r += 1
inp(ws, r, "gov_disc", "Government discount rate for fiscal PV", 0.08, "%", "Proxy: sovereign USD borrowing cost — assumption", "pct", True); r += 1

# ===================================================================================
# 27 SCENARIOS (inputs + effective levers) — built early for references
# ===================================================================================
ws = WS["27_SCENARIOS"]
title(ws, "27 SCENARIOS — Case table, stress parameters and effective levers",
      "Cases are mutually exclusive; stresses are additive toggles (01_CONTROL_PANEL). Snapshot table filled by tools/run_snapshots.py")
ws.column_dimensions["D"].width = 12
for c, h in zip("ABCDEF", ["Case parameter", "Unit", "Base", "Low", "High", "Note"]):
    ws[f"{c}4"] = h; ws[f"{c}4"].font = F_HDR; ws[f"{c}4"].fill = FILL_HDR
CASE_ROWS = [
    ("case_flow", "Hydrology (flow) factor", "x", 1.00, 0.93, 1.04, "Applies to all years"),
    ("case_capex", "CAPEX factor", "x", 1.00, 1.10, 0.95, ""),
    ("case_demg", "Demand growth adjustment (added to each segment)", "pp", 0.0, -0.015, 0.01, ""),
    ("case_opex", "OPEX factor", "x", 1.00, 1.10, 0.95, ""),
]
r = 5
for nm, lab, u, b, lo, hi, nt in CASE_ROWS:
    ws.cell(r, 1, lab).font = F_BASE; ws.cell(r, 2, u).font = F_BASE
    for j, v in enumerate([b, lo, hi]):
        c = ws.cell(r, 3 + j, v); c.font = F_INPUT; c.fill = FILL_INPUT; c.border = BOX
        c.number_format = FMT["pct"] if u == "pp" else FMT["n2"]
    ws.cell(r, 6, nt).font = F_BASE
    REF[nm] = f"CHOOSE({REF['case']},{q(ws.title)}!$C${r},{q(ws.title)}!$D${r},{q(ws.title)}!$E${r})"
    r += 1
r += 1
section(ws, r, "STRESS PARAMETERS (applied only when the toggle is ON)"); r += 1
inp(ws, r, "p_drought", "Drought: flow factor during drought window", 0.55, "x", "Kariba 2024 allocation cut ~47% (news) [CL-04]; calibrate to the basin's worst sequence", "n2"); r += 1
inp(ws, r, "p_drought_start", "Drought: first operating year affected", 4, "op yr", "", "int"); r += 1
inp(ws, r, "p_drought_len", "Drought: duration", 3, "years", "Multi-year droughts occurred at Kariba (see case library)", "int"); r += 1
inp(ws, r, "p_overrun", "CAPEX overrun", 0.27, "%", "Ansar et al. 2014: median real overrun +27%, mean +96% [HY-08]", "pct"); r += 1
inp(ws, r, "p_delay", "Construction delay", 2, "years", "Ansar et al. 2014: mean schedule overrun 2.3 yrs, median 1.7 [HY-08]", "int"); r += 1
inp(ws, r, "p_lowdem", "Low demand: demand level factor", 0.80, "x", "", "n2"); r += 1
inp(ws, r, "p_coll_drop", "Offtaker stress: fall in collection rate (from COD)", 0.08, "pp", "", "pct"); r += 1
inp(ws, r, "p_sub_cut", "Offtaker stress: cut in government transfers to utility (from COD)", 0.30, "%", "", "pct"); r += 1
inp(ws, r, "p_freeze", "Offtaker stress: retail tariff freeze from COD", 5, "years", "Nominal freeze, then indexation resumes (level not recovered)", "int"); r += 1
inp(ws, r, "p_fx_shock", "FX stress: one-off step devaluation (NVL per USD rises by)", 0.50, "%", "Step at plant COD, on top of trend; cf. recent large devaluations in SSA", "pct"); r += 1
inp(ws, r, "p_rate_add", "High interest: add-on to commercial rate", 0.03, "% abs", "Concessional debt assumed fixed-rate", "pct"); r += 1
inp(ws, r, "p_trans_delay", "Transmission delay", 2, "years", "", "int"); r += 1
inp(ws, r, "p_climate", "Climate trend on mean flows", -0.03, "% / decade", "Illustrative; must come from basin-specific climate study", "pct"); r += 1
r += 1
section(ws, r, "EFFECTIVE LEVERS USED BY THE ENGINE"); r += 1
calc(ws, r, "eff_flow", "Effective flow factor", "={case_flow}*(1+{fx_gen})", "x", "n3"); r += 1
calc(ws, r, "eff_capex", "Effective CAPEX factor (overrun borne by owner per contracting structure)", "={case_capex}*(1+{st_capex}*{p_overrun}*{epc_owner})*(1+{fx_capex})", "x", "n3"); r += 1
calc(ws, r, "eff_delay", "Effective construction delay", "={st_delay}*{p_delay}", "years", "int"); r += 1
calc(ws, r, "eff_demg", "Demand growth adjustment", "={case_demg}", "pp", "pct"); r += 1
calc(ws, r, "eff_dem", "Demand level factor", "=IF({st_demand}=1,{p_lowdem},1)", "x", "n3"); r += 1
calc(ws, r, "eff_coll_adj", "Collection-rate adjustment", "=-{st_offtaker}*{p_coll_drop}", "pp", "pct"); r += 1
calc(ws, r, "eff_sub", "Government transfer factor", "=1-{st_offtaker}*{p_sub_cut}", "x", "n3"); r += 1
calc(ws, r, "eff_freeze", "Retail tariff freeze", "={st_offtaker}*{p_freeze}", "years", "int"); r += 1
calc(ws, r, "eff_fxdep", "FX trend depreciation", "={fx_dep}", "% p.a.", "pct"); r += 1
calc(ws, r, "eff_fxshock", "FX step devaluation at COD", "={st_fx}*{p_fx_shock}", "%", "pct"); r += 1
calc(ws, r, "eff_rate_add", "Commercial rate add-on", "={st_rate}*{p_rate_add}+{fx_rate}", "% abs", "pct2"); r += 1
calc(ws, r, "eff_tdelay", "Transmission delay", "={st_trans}*{p_trans_delay}", "years", "int"); r += 1
calc(ws, r, "eff_climate", "Climate trend", "={st_climate}*{p_climate}", "%/decade", "pct"); r += 1
calc(ws, r, "eff_opex", "OPEX factor", "={case_opex}*(1+{fx_opex})", "x", "n3"); r += 1
calc(ws, r, "eff_tariff", "Tariff factor", "=1+{fx_tariff}", "x", "n3"); r += 1
SCEN_SNAP_ROW = r + 2

# ===================================================================================
# 03 HYDROLOGY
# ===================================================================================
ws = WS["03_HYDROLOGY"]
title(ws, "03 HYDROLOGY — Flow, head, efficiency → monthly & annual energy; P50/P75/P90",
      "Installed vs available vs expected vs contracted energy are kept distinct (see 04_GENERATION)")
r = 4
section(ws, r, "A. PLANT HYDRAULIC PARAMETERS"); r += 1
inp(ws, r, "q_design", "Design (rated) turbine flow", 57, "m3/s", "Fictional", "m0", True); r += 1
inp(ws, r, "head", "Net rated head", 120, "m", "Fictional", "m0", True); r += 1
inp(ws, r, "eta_t", "Turbine efficiency", 0.92, "%", "Assumption (not sourced)", "pct"); r += 1
inp(ws, r, "eta_g", "Generator & transformer efficiency", 0.98, "%", "Assumption", "pct"); r += 1
inp(ws, r, "eflow", "Environmental flow release", 4, "m3/s", "Set by ESIA / water permit", "m0", True); r += 1
inp(ws, r, "avail", "Plant availability (planned + forced outages)", 0.95, "%", "Assumption", "pct", True); r += 1
inp(ws, r, "ramp", "First operating year availability factor (commissioning ramp)", 0.85, "x", "", "n2"); r += 1
inp(ws, r, "rho", "Water density", 1000, "kg/m3", "Physical constant", "m0"); r += 1
inp(ws, r, "grav", "Gravity", 9.81, "m/s2", "Physical constant", "n2"); r += 1
section(ws, r, "B. HYDROLOGICAL UNCERTAINTY"); r += 1
inp(ws, r, "cv", "Inter-annual coefficient of variation of energy", 0.15, "%", "Small, steep catchment: more variable than a large river (assumption)", "pct", True); r += 1
inp(ws, r, "z75", "Normal z-score for P75", 0.6745, "", "Normal approximation; replace with empirical distribution if available", "n3"); r += 1
inp(ws, r, "z90", "Normal z-score for P90", 1.2816, "", "", "n3"); r += 1
inp(ws, r, "rec_years", "Length of reliable flow record", 12, "years", "Gauging started at pre-feasibility plus regional correlation (fictional)", "int", True); r += 1
inp(ws, r, "hyd_study", "Hydrology study maturity (1=desk, 2=FS-level, 3=independent review)", 2, "1-3", "Gate 1 test", "int", True); r += 1
r += 1
section(ws, r, "C. MONTHLY MEAN FLOW (long-term average, fictional bimodal regime)"); r += 1
hdr = r
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
days = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
flows = [24, 20, 28, 52, 70, 58, 40, 28, 22, 30, 46, 36]
ws.cell(hdr, 1, "Month").font = F_HDR
for j, m in enumerate(months):
    c = ws.cell(hdr, 5 + j, m); c.font = F_HDR; c.fill = FILL_HDR
    ws.column_dimensions[L(5 + j)].width = 9
ws.cell(hdr, 3, "Annual").font = F_HDR
for cc in range(1, 5):
    ws.cell(hdr, cc).fill = FILL_HDR
rows = {}
labels = [("days", "Days in month", "days"), ("flow", "Mean river flow", "m3/s"),
          ("usable", "Usable turbine flow = MIN(MAX(Q - e-flow,0), Q design)", "m3/s"),
          ("pw", "Average power = MIN(rho*g*Q*H*eta/1e6, installed)", "MW"),
          ("egross", "Energy at 100% availability", "GWh"), ("enet", "Expected energy (x availability)", "GWh"),
          ("spill", "Spilled flow above design flow", "m3/s")]
for k, (key, lab, u) in enumerate(labels):
    rr = hdr + 1 + k
    rows[key] = rr
    ws.cell(rr, 1, lab).font = F_BASE; ws.cell(rr, 2, u).font = F_BASE
for j in range(12):
    col = L(5 + j)
    c = ws[f"{col}{rows['days']}"]; c.value = days[j]; c.font = F_INPUT; c.number_format = FMT["n2"]
    c = ws[f"{col}{rows['flow']}"]; c.value = flows[j]; c.font = F_INPUT; c.fill = FILL_INPUT; c.number_format = FMT["m0"]
    put(ws, f"{col}{rows['usable']}", f"=MIN(MAX({col}{rows['flow']}-{{eflow}},0),{{q_design}})", "m0")
    put(ws, f"{col}{rows['pw']}", f"=MIN({{rho}}*{{grav}}*{col}{rows['usable']}*{{head}}*{{eta_t}}*{{eta_g}}/1000000,{{inst_mw}})", "mw")
    put(ws, f"{col}{rows['egross']}", f"={col}{rows['pw']}*{col}{rows['days']}*24/1000", "gwh")
    put(ws, f"{col}{rows['enet']}", f"={col}{rows['egross']}*{{avail}}", "gwh")
    put(ws, f"{col}{rows['spill']}", f"=MAX({col}{rows['flow']}-{{eflow}}-{{q_design}},0)", "m0")
rng = lambda k: f"E{rows[k]}:P{rows[k]}"
put(ws, f"C{rows['flow']}", f"=SUMPRODUCT({rng('flow')},{rng('days')})/SUM({rng('days')})", "m0")
put(ws, f"C{rows['pw']}", f"=SUMPRODUCT({rng('pw')},{rng('days')})/SUM({rng('days')})", "mw")
put(ws, f"C{rows['egross']}", f"=SUM({rng('egross')})", "gwh")
put(ws, f"C{rows['enet']}", f"=SUM({rng('enet')})", "gwh")
note(ws, rows['spill'] + 1, "Methodology note: energy from long-term mean monthly flows overstates energy when flows exceed design flow in some years (Jensen's inequality). Replace with a daily/monthly simulation over the full record when available.")
r = rows['spill'] + 3
section(ws, r, "D. ANNUAL ENERGY STATISTICS"); r += 1
calc(ws, r, "p50", "P50 annual energy (expected, long-term)", f"=C{rows['enet']}", "GWh", "gwh", out=True); r += 1
calc(ws, r, "p75", "P75 annual energy", "={p50}*(1-{z75}*{cv})", "GWh", "gwh", out=True); r += 1
calc(ws, r, "p90", "P90 annual energy (one-year)", "={p50}*(1-{z90}*{cv})", "GWh", "gwh", out=True); r += 1
inp(ws, r, "rho1", "Year-to-year correlation of annual energy (persistence of dry years)", 0.3, "", "Assumption; estimate from the flow record", "n2"); r += 1
calc(ws, r, "p90_10", "P90 of the 10-year average energy (allowing for persistence)", "={p50}*(1-{z90}*{cv}*SQRT((1+{rho1})/(1-{rho1})/10))", "GWh", "gwh", out=True); r += 1
calc(ws, r, "cf", "Capacity factor at P50", "={p50}/({inst_mw}*8.76)", "%", "pct", out=True); r += 1
calc(ws, r, "avail_mw", "Available capacity (installed x availability)", "={inst_mw}*{avail}", "MW", "mw"); r += 1
calc(ws, r, "avg_mw", "Average output at P50", "={p50}/8.76", "MW", "mw"); r += 1
calc(ws, r, "firm_mw", "Dry-season firm output (lowest month)", f"=MIN({rng('pw')})*{{avail}}", "MW", "mw"); r += 1
calc(ws, r, "p90_p50", "P90 / P50 ratio", "={p90}/{p50}", "x", "n3"); r += 1
calc(ws, r, "check_power", "Check: theoretical power at design flow", "={rho}*{grav}*{q_design}*{head}*{eta_t}*{eta_g}/1000000", "MW", "mw", "Should be ≥ installed capacity"); r += 1

# ===================================================================================
# 06 CONSTRUCTION (timeline master)
# ===================================================================================
ws = WS["06_CONSTRUCTION"]
title(ws, "06 CONSTRUCTION — Timeline master, escalation & FX indices, CAPEX phasing", "Timeline flags drive every time-series sheet", ts=True)
r = 4
ts(ws, r, "year", "Calendar year", "", "={start_year}+#T#-1", "yr"); r += 1
ts(ws, r, "opyr", "Operating year", "#", "=IF([opflag]=1,#T#-{cons_eff},0)", "int"); r += 1
r += 1
calc(ws, r, "cons_eff", "Effective construction period", "={cons_years}+{eff_delay}", "years", "int"); r += 1
calc(ws, r, "cod_year", "Commercial operation date (first full operating year)", "={start_year}+{cons_eff}", "year", "yr", out=True); r += 1
calc(ws, r, "capex_real", "Plant CAPEX (real 2026), incl. case, overrun & delay costs", "={capex_base}*{eff_capex}*(1+{delay_cost}*{eff_delay}*{epc_owner_d})", "USDm", "m", out=True); r += 1
r += 1
section(ws, r, "TIMING FLAGS", ts=True); r += 1
ts(ws, r, "t", "Period index t", "#", "=#T#", "int"); r += 1
ts(ws, r, "consflag", "Construction flag", "flag", "=IF(#T#<={cons_eff},1,0)", "flag"); r += 1
ts(ws, r, "opflag", "Operations flag", "flag", "=IF(AND(#T#>{cons_eff},#T#<={cons_eff}+{ops_years}),1,0)", "flag", total="sum"); r += 1
ts(ws, r, "lastcons", "Last construction year flag", "flag", "=IF(#T#={cons_eff},1,0)", "flag"); r += 1
section(ws, r, "INDICES", ts=True); r += 1
ts(ws, r, "uscpi", "US CPI index (2026 = 1)", "x", "=(1+{us_cpi})^([year]-{base_year})", "n3"); r += 1
ts(ws, r, "lccpi", "Local CPI index (2026 = 1)", "x", "=(1+{lc_cpi})^([year]-{base_year})", "n3"); r += 1
ts(ws, r, "fx", "FX rate", "NVL/USD", "={fx0}*(1+{eff_fxdep})^([year]-{base_year})*IF([year]>={cod_year},1+{eff_fxshock},1)", "n2"); r += 1
ts(ws, r, "fxidx", "FX index (2026 = 1)", "x", "=[fx]/{fx0}", "n3"); r += 1
ts(ws, r, "escidx", "CAPEX escalation index", "x", "=(1+{capex_esc})^([year]-{base_year})", "n3"); r += 1
section(ws, r, "PLANT CAPEX PHASING (sine S-curve over effective construction period)", ts=True); r += 1
ts(ws, r, "share", "CAPEX share (sums to 100%)", "%", "=IF([consflag]=1,SIN(PI()*(#T#-0.5)/{cons_eff})*SIN(PI()/(2*{cons_eff})),0)", "pct", total="sum"); r += 1
ts(ws, r, "cumsh", "Cumulative CAPEX share", "%", "=[cumsh@p]+[share]", "pct"); r += 1
ts(ws, r, "capex_nom", "Plant CAPEX, nominal", "USDm", "={capex_real}*[share]*[escidx]", "m", total="sum", bold=True); r += 1
note(ws, r + 1, "S-curve weight_t = sin(pi(t-0.5)/N)·sin(pi/2N) — closed form that sums exactly to 1 for any N. Replace with EPC payment schedule when available.")

# ===================================================================================
# 05 PLANT CAPEX
# ===================================================================================
ws = WS["05_PLANT_CAPEX"]
title(ws, "05 PLANT CAPEX — Real 2026 USD, before escalation", "Fictional cost estimate; compare with benchmark ranges (source database)")
r = 4
section(ws, r, "A. COST BREAKDOWN (real 2026 USDm)"); r += 1
items = [("cx_civil", "Civil works (weir, intake, headrace tunnel, penstock, powerhouse)", 68),
         ("cx_hm", "Hydro-mechanical (gates, steel lining)", 9),
         ("cx_em", "Electro-mechanical (turbines, generators, switchyard)", 33),
         ("cx_es", "Environmental & social (RAP, livelihood, offsets)", 5),
         ("cx_eng", "Engineering, supervision, owner's engineer", 8),
         ("cx_own", "Owner's costs during construction", 4)]
first = r
for nm, lab, v in items:
    inp(ws, r, nm, lab, v, "USDm", "Fictional", "m"); r += 1
calc(ws, r, "cx_dev", "Development costs reimbursed at financial close (from 01A_DEVELOPMENT)", "={dev_total}", "USDm", "m"); r += 1
calc(ws, r, "cx_epcprem", "Contractor risk premium on civil, hydro-mechanical and E&M works (from 05A_CONTRACTING)", "=({cx_civil}+{cx_hm}+{cx_em})*{epc_prem}", "USDm", "m"); r += 1
calc(ws, r, "cx_sub", "Subtotal before contingency", f"=SUM(C{first}:C{r-1})", "USDm", "m"); r += 1
inp(ws, r, "cont", "Physical contingency", 0.1, "%", "IFC 2015: median contingency 9.8% of total plant cost (5.4-12.6%)", "pct", True); r += 1
calc(ws, r, "capex_base", "Base plant CAPEX (real 2026)", "={cx_sub}*(1+{cont})", "USDm", "m", out=True); r += 1
calc(ws, r, "capex_kw", "Unit CAPEX", "={capex_base}/{inst_mw}*1000", "USD/kW", "m0", out=True); r += 1
inp(ws, r, "delay_cost", "Additional cost per year of delay (claims, owner's costs, escalation)", 0.04, "% per yr", "Assumption", "pct"); r += 1
inp(ws, r, "fs_level", "Feasibility maturity (1=pre-FS, 2=FS, 3=bankable FS + LTA review)", 2, "1-3", "Gate 3 test", "int", True); r += 1
section(ws, r, "B. BENCHMARK (see research/source_database.md)"); r += 1
inp(ws, r, "bm_kw", "Benchmark unit CAPEX — central", 2515, "USD/kW", "IRENA RPGC 2024 Table 6.3: Africa large hydro weighted avg 2018-24 = 2,515 (2024 USD/kW); range 2,330-3,290 [HY-01, PF-11]. Price-year difference vs 2026 not adjusted", "m0", True); r += 1
calc(ws, r, "capex_vs_bm", "Unit CAPEX / benchmark", "={capex_kw}/{bm_kw}", "x", "x"); r += 1
BM_ROW = r - 2

# ===================================================================================
# 08 TRANSMISSION
# ===================================================================================
ws = WS["08_TRANSMISSION"]
title(ws, "08 TRANSMISSION — Evacuation line, substations, reinforcement, readiness gap",
      "Question: can the plant evacuate the electricity it generates?", ts=True)
r = 6
section(ws, r, "A. INPUTS", ts=True); r += 1
inp(ws, r, "tx_point", "Connection point", "Kabanga 400 kV substation (fictional)", "", ""); r += 1
inp(ws, r, "tx_km", "Line length", 35, "km", "", "m0", True); r += 1
inp(ws, r, "tx_kv", "Voltage", 132, "kV", "", "m0"); r += 1
inp(ws, r, "tx_mw", "Line thermal / stability transfer capacity", 120, "MW", "Confirm with load-flow study", "m0", True); r += 1
inp(ws, r, "tx_cost_km", "Line cost per km (real 2026)", 0.22, "USDm/km", "Assumption for 132 kV single circuit; EAPP 2014 lists 220 kV at 0.27-0.63 USDm(2012)/km [TX-04]", "n2", True); r += 1
inp(ws, r, "tx_sub", "Substations & switchyard extension", 6, "USDm", "Fictional", "m"); r += 1
inp(ws, r, "tx_reinf", "Downstream grid reinforcement", 3, "USDm", "Fictional; from grid-impact study", "m"); r += 1
inp(ws, r, "tx_build", "Transmission construction period", 2, "years", "", "int"); r += 1
inp(ws, r, "tx_loss", "Transmission losses to load centre", 0.02, "%", "Assumption", "pct"); r += 1
inp(ws, r, "tx_om", "Transmission O&M", 0.015, "% capex p.a.", "Assumption", "pct"); r += 1
inp(ws, r, "tx_party", "Who builds & finances transmission (1=Government/utility, 2=Project company)", 2, "1-2", "Project builds the interconnector and transfers it to the utility at COD", "int", True); r += 1
inp(ws, r, "tx_lag", "Planned transmission COD relative to plant COD (years, + = late)", 0, "years", "", "int"); r += 1
inp(ws, r, "tx_interim", "Interim evacuation via existing network", 0, "MW", "If line not ready", "m0"); r += 1
inp(ws, r, "tx_wheel", "Wheeling / use-of-system charge borne by project", 0.0, "USD/MWh", "Set >0 for third-party/export sales", "n2"); r += 1
inp(ws, r, "tx_fin", "Transmission financing secured (1=yes, 0=no)", 1, "0/1", "Inside the project financing package", "int", True); r += 1
section(ws, r, "B. CALCULATIONS", ts=True); r += 1
calc(ws, r, "tx_capex_real", "Transmission CAPEX (real 2026, incl. case & overrun)", "=({tx_km}*{tx_cost_km}+{tx_sub}+{tx_reinf})*{eff_capex}", "USDm", "m", out=True); r += 1
calc(ws, r, "tx_cod_plan", "Planned transmission COD (year)", "={start_year}+{cons_years}+{tx_lag}", "year", "yr"); r += 1
calc(ws, r, "tx_cod", "Actual transmission COD (year)", "={tx_cod_plan}+{eff_tdelay}", "year", "yr", out=True); r += 1
calc(ws, r, "tx_gap_yrs", "Transmission readiness gap — timing", "={tx_cod}-{cod_year}", "years", "int", out=True); r += 1
calc(ws, r, "tx_gap_mw", "Transmission readiness gap — capacity at plant COD", "=MAX(0,{inst_mw}-{evac_cod})", "MW", "m0", out=True); r += 1
calc(ws, r, "tx_cost_kw", "Connection cost per kW of plant", "={tx_capex_real}/{inst_mw}*1000", "USD/kW", "m0"); r += 1
r += 1
ts(ws, r, "tx_ready", "Transmission line in service flag", "flag", "=IF([year]>={tx_cod},1,0)", "flag"); r += 1
ts(ws, r, "tx_spend", "Transmission CAPEX, nominal", "USDm", "=IF(AND([year]>={tx_cod_plan}-{tx_build},[year]<{tx_cod}),{tx_capex_real}*(1+{delay_cost}*{eff_tdelay})/({tx_build}+{eff_tdelay})*[escidx],0)", "m", total="sum"); r += 1
ts(ws, r, "tx_spend_pub", "  of which public (Government/utility)", "USDm", "=IF({tx_party}=1,[tx_spend],0)", "m", total="sum"); r += 1
ts(ws, r, "tx_spend_prj", "  of which project company", "USDm", "=IF({tx_party}=2,[tx_spend],0)", "m", total="sum"); r += 1
ts(ws, r, "tx_omc", "Transmission O&M (once in service)", "USDm", "=[tx_ready]*[opflag]*{tx_capex_real}*{tx_om}*[uscpi]", "m", total="sum"); r += 1
ts(ws, r, "tx_lossg", "Transmission losses on delivered energy", "GWh", "=[delivered]*{tx_loss}", "gwh", total="sum"); r += 1
ts(ws, r, "tx_wheelc", "Wheeling charges paid by project", "USDm", "=[delivered]*{tx_wheel}*[uscpi]/1000", "m", total="sum"); r += 1

# ===================================================================================
# 10 DEMAND
# ===================================================================================
ws = WS["10_DEMAND"]
title(ws, "10 DEMAND — Potential vs commercial vs contracted vs bankable demand", "Segment growth by case; 'bankable' = contracted AND absorbable by creditworthy demand", ts=True)
r = 6
section(ws, r, "A. SEGMENT INPUTS (base year 2026)", ts=True); r += 1
for c, h in zip(["A", "B", "C", "D", "E", "F", "G", "H"], ["Segment", "GWh 2026", "Growth Base", "", "Growth Low", "Growth High", "Ability-to-pay share", ""]):
    pass
ws.cell(r, 1, "Segment").font = F_HDR; ws.cell(r, 2, "GWh 2026").font = F_HDR; ws.cell(r, 3, "Growth base").font = F_HDR
ws.cell(r, 5, "Growth low").font = F_HDR; ws.cell(r, 6, "Growth high").font = F_HDR; ws.cell(r, 7, "Commercial share").font = F_HDR
for cc in range(1, 8):
    ws.cell(r, cc).fill = FILL_HDR
r += 1
segs = [("res", "Residential", 2600, .07, .05, .085, .75), ("com", "Commercial", 1400, .06, .045, .075, .92),
        ("ind", "Industrial", 1500, .05, .03, .065, .95), ("min", "Mining", 1100, .06, .02, .09, .98),
        ("pu", "Productive use (agri-processing etc.)", 250, .10, .06, .14, .70), ("pub", "Public sector", 450, .04, .03, .05, .65)]
seg_rows = {}
for k, lab, g0, gb, gl, gh, cs in segs:
    ws.cell(r, 1, lab).font = F_BASE
    for col, v, f in [(2, g0, "gwh"), (3, gb, "pct"), (5, gl, "pct"), (6, gh, "pct"), (7, cs, "pct")]:
        c = ws.cell(r, col, v); c.font = F_INPUT; c.fill = FILL_INPUT; c.number_format = FMT[f]; c.border = BOX
    seg_rows[k] = r
    r += 1
note(ws, r, "Fictional values. Commercial share = share of segment demand from customers able and willing to pay cost-reflective tariffs (assumption)."); r += 1
inp(ws, r, "exp_pot", "Export potential via regional power pool", 600, "GWh/yr", "Potential only", "gwh"); r += 1
inp(ws, r, "exp_con", "Contracted (signed) export sales", 0, "GWh/yr", "", "gwh"); r += 1
inp(ws, r, "sup0", "Existing firm domestic supply (2026)", 8600, "GWh/yr", "Incl. committed plants; fictional", "gwh", True); r += 1
inp(ws, r, "sup_g", "Growth of other supply available to the utility (committed + planned)", 0.045, "% p.a.", "Caps utility sales: demand above available supply is unserved", "pct"); r += 1
inp(ws, r, "thermal_disp", "Displaceable existing thermal generation", 500, "GWh/yr", "Diesel/HFO that new hydro can displace", "gwh"); r += 1
section(ws, r, "B. DEMAND PROJECTION (GWh)", ts=True); r += 1
for k, lab, *_ in segs:
    rr = seg_rows[k]
    ts(ws, r, f"d_{k}", lab, "GWh",
       f"=$B${rr}*(1+CHOOSE({{case}},$C${rr},$E${rr},$F${rr})+{{eff_demg}})^([year]-{{base_year}})*IF([year]>={{cod_year}},{{eff_dem}},1)", "gwh"); r += 1
ts(ws, r, "d_dom", "Total domestic demand (potential, at customer meter)", "GWh", "=" + "+".join(f"[d_{k}]" for k, *_ in segs), "gwh", bold=True); r += 1
ts(ws, r, "d_pot", "POTENTIAL demand incl. export potential", "GWh", "=[d_dom]+{exp_pot}", "gwh"); r += 1
ts(ws, r, "d_comm", "COMMERCIAL demand (ability-to-pay weighted)", "GWh",
   "=" + "+".join(f"[d_{k}]*{q('10_DEMAND')}!$G${seg_rows[k]}" for k, *_ in segs) + "+{exp_con}", "gwh"); r += 1
ts(ws, r, "d_req", "Required sent-out supply (grossed up for utility losses)", "GWh", "=[d_dom]/(1-{ut_tl}-{ut_cl})", "gwh"); r += 1
ts(ws, r, "d_sup", "Other committed supply", "GWh", "={sup0}*(1+{sup_g})^([year]-{base_year})", "gwh"); r += 1
ts(ws, r, "d_gap", "Supply gap before project", "GWh", "=MAX(0,[d_req]-[d_sup])", "gwh"); r += 1
ts(ws, r, "d_absorb", "Absorbable project energy (gap + thermal displacement + export contracts)", "GWh", "=[d_gap]+{thermal_disp}+{exp_con}", "gwh"); r += 1
ts(ws, r, "d_contract", "CONTRACTED demand (PPA contracted energy, P50)", "GWh", "=[opflag]*{p50}", "gwh"); r += 1
ts(ws, r, "d_bank", "BANKABLE demand = MIN(contracted, absorbable x commercial ratio)", "GWh", "=[opflag]*MIN([d_contract],[d_absorb]*[d_comm]/([d_dom]+{exp_con}))", "gwh", bold=True); r += 1
ts(ws, r, "d_bank_ratio", "Bankable / contracted", "x", "=IF([d_contract]>0,[d_bank]/[d_contract],\"\")", "x"); r += 1
ts(ws, r, "d_bank5", "  Ratio in first 5 operating years", "x", "=IF(AND([opyr]>=1,[opyr]<=5),[d_bank_ratio],\"\")", "x", total="=IF(COUNT([RNG:d_bank5])=0,99,MIN([RNG:d_bank5]))"); r += 1
REF["dem_ratio5"] = f"{q('10_DEMAND')}!$C${r-1}"

# ===================================================================================
# 09 GRID
# ===================================================================================
ws = WS["09_GRID"]
title(ws, "09 GRID — System size, absorption limit, project share of peak", "Simplified screening — not a substitute for load-flow / stability studies", ts=True)
r = 6
section(ws, r, "A. INPUTS", ts=True); r += 1
inp(ws, r, "peak0", "System peak demand (2026)", 1450, "MW", "Fictional", "m0", True); r += 1
inp(ws, r, "minload", "Minimum load as % of peak", 0.60, "%", "", "pct"); r += 1
inp(ws, r, "mustrun", "Must-run generation at minimum load", 300, "MW", "Existing baseload / run-of-river", "m0"); r += 1
inp(ws, r, "ic_mw", "Export interconnector capacity", 100, "MW", "", "m0"); r += 1
inp(ws, r, "exist_cap", "Existing installed capacity", 2100, "MW", "", "m0"); r += 1
section(ws, r, "B. CALCULATIONS", ts=True); r += 1
ts(ws, r, "peak", "System peak demand", "MW", "={peak0}*[d_dom]/[C:d_dom0]", "m0"); r += 1
ts(ws, r, "absorb_mw", "Grid absorption limit at minimum load", "MW", "=MAX(0,[peak]*{minload}-{mustrun})+{ic_mw}", "m0"); r += 1
ts(ws, r, "line_mw", "Line capacity available to project", "MW", "=IF([tx_ready]=1,{tx_mw},{tx_interim})", "m0"); r += 1
ts(ws, r, "evac_mw", "Effective evacuation capacity = MIN(line, absorption)", "MW", "=MIN([line_mw],[absorb_mw])", "m0", bold=True); r += 1
ts(ws, r, "evac_ratio", "Evacuation ratio (capped at 1)", "x", "=MIN(1,[evac_mw]/{inst_mw})", "n3"); r += 1
ts(ws, r, "share_peak", "Project share of system peak", "%", "=[opflag]*{inst_mw}/[peak]", "pct"); r += 1
ts(ws, r, "res_margin", "Reserve margin incl. project", "%", "=({exist_cap}+{inst_mw}*[opflag]-[peak])/[peak]", "pct"); r += 1
ts(ws, r, "evac_cod_row", "Evacuation capacity in first operating year", "MW", "=IF([opyr]=1,[evac_mw],0)", "m0", total="sum"); r += 1
REF["evac_cod"] = f"{q('09_GRID')}!$C${r-1}"
ts(ws, r, "share_cod_row", "Project share of peak in first operating year", "%", "=IF([opyr]=1,[share_peak],0)", "pct", total="sum"); r += 1
REF["share_cod"] = f"{q('09_GRID')}!$C${r-1}"
note(ws, r + 1, "Proportional curtailment simplification: delivered = generation x MIN(1, evacuation MW / installed MW). Conservative for peaking plants with storage; replace with dispatch simulation if available.")
# base-year domestic demand cell for peak scaling
ws10 = WS["10_DEMAND"]
TSROW["d_dom0"] = ("10_DEMAND", 99)
ws10["A99"] = "Base-year (2026) domestic demand"; ws10["A99"].font = F_BASE
put(ws10, "C99", "=" + "+".join(f"$B${seg_rows[k]}" for k, *_ in segs), "gwh")

# ===================================================================================
# 04 GENERATION
# ===================================================================================
ws = WS["04_GENERATION"]
title(ws, "04 GENERATION — Installed vs available vs expected vs evacuated vs delivered vs contracted",
      "Hydrology case, drought window and climate trend applied here", ts=True)
r = 6
calc(ws, r, "p_sel", "Selected generation case energy (P50/P75/P90)", "=CHOOSE({gen_case},{p50},{p75},{p90})", "GWh", "gwh"); r += 1
calc(ws, r, "p_len", "Lender sizing case energy", "=CHOOSE({lender_case},{p50},{p75},{p90},{p90_10})", "GWh", "gwh"); r += 1
section(ws, r, "A. CAPACITY", ts=True); r += 1
ts(ws, r, "inst_row", "Installed capacity", "MW", "=[opflag]*{inst_mw}", "mw"); r += 1
ts(ws, r, "availcap", "Available capacity (x availability)", "MW", "=[opflag]*{avail_mw}", "mw"); r += 1
section(ws, r, "B. HYDROLOGY FACTORS", ts=True); r += 1
ts(ws, r, "drought", "Drought factor", "x", "=IF(AND({st_drought}=1,[opyr]>={p_drought_start},[opyr]<{p_drought_start}+{p_drought_len}),{p_drought},1)", "n3"); r += 1
ts(ws, r, "climate", "Climate trend factor", "x", "=(1+{eff_climate})^(([year]-{base_year})/10)", "n3"); r += 1
ts(ws, r, "rampf", "Commissioning ramp factor", "x", "=IF([opyr]=1,{ramp},1)", "n3"); r += 1
section(ws, r, "C. ENERGY (GWh)", ts=True); r += 1
ts(ws, r, "gen_p50", "Expected generation, P50 (reference)", "GWh", "=[opflag]*{p50}*{eff_flow}*[climate]*[rampf]", "gwh", total="sum"); r += 1
ts(ws, r, "gen", "Generation — selected case", "GWh", "=[opflag]*{p_sel}*{eff_flow}*[drought]*[climate]*[rampf]", "gwh", total="sum", bold=True); r += 1
ts(ws, r, "evacuable", "Evacuable energy (x evacuation ratio)", "GWh", "=[gen]*[evac_ratio]", "gwh", total="sum"); r += 1
ts(ws, r, "curt_tx", "Curtailment — transmission / grid", "GWh", "=[gen]-[evacuable]", "gwh", total="sum"); r += 1
ts(ws, r, "delivered", "Delivered energy (absorbed by demand)", "GWh", "=MIN([evacuable],[d_absorb])", "gwh", total="sum", bold=True); r += 1
ts(ws, r, "curt_dem", "Curtailment — insufficient demand", "GWh", "=[evacuable]-[delivered]", "gwh", total="sum"); r += 1
ts(ws, r, "contracted", "Contracted energy (P50 reference)", "GWh", "=[gen_p50]", "gwh", total="sum"); r += 1
ts(ws, r, "gen_len", "Lender-case generation", "GWh", "=[opflag]*{p_len}*{eff_flow}*[climate]*[rampf]", "gwh", total="sum"); r += 1
ts(ws, r, "cf_row", "Capacity factor (selected case)", "%", "=IF([opflag]=1,[gen]/({inst_mw}*8.76),0)", "pct"); r += 1

# ===================================================================================
# 07 OPEX
# ===================================================================================
ws = WS["07_OPEX"]
title(ws, "07 OPEX — Plant operating costs and payments to government", "Real 2026 inputs escalated by US CPI", ts=True)
r = 6
section(ws, r, "A. INPUTS", ts=True); r += 1
inp(ws, r, "om_fix", "Fixed O&M (staff, maintenance contracts)", 3.2, "USDm/yr real", "About 1.6% of CAPEX; IFC range 1-4% [hydro_development_evidence]", "m", True); r += 1
inp(ws, r, "om_var", "Variable O&M", 1.0, "USD/MWh real", "", "n2"); r += 1
inp(ws, r, "ins", "Insurance", 0.0035, "% of CAPEX p.a.", "", "pct2"); r += 1
inp(ws, r, "mmr", "Major maintenance reserve contribution", 0.0025, "% of CAPEX p.a.", "", "pct2"); r += 1
inp(ws, r, "om_other", "Company G&A, E&S monitoring, community programmes", 0.8, "USDm/yr real", "", "m"); r += 1
inp(ws, r, "royalty", "Water-use royalty / resource fee to government", 2.5, "USD/MWh real", "Fiscal revenue", "n2", True); r += 1
section(ws, r, "B. CALCULATIONS (USDm nominal)", ts=True); r += 1
ts(ws, r, "o_fix", "Fixed O&M", "USDm", "=[opflag]*{om_fix}*{eff_opex}*[uscpi]", "m", total="sum"); r += 1
ts(ws, r, "o_var", "Variable O&M", "USDm", "=[gen]*{om_var}*{eff_opex}*[uscpi]/1000", "m", total="sum"); r += 1
ts(ws, r, "o_ins", "Insurance", "USDm", "=[opflag]*{capex_real}*{ins}*[uscpi]", "m", total="sum"); r += 1
ts(ws, r, "o_mmr", "Major maintenance reserve", "USDm", "=[opflag]*{capex_real}*{mmr}*[uscpi]", "m", total="sum"); r += 1
ts(ws, r, "o_oth", "G&A / E&S / community", "USDm", "=[opflag]*{om_other}*{eff_opex}*[uscpi]", "m", total="sum"); r += 1
ts(ws, r, "o_txprj", "Transmission O&M & wheeling (if project-owned)", "USDm", "=IF({tx_party}=2,[tx_omc],0)+[tx_wheelc]", "m", total="sum"); r += 1
ts(ws, r, "opex", "Total OPEX", "USDm", "=[o_fix]+[o_var]+[o_ins]+[o_mmr]+[o_oth]+[o_txprj]", "m", total="sum", bold=True); r += 1
ts(ws, r, "o_roy", "Water royalty (to government)", "USDm", "=[delivered]*{royalty}*[uscpi]/1000", "m", total="sum"); r += 1
ts(ws, r, "o_roy_len", "Water royalty — lender case", "USDm", "=[gen_len]*{royalty}*[uscpi]/1000", "m", total="sum"); r += 1

# ===================================================================================
# 11 OFFTAKER
# ===================================================================================
ws = WS["11_OFFTAKER"]
title(ws, "11 OFFTAKER — Offtake split, credit quality and payment security", "Qualitative inputs feed Gate 5")
r = 4
inp(ws, r, "off_name", "Main offtaker", "Navaria Electricity Company (NEC) — vertically integrated, state-owned", "", "Fictional"); r += 1
inp(ws, r, "off_rating", "Offtaker credit standing", "Unrated; sovereign rated B- (fictional)", "", ""); r += 1
inp(ws, r, "u_share", "Share of plant output sold to utility", 1.0, "%", "", "pct", True); r += 1
calc(ws, r, "m_share", "Share sold to mining offtaker (bilateral, USD, via wheeling)", "=1-{u_share}", "%", "pct"); r += 1
inp(ws, r, "lc_months", "Payment security: letter of credit / escrow cover", 3, "months of PPA billing", "Gate test; 6 months is the READY threshold (assumption)", "int", True); r += 1
inp(ws, r, "arrears_days", "Historical utility payment delays to existing IPPs", 120, "days", "Fictional", "int"); r += 1
calc(ws, r, "lc_amount", "LC amount required (first full operating year)", "={lc_months}/12*[C:rev_util_y2]", "USDm", "m"); r += 1

# ===================================================================================
# 12 UTILITY
# ===================================================================================
ws = WS["12_UTILITY"]
title(ws, "12 UTILITY — Simplified utility cash model and MAXIMUM SUSTAINABLE PPA PAYMENT",
      "The model does not assume the offtaker can pay; it tests it. USD equivalents of local-currency flows.", ts=True)
r = 6
section(ws, r, "A. INPUTS (2026)", ts=True); r += 1
inp(ws, r, "ut_cust", "Customers", 1350000, "#", "Fictional", "m0"); r += 1
inp(ws, r, "ut_custg", "Customer growth", 0.05, "% p.a.", "", "pct"); r += 1
inp(ws, r, "ut_tar0", "Average retail tariff", 2.7, "NVL/kWh", "Equals USD 0.135/kWh at 20 NVL/USD (fictional)", "n2", True); r += 1
inp(ws, r, "ut_pt", "Tariff adjustment: pass-through of local inflation", 1.0, "%", "1.0 = full indexation in base case; offtaker stress freezes tariff", "pct", True); r += 1
inp(ws, r, "ut_tl", "Technical losses", 0.14, "% of sent-out", "", "pct"); r += 1
inp(ws, r, "ut_cl", "Commercial (non-technical) losses", 0.08, "% of sent-out", "", "pct"); r += 1
inp(ws, r, "ut_coll", "Collection rate", 0.88, "% of billing", "", "pct", True); r += 1
inp(ws, r, "ut_supc", "Cost of other supply (own generation + other IPPs)", 55, "USD/MWh 2026", "", "n2"); r += 1
inp(ws, r, "ut_supusd", "USD-linked share of other supply cost", 0.5, "%", "", "pct"); r += 1
inp(ws, r, "ut_opex", "Utility OPEX (T&D, retail, overheads)", 190, "USDm 2026", "Local-currency; 50% fixed, 50% scales with sales volume", "m"); r += 1
inp(ws, r, "ut_sub", "Government operating transfers / subsidies", 80, "USDm 2026", "Local-currency", "m"); r += 1
inp(ws, r, "ut_ds", "Existing utility debt service", 85, "USDm/yr", "USD-denominated, flat", "m"); r += 1
inp(ws, r, "ut_rec0", "Opening receivables", 180, "USDm", "", "m"); r += 1
inp(ws, r, "ut_wo", "Annual write-off of aged receivables", 0.30, "% of stock", "", "pct"); r += 1
inp(ws, r, "ut_cov", "Required cash coverage of new PPA payments", 1.20, "x", "Prudential buffer — assumption", "x", True); r += 1
section(ws, r, "B. ENERGY BALANCE (GWh)", ts=True); r += 1
ts(ws, r, "u_dem", "Utility demand (domestic, excl. mining load served directly by the project)", "GWh", "=MAX(0,[d_dom]-[delivered]*{m_share})", "gwh"); r += 1
ts(ws, r, "u_req", "Sent-out energy required to meet utility demand", "GWh", "=[u_dem]/(1-{ut_tl}-{ut_cl})", "gwh"); r += 1
ts(ws, r, "u_proj", "  from the project (utility share, net of transmission losses)", "GWh", "=MIN([delivered]*{u_share}*(1-{tx_loss}),[u_req])", "gwh"); r += 1
ts(ws, r, "u_other", "  from other supply (capped at available supply)", "GWh", "=MIN([u_req]-[u_proj],[d_sup])", "gwh"); r += 1
ts(ws, r, "u_purch", "Energy purchased / sent-out", "GWh", "=[u_proj]+[u_other]", "gwh"); r += 1
ts(ws, r, "u_sales", "Electricity sales (demand served)", "GWh", "=[u_purch]*(1-{ut_tl}-{ut_cl})", "gwh"); r += 1
ts(ws, r, "u_unserved", "Unserved demand (load shedding)", "GWh", "=[u_dem]-[u_sales]", "gwh", total="sum"); r += 1
section(ws, r, "C. INCOME & CASH (USDm equivalent)", ts=True); r += 1
ts(ws, r, "u_tar", "Average retail tariff", "NVL/kWh", "=IF(#T#=1,{ut_tar0},[u_tar@p])*(1+{lc_cpi}*IF(AND([opyr]>=1,[opyr]<={eff_freeze}),0,{ut_pt}))", "n2"); r += 1
ts(ws, r, "u_tar_usd", "Average retail tariff (USD/MWh)", "USD/MWh", "=[u_tar]/[fx]*1000", "n2"); r += 1
ts(ws, r, "u_bill", "Billed revenue", "USDm", "=[u_sales]*[u_tar]/[fx]", "m"); r += 1
ts(ws, r, "u_collr", "Collection rate", "%", "=MAX(0,MIN(1,{ut_coll}+IF([year]>={cod_year},{eff_coll_adj},0)))", "pct"); r += 1
ts(ws, r, "u_coll", "Cash collected", "USDm", "=[u_bill]*[u_collr]", "m"); r += 1
ts(ws, r, "u_subs", "Government transfers", "USDm", "={ut_sub}*IF([year]>={cod_year},{eff_sub},1)*[lccpi]/[fxidx]", "m"); r += 1
ts(ws, r, "u_opex", "Utility OPEX", "USDm", "=-{ut_opex}*[lccpi]/[fxidx]*(0.5+0.5*[u_sales]/[C:d_dom0])", "m"); r += 1
ts(ws, r, "u_supcost", "Cost of other supply", "USDm", "=-[u_other]*{ut_supc}*({ut_supusd}*[uscpi]+(1-{ut_supusd})*[lccpi]/[fxidx])/1000", "m"); r += 1
ts(ws, r, "u_exds", "Existing debt service", "USDm", "=-{ut_ds}", "m"); r += 1
ts(ws, r, "u_cash_pre", "Cash available after displaced supply, before paying the new PPA", "USDm", "=[u_coll]+[u_subs]+[u_opex]+[u_supcost]+[u_exds]", "m", bold=True); r += 1
ts(ws, r, "u_maxppa", "MAXIMUM SUSTAINABLE PPA PAYMENT", "USDm", "=MAX(0,[u_cash_pre])/{ut_cov}", "m", bold=True); r += 1
ts(ws, r, "u_ppa", "PPA payment billed by project (utility share)", "USDm", "=[rev_util]", "m"); r += 1
ts(ws, r, "u_gap", "OFFTAKER PAYMENT CAPACITY GAP", "USDm", "=[opflag]*MAX(0,[u_ppa]-[u_maxppa])", "m", total="sum", bold=True); r += 1
ts(ws, r, "u_ratio", "Payment capacity / PPA payment", "x", "=IF([u_ppa]>0,[u_maxppa]/[u_ppa],99)", "x"); r += 1
ts(ws, r, "u_ratio10", "  Ratio in first 10 operating years", "x", "=IF(AND([opyr]>=1,[opyr]<=10),[u_ratio],\"\")", "x", total="=IF(COUNT([RNG:u_ratio10])=0,99,MIN([RNG:u_ratio10]))"); r += 1
REF["ut_ratio10"] = f"{q('12_UTILITY')}!$C${r-1}"
ts(ws, r, "u_prefdef", "Pre-existing utility cash deficit (before any new PPA)", "USDm", "=MAX(0,-[u_cash_pre])", "m", total="sum"); r += 1
section(ws, r, "D. PERFORMANCE METRICS", ts=True); r += 1
ts(ws, r, "u_ebitda", "Utility EBITDA (excl. transfers)", "USDm", "=[u_bill]+[u_opex]+[u_supcost]-[u_ppa]", "m"); r += 1
ts(ws, r, "u_ebitda_s", "Utility EBITDA incl. government transfers", "USDm", "=[u_ebitda]+[u_subs]", "m"); r += 1
ts(ws, r, "u_margin", "Operating margin (EBITDA / billed)", "%", "=IF([u_bill]>0,[u_ebitda]/[u_bill],0)", "pct"); r += 1
ts(ws, r, "u_paid", "PPA paid from utility own cash", "USDm", "=[u_ppa]-[u_gap]", "m"); r += 1
ts(ws, r, "u_cash_post", "Utility cash flow after PPA paid", "USDm", "=[u_cash_pre]-[u_paid]", "m"); r += 1
ts(ws, r, "u_dscr", "Utility DSCR on existing debt", "x", "=([u_cash_pre]-[u_exds]-[u_paid])/-[u_exds]", "x"); r += 1
ts(ws, r, "u_rec", "Receivables (closing)", "USDm", "=IF(#T#=1,{ut_rec0},[u_rec@p])*(1-{ut_wo})+[u_bill]-[u_coll]", "m"); r += 1
ts(ws, r, "u_recd", "Receivable days", "days", "=IF([u_bill]>0,[u_rec]/[u_bill]*365,0)", "int"); r += 1
ts(ws, r, "u_arrears", "Cumulative unpaid PPA arrears to project", "USDm", "=[u_arrears@p]+[unpaid]", "m"); r += 1
ts(ws, r, "u_other_np", "No-project case: purchases from other supply", "GWh", "=MIN([u_req]+[delivered]*{m_share}/(1-{ut_tl}-{ut_cl})*[opflag],[d_sup])", "gwh"); r += 1
ts(ws, r, "u_sales_np", "No-project case: sales", "GWh", "=[u_other_np]*(1-{ut_tl}-{ut_cl})", "gwh"); r += 1
ts(ws, r, "u_cash_np", "No-project case: utility cash flow", "USDm", "=[u_sales_np]*[u_tar]/[fx]*[u_collr]+[u_subs]-{ut_opex}*[lccpi]/[fxidx]*(0.5+0.5*[u_sales_np]/[C:d_dom0])-[u_other_np]*{ut_supc}*({ut_supusd}*[uscpi]+(1-{ut_supusd})*[lccpi]/[fxidx])/1000+[u_exds]", "m"); r += 1
ts(ws, r, "f_soe", "Incremental utility (SOE) cash from the project, net of new arrears", "USDm", "=[u_cash_post]-[u_cash_np]-[unpaid]", "m", total="sum", bold=True); r += 1
ts(ws, r, "u_ppa_share", "PPA payment as % of utility billed revenue", "%", "=IF([u_bill]>0,[u_ppa]/[u_bill],0)", "pct"); r += 1
ts(ws, r, "u_cos", "Collected revenue per MWh sent-out", "USD/MWh", "=([u_coll])/[u_purch]*1000", "n2"); r += 1

# ===================================================================================
# 13 REGULATION
# ===================================================================================
ws = WS["13_REGULATION"]
title(ws, "13 REGULATION — Regulatory Bankability Matrix (readiness screening, NOT legal advice)",
      "Status options: READY / PARTIAL / GAP / CRITICAL GAP. Fictional statuses for Navaria.")
for c, h in zip("ABCD", ["Item", "Status", "Score (3-0)", "Evidence required / comment"]):
    ws[f"{c}4"] = h; ws[f"{c}4"].font = F_HDR; ws[f"{c}4"].fill = FILL_HDR
REG = [("Electricity law (IPP participation permitted)", "READY", "Act in force; IPP chapter"),
       ("Generation licence", "PARTIAL", "Provisional licence; final on financial close"),
       ("Water rights / water-use permit", "PARTIAL", "Permit volume vs e-flow to be reconciled"),
       ("Concession agreement / implementation agreement", "PARTIAL", "Term sheet agreed"),
       ("PPP legislation & PPP unit approvals", "READY", ""),
       ("IPP procurement framework", "PARTIAL", "Unsolicited proposal rules unclear"),
       ("PPA enforceability (arbitration, waiver of immunity)", "PARTIAL", "Offshore arbitration accepted in principle"),
       ("Tariff regulation (cost-reflective, pass-through)", "GAP", "No automatic pass-through of PPA costs"),
       ("Regulator independence", "PARTIAL", ""),
       ("Grid access / connection rules", "PARTIAL", ""),
       ("Grid code", "GAP", "Outdated; no ancillary-service rules"),
       ("Environmental & social permits (ESIA approval)", "PARTIAL", "ESIA approved; RAP pending"),
       ("Land rights / acquisition", "GAP", "Reservoir land acquisition incomplete"),
       ("FX convertibility", "GAP", "Central bank allocation queues"),
       ("Tax regime (stability, incentives)", "READY", "Stabilisation clause available"),
       ("Repatriation of dividends & debt service", "PARTIAL", "")]
r = 5
REG_FIRST = r
for lab, st, cm in REG:
    ws.cell(r, 1, lab).font = F_BASE
    c = ws.cell(r, 2, st); c.font = F_INPUT; c.fill = FILL_INPUT; c.border = BOX
    put(ws, f"C{r}", f'=IF(B{r}="READY",3,IF(B{r}="PARTIAL",2,IF(B{r}="GAP",1,IF(B{r}="CRITICAL GAP",0,""))))', "int")
    ws.cell(r, 4, cm).font = F_BASE
    r += 1
REG_LAST = r - 1
dv_list(ws, f"B{REG_FIRST}:B{REG_LAST}", ["READY", "PARTIAL", "GAP", "CRITICAL GAP"])
ws.conditional_formatting.add(f"B{REG_FIRST}:B{REG_LAST}", CellIsRule(operator="equal", formula=['"READY"'], fill=PatternFill("solid", fgColor="C6EFCE")))
ws.conditional_formatting.add(f"B{REG_FIRST}:B{REG_LAST}", CellIsRule(operator="equal", formula=['"PARTIAL"'], fill=PatternFill("solid", fgColor="FFEB9C")))
ws.conditional_formatting.add(f"B{REG_FIRST}:B{REG_LAST}", CellIsRule(operator="equal", formula=['"GAP"'], fill=PatternFill("solid", fgColor="F8CBAD")))
ws.conditional_formatting.add(f"B{REG_FIRST}:B{REG_LAST}", CellIsRule(operator="equal", formula=['"CRITICAL GAP"'], fill=PatternFill("solid", fgColor="FF7C80")))
r += 1
calc(ws, r, "reg_crit", "Count: CRITICAL GAP", f'=COUNTIF(B{REG_FIRST}:B{REG_LAST},"CRITICAL GAP")', "#", "int", out=True); r += 1
calc(ws, r, "reg_gap", "Count: GAP", f'=COUNTIF(B{REG_FIRST}:B{REG_LAST},"GAP")', "#", "int", out=True); r += 1
calc(ws, r, "reg_part", "Count: PARTIAL", f'=COUNTIF(B{REG_FIRST}:B{REG_LAST},"PARTIAL")', "#", "int"); r += 1
calc(ws, r, "reg_ready", "Count: READY", f'=COUNTIF(B{REG_FIRST}:B{REG_LAST},"READY")', "#", "int"); r += 1
calc(ws, r, None, "Average readiness score (0-3)", f"=AVERAGE(C{REG_FIRST}:C{REG_LAST})", "", "n2"); r += 1
r += 1
section(ws, r, "E&S / SUSTAINABILITY READINESS (feeds Gate 9)"); r += 1
inp(ws, r, "es_level", "ESIA & lender E&S standards compliance (1=gaps, 2=in progress, 3=compliant & disclosed)", 2, "1-3", "e.g. IFC Performance Standards / Hydropower Sustainability Standard", "int", True); r += 1
inp(ws, r, "rap_level", "Resettlement Action Plan status (1=not started, 2=approved, 3=implemented & monitored)", 2, "1-3", "", "int", True); r += 1
inp(ws, r, "tb_level", "Transboundary water / riparian notification (1=unresolved, 2=in progress, 3=resolved or n/a)", 3, "1-3", "", "int", True); r += 1

# ===================================================================================
# 14 PPA
# ===================================================================================
ws = WS["14_PPA"]
title(ws, "14 PPA — Two-part tariff, indexation, deemed energy, take-or-pay, termination", "Commercial terms are fictional; structure reflects common African hydro IPP practice")
r = 4
section(ws, r, "A. TARIFF"); r += 1
inp(ws, r, "cap_chg", "Capacity / availability charge", 0.0, "USD/kW-month (2026)", "Energy-only tariff, as in East African feed-in tariffs", "n2", True); r += 1
inp(ws, r, "en_chg", "Energy charge", 112.0, "USD/MWh (2026)", "Negotiated (no REFiT above 20 MW). Uganda REFiT 5.0: 75-79 USD/MWh for <=20 MW; Nyamagasani 85 [hydro_development_evidence]", "n2", True); r += 1
inp(ws, r, "cap_idx", "Share of capacity charge indexed to US CPI", 0.5, "%", "Debt-service portion usually not indexed", "pct"); r += 1
inp(ws, r, "en_idx", "Share of energy charge indexed to US CPI", 0.5, "%", "Assumption", "pct"); r += 1
inp(ws, r, "lc_share", "Share of tariff denominated in local currency (NVL)", 0.0, "%", "0% = full USD (FX risk on utility/government)", "pct", True); r += 1
section(ws, r, "B. VOLUME & RISK TERMS"); r += 1
inp(ws, r, "deemed", "Deemed energy payable for buyer/grid curtailment (1=yes)", 1, "0/1", "Transfers transmission & demand risk to offtaker", "int", True); r += 1
inp(ws, r, "top", "Take-or-pay floor (share of contracted P50 energy)", 0.0, "%", "Alternative to deemed energy", "pct"); r += 1
inp(ws, r, "avail_ratio", "Declared availability / contractual availability", 1.0, "x", "<1 reduces capacity payment", "n2"); r += 1
inp(ws, r, "term_prem", "Termination: equity compensation premium on unrecovered equity", 0.15, "%", "Government-default / political FM termination", "pct"); r += 1
section(ws, r, "C. CONTRACT RISK MAP (qualitative)"); r += 1
for lab, v in [("Change in law", "Compensated by offtaker; tariff adjustment"),
               ("Natural force majeure", "Capacity payments suspended after 180 days (fictional)"),
               ("Political force majeure", "Capacity payments continue; buy-out right"),
               ("Hydrology risk", "Borne by project (energy charge only)"),
               ("FX convertibility & transfer", "Government undertaking in implementation agreement")]:
    ws.cell(r, 1, lab).font = F_BASE; c = ws.cell(r, 3, v); c.font = F_INPUT; r += 1

# ===================================================================================
# 15 TARIFF
# ===================================================================================
ws = WS["15_TARIFF"]
title(ws, "15 TARIFF — Escalated tariff components, blended tariff, affordability", "", ts=True)
r = 6
ts(ws, r, "fxfac", "Currency factor on tariff (local-currency portion)", "x", "=(1-{lc_share})+{lc_share}*[lccpi]/[fxidx]/[uscpi]", "n3"); r += 1
ts(ws, r, "capc", "Capacity charge (nominal)", "USD/kW-mo", "={cap_chg}*((1-{cap_idx})+{cap_idx}*[uscpi])*[fxfac]*{eff_tariff}", "n2"); r += 1
ts(ws, r, "enc", "Energy charge (nominal)", "USD/MWh", "={en_chg}*((1-{en_idx})+{en_idx}*[uscpi])*[fxfac]*{eff_tariff}", "n2"); r += 1
ts(ws, r, "blend", "Blended PPA tariff (billed revenue / energy paid)", "USD/MWh", "=IF([epaid]>0,[rev_bill]/[epaid]*1000,0)", "n2", bold=True); r += 1
ts(ws, r, "lcoe_row", "Project LCOE (constant, nominal levelised)", "USD/MWh", "=[opflag]*{lcoe}", "n2"); r += 1
ts(ws, r, "retail_usd", "Utility average retail tariff", "USD/MWh", "=[u_tar_usd]", "n2"); r += 1
ts(ws, r, "coll_mwh", "Utility collected revenue per MWh sent-out", "USD/MWh", "=[u_cos]", "n2"); r += 1
ts(ws, r, "afford", "Affordability headroom: collected/MWh – blended PPA tariff", "USD/MWh", "=[opflag]*([coll_mwh]-[blend])", "n2"); r += 1

# ===================================================================================
# 16 REVENUE
# ===================================================================================
ws = WS["16_REVENUE"]
title(ws, "16 REVENUE — Billed vs cash revenue; offtaker exposure; unpaid amounts", "", ts=True)
r = 6
section(ws, r, "A. ENERGY PAID (GWh)", ts=True); r += 1
ts(ws, r, "deemed", "Deemed energy (curtailment not caused by seller)", "GWh", "={deemed}*([curt_tx]+[curt_dem])", "gwh", total="sum"); r += 1
ts(ws, r, "topshort", "Take-or-pay shortfall energy", "GWh", "=MAX(0,{top}*[contracted]-[delivered]-[deemed])", "gwh", total="sum"); r += 1
ts(ws, r, "epaid", "Energy paid", "GWh", "=[delivered]+[deemed]+[topshort]", "gwh", total="sum"); r += 1
section(ws, r, "B. BILLED REVENUE (USDm)", ts=True); r += 1
ts(ws, r, "rev_cap", "Capacity payments", "USDm", "=[opflag]*[capc]*{inst_mw}*12/1000*{avail_ratio}*[rampf]", "m", total="sum"); r += 1
ts(ws, r, "rev_en", "Energy payments (delivered)", "USDm", "=[enc]*[delivered]/1000", "m", total="sum"); r += 1
ts(ws, r, "rev_deem", "Deemed energy & take-or-pay payments", "USDm", "=[enc]*([deemed]+[topshort])/1000", "m", total="sum"); r += 1
ts(ws, r, "rev_bill", "Total billed revenue", "USDm", "=[rev_cap]+[rev_en]+[rev_deem]", "m", total="sum", bold=True); r += 1
ts(ws, r, "rev_util", "  billed to utility", "USDm", "=[rev_bill]*{u_share}", "m", total="sum"); r += 1
ts(ws, r, "rev_util_y2", "  billed to utility — first full year (op yr 2)", "USDm", "=IF([opyr]=2,[rev_util],0)", "m", total="sum"); r += 1
ts(ws, r, "rev_min", "  billed to mining offtaker", "USDm", "=[rev_bill]-[rev_util]", "m", total="sum"); r += 1
section(ws, r, "C. PAYMENT OF UTILITY SHORTFALL", ts=True); r += 1
ts(ws, r, "cov_backstop", "Covered by government budget backstop", "USDm", "=IF({backstop}=1,[u_gap]*{bs_share},0)", "m", total="sum"); r += 1
ts(ws, r, "ppag_lim", "PPA guarantee limit (months of utility billing)", "USDm", "={str_ppag}*{ppag_months}/12*[rev_util]", "m"); r += 1
ts(ws, r, "ppag_reimb", "Utility reimbursement of earlier guarantee calls", "USDm", "=[opflag]*MIN([ppag_out@p],MAX(0,[u_maxppa]-[u_ppa]))", "m", total="sum"); r += 1
ts(ws, r, "cov_guar", "Covered by sovereign PPA payment guarantee call (within available limit)", "USDm", "=MIN([u_gap]-[cov_backstop],MAX(0,[ppag_lim]-[ppag_out@p]+[ppag_reimb]))", "m", total="sum"); r += 1
ts(ws, r, "ppag_out", "Guarantee calls outstanding (not yet reimbursed)", "USDm", "=[ppag_out@p]+[cov_guar]-[ppag_reimb]", "m"); r += 1
ts(ws, r, "unpaid", "UNPAID (arrears to project)", "USDm", "=[u_gap]-[cov_backstop]-[cov_guar]", "m", total="sum", bold=True); r += 1
ts(ws, r, "rev_cash", "Cash revenue received by project", "USDm", "=[rev_bill]-[unpaid]", "m", total="sum", bold=True); r += 1
section(ws, r, "D. LENDER CASE REVENUE (for debt sizing)", ts=True); r += 1
ts(ws, r, "rev_len", "Lender-case revenue", "USDm",
   "=[rev_cap]+[enc]*IF({deemed}=1,[gen_len],MIN([gen_len]*[evac_ratio],[d_absorb]))/1000", "m", total="sum"); r += 1
section(ws, r, "E. REVENUE QUALITY METRICS", ts=True); r += 1
calc(ws, r, "rev_fixed", "Revenue certainty: fixed (capacity) share of billed revenue", "=IFERROR([C:rev_cap]/[C:rev_bill],0)", "%", "pct", out=True); r += 1
calc(ws, r, "rev_vol", "Revenue volatility: P90 vs P50 energy revenue at risk (yr 2)", "=IFERROR((1-{p90}/{p50})*SUMPRODUCT(([RNG:opyr]=2)*[RNG:rev_en])/SUMPRODUCT(([RNG:opyr]=2)*[RNG:rev_bill]),0)", "% of revenue", "pct", out=True); r += 1
calc(ws, r, "rev_offexp", "Offtaker exposure: utility share of lifetime billed revenue", "=IFERROR([C:rev_util]/[C:rev_bill],0)", "%", "pct", out=True); r += 1
calc(ws, r, "rev_govreq", "Government support requirement to sustain PPA payments (lifetime, nominal)", "=[C:u_gap]", "USDm", "m", out=True); r += 1

# ===================================================================================
# 17A STRUCTURES
# ===================================================================================
ws = WS["17A_STRUCTURES"]
title(ws, "17A STRUCTURES — Public / IPP / PPP / Hybrid / Blended for the SAME project",
      "Column C = structure selected on 01_CONTROL_PANEL; library columns E:I are inputs")
ws.column_dimensions["D"].width = 4
for j in range(5):
    ws.column_dimensions[L(5 + j)].width = 15
hdrs = ["1 Public", "2 IPP", "3 PPP", "4 Hybrid", "5 Blended"]
ws["A4"] = "Parameter"; ws["B4"] = "Unit"; ws["C4"] = "SELECTED"
for cc in range(1, 10):
    ws.cell(4, cc).fill = FILL_HDR; ws.cell(4, cc).font = F_HDR
for j, h in enumerate(hdrs):
    ws.cell(4, 5 + j, h)
STR = [
    ("str_name", "Structure", "", ["Public (SOE, sovereign-borrowed)", "IPP (private BOOT)", "PPP (SOE + private, DFI-backed)", "Hybrid (public civil works, private E&M/O&M)", "Blended finance (grants + concessional + private)"], None),
    ("str_goveq", "Government equity", "% of funding base", [0.15, 0.0, 0.10, 0.0, 0.05], "pct"),
    ("str_grant", "Grants / VGF / public capital contribution", "% of funding base", [0.0, 0.0, 0.05, 0.35, 0.08], "pct"),
    ("str_conc", "Concessional debt", "% of funding base", [0.55, 0.0, 0.30, 0.25, 0.35], "pct"),
    ("str_maxdebt", "Maximum total senior debt (gearing cap)", "% of funding base", [0.85, 0.70, 0.75, 0.55, 0.72], "pct"),
    ("str_privmax", "Maximum private equity available", "% of funding base", [0.0, 0.35, 0.20, 0.25, 0.25], "pct"),
    ("str_resid", "Residual equity provider (1=private, 2=government)", "1-2", [2, 1, 1, 1, 1], "int"),
    ("str_guar", "Share of senior debt guaranteed / counter-indemnified by sovereign", "%", [1.0, 0.0, 0.40, 0.20, 0.15], "pct"),
    ("str_onbud", "Share of senior debt recorded as public debt", "%", [1.0, 0.0, 0.0, 0.0, 0.0], "pct"),
    ("str_ppag", "Sovereign PPA payment guarantee (1=yes)", "0/1", [0, 1, 1, 1, 1], "int"),
    ("str_term", "Concession termination payment obligation (1=yes)", "0/1", [0, 1, 1, 1, 1], "int"),
    ("str_fxg", "Government FX convertibility guarantee on remittances", "% covered", [0.0, 1.0, 1.0, 1.0, 0.5], "pct"),
    ("str_rc", "Concessional interest rate", "%", [0.02, 0.03, 0.03, 0.03, 0.025], "pct2"),
    ("str_gc", "Concessional grace after COD", "years", [5, 5, 5, 5, 5], "int"),
    ("str_nc", "Concessional repayment period", "years", [20, 20, 20, 20, 20], "int"),
    ("str_rm", "Commercial / DFI senior debt rate (all-in, fixed/swapped)", "%", [0.075, 0.08, 0.075, 0.075, 0.072], "pct2"),
    ("str_nm", "Commercial debt repayment tenor after COD", "years", [15, 16, 16, 16, 18], "int"),
    ("str_dscr", "Target sizing DSCR", "x", [1.20, 1.35, 1.30, 1.30, 1.30], "x"),
    ("str_hurdle", "Private equity target IRR (nominal USD)", "%", [0.10, 0.15, 0.14, 0.14, 0.13], "pct"),
]
r = 5
for nm, lab, u, vals, f in STR:
    ws.cell(r, 1, lab).font = F_BASE; ws.cell(r, 2, u).font = F_BASE
    for j, v in enumerate(vals):
        c = ws.cell(r, 5 + j, v); c.font = F_INPUT; c.fill = FILL_INPUT; c.border = BOX
        if f:
            c.number_format = FMT[f]
    put(ws, f"C{r}", f"=INDEX(E{r}:I{r},{{structure}})", f)
    ws.cell(r, 3).fill = FILL_OUT
    REF[nm] = f"{q(ws.title)}!$C${r}"
    r += 1
STR_LAST = r - 1
calc(ws, r, None, "Check: grants + gov equity + max debt + max private equity ≥ 100%", "=IF({str_grant}+{str_goveq}+{str_maxdebt}+IF({str_resid}=2,1,{str_privmax})>=1,\"OK\",\"Structurally under-funded\")", "", None); r += 1
inp(ws, r, "lockup", "Distribution lock-up DSCR", 1.10, "x", "", "x"); r += 1
inp(ws, r, "upfront_fee", "Upfront & commitment fees", 0.02, "% of senior debt", "", "pct"); r += 1
inp(ws, r, "dsra_m", "DSRA requirement", 6, "months of next-year DS", "", "int"); r += 1
r += 1
section(ws, r, "LIVE CLOSED-FORM STRUCTURE COMPARISON (screening; pre-tax, level real annuity, P50)"); r += 1
CMP0 = r
for cc in range(1, 10):
    ws.cell(r, cc).fill = FILL_HDR; ws.cell(r, cc).font = F_HDR
ws.cell(r, 1, "Metric"); ws.cell(r, 2, "Unit")
for j, h in enumerate(hdrs):
    ws.cell(r, 5 + j, h)
r += 1
note(ws, r, "WACC_s = Σ weights x costs (grants cost 0 to project; government equity at government discount rate). Required tariff = (funding base x (1-grant%) x CRF(WACC, term) + year-2 OPEX) / P50. Not a substitute for full-engine runs (snapshot below)."); r += 1
cmp_rows = {}
def cmp_row(key, lab, unit, fn, f):
    global r
    ws.cell(r, 1, lab).font = F_BASE; ws.cell(r, 2, unit).font = F_BASE
    for j in range(5):
        col = L(5 + j)
        put(ws, f"{col}{r}", fn(col), f)
    cmp_rows[key] = r
    r += 1
srow = {nm: 5 + i for i, (nm, *_rest) in enumerate(STR)}
cmp_row("comm", "Commercial debt share (assumed at gearing cap)", "%", lambda c: f"=MAX(0,{c}{srow['str_maxdebt']}-{c}{srow['str_conc']})", "pct")
cmp_row("priv", "Private equity share", "%", lambda c: f"=IF({c}{srow['str_resid']}=2,0,MAX(0,1-{c}{srow['str_goveq']}-{c}{srow['str_grant']}-{c}{srow['str_maxdebt']}))", "pct")
cmp_row("govx", "Government residual equity share", "%", lambda c: f"=IF({c}{srow['str_resid']}=2,MAX(0,1-{c}{srow['str_grant']}-{c}{srow['str_maxdebt']}-{c}{srow['str_goveq']}),0)", "pct")
cmp_row("wacc", "Blended pre-tax cost of capital (private equity grossed up for tax)", "%",
        lambda c: f"=({c}{srow['str_goveq']}+{c}{cmp_rows['govx']})*{{gov_disc}}+{c}{srow['str_conc']}*{c}{srow['str_rc']}+{c}{cmp_rows['comm']}*{c}{srow['str_rm']}+{c}{cmp_rows['priv']}*{c}{srow['str_hurdle']}/(1-{{tax_rate}})", "pct2")
cmp_row("wacc_ex", "Cost of capital on non-grant funding", "%", lambda c: f"=IFERROR({c}{cmp_rows['wacc']}/(1-{c}{srow['str_grant']}),0)", "pct2")
cmp_row("crf", "Capital recovery factor", "x", lambda c: f"={c}{cmp_rows['wacc_ex']}/(1-(1+{c}{cmp_rows['wacc_ex']})^-{{ops_years}})", "n3")
cmp_row("tariff", "Required levelised tariff (screening; capital incl. IDC and fees)", "USD/MWh", lambda c: f"=({{fund_base}}*(1+{c}{srow['str_maxdebt']}*({{idc_km}}+{{upfront_fee}}))*(1-{c}{srow['str_grant']})*{c}{cmp_rows['crf']}+{{opex_y2}})/{{p50}}*1000", "n2")
cmp_row("afford", "Utility payment headroom per MWh (max sustainable payment / energy, first 10 yrs avg)", "USD/MWh", lambda c: "={afford_tariff}", "n2")
cmp_row("subsidy", "Implied annual subsidy to close affordability gap", "USDm/yr", lambda c: f"=MAX(0,{c}{cmp_rows['tariff']}-{c}{cmp_rows['afford']})*{{p50}}/1000", "m")
cmp_row("pubcap", "Upfront public capital (gov equity + grants)", "USDm", lambda c: f"=({c}{srow['str_goveq']}+{c}{srow['str_grant']}+{c}{cmp_rows['govx']})*{{fund_base}}", "m")
cmp_row("privcap", "Private equity", "USDm", lambda c: f"={c}{cmp_rows['priv']}*{{fund_base}}", "m")
cmp_row("debt", "Senior debt", "USDm", lambda c: f"={c}{srow['str_maxdebt']}*{{fund_base}}", "m")
cmp_row("ds1", "Indicative annual debt service (blended annuity)", "USDm/yr",
        lambda c: f"={{fund_base}}*({c}{srow['str_conc']}*{c}{srow['str_rc']}/(1-(1+{c}{srow['str_rc']})^-{c}{srow['str_nc']})+{c}{cmp_rows['comm']}*{c}{srow['str_rm']}/(1-(1+{c}{srow['str_rm']})^-{c}{srow['str_nm']}))", "m")
cmp_row("onbud", "Direct public debt", "USDm", lambda c: f"={c}{srow['str_onbud']}*{c}{cmp_rows['debt']}", "m")
cmp_row("guar", "Guaranteed debt (contingent)", "USDm", lambda c: f"=(1-{c}{srow['str_onbud']})*{c}{srow['str_guar']}*{c}{cmp_rows['debt']}", "m")
cmp_row("ppag", "PPA guarantee exposure (12 months of payments)", "USDm", lambda c: f"={c}{srow['str_ppag']}*{c}{cmp_rows['tariff']}*{{p50}}/1000", "m")
cmp_row("term", "Termination exposure at COD (debt + private equity x (1+premium))", "USDm", lambda c: f"={c}{srow['str_term']}*({c}{cmp_rows['debt']}+{c}{cmp_rows['privcap']}*(1+{{term_prem}}))", "m")
cmp_row("pubexp", "Gross public exposure at COD. Near the funding base by construction: every dollar is public or termination-protected", "USDm",
        lambda c: f"={c}{cmp_rows['pubcap']}+{c}{cmp_rows['onbud']}+MAX({c}{cmp_rows['guar']}+{c}{cmp_rows['ppag']},{c}{cmp_rows['term']})", "m")
cmp_row("pubexp_pct", "Gross public exposure / GDP", "%", lambda c: f"={c}{cmp_rows['pubexp']}/({{gdp0}}*1000)", "pct")
CMP_SNAP = r + 2
REF["cmp_tariff_sel"] = f"INDEX({q(ws.title)}!$E${cmp_rows['tariff']}:$I${cmp_rows['tariff']},{REF['structure']})"

# ===================================================================================
# 17 PROJECT FINANCE (sources & uses, KPIs)
# ===================================================================================
ws = WS["17_PROJECT_FINANCE"]
title(ws, "17 PROJECT FINANCE — Funding base, sources & uses, debt capacity, financing gap, KPIs", "Structure parameters from 17A_STRUCTURES")
r = 4
section(ws, r, "A. FUNDING BASE & USES (nominal USDm)"); r += 1
calc(ws, r, "u_capex", "Plant CAPEX (nominal)", "=[C:capex_nom]", "USDm", "m"); r += 1
calc(ws, r, "u_tx", "Transmission CAPEX funded by project", "=SUMPRODUCT([RNG:tx_spend_prj],[RNG:consflag])", "USDm", "m", "Project-built transmission spend falling in the construction period"); r += 1
calc(ws, r, "u_devprem", "Development premium paid to the developer at financial close", "={dev_prem}", "USDm", "m"); r += 1
calc(ws, r, "fund_base", "FUNDING BASE (CAPEX + development premium)", "={u_capex}+{u_tx}+{u_devprem}", "USDm", "m", out=True); r += 1
calc(ws, r, "u_idc", "Interest during construction (equity-funded)", "=[C:idc]", "USDm", "m"); r += 1
calc(ws, r, "u_fee", "Upfront financing fees", "={upfront_fee}*({debt_c}+{debt_m})", "USDm", "m"); r += 1
calc(ws, r, "u_dsra", "Initial DSRA funding", "=[C:dsra_init]", "USDm", "m"); r += 1
calc(ws, r, "uses", "TOTAL USES", "={fund_base}+{u_idc}+{u_fee}+{u_dsra}", "USDm", "m", out=True); r += 1
section(ws, r, "B. SOURCES"); r += 1
calc(ws, r, "s_grant", "Grants / VGF / public capital contribution", "=IF({debt_mode}=1,{str_grant}*{fund_base},{lock_grant})", "USDm", "m"); r += 1
calc(ws, r, "s_goveq", "Government equity (structural)", "=IF({debt_mode}=1,{str_goveq}*{fund_base},{lock_goveq})", "USDm", "m"); r += 1
calc(ws, r, "debt_c", "Concessional senior debt", "=IF({debt_mode}=1,MIN({str_conc},{str_maxdebt})*{fund_base},{lock_c})", "USDm", "m"); r += 1
calc(ws, r, "debt_m", "Commercial senior debt (gearing cap applied to CAPEX + debt-funded IDC and fees)", "=IF({debt_mode}=1,MIN({comm_cap},MAX(0,({str_maxdebt}*({fund_base}+{debt_c}*({idc_kc}+{upfront_fee}))-{debt_c})/(1-{str_maxdebt}*({idc_km}+{upfront_fee})))),MIN({lock_m},MAX(0,({str_maxdebt}*({fund_base}+{debt_c}*({idc_kc}+{upfront_fee}))-{debt_c})/(1-{str_maxdebt}*({idc_km}+{upfront_fee})))))", "USDm", "m"); r += 1
calc(ws, r, "eq_total_res", "Residual equity required", "={uses}-{s_grant}-{s_goveq}-{debt_c}-{debt_m}", "USDm", "m"); r += 1
calc(ws, r, "s_goveq_res", "  of which government (if residual provider)", "=IF({str_resid}=2,{eq_total_res},0)", "USDm", "m"); r += 1
calc(ws, r, "s_priv", "  of which private sponsors", "=IF({str_resid}=1,{eq_total_res},0)", "USDm", "m"); r += 1
calc(ws, r, "sources", "TOTAL SOURCES", "={s_grant}+{s_goveq}+{debt_c}+{debt_m}+{eq_total_res}", "USDm", "m", out=True); r += 1
section(ws, r, "C. DEBT CAPACITY & FINANCING GAP"); r += 1
calc(ws, r, "comm_cap", "Commercial debt capacity (DSCR-sculpted, lender case)", "=SUMPRODUCT([RNG:sculpt],[RNG:dfm])", "USDm", "m", out=True); r += 1
calc(ws, r, "debt_cap", "Total senior debt capacity", "={debt_c}+{comm_cap}", "USDm", "m", out=True); r += 1
calc(ws, r, "gearing", "Senior debt / total uses", "=({debt_c}+{debt_m})/{uses}", "%", "pct", out=True); r += 1
calc(ws, r, "priv_avail", "Private equity available", "={str_privmax}*{fund_base}", "USDm", "m"); r += 1
calc(ws, r, "fin_gap", "FINANCING GAP (private equity required beyond availability)", "=IF({str_resid}=1,MAX(0,{s_priv}-{priv_avail}),0)", "USDm", "m", out=True); r += 1
calc(ws, r, "gov_resid_flag", "Government residual funding (public structure)", "={s_goveq_res}", "USDm", "m"); r += 1
calc(ws, r, "fin_gap_pct", "Financing gap / total uses", "={fin_gap}/{uses}", "%", "pct"); r += 1
section(ws, r, "D. KEY RESULTS"); r += 1
calc(ws, r, "kpi_pirr", "Project IRR (post-tax, unlevered, nominal)", "=IFERROR(IRR([RNG:ucf],0.08),\"n/a\")", "%", "pct", out=True); r += 1
calc(ws, r, "kpi_npv", "Project NPV @ discount rate", "=NPV({disc_rate},[RNG:ucf])", "USDm", "m", out=True); r += 1
calc(ws, r, "kpi_eirr", "Private equity IRR (nominal)", "=IF({s_priv}>0,IFERROR(IRR([RNG:eq_priv_cf],0.1),IFERROR(IRR([RNG:eq_priv_cf],-0.1),IFERROR(IRR([RNG:eq_priv_cf],-0.5),-1))),\"n/a\")", "%", "pct", out=True); r += 1
calc(ws, r, "kpi_girr", "Government equity IRR (nominal)", "=IF({s_goveq}+{s_goveq_res}>0,IFERROR(IRR([RNG:eq_gov_cf],0.05),\"n/a\"),\"n/a\")", "%", "pct", out=True); r += 1
calc(ws, r, "lcoe", "LCOE — plant (nominal levelised)", "=NPV({disc_rate},[RNG:lc_cost])/NPV({disc_rate},[RNG:delivered_paid])*1000", "USD/MWh", "n2", out=True); r += 1
calc(ws, r, "lcoe_sys", "LCOE — delivered system cost incl. public transmission & losses", "=NPV({disc_rate},[RNG:lc_cost_sys])/NPV({disc_rate},[RNG:lc_e_sys])*1000", "USD/MWh", "n2", out=True); r += 1
calc(ws, r, "kpi_min_dscr", "Minimum DSCR (actual case)", "=IF(COUNT([RNG:dscr])=0,99,MIN([RNG:dscr]))", "x", "x", out=True); r += 1
calc(ws, r, "kpi_avg_dscr", "Average DSCR (actual case)", "=AVERAGE([RNG:dscr])", "x", "x", out=True); r += 1
calc(ws, r, "kpi_llcr", "LLCR at COD (all tranches, weighted rate, longest tranche life)", "=IFERROR(SUMPRODUCT([RNG:cfads],[RNG:dfw],[RNG:inloan_all])/({debt_c}+{debt_m}),0)", "x", "x", out=True); r += 1
calc(ws, r, "kpi_plcr", "PLCR at COD", "=IFERROR(SUMPRODUCT([RNG:cfads],[RNG:dfm])/({debt_c}+{debt_m}),0)", "x", "x", out=True); r += 1
calc(ws, r, "kpi_short", "Cumulative debt-service shortfall", "=[C:shortfall]", "USDm", "m", out=True); r += 1
calc(ws, r, "opex_y2", "OPEX in operating year 2", "=SUMPRODUCT(([RNG:opyr]=2)*[RNG:opex])", "USDm", "m"); r += 1
calc(ws, r, "afford_tariff", "Utility payment headroom per MWh (avg max sustainable payment / energy paid, op yrs 1-10)", "=IFERROR(SUMPRODUCT(([RNG:opyr]>=1)*([RNG:opyr]<=10)*[RNG:u_maxppa])/{u_share}/SUMPRODUCT(([RNG:opyr]>=1)*([RNG:opyr]<=10)*[RNG:epaid])*1000,0)", "USD/MWh", "n2", out=True); r += 1

# ===================================================================================
# 18 DEBT
# ===================================================================================
ws = WS["18_DEBT"]
title(ws, "18 DEBT — Concessional & commercial tranches, DSCR sculpting, DSRA", "Non-circular: IDC and DSRA are equity-funded; sizing uses an unlevered-tax lender case", ts=True)
r = 6
inp(ws, r, "lock_m", "Locked commercial debt (debt_mode = 2)", 90.0, "USDm", "Base-case debt_m (written by tools/run_snapshots.py)", "m", True); r += 1
inp(ws, r, "lock_c", "Locked concessional debt (debt_mode = 2)", 0.0, "USDm", "Base-case debt_c", "m", True); r += 1
inp(ws, r, "lock_grant", "Locked grant / VGF (debt_mode = 2)", 0.0, "USDm", "Base-case s_grant", "m", True); r += 1
inp(ws, r, "lock_goveq", "Locked government equity (debt_mode = 2)", 0.0, "USDm", "Base-case s_goveq", "m", True); r += 1
inp(ws, r, "hedge", "Share of commercial debt fixed or swapped", 0.75, "%", "Rate stress applies only to the unhedged share", "pct", True); r += 1
calc(ws, r, "rm_eff", "Effective commercial rate", "={str_rm}+{eff_rate_add}*(1-{hedge})", "%", "pct2"); r += 1
ws.cell(r, 1, "Locked commercial principal schedule by OPERATING year (debt_mode = 2; column E = op year 1, F = op year 2, ...)").font = F_BASE
TSROW["lock_ds"] = (ws.title, r)
for c in TCOLS:
    cc = ws[f"{c}{r}"]; cc.value = 0; cc.font = F_INPUT; cc.fill = FILL_INPUT; cc.number_format = FMT["m"]
r += 1
calc(ws, r, "tax_rate_ref", "Tax rate used in lender-case CFADS", "={tax_rate}", "%", "pct"); r += 1
calc(ws, r, "idc_kc", "IDC per USD of concessional debt (non-circular factor)", "={str_rc}*SUMPRODUCT([RNG:consflag],[RNG:cumsh]-0.5*[RNG:share])", "x", "n3"); r += 1
calc(ws, r, "idc_km", "IDC per USD of commercial debt (non-circular factor)", "={rm_eff}*SUMPRODUCT([RNG:consflag],[RNG:cumsh]-0.5*[RNG:share])", "x", "n3"); r += 1
section(ws, r, "A. LENDER-CASE CFADS & SCULPTING", ts=True); r += 1
ts(ws, r, "cfads_len", "Lender-case CFADS (unlevered tax)", "USDm",
   "=[rev_len]-[opex]-[o_roy_len]-IF([opyr]>{tax_hol},{tax_rate}*MAX(0,[rev_len]-[opex]-[o_roy_len]-[dep_len]),0)", "m", total="sum"); r += 1
ts(ws, r, "inloan", "Commercial loan life flag", "flag", "=IF(AND([opyr]>=1,[opyr]<={str_nm}),1,0)", "flag"); r += 1
ts(ws, r, "dfm", "Discount factor at commercial rate (to COD)", "x", "=IF([opyr]>=1,1/(1+{rm_eff})^[opyr],0)", "n3"); r += 1
calc(ws, r, "rw", "Weighted senior debt rate", "=IFERROR(({debt_c}*{str_rc}+{debt_m}*{rm_eff})/({debt_c}+{debt_m}),{rm_eff})", "%", "pct2"); r += 1
ts(ws, r, "inloan_all", "Any senior tranche outstanding (loan life)", "flag", "=IF(AND([opyr]>=1,[opyr]<=MAX({str_nm},IF({debt_c}>0,{str_gc}+{str_nc},0))),1,0)", "flag"); r += 1
ts(ws, r, "dfw", "Discount factor at weighted rate", "x", "=IF([opyr]>=1,1/(1+{rw})^[opyr],0)", "n3"); r += 1
ts(ws, r, "sculpt", "Sculpted commercial DS capacity", "USDm", "=[inloan]*MAX(0,[cfads_len]/{str_dscr}-[c_ds])", "m", total="sum"); r += 1
section(ws, r, "B. CONCESSIONAL TRANCHE", ts=True); r += 1
ts(ws, r, "c_open", "Opening balance", "USDm", "=[c_close@p]", "m"); r += 1
ts(ws, r, "c_draw", "Drawdown", "USDm", "={debt_c}*[share]", "m", total="sum"); r += 1
ts(ws, r, "c_int", "Interest", "USDm", "={str_rc}*([c_open]+0.5*[c_draw]*[consflag])", "m", total="sum"); r += 1
ts(ws, r, "c_prin", "Principal repayment", "USDm", "=IF(AND([opyr]>{str_gc},[opyr]<={str_gc}+{str_nc}),MIN([c_open],{debt_c}/{str_nc}),0)", "m", total="sum"); r += 1
ts(ws, r, "c_close", "Closing balance", "USDm", "=[c_open]+[c_draw]-[c_prin]", "m"); r += 1
ts(ws, r, "c_ds", "Debt service (operations)", "USDm", "=[opflag]*([c_int]+[c_prin])", "m", total="sum"); r += 1
section(ws, r, "C. COMMERCIAL TRANCHE", ts=True); r += 1
ts(ws, r, "m_open", "Opening balance", "USDm", "=[m_close@p]", "m"); r += 1
ts(ws, r, "m_draw", "Drawdown", "USDm", "={debt_m}*[share]", "m", total="sum"); r += 1
ts(ws, r, "m_int", "Interest", "USDm", "={rm_eff}*([m_open]+0.5*[m_draw]*[consflag])", "m", total="sum"); r += 1
ts(ws, r, "m_target", "Target debt service (sculpted or annuity)", "USDm",
   "=IF([inloan]=1,IF({debt_mode}=1,IF({comm_cap}>0,[sculpt]*{debt_m}/{comm_cap},0),IF({lock_m}>0,INDEX([RNG:lock_ds],1,[opyr])*{debt_m}/{lock_m},0)+[m_int]),0)", "m"); r += 1
ts(ws, r, "m_prin", "Principal repayment", "USDm", "=IF([inloan]=1,MAX(0,MIN([m_open],IF([opyr]={str_nm},[m_open],[m_target]-[m_int]))),0)", "m", total="sum"); r += 1
ts(ws, r, "m_close", "Closing balance", "USDm", "=[m_open]+[m_draw]-[m_prin]", "m"); r += 1
ts(ws, r, "m_ds", "Debt service (operations)", "USDm", "=[opflag]*([m_int]+[m_prin])", "m", total="sum"); r += 1
section(ws, r, "D. TOTALS & DSRA", ts=True); r += 1
ts(ws, r, "ds", "Total senior debt service", "USDm", "=[c_ds]+[m_ds]", "m", total="sum", bold=True); r += 1
ts(ws, r, "idc", "Interest during construction", "USDm", "=[consflag]*([c_int]+[m_int])", "m", total="sum"); r += 1
ts(ws, r, "debt_bal", "Total senior debt outstanding", "USDm", "=[c_close]+[m_close]", "m"); r += 1
ts(ws, r, "dsra_tgt", "DSRA target balance", "USDm", "=IF(OR([opflag]=1,[lastcons]=1),{dsra_m}/12*[ds@n],0)", "m"); r += 1
ts(ws, r, "dsra_init", "Initial DSRA funding (end of construction)", "USDm", "=[lastcons]*[dsra_tgt]", "m", total="sum"); r += 1

# ===================================================================================
# 21 TAX
# ===================================================================================
ws = WS["21_TAX"]
title(ws, "21 TAX — Depreciation, interest deductibility, loss carry-forward, tax holiday", "", ts=True)
r = 6
inp(ws, r, "tax_rate", "Corporate income tax rate", 0.30, "%", "Fictional", "pct", True); r += 1
inp(ws, r, "tax_hol", "Tax holiday (operating years)", 5, "years", "Fiscal incentive = forgone revenue", "int", True); r += 1
inp(ws, r, "dep_yrs", "Tax depreciation life (straight line)", 20, "years", "", "int"); r += 1
calc(ws, r, "dep_base", "Depreciable base (funding base + IDC + fees − grants)", "={fund_base}+{u_idc}+{u_fee}-{s_grant}", "USDm", "m"); r += 1
ts(ws, r, "dep", "Tax depreciation", "USDm", "=IF(AND([opyr]>=1,[opyr]<={dep_yrs}),{dep_base}/{dep_yrs},0)", "m", total="sum"); r += 1
ts(ws, r, "dep_len", "Lender-case depreciation (excl. IDC & fees, avoids circularity)", "USDm", "=IF(AND([opyr]>=1,[opyr]<={dep_yrs}),({fund_base}-{s_grant})/{dep_yrs},0)", "m", total="sum"); r += 1
ts(ws, r, "ebitda_t", "EBITDA", "USDm", "=[ebitda]", "m"); r += 1
ts(ws, r, "int_t", "Interest expense (operations)", "USDm", "=[opflag]*([c_int]+[m_int])", "m"); r += 1
ts(ws, r, "taxable", "Taxable income before losses", "USDm", "=[ebitda_t]-[dep]-[int_t]", "m"); r += 1
ts(ws, r, "loss_bf", "Losses brought forward", "USDm", "=[loss_cf@p]", "m"); r += 1
ts(ws, r, "loss_use", "Losses used", "USDm", "=IF(AND([taxable]>0,[opyr]>{tax_hol}),MIN([taxable],[loss_bf]),0)", "m"); r += 1
ts(ws, r, "loss_cf", "Losses carried forward", "USDm", "=[loss_bf]-[loss_use]+MAX(0,-[taxable])", "m"); r += 1
ts(ws, r, "tax", "Corporate tax paid", "USDm", "=IF([opyr]>{tax_hol},{tax_rate}*MAX(0,[taxable]-[loss_use]),0)", "m", total="sum", bold=True); r += 1
ts(ws, r, "tax_forgone", "Tax forgone due to holiday", "USDm", "=IF(AND([opyr]>=1,[opyr]<={tax_hol}),{tax_rate}*MAX(0,[taxable]-[loss_use]),0)", "m", total="sum"); r += 1
ts(ws, r, "tax_unlev", "Unlevered tax (for project IRR)", "USDm", "=IF([opyr]>{tax_hol},{tax_rate}*MAX(0,[ebitda]-[dep]),0)", "m", total="sum"); r += 1

# ===================================================================================
# 20 CASH FLOW
# ===================================================================================
ws = WS["20_CASH_FLOW"]
title(ws, "20 CASH FLOW — Construction funding, operating waterfall, unlevered cash flow, LCOE streams", "", ts=True)
r = 6
section(ws, r, "A. CONSTRUCTION FUNDING", ts=True); r += 1
ts(ws, r, "use_t", "Uses: CAPEX + project transmission + IDC + fees + DSRA", "USDm",
   "=[capex_nom]+[tx_spend_prj]*[consflag]+[idc]+IF(#T#=1,{u_fee}+{u_devprem},0)+[dsra_init]", "m", total="sum"); r += 1
ts(ws, r, "grant_t", "Grants drawn", "USDm", "={s_grant}*[share]", "m", total="sum"); r += 1
ts(ws, r, "debt_t", "Senior debt drawn", "USDm", "=[c_draw]+[m_draw]", "m", total="sum"); r += 1
ts(ws, r, "eq_t", "Equity contributions (total)", "USDm", "=[use_t]-[grant_t]-[debt_t]", "m", total="sum"); r += 1
ts(ws, r, "eq_gov_in", "  Government equity", "USDm", "=IF({eq_total}>0,[eq_t]*({s_goveq}+{s_goveq_res})/{eq_total},0)", "m", total="sum"); r += 1
ts(ws, r, "eq_priv_in", "  Private equity", "USDm", "=[eq_t]-[eq_gov_in]", "m", total="sum"); r += 1
section(ws, r, "B. OPERATING WATERFALL", ts=True); r += 1
ts(ws, r, "cf_rev", "Cash revenue", "USDm", "=[rev_cash]", "m", total="sum"); r += 1
ts(ws, r, "cf_opex", "OPEX", "USDm", "=-[opex]", "m", total="sum"); r += 1
ts(ws, r, "cf_roy", "Water royalty", "USDm", "=-[o_roy]", "m", total="sum"); r += 1
ts(ws, r, "ebitda", "EBITDA", "USDm", "=[cf_rev]+[cf_opex]+[cf_roy]", "m", total="sum", bold=True); r += 1
ts(ws, r, "cf_tax", "Tax", "USDm", "=-[tax]", "m", total="sum"); r += 1
ts(ws, r, "cfads", "CFADS (after any project-funded transmission spend in operations)", "USDm", "=[opflag]*([ebitda]+[cf_tax]-[tx_spend_prj])", "m", total="sum", bold=True); r += 1
ts(ws, r, "cf_ds", "Senior debt service", "USDm", "=-[ds]", "m", total="sum"); r += 1
ts(ws, r, "dscr", "DSCR", "x", "=IF([ds]>0.001,[cfads]/[ds],\"\")", "x"); r += 1
ts(ws, r, "avail0", "Cash after debt service before reserve movements (incl. trapped cash)", "USDm", "=[cfads]+[cf_ds]+[cash_bf]", "m"); r += 1
ts(ws, r, "dsra_draw", "DSRA drawn to meet debt service", "USDm", "=[opflag]*MIN([dsra_act@p],MAX(0,-[avail0]))", "m", total="sum"); r += 1
ts(ws, r, "dsra_relx", "DSRA release of excess over target", "USDm", "=[opflag]*MAX(0,[dsra_act@p]-[dsra_draw]-[dsra_tgt])", "m", total="sum"); r += 1
ts(ws, r, "dsra_top", "DSRA top-up from available cash", "USDm", "=[opflag]*MIN(MAX(0,[dsra_tgt]-[dsra_act@p]+[dsra_draw]),MAX(0,[avail0]))", "m", total="sum"); r += 1
ts(ws, r, "dsra_act", "DSRA actual balance", "USDm", "=[dsra_act@p]+[dsra_init]-[dsra_draw]-[dsra_relx]+[dsra_top]", "m"); r += 1
ts(ws, r, "cf_dsra", "DSRA draw + release - top-up", "USDm", "=[dsra_draw]+[dsra_relx]-[dsra_top]", "m", total="sum"); r += 1
ts(ws, r, "cash_avail", "Cash after debt service", "USDm", "=[cfads]+[cf_ds]+[cf_dsra]", "m", total="sum"); r += 1
ts(ws, r, "cash_bf", "Cash brought forward (trapped)", "USDm", "=[cash_cf@p]", "m"); r += 1
ts(ws, r, "shortfall", "Debt-service shortfall funded by guarantor/sponsor", "USDm", "=MAX(0,-([cash_avail]+[cash_bf]))", "m", total="sum"); r += 1
ts(ws, r, "lock_ok", "Distribution test passed (1=yes)", "flag", "=IF([opflag]=1,IF([ds]>0.001,IF([dscr]>={lockup},1,0),1),0)", "flag"); r += 1
ts(ws, r, "pool", "Cash available after shortfall funding", "USDm", "=[cash_avail]+[cash_bf]+[shortfall]", "m"); r += 1
ts(ws, r, "grepay", "Repayment of sovereign guarantee claims (ahead of distributions)", "USDm", "=IF(OR([lock_ok]=1,[opyr]={ops_years}),MIN([gclaim@p],MAX(0,[pool])),0)", "m", total="sum"); r += 1
ts(ws, r, "dist", "Distributions to equity", "USDm", "=IF(OR([lock_ok]=1,[opyr]={ops_years}),MAX(0,[pool]-[grepay]),0)", "m", total="sum"); r += 1
ts(ws, r, "cash_cf", "Cash carried forward", "USDm", "=[pool]-[grepay]-[dist]", "m"); r += 1
section(ws, r, "C. EQUITY CASH FLOWS", ts=True); r += 1
ts(ws, r, "sf_guar", "Shortfall paid by sovereign guarantee", "USDm", "=[shortfall]*{str_guar}", "m", total="sum"); r += 1
ts(ws, r, "sf_eq", "Shortfall paid by equity (sponsor support)", "USDm", "=[shortfall]-[sf_guar]", "m", total="sum"); r += 1
ts(ws, r, "gclaim", "Sovereign guarantee claim outstanding", "USDm", "=[gclaim@p]+[sf_guar]-[grepay]", "m"); r += 1
ts(ws, r, "eq_gov_cf", "Government equity cash flow", "USDm", "=-[eq_gov_in]+([dist]-[sf_eq])*{gov_eq_share}", "m", total="sum"); r += 1
ts(ws, r, "eq_priv_cf", "Private equity cash flow", "USDm", "=-[eq_priv_in]+([dist]-[sf_eq])*(1-{gov_eq_share})", "m", total="sum", bold=True); r += 1
ts(ws, r, "eq_priv_cum", "Private equity cumulative (unrecovered if negative)", "USDm", "=[eq_priv_cum@p]+[eq_priv_cf]", "m"); r += 1
section(ws, r, "D. UNLEVERED & LCOE STREAMS", ts=True); r += 1
ts(ws, r, "ucf", "Unlevered post-tax project cash flow", "USDm", "=-[capex_nom]-[tx_spend_prj]-IF(#T#=1,{u_devprem},0)+[opflag]*([ebitda]-[tax_unlev])", "m", total="sum", bold=True); r += 1
ts(ws, r, "lc_cost", "Plant cost stream (CAPEX + OPEX + royalty)", "USDm", "=[capex_nom]+[tx_spend_prj]+IF(#T#=1,{u_devprem},0)+[opex]+[o_roy]", "m", total="sum"); r += 1
ts(ws, r, "delivered_paid", "Energy delivered + deemed", "GWh", "=[delivered]+[deemed]", "gwh", total="sum"); r += 1
ts(ws, r, "lc_cost_sys", "System cost stream (+ public transmission CAPEX & O&M)", "USDm", "=[lc_cost]+[tx_spend_pub]+IF({tx_party}=1,[tx_omc],0)", "m", total="sum"); r += 1
ts(ws, r, "lc_e_sys", "Energy delivered to load (net of transmission losses)", "GWh", "=[delivered]*(1-{tx_loss})", "gwh", total="sum"); r += 1

# ===================================================================================
# 19 EQUITY
# ===================================================================================
ws = WS["19_EQUITY"]
title(ws, "19 EQUITY — Contributions, distributions, returns by holder", "", ts=True)
r = 6
calc(ws, r, "eq_total", "Total equity (government + private)", "={eq_total_res}+{s_goveq}", "USDm", "m"); r += 1
calc(ws, r, "gov_eq_share", "Government share of equity", "=IF({eq_total}>0,({s_goveq}+{s_goveq_res})/{eq_total},0)", "%", "pct"); r += 1
calc(ws, r, None, "Private equity IRR", "={kpi_eirr}", "%", "pct", out=True); r += 1
calc(ws, r, None, "Target private equity IRR", "={str_hurdle}", "%", "pct"); r += 1
calc(ws, r, None, "Government equity IRR", "={kpi_girr}", "%", "pct", out=True); r += 1
calc(ws, r, "eq_mult", "Private equity multiple (distributions / contributions)", "=IFERROR(SUMIF([RNG:eq_priv_cf],\">0\")/-SUMIF([RNG:eq_priv_cf],\"<0\"),0)", "x", "x"); r += 1
r += 1
ts(ws, r, "e_in", "Private equity contributed", "USDm", "=[eq_priv_in]", "m", total="sum"); r += 1
ts(ws, r, "e_out", "Distributions to private equity", "USDm", "=[dist]*(1-{gov_eq_share})", "m", total="sum"); r += 1
ts(ws, r, "e_cf", "Net private equity cash flow", "USDm", "=[eq_priv_cf]", "m", total="sum"); r += 1
ts(ws, r, "e_g_out", "Dividends to government", "USDm", "=[dist]*{gov_eq_share}", "m", total="sum"); r += 1
ts(ws, r, "e_pvfwd", "Value of remaining private distributions at target IRR (backward recursion)", "USDm", "=([e_out@n]+[e_pvfwd@n])/(1+{str_hurdle})", "m"); r += 1
ts(ws, r, "e_unrec", "Unrecovered private equity (for termination amount)", "USDm", "=MAX(0,-[eq_priv_cum])", "m"); r += 1

# ===================================================================================
# 22 GOVERNMENT SUPPORT
# ===================================================================================
ws = WS["22_GOVERNMENT_SUPPORT"]
title(ws, "22 GOVERNMENT SUPPORT — Direct exposure (cash)", "Equity, grants/VGF, transmission investment, utility support", ts=True)
r = 6
ts(ws, r, "g_eq", "Government equity contributions", "USDm", "=[eq_gov_in]", "m", total="sum"); r += 1
ts(ws, r, "g_grant", "Grants / VGF / public capital contribution", "USDm", "=[grant_t]", "m", total="sum"); r += 1
ts(ws, r, "g_tx", "Public transmission CAPEX", "USDm", "=[tx_spend_pub]", "m", total="sum"); r += 1
ts(ws, r, "g_txom", "Public transmission O&M", "USDm", "=IF({tx_party}=1,[tx_omc],0)", "m", total="sum"); r += 1
ts(ws, r, "g_util", "Utility support: budget backstop of PPA shortfall", "USDm", "=[cov_backstop]", "m", total="sum"); r += 1
ts(ws, r, "g_direct", "TOTAL DIRECT GOVERNMENT CASH EXPOSURE", "USDm", "=[g_eq]+[g_grant]+[g_tx]+[g_txom]+[g_util]", "m", total="sum", bold=True); r += 1
note(ws, r + 1, "Transmission is shown on a cash (capex) basis. If financed by a sovereign loan, the fiscal profile becomes the loan's debt service; the PV comparison is in 25_FISCAL_IMPACT.")

# ===================================================================================
# 23 GUARANTEES
# ===================================================================================
ws = WS["23_GUARANTEES"]
title(ws, "23 GUARANTEES — Nominal exposure by instrument (maximum amount at risk each year)", "Exposures are NOT additive: see 24 for non-double-counted maximum", ts=True)
r = 6
inp(ws, r, "ppag_months", "PPA guarantee cap", 12, "months of utility billing", "Exposure measure for the guarantee", "int"); r += 1
inp(ws, r, "mrg", "Minimum revenue guarantee level (0 = none)", 0.0, "% of P50 billed revenue", "", "pct"); r += 1
ts(ws, r, "x_debt", "Debt guarantee / counter-indemnity exposure", "USDm", "=(1-{str_onbud})*{str_guar}*[debt_bal]", "m", total="max"); r += 1
ts(ws, r, "x_ppa", "PPA payment guarantee exposure", "USDm", "={str_ppag}*{ppag_months}/12*[rev_util]", "m", total="max"); r += 1
ts(ws, r, "x_term", "Termination payment exposure", "USDm", "={str_term}*([opflag]+[consflag]>0)*([debt_bal]+MAX([e_unrec]*(1+{term_prem}),[e_pvfwd]))", "m", total="max"); r += 1
ts(ws, r, "x_fx", "FX convertibility guarantee (annual remittances covered)", "USDm", "={str_fxg}*([ds]+[e_out])", "m", total="max"); r += 1
ts(ws, r, "x_mrg", "Minimum revenue guarantee — deterministic call", "USDm", "=[opflag]*MAX(0,{mrg}*[rev_cap]/MAX(0.0001,[rampf])-[rev_cash])", "m", total="sum"); r += 1
ts(ws, r, "x_onbud", "Project debt recorded as direct public debt", "USDm", "={str_onbud}*[debt_bal]", "m", total="max"); r += 1

# ===================================================================================
# 24 CONTINGENT LIABILITIES
# ===================================================================================
ws = WS["24_CONTINGENT_LIABILITIES"]
title(ws, "24 CONTINGENT LIABILITIES — Maximum exposure, deterministic calls, user-defined expected loss",
      "Probabilities are USER JUDGEMENTS for screening, not calibrated default probabilities", ts=True)
r = 6
inp(ws, r, "pr_debt", "Annual probability: debt guarantee called", 0.02, "% p.a.", "User judgement", "pct", True); r += 1
inp(ws, r, "pr_ppa", "Annual probability: PPA guarantee called", 0.08, "% p.a.", "User judgement — informed by utility arrears history", "pct", True); r += 1
inp(ws, r, "pr_term", "Annual probability: termination for government default / PFM", 0.005, "% p.a.", "User judgement", "pct", True); r += 1
inp(ws, r, "lgd", "Loss given call (net of recoveries)", 0.6, "%", "User judgement", "pct"); r += 1
section(ws, r, "A. EXPOSURE", ts=True); r += 1
ts(ws, r, "cl_max", "Maximum simultaneous exposure = MAX(termination, debt guarantee + PPA guarantee + FX cover)", "USDm", "=MAX([x_term],[x_debt]+[x_ppa]+[x_fx])", "m", total="max", bold=True); r += 1
section(ws, r, "B. DETERMINISTIC CALLS IN ACTIVE SCENARIO", ts=True); r += 1
ts(ws, r, "call_ppa", "PPA guarantee calls", "USDm", "=[cov_guar]", "m", total="sum"); r += 1
ts(ws, r, "call_debt", "Debt guarantee calls (DS shortfall x guaranteed share)", "USDm", "=[sf_guar]", "m", total="sum"); r += 1
ts(ws, r, "call_mrg", "Minimum revenue guarantee calls", "USDm", "=[x_mrg]", "m", total="sum"); r += 1
ts(ws, r, "call_tot", "Total deterministic calls", "USDm", "=[call_ppa]+[call_debt]+[call_mrg]", "m", total="sum", bold=True); r += 1
section(ws, r, "C. EXPECTED LOSS (only as good as the probabilities entered)", ts=True); r += 1
ts(ws, r, "el", "Expected annual loss", "USDm", "=({pr_debt}*[x_debt]+{pr_ppa}*MAX(0,[x_ppa]-[cov_guar])+{pr_term}*MAX(0,[x_term]-[x_debt]))*{lgd}", "m", total="sum"); r += 1
ts(ws, r, "gdf", "Government discount factor", "x", "=1/(1+{gov_disc})^#T#", "n3"); r += 1
calc(ws, r, "cl_peak", "Peak maximum contingent exposure", "=[C:cl_max]", "USDm", "m", out=True); r += 1
calc(ws, r, "cl_pv_el", "PV of expected loss (screening)", "=SUMPRODUCT([RNG:el],[RNG:gdf])", "USDm", "m", out=True); r += 1
calc(ws, r, "cl_pv_calls", "PV of deterministic calls in active scenario", "=SUMPRODUCT([RNG:call_tot],[RNG:gdf])", "USDm", "m", out=True); r += 1

# ===================================================================================
# 25 FISCAL IMPACT
# ===================================================================================
ws = WS["25_FISCAL_IMPACT"]
title(ws, "25 FISCAL IMPACT — Annual government cash requirement and fiscal NPV", "Negative = cost to government", ts=True)
r = 6
section(ws, r, "A. OUTFLOWS", ts=True); r += 1
ts(ws, r, "f_direct", "Direct support (22)", "USDm", "=-[g_direct]", "m", total="sum"); r += 1
ts(ws, r, "f_calls", "Guarantee calls in active scenario (24)", "USDm", "=-[call_tot]", "m", total="sum"); r += 1
section(ws, r, "B. INFLOWS", ts=True); r += 1
ts(ws, r, "f_tax", "Corporate tax", "USDm", "=[tax]", "m", total="sum"); r += 1
ts(ws, r, "f_roy", "Water royalty", "USDm", "=[o_roy]", "m", total="sum"); r += 1
ts(ws, r, "f_div", "Dividends on government equity", "USDm", "=[e_g_out]-[sf_eq]*{gov_eq_share}", "m", total="sum"); r += 1
ts(ws, r, "f_grep", "Recoveries of guarantee calls (project and utility)", "USDm", "=[grepay]+[ppag_reimb]", "m", total="sum"); r += 1
ts(ws, r, "f_net", "NET FISCAL CASH FLOW (central government)", "USDm", "=[f_direct]+[f_calls]+[f_tax]+[f_roy]+[f_div]+[f_grep]", "m", total="sum", bold=True); r += 1
ts(ws, r, "f_soe_row", "Incremental cash of the state-owned utility (incl. new arrears as a cost)", "USDm", "=[f_soe]", "m", total="sum"); r += 1
ts(ws, r, "f_net_cons", "NET CONSOLIDATED PUBLIC-SECTOR CASH FLOW", "USDm", "=[f_net]+[f_soe_row]", "m", total="sum", bold=True); r += 1
ts(ws, r, "f_cum", "Cumulative net fiscal cash flow", "USDm", "=[f_cum@p]+[f_net]", "m"); r += 1
ts(ws, r, "f_need", "Annual government cash requirement (outflows)", "USDm", "=-([f_direct]+[f_calls])", "m", total="max"); r += 1
ts(ws, r, "f_need_rev", "Annual cash requirement / government revenue", "%", "=[f_need]/[gov_rev]", "pct2", total="max"); r += 1
calc(ws, r, "fis_npv", "FISCAL NPV @ government discount rate", "=SUMPRODUCT([RNG:f_net],[RNG:gdf])", "USDm", "m", out=True); r += 1
calc(ws, r, "fis_npv_cons", "CONSOLIDATED FISCAL NPV (government + state utility)", "=SUMPRODUCT([RNG:f_net_cons],[RNG:gdf])", "USDm", "m", out=True); r += 1
calc(ws, r, "fis_npv_el", "Fiscal NPV less PV of expected loss on remaining contingent exposure", "={fis_npv}-{cl_pv_el}", "USDm", "m", out=True); r += 1
calc(ws, r, "fis_peak", "Peak annual government cash requirement", "=[C:f_need]", "USDm", "m", out=True); r += 1
calc(ws, r, "fis_peak_rev", "Peak annual requirement / government revenue", "=[C:f_need_rev]", "%", "pct2", out=True); r += 1
calc(ws, r, "fis_trough", "Maximum cumulative fiscal outlay", "=-MIN(0,MIN([RNG:f_cum]))", "USDm", "m", out=True); r += 1
calc(ws, r, "fis_tax_forgone", "Tax forgone through holiday (nominal)", "=[C:tax_forgone]", "USDm", "m"); r += 1

# ===================================================================================
# 26 DEBT SUSTAINABILITY
# ===================================================================================
ws = WS["26_DEBT_SUSTAINABILITY"]
title(ws, "26 PROJECT-LEVEL FISCAL EXPOSURE SCREENING", "NOT a debt sustainability analysis. Does not replace IMF/World Bank DSA. Fictional country data.", ts=True)
r = 6
section(ws, r, "A. COUNTRY INPUTS (fictional Navaria, 2026)", ts=True); r += 1
inp(ws, r, "gdp0", "Nominal GDP", 35.0, "USD bn", "Fictional", "n2", True); r += 1
inp(ws, r, "gdp_g", "Nominal USD GDP growth", 0.05, "% p.a.", "", "pct"); r += 1
inp(ws, r, "rev_gdp", "Government revenue (excl. grants)", 0.16, "% GDP", "", "pct"); r += 1
inp(ws, r, "debt_gdp", "Public debt", 0.48, "% GDP", "", "pct", True); r += 1
inp(ws, r, "ext_share", "External / FX share of public debt", 0.55, "%", "", "pct"); r += 1
inp(ws, r, "ds_rev", "Public debt service / revenue", 0.22, "%", "", "pct"); r += 1
inp(ws, r, "fis_bal", "Overall fiscal balance", -0.045, "% GDP", "", "pct"); r += 1
inp(ws, r, "dsa_rating", "Latest published DSA risk of debt distress (1=low, 2=moderate, 3=high, 4=in distress)", 2, "1-4", "Take from latest IMF/WB DSA — fictional here", "int", True); r += 1
section(ws, r, "B. SCREENING THRESHOLDS (user-editable, illustrative)", ts=True); r += 1
inp(ws, r, "th_debt", "Public debt / GDP benchmark", 0.55, "% GDP", "LIC-DSF PV total public debt benchmark 35/55/70% (weak/medium/strong) [FR-09]; nominal vs PV not adjusted", "pct"); r += 1
inp(ws, r, "th_incr", "Material increment in debt / GDP from one project", 0.01, "% GDP", "Screening convention — user-defined", "pct"); r += 1
inp(ws, r, "th_cl", "Material contingent exposure", 0.02, "% GDP", "Screening convention — user-defined", "pct"); r += 1
inp(ws, r, "th_cash", "Material annual cash requirement", 0.01, "% revenue", "Screening convention — user-defined", "pct"); r += 1
section(ws, r, "C. PROJECTIONS", ts=True); r += 1
ts(ws, r, "gdp", "Nominal GDP", "USDm", "={gdp0}*1000*(1+{gdp_g})^([year]-{base_year})", "m0"); r += 1
ts(ws, r, "gov_rev", "Government revenue", "USDm", "=[gdp]*{rev_gdp}", "m0"); r += 1
ts(ws, r, "s_onbud", "On-budget project debt / GDP", "%", "=[x_onbud]/[gdp]", "pct2", total="max"); r += 1
ts(ws, r, "s_cl", "Maximum contingent exposure / GDP", "%", "=[cl_max]/[gdp]", "pct2", total="max"); r += 1
ts(ws, r, "s_cash", "Government cash requirement / revenue", "%", "=[f_need]/[gov_rev]", "pct2", total="max"); r += 1
ts(ws, r, "s_cumout", "Cumulative fiscal outlay / GDP", "%", "=MAX(0,-[f_cum])/[gdp]", "pct2", total="max"); r += 1
ts(ws, r, "s_arr", "Utility arrears to the IPP / GDP", "%", "=[u_arrears]/[gdp]", "pct2", total="max"); r += 1
ts(ws, r, "s_inc", "On-budget increment in the same year (direct debt + cumulative outlay + SOE arrears) / GDP", "%", "=[s_onbud]+[s_cumout]+[s_arr]", "pct2", total="max"); r += 1
section(ws, r, "D. SCREENING RESULT", ts=True); r += 1
calc(ws, r, "sc_debt", "Peak on-budget increment / GDP", "=[C:s_inc]", "% GDP", "pct2", out=True); r += 1
calc(ws, r, "sc_cl", "Peak contingent exposure / GDP", "=[C:s_cl]", "% GDP", "pct2", out=True); r += 1
calc(ws, r, "sc_cash", "Peak cash requirement / revenue", "=[C:s_cash]", "% rev", "pct2", out=True); r += 1
calc(ws, r, "sc_post", "Public debt / GDP incl. peak project increment", "={debt_gdp}+{sc_debt}", "% GDP", "pct", out=True); r += 1
calc(ws, r, "sc_flags", "Thresholds breached (0-4; 4th = project pushes debt above benchmark)",
     "=({sc_debt}>{th_incr})+({sc_cl}>{th_cl})+({sc_cash}>{th_cash})+AND({sc_post}>{th_debt},{debt_gdp}<={th_debt})", "#", "int", out=True); r += 1
calc(ws, r, "sc_result", "PROJECT-LEVEL FISCAL EXPOSURE SCREENING RESULT",
     "=IF(AND({sc_flags}=0,{dsa_rating}<=2),\"LOW additional fiscal pressure\",IF(OR({sc_flags}>=3,AND({sc_flags}>=1,OR({dsa_rating}>=3,{debt_gdp}>{th_debt}))),\"HIGH additional fiscal pressure — escalate to MoF / DSA team\",\"MODERATE additional fiscal pressure\"))", "", None, out=True); r += 1

# ===================================================================================
# 30 BANKABILITY
# ===================================================================================
ws = WS["30_BANKABILITY"]
title(ws, "30 BANKABILITY — Hydropower Bankability Framework™ (9 gates, weakest-link, auditable thresholds)",
      "Score: 3 READY, 2 CONDITIONAL, 1 DEVELOPMENT GAP, 0 CRITICAL GAP. Gate status = weakest test. Thresholds are illustrative and editable.")
heads = ["Gate / test", "Direction", "Metric", "READY if", "COND. if", "DEV. GAP if", "Score", "Status", "Source / logic"]
for j, h in enumerate(heads):
    c = ws.cell(4, 1 + j, h); c.font = F_HDR; c.fill = FILL_HDR
for col, w in zip("ABCDEFGHI", [58, 10, 12, 10, 10, 10, 8, 18, 50]):
    ws.column_dimensions[col].width = w
GATES = [
    ("G1", "GATE 1 — RESOURCE", [
        ("Reliable flow record (years)", "H", "{rec_years}", 25, 15, 8, "int", "03_HYDROLOGY"),
        ("P90 / P50 energy ratio", "H", "{p90_p50}", 0.85, 0.78, 0.70, "n2", "03_HYDROLOGY"),
        ("Hydrology study maturity (1-3)", "H", "{hyd_study}", 3, 2, 1, "int", "03_HYDROLOGY")]),
    ("G2", "GATE 2 — DEMAND", [
        ("Bankable / contracted demand, worst of op yrs 1-5", "H", "{dem_ratio5}", 1.0, 0.9, 0.7, "n2", "10_DEMAND"),
        ("Project share of system peak at COD", "L", "{share_cod}", 0.15, 0.25, 0.35, "pct", "09_GRID")]),
    ("G3", "GATE 3 — CONFIGURATION", [
        ("Unit CAPEX / benchmark", "L", "{capex_vs_bm}", 1.0, 1.25, 1.5, "n2", "05_PLANT_CAPEX"),
        ("Capacity factor (P50)", "H", "{cf}", 0.45, 0.35, 0.25, "pct", "03_HYDROLOGY"),
        ("Feasibility maturity (1-3)", "H", "{fs_level}", 3, 2, 1, "int", "05_PLANT_CAPEX")]),
    ("G4", "GATE 4 — TRANSMISSION", [
        ("Evacuation capacity at COD / installed", "H", "{evac_cod}/{inst_mw}", 1.0, 0.8, 0.5, "n2", "09_GRID"),
        ("Transmission lag behind plant COD (years)", "L", "{tx_gap_yrs}", 0, 1, 2, "int", "08_TRANSMISSION"),
        ("Transmission financing secured (1/0)", "H", "{tx_fin}", 1, 1, 0, "int", "08_TRANSMISSION")]),
    ("G5", "GATE 5 — OFFTAKER / UTILITY", [
        ("Utility payment capacity / PPA payment, worst of op yrs 1-10", "H", "{ut_ratio10}", 1.2, 1.0, 0.8, "n2", "12_UTILITY"),
        ("Utility collection rate", "H", "{ut_coll}+{eff_coll_adj}", 0.95, 0.90, 0.80, "pct", "12_UTILITY"),
        ("Payment security (months of billing)", "H", "{lc_months}", 6, 3, 1, "int", "11_OFFTAKER")]),
    ("G6", "GATE 6 — REGULATION / PPA", [
        ("Regulatory items at CRITICAL GAP", "L", "{reg_crit}", 0, 0, 0, "int", "13_REGULATION"),
        ("Regulatory items at GAP", "L", "{reg_gap}", 1, 3, 5, "int", "13_REGULATION"),
        ("Fixed (capacity) share of revenue", "H", "{rev_fixed}", 0.6, 0.4, 0.2, "pct", "16_REVENUE")]),
    ("G7", "GATE 7 — FINANCING", [
        ("Minimum DSCR, actual case", "H", "{kpi_min_dscr}", "={str_dscr}", "={lockup}", 1.0, "n2", "20_CASH_FLOW"),
        ("Financing gap / total uses", "L", "{fin_gap_pct}", 0, 0.05, 0.15, "pct", "17_PROJECT_FINANCE"),
        ("Private equity IRR vs target (n/a = met)", "H", "IF(ISNUMBER({kpi_eirr}),{kpi_eirr},IF({s_priv}>0,-1,{str_hurdle}))", "={str_hurdle}", "={str_hurdle}-0.02", "={str_hurdle}-0.05", "pct", "19_EQUITY")]),
    ("G8", "GATE 8 — PUBLIC FINANCE", [
        ("Peak annual government cash requirement / revenue", "L", "{sc_cash}", 0.005, 0.01, 0.02, "pct", "26_DEBT_SUSTAINABILITY"),
        ("Peak contingent exposure / GDP", "L", "{sc_cl}", 0.01, 0.02, 0.04, "pct", "24/26"),
        ("Peak on-budget increment / GDP (direct debt, outlays, SOE arrears)", "L", "{sc_debt}", 0.005, 0.01, 0.02, "pct", "26_DEBT_SUSTAINABILITY"),
        ("Consolidated fiscal NPV (incl. state utility) / GDP", "H", "{fis_npv_cons}/({gdp0}*1000)", 0, -0.005, -0.02, "pct", "25_FISCAL_IMPACT"),
        ("Country DSA risk rating (1-4)", "L", "{dsa_rating}", 1, 2, 3, "int", "26_DEBT_SUSTAINABILITY")]),
    ("G9", "GATE 9 — E&S / SUSTAINABILITY", [
        ("ESIA & lender-standard compliance (1-3)", "H", "{es_level}", 3, 2, 1, "int", "13_REGULATION"),
        ("Resettlement plan status (1-3)", "H", "{rap_level}", 3, 2, 1, "int", "13_REGULATION"),
        ("Transboundary / riparian issues (1-3)", "H", "{tb_level}", 3, 2, 1, "int", "13_REGULATION")]),
]
ACTIONS = {
    "G1": ["Commission independent hydrology review; extend record via regional correlation; derive P90 from simulated series",
           "Complete independent hydrology review and agree P90 basis with lenders' technical adviser"],
    "G2": ["Re-phase capacity or secure anchor (mining/export) offtake; update load forecast with utility",
           "Confirm demand absorption with utility dispatch study and anchor-load MoUs"],
    "G3": ["Value-engineer layout / re-optimise installed capacity; obtain EPC price discovery",
           "Finalise bankable feasibility study and lenders' technical adviser review"],
    "G4": ["Secure financing & EPC for evacuation line; align transmission COD with plant COD; agree deemed-energy allocation",
           "Lock transmission financing and interface agreement (dates, LDs, deemed energy)"],
    "G5": ["Agree utility recovery plan (tariff path, loss reduction), escrow of receivables, liquidity facility / LC sizing",
           "Size LC to ≥6 months, ring-fence collections, monitor utility KPIs"],
    "G6": ["Close critical legal/regulatory gaps (tariff pass-through, land, FX) before PPA signature",
           "Resolve remaining GAP items via implementation agreement / regulatory decisions"],
    "G7": ["Restructure financing: more concessional debt, longer tenor, grant/VGF, or tariff adjustment to close gap",
           "Lock financing terms; run lender stress cases; agree DSCR covenants"],
    "G8": ["Cap guarantees, replace sovereign guarantees with liquidity instruments, record commitments in fiscal risk statement",
           "Obtain Ministry of Finance fiscal-risk sign-off and disclose commitments"],
    "G9": ["Upgrade ESIA/RAP to lender standards; independent E&S review; riparian notification",
           "Complete RAP implementation milestones before financial close"],
}
r = 5
GATE_ROWS = {}
for gid, gname, tests in GATES:
    section(ws, r, gname); gate_row = r; r += 1
    first = r
    for (lab, d, metric, rdy, cnd, dev, f, src) in tests:
        ws.cell(r, 1, "   " + lab).font = F_BASE
        ws.cell(r, 2, d).font = F_BASE
        put(ws, f"C{r}", "=" + metric, f)
        for j, v in enumerate([rdy, cnd, dev]):
            col = "DEF"[j]
            if isinstance(v, str):
                put(ws, f"{col}{r}", v, f)
            else:
                c = ws[f"{col}{r}"]; c.value = v; c.font = F_INPUT; c.fill = FILL_INPUT; c.number_format = FMT[f]
        if d == "H":
            put(ws, f"G{r}", f"=IF(C{r}>=D{r},3,IF(C{r}>=E{r},2,IF(C{r}>=F{r},1,0)))", "int")
        else:
            put(ws, f"G{r}", f"=IF(C{r}<=D{r},3,IF(C{r}<=E{r},2,IF(C{r}<=F{r},1,0)))", "int")
        put(ws, f"H{r}", f'=CHOOSE(G{r}+1,"CRITICAL GAP","DEVELOPMENT GAP","CONDITIONAL","READY")')
        ws.cell(r, 9, src).font = F_BASE
        r += 1
    last = r - 1
    put(ws, f"G{gate_row}", f"=MIN(G{first}:G{last})", "int", font=F_BOLD)
    put(ws, f"H{gate_row}", f'=CHOOSE(G{gate_row}+1,"CRITICAL GAP","DEVELOPMENT GAP","CONDITIONAL","READY")', font=F_BOLD)
    put(ws, f"I{gate_row}", f'=IF(G{gate_row}<=1,"{ACTIONS[gid][0]}",IF(G{gate_row}=2,"{ACTIONS[gid][1]}","No pre-close action required"))')
    GATE_ROWS[gid] = (gate_row, gname)
    REF[f"{gid}_score"] = f"{q(ws.title)}!$G${gate_row}"
    REF[f"{gid}_status"] = f"{q(ws.title)}!$H${gate_row}"
    REF[f"{gid}_action"] = f"{q(ws.title)}!$I${gate_row}"
ws.conditional_formatting.add(f"H5:H{r}", CellIsRule(operator="equal", formula=['"READY"'], fill=PatternFill("solid", fgColor="C6EFCE")))
ws.conditional_formatting.add(f"H5:H{r}", CellIsRule(operator="equal", formula=['"CONDITIONAL"'], fill=PatternFill("solid", fgColor="FFEB9C")))
ws.conditional_formatting.add(f"H5:H{r}", CellIsRule(operator="equal", formula=['"DEVELOPMENT GAP"'], fill=PatternFill("solid", fgColor="F8CBAD")))
ws.conditional_formatting.add(f"H5:H{r}", CellIsRule(operator="equal", formula=['"CRITICAL GAP"'], fill=PatternFill("solid", fgColor="FF7C80")))
r += 1
section(ws, r, "GATE SUMMARY & RANKING (tie-break: gate order)"); r += 1
SUM0 = r
for cc, h in enumerate(["Gate", "Score", "Rank key", "Status", "Action"], start=1):
    c = ws.cell(r, cc, h); c.font = F_HDR; c.fill = FILL_HDR
r += 1
gid_list = list(GATE_ROWS.keys())
for i, gid in enumerate(gid_list):
    gr, gname = GATE_ROWS[gid]
    ws.cell(r, 1, gname).font = F_BASE
    put(ws, f"B{r}", f"=G{gr}", "int")
    put(ws, f"C{r}", f"=B{r}+{(i+1)/100}", "n2")
    put(ws, f"D{r}", f"=H{gr}")
    put(ws, f"E{r}", f"=I{gr}")
    r += 1
SUM_FIRST, SUM_LAST = SUM0 + 1, r - 1
REF["gate_keys"] = f"{q(ws.title)}!$C${SUM_FIRST}:$C${SUM_LAST}"
REF["gate_names"] = f"{q(ws.title)}!$A${SUM_FIRST}:$A${SUM_LAST}"
REF["gate_status"] = f"{q(ws.title)}!$D${SUM_FIRST}:$D${SUM_LAST}"
REF["gate_actions"] = f"{q(ws.title)}!$E${SUM_FIRST}:$E${SUM_LAST}"
r += 1
calc(ws, r, "bk_min", "Lowest gate score", f"=MIN(B{SUM_FIRST}:B{SUM_LAST})", "", "int", out=True); r += 1
calc(ws, r, "bk_ncrit", "Gates at CRITICAL GAP", f"=COUNTIF(B{SUM_FIRST}:B{SUM_LAST},0)", "#", "int"); r += 1
calc(ws, r, "bk_ndev", "Gates at DEVELOPMENT GAP", f"=COUNTIF(B{SUM_FIRST}:B{SUM_LAST},1)", "#", "int"); r += 1
calc(ws, r, "bk_overall", "OVERALL VERDICT",
     '=IF({bk_ncrit}>0,"NOT BANKABLE — critical gap(s) must be closed",IF({bk_ndev}>0,"NOT YET BANKABLE — development gaps remain",IF({bk_min}=2,"BANKABLE SUBJECT TO CONDITIONS","READY FOR FINANCIAL CLOSE")))', "", None, out=True); r += 1
note(ws, r + 1, "Methodology: each test maps a metric to a status using three explicit thresholds. A gate's status is its weakest test (no averaging, no hidden weights). "
     "Thresholds are illustrative screening values chosen by the model author; calibrate them to lender term sheets, IMF/WB guidance and the project's context.")

# ===================================================================================
# 29 RISK ALLOCATION
# ===================================================================================
ws = WS["29_RISK_ALLOCATION"]
title(ws, "29 RISK ALLOCATION — Who bears each risk, and can it be contractually mitigated?",
      "P = primary bearer, S = shares risk, blank = none. Indicative allocation for the selected PPP/IPP structure (fictional).")
parties = ["Government", "Developer", "EPC", "Lender", "Utility", "Consumer", "Insurer", "DFI"]
hdr = ["Risk"] + parties + ["Contractually mitigable?", "Main instruments", "Model link"]
for j, h in enumerate(hdr):
    c = ws.cell(4, 1 + j, h); c.font = F_HDR; c.fill = FILL_HDR; c.alignment = Alignment(wrap_text=True)
ws.column_dimensions["A"].width = 28
for j in range(8):
    ws.column_dimensions[L(2 + j)].width = 11
ws.column_dimensions["J"].width = 14; ws.column_dimensions["K"].width = 60; ws.column_dimensions["L"].width = 22
RISKS = [
    ("Hydrology", "", "P", "", "S", "", "", "", "", "Partial", "Energy-only exposure via two-part tariff; DSRA; P90 sizing; hydrology reserve; parametric drought cover (where available)", "03/04, st_drought"),
    ("Construction (geology, quality)", "", "S", "P", "S", "", "", "S", "", "Yes (largely)", "Fixed-price date-certain EPC, LDs, performance bonds, CAR insurance, geotechnical baseline report", "05/06"),
    ("Cost overrun", "S", "P", "S", "S", "", "", "", "S", "Partial", "Contingency, standby debt/equity, sponsor completion support; unforeseen geology often reverts to owner", "st_capex"),
    ("Delay", "S", "P", "S", "S", "", "", "S", "", "Partial", "Delay LDs, DSU insurance, IDC contingency", "st_delay"),
    ("Demand", "S", "", "", "", "P", "S", "", "", "Partial", "Take-or-pay / deemed energy shifts risk to utility → ultimately government/consumers", "10, st_demand"),
    ("Offtaker payment", "P", "S", "", "S", "P", "S", "", "S", "Partial", "LC/escrow, liquidity facility, sovereign guarantee, PRG, MIGA NHSFO, utility recovery plan", "12, st_offtaker"),
    ("Tariff / regulatory reset", "P", "S", "", "S", "S", "S", "", "", "Yes", "PPA tariff fixed by contract; regulator approval of pass-through", "13/14"),
    ("FX", "P", "S", "", "S", "P", "S", "", "S", "Partial", "USD tariff (moves risk to utility), FX convertibility undertaking, local-currency debt tranche", "st_fx"),
    ("Interest rate", "", "P", "", "S", "", "", "", "S", "Yes", "Fixed-rate DFI loans, swaps, concessional fixed-rate tranches", "st_rate"),
    ("Political", "P", "S", "", "S", "", "", "S", "S", "Yes (insurable)", "MIGA/ATI political risk insurance, PRG, stabilisation, arbitration", "23"),
    ("Regulatory / change in law", "P", "S", "", "S", "", "", "", "", "Yes", "Change-in-law compensation in PPA/IA", "13"),
    ("Transmission", "P", "S", "", "S", "P", "", "", "S", "Partial", "Interface agreement, deemed energy, parallel financing of line, transmission PPP", "08/09, st_trans"),
    ("Grid stability / curtailment", "S", "S", "", "", "P", "", "", "", "Partial", "Grid code compliance, deemed energy, dispatch rules", "09"),
    ("Environmental & social", "S", "P", "S", "S", "", "", "", "S", "Partial", "ESIA/ESMP to lender standards, RAP budget, independent monitoring, e-flow covenants", "13 (Gate 9)"),
    ("Natural force majeure", "S", "S", "S", "S", "S", "", "P", "", "Partial", "Insurance; FM relief; extension of term", "14"),
    ("Termination", "P", "S", "", "S", "S", "", "", "S", "Yes (defines liability)", "Termination payment formulae; buy-out; step-in rights", "23 x_term"),
]
r = 5
for row in RISKS:
    for j, v in enumerate(row):
        c = ws.cell(r, 1 + j, v); c.font = F_INPUT if 1 <= j <= 9 else F_BASE
        c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = BOX
    r += 1
ws.conditional_formatting.add(f"B5:I{r-1}", CellIsRule(operator="equal", formula=['"P"'], fill=PatternFill("solid", fgColor="F8CBAD")))
ws.conditional_formatting.add(f"B5:I{r-1}", CellIsRule(operator="equal", formula=['"S"'], fill=PatternFill("solid", fgColor="FFEB9C")))
r += 1
calc(ws, r, None, "Risks where Government is primary bearer", f'=COUNTIF(B5:B{r-2},"P")', "#", "int", out=True); r += 1
calc(ws, r, None, "Risks where Utility is primary bearer", f'=COUNTIF(F5:F{r-3},"P")', "#", "int", out=True); r += 1
note(ws, r + 1, "Allocation reflects a generic risk-matrix logic for discussion; actual allocation depends on negotiated contracts. Not legal advice.")

# ===================================================================================
# 28 SENSITIVITY
# ===================================================================================
ws = WS["28_SENSITIVITY"]
title(ws, "28 SENSITIVITY — Live closed-form LCOE tornado + full-engine snapshot",
      "Live section recalculates instantly; snapshot section is generated by tools/run_snapshots.py")
r = 4
section(ws, r, "A. LIVE LCOE TORNADO (screening: real annuity on plant CAPEX, P50, discount rate)"); r += 1
calc(ws, r, "lc_crf", "Capital recovery factor", "={disc_rate}/(1-(1+{disc_rate})^-{ops_years})", "x", "n3"); r += 1
calc(ws, r, "lc_cap", "Base capital (funding base + IDC)", "={fund_base}+{u_idc}", "USDm", "m"); r += 1
calc(ws, r, "lc_base", "Screening LCOE — base", "=({lc_cap}*{lc_crf}+{opex_y2})/{p50}*1000", "USD/MWh", "n2", out=True); r += 1
for cc, h in enumerate(["Driver", "Flex", "LCOE low", "LCOE high", "Swing", "", ""], start=1):
    c = ws.cell(r, cc, h); c.font = F_HDR; c.fill = FILL_HDR
r += 1
TOR = [("CAPEX ±20%", 0.2, "=({lc_cap}*(1-B#)*{lc_crf}+{opex_y2})/{p50}*1000", "=({lc_cap}*(1+B#)*{lc_crf}+{opex_y2})/{p50}*1000"),
       ("Generation ±10%", 0.1, "=({lc_cap}*{lc_crf}+{opex_y2})/({p50}*(1+B#))*1000", "=({lc_cap}*{lc_crf}+{opex_y2})/({p50}*(1-B#))*1000"),
       ("Discount rate ±2pp", 0.02, "=({lc_cap}*(({disc_rate}-B#)/(1-(1+{disc_rate}-B#)^-{ops_years}))+{opex_y2})/{p50}*1000", "=({lc_cap}*(({disc_rate}+B#)/(1-(1+{disc_rate}+B#)^-{ops_years}))+{opex_y2})/{p50}*1000"),
       ("OPEX ±20%", 0.2, "=({lc_cap}*{lc_crf}+{opex_y2}*(1-B#))/{p50}*1000", "=({lc_cap}*{lc_crf}+{opex_y2}*(1+B#))/{p50}*1000"),
       ("Delivered share (curtailment 0-15%)", 0.15, "=({lc_cap}*{lc_crf}+{opex_y2})/{p50}*1000", "=({lc_cap}*{lc_crf}+{opex_y2})/({p50}*(1-B#))*1000")]
for lab, flex, lo, hi in TOR:
    ws.cell(r, 1, lab).font = F_BASE
    c = ws.cell(r, 2, flex); c.font = F_INPUT; c.fill = FILL_INPUT; c.number_format = FMT["pct"]
    put(ws, f"C{r}", lo.replace("B#", f"$B${r}"), "n2")
    put(ws, f"D{r}", hi.replace("B#", f"$B${r}"), "n2")
    put(ws, f"E{r}", f"=D{r}-C{r}", "n2")
    r += 1
TOR_FIRST, TOR_LAST = r - len(TOR), r - 1
SENS_SNAP_ROW = r + 2
note(ws, r, "Closed-form screening: ignores tax, financing structure and timing. Use full-engine snapshot for financing metrics.")

# ===================================================================================
# 31 CASE STUDY
# ===================================================================================
ws = WS["31_CASE_STUDY"]
title(ws, "31 CASE STUDY — Fictional reference project vs public benchmark cases",
      "Benchmarks only from public sources (see research/). 'PUBLIC DATA NOT FOUND' where not verified.")
CASE_ROW0 = 4
CASES = [
 ("Nachtigal", "Cameroon", "IPP/PPP, IFC-led DFI debt", 420, "EUR 1,184m (~US$1,383m) per World Bank PAD", 1383, "FC Nov 2018; 57-month build planned, COD 2023; 7th unit coupled 27 Feb 2025", "Full capacity ~2 yrs late; defects found by regulator (ARSEL) Aug 2023", "IBRD payment guarantee EUR 86m + loan guarantee EUR 171m (sovereign indemnity); MIGA up to EUR 224.8m; 76:24 debt:equity (PAD)", "Guarantees move payment risk to the sovereign via indemnities", "africa_part2 S1-S5, S63-S64; source_database PF-11"),
 ("Bujagali", "Uganda", "IPP + IDA PRG", 250, "US$582m (2001 est.) → 799m (2007 est.) → 862m (2012, sponsor 'so far')", 862, "c.2007-2012", "+48% vs cancelled 2001 design; not like-for-like (2001 scope incl. 100 km line)", "IDA PRG US$115m with sovereign indemnity; MIGA US$115m; liquidity facility", "Short tenor front-loaded tariff; 2018 refinancing cost the state a tax waiver", "africa_part2 S48-S53"),
 ("Bui", "Ghana", "Public (BPA), China Exim, cocoa escrow", 400, "US$622m → 790m (2012 review)", 790, "COD Dec 2013", "+US$168m (+27%)", "China Exim tranches secured on cocoa export escrow", "Commodity escrow can substitute for a weak offtaker; utility arrears persist", "africa_part1 S38-S43"),
 ("Kafue Gorge Lower", "Zambia", "State-owned, sovereign-guaranteed Chinese debt", 750, "US$2.0bn incl. US$312m capitalised interest", 2000, "Nov 2015 → full COD Mar 2023", "from US$1.48bn; ~3 yrs late", "Sovereign guarantee; ZESCO arrears entered sovereign DSA", "Utility liabilities migrate onto sovereign balance sheet", "africa_part1 S57-S60; source_database DB-03"),
 ("Isimba", "Uganda", "Public, 85% China Exim / 15% GoU", 183, "US$567.7m", 567.7, "Apr 2015 → Mar 2019", "~7 months late; ~700 defects reported", "Sovereign borrower", "Fast state finance ≠ quality; owner's engineer matters", "africa_part2 S34-S35 (defects reported 2021)"),
 ("Karuma", "Uganda", "Public, 85% China Exim / 15% GoU", 600, "US$1.7bn", 1700, "Contract 2013 (5 yrs) → COD Jun 2024", "~5-6 yrs late", "Sovereign borrower", "Delay cost borne by state utility (capitalised interest)", "africa_part2 S40-S42"),
 ("Julius Nyerere (Rufiji)", "Tanzania", "100% state budget", 2115, "US$2.8-2.9bn (TZS 6.5-7.45tn)", 2850, "Construction 2019 → 2025/26 (42-month EPC)", "~3 yrs late; estimate rose TZS 6.5 → 7.45tn", "None (budget-funded; 99.5% domestic revenue)", "Creates surplus over peak; depends on exports/demand growth", "africa_part2 S30-S32, S65"),
 ("Rusumo Falls", "Rwanda/Tanzania/Burundi", "Regional public, IDA-financed", 80, "US$468.9m project cost", 468.9, "Approval 2013 → COD Feb 2025", "CP1 civil contract +47%; livelihood restoration/local development US$18m → ~38m", "IDA grants/credits; transmission parallel-financed AfDB/EU", "Multi-country transmission & PPAs gate the revenue", "africa_part2 S16-S18"),
 ("Mpatamanga", "Malawi", "PPP, storage + peaking", 358.5, "US$1.5-1.64bn (estimate)", 1636, "Pre-construction; 5-yr build in 35-yr PPA", "Estimate grew from ~US$1bn (ENR, Sep 2022)", "IDA PRG US$100m; MIGA US$180m; IDA grant US$350m to govt", "Heavy concessional layering to make tariff affordable", "africa_part2 S26-S29"),
 ("Ruzizi III", "DRC/Rwanda/Burundi", "Regional PPP (stalled)", 206, "US$760m (2025; EUR 728m for 147 MW design in 2020)", 760, "Target 2030 before conflict pause", "In preparation since at least 2009; no financial close", "IFIs ~60% expected; EIB lead arranger", "Multi-state & conflict risk prevents close", "africa_part2 S20-S25"),
 ("GERD", "Ethiopia", "State, domestically financed", 5150, "≈US$5bn (budget US$4.8bn)", 5000, "2011 → inauguration Sep 2025", "~14-yr build", "91% domestic (bonds, payroll, public); China Exim ~US$1bn for E&M; no MDB finance", "Transboundary disputes; low cost/kW but very long build", "africa_part1 S1-S6"),
 ("Gibe III", "Ethiopia", "State, ICBC-financed EPC", 1870, "EUR 1.47-1.55bn", "", "Inaugurated Dec 2016", "PUBLIC DATA NOT FOUND", "ICBC loan after MDBs withdrew", "Procurement governance drives lender eligibility", "africa_part1 S53-S55"),
 ("Nam Theun 2 (intl.)", "Lao PDR", "Export IPP, MDB-guaranteed", 1070, "US$1.25bn base + US$200m contingency", 1450, "FC Jun 2005 → commissioned Apr 2010", "Turnkey price-capped EPC; overrun PUBLIC DATA NOT FOUND", "IDA & ADB PRGs, MIGA (~US$186m debt covered); EGAT take-or-pay PPA", "Creditworthy export offtaker, not the local utility, underpinned bankability", "international_benchmarks S9-S13, S24"),
 ("Upper Trishuli-1 (intl.)", "Nepal", "DFI-led domestic IPP", 216, "US$647.4m", 647.4, "Completion slipped 2024 → Dec 2026 (scheduled)", "~2 yrs", "DFI debt ~70%", "Domestic-utility IPP needs layered DFI risk cover", "international_benchmarks S15-S19"),
 ("Reventazón (intl.)", "Costa Rica", "Utility trust & lease, project bond", 305.5, "US$1.4bn", 1400, "FC Jan 2014 → inaugurated Sep 2016 (search summary)", "Post-COD spillway repairs ~US$15m", "Trust owns plant, leased to ICE; IDB A-loan, IFC, IG-rated bond, local-currency bank debt", "Off-balance-sheet form, but risk remains with the state utility", "international_benchmarks S20-S23"),
]
ws.column_dimensions["A"].width = 24
hdr = ["Project", "Country", "Structure", "MW", "Reported cost (as published)", "Cost used (USDm, nominal)", "USD/kW (nominal, unadjusted)", "Timeline", "Overrun / delay", "Credit support", "Lesson (analyst inference)", "Source (research/ file & IDs)"]
widths = [24, 16, 28, 9, 34, 12, 12, 30, 28, 40, 44, 30]
for j, h in enumerate(hdr):
    c = ws.cell(CASE_ROW0, 1 + j, h); c.font = F_HDR; c.fill = FILL_HDR; c.alignment = Alignment(wrap_text=True)
    ws.column_dimensions[L(1 + j)].width = widths[j]
r = CASE_ROW0 + 1
cfirst = r
for row in CASES:
    for j, v in enumerate(row):
        if j < 6:
            c = ws.cell(r, 1 + j, v)
        else:
            c = ws.cell(r, 2 + j, v)
        c.font = F_BASE; c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(r, 4).number_format = FMT["mw"]; ws.cell(r, 6).number_format = FMT["m0"]
    put(ws, f"G{r}", f'=IF(ISNUMBER(F{r}),F{r}/D{r}*1000,"n/a")', "m0")
    r += 1
clast = r - 1
ws.cell(r, 1, "Kasiri River Hydro (FICTIONAL reference)").font = F_BOLD
ws.cell(r, 2, "Navaria (fictional)").font = F_BASE
put(ws, f"C{r}", "={str_name}")
put(ws, f"D{r}", "={inst_mw}", "mw")
ws.cell(r, 5, "Model: plant CAPEX nominal").font = F_BASE
put(ws, f"F{r}", "={u_capex}", "m0")
put(ws, f"G{r}", f"=F{r}/D{r}*1000", "m0")
put(ws, f"H{r}", '="FC "&{start_year}&" → COD "&{cod_year}')
r += 2
calc(ws, r, None, "Median USD/kW of benchmark cases with USD cost (nominal, unadjusted)", f"=MEDIAN(G{cfirst}:G{clast})", "USD/kW", "m0", out=True); r += 1
calc(ws, r, None, "Kasiri River Hydro / median", f"=G{clast+1}/C{r-1}", "x", "x", out=True); r += 1
note(ws, r + 1, "Costs are as published, in nominal currency of the year reported, with different scopes (some include IDC, transmission, resettlement). Unit costs are NOT price- or scope-adjusted and are indicative only. "
     "Full field-by-field case files (A-AD) incl. 'PUBLIC DATA NOT FOUND' entries are in research/case_studies/. EUR costs not converted (n/a).")

# ===================================================================================
# 01A DEVELOPMENT — stages, budget, attrition, developer returns, valuation step-ups
# ===================================================================================
ws = WS["01A_DEVELOPMENT"]
title(ws, "01A DEVELOPMENT — From site to financial close: budget, attrition and developer returns",
      "Development years precede the model start (financial close). Probabilities are user judgements informed by the research file; not calibrated statistics.")
ND = 10  # development-year columns
DCOLS = [L(6 + i) for i in range(ND)]  # F..O
for c in DCOLS:
    ws.column_dimensions[c].width = 9
ws.column_dimensions["D"].width = 11; ws.column_dimensions["E"].width = 11
r = 4
section(ws, r, "A. DEVELOPMENT STAGES (inputs)"); r += 1
for j, h in enumerate(["Stage", "Funder (typical)", "Duration (months)", "Budget (USDm, real)", "P(success to next stage)"]):
    c = ws.cell(r, 1 + j, h); c.font = F_HDR; c.fill = FILL_HDR
r += 1
STAGES = [
    ("Site identification and reconnaissance", "Developer equity", 6, 0.10, 0.60),
    ("Pre-feasibility and start of flow gauging", "Developer equity / project preparation grant", 12, 0.60, 0.60),
    ("Feasibility study, ESIA, geotechnical and grid studies", "Development equity, preparation facility", 18, 4.50, 0.70),
    ("Licences, water rights, land and permits", "Development equity", 12, 0.80, 0.85),
    ("PPA, implementation agreement and tariff approval", "Development equity", 12, 0.80, 0.80),
    ("Financing: lenders' advisers, legal, insurance, close", "Development equity, co-developer", 12, 2.20, 0.85),
]
ST0 = r
for k, (lab, fund, dur, cost, pr) in enumerate(STAGES):
    ws.cell(r, 1, f"{k+1}. {lab}").font = F_BASE
    ws.cell(r, 2, fund).font = F_BASE
    for col, v, f in [(3, dur, "int"), (4, cost, "n2"), (5, pr, "pct")]:
        c = ws.cell(r, col, v); c.font = F_INPUT; c.fill = FILL_INPUT; c.border = BOX; c.number_format = FMT[f]
    REF[f"dev_c{k+1}"] = f"{q(ws.title)}!$D${r}"; REF[f"dev_p{k+1}"] = f"{q(ws.title)}!$E${r}"
    r += 1
ST1 = r - 1
REF["dev_months"] = f"SUM({q(ws.title)}!$C${ST0}:$C${ST1})"
calc(ws, r, "dev_total", "Total development budget (real)", f"=SUM(D{ST0}:D{ST1})", "USDm", "n2", out=True); r += 1
calc(ws, r, "dev_years", "Development period", f"=SUM(C{ST0}:C{ST1})/12", "years", "n2", out=True); r += 1
calc(ws, r, "dev_pfc", "Probability of reaching financial close from reconnaissance", f"=PRODUCT(E{ST0}:E{ST1})", "%", "pct", out=True); r += 1
calc(ws, r, "dev_pct", "Development budget / plant CAPEX", "={dev_total}/{capex_real}", "%", "pct", out=True); r += 1
r += 1
section(ws, r, "B. DEVELOPER TERMS (inputs)"); r += 1
inp(ws, r, "dev_prem_pct", "Development premium paid at financial close (% of plant CAPEX)", 0.03, "%", "Negotiated; check against the research file before use", "pct", True); r += 1
calc(ws, r, "dev_prem", "Development premium", "={dev_prem_pct}*{capex_real}", "USDm", "n2", out=True); r += 1
inp(ws, r, "dev_stake", "Developer's share of private equity after financial close", 0.40, "%", "Remainder from a co-investor or fund", "pct", True); r += 1
inp(ws, r, "dev_rate", "Developer's discount rate for development-stage cash flows", 0.25, "%", "High-risk capital; assumption", "pct", True); r += 1
inp(ws, r, "r_fc", "Equity discount rate at financial close (construction risk)", 0.15, "%", "Assumption", "pct"); r += 1
inp(ws, r, "r_cod", "Equity discount rate at COD (operating asset)", 0.11, "%", "Assumption", "pct"); r += 1
r += 1
section(ws, r, "C. DEVELOPMENT CASH FLOWS ON THE SUCCESS PATH (USDm nominal; columns = development years, last = year before close)"); r += 1
ws.cell(r, 1, "Development year").font = F_BOLD
for i, c in enumerate(DCOLS):
    put(ws, f"{c}{r}", f"={{start_year}}-{ND}+{i}", "yr")
    ws[f"{c}{r}"].fill = FILL_HDR
YR_ROW = r; r += 1
SPEND0 = r
for k in range(len(STAGES)):
    rr = ST0 + k
    ws.cell(r, 1, f"Spend: stage {k+1}").font = F_BASE
    for i, c in enumerate(DCOLS):
        # months measured backwards: development ends at month dev_months; column i covers months (i-(ND-12*dev_years/12))...
        put(ws, f"{c}{r}",
            f"=IF($C${rr}>0,MAX(0,MIN({{dev_months}}-12*({ND}-1-{i})-0,SUM($C${ST0}:$C${rr}))-MAX({{dev_months}}-12*({ND}-{i}),SUM($C${ST0}:$C${rr})-$C${rr}))/$C${rr}*$D${rr},0)*(1+{{us_cpi}})^({c}${YR_ROW}-{{base_year}})", "n2")
    r += 1
SPEND1 = r - 1
ws.cell(r, 1, "Total development spend").font = F_BOLD
for c in DCOLS:
    put(ws, f"{c}{r}", f"=SUM({c}{SPEND0}:{c}{SPEND1})", "n2", font=F_BOLD)
put(ws, f"C{r}", f"=SUM({DCOLS[0]}{r}:{DCOLS[-1]}{r})", "n2")
TOT_ROW = r; r += 1
ws.cell(r, 1, "Probability the project is still alive when the money is spent").font = F_BASE
for c in DCOLS:
    # weighted by stage: P(reach stage k) = product of probabilities of earlier stages
    terms = "+".join(f"{c}{SPEND0+k}*PRODUCT($E${ST0}:$E${ST0+k})/$E${ST0+k}" for k in range(len(STAGES)))
    put(ws, f"{c}{r}", f"=IF({c}{TOT_ROW}>0,({terms})/{c}{TOT_ROW},0)", "pct")
PALIVE_ROW = r; r += 1
r += 1
section(ws, r, "D. DEVELOPER RETURNS"); r += 1
calc(ws, r, "dev_reimb", "Development costs reimbursed by the project at close (nominal)", f"=C{TOT_ROW}", "USDm", "n2"); r += 1
calc(ws, r, "dev_eq_npv_fc", "Developer's equity stake: NPV at close of its share of private equity flows at the close-stage rate", "={dev_stake}*NPV({r_fc},[RNG:eq_priv_cf])", "USDm", "n2"); r += 1
calc(ws, r, "dev_success_value", "Value received at close on the success path (reimbursement + premium + equity NPV)", "={dev_reimb}+{dev_prem}+{dev_eq_npv_fc}", "USDm", "n2", out=True); r += 1
calc(ws, r, "dev_pv_cost_unw", "PV at the start of development of spend on the success path", f"=NPV({{dev_rate}},{DCOLS[0]}{TOT_ROW}:{DCOLS[-1]}{TOT_ROW})*(1+{{dev_rate}})^({ND}-{{dev_months}}/12)", "USDm", "n2"); r += 1
calc(ws, r, "dev_pv_cost_rw", "PV of risk-weighted spend (each stage weighted by the chance of reaching it)", f"=SUMPRODUCT({DCOLS[0]}{TOT_ROW}:{DCOLS[-1]}{TOT_ROW},{DCOLS[0]}{PALIVE_ROW}:{DCOLS[-1]}{PALIVE_ROW},1/(1+{{dev_rate}})^(COLUMN({DCOLS[0]}{TOT_ROW}:{DCOLS[-1]}{TOT_ROW})-COLUMN({DCOLS[0]}{TOT_ROW})+1))*(1+{{dev_rate}})^({ND}-{{dev_months}}/12)", "USDm", "n2"); r += 1
calc(ws, r, "dev_pv_success", "PV at development start of value received at close", f"={{dev_success_value}}/(1+{{dev_rate}})^({{dev_months}}/12)", "USDm", "n2"); r += 1
calc(ws, r, "dev_npv_success", "Developer NPV if the project reaches close", "={dev_pv_success}-{dev_pv_cost_unw}", "USDm", "n2", out=True); r += 1
calc(ws, r, "dev_enpv", "RISK-WEIGHTED DEVELOPER NPV (expected, from reconnaissance)", "={dev_pfc}*{dev_pv_success}-{dev_pv_cost_rw}", "USDm", "n2", out=True); r += 1
calc(ws, r, "dev_be_prem", "Development premium that sets the risk-weighted NPV to zero", "=MAX(0,{dev_prem}-{dev_enpv}*(1+{dev_rate})^({dev_months}/12)/{dev_pfc})", "USDm", "n2", out=True); r += 1
calc(ws, r, "dev_be_prem_pct", "  as % of plant CAPEX", "={dev_be_prem}/{capex_real}", "%", "pct", out=True); r += 1
calc(ws, r, "dev_be_p", "Break-even probability of reaching close at the current premium (indicative: spend weights held fixed; n/a if the project loses value even on the success path)", '=IF({dev_npv_success}<=0,"n/a: negative on the success path",{dev_pv_cost_rw}/{dev_pv_success})', "%", "pct", out=True); r += 1
r += 1
section(ws, r, "D2. VALUE OF THE DEVELOPMENT POSITION AT THE START OF EACH STAGE (risk-weighted, real, 100%)"); r += 1
for j, h in enumerate(["Stage about to start", "P(close) from here", "PV of value at close", "PV of remaining spend", "Risk-weighted value"]):
    c = ws.cell(r, 1 + j, h); c.font = F_HDR; c.fill = FILL_HDR
r += 1
SV0 = r
for k in range(len(STAGES)):
    rk = ST0 + k
    ws.cell(r, 1, f"{k+1}. " + STAGES[k][0]).font = F_BASE
    start_k = f"(SUM($C${ST0}:$C${rk})-$C${rk})"
    put(ws, f"B{r}", f"=PRODUCT($E${rk}:$E${ST1})", "pct")
    put(ws, f"C{r}", f"=B{r}*{{dev_success_value}}/(1+{{dev_rate}})^(({{dev_months}}-{start_k})/12)", "n2")
    terms = []
    for jj in range(k, len(STAGES)):
        rj = ST0 + jj
        pj = "1" if jj == k else f"PRODUCT($E${rk}:$E${rj-1})"
        terms.append(f"$D${rj}*{pj}/(1+{{dev_rate}})^(((SUM($C${ST0}:$C${rj})-$C${rj})-{start_k}+0.5*$C${rj})/12)")
    put(ws, f"D{r}", "=" + "+".join(terms), "n2")
    put(ws, f"E{r}", f"=C{r}-D{r}", "n2")
    REF[f"sv{k+1}"] = f"{q(ws.title)}!$E${r}"
    REF[f"sp{k+1}"] = f"{q(ws.title)}!$B${r}"
    r += 1
note(ws, r, "Reading: the risk-weighted value is what the whole development position is worth to a buyer with the developer's discount rate, before the stage starts. It is the starting point for pricing a co-developer's entry."); r += 1
r += 1
section(ws, r, "E. VALUATION STEP-UPS (private equity, 100%)"); r += 1
calc(ws, r, "val_eq_in", "Private equity contributed (nominal)", "=[C:eq_priv_in]", "USDm", "n2"); r += 1
calc(ws, r, "val_fc", "Value of private equity at close (NPV of all equity flows at close-stage rate, plus contributions at PV)", "=NPV({r_fc},[RNG:eq_priv_cf])+NPV({r_fc},[RNG:eq_priv_in])", "USDm", "n2"); r += 1
calc(ws, r, "val_cod", "Value of private equity at COD (operating flows only, at COD rate, discounted to close)", "=SUMPRODUCT([RNG:opflag],[RNG:eq_priv_cf],1/(1+{r_cod})^([RNG:t]-{cons_eff}))/(1+{r_fc})^{cons_eff}", "USDm", "n2"); r += 1
calc(ws, r, "val_step_fc", "Value created at close (value at close less PV of contributions)", "=NPV({r_fc},[RNG:eq_priv_cf])", "USDm", "n2", out=True); r += 1
calc(ws, r, "val_step_cod", "De-risking step-up from close to COD (PV terms)", "={val_cod}-SUMPRODUCT([RNG:opflag],[RNG:eq_priv_cf],1/(1+{r_fc})^[RNG:t])", "USDm", "n2", out=True); r += 1
r += 1
section(ws, r, "F. DEVELOPER CASH FLOW ON THE SUCCESS PATH, WITH A SELL-DOWN AT COD"); r += 1
inp(ws, r, "sell_pct", "Share of the developer's stake sold at COD", 0.5, "%", "Sale at the COD value of the operating equity (section E rate)", "pct", True); r += 1
calc(ws, r, "v_cod_nom", "Value of 100% of private equity at COD (end of construction), at the COD rate", "=SUMPRODUCT([RNG:opflag],[RNG:eq_priv_cf],1/(1+{r_cod})^([RNG:t]-{cons_eff}))", "USDm", "n2"); r += 1
calc(ws, r, "sell_proceeds", "Sale proceeds to the developer", "={sell_pct}*{dev_stake}*{v_cod_nom}", "USDm", "n2", out=True); r += 1
NM = 40
ALLC = [L(6 + i) for i in range(ND + NM)]
ws.cell(r, 1, "Year").font = F_BOLD
for i, c in enumerate(ALLC):
    put(ws, f"{c}{r}", f"={{start_year}}-{ND}+{i}", "yr"); ws[f"{c}{r}"].fill = FILL_HDR
r += 1
ws.cell(r, 1, "Developer cash flow (USDm)").font = F_BOLD
for i, c in enumerate(ALLC):
    if i < ND:
        put(ws, f"{c}{r}", f"=-{DCOLS[i]}{TOT_ROW}", "n2")
    else:
        mc = TCOLS[i - ND]
        put(ws, f"{c}{r}",
            f"=IF({i-ND+1}=1,{{dev_reimb}}+{{dev_prem}},0)+{{dev_stake}}*{q('20_CASH_FLOW')}!{mc}{{eqp_row}}*IF({q('06_CONSTRUCTION')}!{mc}{{opf_row}}=1,1-{{sell_pct}},1)+IF({q('06_CONSTRUCTION')}!{mc}{{lc_row}}=1,{{sell_proceeds}},0)", "n2")
DEVCF_ROW = r
r += 1
REF["devcf_rng"] = f"{q(ws.title)}!${ALLC[0]}${DEVCF_ROW}:${ALLC[-1]}${DEVCF_ROW}"
calc(ws, r, "dev_irr", "DEVELOPER IRR on the success path (development spend to final distribution)", "=IFERROR(IF(ABS(IRR({devcf_rng},0.15))<1,IRR({devcf_rng},0.15),IF(ABS(IRR({devcf_rng},-0.05))<1,IRR({devcf_rng},-0.05),-1)),-1)", "%", "pct", out=True); r += 1
calc(ws, r, "dev_mult", "Developer cash multiple (inflows / outflows)", "=IFERROR(SUMIF({devcf_rng},\">0\")/-SUMIF({devcf_rng},\"<0\"),0)", "x", "x", out=True); r += 1
calc(ws, r, "dev_peak", "Developer's peak cumulative cash at risk", "=-MIN(0,MIN(" + ",".join(f"SUM(${ALLC[0]}${DEVCF_ROW}:{c}${DEVCF_ROW})" for c in ALLC[:ND + 8]) + "))", "USDm", "n2", out=True); r += 1
note(ws, r + 1, "Reading: the risk-weighted NPV answers whether a developer should start; the success-path IRR and multiple answer what the developer earns if it closes; the step-ups show where value is created between close and COD. Promotes and carried interest are not modelled.")
DEV_TOT_ROW = TOT_ROW

# ===================================================================================
# 05A CONTRACTING — EPC structure, risk premium and owner's share of overruns
# ===================================================================================
ws = WS["05A_CONTRACTING"]
title(ws, "05A CONTRACTING — Who carries construction risk, and at what price",
      "Indicative parameters for comparing structures; replace with bids. Geological risk usually stays with the owner whatever the label.")
ws.column_dimensions["D"].width = 14
for j in range(3):
    ws.column_dimensions[L(5 + j)].width = 16
r = 4
inp(ws, r, "epc_struct", "Contracting structure (1=turnkey lump-sum EPC, 2=split civil + E&M packages, 3=multi-contract, owner integrates)", 2, "1-3", "", "int", True); r += 1
r += 1
for j, h in enumerate(["Parameter", "Unit", "SELECTED", "", "1 Turnkey EPC", "2 Split packages", "3 Multi-contract"]):
    c = ws.cell(r, 1 + j, h); c.font = F_HDR; c.fill = FILL_HDR
r += 1
EPC = [("epc_prem", "Contractor risk premium on civil, HM and E&M prices", "%", [0.12, 0.06, 0.0], "pct"),
       ("epc_owner", "Share of a cost overrun borne by the owner", "%", [0.30, 0.55, 0.90], "pct"),
       ("epc_owner_d", "Share of delay cost borne by the owner (after liquidated damages)", "%", [0.35, 0.60, 0.90], "pct"),
       ("epc_interface", "Interface risk (qualitative, 1 low to 3 high)", "1-3", [1, 2, 3], "int")]
for nm, lab, u, vals, f in EPC:
    ws.cell(r, 1, lab).font = F_BASE; ws.cell(r, 2, u).font = F_BASE
    for j, v in enumerate(vals):
        c = ws.cell(r, 5 + j, v); c.font = F_INPUT; c.fill = FILL_INPUT; c.border = BOX; c.number_format = FMT[f]
    put(ws, f"C{r}", f"=INDEX(E{r}:G{r},{{epc_struct}})", f)
    REF[nm] = f"{q(ws.title)}!$C${r}"
    r += 1
r += 1
note(ws, r, "Turnkey EPC buys price and date certainty at a premium, but unforeseen ground conditions are often excluded or capped; FIDIC's Emerald Book (2019) allocates subsurface risk through a geotechnical baseline report. Multi-contracting is cheaper on paper and leaves interface and overrun risk with the owner.")

# ===================================================================================
# 30A CLOSE READINESS — financial close gates (evidence first), Go / Conditional Go / Stop
# ===================================================================================
ws = WS["30A_CLOSE_READINESS"]
title(ws, "30A FINANCIAL CLOSE READINESS — 23 gates, evidence first",
      "Status: MET / PARTIAL / NOT MET / NO EVIDENCE. Model tests are automatic. STOP if a critical gate is NOT MET or has NO EVIDENCE; CONDITIONAL GO if every critical gate is MET; GO only if all gates are MET. Not a recommendation.")
for col, w in zip("ABCDEFG", [6, 44, 16, 10, 16, 18, 48]):
    ws.column_dimensions[col].width = w
for j, h in enumerate(["#", "Gate", "Area", "Critical", "Evidence status (input)", "Status used", "Evidence / model test"]):
    c = ws.cell(4, 1 + j, h); c.font = F_HDR; c.fill = FILL_HDR
GATES_FC = [
    ("Flow record of at least 15 years and independent hydrology review", "Resource", "Y", None, "AND({rec_years}>=15,{hyd_study}=3)"),
    ("P90 energy confirmed by the lenders' technical adviser", "Resource", "Y", "PARTIAL", None),
    ("Bankable feasibility study signed off by the lenders' technical adviser", "Design", "Y", None, "{fs_level}=3"),
    ("Geotechnical investigation sufficient for a baseline report", "Design", "Y", "PARTIAL", None),
    ("ESIA approved and compliant with lender standards", "E&S", "Y", None, "{es_level}=3"),
    ("Resettlement action plan approved and funded", "E&S", "Y", None, "{rap_level}>=2"),
    ("Generation licence and water-use permit granted", "Permits", "Y", "PARTIAL", None),
    ("Land rights secured for all project areas", "Permits", "Y", "NOT MET", None),
    ("PPA signed and approved by the regulator", "Revenue", "Y", "PARTIAL", None),
    ("Implementation or concession agreement signed", "Revenue", "Y", "PARTIAL", None),
    ("Grid connection agreement signed and transmission financed", "Grid", "Y", None, "{tx_fin}=1"),
    ("Transmission in service no later than plant COD", "Grid", "N", None, "{tx_gap_yrs}<=0"),
    ("EPC contract(s) signed with fixed price, completion date and LDs", "Construction", "Y", "PARTIAL", None),
    ("O&M arrangements and owner's team in place", "Operations", "N", "PARTIAL", None),
    ("Payment security of at least 6 months in place", "Offtaker", "Y", None, "{lc_months}>=6"),
    ("Offtaker payment capacity at least 1.2x the PPA bill (worst of first 10 years)", "Offtaker", "Y", None, "{ut_ratio10}>=1.2"),
    ("Financing plan fully committed (no financing gap)", "Finance", "Y", None, "{fin_gap}<=0.5"),
    ("Minimum DSCR at or above the sizing target in the base case", "Finance", "Y", None, "{kpi_min_dscr}>={str_dscr}"),
    ("Equity commitments signed and equity IRR at or above target", "Finance", "Y", None, "IF(ISNUMBER({kpi_eirr}),{kpi_eirr}>={str_hurdle},{s_priv}<=0)"),
    ("Political risk cover or guarantees signed", "Risk", "N", "NO EVIDENCE", None),
    ("Government support approved by the finance ministry; fiscal screen not HIGH", "Public finance", "Y", None, "LEFT({sc_result},4)<>\"HIGH\""),
    ("Insurance programme placed (construction all risks, DSU)", "Risk", "N", "PARTIAL", None),
    ("Independent model audit completed", "Finance", "N", "NO EVIDENCE", None),
]
r = 5
G0 = r
FQ = ["Q1 Technically viable", "Q2 Developable", "Q3 Economic for the system", "Q4 Investable for the developer",
      "Q5 Bankable", "Q6 Buildable on budget", "Q7 Affordable for buyer and state", "Q8 Ready to close"]
FQ_WHO = ["Developer, lenders", "Developer, state", "State", "Developer", "Lenders", "Developer, lenders", "State", "Developer, lenders, state"]
GATE_Q = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 5, 5, 6, 6, 4, 4, 3, 4, 6, 5, 4]  # framework question of each gate
for col, w in zip("HI", [32, 24]):
    ws.column_dimensions[col].width = w
for j, h in enumerate(["Framework question", "Must be accepted by"]):
    c = ws.cell(4, 8 + j, h); c.font = F_HDR; c.fill = FILL_HDR
for k, (lab, area, crit, ev, test) in enumerate(GATES_FC):
    ws.cell(r, 8, FQ[GATE_Q[k]]).font = F_BASE; ws.cell(r, 9, FQ_WHO[GATE_Q[k]]).font = F_BASE
    ws.cell(r, 1, k + 1).font = F_BASE
    ws.cell(r, 2, lab).font = F_BASE; ws.cell(r, 3, area).font = F_BASE
    c = ws.cell(r, 4, crit); c.font = F_INPUT
    if test is None:
        c = ws.cell(r, 5, ev); c.font = F_INPUT; c.fill = FILL_INPUT; c.border = BOX
        put(ws, f"F{r}", f"=E{r}")
        ws.cell(r, 7, "Evidence file (document reference to be entered)").font = F_BASE
    else:
        ws.cell(r, 5, "model test").font = Font(name=ARIAL, size=9, italic=True, color="595959")
        put(ws, f"F{r}", f'=IF({test},"MET","NOT MET")')
        ws.cell(r, 7, "Automatic: " + test.replace("{", "").replace("}", "")).font = Font(name=ARIAL, size=9, color="595959")
    r += 1
G1 = r - 1
dv_list(ws, f"E{G0}:E{G1}", ["MET", "PARTIAL", "NOT MET", "NO EVIDENCE"])
for val, col in [("MET", "C6EFCE"), ("PARTIAL", "FFEB9C"), ("NOT MET", "FF7C80"), ("NO EVIDENCE", "D9D9D9")]:
    ws.conditional_formatting.add(f"F{G0}:F{G1}", CellIsRule(operator="equal", formula=[f'"{val}"'], fill=PatternFill("solid", fgColor=col)))
r += 1
calc(ws, r, "fc_met", "Gates met", f'=COUNTIF(F{G0}:F{G1},"MET")', "#", "int", out=True); r += 1
calc(ws, r, "fc_n", "Gates", f"=ROWS(F{G0}:F{G1})", "#", "int"); r += 1
calc(ws, r, "fc_crit_fail", "Critical gates NOT MET", f'=COUNTIFS(D{G0}:D{G1},"Y",F{G0}:F{G1},"NOT MET")', "#", "int", out=True); r += 1
calc(ws, r, "fc_crit_noev", "Critical gates with NO EVIDENCE", f'=COUNTIFS(D{G0}:D{G1},"Y",F{G0}:F{G1},"NO EVIDENCE")', "#", "int"); r += 1
calc(ws, r, "fc_crit_part", "Critical gates PARTIAL", f'=COUNTIFS(D{G0}:D{G1},"Y",F{G0}:F{G1},"PARTIAL")', "#", "int"); r += 1
calc(ws, r, "fc_decision", "FINANCIAL CLOSE DECISION",
     '=IF({fc_crit_fail}>0,"STOP: a critical gate is not met",IF({fc_crit_noev}>0,"STOP: critical evidence missing",IF({fc_crit_part}>0,"NOT READY: critical gates partly met",IF({fc_met}={fc_n},"GO: evidence complete for a close decision","CONDITIONAL GO: all critical gates met"))))', "", None, out=True); r += 1
note(ws, r + 1, "A GO says the evidence file is complete for lenders and sponsors to decide. It is not an investment recommendation.")
r += 3
section(ws, r, "HYDRO READINESS FRAMEWORK: eight questions, 23 gates, one close decision"); r += 1
for j, h in enumerate(["Question", "Must be accepted by", "Gates", "Met", "Critical not met or no evidence"]):
    c = ws.cell(r, 2 + j, h); c.font = F_HDR; c.fill = FILL_HDR
r += 1
for qi, qn in enumerate(FQ[:7]):
    ws.cell(r, 2, qn).font = F_BASE; ws.cell(r, 3, FQ_WHO[qi]).font = F_BASE
    put(ws, f"D{r}", f'=COUNTIF(H{G0}:H{G1},B{r})', "int")
    put(ws, f"E{r}", f'=COUNTIFS(H{G0}:H{G1},B{r},F{G0}:F{G1},"MET")', "int")
    put(ws, f"F{r}", f'=COUNTIFS(H{G0}:H{G1},B{r},D{G0}:D{G1},"Y",F{G0}:F{G1},"NOT MET")+COUNTIFS(H{G0}:H{G1},B{r},D{G0}:D{G1},"Y",F{G0}:F{G1},"NO EVIDENCE")', "int")
    r += 1
ws.cell(r, 2, FQ[7]).font = F_BOLD; ws.cell(r, 3, FQ_WHO[7]).font = F_BASE
put(ws, f"D{r}", "={fc_n}", "int"); put(ws, f"E{r}", "={fc_met}", "int"); put(ws, f"F{r}", "={fc_crit_fail}+{fc_crit_noev}", "int")

# ===================================================================================
# 32 DASHBOARD
# ===================================================================================
ws = WS["32_DASHBOARD"]
title(ws, "32 DASHBOARD — Can this project deliver bankable power without unsustainable public liabilities?", "")
ws.column_dimensions["A"].width = 44; ws.column_dimensions["B"].width = 18; ws.column_dimensions["C"].width = 4
ws.column_dimensions["D"].width = 44; ws.column_dimensions["E"].width = 18; ws.column_dimensions["F"].width = 4
ws.column_dimensions["G"].width = 40; ws.column_dimensions["H"].width = 22
put(ws, "A3", '="Project: "&{proj_name}&"  |  Structure: "&{str_name}&"  |  Case: "&CHOOSE({case},"Base","Low","High")&"  |  Active stresses: "&SUM({st_drought},{st_capex},{st_delay},{st_demand},{st_offtaker},{st_fx},{st_rate},{st_trans},{st_climate})', font=F_BOLD)
put(ws, "A4", '="VERDICT: "&{bk_overall}&"   |   FISCAL SCREEN: "&{sc_result}', font=Font(name=ARIAL, size=11, bold=True, color="C00000"))
def kpi_block(col_lab, col_val, r0, head, items):
    c = ws[f"{col_lab}{r0}"]; c.value = head; c.font = F_HDR; c.fill = FILL_HDR
    ws[f"{col_val}{r0}"].fill = FILL_HDR
    rr = r0 + 1
    for lab, tpl, f in items:
        ws[f"{col_lab}{rr}"] = lab; ws[f"{col_lab}{rr}"].font = F_BASE
        put(ws, f"{col_val}{rr}", tpl, f)
        ws[f"{col_val}{rr}"].border = BOX
        rr += 1
    return rr
kpi_block("A", "B", 6, "PROJECT STATUS", [
    ("Installed capacity (MW)", "={inst_mw}", "mw"), ("P50 generation (GWh/yr)", "={p50}", "gwh"),
    ("Capacity factor (P50)", "={cf}", "pct"), ("Plant CAPEX real 2026 (USDm)", "={capex_real}", "m"),
    ("Unit CAPEX (USD/kW, base)", "={capex_kw}", "m0"), ("COD", "={cod_year}", "yr"),
    ("Blended PPA tariff, op yr 2 (USD/MWh)", "=SUMPRODUCT(([RNG:opyr]=2)*[RNG:blend])", "n2"),
    ("LCOE plant (USD/MWh)", "={lcoe}", "n2"), ("LCOE delivered system (USD/MWh)", "={lcoe_sys}", "n2")])
kpi_block("D", "E", 6, "FINANCIAL", [
    ("Project IRR", "={kpi_pirr}", "pct"), ("Private equity IRR", "={kpi_eirr}", "pct"),
    ("Project NPV (USDm)", "={kpi_npv}", "m"), ("Minimum DSCR", "={kpi_min_dscr}", "x"),
    ("Average DSCR", "={kpi_avg_dscr}", "x"), ("LLCR", "={kpi_llcr}", "x"),
    ("Senior debt capacity (USDm)", "={debt_cap}", "m"), ("Senior debt raised (USDm)", "={debt_c}+{debt_m}", "m"),
    ("Financing gap (USDm)", "={fin_gap}", "m")])
kpi_block("G", "H", 6, "DEVELOPER", [
    ("Development budget (USDm, real)", "={dev_total}", "n2"), ("Development period (years)", "={dev_years}", "n2"),
    ("Probability of reaching close", "={dev_pfc}", "pct"), ("Risk-weighted developer NPV (USDm)", "={dev_enpv}", "n2"),
    ("Developer IRR, success path", "={dev_irr}", "pct"), ("Developer cash multiple", "={dev_mult}", "x"),
    ("Break-even development premium (% CAPEX)", "={dev_be_prem_pct}", "pct"), ("Equity step-up close to COD (USDm)", "={val_step_cod}", "n2"),
    ("Financial close decision", "={fc_decision}", None)])
kpi_block("A", "B", 17, "POWER SYSTEM", [
    ("Transmission readiness gap (years)", "={tx_gap_yrs}", "int"), ("Evacuation capacity at COD (MW)", "={evac_cod}", "m0"),
    ("Project share of system peak at COD", "={share_cod}", "pct"), ("Bankable/contracted demand (worst yr 1-5)", "={dem_ratio5}", "x"),
    ("Lifetime curtailment (GWh)", "=[C:curt_tx]+[C:curt_dem]", "gwh"), ("Deemed energy paid (GWh)", "=[C:deemed]", "gwh")])
kpi_block("D", "E", 17, "UTILITY", [
    ("Utility EBITDA op yr 2 (USDm)", "=SUMPRODUCT(([RNG:opyr]=2)*[RNG:u_ebitda])", "m"),
    ("Collection rate", "={ut_coll}+{eff_coll_adj}", "pct"),
    ("Receivable days op yr 2", "=SUMPRODUCT(([RNG:opyr]=2)*[RNG:u_recd])", "int"),
    ("Payment capacity / PPA (worst yr 1-10)", "={ut_ratio10}", "x"),
    ("Lifetime offtaker payment gap (USDm)", "=[C:u_gap]", "m"), ("Unpaid arrears to IPP (USDm)", "=[C:unpaid]", "m")])
kpi_block("A", "B", 25, "PUBLIC FINANCE", [
    ("Government upfront contribution (USDm)", "=[C:g_eq]+[C:g_grant]+[C:g_tx]", "m"),
    ("Peak contingent exposure (USDm)", "={cl_peak}", "m"), ("PV expected loss (USDm, user probs)", "={cl_pv_el}", "m"),
    ("Fiscal NPV, central government (USDm)", "={fis_npv}", "m"), ("Consolidated fiscal NPV incl. utility (USDm)", "={fis_npv_cons}", "m"),
    ("Peak annual cash need / revenue", "={fis_peak_rev}", "pct2"),
    ("Peak contingent exposure / GDP", "={sc_cl}", "pct2"), ("Screening result", "={sc_result}", None)])
c = ws["D25"]; c.value = "BANKABILITY GATES"; c.font = F_HDR; c.fill = FILL_HDR; ws["E25"].fill = FILL_HDR
rr = 26
for gid in gid_list:
    gr, gname = GATE_ROWS[gid]
    ws[f"D{rr}"] = gname; ws[f"D{rr}"].font = F_BASE
    put(ws, f"E{rr}", f"={{{gid}_status}}")
    ws[f"E{rr}"].border = BOX
    rr += 1
ws.conditional_formatting.add("E26:E34", CellIsRule(operator="equal", formula=['"READY"'], fill=PatternFill("solid", fgColor="C6EFCE")))
ws.conditional_formatting.add("E26:E34", CellIsRule(operator="equal", formula=['"CONDITIONAL"'], fill=PatternFill("solid", fgColor="FFEB9C")))
ws.conditional_formatting.add("E26:E34", CellIsRule(operator="equal", formula=['"DEVELOPMENT GAP"'], fill=PatternFill("solid", fgColor="F8CBAD")))
ws.conditional_formatting.add("E26:E34", CellIsRule(operator="equal", formula=['"CRITICAL GAP"'], fill=PatternFill("solid", fgColor="FF7C80")))
c = ws["A37"]; c.value = "TOP 5 BANKABILITY GAPS"; c.font = F_HDR; c.fill = FILL_HDR; ws["B37"].fill = FILL_HDR
c = ws["D37"]; c.value = "TOP 5 ACTIONS BEFORE FINANCIAL CLOSE"; c.font = F_HDR; c.fill = FILL_HDR
for cc in "EFGH":
    ws[f"{cc}37"].fill = FILL_HDR
for k in range(1, 6):
    rr = 37 + k
    m = f"MATCH(SMALL({{gate_keys}},{k}),{{gate_keys}},0)"
    put(ws, f"A{rr}", f'="{k}. "&INDEX({{gate_names}},{m})')
    put(ws, f"B{rr}", f"=INDEX({{gate_status}},{m})")
    put(ws, f"D{rr}", f'="{k}. "&INDEX({{gate_actions}},{m})')
ws.conditional_formatting.add("B38:B42", CellIsRule(operator="equal", formula=['"READY"'], fill=PatternFill("solid", fgColor="C6EFCE")))
ws.conditional_formatting.add("B38:B42", CellIsRule(operator="equal", formula=['"CONDITIONAL"'], fill=PatternFill("solid", fgColor="FFEB9C")))
ws.conditional_formatting.add("B38:B42", CellIsRule(operator="equal", formula=['"DEVELOPMENT GAP"'], fill=PatternFill("solid", fgColor="F8CBAD")))
ws.conditional_formatting.add("B38:B42", CellIsRule(operator="equal", formula=['"CRITICAL GAP"'], fill=PatternFill("solid", fgColor="FF7C80")))

# ===================================================================================
# 33 CHECKS
# ===================================================================================
ws = WS["33_CHECKS"]
title(ws, "33 CHECKS — Model integrity", "All checks should read OK")
CHECKS = [
    ("Sources = uses", "=IF(ABS({sources}-{uses})<0.01,\"OK\",\"ERROR\")"),
    ("Construction funding balances every year", "=IF(ABS(SUM([RNG:use_t])-SUM([RNG:grant_t])-SUM([RNG:debt_t])-SUM([RNG:eq_t]))<0.01,\"OK\",\"ERROR\")"),
    ("CAPEX phasing sums to 100%", "=IF(ABS([C:share]-1)<0.0001,\"OK\",\"ERROR\")"),
    ("Concessional debt fully repaid by end of term", f"=IF(ABS({q('18_DEBT')}!${LASTC}${{c_close_row}})<0.01,\"OK\",\"ERROR\")"),
    ("Commercial debt fully repaid by end of term", f"=IF(ABS({q('18_DEBT')}!${LASTC}${{m_close_row}})<0.01,\"OK\",\"ERROR\")"),
    ("Concessional repayment within concession", "=IF({str_gc}+{str_nc}<={ops_years},\"OK\",\"ERROR\")"),
    ("Commercial tenor within concession", "=IF({str_nm}<={ops_years},\"OK\",\"ERROR\")"),
    ("Timeline fits model horizon", f"=IF({{cons_eff}}+{{ops_years}}<={N},\"OK\",\"ERROR\")"),
    ("Energy chain: delivered ≤ generation", "=IF([C:delivered]<=[C:gen]+0.001,\"OK\",\"ERROR\")"),
    ("Unpaid amounts non-negative", "=IF(MIN([RNG:unpaid])>=-0.001,\"OK\",\"ERROR\")"),
    ("Commercial debt: no forced balloon in final year", "=IF(SUMPRODUCT(([RNG:opyr]={str_nm})*([RNG:m_prin]-([RNG:m_target]-[RNG:m_int])))<0.5,\"OK\",\"WARNING\")"),
    ("DSRA balance never negative", "=IF(MIN([RNG:dsra_act])>=-0.001,\"OK\",\"ERROR\")"),
    ("Project-funded transmission fully funded (construction + CFADS)", "=IF(ABS([C:tx_spend_prj]-{u_tx}-SUMPRODUCT([RNG:tx_spend_prj],[RNG:opflag]))<0.01,\"OK\",\"ERROR\")"),
    ("Structure check", "=IF(LEFT(" + "'17A_STRUCTURES'!$C${strchk}" + ",2)=\"OK\",\"OK\",\"WARNING\")"),
]
r = 4
chk_first = r
for lab, f in CHECKS:
    ws.cell(r, 1, lab).font = F_BASE
    put(ws, f"C{r}", f)
    r += 1
chk_last = r - 1
calc(ws, r + 1, "chk_all", "ALL CHECKS", f'=IF(COUNTIF(C{chk_first}:C{chk_last},"OK")={chk_last-chk_first+1},"ALL OK",COUNTIF(C{chk_first}:C{chk_last},"<>OK")&" issue(s)")', "", None, out=True)
REF["c_close_row"] = str(TSROW["c_close"][1])
REF["eqp_row"] = str(TSROW["eq_priv_cf"][1]); REF["opf_row"] = str(TSROW["opflag"][1]); REF["lc_row"] = str(TSROW["lastcons"][1])
REF["m_close_row"] = str(TSROW["m_close"][1])
REF["strchk"] = str(STR_LAST + 1)
ws.conditional_formatting.add(f"C{chk_first}:C{chk_last+2}", CellIsRule(operator="equal", formula=['"OK"'], fill=PatternFill("solid", fgColor="C6EFCE")))
ws.conditional_formatting.add(f"C{chk_first}:C{chk_last+2}", CellIsRule(operator="equal", formula=['"ALL OK"'], fill=PatternFill("solid", fgColor="C6EFCE")))
ws.conditional_formatting.add(f"C{chk_first}:C{chk_last+2}", CellIsRule(operator="equal", formula=['"ERROR"'], fill=PatternFill("solid", fgColor="FF7C80")))

# ===================================================================================
# 00 README
# ===================================================================================
ws = WS["00_README"]
title(ws, "MODEL 7 — Hydropower Development and Finance Model (v1.1)",
      "Can this project deliver bankable power WITHOUT creating unsustainable public liabilities?")
ws.column_dimensions["A"].width = 30; ws.column_dimensions["B"].width = 110
lines = [
    ("Purpose", "One integrated engine linking HYDRO RESOURCE → PLANT → TRANSMISSION → GRID → DEMAND → UTILITY → REGULATION → PPA → FINANCE → PPP/IPP → GOVERNMENT SUPPORT → FISCAL EXPOSURE → BANKABILITY."),
    ("Core philosophy", "Technical feasibility is not financial bankability. Financial bankability is not sustainable public finance."),
    ("Reference project", "Kasiri River Hydro (60 MW run-of-river IPP), Republic of Navaria, ENTIRELY FICTIONAL. Companion to Book 7, Hydropower Development and Finance. All inputs are illustrative and must be replaced with project data."),
    ("Users", "Developer, investor, lender, Ministry of Finance / PPP unit, utility, DFI, transaction adviser — same engine, different read-outs (see User Manual)."),
    ("How to use", "1) Set case/structure/stresses on 01_CONTROL_PANEL. 2) Replace blue inputs on sheets 02-17A, 21-26. 3) Read 32_DASHBOARD and 30_BANKABILITY. 4) Check 33_CHECKS = ALL OK."),
    ("Colour code", "Blue font = hard-coded input; yellow fill = key lever; black = formula; green = link to another sheet; green-shaded cell = key output."),
    ("Units", "USD million nominal unless stated; energy GWh; capacity MW; real inputs in 2026 USD."),
    ("Timeline", "Annual, 40 periods from model start year. Construction + concession must fit within 40 years (checked)."),
    ("Circularity", "None. IDC, fees and DSRA are equity-funded; commercial debt is sculpted on a lender-case CFADS with unlevered tax. Documented simplifications."),
    ("Scenarios", "Three exclusive cases (Base/Low/High) + nine combinable stress toggles + five sensitivity flexes. Full-engine snapshots: python tools/run_snapshots.py."),
    ("Structures", "Five structures on 17A_STRUCTURES evaluated by the full engine (select on control panel) and by a live closed-form comparison."),
    ("Bankability", "Nine-gate weakest-link framework with explicit thresholds (30_BANKABILITY). No hidden weights."),
    ("Fiscal screening", "26 is a PROJECT-LEVEL FISCAL EXPOSURE SCREENING. It does not replace IMF/World Bank debt sustainability analysis."),
    ("Limitations", "Simplified utility model; normal-approximation P-values; proportional curtailment; annual periodicity; deterministic guarantee calls; user-judgement probabilities. Not investment, legal or tax advice."),
    ("Sources", "See research/source_database.md and research/case_studies/. Benchmark placeholders are labelled; replace with verified values before use."),
    ("Sheet map", "00 README | 01 Control | 02-07 Project | 08-10 Power system | 11-12 Offtaker/utility | 13-16 Regulation, PPA, tariff, revenue | 17-21 Finance | 22-26 Public finance | 27-28 Scenarios/sensitivity | 29-30 Risk & bankability | 31 Case study | 32 Dashboard | 33 Checks"),
]
r = 4
for k, v in lines:
    ws.cell(r, 1, k).font = F_BOLD
    c = ws.cell(r, 2, v); c.font = F_BASE; c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 30
    r += 1

# ===================================================================================
# CHARTS (dashboard)
# ===================================================================================
def add_line(ws_dash, anchor, ttl, series, ylab):
    ch = LineChart(); ch.title = ttl; ch.y_axis.title = ylab; ch.height = 7; ch.width = 16
    for nm, lab in series:
        s, rr = TSROW[nm]
        ref = Reference(WS[s], min_col=C0, max_col=C0 + N - 1, min_row=rr, max_row=rr)
        ch.add_data(ref, from_rows=True, titles_from_data=False)
        ch.series[-1].tx = None
    from openpyxl.chart.series import SeriesLabel
    for i, (nm, lab) in enumerate(series):
        ch.series[i].tx = SeriesLabel(v=lab)
    yr_s, yr_r = TSROW["year"]
    ch.set_categories(Reference(WS[yr_s], min_col=C0, max_col=C0 + N - 1, min_row=yr_r, max_row=yr_r))
    ws_dash.add_chart(ch, anchor)

dash = WS["32_DASHBOARD"]
add_line(dash, "J3", "Energy: generation vs delivered (GWh)", [("gen", "Generation"), ("delivered", "Delivered"), ("gen_p50", "P50")], "GWh")
add_line(dash, "J18", "Utility: PPA payment vs payment capacity (USDm)", [("u_ppa", "PPA billed (utility)"), ("u_maxppa", "Max sustainable")], "USDm")
add_line(dash, "J33", "Government: net fiscal cash flow & contingent exposure (USDm)", [("f_net", "Net fiscal cash flow"), ("cl_max", "Max contingent exposure")], "USDm")
add_line(dash, "T3", "Debt service vs CFADS (USDm)", [("cfads", "CFADS"), ("ds", "Debt service")], "USDm")

finalize()
for s in SHEETS:
    WS[s].sheet_properties.tabColor = {"0": "1F3864", "1": "2F5597", "2": "548235", "3": "C00000"}.get(s[0], "7F7F7F")
wb.save(OUT)
import json
json.dump({"REF": REF, "TSROW": TSROW, "CMP_ROWS": cmp_rows, "SCEN_SNAP_ROW": SCEN_SNAP_ROW, "CMP_SNAP": CMP_SNAP, "SENS_SNAP_ROW": SENS_SNAP_ROW, "CASE_ROW0": CASE_ROW0},
          open("model/model_map.json", "w"), indent=1)
print("saved", OUT, "formulas:", len(PENDING))
