"""Build Volume 2 - SHS / PAYGo Company Financial Model (v0.1).

Run:  python tools/build_shs_model.py
Out:  volumes/02-solar-home-systems/model/AEF_SHS_PAYGo_Model_v0.1.xlsx

All default inputs are ILLUSTRATIVE placeholders for a fictional company operating
in a fictional market ("LCY" = local currency). They are not benchmarks unless a
source is cited in the cell comment.
"""

from pathlib import Path

from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from aef_engine import (BLUE, FMT_DATE, FMT_INT, FMT_NUM, FMT_NUM2, FMT_PCT, FMT_X,
                        FONT, GREEN, NAVY, ModelBook, col, header_row, label,
                        put_calc, put_input, q, set_font_all)

VERSION = "v0.1"
MONTHS = 60
YEARS = MONTHS // 12
MAX_AGE = 60
OUT = Path(__file__).resolve().parents[1] / "volumes/02-solar-home-systems/model" / f"AEF_SHS_PAYGo_Model_{VERSION}.xlsx"

from shs_defaults import PRODUCTS  # noqa: E402

NP = len(PRODUCTS)
PCOLS = ["C", "D", "E"]  # product columns on Products sheet

ILLUS = "Illustrative placeholder - replace with company data."

mb = ModelBook(MONTHS)
wb = mb.wb
INP = {}  # key -> absolute ref


def inp_ref(ws, cell):
    c, r = cell.rstrip("0123456789"), cell[len(cell.rstrip("0123456789")):]
    return f"{q(ws.title)}!${c}${r}"


# =====================================================================
# 1. COVER
# =====================================================================
cov = mb.sheet("Cover", "AFRICA ENERGY FINANCE - Business & Financial Models",
               "Volume 2 - Solar Home Systems: PAYGo Company Financial Model", tab=NAVY)
cov.column_dimensions["A"].width = 30
cov.column_dimensions["B"].width = 90
rows = [
    ("Model", "SHS / PAYGo Company Financial Model"),
    ("Version", VERSION + " (development build - not for sale)"),
    ("Status", "Draft for expert review. Default inputs are illustrative, not benchmarks."),
    ("Currency", "Model currency = LCY (local currency). Hardware and term debt in USD, converted at the Timeline FX rate."),
    ("Periodicity", f"Monthly, {MONTHS} months; annual summaries on 'Annual' and 'KPIs'."),
    ("Master check", None),
]
for k, (a, b) in enumerate(rows):
    label(cov, f"A{4 + k}", a, bold=True)
    if b:
        label(cov, f"B{4 + k}", b)
label(cov, "A12", "How to use", bold=True, color=NAVY, size=11)
steps = [
    "1. Inputs: set scenario, macro, volumes, opex, financing (blue cells; yellow = key assumptions).",
    "2. Products: set price plan, hardware cost, CAC and credit-risk parameters per product.",
    "3. Scenarios: review Base / Downside / Severe levers.",
    "4. Review Curves (per-unit repayment behaviour) and Unit_Economics (LTV/CAC, payback, unit IRR).",
    "5. Review FS (monthly statements), Annual, KPIs and Dashboard.",
    "6. Confirm the master check on this sheet reads OK before using any output.",
]
for k, s in enumerate(steps):
    label(cov, f"B{13 + k}", s)
label(cov, "A20", "Sheet map", bold=True, color=NAVY, size=11)
sheetmap = [
    ("Inputs", "Scenario selector, macro, volumes, opex, working capital, financing"),
    ("Products", "Product catalogue, PAYGo price plans, CAC, credit-risk parameters"),
    ("Scenarios", "Base / Downside / Severe levers and the active values"),
    ("Timeline", "Dates, years, FX path, inflation and price indices"),
    ("Curves", "Per-unit repayment, default and cash-flow curves by account age"),
    ("Cohort_P1..P3", "Monthly vintage (cohort) matrices: collections, active accounts, balance at risk"),
    ("Ops", "Units, deposits, instalments due, collections, write-offs, ECL, receivables drivers"),
    ("Costs", "COGS, opex, inventory, payables, capex and depreciation"),
    ("Financing", "Equity, USD term loan (with FX), receivables-backed facility"),
    ("FS", "Monthly P&L, balance sheet, cash flow"),
    ("Annual", "Annual statements"),
    ("KPIs", "PAYGo portfolio KPIs (PERFORM-style) and financial KPIs"),
    ("Unit_Economics", "Per-unit economics, LTV/CAC, payback, unit IRR"),
    ("Dashboard", "Key charts"),
    ("Checks", "Integrity checks"),
]
for k, (a, b) in enumerate(sheetmap):
    label(cov, f"A{21 + k}", a)
    label(cov, f"B{21 + k}", b)
label(cov, "A37", "Colour code", bold=True, color=NAVY, size=11)
label(cov, "A38", "1,000", color=BLUE)
label(cov, "B38", "Blue = hard-coded input")
cov["A39"] = "1,000"
cov["A39"].font = Font(name=FONT, color=BLUE)
cov["A39"].fill = PatternFill("solid", fgColor="FFFF00")
label(cov, "B39", "Yellow fill = key assumption to review first")
label(cov, "A40", "1,000")
label(cov, "B40", "Black = formula")
label(cov, "A41", "1,000", color=GREEN)
label(cov, "B41", "Green = link from another sheet")
label(cov, "A43", "Disclaimer", bold=True, color=NAVY, size=11)
cov["B43"] = ("This model is a decision-support tool. It is not investment, legal, tax or accounting advice. "
              "Simplifications are documented in the user manual (revenue recognition, IFRS 9 provisioning, "
              "tax). Users are responsible for their inputs and conclusions.")
cov["B43"].alignment = Alignment(wrap_text=True, vertical="top")
cov["B43"].font = Font(name=FONT, size=9)
cov.row_dimensions[43].height = 48

# =====================================================================
# 2. INPUTS
# =====================================================================
ws = mb.sheet("Inputs", "Inputs", "Blue = input. Yellow = key assumption. All defaults illustrative.", tab="0000FF")
ws.column_dimensions["A"].width = 52
ws.column_dimensions["C"].width = 18
ws.column_dimensions["D"].width = 60


def add_input(key, row, text, unit, value, fmt=FMT_NUM, keyflag=False, note=ILLUS):
    label(ws, f"A{row}", text)
    label(ws, f"B{row}", unit, size=9, color="595959")
    put_input(ws, f"C{row}", value, fmt, keyflag, None)
    if note:
        label(ws, f"D{row}", note, size=9, italic=True, color="595959")
    INP[key] = inp_ref(ws, f"C{row}")


mb.section(ws, 4, "Scenario & model settings")
add_input("scenario", 5, "Active scenario (1 = Base, 2 = Downside, 3 = Severe)", "#", 1, FMT_INT, True,
          "Drives the levers on the Scenarios sheet.")
dv = DataValidation(type="whole", operator="between", formula1="1", formula2="3", allow_blank=False)
ws.add_data_validation(dv)
dv.add("C5")
add_input("start", 6, "First model month (period end)", "date", "2027-01-31", FMT_DATE, False,
          "Enter as a date (period end of month 1).")
ws["C6"] = "=DATE(2027,1,31)"
ws["C6"].font = Font(name=FONT, color=BLUE)
add_input("currency", 7, "Local currency label", "text", "LCY", "@", False, "Display label only.")

mb.section(ws, 9, "Macro")
add_input("fx0", 10, "Opening FX rate", "LCY per USD", 130, FMT_NUM2, True)
add_input("infl", 11, "Local inflation (opex indexation)", "% p.a.", 0.06, FMT_PCT, False)
add_input("tax", 12, "Corporate income tax rate", "%", 0.30, FMT_PCT, False,
          "Simplified: tax losses carried forward indefinitely, tax paid in the month incurred.")
add_input("price_g", 13, "Annual price increase on NEW contracts", "% p.a.", 0.05, FMT_PCT, True,
          "Applies to new cohorts only; existing contracts keep their price plan.")

mb.section(ws, 15, "Sales volume (Base, before scenario multiplier)")
for y in range(1, YEARS + 1):
    add_input(f"vol{y}", 15 + y, f"Units sold - Year {y}", "units", [12000, 24000, 36000, 45000, 50000][y - 1],
              FMT_NUM, y == 1)

mb.section(ws, 22, "Operating costs")
add_input("mm_fee", 23, "Mobile-money / payment fees", "% of cash collected", 0.02, FMT_PCT)
add_input("cs_cost", 24, "Customer service & collections cost", "LCY / active account / month", 60, FMT_NUM)
add_input("staff", 25, "Staff costs (fixed, month 1 level)", "LCY / month", 6_500_000, FMT_NUM, True)
add_input("ga", 26, "G&A, rent, IT (fixed, month 1 level)", "LCY / month", 2_600_000, FMT_NUM)
add_input("warranty", 27, "Warranty & after-sales provision", "% of landed HW cost", 0.05, FMT_PCT)
add_input("duty", 28, "Freight, duty & clearing", "% of USD FOB cost", 0.20, FMT_PCT)

mb.section(ws, 30, "Working capital & capex")
add_input("inv_cover", 31, "Inventory cover", "months of COGS", 2, FMT_NUM2)
add_input("ap_days", 32, "Supplier credit on hardware", "days", 60, FMT_INT)
add_input("capex", 33, "Fixed capex (vehicles, IT, depots)", "LCY / month", 650_000, FMT_NUM)
add_input("dep_life", 34, "Depreciation life of fixed capex", "months", 36, FMT_INT)
add_input("min_cash", 35, "Minimum cash balance", "LCY", 65_000_000, FMT_NUM, True,
          "Shortfalls below this level are covered by an automatic equity injection (funding requirement).")

mb.section(ws, 37, "Financing")
add_input("eq0", 38, "Initial equity (month 1)", "LCY", 390_000_000, FMT_NUM, True)
add_input("tl_amt", 39, "USD term loan - amount", "USD", 2_000_000, FMT_NUM, True)
add_input("tl_month", 40, "USD term loan - drawdown month", "month #", 6, FMT_INT)
add_input("tl_rate", 41, "USD term loan - interest rate", "% p.a.", 0.10, FMT_PCT)
add_input("tl_grace", 42, "USD term loan - grace period after drawdown", "months", 12, FMT_INT)
add_input("tl_amort", 43, "USD term loan - amortisation period", "months", 36, FMT_INT)
add_input("rf_limit", 44, "Receivables facility (LCY) - limit", "LCY", 1_300_000_000, FMT_NUM, True)
add_input("rf_adv", 45, "Receivables facility - advance rate", "% of eligible receivables", 0.70, FMT_PCT, True)
add_input("rf_rate", 46, "Receivables facility - interest rate", "% p.a.", 0.16, FMT_PCT)
add_input("rf_start", 47, "Receivables facility - first available month", "month #", 7, FMT_INT)

# =====================================================================
# 3. PRODUCTS
# =====================================================================
pw = mb.sheet("Products", "Product catalogue & PAYGo price plans",
              "One column per product. Blue = input. Derived values in black.", tab="0000FF")
pw.column_dimensions["A"].width = 50
for c in PCOLS:
    pw.column_dimensions[c].width = 22
pw.column_dimensions["F"].width = 50
header_row(pw, 4, ["Parameter", "Unit"] + [p["name"] for p in PRODUCTS] + ["Notes"])
PR = {}  # key -> list of refs per product

prod_rows = [
    ("name", "Product name", "text", "name", "@", False, ""),
    ("price", "Cash (list) price", "LCY", "price", FMT_NUM, True, "Price if paid upfront. Basis of hardware revenue."),
    ("deposit", "PAYGo deposit", "LCY", "deposit", FMT_NUM, True, ""),
    ("daily", "PAYGo daily rate", "LCY / day", "daily", FMT_NUM, True, ""),
    ("tenor", "PAYGo tenor", "months", "tenor", FMT_INT, True, "Max 60."),
    ("hw", "Hardware FOB cost", "USD / unit", "hw", FMT_NUM2, True, ""),
    ("comm", "Agent commission per sale", "LCY / unit", "comm", FMT_NUM, False, ""),
    ("mkt", "Marketing & acquisition cost per sale", "LCY / unit", "mkt", FMT_NUM, False, ""),
    ("mix", "Sales mix", "% of units", "mix", FMT_PCT, True, "Must sum to 100% (see Checks)."),
    ("hazard", "Base monthly default hazard", "% of performing accounts / month", "hazard", FMT_PCT, True,
     "Share of still-paying accounts that stop paying each month. Scenario multiplier applied."),
    ("coll", "Base collection rate on performing accounts", "% of instalment", "coll", FMT_PCT, True,
     "Partial / late payment of performing accounts. Scenario multiplier applied, capped at 100%."),
]
r0 = 5
for k, (key, text, unit, field, fmt, keyflag, note) in enumerate(prod_rows):
    r = r0 + k
    label(pw, f"A{r}", text)
    label(pw, f"B{r}", unit, size=9, color="595959")
    PR[key] = []
    for j, p in enumerate(PRODUCTS):
        put_input(pw, f"{PCOLS[j]}{r}", p[field], fmt, keyflag)
        PR[key].append(f"Products!${PCOLS[j]}${r}")
    label(pw, f"F{r}", note or ILLUS, size=9, italic=True, color="595959")

mb.section(pw, 17, "Derived price-plan metrics")
derived = [
    ("inst", "Monthly instalment (daily rate x 30.42)", "LCY / month",
     lambda j: f"={PR['daily'][j]}*365/12", FMT_NUM),
    ("contract", "Total PAYGo contract value", "LCY", lambda j: f"={PR['deposit'][j]}+{PR['inst'][j]}*{PR['tenor'][j]}", FMT_NUM),
    ("markup", "PAYGo financing mark-up over cash price", "LCY", lambda j: f"={PR['contract'][j]}-{PR['price'][j]}", FMT_NUM),
    ("markup_pct", "Mark-up as % of cash price", "%", lambda j: f"=IF({PR['price'][j]}=0,0,{PR['markup'][j]}/{PR['price'][j]})", FMT_PCT),
    ("financed", "Amount financed at sale (cash price - deposit)", "LCY", lambda j: f"={PR['price'][j]}-{PR['deposit'][j]}", FMT_NUM),
    ("hazard_s", "Scenario monthly default hazard", "%", lambda j: f"={PR['hazard'][j]}*Scenarios!$G$6", FMT_PCT),
    ("coll_s", "Scenario collection rate on performing", "%", lambda j: f"=MIN(1,{PR['coll'][j]}*Scenarios!$G$7)", FMT_PCT),
    ("landed", "Landed hardware cost at opening FX (scenario)", "LCY / unit",
     lambda j: f"={PR['hw'][j]}*(1+{INP['duty']})*{INP['fx0']}*Scenarios!$G$9", FMT_NUM),
    ("cac", "Customer acquisition cost (commission + marketing)", "LCY / unit", lambda j: f"={PR['comm'][j]}+{PR['mkt'][j]}", FMT_NUM),
]
for k, (key, text, unit, fn, fmt) in enumerate(derived):
    r = 18 + k
    label(pw, f"A{r}", text)
    label(pw, f"B{r}", unit, size=9, color="595959")
    PR[key] = [f"Products!${PCOLS[j]}${r}" for j in range(NP)]
    for j in range(NP):
        put_calc(pw, f"{PCOLS[j]}{r}", fn(j), fmt)

# =====================================================================
# 4. SCENARIOS
# =====================================================================
sw = mb.sheet("Scenarios", "Scenario levers", "Multipliers / overrides applied to Base inputs. Active column follows Inputs!C5.", tab="0000FF")
sw.column_dimensions["A"].width = 46
for c in "CDEFG":
    sw.column_dimensions[c].width = 14
header_row(sw, 5, ["Lever", "Unit", "Base", "Downside", "Severe", "", "ACTIVE"])
levers = [
    (6, "Default hazard multiplier", "x", (1.0, 1.5, 2.0), FMT_NUM2),
    (7, "Collection-rate multiplier (performing accounts)", "x", (1.0, 0.95, 0.88), FMT_NUM2),
    (8, "Sales volume multiplier", "x", (1.0, 0.85, 0.70), FMT_NUM2),
    (9, "Hardware cost multiplier (USD)", "x", (1.0, 1.05, 1.10), FMT_NUM2),
    (10, "LCY depreciation vs USD", "% p.a.", (0.05, 0.15, 0.30), FMT_PCT),
]
for r, text, unit, vals, fmt in levers:
    label(sw, f"A{r}", text)
    label(sw, f"B{r}", unit, size=9, color="595959")
    for c, v in zip("CDE", vals):
        put_input(sw, f"{c}{r}", v, fmt, False)
    put_calc(sw, f"G{r}", f"=CHOOSE({INP['scenario']},C{r},D{r},E{r})", fmt, bold=True)
label(sw, "A12", "Scenario names", bold=True)
for c, n in zip("CDE", ["Base", "Downside", "Severe"]):
    put_input(sw, f"{c}12", n, "@")
put_calc(sw, "G12", f"=CHOOSE({INP['scenario']},C12,D12,E12)", "@", bold=True)
label(sw, "A14", "Downside/Severe levers are illustrative stress settings. Calibrate them to the company's own "
      "cohort history and to sector data before use.", italic=True, size=9, color="595959")
label(sw, "A15", "Context: ESMAP Off-Grid Solar Market Trends Report 2024 reports a sector PAYGo collection rate of "
      "about 62% (2023) - see sources/source-register.md.", italic=True, size=9, color="595959")

# =====================================================================
# 5. TIMELINE
# =====================================================================
T = "Timeline"
tw = mb.sheet(T, "Timeline", "Dates, FX and indices")
mb.time_header(tw)
for i in range(1, MONTHS + 1):
    c = col(i)
    tw[f"{c}4"] = i
    tw[f"{c}5"] = f"=EOMONTH({INP['start']},{i - 1})"
    tw[f"{c}6"] = f"=INT(({c}4-1)/12)+1"
    for rr, fmt in ((4, FMT_INT), (5, FMT_DATE), (6, FMT_INT)):
        tw[f"{c}{rr}"].number_format = fmt
        tw[f"{c}{rr}"].font = Font(name=FONT, bold=True, color="FFFFFF")
mb.register(T, "fx", 8)
mb.write_row(tw, 8, "FX rate", "LCY / USD", lambda i, c, p: f"={p}8*(1+Scenarios!$G$10)^(1/12)",
             FMT_NUM2, opening=f"={INP['fx0']}")
tw["D8"].font = Font(name=FONT, color=GREEN)
mb.register(T, "infl", 9)
mb.write_row(tw, 9, "Opex inflation index", "index", lambda i, c, p: f"=(1+{INP['infl']})^(({c}$4-1)/12)", FMT_NUM2)
mb.register(T, "pidx", 10)
mb.write_row(tw, 10, "Price index on new contracts", "index", lambda i, c, p: f"=(1+{INP['price_g']})^(({c}$4-1)/12)", FMT_NUM2)
mb.register(T, "vol", 11)
mb.write_row(tw, 11, "Total units sold (scenario)", "units",
             lambda i, c, p: f"=CHOOSE({c}$6,{','.join(INP[f'vol{y}'] for y in range(1, YEARS + 1))})/12*Scenarios!$G$8",
             FMT_NUM, total="sum")

# =====================================================================
# 6. CURVES  (per-unit behaviour by account age, vertical)
# =====================================================================
cw = mb.sheet("Curves", "Per-unit repayment curves by account age",
              "Age 0 = month of sale. One block per product. Values are per unit, in month-1 prices (cohorts are scaled by the price index).")
CURVE_COLS = ["Survival (still paying)", "Instalment due", "Collected", "Missed (written off)",
              "Receivable at risk", "Active account", "Net cash flow / unit", "Cumulative cash flow"]
AGE_ROW0 = 8  # age 0 row
CB = []  # per product: dict field -> column letter
cw.column_dimensions["A"].width = 8
for j in range(NP):
    start = 2 + j * (len(CURVE_COLS) + 1)
    letters = {}
    from openpyxl.utils import get_column_letter as gcl
    for k, name in enumerate(CURVE_COLS):
        letters[k] = gcl(start + k)
        cw.column_dimensions[letters[k]].width = 13
    CB.append(letters)
    cw.cell(5, start, PRODUCTS[j]["name"]).font = Font(name=FONT, bold=True, color=NAVY)
    header_row(cw, 6, CURVE_COLS, start_col=start)
    cw.row_dimensions[6].height = 30
header_row(cw, 6, ["Age (m)"], start_col=1)
for a in range(0, MAX_AGE + 1):
    r = AGE_ROW0 + a
    put_calc(cw, f"A{r}", a, FMT_INT)
    for j in range(NP):
        L = CB[j]
        T_ = PR["tenor"][j]
        inst = PR["inst"][j]
        inT = f"AND($A{r}>=1,$A{r}<={T_})"
        # survival: share of accounts still paying at age a
        put_calc(cw, f"{L[0]}{r}", "=1" if a == 0 else f"=(1-{PR['hazard_s'][j]})^$A{r}", FMT_PCT)
        put_calc(cw, f"{L[1]}{r}", f"=IF({inT},{inst},0)", FMT_NUM)
        put_calc(cw, f"{L[2]}{r}", f"={L[1]}{r}*{PR['coll_s'][j]}*{L[0]}{r}", FMT_NUM)
        put_calc(cw, f"{L[3]}{r}", f"={L[1]}{r}-{L[2]}{r}", FMT_NUM)
        put_calc(cw, f"{L[4]}{r}", f"=(1-{L[0]}{r})*MAX(0,{T_}-$A{r})*({inst}-{PR['markup'][j]}/{T_})", FMT_NUM)
        put_calc(cw, f"{L[5]}{r}", f"=IF($A{r}<={T_},{L[0]}{r},0)", FMT_PCT)
        if a == 0:
            ncf = (f"={PR['deposit'][j]}*(1-{INP['mm_fee']})-{PR['landed'][j]}*(1+{INP['warranty']})"
                   f"-{PR['cac'][j]}")
            put_calc(cw, f"{L[7]}{r}", f"={L[6]}{r}", FMT_NUM)
        else:
            ncf = f"={L[2]}{r}*(1-{INP['mm_fee']})-{INP['cs_cost']}*{L[5]}{r}"
            put_calc(cw, f"{L[7]}{r}", f"={L[7]}{r - 1}+{L[6]}{r}", FMT_NUM)
        put_calc(cw, f"{L[6]}{r}", ncf, FMT_NUM)
LAST_AGE_ROW = AGE_ROW0 + MAX_AGE
# summary rows
SUMR = LAST_AGE_ROW + 2
label(cw, f"A{SUMR}", "Totals per unit (month-1 prices)", bold=True, color=NAVY)
CURVE_TOT = {"due": [], "coll": [], "missed": []}
for j in range(NP):
    L = CB[j]
    for k, key in ((1, "due"), (2, "coll"), (3, "missed")):
        cell = f"{L[k]}{SUMR}"
        put_calc(cw, cell, f"=SUM({L[k]}{AGE_ROW0}:{L[k]}{LAST_AGE_ROW})", FMT_NUM, bold=True)
        CURVE_TOT[key].append(f"Curves!${L[k]}${SUMR}")


def curve_range(j, k):
    L = CB[j][k]
    return f"Curves!${L}${AGE_ROW0}:${L}${LAST_AGE_ROW}"


# =====================================================================
# 7. OPS (part 1: units) - needed by cohort sheets
# =====================================================================
O = "Ops"
ow = mb.sheet(O, "Operations & portfolio", "Per product, then totals. LCY unless stated.")
mb.time_header(ow)
OPS_FIELDS = [
    ("units", "Units sold", "units", "sum"),
    ("iunits", "Price-indexed units (units x price index)", "units", "sum"),
    ("deposits", "Deposits collected", "LCY", "sum"),
    ("hw_rev", "Hardware revenue (cash price)", "LCY", "sum"),
    ("financed", "New receivables originated (cash price - deposit)", "LCY", "sum"),
    ("due", "Instalments due", "LCY", "sum"),
    ("coll", "Instalments collected", "LCY", "sum"),
    ("missed", "Missed instalments written off", "LCY", "sum"),
    ("fin_inc", "PAYGo financing income (straight-line over tenor)", "LCY", "sum"),
    ("ecl", "Expected credit loss charge at origination", "LCY", "sum"),
    ("active", "Active (paying, in-tenor) accounts", "accounts", "last"),
    ("rar", "Receivables at risk (carrying amount of accounts that stopped paying)", "LCY", "last"),
    ("cogs", "Landed hardware cost of units sold", "LCY", "sum"),
]
row = 8
for j in range(NP):
    mb.section(ow, row, PRODUCTS[j]["name"])
    ow.cell(row, 1).value = f"={PR['name'][j]}"
    row += 1
    for key, text, unit, tot in OPS_FIELDS:
        mb.register(O, f"{key}{j}", row)
        row += 1
    row += 1
mb.section(ow, row, "TOTAL - all products")
row += 1
for key, text, unit, tot in OPS_FIELDS:
    mb.register(O, f"{key}T", row)
    row += 1
mb.register(O, "coll_rate", row + 1)
mb.register(O, "wo_rate", row + 2)


# =====================================================================
# 8. COHORT SHEETS
# =====================================================================
COH_BLOCKS = [("coll", "Instalments collected by cohort (LCY)", 2, True),
              ("active", "Active accounts by cohort", 5, False),
              ("rar", "Receivables at risk by cohort (LCY)", 4, True)]
for j in range(NP):
    name = f"Cohort_P{j + 1}"
    hw_ = mb.sheet(name, f"Cohort (vintage) matrix - {PRODUCTS[j]['name']}",
                   "Rows = sales cohort (month of sale); columns = calendar month. Cohort size in column C.")
    mb.time_header(hw_)
    hw_.column_dimensions["A"].width = 30
    rr = 8
    for bkey, btitle, k, indexed in COH_BLOCKS:
        mb.section(hw_, rr, btitle)
        tot_row = rr + 1
        mb.register(name, f"{bkey}_tot", tot_row)
        first = rr + 2
        last = first + MONTHS - 1
        mb.write_row(hw_, tot_row, "Total", "", lambda i, c, p, f=first, l=last: f"=SUM({c}{f}:{c}{l})",
                     FMT_NUM, bold=True)
        units_key = f"iunits{j}" if indexed else f"units{j}"
        for ci in range(1, MONTHS + 1):
            r = first + ci - 1
            hw_.cell(r, 1, f"Cohort month {ci}").font = Font(name=FONT, size=9)
            hw_.cell(r, 2, ci).font = Font(name=FONT, size=9)
            put_calc(hw_, f"C{r}", f"=INDEX({mb.range_(O, units_key)},1,$B{r})", FMT_NUM, link=True)
            for i in range(1, MONTHS + 1):
                c = col(i)
                if i > ci:
                    hw_[f"{c}{r}"] = f"=$C{r}*INDEX({curve_range(j, k)},{c}$4-$B{r}+1)"
                    hw_[f"{c}{r}"].number_format = FMT_NUM
                    hw_[f"{c}{r}"].font = Font(name=FONT, size=9)
        rr = last + 2

# =====================================================================
# 9. OPS (part 2: formulas)
# =====================================================================


def R(sheet, key, c):
    return mb.ref(sheet, key, c, this_sheet=O)


for j in range(NP):
    T_ = PR["tenor"][j]
    ranges_iu = mb.range_(O, f"iunits{j}", this_sheet=O)
    idx = f"Timeline!${col(1)}$4:${mb.last}$4"
    window = lambda c: (f"SUMIFS({ranges_iu},{idx},\">=\"&({c}$4-{T_}),{idx},\"<=\"&({c}$4-1))")
    spec = {
        "units": (lambda i, c, p: f"=Timeline!{c}$11*{PR['mix'][j]}", True),
        "iunits": (lambda i, c, p: f"={R(O, f'units{j}', c)}*Timeline!{c}$10", False),
        "deposits": (lambda i, c, p: f"={R(O, f'iunits{j}', c)}*{PR['deposit'][j]}", False),
        "hw_rev": (lambda i, c, p: f"={R(O, f'iunits{j}', c)}*{PR['price'][j]}", False),
        "financed": (lambda i, c, p: f"={R(O, f'iunits{j}', c)}*{PR['financed'][j]}", False),
        "due": (lambda i, c, p: f"={PR['inst'][j]}*{window(c)}", False),
        "coll": (lambda i, c, p: f"=Cohort_P{j + 1}!{c}${mb.r(f'Cohort_P{j + 1}', 'coll_tot')}", True),
        "missed": (lambda i, c, p: f"={R(O, f'due{j}', c)}-{R(O, f'coll{j}', c)}", False),
        "fin_inc": (lambda i, c, p: f"=IF({T_}=0,0,{PR['markup'][j]}/{T_}*{window(c)})", False),
        "ecl": (lambda i, c, p: f"={R(O, f'iunits{j}', c)}*{CURVE_TOT['missed'][j]}", False),
        "active": (lambda i, c, p: f"=Cohort_P{j + 1}!{c}${mb.r(f'Cohort_P{j + 1}', 'active_tot')}", True),
        "rar": (lambda i, c, p: f"=Cohort_P{j + 1}!{c}${mb.r(f'Cohort_P{j + 1}', 'rar_tot')}", True),
        "cogs": (lambda i, c, p: f"={R(O, f'units{j}', c)}*{PR['hw'][j]}*(1+{INP['duty']})*Timeline!{c}$8*Scenarios!$G$9", False),
    }
    for key, text, unit, tot in OPS_FIELDS:
        fn, link = spec[key]
        mb.write_row(ow, mb.r(O, f"{key}{j}"), text, unit, fn, FMT_NUM, total=tot, link=link)
for key, text, unit, tot in OPS_FIELDS:
    mb.write_row(ow, mb.r(O, f"{key}T"), text, unit,
                 lambda i, c, p, k=key: "=" + "+".join(R(O, f"{k}{j}", c) for j in range(NP)),
                 FMT_NUM, bold=True, total=tot)
mb.write_row(ow, mb.r(O, "coll_rate"), "Portfolio collection rate (collected / due, excl. deposits)", "%",
             lambda i, c, p: f"=IF({R(O, 'dueT', c)}=0,0,{R(O, 'collT', c)}/{R(O, 'dueT', c)})", FMT_PCT,
             comment="PERFORM-style definition: follow-on payments collected / scheduled, excluding deposits.")
mb.write_row(ow, mb.r(O, "wo_rate"), "Write-off rate (missed / due)", "%",
             lambda i, c, p: f"=IF({R(O, 'dueT', c)}=0,0,{R(O, 'missedT', c)}/{R(O, 'dueT', c)})", FMT_PCT)

# =====================================================================
# 10. COSTS
# =====================================================================
C_ = "Costs"
kw = mb.sheet(C_, "Operating costs, working capital & capex", "LCY")
mb.time_header(kw)
cost_rows = [
    ("cogs", "Cost of goods sold (landed hardware)", lambda i, c, p: f"={mb.ref(O, 'cogsT', c)}", "sum", True),
    ("warranty", "Warranty & after-sales", lambda i, c, p: f"={c}{{cogs}}*{INP['warranty']}", "sum", False),
    ("comm", "Agent commissions", lambda i, c, p: "=" + "+".join(f"{mb.ref(O, f'units{j}', c)}*{PR['comm'][j]}*Timeline!{c}$9" for j in range(NP)), "sum", False),
    ("mkt", "Marketing & acquisition", lambda i, c, p: "=" + "+".join(f"{mb.ref(O, f'units{j}', c)}*{PR['mkt'][j]}*Timeline!{c}$9" for j in range(NP)), "sum", False),
    ("mm", "Mobile-money / payment fees", lambda i, c, p: f"=({mb.ref(O, 'depositsT', c)}+{mb.ref(O, 'collT', c)})*{INP['mm_fee']}", "sum", False),
    ("cs", "Customer service & collections", lambda i, c, p: f"={mb.ref(O, 'activeT', c)}*{INP['cs_cost']}*Timeline!{c}$9", "sum", False),
    ("staff", "Staff", lambda i, c, p: f"={INP['staff']}*Timeline!{c}$9", "sum", False),
    ("ga", "G&A, rent, IT", lambda i, c, p: f"={INP['ga']}*Timeline!{c}$9", "sum", False),
    ("opex", "Total operating expenses (excl. COGS, ECL)", lambda i, c, p: f"=SUM({c}{{warranty}}:{c}{{ga}})", "sum", False),
    (None, None, None, None, None),
    ("inv", "Inventory (closing)", lambda i, c, p: f"={c}{{cogs}}*{INP['inv_cover']}", "last", False),
    ("purch", "Hardware purchases", lambda i, c, p: f"={c}{{cogs}}+{c}{{inv}}-{p}{{inv}}", "sum", False),
    ("ap", "Supplier payables (closing)", lambda i, c, p: f"={c}{{purch}}*{INP['ap_days']}/(365/12)", "last", False),
    (None, None, None, None, None),
    ("capex", "Fixed capex", lambda i, c, p: f"={INP['capex']}*Timeline!{c}$9", "sum", False),
    ("dep", "Depreciation (straight-line, by vintage)",
     lambda i, c, p: f"=SUMIFS(${col(1)}{{capex}}:{c}{{capex}},${col(1)}$4:{c}$4,\">\"&({c}$4-{INP['dep_life']}))/{INP['dep_life']}",
     "sum", False),
    ("ppe", "Net fixed assets (closing)", lambda i, c, p: f"={p}{{ppe}}+{c}{{capex}}-{c}{{dep}}", "last", False),
]
rr = 8
for key, *_ in cost_rows:
    if key:
        mb.register(C_, key, rr)
    rr += 1
rr = 8
for key, text, fn, tot, link in cost_rows:
    if key:
        rowmap = {k: mb.r(C_, k) for k, *_ in cost_rows if k}
        mb.write_row(kw, rr, text, "LCY",
                     lambda i, c, p, fn=fn, rm=rowmap: fn(i, c, p).format(**rm),
                     FMT_NUM, total=tot, bold=key == "opex", link=link)
    rr += 1

# =====================================================================
# 11. FINANCING
# =====================================================================
F = "Financing"
fw = mb.sheet(F, "Financing", "Equity, USD term loan (with FX translation), receivables-backed facility")
mb.time_header(fw)
fin_rows = [
    ("sec_eq", "EQUITY"),
    ("eq_init", "Initial equity injection"),
    ("eq_top", "Automatic equity top-up (funding requirement)"),
    ("eq_cum", "Cumulative equity invested"),
    ("sec_tl", "USD TERM LOAN"),
    ("tl_draw_usd", "Drawdown (USD)"),
    ("tl_rep_usd", "Repayment (USD)"),
    ("tl_bal_usd", "Closing balance (USD)"),
    ("tl_int", "Interest (LCY)"),
    ("tl_draw", "Drawdown (LCY)"),
    ("tl_rep", "Repayment (LCY)"),
    ("tl_bal", "Closing balance (LCY)"),
    ("fx_loss", "Unrealised FX loss / (gain) on USD debt (LCY)"),
    ("sec_rf", "RECEIVABLES FACILITY (LCY)"),
    ("rf_elig", "Eligible receivables (gross receivables - receivables at risk)"),
    ("rf_bb", "Borrowing base (advance rate x eligible)"),
    ("rf_bal", "Facility drawn (closing)"),
    ("rf_flow", "Net drawdown / (repayment)"),
    ("rf_int", "Interest"),
    ("rf_util", "Utilisation of limit"),
]
rr = 8
for key, _ in fin_rows:
    mb.register(F, key, rr)
    rr += 1


def FR(key, c):
    return mb.ref(F, key, c, this_sheet=F)


S = "FS"
# FS rows registered later; use helper that resolves lazily
fs_ref = lambda key, c: mb.ref(S, key, c, this_sheet=F)

fin_spec = {
    "eq_init": (lambda i, c, p: f"=IF({c}$4=1,{INP['eq0']},0)", "sum", FMT_NUM),
    "eq_top": (lambda i, c, p: f"={fs_ref('eq_top', c)}", "sum", FMT_NUM),
    "eq_cum": (lambda i, c, p: f"={p}{mb.r(F, 'eq_cum')}+{c}{mb.r(F, 'eq_init')}+{c}{mb.r(F, 'eq_top')}", "last", FMT_NUM),
    "tl_draw_usd": (lambda i, c, p: f"=IF({c}$4={INP['tl_month']},{INP['tl_amt']},0)", "sum", FMT_NUM),
    "tl_rep_usd": (lambda i, c, p: (
        f"=IF(AND({c}$4>{INP['tl_month']}+{INP['tl_grace']},{c}$4<={INP['tl_month']}+{INP['tl_grace']}+{INP['tl_amort']}),"
        f"MIN({p}{mb.r(F, 'tl_bal_usd')},{INP['tl_amt']}/{INP['tl_amort']}),0)"), "sum", FMT_NUM),
    "tl_bal_usd": (lambda i, c, p: f"={p}{mb.r(F, 'tl_bal_usd')}+{c}{mb.r(F, 'tl_draw_usd')}-{c}{mb.r(F, 'tl_rep_usd')}", "last", FMT_NUM),
    "tl_int": (lambda i, c, p: f"={p}{mb.r(F, 'tl_bal_usd')}*{INP['tl_rate']}/12*Timeline!{c}$8", "sum", FMT_NUM),
    "tl_draw": (lambda i, c, p: f"={c}{mb.r(F, 'tl_draw_usd')}*Timeline!{c}$8", "sum", FMT_NUM),
    "tl_rep": (lambda i, c, p: f"={c}{mb.r(F, 'tl_rep_usd')}*Timeline!{c}$8", "sum", FMT_NUM),
    "tl_bal": (lambda i, c, p: f"={c}{mb.r(F, 'tl_bal_usd')}*Timeline!{c}$8", "last", FMT_NUM),
    "fx_loss": (lambda i, c, p: f"={p}{mb.r(F, 'tl_bal_usd')}*(Timeline!{c}$8-Timeline!{p}$8)", "sum", FMT_NUM),
    "rf_elig": (lambda i, c, p: f"=MAX(0,{fs_ref('grossrec', c)}-{mb.ref(O, 'rarT', c, this_sheet=F)})", "last", FMT_NUM),
    "rf_bb": (lambda i, c, p: f"={c}{mb.r(F, 'rf_elig')}*{INP['rf_adv']}", "last", FMT_NUM),
    "rf_bal": (lambda i, c, p: f"=IF({c}$4>={INP['rf_start']},MIN({INP['rf_limit']},{c}{mb.r(F, 'rf_bb')}),0)", "last", FMT_NUM),
    "rf_flow": (lambda i, c, p: f"={c}{mb.r(F, 'rf_bal')}-{p}{mb.r(F, 'rf_bal')}", "sum", FMT_NUM),
    "rf_int": (lambda i, c, p: f"={p}{mb.r(F, 'rf_bal')}*{INP['rf_rate']}/12", "sum", FMT_NUM),
    "rf_util": (lambda i, c, p: f"=IF({INP['rf_limit']}=0,0,{c}{mb.r(F, 'rf_bal')}/{INP['rf_limit']})", "max", FMT_PCT),
}
# Timeline!D8 holds opening FX so fx_loss month 1 uses it (opening USD balance is 0 anyway).

# =====================================================================
# 12. FINANCIAL STATEMENTS (monthly)
# =====================================================================
sw_ = mb.sheet(S, "Financial statements (monthly)", "LCY. Simplified IFRS-style presentation; see manual for accounting simplifications.")
mb.time_header(sw_)
fs_rows = [
    ("sec_pl", "INCOME STATEMENT", None, None, None),
    ("rev_hw", "Hardware revenue (cash price)", lambda c, p: f"={mb.ref(O, 'hw_revT', c, this_sheet=S)}", "sum", True),
    ("rev_fin", "PAYGo financing income", lambda c, p: f"={mb.ref(O, 'fin_incT', c, this_sheet=S)}", "sum", True),
    ("rev", "Total revenue", lambda c, p: f"={c}{{rev_hw}}+{c}{{rev_fin}}", "sum", False),
    ("cogs", "Cost of goods sold", lambda c, p: f"=-{mb.ref(C_, 'cogs', c, this_sheet=S)}", "sum", True),
    ("gp", "Gross profit", lambda c, p: f"={c}{{rev}}+{c}{{cogs}}", "sum", False),
    ("opex", "Operating expenses", lambda c, p: f"=-{mb.ref(C_, 'opex', c, this_sheet=S)}", "sum", True),
    ("ecl", "Credit loss expense (ECL)", lambda c, p: f"=-{mb.ref(O, 'eclT', c, this_sheet=S)}", "sum", True),
    ("ebitda", "EBITDA", lambda c, p: f"={c}{{gp}}+{c}{{opex}}+{c}{{ecl}}", "sum", False),
    ("da", "Depreciation", lambda c, p: f"=-{mb.ref(C_, 'dep', c, this_sheet=S)}", "sum", True),
    ("ebit", "EBIT", lambda c, p: f"={c}{{ebitda}}+{c}{{da}}", "sum", False),
    ("int_tl", "Interest - USD term loan", lambda c, p: f"=-{mb.ref(F, 'tl_int', c, this_sheet=S)}", "sum", True),
    ("int_rf", "Interest - receivables facility", lambda c, p: f"=-{mb.ref(F, 'rf_int', c, this_sheet=S)}", "sum", True),
    ("fx", "FX (loss) / gain on USD debt", lambda c, p: f"=-{mb.ref(F, 'fx_loss', c, this_sheet=S)}", "sum", True),
    ("pbt", "Profit before tax", lambda c, p: f"={c}{{ebit}}+{c}{{int_tl}}+{c}{{int_rf}}+{c}{{fx}}", "sum", False),
    ("cum_pbt", "  memo: cumulative PBT", lambda c, p: f"={p}{{cum_pbt}}+{c}{{pbt}}", "last", False),
    ("max_cum", "  memo: running max of cumulative PBT", lambda c, p: f"=MAX({p}{{max_cum}},{c}{{cum_pbt}})", "last", False),
    ("tax", "Income tax", lambda c, p: f"=-{INP['tax']}*(MAX(0,{c}{{max_cum}})-MAX(0,{p}{{max_cum}}))", "sum", False),
    ("ni", "Net income", lambda c, p: f"={c}{{pbt}}+{c}{{tax}}", "sum", False),
    ("blank1", None, None, None, None),
    ("sec_bs", "BALANCE SHEET", None, None, None),
    ("cash", "Cash", lambda c, p: f"={c}{{cash_end}}", "last", False),
    ("grossrec", "PAYGo receivables - gross",
     lambda c, p: (f"={p}{{grossrec}}+{mb.ref(O, 'financedT', c, this_sheet=S)}+{mb.ref(O, 'fin_incT', c, this_sheet=S)}"
                   f"-{mb.ref(O, 'collT', c, this_sheet=S)}-{mb.ref(O, 'missedT', c, this_sheet=S)}"), "last", False),
    ("prov", "Loss allowance (ECL provision)",
     lambda c, p: f"={p}{{prov}}-{mb.ref(O, 'eclT', c, this_sheet=S)}+{mb.ref(O, 'missedT', c, this_sheet=S)}", "last", False),
    ("netrec", "PAYGo receivables - net", lambda c, p: f"={c}{{grossrec}}+{c}{{prov}}", "last", False),
    ("inv", "Inventory", lambda c, p: f"={mb.ref(C_, 'inv', c, this_sheet=S)}", "last", True),
    ("ppe", "Net fixed assets", lambda c, p: f"={mb.ref(C_, 'ppe', c, this_sheet=S)}", "last", True),
    ("ta", "Total assets", lambda c, p: f"={c}{{cash}}+{c}{{netrec}}+{c}{{inv}}+{c}{{ppe}}", "last", False),
    ("ap", "Supplier payables", lambda c, p: f"={mb.ref(C_, 'ap', c, this_sheet=S)}", "last", True),
    ("tl", "USD term loan (in LCY)", lambda c, p: f"={mb.ref(F, 'tl_bal', c, this_sheet=S)}", "last", True),
    ("rf", "Receivables facility", lambda c, p: f"={mb.ref(F, 'rf_bal', c, this_sheet=S)}", "last", True),
    ("tl_", "Total liabilities", lambda c, p: f"={c}{{ap}}+{c}{{tl}}+{c}{{rf}}", "last", False),
    ("sc", "Share capital", lambda c, p: f"={mb.ref(F, 'eq_cum', c, this_sheet=S)}", "last", True),
    ("re", "Retained earnings", lambda c, p: f"={p}{{re}}+{c}{{ni}}", "last", False),
    ("te", "Total equity", lambda c, p: f"={c}{{sc}}+{c}{{re}}", "last", False),
    ("tle", "Total liabilities & equity", lambda c, p: f"={c}{{tl_}}+{c}{{te}}", "last", False),
    ("bs_chk", "Balance check (should be 0)", lambda c, p: f"=ROUND({c}{{ta}}-{c}{{tle}},0)", "max", False),
    ("blank2", None, None, None, None),
    ("sec_cf", "CASH FLOW STATEMENT", None, None, None),
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
    ("cf_eq0", "Equity - initial / scheduled", lambda c, p: f"={mb.ref(F, 'eq_init', c, this_sheet=S)}", "sum", False),
    ("cash_pre", "Cash before equity top-up", lambda c, p: f"={p}{{cash_end}}+{c}{{cfo}}+{c}{{cfi}}+{c}{{cf_tl}}+{c}{{cf_rf}}+{c}{{cf_eq0}}", "last", False),
    ("eq_top", "Equity top-up to maintain minimum cash", lambda c, p: f"=MAX(0,{INP['min_cash']}-{c}{{cash_pre}})", "sum", False),
    ("cash_end", "Closing cash", lambda c, p: f"={c}{{cash_pre}}+{c}{{eq_top}}", "last", False),
]
rr = 8
for key, text, fn, tot, link in fs_rows:
    mb.register(S, key, rr)
    rr += 1
fsmap = {k: mb.r(S, k) for k, *_ in fs_rows}
for key, text, fn, tot, link in fs_rows:
    r = mb.r(S, key)
    if text is None:
        continue
    if fn is None:
        mb.section(sw_, r, text)
        continue
    mb.write_row(sw_, r, text, "LCY", lambda i, c, p, fn=fn: fn(c, p).format(**fsmap), FMT_NUM, total=tot,
                 bold=key in ("rev", "gp", "ebitda", "ebit", "pbt", "ni", "ta", "tle", "netrec", "cfo", "cash_end"),
                 link=link)

# now write financing rows (FS refs exist)
for key, text in fin_rows:
    r = mb.r(F, key)
    if key.startswith("sec_"):
        mb.section(fw, r, text)
        continue
    fn, tot, fmt = fin_spec[key]
    unit = "USD" if key.endswith("_usd") else ("%" if key == "rf_util" else "LCY")
    mb.write_row(fw, r, text, unit, fn, fmt, total=tot)

# =====================================================================
# 13. ANNUAL
# =====================================================================
A = "Annual"
aw = mb.sheet(A, "Annual summary", "Flows summed by financial year; balances at year end. LCY.")
for y in range(1, YEARS + 1):
    c = col(y)
    aw[f"{c}5"] = f"Year {y}"
    aw[f"{c}5"].font = Font(name=FONT, bold=True, color="FFFFFF")
    aw[f"{c}5"].fill = PatternFill("solid", fgColor=NAVY)
    aw[f"{c}5"].alignment = Alignment(horizontal="right")
    aw.column_dimensions[c].width = 16
    aw[f"{c}6"] = y
    aw[f"{c}6"].font = Font(name=FONT, color="FFFFFF")
    aw[f"{c}6"].fill = PatternFill("solid", fgColor=NAVY)
aw["A5"] = "LCY"
aw["A5"].font = Font(name=FONT, bold=True)
YR = f"Timeline!${col(1)}$6:${mb.last}$6"


def annual_formula(sheet, key, c, kind):
    if kind == "sum":
        return f"=SUMIFS({mb.range_(sheet, key)},{YR},{c}$6)"
    return f"=INDEX({mb.range_(sheet, key)},1,{c}$6*12)"


ann_lines = []
rr = 8
for key, text, fn, tot, link in fs_rows:
    if text is None:
        rr += 1
        continue
    if fn is None:
        mb.section(aw, rr, text)
        aw.cell(rr, 1).value = text
    elif not key.startswith("cum_") and not key.startswith("max_"):
        label(aw, f"A{rr}", text, bold=key in ("rev", "gp", "ebitda", "ni", "ta", "tle", "cfo", "cash_end"))
        for y in range(1, YEARS + 1):
            c = col(y)
            put_calc(aw, f"{c}{rr}", annual_formula(S, key, c, "sum" if tot == "sum" else "last"))
        mb.register(A, key, rr)
    else:
        rr -= 1
    rr += 1
aw.freeze_panes = "B7"

# =====================================================================
# 14. KPIs
# =====================================================================
K = "KPIs"
kpw = mb.sheet(K, "Key performance indicators", "Portfolio KPIs follow PAYGo PERFORM-style definitions where noted (simplified, see manual).")
for y in range(1, YEARS + 1):
    c = col(y)
    kpw[f"{c}5"] = f"Year {y}"
    kpw[f"{c}5"].font = Font(name=FONT, bold=True, color="FFFFFF")
    kpw[f"{c}5"].fill = PatternFill("solid", fgColor=NAVY)
    kpw[f"{c}5"].alignment = Alignment(horizontal="right")
    kpw.column_dimensions[c].width = 16
    kpw[f"{c}6"] = y
    kpw[f"{c}6"].font = Font(name=FONT, color="FFFFFF")
    kpw[f"{c}6"].fill = PatternFill("solid", fgColor=NAVY)


def ann(sheet, key, c, kind="sum"):
    f = annual_formula(sheet, key, c, kind)
    return f[1:]


kpi_rows = [
    ("sec", "Portfolio"),
    ("units", "Units sold", lambda c: "=" + ann(O, "unitsT", c), FMT_NUM),
    ("active", "Active accounts (year end)", lambda c: "=" + ann(O, "activeT", c, "last"), FMT_NUM),
    ("cr", "Collection rate (collected / due, excl. deposits)",
     lambda c: f"=IFERROR({ann(O, 'collT', c)}/{ann(O, 'dueT', c)},0)", FMT_PCT),
    ("wo", "Write-off rate (missed / due)", lambda c: f"=IFERROR({ann(O, 'missedT', c)}/{ann(O, 'dueT', c)},0)", FMT_PCT),
    ("rar", "Receivables at risk / gross receivables (year end)",
     lambda c: f"=IFERROR({ann(O, 'rarT', c, 'last')}/{ann(S, 'grossrec', c, 'last')},0)", FMT_PCT),
    ("cov", "Loss allowance coverage (allowance / gross receivables)",
     lambda c: f"=IFERROR(-{ann(S, 'prov', c, 'last')}/{ann(S, 'grossrec', c, 'last')},0)", FMT_PCT),
    ("sec", "Profitability"),
    ("rev", "Revenue (LCY)", lambda c: "=" + ann(S, "rev", c), FMT_NUM),
    ("gm", "Gross margin", lambda c: f"=IFERROR({ann(S, 'gp', c)}/{ann(S, 'rev', c)},0)", FMT_PCT),
    ("ebitda_m", "EBITDA margin", lambda c: f"=IFERROR({ann(S, 'ebitda', c)}/{ann(S, 'rev', c)},0)", FMT_PCT),
    ("ni", "Net income (LCY)", lambda c: "=" + ann(S, "ni", c), FMT_NUM),
    ("rev_usd", "Revenue (USD, at average FX)",
     lambda c: f"=IFERROR({ann(S, 'rev', c)}/AVERAGEIFS(Timeline!${col(1)}$8:${mb.last}$8,{YR},{c}$6),0)", FMT_NUM),
    ("sec", "Funding & leverage"),
    ("cash", "Closing cash (LCY)", lambda c: "=" + ann(S, "cash_end", c, "last"), FMT_NUM),
    ("eq_cum", "Cumulative equity invested (LCY)", lambda c: "=" + ann(F, "eq_cum", c, "last"), FMT_NUM),
    ("eq_top", "Equity top-ups in year (funding gap, LCY)", lambda c: "=" + ann(S, "eq_top", c), FMT_NUM),
    ("debt", "Total debt (year end, LCY)", lambda c: f"={ann(S, 'tl', c, 'last')}+{ann(S, 'rf', c, 'last')}", FMT_NUM),
    ("de", "Debt / equity (book)", lambda c: f"=IFERROR(({ann(S, 'tl', c, 'last')}+{ann(S, 'rf', c, 'last')})/{ann(S, 'te', c, 'last')},0)", FMT_X),
    ("dscr", "Debt service coverage ((CFO + interest) / (interest + term-loan principal))",
     lambda c: (f"=IFERROR(({ann(S, 'cfo', c)}-{ann(S, 'int_tl', c)}-{ann(S, 'int_rf', c)})/"
                f"({ann(F, 'tl_int', c)}+{ann(F, 'tl_rep', c)}+{ann(F, 'rf_int', c)}),0)"), FMT_X),
    ("fx", "FX rate (year end, LCY/USD)", lambda c: f"=INDEX(Timeline!${col(1)}$8:${mb.last}$8,1,{c}$6*12)", FMT_NUM2),
]
rr = 8
for item in kpi_rows:
    if item[0] == "sec":
        mb.section(kpw, rr, item[1])
    else:
        key, text, fn, fmt = item
        label(kpw, f"A{rr}", text)
        for y in range(1, YEARS + 1):
            c = col(y)
            put_calc(kpw, f"{c}{rr}", fn(c), fmt)
        mb.register(K, key, rr)
    rr += 1
label(kpw, f"A{rr + 1}", "Peak cumulative equity requirement (LCY)", bold=True)
put_calc(kpw, f"C{rr + 1}", f"=MAX({mb.range_(F, 'eq_cum')})", FMT_NUM, bold=True)
label(kpw, f"A{rr + 2}", "Peak cumulative equity requirement (USD, at opening FX)", bold=True)
put_calc(kpw, f"C{rr + 2}", f"=C{rr + 1}/{INP['fx0']}", FMT_NUM, bold=True)
PEAK_EQ = f"KPIs!$C${rr + 1}"
label(kpw, f"A{rr + 4}", "DSCR is shown for information; covenant definitions vary by lender. Balance-at-risk is a "
      "model approximation of PERFORM 'Receivables at Risk' (accounts that have stopped paying).", italic=True, size=9,
      color="595959")

# =====================================================================
# 15. UNIT ECONOMICS
# =====================================================================
U = "Unit_Economics"
uw = mb.sheet(U, "Unit economics (per unit, month-1 prices, active scenario)", "Lifetime view of one PAYGo customer per product.")
uw.column_dimensions["A"].width = 52
for c in PCOLS:
    uw.column_dimensions[c].width = 22
header_row(uw, 4, ["Metric", "Unit"] + [p["name"] for p in PRODUCTS])
ue_rows = [
    ("Cash price", "LCY", lambda j: f"={PR['price'][j]}", FMT_NUM),
    ("Total contract value", "LCY", lambda j: f"={PR['contract'][j]}", FMT_NUM),
    ("Deposit", "LCY", lambda j: f"={PR['deposit'][j]}", FMT_NUM),
    ("Expected instalments collected", "LCY", lambda j: f"={CURVE_TOT['coll'][j]}", FMT_NUM),
    ("Expected lifetime cash collected (deposit + instalments)", "LCY", lambda j: f"=C7+C8".replace("C", PCOLS[j]), FMT_NUM),
    ("Expected loss rate (missed / scheduled instalments)", "%",
     lambda j: f"=IFERROR({CURVE_TOT['missed'][j]}/{CURVE_TOT['due'][j]},0)", FMT_PCT),
    ("Lifetime collection rate (collected / contract value)", "%", lambda j: f"=IFERROR({PCOLS[j]}9/{PCOLS[j]}6,0)", FMT_PCT),
    ("Landed hardware cost", "LCY", lambda j: f"={PR['landed'][j]}", FMT_NUM),
    ("Warranty provision", "LCY", lambda j: f"={PR['landed'][j]}*{INP['warranty']}", FMT_NUM),
    ("Customer acquisition cost (CAC)", "LCY", lambda j: f"={PR['cac'][j]}", FMT_NUM),
    ("Payment fees + servicing over life", "LCY",
     lambda j: f"={PCOLS[j]}9*{INP['mm_fee']}+{INP['cs_cost']}*SUM({curve_range(j, 5)})-{INP['cs_cost']}", FMT_NUM),
    ("Contribution per unit (lifetime, undiscounted)", "LCY",
     lambda j: f"={PCOLS[j]}9-{PCOLS[j]}12-{PCOLS[j]}13-{PCOLS[j]}14-{PCOLS[j]}15", FMT_NUM),
    ("LTV / CAC (lifetime gross profit after credit losses / CAC)", "x",
     lambda j: f"=IFERROR(({PCOLS[j]}9-{PCOLS[j]}12-{PCOLS[j]}13-{PCOLS[j]}15)/{PCOLS[j]}14,0)", FMT_X),
    ("Cash payback (months after sale)", "months",
     lambda j: f"=IF(COUNTIF({curve_range(j, 7)},\"<0\")>{MAX_AGE},\"Not paid back\",COUNTIF({curve_range(j, 7)},\"<0\"))", FMT_INT),
    ("Unit IRR (annualised, unlevered)", "%",
     lambda j: f"=IFERROR((1+IRR({curve_range(j, 6)},0.02))^12-1,\"n/a\")", FMT_PCT),
]
for k, (text, unit, fn, fmt) in enumerate(ue_rows):
    r = 5 + k
    label(uw, f"A{r}", text, bold=k in (11, 12, 14))
    label(uw, f"B{r}", unit, size=9, color="595959")
    for j in range(NP):
        put_calc(uw, f"{PCOLS[j]}{r}", fn(j), fmt, bold=k in (11, 12, 14))
label(uw, "A22", "Note: the active-account servicing cost excludes age 0 (sale month). Payback counts months with "
      "negative cumulative cash flow, ages 0..60. Values in month-1 prices; later cohorts scale with the price index.",
      italic=True, size=9, color="595959")

# =====================================================================
# 16. CHECKS
# =====================================================================
X = "Checks"
xw = mb.sheet(X, "Integrity checks", "Each check returns 0 when OK. Master check feeds the Cover.", tab="FF0000")
xw.column_dimensions["A"].width = 60
header_row(xw, 4, ["Check", "Unit", "Result (0 = OK)"])
checks = [
    ("Balance sheet balances (max abs difference, all months)",
     f"=MAX(MAX({mb.range_(S, 'bs_chk')}),-MIN({mb.range_(S, 'bs_chk')}))"),
    ("Sales mix sums to 100%", f"=IF(ABS(SUM(Products!$C$13:$E$13)-1)>0.0001,1,0)"),
    ("Closing cash never below minimum cash", f"=IF(MIN({mb.range_(S, 'cash_end')})<{INP['min_cash']}-1,1,0)"),
    ("Gross receivables never negative", f"=IF(MIN({mb.range_(S, 'grossrec')})<-1,1,0)"),
    ("Loss allowance never positive (contra-asset)", f"=IF(MAX({mb.range_(S, 'prov')})>1,1,0)"),
    ("Facility within limit", f"=IF(MAX({mb.range_(F, 'rf_bal')})>{INP['rf_limit']}+1,1,0)"),
    ("Cash flow ties to balance-sheet cash",
     f"=IF(ABS(FS!{mb.last}{mb.r(S, 'cash')}-FS!{mb.last}{mb.r(S, 'cash_end')})>1,1,0)"),
    ("Tenors within model limit (<= 60 months)", f"=IF(MAX(Products!$C$9:$E$9)>{MAX_AGE},1,0)"),
    ("Scenario selector valid (1-3)", f"=IF(OR({INP['scenario']}<1,{INP['scenario']}>3),1,0)"),
]
for k, (text, f) in enumerate(checks):
    r = 5 + k
    label(xw, f"A{r}", text)
    label(xw, f"B{r}", "flag")
    put_calc(xw, f"C{r}", f, FMT_NUM)
mr = 5 + len(checks) + 1
label(xw, f"A{mr}", "MASTER CHECK", bold=True)
put_calc(xw, f"C{mr}", f"=IF(SUM(C5:C{mr - 2})=0,\"OK\",\"ERROR\")", "@", bold=True)
cov["B9"] = f"=Checks!C{mr}"
cov["B9"].font = Font(name=FONT, bold=True, color="C00000")

# =====================================================================
# 17. DASHBOARD
# =====================================================================
D = "Dashboard"
dw = mb.sheet(D, "Dashboard", "Active scenario shown in Scenarios!G12. Charts read from Annual / KPIs.", tab="00B050")
label(dw, "A4", "Active scenario")
put_calc(dw, "B4", "=Scenarios!G12", "@", bold=True, link=True)
label(dw, "A5", "Peak equity requirement (LCY)")
put_calc(dw, "B5", f"={PEAK_EQ}", FMT_NUM, bold=True, link=True)
label(dw, "A6", "Peak equity requirement (USD at opening FX)")
put_calc(dw, "B6", f"={PEAK_EQ}/{INP['fx0']}", FMT_NUM, bold=True)
label(dw, "A7", "Master check")
put_calc(dw, "B7", f"=Checks!C{mr}", "@", bold=True, link=True)
dw.column_dimensions["B"].width = 18

ch = BarChart()
ch.title = "Revenue and EBITDA (LCY)"
ch.y_axis.title = "LCY"
data_rows = [mb.r(A, "rev"), mb.r(A, "ebitda")]
for drow in data_rows:
    ref = Reference(aw, min_col=5, max_col=4 + YEARS, min_row=drow)
    ch.add_data(ref, from_rows=True, titles_from_data=False)
ch.set_categories(Reference(aw, min_col=5, max_col=4 + YEARS, min_row=5))
ch.height, ch.width = 8, 16
dw.add_chart(ch, "D4")

lc = LineChart()
lc.title = "Collection rate and write-off rate"
for key in ("cr", "wo"):
    lc.add_data(Reference(kpw, min_col=5, max_col=4 + YEARS, min_row=mb.r(K, key)), from_rows=True, titles_from_data=False)
lc.set_categories(Reference(kpw, min_col=5, max_col=4 + YEARS, min_row=5))
lc.y_axis.number_format = "0%"
lc.height, lc.width = 8, 16
dw.add_chart(lc, "D21")

lc2 = LineChart()
lc2.title = "Cumulative equity vs. debt (LCY)"
for key in ("eq_cum", "debt"):
    lc2.add_data(Reference(kpw, min_col=5, max_col=4 + YEARS, min_row=mb.r(K, key)), from_rows=True, titles_from_data=False)
lc2.set_categories(Reference(kpw, min_col=5, max_col=4 + YEARS, min_row=5))
lc2.height, lc2.width = 8, 16
dw.add_chart(lc2, "N4")
label(dw, "A10", "Chart series order: bar = Revenue, EBITDA; line 1 = Collection rate, Write-off rate; "
      "line 2 = Cumulative equity, Total debt.", italic=True, size=9, color="595959")

# ---------------------------------------------------------------------
order = ["Cover", "Inputs", "Products", "Scenarios", "Dashboard", "KPIs", "Annual", "Unit_Economics", "FS", "Ops",
         "Costs", "Financing", "Curves", "Cohort_P1", "Cohort_P2", "Cohort_P3", "Timeline", "Checks"]
wb._sheets = [wb[n] for n in order]
for wsx in wb.worksheets:
    set_font_all(wsx)
from openpyxl.workbook.properties import CalcProperties
wb.calculation = CalcProperties(fullCalcOnLoad=True)
wb.properties.title = "AEF Volume 2 - SHS PAYGo Company Financial Model"
wb.properties.creator = "Africa Energy Finance"
OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(OUT)
