"""Build Volume 2 - SHS / PAYGo Company Financial & Investment Model.

Run:  python tools/build_shs_model.py [--snapshot]
Out:  volumes/02-solar-home-systems/model/AEF_SHS_PAYGo_Model_<VERSION>.xlsx

--snapshot  also fills the static 'Sensitivity' sheet using the verified Python twin
            (tools/shadow_shs.py). Without it the sheet is left empty.

All default inputs live in tools/shs_defaults.py and are ILLUSTRATIVE placeholders
for a fictional company in a fictional market ("LCY" = local currency).
"""

import sys
from datetime import date
from pathlib import Path

from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter as gcl
from openpyxl.workbook.properties import CalcProperties
from openpyxl.worksheet.datavalidation import DataValidation

from aef_engine import (BLUE, FMT_DATE, FMT_INT, FMT_NUM, FMT_NUM2, FMT_PCT, FMT_X, FONT, GREEN, NAVY,
                        ModelBook, col, header_row, label, put_calc, put_input, q, set_font_all)
from shs_defaults import GENERAL as G
from shs_defaults import MAX_AGE, MONTHS, MTF_CAPACITY, PRODUCTS, SCENARIOS

VERSION = "v0.2"
YEARS = MONTHS // 12
NP = len(PRODUCTS)
PCOLS = [gcl(3 + j) for j in range(NP)]  # C..G on Products / Unit_Economics
OUT = (Path(__file__).resolve().parents[1] / "volumes/02-solar-home-systems/model"
       / f"AEF_SHS_PAYGo_Model_{VERSION}.xlsx")
ILLUS = "Illustrative placeholder - replace with company data."
GREY_TXT = "595959"

mb = ModelBook(MONTHS)
wb = mb.wb
INP = {}


def absref(ws, cell):
    c = cell.rstrip("0123456789")
    return f"{q(ws.title)}!${c}${cell[len(c):]}"


def note(ws, cell, text):
    label(ws, cell, text, size=9, italic=True, color=GREY_TXT)


def year_header(ws, row=5, with_y0=False):
    for y in range(0 if with_y0 else 1, YEARS + 1):
        c = col(y) if y else "D"
        ws[f"{c}{row}"] = f"Year {y}"
        ws[f"{c}{row + 1}"] = y
        for rr in (row, row + 1):
            ws[f"{c}{rr}"].font = Font(name=FONT, bold=True, color="FFFFFF")
            ws[f"{c}{rr}"].fill = PatternFill("solid", fgColor=NAVY)
            ws[f"{c}{rr}"].alignment = Alignment(horizontal="right")
        ws.column_dimensions[c].width = 16
    ws.freeze_panes = f"{col(1)}7"


# =====================================================================
# COVER & SUMMARY (created first for sheet order; filled at the end)
# =====================================================================
cov = mb.sheet("Cover", "AFRICA ENERGY FINANCE  |  Business & Financial Models",
               "Volume 2 - Solar Home Systems  |  PAYGo Company Financial & Investment Model", tab=NAVY)
inv_ws = mb.sheet("Investment_Summary", "Investment summary",
                  "One-page view for investment committees and lenders. Active scenario, LCY unless stated.", tab="00B050")

# =====================================================================
# INPUTS
# =====================================================================
ws = mb.sheet("Inputs", "Inputs", "Blue = input. Yellow = key assumption to review first. All defaults illustrative.",
              tab="0000FF")
ws.column_dimensions["A"].width = 58
ws.column_dimensions["C"].width = 18
ws.column_dimensions["D"].width = 70


def add_input(key, row, text, unit, value, fmt=FMT_NUM, keyflag=False, n=ILLUS):
    label(ws, f"A{row}", text)
    label(ws, f"B{row}", unit, size=9, color=GREY_TXT)
    put_input(ws, f"C{row}", value, fmt, keyflag)
    if n:
        note(ws, f"D{row}", n)
    INP[key] = absref(ws, f"C{row}")


r = 4
mb.section(ws, r, "Scenario & settings"); r += 1
add_input("scenario", r, "Active scenario (1 = Base, 2 = Downside, 3 = Severe)", "#", G["scenario"], FMT_INT, True,
          "Drives the levers on the Scenarios sheet.")
dv = DataValidation(type="whole", operator="between", formula1="1", formula2="3")
ws.add_data_validation(dv); dv.add(f"C{r}"); r += 1
add_input("start", r, "First model month (period end)", "date", None, FMT_DATE, False, "Period-end date of month 1.")
ws[f"C{r}"] = "=DATE(2027,1,31)"; ws[f"C{r}"].font = Font(name=FONT, color=BLUE); r += 1
add_input("currency", r, "Local currency label", "text", "LCY", "@", False, "Display only."); r += 2

mb.section(ws, r, "Macro"); r += 1
add_input("fx0", r, "Opening FX rate", "LCY per USD", G["fx0"], FMT_NUM2, True); r += 1
add_input("infl", r, "Local inflation (opex indexation)", "% p.a.", G["infl"], FMT_PCT); r += 1
add_input("tax", r, "Corporate income tax rate", "%", G["tax"], FMT_PCT, False,
          "Simplified: unlimited loss carry-forward, tax paid in the month it arises."); r += 1
add_input("price_g", r, "Annual price increase on NEW PAYGo contracts", "% p.a.", G["price_g"], FMT_PCT, True,
          "Existing contracts keep their price plan."); r += 1
add_input("fx_pass", r, "Pass-through of LCY depreciation into new-contract prices", "%", G["fx_pass"], FMT_PCT, True,
          "Share of cumulative FX depreciation passed into prices of NEW contracts (0% = none, 100% = USD-indexed)."); r += 2

mb.section(ws, r, "Sales volume - all tiers (Base, before scenario multiplier; split by Products mix)"); r += 1
for y in range(1, YEARS + 1):
    add_input(f"vol{y}", r, f"Units sold - Year {y}", "units", G["vols"][y - 1], FMT_NUM, y == 1); r += 1
r += 1

mb.section(ws, r, "Operating costs"); r += 1
add_input("mm_fee", r, "Mobile-money / payment processing fees", "% of cash collected", G["mm_fee"], FMT_PCT); r += 1
add_input("cs_cost", r, "Customer service & collections cost", "LCY / active account / month", G["cs_cost"]); r += 1
add_input("staff", r, "Staff costs (fixed, month-1 level)", "LCY / month", G["staff"], FMT_NUM, True); r += 1
add_input("ga", r, "G&A, rent, IT, licences (fixed, month-1 level)", "LCY / month", G["ga"]); r += 1
add_input("duty", r, "Freight, duty & clearing on hardware", "% of USD FOB cost", G["duty"], FMT_PCT); r += 2

mb.section(ws, r, "Repossession & results-based financing (RBF)"); r += 1
add_input("repo_lag", r, "Months from default to resale of repossessed unit", "months", G["repo_lag"], FMT_INT); r += 1
add_input("rbf_on", r, "RBF programme active (1 = yes, 0 = no)", "switch", G["rbf_on"], FMT_INT, True,
          "RBF per unit is set by tier on Products. Recognised as other income when received (cash basis)."); r += 1
add_input("rbf_lag", r, "Months from sale to RBF disbursement (verification lag)", "months", G["rbf_lag"], FMT_INT); r += 2

mb.section(ws, r, "Working capital & capex"); r += 1
add_input("inv_cover", r, "Inventory cover", "months of hardware COGS", G["inv_cover"], FMT_NUM2); r += 1
add_input("ap_days", r, "Supplier credit on hardware", "days", G["ap_days"], FMT_INT); r += 1
add_input("capex", r, "Fixed capex (vehicles, IT, depots, month-1 level)", "LCY / month", G["capex"]); r += 1
add_input("dep_life", r, "Depreciation life of fixed capex", "months", G["dep_life"], FMT_INT); r += 1
add_input("min_cash", r, "Minimum operating cash balance", "LCY", G["min_cash"], FMT_NUM, True,
          "Any shortfall is covered by an automatic equity top-up = funding requirement."); r += 2

mb.section(ws, r, "Financing"); r += 1
add_input("eq0", r, "Initial equity (month 1, all shareholders)", "LCY", G["eq0"], FMT_NUM, True); r += 1
add_input("tl_amt", r, "USD term loan - amount", "USD", G["tl_amt"], FMT_NUM, True); r += 1
add_input("tl_month", r, "USD term loan - drawdown month", "month #", G["tl_month"], FMT_INT); r += 1
add_input("tl_rate", r, "USD term loan - interest rate", "% p.a.", G["tl_rate"], FMT_PCT); r += 1
add_input("tl_grace", r, "USD term loan - grace period after drawdown", "months", G["tl_grace"], FMT_INT); r += 1
add_input("tl_amort", r, "USD term loan - amortisation period", "months", G["tl_amort"], FMT_INT); r += 1
add_input("rf_limit", r, "Receivables facility (LCY) - limit", "LCY", G["rf_limit"], FMT_NUM, True,
          "Drawn as needed to hold minimum cash (cash sweep), capped at the borrowing base and the limit. "
          "Borrowing base = sum over tiers of advance rate x eligible receivables."); r += 1
add_input("rf_rate", r, "Receivables facility - interest rate", "% p.a.", G["rf_rate"], FMT_PCT); r += 1
add_input("rf_start", r, "Receivables facility - first available month", "month #", G["rf_start"], FMT_INT); r += 2

mb.section(ws, r, "Lender covenants (tested on Covenants sheet)"); r += 1
add_input("cov_cr", r, "Minimum trailing-3-month collection rate", "%", G["cov_cr"], FMT_PCT, True); r += 1
add_input("cov_rar", r, "Maximum receivables at risk / gross receivables", "%", G["cov_rar"], FMT_PCT, True); r += 1
add_input("cov_lev", r, "Maximum debt / book equity", "x", G["cov_lev"], FMT_X); r += 1
add_input("cov_dscr", r, "Minimum annual DSCR (years with debt service)", "x", G["cov_dscr"], FMT_X); r += 1
add_input("cov_cash", r, "Minimum liquidity: cash before equity top-up", "LCY", G["cov_cash"]); r += 2

mb.section(ws, r, "Valuation & transaction"); r += 1
add_input("wacc", r, "Discount rate for DCF (LCY, nominal)", "% p.a.", G["wacc"], FMT_PCT, True,
          "Should reflect LCY risk-free rate, country and company risk premia."); r += 1
add_input("tg", r, "Terminal growth rate (LCY, nominal)", "% p.a.", G["tg"], FMT_PCT); r += 1
add_input("inv_usd", r, "Investor ticket (part of initial equity)", "USD", G["inv_usd"], FMT_NUM, True); r += 1
add_input("pre_money", r, "Pre-money equity valuation", "USD", G["pre_money_usd"], FMT_NUM, True); r += 1
add_input("exit_method", r, "Exit valuation method (1 = EV/EBITDA, 2 = Price/Book)", "#", G["exit_method"], FMT_INT); r += 1
add_input("exit_mult", r, "Exit EV / EBITDA multiple (end of Year 5)", "x", G["exit_ebitda_mult"], FMT_X); r += 1
add_input("exit_pb", r, "Exit price / book equity multiple (end of Year 5)", "x", G["exit_pb_mult"], FMT_X); r += 1

# =====================================================================
# PRODUCTS
# =====================================================================
pw = mb.sheet("Products", "Product range & PAYGo price plans - MTF Tiers 1-5",
              "One column per tier. Tier labels follow the MTF capacity attribute only (indicative). Blue = input.",
              tab="0000FF")
pw.column_dimensions["A"].width = 54
pw.column_dimensions["B"].width = 16
for c in PCOLS:
    pw.column_dimensions[c].width = 24
NOTE_COL = gcl(3 + NP)
pw.column_dimensions[NOTE_COL].width = 60
header_row(pw, 4, ["Parameter", "Unit"] + [f"Tier {p['tier']}" for p in PRODUCTS] + ["Notes"])
PR = {}
PROW = [5]


def prod_section(text):
    mb.section(pw, PROW[0], text)
    PROW[0] += 1


def prod_input(key, text, unit, fmt, keyflag=False, n=""):
    r_ = PROW[0]
    label(pw, f"A{r_}", text)
    label(pw, f"B{r_}", unit, size=9, color=GREY_TXT)
    PR[key] = []
    for j, p in enumerate(PRODUCTS):
        put_input(pw, f"{PCOLS[j]}{r_}", p[key], fmt, keyflag)
        if fmt == "@":
            pw[f"{PCOLS[j]}{r_}"].alignment = Alignment(wrap_text=True, vertical="top")
        PR[key].append(f"Products!${PCOLS[j]}${r_}")
    note(pw, f"{NOTE_COL}{r_}", n or ILLUS)
    if fmt == "@":
        pw.row_dimensions[r_].height = 30
    PROW[0] += 1


def prod_calc(key, text, unit, fn, fmt, n=""):
    r_ = PROW[0]
    label(pw, f"A{r_}", text)
    label(pw, f"B{r_}", unit, size=9, color=GREY_TXT)
    PR[key] = [f"Products!${PCOLS[j]}${r_}" for j in range(NP)]
    for j in range(NP):
        put_calc(pw, f"{PCOLS[j]}{r_}", fn(j), fmt)
    if n:
        note(pw, f"{NOTE_COL}{r_}", n)
    PROW[0] += 1


prod_section("Product specification")
prod_input("name", "Product name", "text", "@")
prod_input("tier", "MTF capacity tier (indicative)", "tier", FMT_INT, False,
           "Capacity minimums: " + "; ".join(f"T{k} {v}" for k, v in MTF_CAPACITY.items()) + " (ESMAP MTF - verify).")
prod_input("wp", "PV array size", "Wp", FMT_NUM)
prod_input("wh", "Battery capacity", "Wh", FMT_NUM)
prod_input("loads", "Typical loads / appliances", "text", "@")
prod_input("segment", "Target customer segment", "text", "@")
prod_section("PAYGo price plan")
prod_input("price", "Cash (list) price", "LCY", FMT_NUM, True, "Price if paid upfront. Basis of hardware revenue.")
prod_input("deposit", "Down payment (deposit)", "LCY", FMT_NUM, True)
prod_input("daily", "PAYGo daily rate", "LCY / day", FMT_NUM, True)
prod_input("tenor", "PAYGo tenor", "months", FMT_INT, True, "Maximum 60 months (horizon of the curves).")
prod_section("Cost to serve & acquisition")
prod_input("hw", "Hardware FOB cost", "USD / unit", FMT_NUM, True)
prod_input("install", "Installation & last-mile logistics", "LCY / unit", FMT_NUM, False, "Indexed to local inflation.")
prod_input("comm", "Agent / installer commission per sale", "LCY / unit", FMT_NUM, False, "Indexed to local inflation.")
prod_input("mkt", "Marketing & other acquisition cost per sale", "LCY / unit", FMT_NUM, False, "Indexed to local inflation.")
prod_input("warranty", "Warranty & after-sales provision", "% of landed HW cost", FMT_PCT)
prod_input("mix", "Sales mix", "% of units", FMT_PCT, True, "Must sum to 100% (see Checks).")
prod_section("Credit risk & recovery")
prod_input("hazard", "Base monthly default hazard", "% of paying accounts / month", FMT_PCT, True,
           "Share of still-paying accounts that stop paying each month. Calibrate to the company's own cohort curves.")
prod_input("coll", "Base collection rate on paying accounts", "% of instalment", FMT_PCT, True,
           "Captures partial / late payment by accounts that keep paying.")
prod_input("repo", "Repossession rate of defaulted units", "% of defaults", FMT_PCT)
prod_input("recov", "Net resale value of repossessed unit", "% of cash price", FMT_PCT, False,
           "Net of retrieval and refurbishment. Recognised as a recovery against credit losses.")
prod_section("Subsidy & funding")
prod_input("rbf", "RBF per unit sold", "USD / unit", FMT_NUM, False, "Set to 0 for tiers outside the programme.")
prod_input("adv", "Receivables facility advance rate", "% of eligible receivables", FMT_PCT, True,
           "Lenders often apply different advance rates by product.")

prod_section("Derived price-plan metrics (do not edit)")
prod_calc("inst", "Monthly instalment (daily rate x 365/12)", "LCY / month", lambda j: f"={PR['daily'][j]}*365/12", FMT_NUM)
prod_calc("contract", "Total PAYGo contract value", "LCY", lambda j: f"={PR['deposit'][j]}+{PR['inst'][j]}*{PR['tenor'][j]}", FMT_NUM)
prod_calc("markup", "PAYGo price premium over cash price", "LCY", lambda j: f"={PR['contract'][j]}-{PR['price'][j]}", FMT_NUM)
prod_calc("markup_pct", "PAYGo premium as % of cash price", "%",
          lambda j: f"=IF({PR['price'][j]}=0,0,{PR['markup'][j]}/{PR['price'][j]})", FMT_PCT)
prod_calc("dep_pct", "Down payment as % of cash price", "%",
          lambda j: f"=IF({PR['price'][j]}=0,0,{PR['deposit'][j]}/{PR['price'][j]})", FMT_PCT)
prod_calc("financed", "Amount financed at sale (cash price - deposit)", "LCY",
          lambda j: f"={PR['price'][j]}-{PR['deposit'][j]}", FMT_NUM)
prod_calc("apr", "Implied annual financing rate (nominal APR)", "% p.a.",
          lambda j: f"=IFERROR(RATE({PR['tenor'][j]},-{PR['inst'][j]},{PR['financed'][j]})*12,0)", FMT_PCT,
          "Rate equating the financed amount with the instalment stream (consumer-protection disclosure).")
prod_calc("price_usd", "Cash price in USD at opening FX", "USD", lambda j: f"={PR['price'][j]}/{INP['fx0']}", FMT_NUM)
prod_calc("hazard_s", "Scenario monthly default hazard", "%", lambda j: f"={PR['hazard'][j]}*Scenarios!$G$6", FMT_PCT)
prod_calc("coll_s", "Scenario collection rate on paying accounts", "%",
          lambda j: f"=MIN(1,{PR['coll'][j]}*Scenarios!$G$7)", FMT_PCT)
prod_calc("landed", "Landed hardware cost at opening FX (scenario)", "LCY / unit",
          lambda j: f"={PR['hw'][j]}*(1+{INP['duty']})*{INP['fx0']}*Scenarios!$G$9", FMT_NUM)
prod_calc("cac", "Customer acquisition cost (commission + marketing)", "LCY / unit",
          lambda j: f"={PR['comm'][j]}+{PR['mkt'][j]}", FMT_NUM)
prod_calc("hw_margin", "Hardware gross margin on cash price (month 1)", "%",
          lambda j: f"=IF({PR['price'][j]}=0,0,1-({PR['landed'][j]}+{PR['install'][j]})/{PR['price'][j]})", FMT_PCT)

# =====================================================================
# SCENARIOS
# =====================================================================
sw = mb.sheet("Scenarios", "Scenario levers",
              "Multipliers / overrides on Base inputs. ACTIVE column follows the selector on Inputs.", tab="0000FF")
sw.column_dimensions["A"].width = 50
for c in "CDEFG":
    sw.column_dimensions[c].width = 14
header_row(sw, 5, ["Lever", "Unit", "Base", "Downside", "Severe", "", "ACTIVE"])
levers = [(6, "Default hazard multiplier", "x", "haz", FMT_NUM2),
          (7, "Collection-rate multiplier (paying accounts)", "x", "coll", FMT_NUM2),
          (8, "Sales volume multiplier", "x", "vol", FMT_NUM2),
          (9, "Hardware cost multiplier (USD)", "x", "hw", FMT_NUM2),
          (10, "LCY depreciation vs USD", "% p.a.", "dep", FMT_PCT)]
for rr, text, unit, key, fmt in levers:
    label(sw, f"A{rr}", text)
    label(sw, f"B{rr}", unit, size=9, color=GREY_TXT)
    for c, v in zip("CDE", SCENARIOS[key]):
        put_input(sw, f"{c}{rr}", v, fmt)
    put_calc(sw, f"G{rr}", f"=CHOOSE({INP['scenario']},C{rr},D{rr},E{rr})", fmt, bold=True)
label(sw, "A12", "Scenario name", bold=True)
for c, n in zip("CDE", ["Base", "Downside", "Severe"]):
    put_input(sw, f"{c}12", n, "@")
put_calc(sw, "G12", f"=CHOOSE({INP['scenario']},C12,D12,E12)", "@", bold=True)
note(sw, "A14", "Downside / Severe are illustrative stress settings. Calibrate to the company's cohort history and sector data.")
note(sw, "A15", "Context: ESMAP Off-Grid Solar Market Trends Report 2024 reports a sector PAYGo collection rate of about 62% "
     "in 2023 (source register S01, to verify).")

# =====================================================================
# TIMELINE
# =====================================================================
T = "Timeline"
tw = mb.sheet(T, "Timeline", "Dates, FX path and indices")
mb.time_header(tw)
for i in range(1, MONTHS + 1):
    c = col(i)
    tw[f"{c}4"] = i
    tw[f"{c}5"] = f"=EOMONTH({INP['start']},{i - 1})"
    tw[f"{c}6"] = f"=INT(({c}4-1)/12)+1"
    for rr, fmt in ((4, FMT_INT), (5, FMT_DATE), (6, FMT_INT)):
        tw[f"{c}{rr}"].number_format = fmt
        tw[f"{c}{rr}"].font = Font(name=FONT, bold=True, color="FFFFFF")
for key, rr in (("fx", 8), ("infl", 9), ("pidx", 10), ("vol", 11)):
    mb.register(T, key, rr)
mb.write_row(tw, 8, "FX rate", "LCY / USD", lambda i, c, p: f"={p}8*(1+Scenarios!$G$10)^(1/12)", FMT_NUM2,
             opening=f"={INP['fx0']}")
tw["D8"].font = Font(name=FONT, color=GREEN)
mb.write_row(tw, 9, "Opex inflation index", "index", lambda i, c, p: f"=(1+{INP['infl']})^(({c}$4-1)/12)", FMT_NUM2)
mb.write_row(tw, 10, "Price index on new contracts", "index",
             lambda i, c, p: f"=(1+{INP['price_g']})^(({c}$4-1)/12)*({c}$8/{INP['fx0']})^{INP['fx_pass']}", FMT_NUM2)
mb.write_row(tw, 11, "Total units sold (scenario)", "units",
             lambda i, c, p: f"=CHOOSE({c}$6,{','.join(INP[f'vol{y}'] for y in range(1, YEARS + 1))})/12*Scenarios!$G$8",
             FMT_NUM, total="sum")
TL_IDX = f"Timeline!${col(1)}$4:${mb.last}$4"
TL_YR = f"Timeline!${col(1)}$6:${mb.last}$6"
TL_FX = f"Timeline!${col(1)}$8:${mb.last}$8"

# =====================================================================
# CURVES (per unit, by account age)
# =====================================================================
CURVE_COLS = ["Survival (still paying)", "Instalment due", "Collected", "Missed (written off)", "Receivable at risk",
              "Active account", "Defaults at this age", "Recovery (resale)", "RBF received", "Net cash flow / unit",
              "Cumulative cash flow"]
CI = {k: n for n, k in enumerate(["surv", "due", "coll", "missed", "rar", "active", "defaults", "recov", "rbf", "ncf", "cum"])}
cw = mb.sheet("Curves", "Per-unit PAYGo behaviour by account age",
              "Age 0 = month of sale. Per unit, month-1 prices; cohorts are scaled by the price index. RBF at opening FX.")
AGE0 = 8
LAST_AGE = AGE0 + MAX_AGE
cw.column_dimensions["A"].width = 8
CB = []
for j in range(NP):
    start = 2 + j * (len(CURVE_COLS) + 1)
    letters = {k: gcl(start + n) for k, n in CI.items()}
    for L_ in letters.values():
        cw.column_dimensions[L_].width = 13
    CB.append(letters)
    cw.cell(5, start, PRODUCTS[j]["name"]).font = Font(name=FONT, bold=True, color=NAVY)
    header_row(cw, 6, CURVE_COLS, start_col=start)
header_row(cw, 6, ["Age (m)"], start_col=1)
cw.row_dimensions[6].height = 42
cw.freeze_panes = "B7"


def crange(j, key):
    L_ = CB[j][key]
    return f"Curves!${L_}${AGE0}:${L_}${LAST_AGE}"


for a in range(0, MAX_AGE + 1):
    rr = AGE0 + a
    put_calc(cw, f"A{rr}", a, FMT_INT)
    for j in range(NP):
        L_ = CB[j]
        Tn, inst = PR["tenor"][j], PR["inst"][j]
        inT = f"AND($A{rr}>=1,$A{rr}<={Tn})"
        put_calc(cw, f"{L_['surv']}{rr}", "=1" if a == 0 else f"=(1-{PR['hazard_s'][j]})^$A{rr}", FMT_PCT)
        put_calc(cw, f"{L_['due']}{rr}", f"=IF({inT},{inst},0)")
        put_calc(cw, f"{L_['coll']}{rr}", f"={L_['due']}{rr}*{PR['coll_s'][j]}*{L_['surv']}{rr}")
        put_calc(cw, f"{L_['missed']}{rr}", f"={L_['due']}{rr}-{L_['coll']}{rr}")
        put_calc(cw, f"{L_['rar']}{rr}", f"=(1-{L_['surv']}{rr})*MAX(0,{Tn}-$A{rr})*({inst}-{PR['markup'][j]}/{Tn})")
        put_calc(cw, f"{L_['active']}{rr}", f"=IF($A{rr}<={Tn},{L_['surv']}{rr},0)", FMT_PCT)
        put_calc(cw, f"{L_['defaults']}{rr}",
                 "=0" if a == 0 else f"=IF({inT},{L_['surv']}{rr - 1}-{L_['surv']}{rr},0)", FMT_PCT)
        put_calc(cw, f"{L_['recov']}{rr}",
                 f"=IF(AND($A{rr}-{INP['repo_lag']}>=1,$A{rr}-{INP['repo_lag']}<={Tn}),"
                 f"INDEX({crange(j, 'defaults')},$A{rr}-{INP['repo_lag']}+1),0)*{PR['repo'][j]}*{PR['recov'][j]}*{PR['price'][j]}")
        put_calc(cw, f"{L_['rbf']}{rr}", f"=IF($A{rr}={INP['rbf_lag']},{PR['rbf'][j]}*{INP['fx0']}*{INP['rbf_on']},0)")
        if a == 0:
            ncf = (f"={PR['deposit'][j]}*(1-{INP['mm_fee']})-{PR['landed'][j]}*(1+{PR['warranty'][j]})"
                   f"-{PR['install'][j]}-{PR['cac'][j]}+{L_['rbf']}{rr}")
            put_calc(cw, f"{L_['cum']}{rr}", f"={L_['ncf']}{rr}")
        else:
            ncf = (f"={L_['coll']}{rr}*(1-{INP['mm_fee']})-{INP['cs_cost']}*{L_['active']}{rr}"
                   f"+{L_['recov']}{rr}+{L_['rbf']}{rr}")
            put_calc(cw, f"{L_['cum']}{rr}", f"={L_['cum']}{rr - 1}+{L_['ncf']}{rr}")
        put_calc(cw, f"{L_['ncf']}{rr}", ncf)
SUMR = LAST_AGE + 2
label(cw, f"A{SUMR}", "Totals per unit", bold=True, color=NAVY)
CT = {k: [] for k in ("due", "coll", "missed", "recov", "rbf")}
for j in range(NP):
    for key in CT:
        L_ = CB[j][key]
        put_calc(cw, f"{L_}{SUMR}", f"=SUM({L_}{AGE0}:{L_}{LAST_AGE})", FMT_NUM, bold=True)
        CT[key].append(f"Curves!${L_}${SUMR}")

# =====================================================================
# OPS - register rows
# =====================================================================
O = "Ops"
ow = mb.sheet(O, "Operations & PAYGo portfolio", "By tier, then total. LCY unless stated.")
mb.time_header(ow)
OPS_FIELDS = [
    ("units", "Units sold", "units", "sum"),
    ("iunits", "Price-indexed units (units x price index)", "units", "sum"),
    ("deposits", "Down payments collected", "LCY", "sum"),
    ("hw_rev", "Hardware revenue (cash price)", "LCY", "sum"),
    ("financed", "New PAYGo receivables originated", "LCY", "sum"),
    ("due", "Instalments due", "LCY", "sum"),
    ("coll", "Instalments collected", "LCY", "sum"),
    ("missed", "Missed instalments written off", "LCY", "sum"),
    ("fin_inc", "PAYGo financing income (straight-line over tenor)", "LCY", "sum"),
    ("ecl", "Expected credit loss charged at origination", "LCY", "sum"),
    ("recov", "Recoveries from resale of repossessed units", "LCY", "sum"),
    ("rbf", "RBF received", "LCY", "sum"),
    ("active", "Active (paying, in-tenor) accounts", "accounts", "last"),
    ("unlocks", "Accounts reaching end of tenor (unlocked)", "accounts", "sum"),
    ("rar", "Receivables at risk (carrying amount, accounts that stopped paying)", "LCY", "last"),
    ("grossrec", "Gross PAYGo receivables (closing)", "LCY", "last"),
    ("elig", "Eligible receivables (gross - at risk)", "LCY", "last"),
    ("bb", "Borrowing-base contribution (advance rate x eligible)", "LCY", "last"),
    ("cogs", "Landed hardware cost of units sold", "LCY", "sum"),
    ("install", "Installation & logistics", "LCY", "sum"),
    ("warranty", "Warranty & after-sales provision", "LCY", "sum"),
    ("comm", "Commissions", "LCY", "sum"),
    ("mkt", "Marketing & acquisition", "LCY", "sum"),
]
rr = 8
for j in range(NP):
    mb.section(ow, rr, PRODUCTS[j]["name"])
    ow.cell(rr, 1).value = f"={PR['name'][j]}"
    rr += 1
    for key, *_ in OPS_FIELDS:
        mb.register(O, f"{key}{j}", rr)
        rr += 1
    rr += 1
mb.section(ow, rr, "TOTAL - all tiers"); rr += 1
for key, *_ in OPS_FIELDS:
    mb.register(O, f"{key}T", rr)
    rr += 1
rr += 1
for key in ("unlocks_cum", "coll_rate", "wo_rate", "rar_ratio"):
    mb.register(O, key, rr)
    rr += 1

# =====================================================================
# COHORT SHEETS
# =====================================================================
COH = [("coll", "Instalments collected by cohort (LCY)", "coll", True),
       ("active", "Active accounts by cohort", "active", False),
       ("rar", "Receivables at risk by cohort (LCY)", "rar", True),
       ("recov", "Recoveries by cohort (LCY)", "recov", True)]
for j in range(NP):
    name = f"Cohort_T{j + 1}"
    hw_ = mb.sheet(name, f"Cohort (vintage) analysis - {PRODUCTS[j]['name']}",
                   "Rows = sales cohort (month of sale); columns = calendar month. Cohort size in column C.")
    mb.time_header(hw_)
    hw_.column_dimensions["A"].width = 30
    rr = 8
    for bkey, btitle, ckey, indexed in COH:
        mb.section(hw_, rr, btitle)
        tot = rr + 1
        mb.register(name, f"{bkey}_tot", tot)
        first, last = rr + 2, rr + 1 + MONTHS
        mb.write_row(hw_, tot, "Total", "", lambda i, c, p, f=first, l=last: f"=SUM({c}{f}:{c}{l})", FMT_NUM, bold=True)
        ukey = f"iunits{j}" if indexed else f"units{j}"
        for ci in range(1, MONTHS + 1):
            r_ = first + ci - 1
            hw_.cell(r_, 1, f"Cohort month {ci}").font = Font(name=FONT, size=9)
            hw_.cell(r_, 2, ci).font = Font(name=FONT, size=9)
            put_calc(hw_, f"C{r_}", f"=INDEX({mb.range_(O, ukey)},1,$B{r_})", FMT_NUM, link=True)
            for i in range(ci + 1, MONTHS + 1):
                c = col(i)
                hw_[f"{c}{r_}"] = f"=$C{r_}*INDEX({crange(j, ckey)},{c}$4-$B{r_}+1)"
                hw_[f"{c}{r_}"].number_format = FMT_NUM
                hw_[f"{c}{r_}"].font = Font(name=FONT, size=9)
        rr = last + 2


# =====================================================================
# OPS formulas
# =====================================================================
def R(sheet, key, c, here=O):
    return mb.ref(sheet, key, c, this_sheet=here)


for j in range(NP):
    Tn = PR["tenor"][j]
    iu_rng = mb.range_(O, f"iunits{j}", this_sheet=O)
    u_rng = mb.range_(O, f"units{j}", this_sheet=O)
    coh = f"Cohort_T{j + 1}"
    S_T = f"INDEX({crange(j, 'surv')},{Tn}+1)"

    def window(c, iu_rng=iu_rng, Tn=Tn):
        return f"SUMIFS({iu_rng},{TL_IDX},\">=\"&({c}$4-{Tn}),{TL_IDX},\"<=\"&({c}$4-1))"

    rw = lambda k, j=j: mb.r(O, f"{k}{j}")
    spec = {
        "units": lambda c, p: f"=Timeline!{c}$11*{PR['mix'][j]}",
        "iunits": lambda c, p: f"={c}{rw('units')}*Timeline!{c}$10",
        "deposits": lambda c, p: f"={c}{rw('iunits')}*{PR['deposit'][j]}",
        "hw_rev": lambda c, p: f"={c}{rw('iunits')}*{PR['price'][j]}",
        "financed": lambda c, p: f"={c}{rw('iunits')}*{PR['financed'][j]}",
        "due": lambda c, p: f"={PR['inst'][j]}*{window(c)}",
        "coll": lambda c, p: f"={coh}!{c}${mb.r(coh, 'coll_tot')}",
        "missed": lambda c, p: f"={c}{rw('due')}-{c}{rw('coll')}",
        "fin_inc": lambda c, p: f"=IF({Tn}=0,0,{PR['markup'][j]}/{Tn}*{window(c)})",
        "ecl": lambda c, p: f"={c}{rw('iunits')}*{CT['missed'][j]}",
        "recov": lambda c, p: f"={coh}!{c}${mb.r(coh, 'recov_tot')}",
        "rbf": lambda c, p: (f"=IF({c}$4-{INP['rbf_lag']}>=1,INDEX({u_rng},1,{c}$4-{INP['rbf_lag']}),0)"
                             f"*{PR['rbf'][j]}*Timeline!{c}$8*{INP['rbf_on']}"),
        "active": lambda c, p: f"={coh}!{c}${mb.r(coh, 'active_tot')}",
        "unlocks": lambda c, p: f"=IF({c}$4>{Tn},INDEX({u_rng},1,{c}$4-{Tn})*{S_T},0)",
        "rar": lambda c, p: f"={coh}!{c}${mb.r(coh, 'rar_tot')}",
        "grossrec": lambda c, p: (f"={p}{rw('grossrec')}+{c}{rw('financed')}+{c}{rw('fin_inc')}"
                                  f"-{c}{rw('coll')}-{c}{rw('missed')}"),
        "elig": lambda c, p: f"=MAX(0,{c}{rw('grossrec')}-{c}{rw('rar')})",
        "bb": lambda c, p: f"={c}{rw('elig')}*{PR['adv'][j]}",
        "cogs": lambda c, p: f"={c}{rw('units')}*{PR['hw'][j]}*(1+{INP['duty']})*Timeline!{c}$8*Scenarios!$G$9",
        "install": lambda c, p: f"={c}{rw('units')}*{PR['install'][j]}*Timeline!{c}$9",
        "warranty": lambda c, p: f"={c}{rw('cogs')}*{PR['warranty'][j]}",
        "comm": lambda c, p: f"={c}{rw('units')}*{PR['comm'][j]}*Timeline!{c}$9",
        "mkt": lambda c, p: f"={c}{rw('units')}*{PR['mkt'][j]}*Timeline!{c}$9",
    }
    for key, text, unit, tot in OPS_FIELDS:
        mb.write_row(ow, rw(key), text, unit, lambda i, c, p, fn=spec[key]: fn(c, p), FMT_NUM, total=tot,
                     link=key in ("coll", "recov", "active", "rar"))
for key, text, unit, tot in OPS_FIELDS:
    mb.write_row(ow, mb.r(O, f"{key}T"), text, unit,
                 lambda i, c, p, k=key: "=" + "+".join(f"{c}{mb.r(O, f'{k}{j}')}" for j in range(NP)),
                 FMT_NUM, bold=True, total=tot)
mb.write_row(ow, mb.r(O, "unlocks_cum"), "Cumulative unlocked accounts (customer ownership)", "accounts",
             lambda i, c, p: f"={p}{mb.r(O, 'unlocks_cum')}+{c}{mb.r(O, 'unlocksT')}", FMT_NUM, total="last")
mb.write_row(ow, mb.r(O, "coll_rate"), "Collection rate (collected / due, excl. down payments)", "%",
             lambda i, c, p: f"=IF({c}{mb.r(O, 'dueT')}=0,0,{c}{mb.r(O, 'collT')}/{c}{mb.r(O, 'dueT')})", FMT_PCT,
             comment="PAYGo PERFORM-style: follow-on payments collected / scheduled, excluding deposits.")
mb.write_row(ow, mb.r(O, "wo_rate"), "Write-off rate (missed / due)", "%",
             lambda i, c, p: f"=IF({c}{mb.r(O, 'dueT')}=0,0,{c}{mb.r(O, 'missedT')}/{c}{mb.r(O, 'dueT')})", FMT_PCT)
mb.write_row(ow, mb.r(O, "rar_ratio"), "Receivables at risk / gross receivables", "%",
             lambda i, c, p: f"=IF({c}{mb.r(O, 'grossrecT')}=0,0,{c}{mb.r(O, 'rarT')}/{c}{mb.r(O, 'grossrecT')})", FMT_PCT)

# =====================================================================
# COSTS
# =====================================================================
C_ = "Costs"
kw = mb.sheet(C_, "Operating costs, working capital & capex", "LCY")
mb.time_header(kw)
oc = lambda k, c: mb.ref(O, k, c, this_sheet=C_)
cost_rows = [
    ("cogs", "Landed hardware cost (COGS)", lambda c, p: f"={oc('cogsT', c)}", "sum", True),
    ("install", "Installation & logistics (cost of sales)", lambda c, p: f"={oc('installT', c)}", "sum", True),
    ("cos", "Total cost of sales", lambda c, p: f"={c}{{cogs}}+{c}{{install}}", "sum", False),
    (None,),
    ("warranty", "Warranty & after-sales", lambda c, p: f"={oc('warrantyT', c)}", "sum", True),
    ("comm", "Agent / installer commissions", lambda c, p: f"={oc('commT', c)}", "sum", True),
    ("mkt", "Marketing & acquisition", lambda c, p: f"={oc('mktT', c)}", "sum", True),
    ("mm", "Payment processing fees", lambda c, p: f"=({oc('depositsT', c)}+{oc('collT', c)})*{INP['mm_fee']}", "sum", False),
    ("cs", "Customer service & collections", lambda c, p: f"={oc('activeT', c)}*{INP['cs_cost']}*Timeline!{c}$9", "sum", False),
    ("staff", "Staff", lambda c, p: f"={INP['staff']}*Timeline!{c}$9", "sum", False),
    ("ga", "G&A, rent, IT", lambda c, p: f"={INP['ga']}*Timeline!{c}$9", "sum", False),
    ("opex", "Total operating expenses", lambda c, p: f"=SUM({c}{{warranty}}:{c}{{ga}})", "sum", False),
    (None,),
    ("inv", "Inventory (closing)", lambda c, p: f"={c}{{cogs}}*{INP['inv_cover']}", "last", False),
    ("purch", "Hardware purchases", lambda c, p: f"={c}{{cogs}}+{c}{{inv}}-{p}{{inv}}", "sum", False),
    ("ap", "Supplier payables (closing)", lambda c, p: f"={c}{{purch}}*{INP['ap_days']}/(365/12)", "last", False),
    (None,),
    ("capex", "Fixed capex", lambda c, p: f"={INP['capex']}*Timeline!{c}$9", "sum", False),
    ("dep", "Depreciation (straight-line by vintage)",
     lambda c, p: (f"=SUMIFS(${col(1)}{{capex}}:{c}{{capex}},${col(1)}$4:{c}$4,\">\"&({c}$4-{INP['dep_life']}))"
                   f"/{INP['dep_life']}"), "sum", False),
    ("ppe", "Net fixed assets (closing)", lambda c, p: f"={p}{{ppe}}+{c}{{capex}}-{c}{{dep}}", "last", False),
]
rr = 8
for row_ in cost_rows:
    if row_[0]:
        mb.register(C_, row_[0], rr)
    rr += 1
cmap = {row_[0]: mb.r(C_, row_[0]) for row_ in cost_rows if row_[0]}
for row_ in cost_rows:
    if not row_[0]:
        continue
    key, text, fn, tot, link = row_
    mb.write_row(kw, mb.r(C_, key), text, "LCY", lambda i, c, p, fn=fn: fn(c, p).format(**cmap), FMT_NUM, total=tot,
                 bold=key in ("cos", "opex"), link=link)

# =====================================================================
# FINANCING (register) + FS
# =====================================================================
F = "Financing"
fw = mb.sheet(F, "Financing", "Equity, USD term loan with FX translation, receivables-backed facility")
mb.time_header(fw)
fin_rows = [("sec", "EQUITY"), ("eq_init", "Initial equity injection"),
            ("eq_top", "Automatic equity top-up (funding requirement)"), ("eq_cum", "Cumulative equity invested"),
            ("sec", "USD TERM LOAN"), ("tl_draw_usd", "Drawdown (USD)"), ("tl_rep_usd", "Repayment (USD)"),
            ("tl_bal_usd", "Closing balance (USD)"), ("tl_int", "Interest (LCY)"), ("tl_draw", "Drawdown (LCY)"),
            ("tl_rep", "Repayment (LCY)"), ("tl_bal", "Closing balance (LCY)"),
            ("fx_loss", "Unrealised FX loss / (gain) on USD debt (LCY)"),
            ("sec", "RECEIVABLES FACILITY (LCY)"), ("rf_bb", "Borrowing base (sum of tier contributions)"),
            ("rf_bal", "Facility drawn (closing; cash sweep within borrowing base)"), ("rf_flow", "Net drawdown / (repayment)"), ("rf_int", "Interest"),
            ("rf_util", "Utilisation of limit")]
rr = 8
FIN_ORDER = []
for k_, t_ in fin_rows:
    if k_ != "sec":
        mb.register(F, k_, rr)
    FIN_ORDER.append((None if k_ == "sec" else k_, t_, rr))
    rr += 1

S = "FS"
sw_ = mb.sheet(S, "Financial statements (monthly)", "LCY. Simplified IFRS-style presentation; simplifications listed in the manual.")
mb.time_header(sw_)
o = lambda k, c: mb.ref(O, k, c, this_sheet=S)
fs_rows = [
    ("sec", "INCOME STATEMENT"),
    ("rev_hw", "Hardware revenue (cash price)", lambda c, p: f"={o('hw_revT', c)}", "sum", True),
    ("rev_fin", "PAYGo financing income", lambda c, p: f"={o('fin_incT', c)}", "sum", True),
    ("rev", "Total revenue", lambda c, p: f"={c}{{rev_hw}}+{c}{{rev_fin}}", "sum", False),
    ("cos", "Cost of sales (hardware, installation)", lambda c, p: f"=-{mb.ref(C_, 'cos', c, this_sheet=S)}", "sum", True),
    ("gp", "Gross profit", lambda c, p: f"={c}{{rev}}+{c}{{cos}}", "sum", False),
    ("rbf", "RBF / subsidy income", lambda c, p: f"={o('rbfT', c)}", "sum", True),
    ("opex", "Operating expenses", lambda c, p: f"=-{mb.ref(C_, 'opex', c, this_sheet=S)}", "sum", True),
    ("ecl", "Expected credit losses", lambda c, p: f"=-{o('eclT', c)}", "sum", True),
    ("recov", "Recoveries on repossessed units", lambda c, p: f"={o('recovT', c)}", "sum", True),
    ("ebitda", "EBITDA", lambda c, p: f"={c}{{gp}}+{c}{{rbf}}+{c}{{opex}}+{c}{{ecl}}+{c}{{recov}}", "sum", False),
    ("da", "Depreciation", lambda c, p: f"=-{mb.ref(C_, 'dep', c, this_sheet=S)}", "sum", True),
    ("ebit", "EBIT", lambda c, p: f"={c}{{ebitda}}+{c}{{da}}", "sum", False),
    ("int_tl", "Interest - USD term loan", lambda c, p: f"=-{mb.ref(F, 'tl_int', c, this_sheet=S)}", "sum", True),
    ("int_rf", "Interest - receivables facility", lambda c, p: f"=-{mb.ref(F, 'rf_int', c, this_sheet=S)}", "sum", True),
    ("fx", "FX (loss) / gain on USD debt", lambda c, p: f"=-{mb.ref(F, 'fx_loss', c, this_sheet=S)}", "sum", True),
    ("pbt", "Profit before tax", lambda c, p: f"={c}{{ebit}}+{c}{{int_tl}}+{c}{{int_rf}}+{c}{{fx}}", "sum", False),
    ("cum_pbt", "  memo: cumulative PBT", lambda c, p: f"={p}{{cum_pbt}}+{c}{{pbt}}", "last", False),
    ("max_cum", "  memo: running maximum of cumulative PBT", lambda c, p: f"=MAX({p}{{max_cum}},{c}{{cum_pbt}})", "last", False),
    ("tax", "Income tax", lambda c, p: f"=-{INP['tax']}*(MAX(0,{c}{{max_cum}})-MAX(0,{p}{{max_cum}}))", "sum", False),
    ("ni", "Net income", lambda c, p: f"={c}{{pbt}}+{c}{{tax}}", "sum", False),
    ("blank",),
    ("sec", "BALANCE SHEET"),
    ("cash", "Cash", lambda c, p: f"={c}{{cash_end}}", "last", False),
    ("grossrec", "PAYGo receivables - gross", lambda c, p: f"={o('grossrecT', c)}", "last", True),
    ("prov", "Loss allowance (ECL)", lambda c, p: f"={p}{{prov}}-{o('eclT', c)}+{o('missedT', c)}", "last", False),
    ("netrec", "PAYGo receivables - net", lambda c, p: f"={c}{{grossrec}}+{c}{{prov}}", "last", False),
    ("inv", "Inventory", lambda c, p: f"={mb.ref(C_, 'inv', c, this_sheet=S)}", "last", True),
    ("ppe", "Net fixed assets", lambda c, p: f"={mb.ref(C_, 'ppe', c, this_sheet=S)}", "last", True),
    ("ta", "Total assets", lambda c, p: f"={c}{{cash}}+{c}{{netrec}}+{c}{{inv}}+{c}{{ppe}}", "last", False),
    ("ap", "Supplier payables", lambda c, p: f"={mb.ref(C_, 'ap', c, this_sheet=S)}", "last", True),
    ("tl", "USD term loan (in LCY)", lambda c, p: f"={mb.ref(F, 'tl_bal', c, this_sheet=S)}", "last", True),
    ("rf", "Receivables facility", lambda c, p: f"={mb.ref(F, 'rf_bal', c, this_sheet=S)}", "last", True),
    ("tliab", "Total liabilities", lambda c, p: f"={c}{{ap}}+{c}{{tl}}+{c}{{rf}}", "last", False),
    ("sc", "Share capital", lambda c, p: f"={mb.ref(F, 'eq_cum', c, this_sheet=S)}", "last", True),
    ("re", "Retained earnings", lambda c, p: f"={p}{{re}}+{c}{{ni}}", "last", False),
    ("te", "Total equity", lambda c, p: f"={c}{{sc}}+{c}{{re}}", "last", False),
    ("tle", "Total liabilities & equity", lambda c, p: f"={c}{{tliab}}+{c}{{te}}", "last", False),
    ("bs_chk", "Balance check (should be 0)", lambda c, p: f"=ROUND({c}{{ta}}-{c}{{tle}},0)", "max", False),
    ("blank",),
    ("sec", "CASH FLOW STATEMENT"),
    ("cf_ni", "Net income", lambda c, p: f"={c}{{ni}}", "sum", False),
    ("cf_da", "Add back: depreciation", lambda c, p: f"=-{c}{{da}}", "sum", False),
    ("cf_fx", "Add back: unrealised FX loss", lambda c, p: f"=-{c}{{fx}}", "sum", False),
    ("cf_rec", "(Increase) / decrease in net receivables", lambda c, p: f"=-({c}{{netrec}}-{p}{{netrec}})", "sum", False),
    ("cf_inv", "(Increase) / decrease in inventory", lambda c, p: f"=-({c}{{inv}}-{p}{{inv}})", "sum", False),
    ("cf_ap", "Increase / (decrease) in payables", lambda c, p: f"={c}{{ap}}-{p}{{ap}}", "sum", False),
    ("cfo", "Cash flow from operations", lambda c, p: f"=SUM({c}{{cf_ni}}:{c}{{cf_ap}})", "sum", False),
    ("cfi", "Cash flow from investing (capex)", lambda c, p: f"=-{mb.ref(C_, 'capex', c, this_sheet=S)}", "sum", False),
    ("cf_tl", "Term loan drawdown / (repayment)",
     lambda c, p: f"={mb.ref(F, 'tl_draw', c, this_sheet=S)}-{mb.ref(F, 'tl_rep', c, this_sheet=S)}", "sum", False),
    ("cf_rf", "Receivables facility drawdown / (repayment)", lambda c, p: f"={mb.ref(F, 'rf_flow', c, this_sheet=S)}", "sum", False),
    ("cf_eq0", "Equity - initial", lambda c, p: f"={mb.ref(F, 'eq_init', c, this_sheet=S)}", "sum", False),
    ("cash_pre_nf", "  memo: cash before facility and equity top-up",
     lambda c, p: f"={p}{{cash_end}}+{c}{{cfo}}+{c}{{cfi}}+{c}{{cf_tl}}+{c}{{cf_eq0}}", "last", False),
    ("cash_pre", "Cash before equity top-up", lambda c, p: f"={c}{{cash_pre_nf}}+{c}{{cf_rf}}", "last", False),
    ("eq_top", "Equity top-up to maintain minimum cash", lambda c, p: f"=MAX(0,{INP['min_cash']}-{c}{{cash_pre}})", "sum", False),
    ("cash_end", "Closing cash", lambda c, p: f"={c}{{cash_pre}}+{c}{{eq_top}}", "last", False),
    ("blank",),
    ("sec", "MEMO"),
    ("ebitda_pos", "EBITDA positive (1 = yes)", lambda c, p: f"=IF({c}{{ebitda}}>0,1,0)", None, False),
    ("cfo_pos", "Operating cash flow positive (1 = yes)", lambda c, p: f"=IF({c}{{cfo}}>0,1,0)", None, False),
]
rr = 8
for row_ in fs_rows:
    if row_[0] not in ("sec", "blank"):
        mb.register(S, row_[0], rr)
    rr += 1
fsmap = {row_[0]: mb.r(S, row_[0]) for row_ in fs_rows if row_[0] not in ("sec", "blank")}
BOLD_FS = ("rev", "gp", "ebitda", "ebit", "pbt", "ni", "ta", "tle", "netrec", "cfo", "cash_end")
rr = 8
for row_ in fs_rows:
    if row_[0] == "sec":
        mb.section(sw_, rr, row_[1])
    elif row_[0] != "blank":
        key, text, fn, tot, link = row_
        flag = key.endswith("_pos")
        mb.write_row(sw_, rr, text, "flag" if flag else "LCY", lambda i, c, p, fn=fn: fn(c, p).format(**fsmap),
                     FMT_INT if flag else FMT_NUM, total=tot, bold=key in BOLD_FS, link=link)
    rr += 1

fs_ref = lambda k, c: mb.ref(S, k, c, this_sheet=F)
fin_spec = {
    "eq_init": (lambda c, p: f"=IF({c}$4=1,{INP['eq0']},0)", "sum", FMT_NUM),
    "eq_top": (lambda c, p: f"={fs_ref('eq_top', c)}", "sum", FMT_NUM),
    "eq_cum": (lambda c, p: f"={p}{mb.r(F, 'eq_cum')}+{c}{mb.r(F, 'eq_init')}+{c}{mb.r(F, 'eq_top')}", "last", FMT_NUM),
    "tl_draw_usd": (lambda c, p: f"=IF({c}$4={INP['tl_month']},{INP['tl_amt']},0)", "sum", FMT_NUM),
    "tl_rep_usd": (lambda c, p: (
        f"=IF(AND({c}$4>{INP['tl_month']}+{INP['tl_grace']},{c}$4<={INP['tl_month']}+{INP['tl_grace']}+{INP['tl_amort']}),"
        f"MIN({p}{mb.r(F, 'tl_bal_usd')},{INP['tl_amt']}/{INP['tl_amort']}),0)"), "sum", FMT_NUM),
    "tl_bal_usd": (lambda c, p: f"={p}{mb.r(F, 'tl_bal_usd')}+{c}{mb.r(F, 'tl_draw_usd')}-{c}{mb.r(F, 'tl_rep_usd')}",
                   "last", FMT_NUM),
    "tl_int": (lambda c, p: f"={p}{mb.r(F, 'tl_bal_usd')}*{INP['tl_rate']}/12*Timeline!{c}$8", "sum", FMT_NUM),
    "tl_draw": (lambda c, p: f"={c}{mb.r(F, 'tl_draw_usd')}*Timeline!{c}$8", "sum", FMT_NUM),
    "tl_rep": (lambda c, p: f"={c}{mb.r(F, 'tl_rep_usd')}*Timeline!{c}$8", "sum", FMT_NUM),
    "tl_bal": (lambda c, p: f"={c}{mb.r(F, 'tl_bal_usd')}*Timeline!{c}$8", "last", FMT_NUM),
    "fx_loss": (lambda c, p: f"={p}{mb.r(F, 'tl_bal_usd')}*(Timeline!{c}$8-Timeline!{p}$8)", "sum", FMT_NUM),
    "rf_bb": (lambda c, p: f"={mb.ref(O, 'bbT', c, this_sheet=F)}", "last", FMT_NUM),
    "rf_bal": (lambda c, p: (f"=IF({c}$4>={INP['rf_start']},MAX(0,MIN({INP['rf_limit']},{c}{mb.r(F, 'rf_bb')},"
                             f"{p}{mb.r(F, 'rf_bal')}+{INP['min_cash']}-{fs_ref('cash_pre_nf', c)})),0)"), "last", FMT_NUM),
    "rf_flow": (lambda c, p: f"={c}{mb.r(F, 'rf_bal')}-{p}{mb.r(F, 'rf_bal')}", "sum", FMT_NUM),
    "rf_int": (lambda c, p: f"={p}{mb.r(F, 'rf_bal')}*{INP['rf_rate']}/12", "sum", FMT_NUM),
    "rf_util": (lambda c, p: f"=IF({INP['rf_limit']}=0,0,{c}{mb.r(F, 'rf_bal')}/{INP['rf_limit']})", "max", FMT_PCT),
}
for key, text, rr in FIN_ORDER:
    if key is None:
        mb.section(fw, rr, text)
        continue
    fn, tot, fmt = fin_spec[key]
    unit = "USD" if key.endswith("_usd") else ("%" if key == "rf_util" else "LCY")
    mb.write_row(fw, rr, text, unit, lambda i, c, p, fn=fn: fn(c, p), fmt, total=tot)

# =====================================================================
# COVENANTS (monthly)
# =====================================================================
CV = "Covenants"
cvw = mb.sheet(CV, "Lender covenant tests (monthly)",
               "Flags = 1 when a covenant is breached. Tested only while the relevant debt is outstanding.", tab="FF0000")
mb.time_header(cvw)
o_coll, o_due = mb.r(O, "collT"), mb.r(O, "dueT")
cov_rows = [
    ("cr3", "Trailing 3-month collection rate", FMT_PCT,
     lambda i, c, p: (f"=IFERROR(SUM(Ops!{col(max(1, i - 2))}{o_coll}:{c}{o_coll})/"
                      f"SUM(Ops!{col(max(1, i - 2))}{o_due}:{c}{o_due}),0)")),
    ("cr_flag", "Breach: collection rate below minimum", FMT_INT,
     lambda i, c, p: f"=IF(AND({mb.ref(F, 'rf_bal', c, this_sheet=CV)}>0,{c}{{cr3}}<{INP['cov_cr']}),1,0)"),
    ("rar", "Receivables at risk / gross receivables", FMT_PCT, lambda i, c, p: f"={mb.ref(O, 'rar_ratio', c, this_sheet=CV)}"),
    ("rar_flag", "Breach: receivables at risk above maximum", FMT_INT,
     lambda i, c, p: f"=IF(AND({mb.ref(F, 'rf_bal', c, this_sheet=CV)}>0,{c}{{rar}}>{INP['cov_rar']}),1,0)"),
    ("debt", "Total financial debt (LCY)", FMT_NUM,
     lambda i, c, p: f"={mb.ref(S, 'tl', c, this_sheet=CV)}+{mb.ref(S, 'rf', c, this_sheet=CV)}"),
    ("lev", "Debt / book equity", FMT_X,
     lambda i, c, p: f"=IF({mb.ref(S, 'te', c, this_sheet=CV)}<=0,99,{c}{{debt}}/{mb.ref(S, 'te', c, this_sheet=CV)})"),
    ("lev_flag", "Breach: leverage above maximum", FMT_INT,
     lambda i, c, p: f"=IF(AND({c}{{debt}}>0,{c}{{lev}}>{INP['cov_lev']}),1,0)"),
    ("liq", "Cash before equity top-up (LCY)", FMT_NUM, lambda i, c, p: f"={mb.ref(S, 'cash_pre', c, this_sheet=CV)}"),
    ("liq_flag", "Breach: liquidity below minimum (before new equity)", FMT_INT,
     lambda i, c, p: f"=IF(AND({c}{{debt}}>0,{c}{{liq}}<{INP['cov_cash']}),1,0)"),
    ("any_flag", "Any covenant breached in month", FMT_INT,
     lambda i, c, p: f"=MAX({c}{{cr_flag}},{c}{{rar_flag}},{c}{{lev_flag}},{c}{{liq_flag}})"),
]
rr = 8
for key, *_ in cov_rows:
    mb.register(CV, key, rr)
    rr += 1
cvmap = {k: mb.r(CV, k) for k, *_ in cov_rows}
for key, text, fmt, fn in cov_rows:
    mb.write_row(cvw, mb.r(CV, key), text, "", lambda i, c, p, fn=fn: fn(i, c, p).format(**cvmap), fmt,
                 total="sum" if key.endswith("flag") else ("min" if key in ("cr3", "liq") else "max"),
                 bold=key == "any_flag")

# =====================================================================
# ANNUAL
# =====================================================================
A = "Annual"
aw = mb.sheet(A, "Annual financial statements", "Flows summed by year; balances at year end. LCY.")
year_header(aw)
aw.column_dimensions["A"].width = 50


def ann(sheet, key, c, kind="sum"):
    if kind == "sum":
        return f"SUMIFS({mb.range_(sheet, key)},{TL_YR},{c}$6)"
    return f"INDEX({mb.range_(sheet, key)},1,{c}$6*12)"


rr = 8
ANN_BOLD = ("rev", "gp", "ebitda", "ni", "ta", "tle", "cfo", "cash_end")
for row_ in fs_rows:
    if row_[0] == "blank":
        rr += 1
        continue
    if row_[0] == "sec":
        if row_[1] == "MEMO":
            break
        mb.section(aw, rr, row_[1])
        rr += 1
        continue
    key, text, fn, tot, link = row_
    if key in ("cum_pbt", "max_cum", "cash_pre_nf"):
        continue
    label(aw, f"A{rr}", text, bold=key in ANN_BOLD)
    for y in range(1, YEARS + 1):
        c = col(y)
        put_calc(aw, f"{c}{rr}", "=" + ann(S, key, c, "sum" if tot == "sum" else "last"), FMT_NUM, bold=key in ANN_BOLD)
    mb.register(A, key, rr)
    rr += 1

# =====================================================================
# KPIs
# =====================================================================
K = "KPIs"
kpw = mb.sheet(K, "Key performance indicators", "PAYGo portfolio KPIs (PERFORM-style where noted), financial and lender KPIs.")
year_header(kpw)
kpw.column_dimensions["A"].width = 62
kpi_rows = [("sec", "Sales & customers")]
for j in range(NP):
    kpi_rows.append((f"units{j}", f"Units sold - {PRODUCTS[j]['name']}", lambda c, j=j: "=" + ann(O, f"units{j}", c), FMT_NUM))
kpi_rows += [
    ("units", "Units sold - total", lambda c: "=" + ann(O, "unitsT", c), FMT_NUM),
    ("asp_usd", "Average cash price per unit sold (USD, opening FX)",
     lambda c: f"=IFERROR({ann(O, 'hw_revT', c)}/{ann(O, 'unitsT', c)}/{INP['fx0']},0)", FMT_NUM),
    ("active", "Active PAYGo accounts (year end)", lambda c: "=" + ann(O, "activeT", c, "last"), FMT_NUM),
    ("unlocked", "Cumulative unlocked accounts (customer ownership)", lambda c: "=" + ann(O, "unlocks_cum", c, "last"), FMT_NUM),
    ("sec", "Portfolio quality"),
    ("cr", "Collection rate (collected / due, excl. down payments)",
     lambda c: f"=IFERROR({ann(O, 'collT', c)}/{ann(O, 'dueT', c)},0)", FMT_PCT),
    ("wo", "Write-off rate (missed / due)", lambda c: f"=IFERROR({ann(O, 'missedT', c)}/{ann(O, 'dueT', c)},0)", FMT_PCT),
    ("rar", "Receivables at risk / gross receivables (year end)",
     lambda c: f"=IFERROR({ann(O, 'rarT', c, 'last')}/{ann(O, 'grossrecT', c, 'last')},0)", FMT_PCT),
    ("cov", "Loss allowance coverage (allowance / gross receivables)",
     lambda c: f"=IFERROR(-{ann(S, 'prov', c, 'last')}/{ann(S, 'grossrec', c, 'last')},0)", FMT_PCT),
    ("recov_rate", "Recoveries / write-offs", lambda c: f"=IFERROR({ann(O, 'recovT', c)}/{ann(O, 'missedT', c)},0)", FMT_PCT),
    ("sec", "Revenue mix"),
]
for j in range(NP):
    kpi_rows.append((f"rev{j}", f"Revenue share - {PRODUCTS[j]['name']}",
                     lambda c, j=j: f"=IFERROR(({ann(O, f'hw_rev{j}', c)}+{ann(O, f'fin_inc{j}', c)})/{ann(S, 'rev', c)},0)",
                     FMT_PCT))
kpi_rows += [
    ("sec", "Profitability"),
    ("rev", "Revenue (LCY)", lambda c: "=" + ann(S, "rev", c), FMT_NUM),
    ("rev_usd", "Revenue (USD, average FX)", lambda c: f"=IFERROR({ann(S, 'rev', c)}/AVERAGEIFS({TL_FX},{TL_YR},{c}$6),0)", FMT_NUM),
    ("gm", "Gross margin", lambda c: f"=IFERROR({ann(S, 'gp', c)}/{ann(S, 'rev', c)},0)", FMT_PCT),
    ("ebitda", "EBITDA (LCY)", lambda c: "=" + ann(S, "ebitda", c), FMT_NUM),
    ("ebitda_m", "EBITDA margin", lambda c: f"=IFERROR({ann(S, 'ebitda', c)}/{ann(S, 'rev', c)},0)", FMT_PCT),
    ("credit_cost", "Net credit losses / revenue",
     lambda c: f"=IFERROR(-({ann(S, 'ecl', c)}+{ann(S, 'recov', c)})/{ann(S, 'rev', c)},0)", FMT_PCT),
    ("rbf_share", "RBF dependency (RBF income / revenue)", lambda c: f"=IFERROR({ann(S, 'rbf', c)}/{ann(S, 'rev', c)},0)", FMT_PCT),
    ("ni", "Net income (LCY)", lambda c: "=" + ann(S, "ni", c), FMT_NUM),
    ("sec", "Funding, leverage & coverage"),
    ("cash", "Closing cash (LCY)", lambda c: "=" + ann(S, "cash_end", c, "last"), FMT_NUM),
    ("eq_cum", "Cumulative equity invested (LCY)", lambda c: "=" + ann(F, "eq_cum", c, "last"), FMT_NUM),
    ("eq_top", "Equity top-ups in year (funding gap, LCY)", lambda c: "=" + ann(S, "eq_top", c), FMT_NUM),
    ("debt", "Total debt (year end, LCY)", lambda c: f"={ann(S, 'tl', c, 'last')}+{ann(S, 'rf', c, 'last')}", FMT_NUM),
    ("de", "Debt / book equity",
     lambda c: f"=IFERROR(({ann(S, 'tl', c, 'last')}+{ann(S, 'rf', c, 'last')})/{ann(S, 'te', c, 'last')},0)", FMT_X),
    ("ds", "Debt service (interest + term-loan principal, LCY)",
     lambda c: f"={ann(F, 'tl_int', c)}+{ann(F, 'tl_rep', c)}+{ann(F, 'rf_int', c)}", FMT_NUM),
    ("dscr", "DSCR ((CFO + interest) / debt service)",
     lambda c: f"=IFERROR(({ann(S, 'cfo', c)}-{ann(S, 'int_tl', c)}-{ann(S, 'int_rf', c)})/{c}<<ds>>,0)", FMT_X),
    ("dscr_flag", "Breach: DSCR below minimum (years with debt service)",
     lambda c: f"=IF(AND({c}<<ds>>>0,{c}<<dscr>><{INP['cov_dscr']}),1,0)", FMT_INT),
    ("cov_months", "Months with any monthly covenant breach", lambda c: "=" + ann(CV, "any_flag", c), FMT_INT),
    ("fx", "FX rate (year end, LCY / USD)", lambda c: f"=INDEX({TL_FX},1,{c}$6*12)", FMT_NUM2),
]
rr = 8
KROWS = {}
for item in kpi_rows:
    if item[0] != "sec":
        KROWS[item[0]] = rr
    rr += 1
rr = 8
for item in kpi_rows:
    if item[0] == "sec":
        mb.section(kpw, rr, item[1])
    else:
        key, text, fn, fmt = item
        label(kpw, f"A{rr}", text, bold=key in ("units", "rev", "ebitda", "ni", "cr"))
        for y in range(1, YEARS + 1):
            c = col(y)
            f = fn(c).replace("<<ds>>", str(KROWS["ds"])).replace("<<dscr>>", str(KROWS["dscr"]))
            put_calc(kpw, f"{c}{rr}", f, fmt)
        mb.register(K, key, rr)
    rr += 1
rr += 1
mb.section(kpw, rr, "Headline metrics"); rr += 1
cr3r = mb.r(CV, "cr3")
heads = [
    ("peak_eq", "Peak cumulative equity requirement (LCY)", f"=MAX({mb.range_(F, 'eq_cum')})", FMT_NUM),
    ("peak_eq_usd", "Peak cumulative equity requirement (USD, opening FX)", f"=C<<peak_eq>>/{INP['fx0']}", FMT_NUM),
    ("peak_debt", "Peak total debt (LCY)", f"=MAX({mb.range_(CV, 'debt')})", FMT_NUM),
    ("rbf_total_usd", "Total RBF received (USD, opening FX)", f"=SUM({mb.range_(O, 'rbfT')})/{INP['fx0']}", FMT_NUM),
    ("be_ebitda", "First month with positive EBITDA", f"=IFERROR(MATCH(1,{mb.range_(S, 'ebitda_pos')},0),\"Not reached\")", FMT_INT),
    ("be_cfo", "First month with positive operating cash flow",
     f"=IFERROR(MATCH(1,{mb.range_(S, 'cfo_pos')},0),\"Not reached\")", FMT_INT),
    ("min_cr3", "Lowest trailing-3-month collection rate (from month 3)",
     f"=MIN(Covenants!{col(3)}{cr3r}:{mb.last}{cr3r})", FMT_PCT),
    ("max_rar", "Highest receivables-at-risk ratio", f"=MAX({mb.range_(O, 'rar_ratio')})", FMT_PCT),
    ("breach_months", "Total months with a covenant breach", f"=SUM({mb.range_(CV, 'any_flag')})", FMT_INT),
    ("dscr_breaches", "Years with DSCR below minimum",
     f"=SUM({col(1)}{KROWS['dscr_flag']}:{col(YEARS)}{KROWS['dscr_flag']})", FMT_INT),
]
HEAD = {}
for key, *_ in heads:
    HEAD[key] = rr
    rr += 1
for key, text, f, fmt in heads:
    r_ = HEAD[key]
    label(kpw, f"A{r_}", text, bold=True)
    put_calc(kpw, f"C{r_}", f.replace("<<peak_eq>>", str(HEAD["peak_eq"])), fmt, bold=True)
H = {k: f"KPIs!$C${v}" for k, v in HEAD.items()}
note(kpw, f"A{rr + 1}", "Receivables at risk approximates PAYGo PERFORM 'Receivables at Risk'. Covenant definitions are "
     "illustrative; use those in the actual facility agreement.")

# =====================================================================
# VALUATION & RETURNS
# =====================================================================
V = "Valuation"
vw = mb.sheet(V, "Valuation & investor returns", "DCF of unlevered free cash flow (LCY) and equity investor returns (USD).",
              tab="00B050")
year_header(vw, with_y0=True)
vw.column_dimensions["A"].width = 64
vw.column_dimensions["C"].width = 18
val_rows = [
    ("sec", "Unlevered free cash flow (LCY)"),
    ("ebitda", "EBITDA", lambda c: "=" + ann(S, "ebitda", c)),
    ("tax", "Less: income tax paid (levered tax - simplification)", lambda c: "=" + ann(S, "tax", c)),
    ("capex", "Less: capex", lambda c: "=-" + ann(C_, "capex", c)),
    ("nwc", "Net working capital (net receivables + inventory - payables), year end",
     lambda c: f"={ann(S, 'netrec', c, 'last')}+{ann(S, 'inv', c, 'last')}-{ann(S, 'ap', c, 'last')}"),
    ("dnwc", "Less: increase in net working capital", lambda c: f"=-({c}<<nwc>>-{gcl(ord(c) - 64 - 1)}<<nwc>>)"),
    ("fcff", "Unlevered free cash flow (FCFF)", lambda c: f"={c}<<ebitda>>+{c}<<tax>>+{c}<<capex>>+{c}<<dnwc>>"),
    ("df", "Discount factor (mid-year)", lambda c: f"=1/(1+{INP['wacc']})^({c}$6-0.5)"),
    ("pv", "Present value of FCFF", lambda c: f"={c}<<fcff>>*{c}<<df>>"),
    ("sec", "Equity investor (USD)"),
    ("topups", "Equity top-ups in year (LCY)", lambda c: "=" + ann(S, "eq_top", c)),
    ("fx_avg", "Average FX in year (LCY / USD)", lambda c: f"=AVERAGEIFS({TL_FX},{TL_YR},{c}$6)"),
    ("inv_flow", "Investor cash flow (USD)", None),
]
VR = {}
rr = 8
for item in val_rows:
    if item[0] != "sec":
        VR[item[0]] = rr
    rr += 1


def vsub(f):
    for k_, v_ in VR.items():
        f = f.replace(f"<<{k_}>>", str(v_))
    return f


rr = 8
for item in val_rows:
    if item[0] == "sec":
        mb.section(vw, rr, item[1])
    else:
        key, text, fn = item
        label(vw, f"A{rr}", text, bold=key in ("fcff", "inv_flow"))
        if fn:
            for y in range(1, YEARS + 1):
                c = col(y)
                fmt = FMT_NUM2 if key in ("df", "fx_avg") else FMT_NUM
                put_calc(vw, f"{c}{rr}", vsub(fn(c)), fmt, bold=key == "fcff")
    rr += 1
put_calc(vw, f"D{VR['nwc']}", 0, FMT_NUM)
rr += 1
mb.section(vw, rr, "Valuation summary"); rr += 1
L5 = col(YEARS)
vsum = [
    ("sum_pv", "Sum of PV of FCFF, Years 1-5 (LCY)", f"=SUM({col(1)}{VR['pv']}:{L5}{VR['pv']})", FMT_NUM),
    ("tv_fcff", "Normalised terminal FCFF: (EBITDA - tax - capex)_Y5 x (1+g) - g x NWC_Y5 (LCY)",
     f"=({L5}{VR['ebitda']}+{L5}{VR['tax']}+{L5}{VR['capex']})*(1+{INP['tg']})-{INP['tg']}*{L5}{VR['nwc']}", FMT_NUM),
    ("tv", "Terminal value at end of Year 5 (Gordon growth on normalised FCFF, LCY)",
     f"=IF({INP['wacc']}>{INP['tg']},C<<tv_fcff>>/({INP['wacc']}-{INP['tg']}),0)", FMT_NUM),
    ("pv_tv", "PV of terminal value (LCY)", f"=C<<tv>>/(1+{INP['wacc']})^{YEARS}", FMT_NUM),
    ("ev", "DCF enterprise value at model start (LCY)", "=C<<sum_pv>>+C<<pv_tv>>", FMT_NUM),
    ("ev_usd", "DCF enterprise value at model start (USD, opening FX)", f"=C<<ev>>/{INP['fx0']}", FMT_NUM),
    ("tv_share", "Terminal value share of EV", "=IFERROR(C<<pv_tv>>/C<<ev>>,0)", FMT_PCT),
    ("gap1", None, None, None),
    ("ebitda5", "Year 5 EBITDA (LCY)", f"={L5}{VR['ebitda']}", FMT_NUM),
    ("net_debt5", "Net debt at end of Year 5 (LCY)",
     f"={ann(S, 'tl', L5, 'last')}+{ann(S, 'rf', L5, 'last')}-{ann(S, 'cash_end', L5, 'last')}", FMT_NUM),
    ("book5", "Book equity at end of Year 5 (LCY)", "=" + ann(S, "te", L5, "last"), FMT_NUM),
    ("exit_eq", "Exit equity value, 100% (LCY)",
     f"=MAX(0,IF({INP['exit_method']}=1,{INP['exit_mult']}*C<<ebitda5>>-C<<net_debt5>>,{INP['exit_pb']}*C<<book5>>))", FMT_NUM),
    ("fx5", "FX at exit (LCY / USD)", f"=INDEX({TL_FX},1,{MONTHS})", FMT_NUM2),
    ("exit_eq_usd", "Exit equity value, 100% (USD)", "=C<<exit_eq>>/C<<fx5>>", FMT_NUM),
    ("gap2", None, None, None),
    ("stake", "Investor stake (ticket / post-money)", f"=IFERROR({INP['inv_usd']}/({INP['pre_money']}+{INP['inv_usd']}),0)", FMT_PCT),
    ("irr", "Investor IRR (USD)", f"=IFERROR(IRR(D{VR['inv_flow']}:{L5}{VR['inv_flow']},0.1),\"n/a\")", FMT_PCT),
    ("moic", "Investor MOIC (USD)",
     f"=IFERROR(SUMIF(D{VR['inv_flow']}:{L5}{VR['inv_flow']},\">0\")/-SUMIF(D{VR['inv_flow']}:{L5}{VR['inv_flow']},\"<0\"),0)", FMT_X),
]
VS = {}
for key, *_ in vsum:
    VS[key] = rr
    rr += 1
for key, text, f, fmt in vsum:
    if text is None:
        continue
    r_ = VS[key]
    for k_, v_ in VS.items():
        f = f.replace(f"<<{k_}>>", str(v_))
    b = key in ("ev", "ev_usd", "irr", "moic", "exit_eq_usd")
    label(vw, f"A{r_}", text, bold=b)
    put_calc(vw, f"C{r_}", f, fmt, bold=b)
put_calc(vw, f"D{VR['inv_flow']}", f"=-{INP['inv_usd']}", FMT_NUM, bold=True)
for y in range(1, YEARS + 1):
    c = col(y)
    exit_term = f"+C{VS['stake']}*C{VS['exit_eq_usd']}" if y == YEARS else ""
    put_calc(vw, f"{c}{VR['inv_flow']}", f"=-C{VS['stake']}*{c}{VR['topups']}/{c}{VR['fx_avg']}{exit_term}", FMT_NUM, bold=True)
VAL = {k: f"Valuation!$C${v}" for k, v in VS.items()}
note(vw, f"A{rr + 1}", "Investor funds its pro-rata share of any equity top-up and receives no dividends before exit. "
     "LCY flows are converted to USD at average FX for the year; exit at year-end FX.")
note(vw, f"A{rr + 2}", "For PAYGo companies, growth of the receivables book is working capital, so FCFF is negative while the "
     "book grows. The terminal value therefore uses a normalised FCFF that reinvests only g x NWC (steady-state growth).")

# =====================================================================
# UNIT ECONOMICS
# =====================================================================
U = "Unit_Economics"
uw = mb.sheet(U, "Unit economics by tier (per unit, month-1 prices, active scenario)",
              "Lifetime view of one PAYGo customer. Undiscounted unless stated.", tab="00B050")
uw.column_dimensions["A"].width = 62
for c in PCOLS:
    uw.column_dimensions[c].width = 18
header_row(uw, 4, ["Metric", "Unit"] + [f"Tier {p['tier']}" for p in PRODUCTS])
ue = [
    ("price", "Cash price", "LCY", lambda j: f"={PR['price'][j]}", FMT_NUM),
    ("contract", "Total PAYGo contract value", "LCY", lambda j: f"={PR['contract'][j]}", FMT_NUM),
    ("apr", "Implied annual financing rate (nominal APR)", "%", lambda j: f"={PR['apr'][j]}", FMT_PCT),
    ("deposit", "Down payment", "LCY", lambda j: f"={PR['deposit'][j]}", FMT_NUM),
    ("coll", "Expected instalments collected", "LCY", lambda j: f"={CT['coll'][j]}", FMT_NUM),
    ("cash_in", "Expected lifetime customer cash (down payment + instalments)", "LCY", lambda j: "=<c><deposit>+<c><coll>", FMT_NUM),
    ("loss", "Expected loss rate (missed / scheduled instalments)", "%", lambda j: f"=IFERROR({CT['missed'][j]}/{CT['due'][j]},0)", FMT_PCT),
    ("lcr", "Lifetime collection rate (customer cash / contract value)", "%", lambda j: "=IFERROR(<c><cash_in>/<c><contract>,0)", FMT_PCT),
    ("recov", "Expected recoveries from repossession", "LCY", lambda j: f"={CT['recov'][j]}", FMT_NUM),
    ("rbf", "RBF per unit (opening FX)", "LCY", lambda j: f"={CT['rbf'][j]}", FMT_NUM),
    ("landed", "Landed hardware cost", "LCY", lambda j: f"={PR['landed'][j]}", FMT_NUM),
    ("install", "Installation & logistics", "LCY", lambda j: f"={PR['install'][j]}", FMT_NUM),
    ("warr", "Warranty provision", "LCY", lambda j: f"={PR['landed'][j]}*{PR['warranty'][j]}", FMT_NUM),
    ("cac", "Customer acquisition cost (CAC)", "LCY", lambda j: f"={PR['cac'][j]}", FMT_NUM),
    ("serv", "Payment fees + servicing over life", "LCY",
     lambda j: f"=<c><cash_in>*{INP['mm_fee']}+{INP['cs_cost']}*(SUM({crange(j, 'active')})-1)", FMT_NUM),
    ("contrib", "Lifetime contribution per unit", "LCY",
     lambda j: "=<c><cash_in>+<c><recov>+<c><rbf>-<c><landed>-<c><install>-<c><warr>-<c><cac>-<c><serv>", FMT_NUM),
    ("ltv_cac", "LTV / CAC (contribution before CAC / CAC)", "x", lambda j: "=IFERROR((<c><contrib>+<c><cac>)/<c><cac>,0)", FMT_X),
    ("payback", "Cash payback (months after sale)", "months",
     lambda j: f"=IF(COUNTIF({crange(j, 'cum')},\"<0\")>{MAX_AGE},\"Not paid back\",COUNTIF({crange(j, 'cum')},\"<0\"))", FMT_INT),
    ("irr", "Unit IRR (annualised, unlevered)", "%", lambda j: f"=IFERROR((1+IRR({crange(j, 'ncf')},0.02))^12-1,\"n/a\")", FMT_PCT),
    ("npv", "Unit NPV at the DCF discount rate", "LCY",
     lambda j: (f"=NPV((1+{INP['wacc']})^(1/12)-1,{crange(j, 'ncf')})*(1+{INP['wacc']})^(1/12)"), FMT_NUM),
]
UR = {k: 5 + n for n, (k, *_) in enumerate(ue)}
for key, text, unit, fn, fmt in ue:
    r_ = UR[key]
    b = key in ("contrib", "ltv_cac", "irr", "npv")
    label(uw, f"A{r_}", text, bold=b)
    label(uw, f"B{r_}", unit, size=9, color=GREY_TXT)
    for j in range(NP):
        f = fn(j).replace("<c>", PCOLS[j])
        for k_, v_ in UR.items():
            f = f.replace(f"<{k_}>", str(v_))
        put_calc(uw, f"{PCOLS[j]}{r_}", f, fmt, bold=b)
note(uw, f"A{5 + len(ue) + 1}", "Servicing counts active months after the sale month. Payback counts months with negative "
     "cumulative cash flow (ages 0-60). Unit NPV discounts monthly at the DCF rate; age 0 undiscounted.")

# =====================================================================
# CHECKS
# =====================================================================
X = "Checks"
xw = mb.sheet(X, "Integrity checks", "Each check returns 0 when OK. The master check feeds Cover, Investment_Summary and Dashboard.",
              tab="FF0000")
xw.column_dimensions["A"].width = 64
header_row(xw, 4, ["Check", "Unit", "Result (0 = OK)"])
mixrow = PR["mix"][0].split("$")[-1]
tenrow = PR["tenor"][0].split("$")[-1]
checks = [
    ("Balance sheet balances (max abs difference, all months)", f"=MAX(MAX({mb.range_(S, 'bs_chk')}),-MIN({mb.range_(S, 'bs_chk')}))"),
    ("Sales mix sums to 100%", f"=IF(ABS(SUM(Products!$C${mixrow}:${PCOLS[-1]}${mixrow})-1)>0.0001,1,0)"),
    ("Closing cash never below minimum cash", f"=IF(MIN({mb.range_(S, 'cash_end')})<{INP['min_cash']}-1,1,0)"),
    ("Gross receivables never negative", f"=IF(MIN({mb.range_(S, 'grossrec')})<-1,1,0)"),
    ("Loss allowance never positive (contra-asset)", f"=IF(MAX({mb.range_(S, 'prov')})>1,1,0)"),
    ("Facility within limit", f"=IF(MAX({mb.range_(F, 'rf_bal')})>{INP['rf_limit']}+1,1,0)"),
    ("Cash flow ties to balance-sheet cash", f"=IF(ABS(FS!{mb.last}{mb.r(S, 'cash')}-FS!{mb.last}{mb.r(S, 'cash_end')})>1,1,0)"),
    ("Tenors within curve horizon (<= 60 months)", f"=IF(MAX(Products!$C${tenrow}:${PCOLS[-1]}${tenrow})>{MAX_AGE},1,0)"),
    ("Down payment not above cash price", "=" + "+".join(f"IF({PR['deposit'][j]}>{PR['price'][j]},1,0)" for j in range(NP))),
    ("Scenario selector valid (1-3)", f"=IF(OR({INP['scenario']}<1,{INP['scenario']}>3),1,0)"),
    ("Investor ticket within initial equity", f"=IF({INP['inv_usd']}*{INP['fx0']}>{INP['eq0']}+1,1,0)"),
    ("Terminal growth below discount rate", f"=IF({INP['tg']}>={INP['wacc']},1,0)"),
]
for k_, (text, f) in enumerate(checks):
    r_ = 5 + k_
    label(xw, f"A{r_}", text)
    label(xw, f"B{r_}", "flag")
    put_calc(xw, f"C{r_}", f, FMT_NUM)
MR = 5 + len(checks) + 1
label(xw, f"A{MR}", "MASTER CHECK", bold=True)
put_calc(xw, f"C{MR}", f"=IF(SUM(C5:C{MR - 2})=0,\"OK\",\"ERROR\")", "@", bold=True)
MASTER = f"Checks!$C${MR}"

# =====================================================================
# SENSITIVITY (static snapshot)
# =====================================================================
SN = "Sensitivity"
snw = mb.sheet(SN, "Scenario & sensitivity snapshot (static values)",
               "Generated by the verified Python twin (tools/shadow_shs.py) at DEFAULT inputs. Does NOT update when inputs change.",
               tab="00B050")
SENS_METRICS = [("peak_eq_usd", "Peak equity need (USD m)", 1e-6, FMT_NUM2),
                ("rev5_usd", "Year 5 revenue (USD m)", 1e-6, FMT_NUM2),
                ("ebitda_m5", "Year 5 EBITDA margin", 1, FMT_PCT),
                ("cr5", "Year 5 collection rate", 1, FMT_PCT),
                ("ev_usd", "DCF EV (USD m)", 1e-6, FMT_NUM2),
                ("irr", "Investor IRR (USD)", 1, FMT_PCT),
                ("moic", "Investor MOIC", 1, FMT_X),
                ("breach_months", "Covenant-breach months", 1, FMT_INT)]
snw.column_dimensions["A"].width = 48
header_row(snw, 5, ["Case"] + [m[1] for m in SENS_METRICS])
for k_ in range(len(SENS_METRICS)):
    snw.column_dimensions[gcl(2 + k_)].width = 16
snw.row_dimensions[5].height = 32
SENS_ROW0 = 6

# =====================================================================
# GLOSSARY
# =====================================================================
GL = "Glossary"
gw = mb.sheet(GL, "Glossary - PAYGo & SHS terms used in this model", "Definitions as implemented in the model.")
gw.column_dimensions["A"].width = 34
gw.column_dimensions["B"].width = 120
terms = [
    ("PAYGo (pay-as-you-go)", "Asset financing in which the customer pays a down payment, then small frequent instalments priced as a "
     "daily rate, usually by mobile money. The device can be locked remotely if payments stop."),
    ("Down payment (deposit)", "Upfront payment at the time of sale. Excluded from the collection rate."),
    ("Daily rate / instalment", "Price per day of use. Monthly instalment = daily rate x 365 / 12."),
    ("Tenor", "Number of months over which the PAYGo contract is repaid."),
    ("Unlock (customer ownership)", "The customer reaches the end of the payment plan and the device is permanently unlocked. "
     "The model counts accounts still paying at the end of tenor."),
    ("Cohort (vintage)", "All units sold in the same month. Cohort analysis follows each vintage's repayment over time."),
    ("Survival curve", "Share of a cohort's accounts that are still paying at each age; driven by the monthly default hazard."),
    ("Collection rate", "Instalments collected / instalments due in the period, excluding down payments (PAYGo PERFORM-style)."),
    ("Write-off rate", "Missed instalments written off / instalments due. The model writes off missed instalments as they fall due."),
    ("Receivables at risk (RaR)", "Carrying amount of receivables of accounts that have stopped paying. Approximates PAYGo PERFORM RaR."),
    ("Expected credit loss (ECL)", "Lifetime expected loss recognised at origination from the scenario repayment curve "
     "(simplified IFRS 9 - no staging)."),
    ("Recoveries", "Net resale value of repossessed units, recognised as a reduction of credit losses."),
    ("RBF (results-based financing)", "Subsidy paid per verified unit sold, after a verification lag. Recognised as other income when "
     "received (cash basis)."),
    ("Borrowing base", "Maximum facility drawing = sum over tiers of advance rate x eligible receivables "
     "(gross receivables less receivables at risk)."),
    ("Advance rate", "Share of eligible receivables a lender is willing to finance."),
    ("DSCR", "Debt service coverage ratio: (operating cash flow + interest) / (interest + scheduled principal)."),
    ("Funding requirement", "Equity that must be injected to keep cash at the minimum balance (automatic equity top-up)."),
    ("MTF tier", "ESMAP Multi-Tier Framework for household electricity access, Tiers 0-5. Tiers here refer to the capacity attribute "
     "only and are indicative; a full assessment also covers duration, reliability, quality, affordability, legality, health & safety."),
    ("Solar inverter system (Tiers 4-5)", "Larger PV + lithium battery + inverter systems supplying AC appliances; typically sold to "
     "urban / peri-urban households and SMEs, often as backup to an unreliable grid."),
    ("LTV / CAC", "Lifetime contribution before acquisition cost divided by customer acquisition cost."),
    ("Unit IRR", "Annualised IRR of one unit's cash flows: down payment, collections, recoveries and RBF less hardware, installation, "
     "warranty, acquisition and servicing costs."),
]
header_row(gw, 4, ["Term", "Definition"])
for k_, (t_, d_) in enumerate(terms):
    label(gw, f"A{5 + k_}", t_, bold=True)
    gw[f"B{5 + k_}"] = d_
    gw[f"B{5 + k_}"].alignment = Alignment(wrap_text=True, vertical="top")
    gw[f"B{5 + k_}"].font = Font(name=FONT, size=10)
    gw.row_dimensions[5 + k_].height = 28

# =====================================================================
# INVESTMENT SUMMARY
# =====================================================================
iw = inv_ws
iw.column_dimensions["A"].width = 52
for c in "BCDEFG":
    iw.column_dimensions[c].width = 17
label(iw, "A4", "Active scenario"); put_calc(iw, "B4", "=Scenarios!$G$12", "@", bold=True, link=True)
label(iw, "A5", "Master check"); put_calc(iw, "B5", f"={MASTER}", "@", bold=True, link=True)
label(iw, "D4", "Model version"); label(iw, "E4", VERSION, bold=True)
label(iw, "D5", "Currency"); put_calc(iw, "E5", f"={INP['currency']}", "@", link=True)
r_ = 7
mb.section(iw, r_, "1. Operating & financial trajectory"); r_ += 1
header_row(iw, r_, ["Metric", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]); r_ += 1
for key, text, fmt in [("units", "Units sold", FMT_NUM), ("active", "Active PAYGo accounts (year end)", FMT_NUM),
                       ("asp_usd", "Average cash price per unit (USD)", FMT_NUM),
                       ("rev_usd", "Revenue (USD, average FX)", FMT_NUM), ("gm", "Gross margin", FMT_PCT),
                       ("ebitda_m", "EBITDA margin", FMT_PCT), ("ni", "Net income (LCY)", FMT_NUM),
                       ("cr", "Collection rate", FMT_PCT), ("rar", "Receivables at risk / gross receivables", FMT_PCT),
                       ("debt", "Total debt (LCY, year end)", FMT_NUM), ("dscr", "DSCR", FMT_X)]:
    label(iw, f"A{r_}", text)
    for y in range(1, YEARS + 1):
        put_calc(iw, f"{gcl(1 + y)}{r_}", f"=KPIs!{col(y)}{mb.r(K, key)}", fmt, link=True)
    r_ += 1
r_ += 1


def summary_block(title, items):
    global r_
    mb.section(iw, r_, title); r_ += 1
    for text, ref, fmt in items:
        label(iw, f"A{r_}", text)
        put_calc(iw, f"B{r_}", f"={ref}", fmt, bold=True, link=True)
        r_ += 1
    r_ += 1


summary_block("2. Funding requirement", [
    ("Peak equity requirement (USD, opening FX)", H["peak_eq_usd"], FMT_NUM),
    ("Peak equity requirement (LCY)", H["peak_eq"], FMT_NUM),
    ("Peak total debt (LCY)", H["peak_debt"], FMT_NUM),
    ("Total RBF received (USD)", H["rbf_total_usd"], FMT_NUM),
    ("First month with positive EBITDA", H["be_ebitda"], FMT_INT),
    ("First month with positive operating cash flow", H["be_cfo"], FMT_INT)])
summary_block("3. Valuation & equity returns", [
    ("DCF enterprise value at start (USD)", VAL["ev_usd"], FMT_NUM),
    ("Terminal value share of EV", VAL["tv_share"], FMT_PCT),
    ("Exit equity value, 100% (USD, end Year 5)", VAL["exit_eq_usd"], FMT_NUM),
    ("Investor stake", VAL["stake"], FMT_PCT),
    ("Investor IRR (USD)", VAL["irr"], FMT_PCT),
    ("Investor MOIC (USD)", VAL["moic"], FMT_X)])
summary_block("4. Lender view", [
    ("Lowest trailing-3-month collection rate", H["min_cr3"], FMT_PCT),
    ("Highest receivables-at-risk ratio", H["max_rar"], FMT_PCT),
    ("Months with any covenant breach", H["breach_months"], FMT_INT),
    ("Years with DSCR below minimum", H["dscr_breaches"], FMT_INT),
    ("Peak facility utilisation", f"Financing!$C${mb.r(F, 'rf_util')}", FMT_PCT)])
mb.section(iw, r_, "5. Unit economics by tier"); r_ += 1
header_row(iw, r_, ["Metric"] + [f"Tier {p['tier']}" for p in PRODUCTS]); r_ += 1
for key, text, fmt in [("price", "Cash price (LCY)", FMT_NUM), ("apr", "Implied APR", FMT_PCT),
                       ("loss", "Expected loss rate", FMT_PCT), ("ltv_cac", "LTV / CAC", FMT_X),
                       ("payback", "Cash payback (months)", FMT_INT), ("irr", "Unit IRR", FMT_PCT)]:
    label(iw, f"A{r_}", text)
    for j in range(NP):
        put_calc(iw, f"{gcl(2 + j)}{r_}", f"=Unit_Economics!{PCOLS[j]}{UR[key]}", fmt, link=True)
    r_ += 1
r_ += 1
mb.section(iw, r_, "6. Scenario snapshot (static, default inputs - see Sensitivity)"); r_ += 1
header_row(iw, r_, ["Case", "Peak equity (USD m)", "Investor IRR", "MOIC", "Breach months"]); r_ += 1
for k_ in range(3):
    for cc, src, fmt in zip("ABCDE", ["A", "B", "G", "H", "I"], ["@", FMT_NUM2, FMT_PCT, FMT_X, FMT_INT]):
        put_calc(iw, f"{cc}{r_}", f"=IF(Sensitivity!{src}{SENS_ROW0 + k_}=\"\",\"\",Sensitivity!{src}{SENS_ROW0 + k_})", fmt, link=True)
    r_ += 1
note(iw, f"A{r_ + 1}", "All default inputs are illustrative. Not investment advice. See Cover for the disclaimer.")

# =====================================================================
# DASHBOARD
# =====================================================================
D = "Dashboard"
dw = mb.sheet(D, "Dashboard", "Charts read from Annual and KPIs (active scenario).", tab="00B050")
label(dw, "A4", "Active scenario"); put_calc(dw, "B4", "=Scenarios!$G$12", "@", bold=True, link=True)
label(dw, "A5", "Master check"); put_calc(dw, "B5", f"={MASTER}", "@", bold=True, link=True)
dw.column_dimensions["A"].width = 30
dw.column_dimensions["B"].width = 16


def chart_rows(ch, ws_, keys, sheet_key):
    for key in keys:
        ch.add_data(Reference(ws_, min_col=5, max_col=4 + YEARS, min_row=mb.r(sheet_key, key)), from_rows=True,
                    titles_from_data=False)
    ch.set_categories(Reference(ws_, min_col=5, max_col=4 + YEARS, min_row=5))
    ch.height, ch.width = 8, 15


c1 = BarChart(); c1.title = "Revenue & EBITDA (LCY)"; chart_rows(c1, aw, ["rev", "ebitda"], A); dw.add_chart(c1, "D4")
c2 = BarChart(); c2.grouping = "stacked"; c2.overlap = 100
c2.title = "Units sold by tier"; chart_rows(c2, kpw, [f"units{j}" for j in range(NP)], K); dw.add_chart(c2, "M4")
c3 = LineChart(); c3.title = "Collection rate & write-off rate"; chart_rows(c3, kpw, ["cr", "wo"], K)
c3.y_axis.number_format = "0%"; dw.add_chart(c3, "D21")
c4 = LineChart(); c4.title = "Cumulative equity vs total debt (LCY)"; chart_rows(c4, kpw, ["eq_cum", "debt"], K)
dw.add_chart(c4, "M21")
note(dw, "A8", "Series order: Revenue, EBITDA | Tier 1..5 | Collection, Write-off | Equity, Debt.")

# =====================================================================
# COVER
# =====================================================================
cov.column_dimensions["A"].width = 30
cov.column_dimensions["B"].width = 100
info = [("Model", "SHS / PAYGo Company Financial & Investment Model - MTF Tiers 1-5"),
        ("Version", f"{VERSION} - development build, generated {date.today().isoformat()}"),
        ("Status", "Draft for expert review. Default inputs are illustrative, not benchmarks."),
        ("Currency", "Model currency = LCY. Hardware, RBF and term debt in USD, converted at the Timeline FX path."),
        ("Periodicity", f"Monthly over {MONTHS} months; annual roll-ups on Annual, KPIs and Valuation."),
        ("Master check", None)]
for k_, (a_, b_) in enumerate(info):
    label(cov, f"A{4 + k_}", a_, bold=True)
    if b_:
        label(cov, f"B{4 + k_}", b_)
put_calc(cov, "B9", f"={MASTER}", "@", bold=True)
cov["B9"].font = Font(name=FONT, bold=True, color="C00000")
label(cov, "A11", "How to use", bold=True, color=NAVY, size=11)
steps = ["1. Inputs - scenario, macro, volumes, opex, RBF, financing, covenants, valuation (yellow = review first).",
         "2. Products - five MTF tiers: specification, PAYGo price plan, cost to serve, credit risk, recovery, RBF, advance rate.",
         "3. Scenarios - Base / Downside / Severe levers.",
         "4. Read Investment_Summary, then Dashboard, KPIs, Valuation, Covenants and Unit_Economics.",
         "5. Audit trail: FS -> Ops -> Cohort_T1..T5 -> Curves. Every number traces back to Inputs or Products.",
         "6. The master check must read OK before any output is used."]
for k_, s_ in enumerate(steps):
    label(cov, f"B{12 + k_}", s_)
label(cov, "A19", "Sheet index", bold=True, color=NAVY, size=11)
index = [("Investment_Summary", "One-page investment committee / lender summary"),
         ("Inputs", "Global inputs"), ("Products", "Tiers 1-5: specification, price plans, risk"),
         ("Scenarios", "Stress levers"), ("Dashboard", "Charts"), ("KPIs", "Portfolio, financial and lender KPIs"),
         ("Valuation", "DCF and investor IRR / MOIC"), ("Covenants", "Monthly covenant tests"),
         ("Unit_Economics", "Per-unit economics by tier"), ("Sensitivity", "Static scenario & sensitivity snapshot"),
         ("Annual", "Annual statements"), ("FS", "Monthly statements"), ("Ops", "Portfolio engine"),
         ("Costs", "Costs, working capital, capex"), ("Financing", "Equity, term loan, receivables facility"),
         ("Curves", "Per-unit repayment curves"), ("Cohort_T1", "Vintage matrices (one sheet per tier)"),
         ("Timeline", "Dates, FX, indices"), ("Glossary", "PAYGo & SHS terms"), ("Checks", "Integrity checks")]
for k_, (sh, d_) in enumerate(index):
    cell = cov[f"A{20 + k_}"]
    cell.value = sh
    cell.hyperlink = f"#'{sh}'!A1"
    cell.font = Font(name=FONT, color="0563C1", underline="single")
    label(cov, f"B{20 + k_}", d_)
base = 20 + len(index) + 1
label(cov, f"A{base}", "Colour code", bold=True, color=NAVY, size=11)
label(cov, f"A{base + 1}", "1,000", color=BLUE); label(cov, f"B{base + 1}", "Blue = hard-coded input")
cov[f"A{base + 2}"] = "1,000"; cov[f"A{base + 2}"].font = Font(name=FONT, color=BLUE)
cov[f"A{base + 2}"].fill = PatternFill("solid", fgColor="FFFF00"); label(cov, f"B{base + 2}", "Yellow fill = key assumption")
label(cov, f"A{base + 3}", "1,000"); label(cov, f"B{base + 3}", "Black = formula")
label(cov, f"A{base + 4}", "1,000", color=GREEN); label(cov, f"B{base + 4}", "Green = link from another sheet")
label(cov, f"A{base + 6}", "Disclaimer", bold=True, color=NAVY, size=11)
cov[f"B{base + 6}"] = ("Decision-support tool. Not investment, legal, tax or accounting advice. Default inputs are illustrative. "
                       "Accounting simplifications (revenue recognition, ECL without staging, tax, valuation) are listed in the "
                       "user manual. Users are responsible for their inputs and conclusions.")
cov[f"B{base + 6}"].alignment = Alignment(wrap_text=True, vertical="top")
cov[f"B{base + 6}"].font = Font(name=FONT, size=9)
cov.row_dimensions[base + 6].height = 40

# =====================================================================
# ORDER, PRINT SETUP, SNAPSHOT, SAVE
# =====================================================================
order = ["Cover", "Investment_Summary", "Inputs", "Products", "Scenarios", "Dashboard", "KPIs", "Valuation",
         "Covenants", "Unit_Economics", "Sensitivity", "Annual", "FS", "Ops", "Costs", "Financing", "Curves"] + \
        [f"Cohort_T{j + 1}" for j in range(NP)] + ["Timeline", "Glossary", "Checks"]
wb._sheets = [wb[n] for n in order]


def fill_snapshot():
    from shadow_shs import sensitivity_cases
    cases = sensitivity_cases()
    for k_, (name, res) in enumerate(cases):
        r0 = SENS_ROW0 + k_
        label(snw, f"A{r0}", name, bold=k_ < 3)
        for m, (key, text, scale, fmt) in enumerate(SENS_METRICS):
            v = res[key]
            if isinstance(v, float) and v != v:  # NaN (e.g. IRR undefined when no positive flows)
                v, scale = "n/a", 1
            cell = snw.cell(r0, 2 + m, v * scale if isinstance(v, (int, float)) else v)
            cell.number_format = fmt
            cell.font = Font(name=FONT, bold=k_ < 3)
    end = SENS_ROW0 + len(cases)
    note(snw, f"A{end + 1}", f"Snapshot generated {date.today().isoformat()} at default inputs (tools/shs_defaults.py) by the Python "
         "twin, which reproduces the workbook exactly (QA in the volume README). Refresh: python tools/build_shs_model.py --snapshot")
    ch = BarChart(); ch.type = "bar"; ch.title = "Investor IRR by case (static)"
    ch.add_data(Reference(snw, min_col=7, max_col=7, min_row=SENS_ROW0, max_row=end - 1), titles_from_data=False)
    ch.set_categories(Reference(snw, min_col=1, max_col=1, min_row=SENS_ROW0, max_row=end - 1))
    ch.height, ch.width = 9, 18
    snw.add_chart(ch, f"A{end + 3}")


if "--snapshot" in sys.argv:
    fill_snapshot()
else:
    note(snw, f"A{SENS_ROW0 + 12}", "Snapshot not generated. Run: python tools/build_shs_model.py --snapshot")

for wsx in wb.worksheets:
    set_font_all(wsx)
    wsx.page_setup.orientation = "landscape"
    wsx.page_setup.fitToWidth = 1
    wsx.page_setup.fitToHeight = 0
    wsx.sheet_properties.pageSetUpPr.fitToPage = True
wb.calculation = CalcProperties(fullCalcOnLoad=True)
wb.properties.title = "AEF Volume 2 - SHS PAYGo Company Financial & Investment Model"
wb.properties.creator = "Africa Energy Finance"
OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(OUT)
