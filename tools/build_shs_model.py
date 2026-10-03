"""Build MODEL 2 (Book 2) - PAYGo Company Financial & Investment Model for solar home systems.

Run:  python tools/build_shs_model.py [--snapshot]
Out:  volumes/02-solar-home-systems/model/AEF_SHS_PAYGo_Model_<VERSION>.xlsx

--snapshot  also fills the static 'Sensitivity' sheet using the verified Python twin
            (tools/shadow_shs.py). Without it the sheet is left empty.

All default inputs live in tools/shs_defaults.py and are ILLUSTRATIVE placeholders
for a fictional company in a fictional market ("LCY" = local currency).
"""

import copy
import re
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

VERSION = "v0.8-dev"  # development build towards v0.8; the v0.7 release files are kept unchanged
CASE = None
if "--case" in sys.argv:  # e.g. --case solarapay : apply a worked-case input set before anything is built
    import importlib
    CASE_MOD = importlib.import_module(f"cases.{sys.argv[sys.argv.index('--case') + 1]}")
    CASE_MOD.apply(G, PRODUCTS)
    CASE = CASE_MOD.CASE
YEARS = MONTHS // 12
NP = len(PRODUCTS)
PCOLS = [gcl(3 + j) for j in range(NP)]  # C..G on Products / Unit_Economics
OUT = (Path(__file__).resolve().parents[1] / "volumes/02-solar-home-systems/model"
       / f"AEF_SHS_PAYGo_Model_{VERSION}.xlsx")
if CASE:
    OUT = Path(__file__).resolve().parents[1] / CASE["out"].replace("v0.7", VERSION)
ILLUS = "Illustrative placeholder - replace with company data."
GREY_TXT = "595959"
# M4: provenance of every input (brief section 13). Default inputs are model assumptions for a fictional company;
# a worked case may relabel inputs through CASE_MOD.PROVENANCE ({input key: label}).
PROV_LABELS = ["MODEL ASSUMPTION", "COMPANY DATA", "EXTERNAL EVIDENCE", "CALIBRATED ASSUMPTION", "UNVERIFIED"]
PROV_FILL = {"MODEL ASSUMPTION": "DDEBF7", "COMPANY DATA": "E2EFDA", "EXTERNAL EVIDENCE": "FFF2CC",
             "CALIBRATED ASSUMPTION": "EDE2F6", "UNVERIFIED": "FCE4D6"}
PROV_DEFAULT = {"tier": "UNVERIFIED"}  # MTF thresholds: ESMAP framework report not yet read (Source_Register E3)
PROV_OVERRIDE = dict(getattr(CASE_MOD, "PROVENANCE", {})) if CASE else {}
PROV_NOTES = dict(getattr(CASE_MOD, "PROVENANCE_NOTES", {})) if CASE else {}
PROV_CELLS = []  # (sheet, cell) of every provenance label, summarised on Start


def prov_of(key):
    return PROV_OVERRIDE.get(key, PROV_DEFAULT.get(key, "MODEL ASSUMPTION"))


def put_prov(ws_, cell, key):
    v = prov_of(key)
    ws_[cell] = v
    ws_[cell].font = Font(name=FONT, size=8, bold=True, color="404040")
    ws_[cell].fill = PatternFill("solid", fgColor=PROV_FILL[v])
    ws_[cell].alignment = Alignment(horizontal="center", vertical="center")
    PROV_CELLS.append((ws_.title, cell))

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
cov = wb.create_sheet("Cover")  # branded cover page, filled at the end
cts = mb.sheet("Contents", "Contents - how to use this model",
               "MODEL 2  |  PAYGo Company Financial & Investment Model  |  Book 2, PAYGo Solar Finance", tab=NAVY)
stw = mb.sheet("Start", "Start here", "What to input, what the model calculates, what the results mean and what an investor should look at.",
               tab="00B050")
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
ws.column_dimensions["E"].width = 24
header_row(ws, 3, ["Input", "Unit", "Value", "Note", "Provenance"])


def add_input(key, row, text, unit, value, fmt=FMT_NUM, keyflag=False, n=ILLUS):
    label(ws, f"A{row}", text)
    label(ws, f"B{row}", unit, size=9, color=GREY_TXT)
    put_input(ws, f"C{row}", value, fmt, keyflag)
    if n:
        note(ws, f"D{row}", n)
    put_prov(ws, f"E{row}", key)
    INP[key] = absref(ws, f"C{row}")


r = 4
mb.section(ws, r, "Scenario & settings"); r += 1
add_input("scenario", r, "Active scenario (1 = Base, 2 = Downside, 3 = Severe)", "#", G["scenario"], FMT_INT, True,
          "Drives the levers on the Scenarios sheet.")
dv = DataValidation(type="whole", operator="between", formula1="1", formula2="3")
ws.add_data_validation(dv); dv.add(f"C{r}"); r += 1
add_input("start", r, "First model month (period end)", "date", None, FMT_DATE, False, "Period-end date of month 1.")
ws[f"C{r}"] = "=DATE(2027,1,31)"; ws[f"C{r}"].font = Font(name=FONT, color=BLUE); r += 1
add_input("currency", r, "Local currency label", "text", G.get("currency", "LCY"), "@", False, "Display only."); r += 2

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
add_input("rbf_lag", r, "Months from sale to RBF disbursement (verification lag)", "months", G["rbf_lag"], FMT_INT); r += 1
add_input("rbf_mode", r, "RBF design mode (1 sales, 2 repayment-linked, 3 ownership-linked, 4 hybrid)", "#", G["rbf_mode"], FMT_INT, True,
          "See RBF_Engine. Ownership-linked RBF pays nothing until validated ownership-at-2x data exist."); r += 1
dv_rbf = DataValidation(type="whole", operator="between", formula1="1", formula2="4"); ws.add_data_validation(dv_rbf); dv_rbf.add(f"C{r - 1}")
add_input("rbf_rr_target", r, "Repayment rate at verification for 100% of repayment-linked RBF", "%", G["rbf_rr_target"], FMT_PCT); r += 1
for k_, nm in enumerate(["sales-based", "repayment-linked", "ownership-linked"]):
    add_input(f"rbf_w{k_ + 1}", r, f"Hybrid weight - {nm}", "%", G["rbf_w"][k_], FMT_PCT, False, "Hybrid weights must sum to 100% (Checks)."); r += 1
add_input("own_evidence", r, "Validated ownership-at-2x evidence available (1 = yes)", "switch", G["own_evidence"], FMT_INT, True,
          "Set to 1 ONLY when Vintage_Input holds validated ownership-at-2x data. Never infer this KPI."); r += 2

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

mb.section(ws, r, "Receivables financing structure"); r += 1
add_input("fin_struct", r, "Structure (1 = warehouse facility, 2 = securitisation / term ABS)", "#", G["fin_struct"], FMT_INT, True,
          "Both are modelled on balance sheet. Option 2 applies the rate, advance-rate haircut and upfront fee below."); r += 1
dv_fs = DataValidation(type="whole", operator="between", formula1="1", formula2="2"); ws.add_data_validation(dv_fs); dv_fs.add(f"C{r - 1}")
add_input("sec_rate", r, "Securitisation - all-in interest rate", "% p.a.", G["sec_rate"], FMT_PCT); r += 1
add_input("sec_adv_mult", r, "Securitisation - advance-rate multiplier vs warehouse", "x", G["sec_adv_mult"], FMT_NUM2); r += 1
add_input("sec_fee", r, "Securitisation - upfront structuring fee on new drawings", "%", G["sec_fee"], FMT_PCT, False,
          "Paid the month after the drawing (avoids a circular reference)."); r += 2

mb.section(ws, r, "Other revenue streams (digital loans, other services)"); r += 1
add_input("other_arpu", r, "Net revenue per active PAYGo account (month-1 level)", "LCY / account / month", G["other_arpu"], FMT_NUM, False,
          "Simplification: take-rate revenue only, no on-balance-sheet lending. 0 = switched off."); r += 1
add_input("other_margin", r, "Gross margin on other revenue", "%", G["other_margin"], FMT_PCT); r += 2

mb.section(ws, r, "Lender covenants (tested on Covenants sheet)"); r += 1
add_input("cov_cr", r, "Minimum trailing-3-month collection rate", "%", G["cov_cr"], FMT_PCT, True); r += 1
add_input("cov_rar", r, "Maximum receivables at risk / gross receivables", "%", G["cov_rar"], FMT_PCT, True); r += 1
add_input("cov_lev", r, "Maximum debt / book equity", "x", G["cov_lev"], FMT_X); r += 1
add_input("cov_dscr", r, "Minimum annual DSCR (years with debt service)", "x", G["cov_dscr"], FMT_X); r += 1
add_input("cov_cash", r, "Minimum liquidity: cash before equity top-up", "LCY", G["cov_cash"]); r += 1
add_input("cov_dpd30", r, "Maximum 30+ DPD receivables / gross receivables", "%", G["cov_dpd30"], FMT_PCT); r += 1
add_input("cov_dpd90", r, "Maximum 90+ DPD receivables / gross receivables", "%", G["cov_dpd90"], FMT_PCT); r += 2

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
PROV_COL = gcl(4 + NP)
pw.column_dimensions[PROV_COL].width = 24
header_row(pw, 4, ["Parameter", "Unit"] + [f"Tier {p['tier']}" for p in PRODUCTS] + ["Notes", "Provenance"])
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
    note(pw, f"{NOTE_COL}{r_}", ((n or ILLUS) + " " + PROV_NOTES[key]) if key in PROV_NOTES else (n or ILLUS))
    put_prov(pw, f"{PROV_COL}{r_}", key)
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
           "Capacity minimums: " + "; ".join(f"T{k} {v}" for k, v in MTF_CAPACITY.items()) + " (ESMAP MTF; to be checked against the framework report).")
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
prod_input("recov", "Gross resale value of repossessed unit", "% of cash price", FMT_PCT, False,
           "Before recovery costs (Credit_Assumptions). Net proceeds are recognised as recoveries against credit losses.")
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
prod_calc("perf2x", "PERFORM ownership horizon (2 x tenor)", "months", lambda j: f"=2*{PR['tenor'][j]}", FMT_INT,
          "Each tier references its own tenor (avoids the cross-tier reference error found in an earlier workbook).")
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
label(sw, "I5", "Provenance", bold=True)
for rr, text, unit, key, fmt in levers:
    put_prov(sw, f"I{rr}", f"lever_{key}")
sw.column_dimensions["I"].width = 24
label(sw, "A13", "Input set loaded on Inputs, Products and Credit_Assumptions", bold=True)
INPUT_SETS = ["Illustrative (model assumptions)", "Management case", "Calibrated case"]
put_input(sw, "C13", INPUT_SETS[2] if CASE else INPUT_SETS[0], "@", True)
dv_is = DataValidation(type="list", formula1='"' + ",".join(INPUT_SETS) + '"', allow_blank=False)
sw.add_data_validation(dv_is); dv_is.add("C13")
label(sw, "F13", "Active case")
put_calc(sw, "G13", "=C13&\", \"&G12", "@", bold=True)
INP["input_set"] = "Scenarios!$C$13"
note(sw, "A14", "Downside / Severe are illustrative stress settings. Calibrate to the company's cohort history and sector data.")
note(sw, "A15", "Context: the ESMAP Off-Grid Solar Market Trends Report 2024 is reported to give an average PAYGo collection rate of about 62% "
     "for 2021-2023 (Source_Register E1-14, PENDING PRIMARY DOCUMENT). A collection rate, not the PERFORM Repayment Rate.")

# =====================================================================
# CREDIT ASSUMPTIONS (v0.4)
# =====================================================================
CA = "Credit_Assumptions"
caw = mb.sheet(CA, "Credit assumptions - DPD buckets, stages, recovery, eligibility",
               "Drives Credit_Engine. Proxy = projection from the model's repayment curves; Actual = company data in Credit_Input. This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS.",
               tab="0000FF")
caw.column_dimensions["A"].width = 58
caw.column_dimensions["C"].width = 16
caw.column_dimensions["D"].width = 70


def ca_input(key, row, text, unit, value, fmt=FMT_NUM, keyflag=False, n=ILLUS):
    label(caw, f"A{row}", text)
    label(caw, f"B{row}", unit, size=9, color=GREY_TXT)
    put_input(caw, f"C{row}", value, fmt, keyflag)
    note(caw, f"D{row}", n)
    put_prov(caw, f"E{row}", key)
    INP[key] = absref(caw, f"C{row}")


mb.section(caw, 4, "Data mode")
ca_input("credit_mode", 5, "Credit data mode (1 = Proxy, 2 = Actual)", "#", G["credit_mode"], FMT_INT, True,
         "Actual mode reads Credit_Input (company history) for reporting. Projections and the facility always use the proxy engine.")
dv_cm = DataValidation(type="whole", operator="between", formula1="1", formula2="2"); caw.add_data_validation(dv_cm); dv_cm.add("C5")
mb.section(caw, 7, "Definitions")
ca_input("dpd_default", 8, "Default definition", "days past due", G["dpd_default"], FMT_INT, True, "Common PAYGo / lender convention; confirm against facility documents.")
ca_input("dpd_s2", 9, "Stage 2 threshold (significant increase in credit risk)", "DPD", G["dpd_s2"], FMT_INT, False, "Indicative IFRS 9-style staging.")
ca_input("dpd_s3", 10, "Stage 3 threshold (credit-impaired)", "DPD", G["dpd_s3"], FMT_INT, False, "Indicative IFRS 9-style staging.")
ca_input("bb_max_dpd", 11, "Borrowing-base eligibility: maximum DPD", "DPD", G["bb_max_dpd"], FMT_INT, True, "Receivables in buckets starting above this DPD are ineligible.")
mb.section(caw, 13, "Recovery, cures and ECL")
label(caw, "A14", "Repossession lag (link to Inputs)"); label(caw, "B14", "months", size=9, color=GREY_TXT)
put_calc(caw, "C14", f"={INP['repo_lag']}", FMT_INT, link=True)
ca_input("recov_cost", 15, "Recovery cost (retrieval, refurbishment, resale)", "% of gross resale", G["recov_cost"], FMT_PCT, True)
ca_input("cure", 16, "Cure rate of Stage-2 balances (ECL only)", "%", G["cure"], FMT_PCT, False,
         "The proxy engine assumes accounts that stop paying do not resume; cures enter only the indicative ECL.")
ca_input("ecl_disc", 17, "Discount rate for indicative ECL", "% p.a.", G["ecl_disc"], FMT_PCT)
mb.section(caw, 19, "Proxy DPD distribution")
ca_input("perf_current", 20, "Paying accounts: share of balances current", "%", G["perf_current"], FMT_PCT, False, "Remainder is 1-30 DPD.")
for k_, nm in enumerate(["31-60", "61-90", "91-180", "180+"]):
    ca_input(f"rar_s{k_ + 1}", 21 + k_, f"Receivables at risk: share {nm} DPD", "%", G["rar_shares"][k_], FMT_PCT, False,
             "Shares of receivables at risk must sum to 100% (Checks).")
mb.section(caw, 26, "Bucket table (derived - do not edit)")
header_row(caw, 27, ["DPD bucket", "Lower DPD", "Upper DPD", "Stage", "BB eligible", "In default", "30+ DPD", "90+ DPD", "Proxy share"])
for c_ in "FGHI":
    caw.column_dimensions[c_].width = 12
caw.column_dimensions["E"].width = 24
BUCKETS = [("Current", 0, 0), ("1-30", 1, 30), ("31-60", 31, 60), ("61-90", 61, 90), ("91-180", 91, 180), ("180+", 181, 9999)]
BK = []
for k_, (nm, lo, hi) in enumerate(BUCKETS):
    r_ = 28 + k_
    label(caw, f"A{r_}", nm)
    put_calc(caw, f"B{r_}", lo, FMT_INT); put_calc(caw, f"C{r_}", hi, FMT_INT)
    put_calc(caw, f"D{r_}", f"=IF(B{r_}>{INP['dpd_s3']},3,IF(B{r_}>{INP['dpd_s2']},2,1))", FMT_INT)
    put_calc(caw, f"E{r_}", f"=IF(B{r_}<={INP['bb_max_dpd']},1,0)", FMT_INT)
    put_calc(caw, f"F{r_}", f"=IF(B{r_}>{INP['dpd_default']},1,0)", FMT_INT)
    put_calc(caw, f"G{r_}", f"=IF(B{r_}>30,1,0)", FMT_INT)
    put_calc(caw, f"H{r_}", f"=IF(B{r_}>90,1,0)", FMT_INT)
    share = (f"={INP['perf_current']}" if k_ == 0 else f"=1-{INP['perf_current']}" if k_ == 1 else f"={INP[f'rar_s{k_ - 1}']}")
    put_calc(caw, f"I{r_}", share, FMT_PCT)
    BK.append({f: f"Credit_Assumptions!${c_}${r_}" for f, c_ in zip(["stage", "elig", "dflt", "p30", "p90", "share"], "DEFGHI")})
note(caw, "A35", "Current and 1-30 shares apply to balances of paying accounts; 31+ shares apply to receivables at risk (accounts that stopped "
     "paying). The 30+/90+ flags use fixed market definitions; stage, eligibility and default follow the thresholds above.")
note(caw, "A36", "The 12-month PD shown by Credit_Engine is a proxy derived from the repayment curve or from observed loss rates. "
     "It is NOT an audited IFRS 9 PD.")
note(caw, "A37", "This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS.")

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
              "Active account", "Defaults at this age", "Net recovery (resale - costs)", "RBF received", "Net cash flow / unit",
              "Cumulative cash flow", "Arrears of stopped accounts"]
CI = {k: n for n, k in enumerate(["surv", "due", "coll", "missed", "rar", "active", "defaults", "recov", "rbf", "ncf", "cum", "arrears"])}
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
                 f"INDEX({crange(j, 'defaults')},$A{rr}-{INP['repo_lag']}+1),0)*{PR['repo'][j]}*{PR['recov'][j]}*{PR['price'][j]}"
                 f"*(1-{INP['recov_cost']})")
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
        put_calc(cw, f"{L_['arrears']}{rr}", f"={L_['due']}{rr}*(1-{L_['surv']}{rr})")
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
    ("elig", "Eligible receivables (Credit_Engine, max-DPD rule)", "LCY", "last"),
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
for key in ("unlocks_cum", "coll_rate", "wo_rate", "rar_ratio", "other_rev", "other_cos"):
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
# DATA-INPUT LAYOUTS (Credit_Input, Vintage_Input) - constants used by engines
# =====================================================================
CI_COLS = ["Obs #", "Period end", "Originations (units)", "Gross receivables", "Current", "1-30 DPD", "31-60 DPD",
           "61-90 DPD", "91-180 DPD", "180+ DPD", "Default EAD (stock beyond default definition)", "Repossessions (units)",
           "Gross resale proceeds", "Recovery costs", "Cures (accounts)", "Write-offs", "Collections",
           "Instalments due", "Ownership events (unlocks)", "Notes"]
CI_KEYS = ["obs", "date", "orig", "gross", "b0", "b1", "b2", "b3", "b4", "b5", "dflt", "repo_units", "resale", "rcost",
           "cures", "wo", "coll", "due", "own", "notes"]
CI_COL = {k: gcl(1 + n) for n, k in enumerate(CI_KEYS)}
CI_R0 = lambda j: 8 + j * (MONTHS + 4)


def ci_range(j, key):
    c_ = CI_COL[key]
    return f"Credit_Input!${c_}${CI_R0(j)}:${c_}${CI_R0(j) + MONTHS - 1}"


VI_METRICS = [("coll", "Cumulative collections"), ("due", "Cumulative instalments due"),
              ("dpd30", "30+ DPD exposure (arrears incl. written off + outstanding)"),
              ("dpd90", "90+ DPD exposure (arrears incl. written off + outstanding)"),
              ("def180", "180+ default exposure (cumulative)"), ("recov", "Cumulative recoveries (net)"),
              ("active", "Active accounts")]
CHECKPOINTS = [3, 6, 12, 18, 24, 36, 48, 60]
NCP = len(CHECKPOINTS)
VI_R0 = lambda j: 9 + j * (MONTHS + 5)


def vi_col(metric, k):
    m_i = [m for m, _ in VI_METRICS].index(metric)
    return gcl(4 + m_i * NCP + k)


VI_OWN_COL = gcl(4 + len(VI_METRICS) * NCP)
VI_NOTE_COL = gcl(5 + len(VI_METRICS) * NCP)


def vi_range(j, col_letter):
    return f"Vintage_Input!${col_letter}${VI_R0(j)}:${col_letter}${VI_R0(j) + MONTHS - 1}"


# =====================================================================
# RBF ENGINE (v0.4)
# =====================================================================
RB = "RBF_Engine"
rbw = mb.sheet(RB, "RBF engine - sales-based, repayment-linked, ownership-linked, hybrid",
               "Selected design feeds Ops / P&L. Ownership-linked RBF pays nothing until validated ownership-at-2x evidence exists.")
mb.time_header(rbw)
rbw.column_dimensions["A"].width = 52
label(rbw, "A8", "Design mode"); put_calc(rbw, "C8",
    f"=CHOOSE({INP['rbf_mode']},\"Sales-based\",\"Repayment-linked\",\"Ownership-linked\",\"Hybrid\")", "@", bold=True)
RBF_PAR = {}
rr = 10
mb.section(rbw, rr, "Tier parameters (per unit, active scenario)"); rr += 1
header_row(rbw, rr, ["Parameter", "Unit"] + [f"Tier {p['tier']}" for p in PRODUCTS], start_col=1); rr += 1
TCOLS = [gcl(3 + j) for j in range(NP)]
for key, text, unit, fn, fmt in [
    ("rr_lag", "Cohort repayment ratio at verification age (curve; not PERFORM RR)", "%",
     lambda j: (f"=IFERROR(SUMIFS({crange(j, 'coll')},Curves!$A${AGE0}:$A${LAST_AGE},\"<=\"&{INP['rbf_lag']})/"
                f"SUMIFS({crange(j, 'due')},Curves!$A${AGE0}:$A${LAST_AGE},\"<=\"&{INP['rbf_lag']}),0)"), FMT_PCT),
    ("factor", "Repayment-linked payout factor (RR / target, max 100%)", "%",
     lambda j: f"=IFERROR(MIN(1,{TCOLS[j]}{{rr_lag}}/{INP['rbf_rr_target']}),0)", FMT_PCT),
    ("own", "Ownership-at-2x rate (validated actual cohorts only)", "%",
     lambda j: (f"=IF({INP['own_evidence']}=1,IFERROR(AVERAGEIFS({vi_range(j, VI_OWN_COL)},{vi_range(j, 'B')},2),0),0)"), FMT_PCT),
    ("h2x", "PERFORM ownership horizon (2 x tenor)", "months", lambda j: f"={PR['perf2x'][j]}", FMT_INT),
]:
    RBF_PAR[key] = rr
    label(rbw, f"A{rr}", text); label(rbw, f"B{rr}", unit, size=9, color=GREY_TXT)
    for j in range(NP):
        put_calc(rbw, f"{TCOLS[j]}{rr}", fn(j).replace("{rr_lag}", str(RBF_PAR.get("rr_lag", 0))), fmt)
    rr += 1
rr += 1
for j in range(NP):
    mb.section(rbw, rr, PRODUCTS[j]["name"]); rr += 1
    for key in ("sales", "repay", "own", "hybrid", "sel", "var"):
        mb.register(RB, f"{key}{j}", rr); rr += 1
    rr += 1
mb.section(rbw, rr, "TOTAL - all tiers"); rr += 1
mb.register(RB, "selT", rr); mb.register(RB, "salesT", rr + 1); mb.register(RB, "varT", rr + 2)
for j in range(NP):
    u_rng = mb.range_(O, f"units{j}")
    tc = TCOLS[j]
    rw = lambda k, j=j: mb.r(RB, f"{k}{j}")
    specs = [
        ("sales", "Sales-based RBF (per unit sold, after verification lag)",
         lambda c, p: (f"=IF({c}$4-{INP['rbf_lag']}>=1,INDEX({u_rng},1,{c}$4-{INP['rbf_lag']}),0)"
                       f"*{PR['rbf'][j]}*Timeline!{c}$8*{INP['rbf_on']}")),
        ("repay", "Repayment-linked RBF (sales-based x payout factor)", lambda c, p: f"={c}{rw('sales')}*${tc}${RBF_PAR['factor']}"),
        ("own", "Ownership-linked RBF (paid at 2 x tenor on validated ownership)",
         lambda c, p: (f"=IF(AND({INP['own_evidence']}=1,{c}$4-${tc}${RBF_PAR['h2x']}>=1),"
                       f"INDEX({u_rng},1,{c}$4-${tc}${RBF_PAR['h2x']}),0)*{PR['rbf'][j]}*Timeline!{c}$8*{INP['rbf_on']}*${tc}${RBF_PAR['own']}")),
        ("hybrid", "Hybrid RBF (weighted)",
         lambda c, p: f"={INP['rbf_w1']}*{c}{rw('sales')}+{INP['rbf_w2']}*{c}{rw('repay')}+{INP['rbf_w3']}*{c}{rw('own')}"),
        ("sel", "Selected RBF (feeds Ops and P&L)",
         lambda c, p: f"=CHOOSE({INP['rbf_mode']},{c}{rw('sales')},{c}{rw('repay')},{c}{rw('own')},{c}{rw('hybrid')})"),
        ("var", "Variance vs sales-based", lambda c, p: f"={c}{rw('sel')}-{c}{rw('sales')}"),
    ]
    for key, text, fn in specs:
        mb.write_row(rbw, rw(key), text, "LCY", lambda i, c, p, fn=fn: fn(c, p), FMT_NUM, total="sum", bold=key == "sel")
for key, text in (("selT", "Selected RBF - total"), ("salesT", "Sales-based RBF - total"), ("varT", "Variance vs sales-based - total")):
    base_k = key[:-1]
    mb.write_row(rbw, mb.r(RB, key), text, "LCY",
                 lambda i, c, p, b=base_k: "=" + "+".join(f"{c}{mb.r(RB, f'{b}{j}')}" for j in range(NP)), FMT_NUM, total="sum", bold=True)
# M11: claim cycle, from eligibility to cash (USD unless stated). RBF never enters customer collections (Checks).
rr_c = mb.r(RB, "varT") + 2
mb.section(rbw, rr_c, "CLAIM CYCLE - eligibility, claim, verification, disbursement and the working capital gap"); rr_c += 1
for key in ("eligT", "claimT", "verifT", "dispT", "gapT", "gapL"):
    mb.register(RB, key, rr_c); rr_c += 1
u_all = lambda c: "+".join(f"{mb.ref(O, f'units{j}', c, this_sheet=RB)}*IF({PR['rbf'][j]}>0,1,0)" for j in range(NP))
mb.write_row(rbw, mb.r(RB, "eligT"), "1. Eligible units sold (tiers with RBF per unit above zero; programme active)", "units",
             lambda i, c, p: f"=({u_all(c)})*{INP['rbf_on']}", FMT_NUM, total="sum")
mb.write_row(rbw, mb.r(RB, "claimT"), "2. Claims submitted at sale (USD)", "USD",
             lambda i, c, p: "=(" + "+".join(f"{mb.ref(O, f'units{j}', c, this_sheet=RB)}*{PR['rbf'][j]}" for j in range(NP)) + f")*{INP['rbf_on']}",
             FMT_NUM, total="sum")
mb.write_row(rbw, mb.r(RB, "verifT"), "3. Claims reaching verification after the lag (USD, before any outcome adjustment)", "USD",
             lambda i, c, p: f"={c}{mb.r(RB, 'salesT')}/Timeline!{c}$8", FMT_NUM, total="sum")
mb.write_row(rbw, mb.r(RB, "dispT"), "4. Disbursed under the selected design (USD; equals RBF income in FS at the month's FX)", "USD",
             lambda i, c, p: f"={c}{mb.r(RB, 'selT')}/Timeline!{c}$8", FMT_NUM, total="sum", bold=True)
mb.write_row(rbw, mb.r(RB, "gapT"), "5. Claimed but not yet received, cumulative (USD): RBF working capital gap", "USD",
             lambda i, c, p: f"={p}{mb.r(RB, 'gapT')}+{c}{mb.r(RB, 'claimT')}-{c}{mb.r(RB, 'dispT')}", FMT_NUM, total="last", bold=True)
mb.write_row(rbw, mb.r(RB, "gapL"), "   RBF working capital gap at the month's FX (LCY)", "LCY",
             lambda i, c, p: f"={c}{mb.r(RB, 'gapT')}*Timeline!{c}$8", FMT_NUM, total="last")
note(rbw, f"A{rr_c + 1}", "The gap is subsidy claimed but not yet in the bank. Under the repayment-linked and hybrid designs it includes amounts reduced at "
     "verification, which are never received; under the ownership-linked design it includes amounts deferred to twice the tenor. "
     "The company finances the gap until disbursement. RBF is cash from the programme, never a customer payment.")

# =====================================================================
# CREDIT INPUT (v0.4) - company data template
# =====================================================================
CIN = "Credit_Input"
ciw = mb.sheet(CIN, "Credit input - actual company portfolio data (monthly, by tier)",
               "Paste ERP / servicing-system exports here. Used when Credit_Assumptions data mode = 2 (Actual). Leave blank in Proxy mode.",
               tab="0000FF")
ciw.column_dimensions["A"].width = 8
for n_, k_ in enumerate(CI_KEYS):
    ciw.column_dimensions[gcl(1 + n_)].width = 14
ciw.column_dimensions[CI_COL["notes"]].width = 40
note(ciw, "A4", "Stocks (balances, DPD buckets, default EAD) at period end; flows (originations, repossessions, proceeds, costs, cures, "
     "write-offs, collections, due, unlocks) for the month. LCY. Buckets must reconcile to gross receivables (Checks).")
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
for j in range(NP):
    r0 = CI_R0(j)
    ciw.cell(r0 - 2, 1, PRODUCTS[j]["name"]).font = Font(name=FONT, bold=True, color=NAVY)
    header_row(ciw, r0 - 1, CI_COLS)
    ciw.row_dimensions[r0 - 1].height = 42
    for i in range(1, MONTHS + 1):
        r_ = r0 + i - 1
        put_calc(ciw, f"A{r_}", i, FMT_INT)
        for k_ in CI_KEYS[1:]:
            cell = ciw[f"{CI_COL[k_]}{r_}"]
            cell.fill = INPUT_FILL
            cell.font = Font(name=FONT, color=BLUE)
            cell.number_format = FMT_DATE if k_ == "date" else ("@" if k_ == "notes" else FMT_NUM)
ciw.freeze_panes = "B8"

# =====================================================================
# CREDIT ENGINE (v0.4)
# =====================================================================
CE = "Credit_Engine"
cew = mb.sheet(CE, "Credit engine - DPD, default, recovery, PD/LGD proxies, indicative ECL, eligibility",
               "PROXY block = projection from repayment curves (drives the facility). SELECTED block = Proxy or Actual per data mode (reporting).")
mb.time_header(cew)
cew.column_dimensions["A"].width = 56
PROXY_ROWS = [("gross", "Gross receivables"), ("rar", "Receivables at risk (stopped paying)"), ("perf", "Receivables of paying accounts")] + \
             [(f"b{k_}", f"{BUCKETS[k_][0]} DPD" if k_ else "Current") for k_ in range(6)] + \
             [("dflt", "Default EAD (beyond default definition)"), ("dpd30", "30+ DPD receivables"), ("dpd90", "90+ DPD receivables"),
              ("resale", "Gross resale proceeds"), ("rcost", "Recovery costs"), ("repo_units", "Repossessions (units, approx.)"),
              ("cures", "Cures (proxy engine: none)"), ("wo", "Write-offs"), ("coll", "Collections"), ("due", "Instalments due"),
              ("own", "Ownership events (unlocks)"), ("rr", "Observed repayment rate (collections / due)"),
              ("pd12", "12-month PD proxy (NOT an audited IFRS 9 PD)"), ("lgd", "LGD proxy"),
              ("ecl", "Indicative stage-based ECL (diagnostic, not booked)"), ("elig", "Eligible receivables (borrowing base)"),
              ("bb", "Borrowing-base contribution (advance rate x eligible)"), ("recon", "Reconciliation: buckets - gross (should be 0)")]
SRC = ["gross"] + [f"b{k_}" for k_ in range(6)] + ["dflt", "resale", "rcost", "repo_units", "cures", "wo", "coll", "due", "own"]
SEL_ROWS = [(k_, t_) for k_, t_ in PROXY_ROWS if k_ not in ("rar", "perf")]
rr = 8
for j in range(NP):
    mb.section(cew, rr, f"{PRODUCTS[j]['name']} - PROXY (projection)"); rr += 1
    for k_, _ in PROXY_ROWS:
        mb.register(CE, f"p_{k_}{j}", rr); rr += 1
    rr += 1
    mb.section(cew, rr, f"{PRODUCTS[j]['name']} - SELECTED (data mode)"); rr += 1
    for k_, _ in SEL_ROWS:
        mb.register(CE, f"s_{k_}{j}", rr); rr += 1
    rr += 1
DF = f"(1+{INP['ecl_disc']})^-0.5"


def bucket_sum(prefix, j, c, flag):
    return "+".join(f"{c}{mb.r(CE, f'{prefix}b{k_}{j}')}*{BK[k_][flag]}" for k_ in range(6))


def ecl_formula(prefix, j, c):
    terms = []
    for k_ in range(6):
        b = f"{c}{mb.r(CE, f'{prefix}b{k_}{j}')}"
        pd_, lgd_ = f"{c}{mb.r(CE, f'{prefix}pd12{j}')}", f"{c}{mb.r(CE, f'{prefix}lgd{j}')}"
        terms.append(f"{b}*CHOOSE({BK[k_]['stage']},{pd_}*{lgd_}*{DF},(1-{INP['cure']})*{lgd_}*{DF},{lgd_})")
    return "=" + "+".join(terms)


for j in range(NP):
    pr = lambda k, j=j: mb.r(CE, f"p_{k}{j}")
    sr = lambda k, j=j: mb.r(CE, f"s_{k}{j}")
    oref = lambda k, c, j=j: mb.ref(O, f"{k}{j}", c, this_sheet=CE)
    proxy = {
        "gross": lambda c, p: f"={oref('grossrec', c)}",
        "rar": lambda c, p: f"={oref('rar', c)}",
        "perf": lambda c, p: f"={c}{pr('gross')}-{c}{pr('rar')}",
        "dflt": lambda c, p: "=" + bucket_sum("p_", j, c, "dflt"),
        "dpd30": lambda c, p: "=" + bucket_sum("p_", j, c, "p30"),
        "dpd90": lambda c, p: "=" + bucket_sum("p_", j, c, "p90"),
        "resale": lambda c, p: f"=IF({INP['recov_cost']}>=1,0,{oref('recov', c)}/(1-{INP['recov_cost']}))",
        "rcost": lambda c, p: f"={c}{pr('resale')}-{oref('recov', c)}",
        "repo_units": lambda c, p: f"=IFERROR({c}{pr('resale')}/({PR['recov'][j]}*{PR['price'][j]}*Timeline!{c}$10),0)",
        "cures": lambda c, p: "=0",
        "wo": lambda c, p: f"={oref('missed', c)}",
        "coll": lambda c, p: f"={oref('coll', c)}",
        "due": lambda c, p: f"={oref('due', c)}",
        "own": lambda c, p: f"={oref('unlocks', c)}",
        "rr": lambda c, p: f"=IF({c}{pr('due')}=0,0,{c}{pr('coll')}/{c}{pr('due')})",
        "pd12": lambda c, p: f"=1-(1-{PR['hazard_s'][j]})^12",
        "lgd": lambda c, p: f"=MAX(0,MIN(1,1-{PR['repo'][j]}*{PR['recov'][j]}*(1-{INP['recov_cost']})*{PR['price'][j]}/{PR['financed'][j]}))",
        "ecl": lambda c, p: ecl_formula("p_", j, c),
        "elig": lambda c, p: "=" + bucket_sum("p_", j, c, "elig"),
        "bb": lambda c, p: f"={c}{pr('elig')}*{PR['adv'][j]}",
        "recon": lambda c, p: f"=ROUND(SUM({c}{pr('b0')}:{c}{pr('b5')})-{c}{pr('gross')},0)",
    }
    for k_ in range(6):
        base = "perf" if k_ < 2 else "rar"
        proxy[f"b{k_}"] = (lambda c, p, k_=k_, base=base: f"={c}{pr(base)}*{BK[k_]['share']}")
    for k_, text in PROXY_ROWS:
        mb.write_row(cew, pr(k_), text, "%" if k_ in ("rr", "pd12", "lgd") else "LCY", lambda i, c, p, fn=proxy[k_]: fn(c, p),
                     FMT_PCT if k_ in ("rr", "pd12", "lgd") else FMT_NUM,
                     total=None if k_ in ("rr", "pd12", "lgd") else ("sum" if k_ in ("resale", "rcost", "repo_units", "cures", "wo", "coll", "due", "own") else "last"),
                     link=k_ in ("gross", "rar", "wo", "coll", "due", "own"))
    MODE = INP["credit_mode"]

    def trailing(rowkey, i, c, fn="SUM"):
        return f"{fn}({col(max(1, i - 11))}{sr(rowkey)}:{c}{sr(rowkey)})"

    sel = {}
    for k_ in SRC:
        sel[k_] = (lambda i, c, p, k_=k_: f"=IF({MODE}=1,{c}{pr(k_)},INDEX({ci_range(j, k_)},{c}$4))")
    sel.update({
        "dpd30": lambda i, c, p: "=" + bucket_sum("s_", j, c, "p30"),
        "dpd90": lambda i, c, p: "=" + bucket_sum("s_", j, c, "p90"),
        "rr": lambda i, c, p: f"=IF({c}{sr('due')}=0,0,{c}{sr('coll')}/{c}{sr('due')})",
        "pd12": lambda i, c, p: f"=IF({MODE}=1,{c}{pr('pd12')},IFERROR({trailing('wo', i, c)}/{trailing('gross', i, c, 'AVERAGE')},0))",
        "lgd": lambda i, c, p: (f"=IF({MODE}=1,{c}{pr('lgd')},IFERROR(MAX(0,MIN(1,1-({trailing('resale', i, c)}-{trailing('rcost', i, c)})"
                                f"/{trailing('wo', i, c)})),{c}{pr('lgd')}))"),
        "ecl": lambda i, c, p: ecl_formula("s_", j, c),
        "elig": lambda i, c, p: "=" + bucket_sum("s_", j, c, "elig"),
        "bb": lambda i, c, p: f"={c}{sr('elig')}*{PR['adv'][j]}",
        "recon": lambda i, c, p: f"=ROUND(SUM({c}{sr('b0')}:{c}{sr('b5')})-{c}{sr('gross')},0)",
    })
    for k_, text in SEL_ROWS:
        pct = k_ in ("rr", "pd12", "lgd")
        mb.write_row(cew, sr(k_), text, "%" if pct else "LCY", sel[k_], FMT_PCT if pct else FMT_NUM,
                     total=None if pct else ("sum" if k_ in ("resale", "rcost", "repo_units", "cures", "wo", "coll", "due", "own") else "last"))


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
        "rbf": lambda c, p: f"={mb.ref(RB, f'sel{j}', c, this_sheet=O)}",
        "active": lambda c, p: f"={coh}!{c}${mb.r(coh, 'active_tot')}",
        "unlocks": lambda c, p: f"=IF({c}$4>{Tn},INDEX({u_rng},1,{c}$4-{Tn})*{S_T},0)",
        "rar": lambda c, p: f"={coh}!{c}${mb.r(coh, 'rar_tot')}",
        "grossrec": lambda c, p: (f"={p}{rw('grossrec')}+{c}{rw('financed')}+{c}{rw('fin_inc')}"
                                  f"-{c}{rw('coll')}-{c}{rw('missed')}"),
        "elig": lambda c, p: f"={mb.ref(CE, f'p_elig{j}', c, this_sheet=O)}",
        "bb": lambda c, p: f"={c}{rw('elig')}*{PR['adv'][j]}",
        "cogs": lambda c, p: f"={c}{rw('units')}*{PR['hw'][j]}*(1+{INP['duty']})*Timeline!{c}$8*Scenarios!$G$9",
        "install": lambda c, p: f"={c}{rw('units')}*{PR['install'][j]}*Timeline!{c}$9",
        "warranty": lambda c, p: f"={c}{rw('cogs')}*{PR['warranty'][j]}",
        "comm": lambda c, p: f"={c}{rw('units')}*{PR['comm'][j]}*Timeline!{c}$9",
        "mkt": lambda c, p: f"={c}{rw('units')}*{PR['mkt'][j]}*Timeline!{c}$9",
    }
    for key, text, unit, tot in OPS_FIELDS:
        mb.write_row(ow, rw(key), text, unit, lambda i, c, p, fn=spec[key]: fn(c, p), FMT_NUM, total=tot,
                     link=key in ("coll", "recov", "active", "rar", "rbf", "elig"))
for key, text, unit, tot in OPS_FIELDS:
    mb.write_row(ow, mb.r(O, f"{key}T"), text, unit,
                 lambda i, c, p, k=key: "=" + "+".join(f"{c}{mb.r(O, f'{k}{j}')}" for j in range(NP)),
                 FMT_NUM, bold=True, total=tot)
mb.write_row(ow, mb.r(O, "unlocks_cum"), "Cumulative unlocked accounts (customer ownership)", "accounts",
             lambda i, c, p: f"={p}{mb.r(O, 'unlocks_cum')}+{c}{mb.r(O, 'unlocksT')}", FMT_NUM, total="last")
mb.write_row(ow, mb.r(O, "coll_rate"), "Operational collection rate (collected / due, excl. down payments; not a PERFORM KPI)", "%",
             lambda i, c, p: f"=IF({c}{mb.r(O, 'dueT')}=0,0,{c}{mb.r(O, 'collT')}/{c}{mb.r(O, 'dueT')})", FMT_PCT,
             comment="Cash conversion in the month. Not the PAYGo PERFORM 2026 Repayment Rate, which is computed on contract data (see PERFORM_2026).")
mb.write_row(ow, mb.r(O, "wo_rate"), "Write-off rate (missed / due)", "%",
             lambda i, c, p: f"=IF({c}{mb.r(O, 'dueT')}=0,0,{c}{mb.r(O, 'missedT')}/{c}{mb.r(O, 'dueT')})", FMT_PCT)
mb.write_row(ow, mb.r(O, "other_rev"), "Other revenue: digital loans & services (net take rate)", "LCY",
             lambda i, c, p: f"={c}{mb.r(O, 'activeT')}*{INP['other_arpu']}*Timeline!{c}$9", FMT_NUM, total="sum")
mb.write_row(ow, mb.r(O, "other_cos"), "Cost of other revenue", "LCY",
             lambda i, c, p: f"={c}{mb.r(O, 'other_rev')}*(1-{INP['other_margin']})", FMT_NUM, total="sum")
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
    ("other_cos", "Cost of other revenue", lambda c, p: f"={mb.ref(O, 'other_cos', c, this_sheet=C_)}", "sum", True),
    ("cos", "Total cost of sales", lambda c, p: f"={c}{{cogs}}+{c}{{install}}+{c}{{other_cos}}", "sum", False),
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
    ("inv", "Inventory (closing; target cover, run down by consumption when sales fall)",
     lambda c, p: f"=MAX({c}{{cogs}}*{INP['inv_cover']},{p}{{inv}}-{c}{{cogs}})", "last", False),
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
            ("rf_fee", "Upfront fees on prior-month new drawings (securitisation option)"),
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
    ("rev_oth", "Other revenue (digital loans & services)", lambda c, p: f"={mb.ref(O, 'other_rev', c, this_sheet=S)}", "sum", True),
    ("rev", "Total revenue", lambda c, p: f"={c}{{rev_hw}}+{c}{{rev_fin}}+{c}{{rev_oth}}", "sum", False),
    ("cos", "Cost of sales (hardware, installation, other)", lambda c, p: f"=-{mb.ref(C_, 'cos', c, this_sheet=S)}", "sum", True),
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
    ("fees", "Facility / securitisation fees", lambda c, p: f"=-{mb.ref(F, 'rf_fee', c, this_sheet=S)}", "sum", True),
    ("fx", "FX (loss) / gain on USD debt", lambda c, p: f"=-{mb.ref(F, 'fx_loss', c, this_sheet=S)}", "sum", True),
    ("pbt", "Profit before tax", lambda c, p: f"={c}{{ebit}}+{c}{{int_tl}}+{c}{{int_rf}}+{c}{{fees}}+{c}{{fx}}", "sum", False),
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
    ("cfo_stay_pos", "Operating cash flow positive from this month to the horizon (1 = yes)",
     lambda c, p: f"=IF(MIN({c}{{cfo}}:${mb.last}{{cfo}})>0,1,0)", None, False),
    ("eqtop_pos", "Equity top-up needed this month (1 = yes; above LCY 1, ignoring rounding residue)", lambda c, p: f"=IF({c}{{eq_top}}>1,1,0)", None, False),
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
    "rf_bb": (lambda c, p: f"={mb.ref(O, 'bbT', c, this_sheet=F)}*IF({INP['fin_struct']}=2,{INP['sec_adv_mult']},1)", "last", FMT_NUM),
    "rf_bal": (lambda c, p: (f"=IF({c}$4>={INP['rf_start']},MAX(0,MIN({INP['rf_limit']},{c}{mb.r(F, 'rf_bb')},"
                             f"{p}{mb.r(F, 'rf_bal')}+{INP['min_cash']}-{fs_ref('cash_pre_nf', c)})),0)"), "last", FMT_NUM),
    "rf_flow": (lambda c, p: f"={c}{mb.r(F, 'rf_bal')}-{p}{mb.r(F, 'rf_bal')}", "sum", FMT_NUM),
    "rf_int": (lambda c, p: f"={p}{mb.r(F, 'rf_bal')}*IF({INP['fin_struct']}=2,{INP['sec_rate']},{INP['rf_rate']})/12", "sum", FMT_NUM),
    "rf_fee": (lambda c, p: f"=IF({INP['fin_struct']}=2,{INP['sec_fee']}*MAX(0,{p}{mb.r(F, 'rf_flow')}),0)", "sum", FMT_NUM),
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
    ("dpd30", "30+ DPD receivables / gross receivables (projection)", FMT_PCT,
     lambda i, c, p: f"=IFERROR(({'+'.join(mb.ref(CE, f'p_dpd30{j}', c, this_sheet=CV) for j in range(NP))})/{mb.ref(O, 'grossrecT', c, this_sheet=CV)},0)"),
    ("dpd30_flag", "Breach: 30+ DPD above maximum", FMT_INT,
     lambda i, c, p: f"=IF(AND({mb.ref(F, 'rf_bal', c, this_sheet=CV)}>0,{c}{{dpd30}}>{INP['cov_dpd30']}),1,0)"),
    ("dpd90", "90+ DPD receivables / gross receivables (projection)", FMT_PCT,
     lambda i, c, p: f"=IFERROR(({'+'.join(mb.ref(CE, f'p_dpd90{j}', c, this_sheet=CV) for j in range(NP))})/{mb.ref(O, 'grossrecT', c, this_sheet=CV)},0)"),
    ("dpd90_flag", "Breach: 90+ DPD above maximum", FMT_INT,
     lambda i, c, p: f"=IF(AND({mb.ref(F, 'rf_bal', c, this_sheet=CV)}>0,{c}{{dpd90}}>{INP['cov_dpd90']}),1,0)"),
    ("bb_head", "Borrowing-base headroom (borrowing base - drawn, LCY)", FMT_NUM,
     lambda i, c, p: f"={mb.ref(F, 'rf_bb', c, this_sheet=CV)}-{mb.ref(F, 'rf_bal', c, this_sheet=CV)}"),
    ("bb_flag", "Breach: facility drawn above borrowing base", FMT_INT, lambda i, c, p: f"=IF({c}{{bb_head}}<-1,1,0)"),
    ("ecl", "Indicative stage-based ECL (projection, diagnostic)", FMT_NUM,
     lambda i, c, p: "=" + "+".join(mb.ref(CE, f"p_ecl{j}", c, this_sheet=CV) for j in range(NP))),
    ("ecl_cov", "Indicative ECL / gross receivables", FMT_PCT,
     lambda i, c, p: f"=IFERROR({c}{{ecl}}/{mb.ref(O, 'grossrecT', c, this_sheet=CV)},0)"),
    ("credit_flag", "Composite credit covenant flag", FMT_INT,
     lambda i, c, p: f"=MAX({c}{{cr_flag}},{c}{{rar_flag}},{c}{{dpd30_flag}},{c}{{dpd90_flag}},{c}{{bb_flag}})"),
    ("any_flag", "Any covenant breached in month", FMT_INT,
     lambda i, c, p: f"=MAX({c}{{credit_flag}},{c}{{lev_flag}},{c}{{liq_flag}})"),
]
rr = 8
for key, *_ in cov_rows:
    mb.register(CV, key, rr)
    rr += 1
cvmap = {k: mb.r(CV, k) for k, *_ in cov_rows}
for key, text, fmt, fn in cov_rows:
    mb.write_row(cvw, mb.r(CV, key), text, "", lambda i, c, p, fn=fn: fn(i, c, p).format(**cvmap), fmt,
                 total="sum" if key.endswith("flag") else ("min" if key in ("cr3", "liq", "bb_head") else "max"),
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
kpw = mb.sheet(K, "Key performance indicators", "Portfolio, financial and lender KPIs. PAYGo PERFORM 2026 KPIs are on PERFORM_2026.")
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
    ("cr", "Operational collection rate (collected / due, excl. down payments; not a PERFORM KPI)",
     lambda c: f"=IFERROR({ann(O, 'collT', c)}/{ann(O, 'dueT', c)},0)", FMT_PCT),
    ("wo", "Write-off rate (missed / due)", lambda c: f"=IFERROR({ann(O, 'missedT', c)}/{ann(O, 'dueT', c)},0)", FMT_PCT),
    ("rar", "Receivables at risk / gross receivables (year end)",
     lambda c: f"=IFERROR({ann(O, 'rarT', c, 'last')}/{ann(O, 'grossrecT', c, 'last')},0)", FMT_PCT),
    ("cov", "Loss allowance coverage (allowance / gross receivables)",
     lambda c: f"=IFERROR(-{ann(S, 'prov', c, 'last')}/{ann(S, 'grossrec', c, 'last')},0)", FMT_PCT),
    ("recov_rate", "Net recoveries / write-offs", lambda c: f"=IFERROR({ann(O, 'recovT', c)}/{ann(O, 'missedT', c)},0)", FMT_PCT),
    ("dpd30", "30+ DPD / gross receivables (year end, projection)", lambda c: "=" + ann(CV, "dpd30", c, "last"), FMT_PCT),
    ("dpd90", "90+ DPD / gross receivables (year end, projection)", lambda c: "=" + ann(CV, "dpd90", c, "last"), FMT_PCT),
    ("ecl_cov", "Indicative stage-based ECL / gross receivables (year end)", lambda c: "=" + ann(CV, "ecl_cov", c, "last"), FMT_PCT),
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
    ("oth_share", "Other revenue share (digital loans & services)", lambda c: f"=IFERROR({ann(S, 'rev_oth', c)}/{ann(S, 'rev', c)},0)", FMT_PCT),
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
    ("be_cfo", "Month from which operating cash flow stays positive",
     f"=IFERROR(MATCH(1,{mb.range_(S, 'cfo_stay_pos')},0),\"Not reached\")", FMT_INT),
    ("min_cr3", "Lowest trailing-3-month collection rate (from month 3)",
     f"=MIN(Covenants!{col(3)}{cr3r}:{mb.last}{cr3r})", FMT_PCT),
    ("max_rar", "Highest receivables-at-risk ratio", f"=MAX({mb.range_(O, 'rar_ratio')})", FMT_PCT),
    ("breach_months", "Total months with a monthly covenant breach (annual DSCR not included: next row)", f"=SUM({mb.range_(CV, 'any_flag')})", FMT_INT),
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
note(kpw, f"A{rr + 1}", "Receivables at risk follows the logic of the 2021 PAYGo PERFORM guide (historical) with a curve-based proxy. Covenant definitions are "
     "illustrative; use those in the actual facility agreement.")

def robust_irr(rng, guesses, annualise=False):
    """IRR that tries several starting guesses (spreadsheet IRR solvers can fail to converge from one guess, e.g. for
    strongly negative returns) and says why when no IRR exists."""
    def wrap(g):
        f = f"IRR({rng},{g})"
        return f"(1+{f})^12-1" if annualise else f
    chain = "\"n/a: no convergence\""
    for g in reversed(guesses):
        chain = f"IFERROR({wrap(g)},{chain})"
    return f"IF(OR(COUNTIF({rng},\">0\")=0,COUNTIF({rng},\"<0\")=0),\"n/a: no sign change\",{chain})"


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
    ("irr", "Investor IRR (USD)", "=" + robust_irr(f"D{VR['inv_flow']}:{L5}{VR['inv_flow']}", (0.1, -0.2, 0.5)), FMT_PCT),
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
    ("irr", "Unit IRR (annualised, unlevered)", "%", lambda j: "=" + robust_irr(crange(j, 'ncf'), (0.02, -0.02, 0.1), annualise=True), FMT_PCT),
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
# CREDIT PORTFOLIO (v0.4) - consolidated, selected data mode
# =====================================================================
CP = "Credit_Portfolio"
cpw = mb.sheet(CP, "Credit portfolio dashboard - all tiers (selected data mode)",
               "Proxy = projection; Actual = Credit_Input history. Facility headroom always reflects the projection.", tab="00B050")
mb.time_header(cpw)
cpw.column_dimensions["A"].width = 56
label(cpw, "A8", "Credit data mode")
put_calc(cpw, "C8", f"=IF({INP['credit_mode']}=1,\"PROXY (model curves)\",\"ACTUAL (Credit_Input)\")", "@", bold=True)
sumT = lambda key, c: "+".join(f"Credit_Engine!{c}{mb.r(CE, f's_{key}{j}')}" for j in range(NP))
cp_rows = [("gross", "Gross receivables", lambda i, c, p: "=" + sumT("gross", c), FMT_NUM)] + \
    [(f"b{k_}", f"{BUCKETS[k_][0]}" + (" DPD" if k_ else ""), (lambda i, c, p, k_=k_: "=" + sumT(f"b{k_}", c)), FMT_NUM) for k_ in range(6)] + [
    ("dflt", "Default EAD", lambda i, c, p: "=" + sumT("dflt", c), FMT_NUM),
    ("coll", "Collections", lambda i, c, p: "=" + sumT("coll", c), FMT_NUM),
    ("due", "Instalments due", lambda i, c, p: "=" + sumT("due", c), FMT_NUM),
    ("cratio", "Collection ratio", lambda i, c, p: f"=IF({c}<<due>>=0,0,{c}<<coll>>/{c}<<due>>)", FMT_PCT),
    ("wpd", "Weighted 12-month PD proxy (not an IFRS 9 PD)",
     lambda i, c, p: "=IFERROR((" + "+".join(f"Credit_Engine!{c}{mb.r(CE, f's_pd12{j}')}*Credit_Engine!{c}{mb.r(CE, f's_gross{j}')}" for j in range(NP)) + f")/{c}<<gross>>,0)", FMT_PCT),
    ("wlgd", "Weighted LGD proxy",
     lambda i, c, p: "=IFERROR((" + "+".join(f"Credit_Engine!{c}{mb.r(CE, f's_lgd{j}')}*Credit_Engine!{c}{mb.r(CE, f's_gross{j}')}" for j in range(NP)) + f")/{c}<<gross>>,0)", FMT_PCT),
    ("ecl", "Indicative ECL (diagnostic)", lambda i, c, p: "=" + sumT("ecl", c), FMT_NUM),
    ("eclcov", "Indicative ECL coverage", lambda i, c, p: f"=IFERROR({c}<<ecl>>/{c}<<gross>>,0)", FMT_PCT),
    ("elig", "Eligible receivables", lambda i, c, p: "=" + sumT("elig", c), FMT_NUM),
    ("bb", "Borrowing-base contribution", lambda i, c, p: "=" + sumT("bb", c), FMT_NUM),
    ("drawn", "Facility drawn (projection)", lambda i, c, p: f"={mb.ref(F, 'rf_bal', c, this_sheet=CP)}", FMT_NUM),
    ("head", "Borrowing-base headroom (projection)", lambda i, c, p: f"={mb.ref(F, 'rf_bb', c, this_sheet=CP)}-{c}<<drawn>>", FMT_NUM),
    ("r30", "30+ DPD / gross receivables", lambda i, c, p: "=IFERROR((" + sumT("dpd30", c) + f")/{c}<<gross>>,0)", FMT_PCT),
    ("r90", "90+ DPD / gross receivables", lambda i, c, p: "=IFERROR((" + sumT("dpd90", c) + f")/{c}<<gross>>,0)", FMT_PCT),
    ("flag", "Credit risk flag (30+ or 90+ above covenant)",
     lambda i, c, p: f"=IF(OR({c}<<r30>>>{INP['cov_dpd30']},{c}<<r90>>>{INP['cov_dpd90']}),1,0)", FMT_INT),
]
rr = 10
for key, *_ in cp_rows:
    mb.register(CP, key, rr); rr += 1
cpmap = {k: mb.r(CP, k) for k, *_ in cp_rows}


def subst(f, m):
    for k_, v_ in m.items():
        f = f.replace(f"<<{k_}>>", str(v_))
    return f


for key, text, fn, fmt in cp_rows:
    mb.write_row(cpw, mb.r(CP, key), text, "", lambda i, c, p, fn=fn: subst(fn(i, c, p), cpmap), fmt,
                 total="max" if key == "flag" else "last", bold=key in ("gross", "ecl", "flag"))

# company history summary (Credit_Input, all tiers): read whatever the selected mode, so that history figures quoted
# in reports are workbook cells. Month 1 of a history normally has no instalment due.
HR0 = rr + 2
mb.section(cpw, HR0, "COMPANY HISTORY LOADED IN Credit_Input (COMPANY DATA, all tiers; independent of the selected mode)")
CI_DUE = lambda j, a, b: f"Credit_Input!${CI_COL['due']}${CI_R0(j) + a - 1}:${CI_COL['due']}${CI_R0(j) + b - 1}"
CI_COLL = lambda j, a, b: f"Credit_Input!${CI_COL['coll']}${CI_R0(j) + a - 1}:${CI_COL['coll']}${CI_R0(j) + b - 1}"
hist_n = "MAX(" + ",".join(f"COUNT({ci_range(j, 'due')})" for j in range(NP)) + ")"
label(cpw, f"A{HR0 + 1}", "Months of history with data (longest tier)")
put_calc(cpw, f"C{HR0 + 1}", f"={hist_n}", FMT_INT, bold=True)
HIST_CELLS = {}
for k_, (a_, b_, text) in enumerate([(1, 12, "Operational collection rate, history months 1 to 12"),
                                      (13, 24, "Operational collection rate, history months 13 to 24"),
                                      (25, 36, "Operational collection rate, history months 25 to 36")]):
    r_ = HR0 + 2 + k_
    num = "+".join(f"SUM({CI_COLL(j, a_, b_)})" for j in range(NP))
    den = "+".join(f"SUM({CI_DUE(j, a_, b_)})" for j in range(NP))
    label(cpw, f"A{r_}", text)
    put_calc(cpw, f"C{r_}", f"=IF(C{HR0 + 1}<{b_},\"n/a: fewer than {b_} months\",IFERROR(({num})/({den}),\"n/a\"))", FMT_PCT, bold=True)
    HIST_CELLS[(a_, b_)] = f"Credit_Portfolio!$C${r_}"
r_ = HR0 + 5
last12_num = "+".join(f"SUMPRODUCT({ci_range(j, 'coll')}*((ROW({ci_range(j, 'coll')})-{CI_R0(j)}+1)>C{HR0 + 1}-12)*((ROW({ci_range(j, 'coll')})-{CI_R0(j)}+1)<=C{HR0 + 1}))" for j in range(NP))
last12_den = "+".join(f"SUMPRODUCT({ci_range(j, 'due')}*((ROW({ci_range(j, 'due')})-{CI_R0(j)}+1)>C{HR0 + 1}-12)*((ROW({ci_range(j, 'due')})-{CI_R0(j)}+1)<=C{HR0 + 1}))" for j in range(NP))
label(cpw, f"A{r_}", "Operational collection rate, latest 12 months of history")
put_calc(cpw, f"C{r_}", f"=IF(C{HR0 + 1}<12,\"n/a: fewer than 12 months\",IFERROR(({last12_num})/({last12_den}),\"n/a\"))", FMT_PCT, bold=True)
note(cpw, f"A{HR0 + 7}", "Collected instalments divided by instalments due, deposits excluded, summed over tiers. An operational ratio, not the "
     "PAYGo PERFORM 2026 Repayment Rate. Blank Credit_Input gives n/a.")

# =====================================================================
# CONSUMER RISK (v0.4)
# =====================================================================
CR = "Consumer_Risk"
crw = mb.sheet(CR, "Consumer risk - affordability, APR, evidence of consumer protection",
               "Household incomes are ILLUSTRATIVE - TO BE REPLACED BY COUNTRY / CUSTOMER DATA. Not market data.", tab="0000FF")
crw.column_dimensions["A"].width = 58
for c_ in TCOLS:
    crw.column_dimensions[c_].width = 18
label(crw, "A4", "Maximum payment burden (instalment / monthly household income)")
put_input(crw, "C4", G["afford_max"], FMT_PCT, True); INP["afford_max"] = "Consumer_Risk!$C$4"
note(crw, "D4", "Illustrative policy threshold - set from the company's credit policy or regulator guidance.")
label(crw, "A5", "Affordability assumptions reviewed by management (1 = yes)")
put_input(crw, "C5", G["afford_reviewed"], FMT_INT, True); INP["afford_reviewed"] = "Consumer_Risk!$C$5"
header_row(crw, 7, ["Metric", "Unit"] + [f"Tier {p['tier']}" for p in PRODUCTS])
CRR = {}
STATUS_LIST = '"Not provided,Provided,Validated"'
dv_st = DataValidation(type="list", formula1=STATUS_LIST, allow_blank=False)
crw.add_data_validation(dv_st)
cr_rows = [
    ("income", "Household monthly income - ILLUSTRATIVE, TO BE REPLACED", "LCY / month", None, FMT_NUM),
    ("inst", "PAYGo monthly instalment", "LCY / month", lambda j: f"={PR['inst'][j]}", FMT_NUM),
    ("burden", "Payment burden (instalment / income)", "%", lambda j: f"=IFERROR({TCOLS[j]}<<inst>>/{TCOLS[j]}<<income>>,0)", FMT_PCT),
    ("dp_inc", "Down payment / monthly income", "x", lambda j: f"=IFERROR({PR['deposit'][j]}/{TCOLS[j]}<<income>>,0)", FMT_X),
    ("apr", "Implied consumer APR", "% p.a.", lambda j: f"={PR['apr'][j]}", FMT_PCT),
    ("flag", "Affordability flag (burden above threshold)", "flag", lambda j: f"=IF({TCOLS[j]}<<burden>>>{INP['afford_max']},1,0)", FMT_INT),
    ("perform", "PAYGo PERFORM KPI evidence status", "status", None, "@"),
    ("cp", "Consumer-protection evidence status (pricing disclosure, collections conduct, complaints)", "status", None, "@"),
]
for n_, (key, *_r) in enumerate(cr_rows):
    CRR[key] = 8 + n_
for key, text, unit, fn, fmt in cr_rows:
    r_ = CRR[key]
    label(crw, f"A{r_}", text, bold=key in ("burden", "flag"))
    label(crw, f"B{r_}", unit, size=9, color=GREY_TXT)
    for j in range(NP):
        cell = f"{TCOLS[j]}{r_}"
        if key == "income":
            put_input(crw, cell, PRODUCTS[j]["income"], FMT_NUM, True)
        elif key in ("perform", "cp"):
            put_input(crw, cell, "Not provided", "@")
            dv_st.add(cell)
        else:
            put_calc(crw, cell, subst(fn(j), CRR), fmt)
note(crw, f"A{CRR['cp'] + 2}", "Consumer protection is treated as a financial risk: affordability, collections practices, pricing transparency and "
     "ownership outcomes affect repayment, default, reputation, RBF eligibility and investor risk.")
CONS = {k: [f"Consumer_Risk!${TCOLS[j]}${v}" for j in range(NP)] for k, v in CRR.items()}

# =====================================================================
# VINTAGE INPUT (v0.5)
# =====================================================================
VIN = "Vintage_Input"
viw = mb.sheet(VIN, "Vintage input - actual cohort observations (5 tiers x 60 cohorts)",
               "Mode per cohort: 1 = Proxy (model curves), 2 = Actual (row data). Cumulative values at checkpoints M3...M60, LCY.", tab="0000FF")
viw.column_dimensions["A"].width = 10
dv_vm = DataValidation(type="whole", operator="between", formula1="1", formula2="2")
viw.add_data_validation(dv_vm)
for j in range(NP):
    r0 = VI_R0(j)
    viw.cell(r0 - 3, 1, PRODUCTS[j]["name"]).font = Font(name=FONT, bold=True, color=NAVY)
    viw.cell(r0 - 2, 4, None)
    for m_i, (mk, mt) in enumerate(VI_METRICS):
        viw.cell(r0 - 2, 4 + m_i * NCP, mt).font = Font(name=FONT, bold=True, color=NAVY, size=9)
    header_row(viw, r0 - 1, ["Cohort #", "Mode", "Units originated"] +
               [f"M{cp_}" for _ in VI_METRICS for cp_ in CHECKPOINTS] + ["Ownership at 2x (%)", "Notes"])
    for ci in range(1, MONTHS + 1):
        r_ = r0 + ci - 1
        put_calc(viw, f"A{r_}", ci, FMT_INT)
        put_input(viw, f"B{r_}", 1, FMT_INT)
        dv_vm.add(f"B{r_}")
        for c_idx in range(3, 6 + len(VI_METRICS) * NCP):
            cell = viw.cell(r_, c_idx)
            cell.fill = INPUT_FILL
            cell.font = Font(name=FONT, color=BLUE, size=9)
            cell.number_format = FMT_PCT if gcl(c_idx) == VI_OWN_COL else ("@" if gcl(c_idx) == VI_NOTE_COL else FMT_NUM)
viw.freeze_panes = "D9"

# =====================================================================
# VINTAGE ENGINE (v0.5)
# =====================================================================
VE = "Vintage_Engine"
vew = mb.sheet(VE, "Vintage engine - cohort -> repayment -> DPD -> default -> recovery -> ownership -> economics",
               "Proxy cohorts use the model curves (identical within a tier). Actual cohorts use Vintage_Input. Ownership is 0 in Proxy mode. "
               "DPD exposure = cumulative arrears of accounts at or beyond the threshold (incl. written off) + their outstanding balance.")
vew.column_dimensions["A"].width = 44
VK = [("rr", "Cohort repayment ratio (not PERFORM)"), ("d30", "30+ DPD exposure / due"), ("d90", "90+ DPD exposure / due"), ("d180", "180+ default exposure / due"),
      ("recdef", "Recovery / default"), ("active", "Active account share"), ("contrib", "Cumulative contribution per unit (LCY)")]
AGE_RNG = f"Curves!$A${AGE0}:$A${LAST_AGE}"
PROXY_CELL = {}
rr = 5
mb.section(vew, rr, "A. Proxy curve values by tier and checkpoint"); rr += 1
for j in range(NP):
    vew.cell(rr, 1, PRODUCTS[j]["name"]).font = Font(name=FONT, bold=True, color=NAVY); rr += 1
    header_row(vew, rr, ["KPI"] + [f"M{cp_}" for cp_ in CHECKPOINTS], start_col=1); rr += 1
    s30 = "+".join(f"{BK[k_]['share']}*{BK[k_]['p30']}" for k_ in range(2, 6))
    s90 = "+".join(f"{BK[k_]['share']}*{BK[k_]['p90']}" for k_ in range(2, 6))
    sdf = "+".join(f"{BK[k_]['share']}*{BK[k_]['dflt']}" for k_ in range(2, 6))
    for key, text in VK:
        label(vew, f"A{rr}", text)
        for n_, m in enumerate(CHECKPOINTS):
            cum = lambda ck: f"SUMIFS({crange(j, ck)},{AGE_RNG},\"<=\"&{m})"
            rar_m = f"INDEX({crange(j, 'rar')},{m}+1)"
            Tn_, inst_ = PR["tenor"][j], PR["inst"][j]

            def arrears_k(k, m=m, j=j, Tn_=Tn_, inst_=inst_):
                # cumulative arrears of accounts with >= k missed instalments at age m (incl. amounts written off)
                L_ = f"MAX(0,MIN(MIN({m},{Tn_}),{m}-{k}+1))"
                return (f"(SUMIFS({crange(j, 'arrears')},{AGE_RNG},\"<=\"&{L_})"
                        f"+MAX(0,MIN({m},{Tn_})-{L_})*{inst_}*(1-INDEX({crange(j, 'surv')},{L_}+1)))")
            f = {"rr": f"=IFERROR({cum('coll')}/{cum('due')},0)",
                 "d30": f"=IFERROR(({arrears_k(2)}+{rar_m}*({s30}))/{cum('due')},0)",
                 "d90": f"=IFERROR(({arrears_k(4)}+{rar_m}*({s90}))/{cum('due')},0)",
                 "d180": f"=IFERROR(({arrears_k(7)}+{rar_m}*({sdf}))/{cum('due')},0)",
                 "recdef": f"=IFERROR({cum('recov')}/{cum('missed')},0)",
                 "active": f"=INDEX({crange(j, 'active')},{m}+1)",
                 "contrib": f"=INDEX({crange(j, 'cum')},{m}+1)"}[key]
            cell = f"{gcl(2 + n_)}{rr}"
            put_calc(vew, cell, f, FMT_NUM if key == "contrib" else FMT_PCT)
            PROXY_CELL[(j, key, n_)] = f"${gcl(2 + n_)}${rr}"
        rr += 1
    rr += 1
rr += 1
mb.section(vew, rr, "B. Cohort results (selected per cohort mode)"); rr += 1
VE_R0 = {}
VE_COL = {}
for n_k, (key, text) in enumerate(VK):
    for n_, cp_ in enumerate(CHECKPOINTS):
        VE_COL[(key, n_)] = gcl(4 + n_k * NCP + n_)
VE_OWN = gcl(4 + len(VK) * NCP)
unit_cost = lambda j: f"({PR['landed'][j]}+{PR['install'][j]}+{PR['landed'][j]}*{PR['warranty'][j]}+{PR['cac'][j]})"
for j in range(NP):
    vew.cell(rr, 1, PRODUCTS[j]["name"]).font = Font(name=FONT, bold=True, color=NAVY); rr += 1
    for n_k, (key, text) in enumerate(VK):
        vew.cell(rr, 4 + n_k * NCP, text).font = Font(name=FONT, bold=True, color=NAVY, size=9)
    rr += 1
    header_row(vew, rr, ["Cohort #", "Mode", "Units"] + [f"M{cp_}" for _ in VK for cp_ in CHECKPOINTS] + ["Ownership at 2x"]); rr += 1
    VE_R0[j] = rr
    vr0 = VI_R0(j)
    for ci in range(1, MONTHS + 1):
        r_ = rr + ci - 1
        vi_r = vr0 + ci - 1
        put_calc(vew, f"A{r_}", ci, FMT_INT)
        put_calc(vew, f"B{r_}", f"=Vintage_Input!$B${vi_r}", FMT_INT, link=True)
        put_calc(vew, f"C{r_}", f"=IF(Vintage_Input!$C${vi_r}=\"\",0,Vintage_Input!$C${vi_r})", FMT_NUM, link=True)
        for n_ in range(NCP):
            V = lambda mk, n_=n_, vi_r=vi_r: f"Vintage_Input!{vi_col(mk, n_)}{vi_r}"
            act = {"rr": f"{V('coll')}/{V('due')}", "d30": f"{V('dpd30')}/{V('due')}", "d90": f"{V('dpd90')}/{V('due')}",
                   "d180": f"{V('def180')}/{V('due')}", "recdef": f"IFERROR({V('recov')}/{V('def180')},\"\")",
                   "active": f"IFERROR({V('active')}/$C{r_},\"\")",
                   "contrib": f"IFERROR(({V('coll')}+{V('recov')})/$C{r_}+{PR['deposit'][j]}-{unit_cost(j)},\"\")"}
            for key, _t in VK:
                f = f"=IF($B{r_}=1,{PROXY_CELL[(j, key, n_)]},IF(N({V('due')})>0,{act[key]},\"\"))"
                cell = f"{VE_COL[(key, n_)]}{r_}"
                put_calc(vew, cell, f, FMT_NUM if key == "contrib" else FMT_PCT)
                vew[cell].font = Font(name=FONT, size=9)
        own_in = f"Vintage_Input!${VI_OWN_COL}${vi_r}"
        put_calc(vew, f"{VE_OWN}{r_}", f"=IF($B{r_}=1,0,IF({own_in}=\"\",\"\",{own_in}))", FMT_PCT)
    rr += MONTHS + 1
vew.freeze_panes = "D5"


def ve_range(j, col_letter):
    return f"Vintage_Engine!${col_letter}${VE_R0[j]}:${col_letter}${VE_R0[j] + MONTHS - 1}"


# =====================================================================
# VINTAGE DASHBOARD (v0.5)
# =====================================================================
VD = "Vintage_Dashboard"
vdw = mb.sheet(VD, "Vintage dashboard", "Portfolio data mode, actual cohort coverage, ownership evidence, M12 tier summary, vintage curve.",
               tab="00B050")
vdw.column_dimensions["A"].width = 52
for c_ in "BCDEFGHI":
    vdw.column_dimensions[c_].width = 15
n_act = "+".join(f"COUNTIF({vi_range(j, 'B')},2)" for j in range(NP))
label(vdw, "A4", "Cohorts in Actual mode (all tiers)"); put_calc(vdw, "C4", f"={n_act}", FMT_INT, bold=True)
label(vdw, "A5", "Portfolio vintage mode")
put_calc(vdw, "C5", f"=IF(C4=0,\"PROXY\",IF(C4={NP * MONTHS},\"ACTUAL\",\"MIXED\"))", "@", bold=True)
label(vdw, "A6", "Cohorts with ownership-at-2x data")
put_calc(vdw, "C6", "=" + "+".join(f"COUNT({vi_range(j, VI_OWN_COL)})" for j in range(NP)), FMT_INT, bold=True)
label(vdw, "A7", "Ownership evidence switch (Inputs)"); put_calc(vdw, "C7", f"={INP['own_evidence']}", FMT_INT, link=True)
header_row(vdw, 9, ["Tier summary at M12", "Actual cohorts", "Cohort repayment ratio", "30+ DPD / due", "90+ DPD / due",
                    "180+ default / due", "Recovery / default", "Active share", "CAC payback (m)"])
vdw.row_dimensions[9].height = 30
m12 = CHECKPOINTS.index(12)
VD_ROWS = {}
for j in range(NP):
    r_ = 10 + j
    VD_ROWS[j] = r_
    label(vdw, f"A{r_}", PRODUCTS[j]["name"])
    put_calc(vdw, f"B{r_}", f"=COUNTIF({vi_range(j, 'B')},2)", FMT_INT)
    for n_, key in enumerate(["rr", "d30", "d90", "d180", "recdef", "active"]):
        put_calc(vdw, f"{gcl(3 + n_)}{r_}", f"=IFERROR(AVERAGE({ve_range(j, VE_COL[(key, m12)])}),\"\")", FMT_PCT)
    put_calc(vdw, f"I{r_}", f"=Unit_Economics!{PCOLS[j]}{UR['payback']}", FMT_INT, link=True)
header_row(vdw, 17, ["Portfolio vintage curve (mix-weighted tier averages)"] + [f"M{cp_}" for cp_ in CHECKPOINTS])
for n_r, (key, text) in enumerate([("rr", "Cohort repayment ratio"), ("d30", "30+ DPD / due"), ("d90", "90+ DPD / due")]):
    r_ = 18 + n_r
    label(vdw, f"A{r_}", text)
    for n_ in range(NCP):
        f = "=" + "+".join(f"{PR['mix'][j]}*IFERROR(AVERAGE({ve_range(j, VE_COL[(key, n_)])}),0)" for j in range(NP))
        put_calc(vdw, f"{gcl(2 + n_)}{r_}", f, FMT_PCT)
lc_v = LineChart(); lc_v.title = "Portfolio vintage curve"
from openpyxl.chart.series import SeriesLabel  # noqa: E402
for r_, nm_ in zip((18, 19, 20), ("Cohort repayment ratio", "30+ DPD / due", "90+ DPD / due")):
    lc_v.add_data(Reference(vdw, min_col=2, max_col=1 + NCP, min_row=r_), from_rows=True, titles_from_data=False)
    lc_v.series[-1].tx = SeriesLabel(v=nm_)
lc_v.set_categories(Reference(vdw, min_col=2, max_col=1 + NCP, min_row=17))
lc_v.y_axis.number_format = "0%"; lc_v.height, lc_v.width = 8, 16
vdw.add_chart(lc_v, "A24")
label(vdw, "K4", "Readiness flags", bold=True, color=NAVY)
VD_FLAGS = {}
for n_, (key, text, f) in enumerate([
    ("actual_loaded", "Actual cohort data loaded", "=IF(C4>0,1,0)"),
    ("own_validated", "Ownership-at-2x evidence validated (switch = 1 and data present)", "=IF(AND(C7=1,C6>0),1,0)"),
    ("own_conflict", "Conflict: ownership switch = 1 without ownership data", "=IF(AND(C7=1,C6=0),1,0)"),
]):
    r_ = 5 + n_
    label(vdw, f"K{r_}", text); put_calc(vdw, f"Q{r_}", f, FMT_INT, bold=True)
    VD_FLAGS[key] = f"Vintage_Dashboard!$Q${r_}"
note(vdw, "A22", "Proxy cohorts are identical within a tier (same curve). Mixed portfolios average Proxy and Actual cohorts - read with care.")

# =====================================================================
# PAYGo PERFORM 2026 (v0.8): company-reported KPIs, aggregated by the standard's rule, plus labelled approximations
# =====================================================================
PF = "PERFORM_2026"
pfw = mb.sheet(PF, "PAYGo PERFORM KPIs (GOGLA Technical Guide, June 2026)",
               "Company-reported results computed on contract-level data under the 2026 standard, aggregated by summing numerators "
               "and denominators. The model does not compute PERFORM KPIs; section B shows labelled approximations only.", tab="00B050")
pfw.column_dimensions["A"].width = 58
pfw.column_dimensions["B"].width = 16
for c_ in "CDEFGHIJKLMNO":
    pfw.column_dimensions[c_].width = 14
PF_COLS = ["Cohort #", "Origination month", "Contracts", "RR PvP: payments applied to due instalments", "RR PvP: instalments due to date",
           "RR PvFin: payments applied to due instalments", "RR PvFin: total amount financed", "RR @90 days: payments applied",
           "RR @90 days: instalments due by day 90", "RR @2x: payments applied by 2x term", "RR @2x: instalments due over 1x term",
           "OR @2x: contracts fully paid by 2x", "OR @2x: contracts that reached 2x", "Data as of", "Notes"]
PF_KEY = {k: gcl(1 + n) for n, k in enumerate(["coh", "orig", "n", "pvp_n", "pvp_d", "pvf_n", "pvf_d", "d90_n", "d90_d", "x2_n", "x2_d",
                                                 "or_n", "or_d", "asof", "notes"])}
PF_R0 = {}
r0_ = 40
for j in range(NP):
    PF_R0[j] = r0_ + 3 + j * (MONTHS + 5)


def pf_rng(j, key):
    c_ = PF_KEY[key]
    return f"{q(PF)}!${c_}${PF_R0[j]}:${c_}${PF_R0[j] + MONTHS - 1}"


# section A: reported KPIs
mb.section(pfw, 5, "A. Company-reported PAYGo PERFORM KPIs (from section C; blank = not provided)")
header_row(pfw, 6, ["KPI", "Type"] + [f"Tier {p['tier']}" for p in PRODUCTS] + ["Portfolio", "Status"], start_col=1)
PF_KPI = [("pvp", "RR, paid vs plan (PvP), to date", "Time series"), ("pvf", "RR, paid vs financed (PvFin), to date", "Time series"),
          ("d90", "RR PvP at 90 days", "Cohort milestone"), ("x2", "RR PvP at 2x contract term", "Cohort outcome"),
          ("or", "Ownership rate at 2x contract term (OR @2x)", "Cohort outcome")]
PF_OUT = {}
for n_, (k_, text, typ) in enumerate(PF_KPI):
    r_ = 7 + n_
    label(pfw, f"A{r_}", text, bold=True)
    label(pfw, f"B{r_}", typ, size=9, color=GREY_TXT)
    for j in range(NP):
        put_calc(pfw, f"{TCOLS[j]}{r_}", f"=IF(SUM({pf_rng(j, k_ + '_d')})=0,\"not provided\",SUM({pf_rng(j, k_ + '_n')})/SUM({pf_rng(j, k_ + '_d')}))", FMT_PCT)
    num = "+".join(f"SUM({pf_rng(j, k_ + '_n')})" for j in range(NP))
    den = "+".join(f"SUM({pf_rng(j, k_ + '_d')})" for j in range(NP))
    put_calc(pfw, f"H{r_}", f"=IF(({den})=0,\"not provided\",({num})/({den}))", FMT_PCT, bold=True)
    put_calc(pfw, f"I{r_}", f"=IF(ISNUMBER(H{r_}),\"Company reported\",\"Not provided\")", "@")
    PF_OUT[k_] = f"{q(PF)}!$H${r_}"
for n_, (text, fn) in enumerate([
        ("Cohorts reported (RR PvP)", lambda j: f"=COUNT({pf_rng(j, 'pvp_d')})"),
        ("Contracts reported", lambda j: f"=SUM({pf_rng(j, 'n')})"),
        ("Cohorts with fewer than 100 contracts (the guide recommends at least 100 per monthly cohort)",
         lambda j: f"=COUNTIFS({pf_rng(j, 'n')},\">0\",{pf_rng(j, 'n')},\"<100\")")]):
    r_ = 13 + n_
    label(pfw, f"A{r_}", text)
    for j in range(NP):
        put_calc(pfw, f"{TCOLS[j]}{r_}", fn(j), FMT_INT)
    put_calc(pfw, f"H{r_}", f"=SUM(C{r_}:G{r_})", FMT_INT, bold=True)
PF_SMALL = f"{q(PF)}!$H$15"
PF_COUNT = [f"{q(PF)}!${TCOLS[j]}$13" for j in range(NP)]

# section B: approximations from Vintage_Input
mb.section(pfw, 18, "B. Approximations from Vintage_Input monthly checkpoints: NOT PAYGo PERFORM KPIs (monthly, no payment allocation)")
label(pfw, "A19", "Vintage_Input checkpoints (account age, months)")
for k_, m_ in enumerate(CHECKPOINTS):
    put_calc(pfw, f"{gcl(3 + k_)}19", m_, FMT_INT)
CPROW = f"{q(PF)}!$C$19:${gcl(2 + NCP)}$19"
header_row(pfw, 20, ["Approximation", "Basis"] + [f"Tier {p['tier']}" for p in PRODUCTS], start_col=1)


def vi_choose(metric, k_expr, j):
    return "CHOOSE(" + k_expr + "," + ",".join(vi_range(j, vi_col(metric, n_)) for n_ in range(NCP)) + ")"


def rr2x_formula(j):
    T_ = PR["tenor"][j]
    k2 = f"MATCH(2*{T_},{CPROW},0)"
    k1 = f'COUNTIF({CPROW},"<"&{T_})+1'
    coll2 = vi_choose("coll", k2, j)
    due1 = vi_choose("due", k1, j)
    mode = vi_range(j, "B")
    return (f'=IF(COUNTIF({mode},2)=0,"not available: proxy data only",'
            f'IF(ISNA({k2}),"2x term beyond the input checkpoints",'
            f'IFERROR(SUMIFS({coll2},{mode},2)/SUMIFS({due1},{mode},2,{coll2},"<>"),"no cohort has reached 2x term")))')


for n_, (text, basis, fn) in enumerate([
        ("Cohort repayment ratio at about 90 days", "M3 checkpoint, Actual cohorts",
         lambda j: (f"=IF(COUNTIF({vi_range(j, 'B')},2)=0,\"not available: proxy data only\","
                    f"IFERROR(SUMIFS({vi_range(j, vi_col('coll', 0))},{vi_range(j, 'B')},2,{vi_range(j, vi_col('due', 0))},\"<>\")/"
                    f"SUMIFS({vi_range(j, vi_col('due', 0))},{vi_range(j, 'B')},2,{vi_range(j, vi_col('coll', 0))},\"<>\"),\"no data at M3\"))")),
        ("Cohort repayment ratio at 2x term", "Collections at the 2x checkpoint over instalments due over 1x term, Actual cohorts",
         lambda j: rr2x_formula(j)),
        ("Ownership at 2x reported in Vintage_Input", "Unit weighted, cohorts with ownership data",
         lambda j: (f"=IF(COUNT({vi_range(j, VI_OWN_COL)})=0,\"not reported\","
                    f"SUMPRODUCT({vi_range(j, VI_OWN_COL)},{vi_range(j, 'C')})/SUMIFS({vi_range(j, 'C')},{vi_range(j, VI_OWN_COL)},\"<>\"))"))]):
    r_ = 21 + n_
    label(pfw, f"A{r_}", text, bold=True)
    label(pfw, f"B{r_}", basis, size=8, color=GREY_TXT)
    pfw[f"B{r_}"].alignment = Alignment(wrap_text=True, vertical="top")
    pfw.row_dimensions[r_].height = 30
    for j in range(NP):
        put_calc(pfw, f"{TCOLS[j]}{r_}", fn(j), FMT_PCT)
note(pfw, "A25", "Under the 2026 standard a collection rate, days locked or enabled, or self-defined variants may not substitute for the "
     "Repayment Rate (Technical Guide, page 10, rule 3A). The operational collection rate on KPIs and Covenants is a cash conversion "
     "metric only.")
note(pfw, "A26", "Rules for section C (Technical Guide, pages 8 to 10): exclude deposits, prepayments, penalties, fees and subsidies; include "
     "arrears payments and written-off contracts; cumulative from contract start after any free-use period; original contract terms; "
     "daily-normalised instalments; payments recognised when applied to due instalments.")

# section C: input template
mb.section(pfw, 38, "C. Company-reported results by monthly cohort (COMPANY DATA: inputs, blank by default)")
for j in range(NP):
    pfw.cell(PF_R0[j] - 2, 1, PRODUCTS[j]["name"]).font = Font(name=FONT, bold=True, color=NAVY)
    header_row(pfw, PF_R0[j] - 1, PF_COLS, start_col=1)
    pfw.row_dimensions[PF_R0[j] - 1].height = 54
    for ci in range(1, MONTHS + 1):
        r_ = PF_R0[j] + ci - 1
        put_calc(pfw, f"A{r_}", ci, FMT_INT)
        for k_ in ("n", "pvp_n", "pvp_d", "pvf_n", "pvf_d", "d90_n", "d90_d", "x2_n", "x2_d", "or_n", "or_d"):
            c_ = pfw[f"{PF_KEY[k_]}{r_}"]
            c_.font = Font(name=FONT, size=9, color=BLUE)
            c_.number_format = FMT_NUM
        for k_ in ("orig", "asof"):
            pfw[f"{PF_KEY[k_]}{r_}"].number_format = FMT_DATE
            pfw[f"{PF_KEY[k_]}{r_}"].font = Font(name=FONT, size=9, color=BLUE)
pfw.freeze_panes = "C7"


# =====================================================================
# SOURCE REGISTER (v0.8: built from tools/source_register_data.py, shared with output/04_SOURCE_REGISTER)
# =====================================================================
import source_register_data as SRD  # noqa: E402

SRG = "Source_Register"
srw = mb.sheet(SRG, "Source register: market, sector and standard sources",
               "Grade describes the source (A primary official or audited; B institutional or company disclosure; C reputable secondary; D unverified). "
               "Status describes what has been verified. Only VERIFIED claims feed Calibration. Full register: 04_SOURCE_REGISTER.", tab="7030A0")
SR_HEAD = ["Ref", "Claim", "Value", "Unit", "Period", "Source", "Publisher", "Publication date", "Page", "URL / location", "Evidence type",
           "Grade", "Status", "Book usage", "Model usage", "Notes", "Key"]
SR_FIELDS = ["ref", "claim", "value", "unit", "period", "source", "publisher", "date", "page", "url", "evidence", "grade", "status", "book", "model", "notes", "key"]
header_row(srw, 4, SR_HEAD)
for n_, w_ in enumerate([8, 40, 12, 10, 14, 30, 22, 14, 12, 30, 28, 7, 22, 24, 24, 40, 30]):
    srw.column_dimensions[gcl(1 + n_)].width = w_
SR_STATUS_FILL = {SRD.VERIFIED: "E2EFDA", SRD.HISTORICAL: "EDEDED", SRD.PENDING: "FFF2CC", SRD.UNVERIFIED: "FCE4D6",
                  SRD.CONFLICT: "F8CBAD", SRD.NOT_USED: "F2F2F2"}
for n_, d_ in enumerate(SRD.REGISTER):
    r_ = 5 + n_
    for c_i, fld in enumerate(SR_FIELDS):
        v = d_[fld]
        cell = srw.cell(r_, 1 + c_i, v)
        cell.font = Font(name=FONT, size=9, color=BLUE if fld == "value" else "000000")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if fld == "value" and isinstance(v, float) and abs(v) < 1 and d_["unit"] == "%":
            cell.number_format = FMT_PCT
        elif fld == "value" and isinstance(v, (int, float)):
            cell.number_format = "#,##0.0;(#,##0.0)"
    srw.cell(r_, SR_FIELDS.index("status") + 1).fill = PatternFill("solid", fgColor=SR_STATUS_FILL.get(d_["status"], "FFFFFF"))
SR_LAST = 4 + len(SRD.REGISTER)
srw.freeze_panes = "C5"
SR_KEYS = f"Source_Register!$Q$5:$Q${SR_LAST}"


def sr_val(company, metric, col_letter="C"):
    """Register value (or another column) for a key, whatever its status."""
    return (f"IFERROR(INDEX(Source_Register!${col_letter}$5:${col_letter}${SR_LAST},"
            f"MATCH(\"{company}|{metric}\",{SR_KEYS},0)),\"\")")


def sr_status(company, metric):
    return sr_val(company, metric, "M")


def sr_used(company, metric):
    """Value only when the claim is VERIFIED: the only claims allowed to feed a calculation or diagnostic."""
    st = sr_status(company, metric)
    return f"IF(OR({st}=\"{SRD.VERIFIED}\",{st}=\"{SRD.HISTORICAL}\"),{sr_val(company, metric)},\"\")"


def sr_shown(company, metric):
    """Value for display as context: hidden when the claim is CONFLICTING or NOT USED."""
    st = sr_status(company, metric)
    return f"IF(OR({st}=\"{SRD.CONFLICT}\",{st}=\"{SRD.NOT_USED}\"),\"\",{sr_val(company, metric)})"


# =====================================================================
# MARKET BENCHMARK (v0.6)
# =====================================================================
MB_ = "Market_Benchmark"
mbw = mb.sheet(MB_, "Market benchmark - PAYGo / off-grid companies vs this model",
               "Values pulled from Source_Register as context, with their status in column N. None is VERIFIED today: read them as reported figures, "
               "not benchmarks. Conflicting and unused figures are not shown.",
               tab="7030A0")
mb_cols = ["Company", "Revenue (USD m)", "Net profit (USD m)", "Revenue growth", "Net margin (derived)", "Securitisation / facility (USD m)",
           "Receivables financing capacity (USD m)", "Cumulative solar loans (USD m)", "Customers (m, cumulative)", "Systems financed",
           "Active customers", "Active / originated (derived)", "PAYGo / asset finance", "Source status", "Notes"]
header_row(mbw, 5, mb_cols)
mbw.row_dimensions[5].height = 44
mbw.column_dimensions["A"].width = 34
for n_ in range(1, len(mb_cols)):
    mbw.column_dimensions[gcl(1 + n_)].width = 15
mbw.column_dimensions["O"].width = 60
MB_ROWS = [
    ("M-KOPA", [sr_shown("M-KOPA", "Revenue"), sr_shown("M-KOPA", "Net profit"), sr_shown("M-KOPA", "Revenue growth"),
                "IFERROR(C{r}/B{r},\"\")", "\"\"", "\"\"", "\"\"", "\"\"", "\"\"", "\"\"", "\"\""], "Yes", sr_status("M-KOPA", "Revenue"),
     "Group revenue: CONFLICTING SOURCES (E4-04 USD 416m, E4-05 USD 253.5m), so revenue and margin are not shown. The primary filing held "
     "(E4-01) is M-KOPA UK LIMITED, a subsidiary whose revenue is carbon credit sales: not a PAYGo benchmark."),
    ("Sun King", ["\"\"", "\"\"", "\"\"", "\"\"", sr_shown("Sun King", "Securitisation 2025"), "\"\"",
                  sr_shown("Sun King", "Cumulative solar loans"), sr_shown("Sun King", "Cumulative loan customers"), "\"\"", "\"\"", "\"\""],
     "Yes", sr_status("Sun King", "Securitisation 2025"), "Company disclosures not yet read in this project (E5-01 to E5-04). Customers are cumulative loan customers, not active."),
    ("d.light", ["\"\"", "\"\"", sr_shown("d.light", "Revenue growth"), "\"\"", sr_shown("d.light", "Securitisation facility 2024"),
                 sr_shown("d.light", "Securitisation purchasing capacity since 2020"), "\"\"", "\"\"", "\"\"", "\"\"", "\"\""],
     "Yes", sr_status("d.light", "Securitisation facility 2024"), "Growth is H1 2023. Purchasing capacity is not debt raised. Revenue estimate (E6-04) not used."),
    ("Bboxx", ["\"\""] * 11, "Yes", "\"" + SRD.PENDING + "\"", "Administration from 19 May 2025 as recorded (E7-01), pending the Gazette notice; latest filed accounts FY2022 (E7-02)."),
    ("Pawame", ["\"\""] * 8 + [sr_shown("Pawame", "SHS financed"), sr_shown("Pawame", "Active customers"), "IFERROR(K{r}/J{r},\"\")"],
     "Yes", sr_status("Pawame", "SHS financed"), "NOT USED: no public source found (X-01, X-02)."),
    ("ZOLA Electric", ["\"\"", "\"\"", "\"\"", "\"\"", sr_shown("ZOLA Electric", "Financing round"), "\"\"", "\"\"", "\"\"", "\"\"", "\"\"", "\"\""],
     "Yes", sr_status("ZOLA Electric", "Financing round"), "USD 90m is the 2021 round (equity and debt), not a facility (E9-01)."),
]
for n_, (name, cells, paygo, evid, flag) in enumerate(MB_ROWS):
    r_ = 6 + n_
    label(mbw, f"A{r_}", name, bold=True)
    for c_i, f in enumerate(cells):
        fmt = FMT_PCT if c_i in (2, 3, 10) else "#,##0.0;(#,##0.0);\"-\""
        put_calc(mbw, f"{gcl(2 + c_i)}{r_}", "=" + f.replace("{r}", str(r_)), fmt, link=True)
    label(mbw, f"M{r_}", paygo)
    put_calc(mbw, f"N{r_}", "=" + evid, "@")
    label(mbw, f"O{r_}", flag, size=9, italic=True)
    mbw[f"O{r_}"].alignment = Alignment(wrap_text=True, vertical="top")
MODEL_ROW = 6 + len(MB_ROWS) + 1
label(mbw, f"A{MODEL_ROW}", "THIS MODEL - active scenario, Year 5", bold=True, color=NAVY)
Y5, Y4 = col(YEARS), col(YEARS - 1)
fx_avg5 = f"AVERAGEIFS({TL_FX},{TL_YR},{YEARS})"
fx_end5 = f"INDEX({TL_FX},1,{MONTHS})"
model_cells = [
    f"=KPIs!{Y5}{mb.r(K, 'rev_usd')}/1000000",
    f"=Annual!{Y5}{mb.r(A, 'ni')}/{fx_avg5}/1000000",
    f"=IFERROR(KPIs!{Y5}{mb.r(K, 'rev')}/KPIs!{Y4}{mb.r(K, 'rev')}-1,\"\")",
    f"=IFERROR(B{MODEL_ROW}/0+C{MODEL_ROW}/B{MODEL_ROW},\"\")",
    f"=Annual!{Y5}{mb.r(A, 'rf')}/{fx_end5}/1000000",
    f"=MAX({mb.range_(F, 'rf_bb')})/{fx_end5}/1000000",
    f"=Annual!{Y5}{mb.r(A, 'grossrec')}/{fx_end5}/1000000",
    f"=SUM({mb.range_(O, 'unitsT')})/1000000",
    f"=SUM({mb.range_(O, 'unitsT')})",
    f"=KPIs!{Y5}{mb.r(K, 'active')}",
    f"=IFERROR(K{MODEL_ROW}/J{MODEL_ROW},\"\")",
]
model_cells[3] = f"=IFERROR(C{MODEL_ROW}/B{MODEL_ROW},\"\")"
for c_i, f in enumerate(model_cells):
    fmt = FMT_PCT if c_i in (2, 3, 10) else ("#,##0;(#,##0)" if c_i in (8, 9) else "#,##0.00;(#,##0.00);\"-\"")
    put_calc(mbw, f"{gcl(2 + c_i)}{MODEL_ROW}", f, fmt, bold=True)
label(mbw, f"M{MODEL_ROW}", "Yes"); label(mbw, f"N{MODEL_ROW}", "Model (illustrative)")
label(mbw, f"O{MODEL_ROW}", "Column G = peak borrowing base; column H = gross PAYGo receivables at Y5; column I = cumulative units sold (m).",
      size=9, italic=True)
note(mbw, f"A{MODEL_ROW + 2}", "Do not read single-company figures as targets. Only VERIFIED sources feed the Calibration sheet; "
     "everything else here is context.")
note(mbw, f"A{MODEL_ROW + 3}", "Comparability warning: periods, entities, currencies and definitions differ between companies and from the "
     "model's Year 5 (see the period and status in Source_Register and the comparability flags on Benchmark_DB).")
MBM = {k: f"Market_Benchmark!${c_}${MODEL_ROW}" for k, c_ in
       zip(["rev", "ni", "growth", "margin", "rf", "bbpeak", "gross", "units_m", "units", "active", "ratio"], "BCDEFGHIJKL")}

# =====================================================================
# CALIBRATION (v0.6)
# =====================================================================
CAL = "Calibration"
calw = mb.sheet(CAL, "Calibration - turning benchmarks into model assumptions",
                "Diagnostics compare the active scenario with VERIFIED references only; a reference whose source is not verified is suspended. They flag questions; they do not change inputs.", tab="7030A0")
for c_, w_ in zip("ABCDEFG", [26, 14, 14, 26, 60, 50, 1]):
    calw.column_dimensions[c_].width = w_
header_row(calw, 5, ["Area", "Model (Y5)", "Reference", "Reference source", "Guidance", "Diagnostic"])
cal_rows = [
    ("Revenue growth", f"={MBM['growth']}", f"={sr_used('M-KOPA', 'Revenue growth')}",
     f"=\"E4-06 M-KOPA group growth: \"&{sr_status('M-KOPA', 'Revenue growth')}&\"; E6-03 d.light H1 2023: \"&{sr_status('d.light', 'Revenue growth')}",
     "Do not use one company as the benchmark. Run downside / base / upside growth scenarios.",
     "=IF(C{r}=\"\",\"Reference suspended: source not VERIFIED (see Source_Register)\",IF(B{r}>C{r},\"Model growth above the reference: justify\",\"Within the reference\"))"),
    ("Net margin", f"={MBM['margin']}", f"=IFERROR({sr_used('M-KOPA', 'Net profit')}/{sr_used('M-KOPA', 'Revenue')},\"\")",
     f"=\"E4-04 / E4-07 M-KOPA group: revenue \"&{sr_status('M-KOPA', 'Revenue')}&\"; the primary filing held is a UK subsidiary (E4-01)\"",
     "No verified net margin reference at scale is available. A margin from conflicting revenue figures is not used.",
     "=IF(C{r}=\"\",\"Reference suspended: source not VERIFIED (see Source_Register)\",IFERROR(IF(B{r}>3*C{r},\"Model margin \"&TEXT(B{r}/C{r},\"0.0\")&\"x the scale reference: justify cost and credit assumptions\",\"Within 3x of reference\"),\"\"))"),
    ("Debt / receivables", f"=IFERROR({MBM['rf']}/{MBM['gross']},\"\")", "=\"\"", "No verified ratio",
     "Add a receivables financing / securitisation scenario (Inputs: financing structure = 2).", "=\"No verified benchmark\""),
    ("Portfolio maturity (active / originated)", f"={MBM['ratio']}", "=\"\"", "No sourced reference (X-01, X-02 not used)",
     "Use active / originated only as a diagnostic, never as a churn or default assumption.", "=\"No verified reference\""),
    ("Credit: operational collection rate", f"=KPIs!{Y5}{mb.r(K, 'cr')}", f"={sr_used('ESMAP / World Bank', 'Sector PAYGo collection rate')}",
     f"=\"E1-14 ESMAP MTR 2024, average collection rate 2021-2023 (about 62%): \"&{sr_status('ESMAP / World Bank', 'Sector PAYGo collection rate')}",
     "A sector collection rate is context for the model's operational collection rate. Neither is the PAYGo PERFORM 2026 Repayment Rate. "
     "The cohort engine has priority: calibrate with company cohort data.",
     "=IF(C{r}=\"\",\"Reference suspended: source not VERIFIED (see Source_Register)\",IFERROR(IF(B{r}>C{r}+0.1,\"Model collection rate more than 10 pts above the sector reference: calibrate with cohort data\",\"Within 10 pts of the sector reference\"),\"\"))"),
    ("Receivables financing", f"={MBM['rf']}", f"={sr_used('Sun King', 'Securitisation 2025')}",
     f"=\"E5-04 Sun King 2025 securitisation: \"&{sr_status('Sun King', 'Securitisation 2025')}",
     "Scaled PAYGo companies are reported to fund receivables through local-currency securitisations and warehouses.",
     "=\"Option available: Inputs financing structure = 2 (securitisation)\""),
    ("Revenue mix", f"=KPIs!{Y5}{mb.r(K, 'oth_share')}", "=\"\"", "Qualitative",
     "Revenue can include hardware, PAYGo financing, digital loans and other services (Inputs: other revenue).",
     "=IF(B{r}=0,\"Other revenue switched off\",\"Other revenue included: document take rate\")"),
]
for n_, (area, mv, ref, src, guide, diag) in enumerate(cal_rows):
    r_ = 6 + n_
    label(calw, f"A{r_}", area, bold=True)
    put_calc(calw, f"B{r_}", mv, FMT_PCT if n_ in (0, 1, 2, 3, 4, 6) else "#,##0.0", link=True)
    put_calc(calw, f"C{r_}", ref, FMT_PCT if n_ in (0, 1, 4) else "#,##0.0", link=True)
    if src.startswith("="):
        put_calc(calw, f"D{r_}", src, "@")
    else:
        label(calw, f"D{r_}", src, size=9)
    label(calw, f"E{r_}", guide, size=9)
    put_calc(calw, f"F{r_}", diag.replace("{r}", str(r_)), "@")
    for c_ in "DEF":
        calw[f"{c_}{r_}"].alignment = Alignment(wrap_text=True, vertical="top")
    calw.row_dimensions[r_].height = 42

# =====================================================================
# COMPANY CASES (v0.6)
# =====================================================================
CC = "Company_Cases"
ccw = mb.sheet(CC, "Company cases - what scaled PAYGo companies teach the model",
               "Facts come only from Source_Register (references cited, with their status). Lessons and implications are analytical judgements.", tab="7030A0")
for c_, w_ in zip("ABCDEFG", [14, 34, 34, 34, 34, 34, 22]):
    ccw.column_dimensions[c_].width = w_
header_row(ccw, 5, ["Company", "Business model (as reported)", "Financial evidence", "Financing evidence", "Credit / portfolio lesson",
                    "Model implication", "Evidence status"])
cases = [
    ("M-KOPA", "PAYGo asset financing for underbanked customers (verify the current product mix in the group accounts).",
     "Group FY2024 revenue reported as USD 416m and as USD 253.5m: CONFLICTING SOURCES (E4-04, E4-05). The filing held, M-KOPA UK LIMITED, "
     "reports GBP 1.7m of carbon credit revenue (E4-01): a subsidiary, not the group.", "Not in register.",
     "A figure reported as coming from 'UK filings' must be traced to the reporting entity before use.",
     "No net margin reference is used until the consolidated accounts are read.", "CONFLICTING SOURCES"),
    ("Sun King", "Off-grid solar sold on PAYGo at scale.", "Not in register (no income statement).",
     "Reported: about USD 1.3bn cumulative solar loans to almost 10m customers; KES securitisations of about USD 130m (2023) and USD 156m (2025) (E5-01 to E5-04).",
     "Receivables can be financed in local currency at scale once portfolio data are robust.",
     "Keep the securitisation option and the borrowing base central; local-currency funding reduces FX mismatch.", "PENDING PRIMARY DOCUMENT"),
    ("d.light", "Off-grid solar products with PAYGo financing.", "Revenue reported +41% in H1 2023 (E6-03). A USD 301m revenue estimate is not used (E6-04).",
     "Reported: five securitisation facilities, about USD 718m purchasing capacity since 2020, including about USD 176m multi-currency facility in 2024 (E6-01, E6-02).",
     "Repeated securitisations require consistent cohort performance reporting.",
     "Cohort data (Vintage_Input) are a precondition for receivables financing.", "PENDING PRIMARY DOCUMENT"),
    ("Bboxx", "PAYGo solar and energy services.", "Latest filed accounts FY2022; FY2023 overdue, as recorded (E7-02).",
     "Recorded as entering UK administration on 19 May 2025 (E7-01), pending the Gazette notice.",
     "Scale does not protect against liquidity and funding stress.",
     "Stress liquidity and covenants; never read Base as the only case.", "PENDING PRIMARY DOCUMENT"),
    ("Pawame", "SHS on PAYGo.", "No public source found for the figures previously recorded (X-01, X-02).", "Not in register.",
     "Pending sourced data.", "No use until figures are sourced.", "NOT USED"),
    ("ZOLA Electric", "Energy systems with PAYGo / asset financing (verify current model).", "No financial statements obtained.",
     "Reported USD 90m round in Sep 2021 (USD 45m equity, USD 45m debt) (E9-01).", "Pending financial statements.",
     "Qualitative case only.", "PENDING PRIMARY DOCUMENT"),
]
for n_, row_ in enumerate(cases):
    r_ = 6 + n_
    for c_i, v in enumerate(row_):
        cell = ccw.cell(r_, 1 + c_i, v)
        cell.font = Font(name=FONT, size=9, bold=c_i == 0)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ccw.row_dimensions[r_].height = 72


# =====================================================================
# v0.7 PAYGO FINANCIAL BENCHMARK DATABASE
# =====================================================================
import csv as _csv  # noqa: E402

DB_CSV = Path(__file__).resolve().parents[1] / "benchmarks" / "db" / "paygo_financial_db.csv"
DB_ROWS = list(_csv.DictReader(open(DB_CSV, encoding="utf-8")))
# taxonomy: code -> (label, type, model formula builder or None)
# model formulas take the model year y (1..5) as a literal - no text substitution
fxa = lambda y: f"AVERAGEIFS({TL_FX},{TL_YR},{y})"
fxe = lambda y: f"INDEX({TL_FX},1,{y * 12})"
ay = lambda sheet, key, y: f"SUMIFS({mb.range_(sheet, key)},{TL_YR},{y})"
ey = lambda sheet, key, y: f"INDEX({mb.range_(sheet, key)},1,{y * 12})"
flow = lambda key, sign="": (lambda y: f"={sign}{ay(S, key, y)}/{fxa(y)}/1000000")
stock = lambda key: (lambda y: f"={ey(S, key, y)}/{fxe(y)}/1000000")
TAX_ = [
    ("REV", "Revenue", "money", flow("rev")), ("REV_FIN", "Financing / interest revenue", "money", flow("rev_fin")),
    ("COGS", "Cost of sales", "money", flow("cos", "-")), ("GP", "Gross profit", "money", flow("gp")),
    ("OPEX", "Operating expenses", "money", flow("opex", "-")), ("EBITDA", "EBITDA", "money", flow("ebitda")),
    ("EBIT", "EBIT / operating income", "money", flow("ebit")), ("DA", "Depreciation & amortisation", "money", flow("da", "-")),
    ("FIN_COST", "Finance costs", "money",
     lambda y: f"=-({ay(S, 'int_tl', y)}+{ay(S, 'int_rf', y)}+{ay(S, 'fees', y)})/{fxa(y)}/1000000"),
    ("ECL", "Impairment / expected credit losses", "money", flow("ecl", "-")), ("TAX", "Income tax", "money", flow("tax", "-")),
    ("NI", "Net income", "money", flow("ni")),
    ("CASH", "Cash", "money", stock("cash_end")), ("INV", "Inventory", "money", stock("inv")), ("AP", "Trade payables", "money", stock("ap")),
    ("TRADE_REC", "Trade receivables", "money", None), ("PAYGO_REC_GROSS", "PAYGo receivables - gross", "money", stock("grossrec")),
    ("PAYGO_REC_NET", "PAYGo receivables - net", "money", stock("netrec")), ("PPE", "Property, plant & equipment", "money", stock("ppe")),
    ("DEBT", "Borrowings", "money", lambda y: f"=({ey(S, 'tl', y)}+{ey(S, 'rf', y)})/{fxe(y)}/1000000"),
    ("LEASE", "Lease liabilities", "money", None), ("EQUITY", "Equity", "money", stock("te")),
    ("TOTAL_ASSETS", "Total assets", "money", stock("ta")), ("TOTAL_LIAB", "Total liabilities", "money", stock("tliab")),
    ("CFO", "Operating cash flow", "money", flow("cfo")), ("CAPEX", "Capex", "money", flow("cfi", "-")),
    ("DEBT_DRAW", "Debt raised", "money", None),
    ("EQUITY_RAISED", "Equity raised", "money", lambda y: f"=({ay(F, 'eq_init', y)}+{ay(F, 'eq_top', y)})/{fxa(y)}/1000000"),
    ("SECURITISATION", "Securitisation / receivables financing closed", "money", None),
    ("CUST_ACTIVE", "Active customers", "count", lambda y: f"=KPIs!{col(y)}{mb.r(K, 'active')}"),
    ("CUST_CUM", "Cumulative customers (model: cumulative units sold)", "count",
     lambda y: f"=SUMIFS({mb.range_(O, 'unitsT')},{TL_IDX},\"<=\"&{y * 12})"),
    ("UNITS", "Units sold", "count", lambda y: f"=KPIs!{col(y)}{mb.r(K, 'units')}"),
    ("LOANS_CUM", "Cumulative financing disbursed (USD m)", "money",
     lambda y: f"=SUMIFS({mb.range_(O, 'financedT')},{TL_IDX},\"<=\"&{y * 12})/{fxe(y)}/1000000"),
    ("REV_GROWTH", "Revenue growth (reported)", "ratio",
     lambda y: f"=IFERROR(KPIs!{col(y)}{mb.r(K, 'rev')}/KPIs!{col(y - 1)}{mb.r(K, 'rev')}-1,\"\")" if y > 1 else '=""'),
    ("COLL_RATE", "Operational collection rate (not PERFORM RR)", "ratio", lambda y: f"=KPIs!{col(y)}{mb.r(K, 'cr')}"),
    ("PAR30", "PAR30 / 30+ DPD ratio", "ratio", lambda y: f"=KPIs!{col(y)}{mb.r(K, 'dpd30')}"),
    ("OWNERSHIP_RATE", "Customer ownership rate", "ratio", None),
    ("RAGP", "Risk-adjusted gross profit (non-IFRS)", "money", None),
]
TYPE_OF = {t[0]: t[2] for t in TAX_}

# ---------- Benchmark_DB ----------
BD = "Benchmark_DB"
bdw = mb.sheet(BD, "PAYGo financial benchmark database: raw records",
               "Loaded from benchmarks/db/paygo_financial_db.csv - edit the CSV, never this sheet. use = 1 enters the matrix; "
               "conflicting, undated, half-year-only or D-grade records are kept but excluded.", tab="7030A0")
DB_COLS = ["id", "company", "entity", "fiscal_year", "period_end", "period_months", "statement", "item", "value", "currency", "scale",
           "fx_to_usd", "fx_note", "use", "publisher", "url", "date_published", "status", "grade", "notes"]
header_row(bdw, 4, DB_COLS + ["type", "normalised (USD m / count / ratio)"])
for n_, w_ in enumerate([7, 14, 26, 8, 11, 7, 7, 15, 10, 7, 12, 10, 26, 5, 24, 40, 11, 18, 6, 50, 8, 14]):
    bdw.column_dimensions[gcl(1 + n_)].width = w_
for n_, rec in enumerate(DB_ROWS):
    r_ = 5 + n_
    for c_i, k_ in enumerate(DB_COLS):
        v = rec[k_]
        if k_ in ("fiscal_year", "period_months", "use") and v != "":
            v = int(v)
        elif k_ in ("value", "scale", "fx_to_usd") and v != "":
            v = float(v)
        cell = bdw.cell(r_, 1 + c_i, v if v != "" else None)
        cell.font = Font(name=FONT, size=9, color=BLUE if k_ in ("value", "fx_to_usd", "use") else "000000")
    t_ = TYPE_OF.get(rec["item"], "money")
    bdw.cell(r_, len(DB_COLS) + 1, t_).font = Font(name=FONT, size=9)
    nv = (f'=IF(U{r_}="money",IF(L{r_}="","",I{r_}*K{r_}*L{r_}/1000000),IF(U{r_}="count",I{r_}*K{r_},I{r_}))')
    put_calc(bdw, f"V{r_}", nv, "#,##0.000;(#,##0.000);\"-\"")
    if rec["use"] != "1":
        for c_i in range(1, len(DB_COLS) + 3):
            bdw.cell(r_, c_i).fill = PatternFill("solid", fgColor="FCE4D6")
DB_LAST = 4 + len(DB_ROWS)
# M16: country, page, the model's definition of the item and a comparability flag (columns W to Z, after the computed columns)
ITEM_DEF = {
    "REV": "Total revenue for the period (company's own recognition policy)",
    "NI": "Net income after tax", "EBITDA": "Earnings before interest, tax, depreciation and amortisation (company definition)",
    "REV_GROWTH": "Revenue growth on the prior period as reported",
    "COLL_RATE": "Operational collection rate as defined by the company: not the PAYGo PERFORM Repayment Rate",
    "REPAY_RATE": "PAYGo PERFORM 2026 Repayment Rate (PvP or PvFin; horizon in notes)",
    "PAR30": "Share of receivables 30+ days past due (company definition of arrears and of the balance)",
    "OWNERSHIP_RATE": "Ownership Rate at 2x contract term (PAYGo PERFORM 2026)",
    "CUST_ACTIVE": "Active customers as defined by the company (often not the same as accounts still paying)",
    "CUST_CUM": "Cumulative customers since inception", "UNITS": "Units sold in the period",
    "LOANS_CUM": "Cumulative financing disbursed", "SECURITISATION": "Size of the securitisation or facility closed (capacity, not drawn debt)",
}
for c_, h_, w_ in (("W", "country", 14), ("X", "page", 16), ("Y", "definition (what the figure measures)", 46), ("Z", "comparable with the model?", 46)):
    bdw[f"{c_}4"] = h_
    bdw[f"{c_}4"].font = Font(name=FONT, bold=True, color="FFFFFF")
    bdw[f"{c_}4"].fill = PatternFill("solid", fgColor=NAVY)
    bdw.column_dimensions[c_].width = w_
for n_, rec in enumerate(DB_ROWS):
    r_ = 5 + n_
    bdw[f"W{r_}"] = rec.get("country") or "TO VERIFY"
    bdw[f"X{r_}"] = rec.get("page") or "PAGE TO VERIFY"
    bdw[f"Y{r_}"] = ITEM_DEF.get(rec["item"], dict((t[0], t[1]) for t in TAX_).get(rec["item"], rec["item"]))
    put_calc(bdw, f"Z{r_}", (f'=IF(N{r_}<>1,"No: excluded ("&R{r_}&")",IF(F{r_}<>12,"No: not a full year",'
                             f'IF(R{r_}<>"VERIFIED","With care: status "&R{r_}&"; definition and period to check",'
                             f'"With care: check definition and fiscal year against model years")))'), "@")
    for c_ in "WXYZ":
        bdw[f"{c_}{r_}"].font = Font(name=FONT, size=9)
bdw.freeze_panes = "C5"
DBR = lambda col_letter: f"Benchmark_DB!${col_letter}$5:${col_letter}${DB_LAST}"

# ---------- Benchmark_Matrix ----------
BMX = "Benchmark_Matrix"
bmw = mb.sheet(BMX, "Benchmark matrix - company-year x line item (USD m unless count / ratio)",
               "Peer rows: SUMIFS over usable full-year records. Model rows: live from the active scenario (flows at average FX, "
               "balances at year-end FX).", tab="7030A0")
pairs = sorted({(r["company"], int(r["fiscal_year"])) for r in DB_ROWS
                if r["fiscal_year"] and r["period_months"] == "12" and r["use"] == "1"})
header_row(bmw, 5, ["Company", "Year", "Row type", "Worst grade used", "Peer include"] + [t[0] for t in TAX_])
for n_ in range(len(TAX_)):
    bmw.column_dimensions[gcl(6 + n_)].width = 11
bmw.column_dimensions["A"].width = 22
for c_ in "BCDE":
    bmw.column_dimensions[c_].width = 10
for n_, t_ in enumerate(TAX_):
    bmw.cell(4, 6 + n_, t_[1]).font = Font(name=FONT, size=7, italic=True, color=GREY_TXT)
    bmw.cell(4, 6 + n_).alignment = Alignment(wrap_text=True, vertical="bottom")
bmw.row_dimensions[4].height = 48
MX_COL = {t[0]: gcl(6 + n_) for n_, t in enumerate(TAX_)}
MX_ROWS = []
r_ = 6
for comp, fy in pairs:
    label(bmw, f"A{r_}", comp); put_calc(bmw, f"B{r_}", fy, FMT_INT); label(bmw, f"C{r_}", "Peer")
    crit = f"{DBR('B')},$A{r_},{DBR('D')},$B{r_},{DBR('N')},1,{DBR('F')},12"
    put_calc(bmw, f"D{r_}", "=" + "".join(f"IF(COUNTIFS({crit},{DBR('S')},\"{g}\")>0,\"{g}\"," for g in "EDCBA") + "\"-\"" + ")" * 5, "@")
    put_calc(bmw, f"E{r_}", f"=IF(OR(D{r_}=\"A\",D{r_}=\"B\",D{r_}=\"C\"),1,0)", FMT_INT)
    for code, lab_, typ, _m in TAX_:
        c_ = MX_COL[code]
        put_calc(bmw, f"{c_}{r_}", f"=IF(COUNTIFS({crit},{DBR('H')},\"{code}\")=0,\"\",SUMIFS({DBR('V')},{crit},{DBR('H')},\"{code}\"))",
                 FMT_PCT if typ == "ratio" else ("#,##0;(#,##0);\"-\"" if typ == "count" else "#,##0.0;(#,##0.0);\"-\""))
    MX_ROWS.append(r_)
    r_ += 1
MODEL_MX_ROWS = []
for y in range(1, YEARS + 1):
    label(bmw, f"A{r_}", "THIS MODEL (active scenario)", bold=True, color=NAVY)
    put_calc(bmw, f"B{r_}", y, FMT_INT); label(bmw, f"C{r_}", "Model"); label(bmw, f"D{r_}", "Model"); put_calc(bmw, f"E{r_}", 0, FMT_INT)
    for code, lab_, typ, mf in TAX_:
        c_ = MX_COL[code]
        f = mf(y) if mf else '=""'
        put_calc(bmw, f"{c_}{r_}", f, FMT_PCT if typ == "ratio" else ("#,##0;(#,##0);\"-\"" if typ == "count" else "#,##0.0;(#,##0.0);\"-\""))
    MODEL_MX_ROWS.append(r_)
    r_ += 1
ALL_MX = MX_ROWS + MODEL_MX_ROWS
bmw.freeze_panes = "F6"

# ---------- Benchmark_KPIs ----------
BK_ = "Benchmark_KPIs"
bkw = mb.sheet(BK_, "Benchmark KPIs - derived ratios per company-year and for the model",
               "Blank = not computable from usable records. Ratios are diagnostics, not performance norms.", tab="7030A0")
M = lambda code, r: f"Benchmark_Matrix!${MX_COL[code]}${r}"
KPI_DEF = [
    ("gm", "Gross margin", FMT_PCT, lambda r: f"=IFERROR(IF({M('GP', r)}=\"\",({M('REV', r)}-{M('COGS', r)})/{M('REV', r)},{M('GP', r)}/{M('REV', r)}),\"\")"),
    ("ebitda_m", "EBITDA margin", FMT_PCT, lambda r: f"=IFERROR({M('EBITDA', r)}/{M('REV', r)},\"\")"),
    ("ebit_m", "Operating (EBIT) margin", FMT_PCT, lambda r: f"=IFERROR({M('EBIT', r)}/{M('REV', r)},\"\")"),
    ("net_m", "Net margin", FMT_PCT, lambda r: f"=IFERROR({M('NI', r)}/{M('REV', r)},\"\")"),
    ("growth", "Revenue growth", FMT_PCT,
     lambda r: (f"=IFERROR({M('REV', r)}/SUMIFS(Benchmark_Matrix!${MX_COL['REV']}$6:${MX_COL['REV']}${ALL_MX[-1]},"
                f"Benchmark_Matrix!$A$6:$A${ALL_MX[-1]},Benchmark_Matrix!$A{r},Benchmark_Matrix!$B$6:$B${ALL_MX[-1]},Benchmark_Matrix!$B{r}-1)-1,"
                f"IF({M('REV_GROWTH', r)}=\"\",\"\",{M('REV_GROWTH', r)}))")),
    ("fin_share", "Financing revenue / revenue", FMT_PCT, lambda r: f"=IFERROR({M('REV_FIN', r)}/{M('REV', r)},\"\")"),
    ("rec_days", "Receivables days", FMT_INT,
     lambda r: f"=IFERROR(IF({M('PAYGO_REC_NET', r)}=\"\",{M('TRADE_REC', r)},{M('PAYGO_REC_NET', r)})/{M('REV', r)}*365,\"\")"),
    ("inv_days", "Inventory days", FMT_INT, lambda r: f"=IFERROR({M('INV', r)}/{M('COGS', r)}*365,\"\")"),
    ("pay_days", "Payables days", FMT_INT, lambda r: f"=IFERROR({M('AP', r)}/{M('COGS', r)}*365,\"\")"),
    ("ccc", "Cash conversion cycle (days)", FMT_INT, lambda r: "=IFERROR(<rec_days>+<inv_days>-<pay_days>,\"\")"),
    ("debt_rec", "Debt / net receivables", FMT_X, lambda r: f"=IFERROR({M('DEBT', r)}/{M('PAYGO_REC_NET', r)},\"\")"),
    ("debt_ebitda", "Debt / EBITDA", FMT_X, lambda r: f"=IFERROR(IF({M('EBITDA', r)}<=0,\"\",{M('DEBT', r)}/{M('EBITDA', r)}),\"\")"),
    ("liab_assets", "Total liabilities / total assets", FMT_PCT, lambda r: f"=IFERROR({M('TOTAL_LIAB', r)}/{M('TOTAL_ASSETS', r)},\"\")"),
    ("equity", "Equity (USD m; derived = assets - liabilities when not reported)", "#,##0.0",
     lambda r: f"=IF({M('EQUITY', r)}<>\"\",{M('EQUITY', r)},IFERROR({M('TOTAL_ASSETS', r)}-{M('TOTAL_LIAB', r)},\"\"))"),
    ("roe", "Return on equity (NI / equity)", FMT_PCT, lambda r: "=IFERROR(" + M('NI', r) + "/<equity>,\"\")"),
    ("ecl_rec", "ECL / gross receivables", FMT_PCT, lambda r: f"=IFERROR({M('ECL', r)}/{M('PAYGO_REC_GROSS', r)},\"\")"),
    ("ecl_rev", "ECL / revenue", FMT_PCT, lambda r: f"=IFERROR({M('ECL', r)}/{M('REV', r)},\"\")"),
    ("ecl_finrev", "ECL / financing revenue", FMT_PCT, lambda r: f"=IFERROR({M('ECL', r)}/{M('REV_FIN', r)},\"\")"),
    ("rev_cust", "Revenue per active customer (USD)", FMT_NUM, lambda r: f"=IFERROR({M('REV', r)}*1000000/{M('CUST_ACTIVE', r)},\"\")"),
    ("rec_cust", "Net receivables per active customer (USD)", FMT_NUM, lambda r: f"=IFERROR({M('PAYGO_REC_NET', r)}*1000000/{M('CUST_ACTIVE', r)},\"\")"),
    ("active_ratio", "Active / cumulative customers", FMT_PCT, lambda r: f"=IFERROR({M('CUST_ACTIVE', r)}/{M('CUST_CUM', r)},\"\")"),
    ("repay", "Operational collection rate (not PERFORM RR)", FMT_PCT, lambda r: f"=IF({M('COLL_RATE', r)}=\"\",\"\",{M('COLL_RATE', r)})"),
    ("own", "Customer ownership rate", FMT_PCT, lambda r: f"=IF({M('OWNERSHIP_RATE', r)}=\"\",\"\",{M('OWNERSHIP_RATE', r)})"),
]
KC = {k: gcl(4 + n_) for n_, (k, *_r) in enumerate(KPI_DEF)}
header_row(bkw, 5, ["Company", "Year", "Peer include"] + [d[1] for d in KPI_DEF])
bkw.row_dimensions[5].height = 54
bkw.column_dimensions["A"].width = 26
for c_ in KC.values():
    bkw.column_dimensions[c_].width = 12
KROW = {}
for n_, mr in enumerate(ALL_MX):
    r_ = 6 + n_
    KROW[mr] = r_
    put_calc(bkw, f"A{r_}", f"=Benchmark_Matrix!A{mr}", "@", link=True)
    put_calc(bkw, f"B{r_}", f"=Benchmark_Matrix!B{mr}", FMT_INT, link=True)
    put_calc(bkw, f"C{r_}", f"=Benchmark_Matrix!E{mr}", FMT_INT, link=True)
    for k_, text, fmt, fn in KPI_DEF:
        f = fn(mr)
        for kk, cc in KC.items():
            f = f.replace(f"<{kk}>", f"{cc}{r_}")
        put_calc(bkw, f"{KC[k_]}{r_}", f, fmt)
LAST_K = 6 + len(ALL_MX) - 1
PEER_R0 = LAST_K + 3
label(bkw, f"A{PEER_R0 - 1}", "Peer-only values (graded A-C, usable) - feed the peer ranges", bold=True, color=NAVY)
for n_, mr in enumerate(MX_ROWS):
    r_ = PEER_R0 + n_
    src = KROW[mr]
    put_calc(bkw, f"A{r_}", f"=A{src}", "@"); put_calc(bkw, f"B{r_}", f"=B{src}", FMT_INT)
    for k_, text, fmt, fn in KPI_DEF:
        c_ = KC[k_]
        put_calc(bkw, f"{c_}{r_}", f"=IF(AND($C{src}=1,ISNUMBER({c_}{src})),{c_}{src},\"\")", fmt)
PEER_LAST = PEER_R0 + max(len(MX_ROWS), 1) - 1
bkw.freeze_panes = "D6"

# ---------- Benchmark_Compare ----------
BC = "Benchmark_Compare"
bcw = mb.sheet(BC, "How does this PAYGo company compare with real companies at scale?",
               "Model (active scenario) vs graded peer records. Peer ranges use grade A-C usable records only; n shows how thin the evidence is.",
               tab="7030A0")
header_row(bcw, 5, ["KPI", "Model Y1", "Model Y2", "Model Y3", "Model Y4", "Model Y5", "Peer n", "Peer min", "Peer median", "Peer max",
                    "Model Y5 vs peers"])
bcw.column_dimensions["A"].width = 44
for c_ in "BCDEFGHIJ":
    bcw.column_dimensions[c_].width = 12
bcw.column_dimensions["K"].width = 34
bcw["L5"] = "Comparability warning"
bcw["L5"].font = Font(name=FONT, bold=True, color="FFFFFF"); bcw["L5"].fill = PatternFill("solid", fgColor=NAVY)
bcw.column_dimensions["L"].width = 70
CMP_WARN = {
    "gm": "Cost of sales lines differ (installation, warranty, financing costs).",
    "ebitda_m": "Companies define EBITDA differently; RBF and credit losses may sit above or below it.",
    "net_m": "Group accounts include non-PAYGo activities and other currencies.",
    "growth": "Fiscal years differ from model years; currency of growth matters.",
    "fin_share": "Revenue recognition policies split hardware and financing income differently.",
    "rec_days": "Gross or net receivables; securitised books may be off balance sheet.",
    "ecl_rec": "ECL policies, staging and write-off timing differ between companies.",
    "ecl_rev": "ECL policies, staging and write-off timing differ between companies.",
    "ecl_finrev": "ECL policies, staging and write-off timing differ between companies.",
    "rev_cust": "Active customer definitions differ (paying accounts, any product, any period).",
    "rec_cust": "Active customer definitions differ.",
    "active_ratio": "Cumulative customers and active customers are defined differently by each company.",
    "repay": "A company collection rate is not the model's operational collection rate unless deposits, period and denominator match; neither is the PERFORM Repayment Rate.",
    "own": "Ownership rate is comparable only on the PAYGo PERFORM 2026 definition (at 2x term).",
}
for n_, (k_, text, fmt, fn) in enumerate(KPI_DEF):
    r_ = 6 + n_
    label(bcw, f"A{r_}", text)
    for y, mr in enumerate(MODEL_MX_ROWS):
        put_calc(bcw, f"{gcl(2 + y)}{r_}", f"=Benchmark_KPIs!{KC[k_]}{KROW[mr]}", fmt, link=True)
    rng = f"Benchmark_KPIs!${KC[k_]}${PEER_R0}:${KC[k_]}${PEER_LAST}"
    put_calc(bcw, f"G{r_}", f"=COUNT({rng})", FMT_INT)
    put_calc(bcw, f"H{r_}", f"=IF(G{r_}=0,\"\",MIN({rng}))", fmt)
    put_calc(bcw, f"I{r_}", f"=IF(G{r_}=0,\"\",MEDIAN({rng}))", fmt)
    put_calc(bcw, f"J{r_}", f"=IF(G{r_}=0,\"\",MAX({rng}))", fmt)
    label(bcw, f"L{r_}", CMP_WARN.get(k_, "Check definitions, periods and currency before comparing."), size=9, italic=True)
    put_calc(bcw, f"K{r_}", (f"=IF(G{r_}=0,\"No graded peer data yet\",IF(NOT(ISNUMBER(F{r_})),\"Model value n/a\","
                             f"IF(F{r_}>J{r_},\"Above peer range\",IF(F{r_}<H{r_},\"Below peer range\",\"Within peer range\")))&IF(G{r_}<3,\" (n<3: anecdotal)\",\"\"))"), "@")
note(bcw, f"A{8 + len(KPI_DEF)}", "CAC payback is not disclosed by companies; see Unit_Economics for the model. Watu is an asset-finance "
     "comparable (motorcycles / smartphones), not a solar company. Unresolved conflicts (e.g. M-KOPA FY2024 revenue: USD 416m vs "
     "USD 253.5m) are excluded until primary filings are read - see Benchmark_DB.")
BENCH_SUMMARY = {"n_records": len(DB_ROWS), "n_used": sum(r["use"] == "1" for r in DB_ROWS)}


# =====================================================================
# CHECKS
# =====================================================================
X = "Checks"
xw = mb.sheet(X, "Integrity checks", "Each check returns 0 when OK. The master check feeds Cover, Investment_Summary and Dashboard.",
              tab="FF0000")
xw.column_dimensions["A"].width = 64
header_row(xw, 4, ["Check", "Unit", "Result (0 = OK)"])
mixrow = PR["mix"][0].split("$")[-1]


def prev_(sheet, key):
    """The same row shifted one month back (column D holds the opening value, zero)."""
    r_ = mb.r(sheet, key)
    return f"{q(sheet)}!$D${r_}:${col(MONTHS - 1)}${r_}"



tenrow = PR["tenor"][0].split("$")[-1]


def whole_in(ref, lo, hi):
    """1 when an input is not a whole number within [lo, hi] (text, blank, decimal or out of range), else 0."""
    return f"IFERROR(IF(AND(ISNUMBER({ref}),{ref}=INT({ref}),{ref}>={lo},{ref}<={hi}),0,1),1)"


checks = [
    ("Balance sheet balances (max abs difference, all months)", f"=MAX(MAX({mb.range_(S, 'bs_chk')}),-MIN({mb.range_(S, 'bs_chk')}))"),
    ("Sales mix sums to 100%", f"=IF(ABS(SUM(Products!$C${mixrow}:${PCOLS[-1]}${mixrow})-1)>0.0001,1,0)"),
    ("Closing cash never below minimum cash", f"=IF(MIN({mb.range_(S, 'cash_end')})<{INP['min_cash']}-1,1,0)"),
    ("Gross receivables never negative", f"=IF(MIN({mb.range_(S, 'grossrec')})<-1,1,0)"),
    ("Loss allowance never positive (contra-asset)", f"=IF(MAX({mb.range_(S, 'prov')})>1,1,0)"),
    ("Facility within limit", f"=IF(MAX({mb.range_(F, 'rf_bal')})>{INP['rf_limit']}+1,1,0)"),
    ("Cash flow reconciles to balance-sheet cash every month (opening cash + net cash flow = closing cash)",
     f"=IF(SUMPRODUCT(ABS({mb.range_(S, 'cash_end')}-{prev_(S, 'cash_end')}-{mb.range_(S, 'cfo')}-{mb.range_(S, 'cfi')}-{mb.range_(S, 'cf_tl')}"
     f"-{mb.range_(S, 'cf_rf')}-{mb.range_(S, 'cf_eq0')}-{mb.range_(S, 'eq_top')}))+SUMPRODUCT(ABS({mb.range_(S, 'cash')}-{mb.range_(S, 'cash_end')}))>1,1,0)"),
    ("Tenors are whole numbers from 1 to 60 months (curve horizon)", "=" + "+".join(whole_in(PR['tenor'][j], 1, MAX_AGE) for j in range(NP))),
    ("Down payment not above cash price", "=" + "+".join(f"IF({PR['deposit'][j]}>{PR['price'][j]},1,0)" for j in range(NP))),
    ("Scenario selector valid (whole number 1 to 3)", "=" + whole_in(INP['scenario'], 1, 3)),
    ("Investor ticket within initial equity", f"=IF({INP['inv_usd']}*{INP['fx0']}>{INP['eq0']}+1,1,0)"),
    ("Terminal growth below discount rate", f"=IF({INP['tg']}>={INP['wacc']},1,0)"),
    ("Credit data mode valid (whole number 1 to 2)", "=" + whole_in(INP['credit_mode'], 1, 2)),
    ("Proxy DPD buckets reconcile to gross receivables (all tiers, all months)",
     "=IF(" + "+".join(f"SUMPRODUCT(ABS({mb.range_(CE, f'p_recon{j}')}))" for j in range(NP)) + ">0,1,0)"),
    ("Actual DPD buckets reconcile to gross receivables (Actual mode only)",
     f"=IF({INP['credit_mode']}=2,IF(" + "+".join(f"SUMPRODUCT(ABS({mb.range_(CE, f's_recon{j}')}))" for j in range(NP)) + ">0,1,0),0)"),
    ("Indicative ECL non-negative", "=IF(MIN(" + ",".join(f"MIN({mb.range_(CE, f's_ecl{j}')}),MIN({mb.range_(CE, f'p_ecl{j}')})" for j in range(NP)) + ")<-1,1,0)"),
    ("Facility drawn within borrowing base and limit",
     f"=IF(OR(SUMPRODUCT(--({mb.range_(F, 'rf_bal')}>{mb.range_(F, 'rf_bb')}+1))>0,MAX({mb.range_(F, 'rf_bal')})>{INP['rf_limit']}+1),1,0)"),
    ("Proxy shares of receivables at risk sum to 100%",
     f"=IF(ABS({INP['rar_s1']}+{INP['rar_s2']}+{INP['rar_s3']}+{INP['rar_s4']}-1)>0.0001,1,0)"),
    ("Hybrid RBF weights sum to 100%", f"=IF(ABS({INP['rbf_w1']}+{INP['rbf_w2']}+{INP['rbf_w3']}-1)>0.0001,1,0)"),
    ("RBF mode valid (whole number 1 to 4)", "=" + whole_in(INP['rbf_mode'], 1, 4)),
    ("Stage thresholds ordered (Stage 2 < Stage 3 <= default)",
     f"=IF(OR({INP['dpd_s2']}>={INP['dpd_s3']},{INP['dpd_s3']}>{INP['dpd_default']}),1,0)"),
    ("Structural inputs valid: financing structure and exit method (1 or 2); RBF, ownership evidence and affordability switches (0 or 1); "
     "opening FX rate above zero; depreciation life and lags whole numbers in range",
     "=" + "+".join([whole_in(INP['fin_struct'], 1, 2), whole_in(INP['exit_method'], 1, 2), whole_in(INP['rbf_on'], 0, 1),
                     whole_in(INP['own_evidence'], 0, 1), whole_in(INP['afford_reviewed'], 0, 1),
                     f"IFERROR(IF({INP['fx0']}>0,0,1),1)", whole_in(INP['dep_life'], 1, 600),
                     whole_in(INP['rbf_lag'], 0, MAX_AGE), whole_in(INP['repo_lag'], 0, MAX_AGE)])),
    ("PERFORM horizon = 2 x tenor for every tier", "=" + "+".join(f"IF({PR['perf2x'][j]}<>2*{PR['tenor'][j]},1,0)" for j in range(NP))),
    ("Vintage cohort modes valid (1 or 2)",
     "=" + "+".join(f"(ROWS({vi_range(j, 'B')})-COUNTIF({vi_range(j, 'B')},1)-COUNTIF({vi_range(j, 'B')},2))" for j in range(NP))),
    # v0.8 reconciliations
    ("Receivables roll forward every month (opening plus originations and financing income, less collections and write-offs, equals closing; Ops = FS)",
     f"=IF(SUMPRODUCT(ABS({mb.range_(O, 'grossrecT')}-{prev_(O, 'grossrecT')}-{mb.range_(O, 'financedT')}-{mb.range_(O, 'fin_incT')}"
     f"+{mb.range_(O, 'collT')}+{mb.range_(O, 'missedT')}))+SUMPRODUCT(ABS({mb.range_(S, 'grossrec')}-{mb.range_(O, 'grossrecT')}))>1,1,0)"),
    ("Loss allowance roll forward (opening, less ECL charged, plus amounts written off, equals closing)",
     f"=IF(SUMPRODUCT(ABS({mb.range_(S, 'prov')}-{prev_(S, 'prov')}+{mb.range_(O, 'eclT')}-{mb.range_(O, 'missedT')}))>1,1,0)"),
    ("USD term loan roll forward in USD and in LCY (translation at month-end FX; FS = Financing)",
     f"=IF(SUMPRODUCT(ABS({mb.range_(F, 'tl_bal_usd')}-{prev_(F, 'tl_bal_usd')}-{mb.range_(F, 'tl_draw_usd')}+{mb.range_(F, 'tl_rep_usd')}))"
     f"+SUMPRODUCT(ABS({mb.range_(F, 'tl_bal')}-{prev_(F, 'tl_bal')}-{mb.range_(F, 'tl_draw')}+{mb.range_(F, 'tl_rep')}-{mb.range_(F, 'fx_loss')}))"
     f"+SUMPRODUCT(ABS({mb.range_(S, 'tl')}-{mb.range_(F, 'tl_bal')}))>1,1,0)"),
    ("Receivables facility roll forward (opening + net drawdown = closing; FS = Financing)",
     f"=IF(SUMPRODUCT(ABS({mb.range_(F, 'rf_bal')}-{prev_(F, 'rf_bal')}-{mb.range_(F, 'rf_flow')}))+SUMPRODUCT(ABS({mb.range_(S, 'rf')}-{mb.range_(F, 'rf_bal')}))"
     f"+SUMPRODUCT(ABS({mb.range_(S, 'cf_rf')}-{mb.range_(F, 'rf_flow')}))>1,1,0)"),
    ("Equity roll forward (opening + net income + equity injected = closing; no dividends)",
     f"=IF(SUMPRODUCT(ABS({mb.range_(S, 'te')}-{prev_(S, 'te')}-{mb.range_(S, 'ni')}-{mb.range_(S, 'cf_eq0')}-{mb.range_(S, 'eq_top')}))"
     f"+SUMPRODUCT(ABS({mb.range_(F, 'eq_cum')}-{prev_(F, 'eq_cum')}-{mb.range_(F, 'eq_init')}-{mb.range_(F, 'eq_top')}))>1,1,0)"),
    ("Cohort totals equal portfolio totals (cohort sizes = units sold; tier rows sum to totals for collections, instalments due, receivables)",
     "=IF(" + "+".join(f"ABS(SUM(Cohort_T{j + 1}!$C${mb.r(f'Cohort_T{j + 1}', 'coll_tot') + 1}:$C${mb.r(f'Cohort_T{j + 1}', 'coll_tot') + MONTHS})-SUM({mb.range_(O, f'iunits{j}')}))"
                       f"+ABS(SUM(Cohort_T{j + 1}!$C${mb.r(f'Cohort_T{j + 1}', 'active_tot') + 1}:$C${mb.r(f'Cohort_T{j + 1}', 'active_tot') + MONTHS})-SUM({mb.range_(O, f'units{j}')}))"
                       for j in range(NP))
     + "+" + "+".join(f"SUMPRODUCT(ABS({mb.range_(O, k + 'T')}-(" + "+".join(mb.range_(O, f'{k}{j}') for j in range(NP)) + ")))" for k in ("coll", "due", "grossrec"))
     + ">1,1,0)"),
    ("Vintage engine carries cohort units from Vintage_Input (all tiers)",
     "=IF(" + "+".join(f"ABS(SUM({ve_range(j, 'C')})-SUM({vi_range(j, 'C')}))" for j in range(NP)) + ">0.5,1,0)"),
    ("Vintage_Input: cumulative collections never fall between checkpoints",
     "=IF(" + "+".join(f"SUMPRODUCT(ISNUMBER({vi_range(j, vi_col('coll', n_ + 1))})*ISNUMBER({vi_range(j, vi_col('coll', n_))})*({vi_range(j, vi_col('coll', n_ + 1))}<{vi_range(j, vi_col('coll', n_))}-0.5))"
                       for j in range(NP) for n_ in range(NCP - 1)) + ">0,1,0)"),
    ("Vintage_Input: cumulative instalments due never fall between checkpoints",
     "=IF(" + "+".join(f"SUMPRODUCT(ISNUMBER({vi_range(j, vi_col('due', n_ + 1))})*ISNUMBER({vi_range(j, vi_col('due', n_))})*({vi_range(j, vi_col('due', n_ + 1))}<{vi_range(j, vi_col('due', n_))}-0.5))"
                       for j in range(NP) for n_ in range(NCP - 1)) + ">0,1,0)"),
    ("RBF: statements equal the engine's selected design, RBF non-negative, cumulative disbursements never above cumulative claims "
     "(RBF is never part of customer collections, which come from the cohorts only)",
     f"=IF(ABS(SUM({mb.range_(S, 'rbf')})-SUM({mb.range_(RB, 'selT')}))+ABS(SUM({mb.range_(O, 'rbfT')})-SUM({mb.range_(RB, 'selT')}))>1,1,0)"
     f"+IF(MIN({mb.range_(RB, 'selT')})<-1,1,0)+IF(MIN({mb.range_(RB, 'gapT')})<-0.01,1,0)"),
    ("Valuation reconciles to the statements (EBITDA, tax, capex, Year 5 working capital)",
     f"=IF(ABS(SUM(Valuation!${col(1)}${VR['ebitda']}:${col(YEARS)}${VR['ebitda']})-SUM({mb.range_(S, 'ebitda')}))"
     f"+ABS(SUM(Valuation!${col(1)}${VR['tax']}:${col(YEARS)}${VR['tax']})-SUM({mb.range_(S, 'tax')}))"
     f"+ABS(SUM(Valuation!${col(1)}${VR['capex']}:${col(YEARS)}${VR['capex']})+SUM({mb.range_(C_, 'capex')}))"
     f"+ABS(Valuation!${col(YEARS)}${VR['nwc']}-(FS!${mb.last}${mb.r(S, 'netrec')}+FS!${mb.last}${mb.r(S, 'inv')}-FS!${mb.last}${mb.r(S, 'ap')}))>1,1,0)"),
    ("Scenario levers in use equal the selected scenario column (no overwritten lever)",
     f"=IF(SUMPRODUCT(ABS(Scenarios!$G$6:$G$10-CHOOSE({INP['scenario']},Scenarios!$C$6:$C$10,Scenarios!$D$6:$D$10,Scenarios!$E$6:$E$10)))>0.000001,1,0)"),
    ("PERFORM_2026 inputs: no negative values, numerators within denominators (RR PvP, at 90 days, at 2x; ownership)",
     "=IF(" + "+".join(f"COUNTIF({pf_rng(j, k)},\"<0\")" for j in range(NP) for k in ("n", "pvp_n", "pvp_d", "pvf_n", "pvf_d", "d90_n", "d90_d", "x2_n", "x2_d", "or_n", "or_d"))
     + "+" + "+".join(f"SUMPRODUCT(ISNUMBER({pf_rng(j, a)})*({pf_rng(j, a)}>{pf_rng(j, b)}+0.5))" for j in range(NP)
                      for a, b in (("pvp_n", "pvp_d"), ("d90_n", "d90_d"), ("x2_n", "x2_d"), ("or_n", "or_d"))) + ">0,1,0)"),
    ("No impossible negative balances (inventory, fixed assets, payables, active accounts, units, debt, cumulative equity)",
     "=IF(MIN(" + ",".join(f"MIN({mb.range_(sh_, k_)})" for sh_, k_ in ((C_, 'inv'), (C_, 'ppe'), (C_, 'ap'), (O, 'activeT'), (O, 'unitsT'),
                                                                        (F, 'tl_bal_usd'), (F, 'rf_bal'), (F, 'eq_cum'))) + ")<-1,1,0)"),
]
for k_, (text, f) in enumerate(checks):
    r_ = 5 + k_
    label(xw, f"A{r_}", text)
    label(xw, f"B{r_}", "flag")
    put_calc(xw, f"C{r_}", f, FMT_NUM)
CHK_ROW = {text: 5 + k_ for k_, (text, _f) in enumerate(checks)}
MR = 5 + len(checks) + 1
label(xw, f"A{MR}", "MASTER CHECK", bold=True)
put_calc(xw, f"C{MR}", f"=IF(SUMPRODUCT(--ISERROR(C5:C{MR - 2}))>0,\"ERROR\",IF(SUM(C5:C{MR - 2})=0,\"OK\",\"ERROR\"))", "@", bold=True)
MASTER = f"Checks!$C${MR}"
label(xw, f"A{MR + 2}", "READINESS FLAGS (informational - not part of the master check)", bold=True, color=NAVY)
header_row(xw, MR + 3, ["Flag", "Unit", "Value (1 = attention)"])
RF = {}
for n_, (key, text, f) in enumerate([
    ("afford", "Consumer affordability assumptions not yet reviewed", f"=IF({INP['afford_reviewed']}=1,0,1)"),
    ("afford_flags", "Tiers above the affordability threshold", "=" + "+".join(CONS["flag"])),
    ("horizon", "Actual credit data horizon not supplied (Actual mode)",
     f"=IF(AND({INP['credit_mode']}=2," + "+".join(f"COUNT({ci_range(j, 'gross')})" for j in range(NP)) + "=0),1,0)"),
    ("own_conflict", "Ownership evidence switch set without ownership data", f"={VD_FLAGS['own_conflict']}"),
    ("proxy_only", "Credit and vintage analysis rely on proxy data only", f"=IF(AND({INP['credit_mode']}=1,Vintage_Dashboard!$C$4=0),1,0)"),
    ("perform_conflict", "PERFORM evidence marked Validated on Consumer_Risk without PERFORM_2026 results (tiers)",
     "=" + "+".join(f"IF(AND({CONS['perform'][j]}=\"Validated\",{PF_COUNT[j]}=0),1,0)" for j in range(NP))),
    ("perform_small", "PERFORM_2026 cohorts with fewer than 100 contracts", f"={PF_SMALL}"),
]):
    r_ = MR + 4 + n_
    label(xw, f"A{r_}", text); label(xw, f"B{r_}", "flag")
    put_calc(xw, f"C{r_}", f, FMT_INT)
    RF[key] = f"Checks!$C${r_}"

# =====================================================================
# INVESTMENT READINESS (v0.4 gates; v0.8 evidence columns and decision rule)
# =====================================================================
IR = "Investment_Readiness"
irw = mb.sheet(IR, "Investment readiness gates and evidence-based decision",
               "Each gate counts only on evidence: automatic gates are computed by the model; a manual gate counts only when marked Met with "
               "the place the evidence is held and the person who signed it off. The decision rule below uses these results only. It is not "
               "an investment recommendation, a credit rating or an opinion on the company.",
               tab="C00000")
for c_, w_ in zip("ABCDEFGHIJKL", [5, 50, 9, 14, 12, 6, 46, 10, 26, 20, 12, 34]):
    irw.column_dimensions[c_].width = w_
header_row(irw, 6, ["#", "Gate", "Type", "Manual status", "Auto result", "Met", "Evidence required", "Critical",
                    "Where the evidence is held", "Signed off by", "Date", "Evidence check"])
irw.row_dimensions[6].height = 30
dv_g = DataValidation(type="list", formula1='"Not started,In progress,Met"', allow_blank=False)
irw.add_data_validation(dv_g)
min_contrib = "MIN(" + ",".join(f"Unit_Economics!{PCOLS[j]}{UR['contrib']}" for j in range(NP)) + ")"
cons_valid = "AND(" + ",".join(f"{CONS['perform'][j]}=\"Validated\",{CONS['cp'][j]}=\"Validated\"" for j in range(NP)) + ")"
# (gate, automatic test or None, evidence required, critical for the decision)
GATES = [
    ("Model integrity (master check OK)", f"={MASTER}=\"OK\"", "Automatic: Checks sheet, master check.", True),
    ("Inputs reviewed and signed off by management", None, "Signed input sheet or board paper approving the plan inputs.", True),
    ("Product specifications and MTF tier labels verified", None, "Datasheets; ESMAP MTF report (Source_Register E3-01, pending).", False),
    ("Pricing, deposits and APR disclosures reviewed", None, "Price list, customer contract and APR disclosure (Consumer_Risk, Products).", False),
    ("Sales plan supported by pipeline / channel evidence", None, "Agent network data, sales history, channel contracts.", False),
    ("Cost base benchmarked", None, "Management accounts and peer cost data with sources.", False),
    ("Stress tests run and documented", None, "Downside and Severe results and the Sensitivity table, reviewed and minuted.", True),
    ("FX and pass-through assumptions validated", None, "Pricing history after past depreciation; FX_Exposure reviewed.", False),
    ("Funding plan supported by term sheets", None, "Signed term sheets or commitment letters for equity and debt.", True),
    ("No covenant breach in the active scenario", f"={H['breach_months']}=0", "Automatic: monthly covenants on the Covenants sheet. The annual DSCR test (KPIs, years below minimum) is not part of this gate.", True),
    ("Downside survivable without unplanned equity", None, "Downside peak equity compared with committed funding, documented.", True),
    ("Valuation assumptions reviewed", None, "Discount rate, terminal growth and exit multiple justified in writing.", False),
    ("Positive lifetime contribution in every tier", f"={min_contrib}>0", "Automatic: Unit_Economics.", True),
    ("Market data sourced and graded (Source_Register)", None, "Every market figure used has a VERIFIED status (Source_Register).", False),
    ("Tax and accounting treatment reviewed", None, "Written review by an accountant of revenue recognition, ECL and tax (the model treatment is not an IFRS determination).", True),
    ("Legal and regulatory review (consumer credit, data, mobile money)", None, "Legal opinion or regulatory checklist signed by counsel.", True),
    ("Workbook tested in Microsoft Excel", None, "Test log: opens, recalculates, master check OK, no circular references.", True),
    ("Credit engine running on actual company data", f"=AND({INP['credit_mode']}=2,{RF['horizon']}=0)", "Automatic: Actual mode with Credit_Input data.", True),
    ("IFRS 9 / ECL validated by auditor or independent reviewer", None, "Auditor's or reviewer's report; indicative ECL and PD proxies are not IFRS 9 measures.", False),
    ("Consumer protection evidenced", f"=AND({INP['afford_reviewed']}=1,{RF['afford_flags']}=0,{cons_valid},{RF['perform_conflict']}=0)",
     "Automatic: affordability reviewed, no flags, PERFORM and consumer-protection evidence validated, PERFORM_2026 results loaded.", True),
    ("Outcome-linked RBF supported by data", f"={VD_FLAGS['own_validated']}=1", "Automatic: validated ownership-at-2x data.", False),
    ("Data reconciliation (actual DPD buckets = gross receivables)",
     f"=AND({INP['credit_mode']}=2,{RF['horizon']}=0,Checks!$C${CHK_ROW['Actual DPD buckets reconcile to gross receivables (Actual mode only)']}=0)",
     "Automatic: Actual mode, data supplied, buckets reconcile.", True),
    ("Lender underwriting pack assembled", None, "Cohort tables, PAYGo PERFORM 2026 KPIs (PERFORM_2026), covenant history, borrowing-base reports.", False),
]
HARD_FAIL = [0, 9, 12]  # automatic gates whose failure is a finding against the business or the model, not missing evidence
for n_, (text, auto, ev, crit) in enumerate(GATES):
    r_ = 7 + n_
    put_calc(irw, f"A{r_}", n_ + 1, FMT_INT)
    label(irw, f"B{r_}", text)
    label(irw, f"C{r_}", "Auto" if auto else "Manual")
    if auto:
        put_calc(irw, f"E{r_}", f"=IFERROR(IF({auto[1:]},\"Met\",\"Not met\"),\"Not met\")", "@")
        put_calc(irw, f"F{r_}", f"=IF(E{r_}=\"Met\",1,0)", FMT_INT, bold=True)
        put_calc(irw, f"L{r_}", "=\"Computed in the model\"", "@")
    else:
        put_input(irw, f"D{r_}", "Not started", "@")
        dv_g.add(f"D{r_}")
        for c_ in "IJK":
            put_input(irw, f"{c_}{r_}", None, FMT_DATE if c_ == "K" else "@")
        put_calc(irw, f"F{r_}", f"=IF(AND(D{r_}=\"Met\",I{r_}<>\"\",J{r_}<>\"\"),1,0)", FMT_INT, bold=True)
        put_calc(irw, f"L{r_}", (f"=IF(D{r_}<>\"Met\",\"\",IF(F{r_}=1,\"Evidenced\",\"Marked Met without evidence location or sign-off: "
                                 f"not counted\"))"), "@")
    label(irw, f"G{r_}", ev, size=9, italic=True)
    label(irw, f"H{r_}", "Yes" if crit else "No", bold=crit)
    for c_ in "ABCDEFGHIJKL":
        irw[f"{c_}{r_}"].alignment = Alignment(wrap_text=c_ in "GL", vertical="center", horizontal="center" if c_ in "ACFH" else None)
    irw.row_dimensions[r_].height = 30
NG = len(GATES)
GL_ = 7 + NG - 1
NCRIT = sum(1 for g in GATES if g[3])
label(irw, "B4", "Gates met")
put_calc(irw, "C4", f"=SUM(F7:F{GL_})", FMT_INT, bold=True)
put_calc(irw, "D4", f"=\"of {NG}\"", "@")
# evidence-based decision (M8)
DR = GL_ + 2
mb.section(irw, DR, "DECISION RULE (evidence only; no judgement enters these cells)")
hard = "+".join(f"IF(F{7 + k}=0,1,0)" for k in HARD_FAIL)
hard_txt = "&".join(f"IF(F{7 + k}=0,\"{GATES[k][0]}; \",\"\")" for k in HARD_FAIL)
rows_ = [
    ("Critical gates met", f"=SUMPRODUCT((H7:H{GL_}=\"Yes\")*(F7:F{GL_}=1))", FMT_INT),
    ("Critical gates", f"={NCRIT}", FMT_INT),
    ("Failed tests (automatic gates that measure the business or the model)", f"={hard}", FMT_INT),
    ("Decision", (f"=IF(C{DR + 3}>0,\"STOP\",IF(C4={NG},\"GO\",IF(C{DR + 1}=C{DR + 2},\"CONDITIONAL GO\",\"STOP\")))"), "@"),
    ("Reason", (f"=IF(C{DR + 3}>0,\"Failed test: \"&LEFT({hard_txt},LEN({hard_txt})-2),IF(C4={NG},\"All {NG} gates met with evidence\","
                f"IF(C{DR + 1}=C{DR + 2},\"All critical gates met; open gates to set as conditions: \"&({NG}-C4),"
                f"\"Evidence incomplete: \"&(C{DR + 2}-C{DR + 1})&\" of \"&C{DR + 2}&\" critical gates not met\")))"), "@"),
]
for n_, (text, f, fmt) in enumerate(rows_):
    r_ = DR + 1 + n_
    label(irw, f"B{r_}", text, bold=n_ >= 3)
    put_calc(irw, f"C{r_}", f, fmt, bold=True)
irw[f"C{DR + 4}"].font = Font(name=FONT, bold=True, size=12, color="C00000")
rule = ["STOP when any failed test exists (master check, covenant breach in the active scenario, negative lifetime contribution in a tier).",
        "GO only when all gates are met with evidence. CONDITIONAL GO when every critical gate is met; the open gates become conditions.",
        "Otherwise STOP: evidence incomplete. A STOP on incomplete evidence says the file is not ready for a decision, not that the business fails.",
        "GO is a statement about the completeness of the evidence for an investment committee. It is never an investment recommendation."]
for n_, t_ in enumerate(rule):
    note(irw, f"B{DR + 7 + n_}", t_)
DECISION = f"Investment_Readiness!$C${DR + 4}"
DECISION_WHY = f"Investment_Readiness!$C${DR + 5}"
put_calc(irw, "B5", f"=\"INVESTMENT READINESS: \"&C4&\"/{NG} gates met. Decision: \"&{DECISION}&\" (\"&{DECISION_WHY}&\")\"", "@", bold=True)
irw["B5"].font = Font(name=FONT, bold=True, color="C00000", size=11)
READY = "Investment_Readiness!$B$5"



# =====================================================================
# FX EXPOSURE (v0.8, M10): currency map, transaction and translation effects (presentation of existing calculations)
# =====================================================================
FXR0 = 13
mb.section(tw, FXR0, "FX EFFECTS (monthly, LCY unless stated; actual FX path compared with the opening rate; feeds FX_Exposure)")
FXK = ["fx_hw", "fx_tlint", "fx_tlrep", "fx_rbf", "fx_net", "fx_reval", "fx_rev_open", "fx_rev_act", "fx_rev_tr", "fx_ebitda_tr", "fx_pass_rev"]
for n_, k_ in enumerate(FXK):
    mb.register(T, k_, FXR0 + 1 + n_)
fx_open = lambda c: f"{INP['fx0']}/Timeline!{c}$8"
tref = lambda sh, k, c: mb.ref(sh, k, c, this_sheet=T)
FX_SPECS = [
    ("fx_hw", "Transaction: extra cost of USD-linked hardware (COGS and warranty)", "LCY",
     lambda c: f"=({tref(C_, 'cogs', c)}+{tref(C_, 'warranty', c)})*(1-{fx_open(c)})"),
    ("fx_tlint", "Transaction: extra interest on the USD term loan", "LCY", lambda c: f"={tref(F, 'tl_int', c)}*(1-{fx_open(c)})"),
    ("fx_tlrep", "Transaction: extra LCY to repay USD principal", "LCY",
     lambda c: f"={tref(F, 'tl_rep', c)}-{tref(F, 'tl_rep_usd', c)}*{INP['fx0']}"),
    ("fx_rbf", "Transaction: extra LCY received on USD-denominated RBF", "LCY", lambda c: f"={tref(O, 'rbfT', c)}*(1-{fx_open(c)})"),
    ("fx_net", "Net transaction effect on costs and RBF, before price pass-through (negative = cost)", "LCY",
     lambda c: f"=-{c}{FXR0 + 1}-{c}{FXR0 + 2}-{c}{FXR0 + 3}+{c}{FXR0 + 4}"),
    ("fx_reval", "Remeasurement: unrealised FX loss on USD debt (FS; non-cash)", "LCY", lambda c: f"={tref(F, 'fx_loss', c)}"),
    ("fx_rev_open", "Translation: revenue in USD at the opening rate", "USD", lambda c: f"={tref(S, 'rev', c)}/{INP['fx0']}"),
    ("fx_rev_act", "Translation: revenue in USD at the month's rate", "USD", lambda c: f"={tref(S, 'rev', c)}/Timeline!{c}$8"),
    ("fx_rev_tr", "Translation effect on revenue in USD (negative = lower in USD)", "USD", lambda c: f"={c}{FXR0 + 8}-{c}{FXR0 + 7}"),
    ("fx_ebitda_tr", "Translation effect on EBITDA in USD", "USD",
     lambda c: f"={tref(S, 'ebitda', c)}/Timeline!{c}$8-{tref(S, 'ebitda', c)}/{INP['fx0']}"),
    ("fx_pass_rev", "Memo: hardware revenue added by price pass-through on new contracts (booked at sale, collected over the tenor)", "LCY",
     lambda c: f"={tref(S, 'rev_hw', c)}*(1-({INP['fx0']}/Timeline!{c}$8)^{INP['fx_pass']})"),
]
for k_, text, unit, fn in FX_SPECS:
    mb.write_row(tw, mb.r(T, k_), text, unit, lambda i, c, p, fn=fn: fn(c), FMT_NUM, total="sum", bold=k_ == "fx_net")

FXS = "FX_Exposure"
fxw = mb.sheet(FXS, "FX exposure: currencies, hedging, transaction and translation effects",
               "Presentation of the model's existing FX calculations. Transaction effects change cash in LCY; translation changes how LCY results "
               "look in USD; remeasurement of USD debt is a non-cash accounting entry.", tab="00B050")
for c_, w_ in zip("ABCDEFGH", [54, 14, 22, 22, 14, 14, 14, 14]):
    fxw.column_dimensions[c_].width = w_
mb.section(fxw, 4, "A. Currency map (where each item sits and how the model treats it)")
header_row(fxw, 5, ["Item", "Currency", "Treatment in the model", "", "Year 5 (LCY m)"])
fxw.merge_cells("C5:D5")
yref = lambda sh, k: f"={sh}!{col(YEARS)}{mb.r(sh, k)}/1000000"
CMAP = [
    ("Revenue: hardware and PAYGo financing", "LCY", "Contract prices in LCY. New contracts are indexed by the pass-through input (Inputs).",
     yref("Annual", "rev")),
    ("Customer collections (mobile money)", "LCY", "Collected in LCY from the cohort engine.", f"=SUMIFS({mb.range_(O, 'collT')},{TL_YR},{YEARS})/1000000"),
    ("PAYGo receivables", "LCY", "Gross receivables in LCY; no USD indexation of existing contracts.", yref("Annual", "grossrec")),
    ("Hardware (FOB) and freight, duty", "USD", "Converted at the month's FX rate when units are sold; inventory follows COGS.",
     f"=SUMIFS({mb.range_(C_, 'cogs')},{TL_YR},{YEARS})/1000000"),
    ("Installation, commissions, opex", "LCY", "Indexed to local inflation.", f"=SUMIFS({mb.range_(C_, 'opex')},{TL_YR},{YEARS})/1000000"),
    ("RBF", "USD", "Set per unit in USD; received in LCY at the FX rate of the payment month.", yref("Annual", "rbf")),
    ("USD term loan", "USD", "Remeasured monthly at the closing rate; unrealised FX loss in the income statement.", yref("Annual", "tl")),
    ("Receivables facility or securitisation", "LCY", "Drawn and repaid in LCY against the borrowing base.", yref("Annual", "rf")),
    ("Equity", "LCY (investor view in USD)", "Booked in LCY; the investor's IRR and MOIC are measured in USD on Valuation.", yref("Annual", "te")),
    ("Hedging", "None", "No forward, swap or option is modelled. The depreciation path is a scenario lever (Scenarios).", '=""'),
]
for n_, (item, ccy, treat, f) in enumerate(CMAP):
    r_ = 6 + n_
    label(fxw, f"A{r_}", item, bold=True)
    label(fxw, f"B{r_}", ccy)
    label(fxw, f"C{r_}", treat, size=9)
    fxw.merge_cells(f"C{r_}:D{r_}")
    fxw[f"C{r_}"].alignment = Alignment(wrap_text=True, vertical="top")
    fxw.row_dimensions[r_].height = 30
    put_calc(fxw, f"E{r_}", f, "#,##0.0;(#,##0.0);\"-\"", link=True)
r_ = 6 + len(CMAP) + 1
mb.section(fxw, r_, "B. Exposure and effects by year (active scenario)"); r_ += 1
header_row(fxw, r_, ["Measure", "Unit"] + [f"Year {y}" for y in range(1, YEARS + 1)] + ["Total"], start_col=1); r_ += 1
FXY0 = r_
yc = lambda y: gcl(2 + y)  # C..G
FXROWS = [
    ("LCY depreciation against USD (scenario lever)", "% p.a.", lambda y: "=Scenarios!$G$10", FMT_PCT, None),
    ("FX rate at year end", "LCY / USD", lambda y: f"=INDEX({TL_FX},1,{y * 12})", FMT_NUM2, None),
    ("Pass-through of depreciation into new-contract prices", "%", lambda y: f"={INP['fx_pass']}", FMT_PCT, None),
    ("Share of debt in USD at year end", "%",
     lambda y: f"=IFERROR(Annual!{col(y)}{mb.r(A, 'tl')}/(Annual!{col(y)}{mb.r(A, 'tl')}+Annual!{col(y)}{mb.r(A, 'rf')}),0)", FMT_PCT, None),
]
for k_, text, unit in [(k, t, u) for k, t, u, _f in FX_SPECS]:
    FXROWS.append((text, unit + " m", lambda y, k_=k_: f"=SUMIFS({mb.range_(T, k_)},{TL_YR},{y})/1000000", "#,##0.0;(#,##0.0);\"-\"", "sum"))
FXR = {}
for n_, (text, unit, fn, fmt, tot) in enumerate(FXROWS):
    rr_ = FXY0 + n_
    label(fxw, f"A{rr_}", text, bold="Net transaction" in text)
    label(fxw, f"B{rr_}", unit, size=9, color=GREY_TXT)
    for y in range(1, YEARS + 1):
        put_calc(fxw, f"{yc(y)}{rr_}", fn(y), fmt, link=True)
    if tot:
        put_calc(fxw, f"H{rr_}", f"=SUM(C{rr_}:G{rr_})", fmt, bold=True)
    FXR[text] = rr_
FX_NET_TOT = f"FX_Exposure!$H${FXR['Net transaction effect on costs and RBF, before price pass-through (negative = cost)']}"
FX_USD_DEBT5 = f"FX_Exposure!$G${FXR['Share of debt in USD at year end']}"
rr_ = FXY0 + len(FXROWS) + 1
for t_ in ["Transaction effects compare each LCY amount with what it would have been at the opening rate. They are already inside the "
           "statements; this table isolates them. The USD principal effect is the realised counterpart of the remeasurement loss.",
           "The pass-through memo row is the offset on the revenue side: new contracts are priced up by the pass-through share of "
           "depreciation. It is booked at sale and collected over the tenor; the effect on financing income of older contracts is not isolated.",
           "Translation does not move LCY cash. It changes how LCY revenue and EBITDA look to a USD investor and drives the USD IRR.",
           "Monthly detail: Timeline, section FX EFFECTS. Stress the path on Scenarios (LCY depreciation) and read the change here and on Valuation."]:
    note(fxw, f"A{rr_}", t_); rr_ += 1


# =====================================================================
# SENSITIVITY (static snapshot)
# =====================================================================
SN = "Sensitivity"
snw = mb.sheet(SN, "Scenario & sensitivity table (static, dated) and the live active case",
               "Static rows: computed at DEFAULT inputs and recomputed inside this workbook for every case before release (date below). "
               "They do NOT update when inputs change; the LIVE row does.",
               tab="00B050")
SENS_METRICS = [("peak_eq_usd", "Peak equity need (USD m)", 1e-6, FMT_NUM2),
                ("rev5_usd", "Year 5 revenue (USD m)", 1e-6, FMT_NUM2),
                ("ebitda_m5", "Year 5 EBITDA margin", 1, FMT_PCT),
                ("cr5", "Year 5 collection rate", 1, FMT_PCT),
                ("ev_usd", "DCF EV (USD m)", 1e-6, FMT_NUM2),
                ("irr", "Investor IRR (USD)", 1, FMT_PCT),
                ("moic", "Investor MOIC", 1, FMT_X),
                ("breach_months", "Monthly covenant-breach months (excl. annual DSCR)", 1, FMT_INT)]
snw.column_dimensions["A"].width = 48
header_row(snw, 5, ["Case"] + [m[1] for m in SENS_METRICS])
for k_ in range(len(SENS_METRICS)):
    snw.column_dimensions[gcl(2 + k_)].width = 16
snw.row_dimensions[5].height = 32
SENS_ROW0 = 6
LIVE_ROW = SENS_ROW0 + 18
label(snw, f"A{LIVE_ROW - 1}", "LIVE: active case with the current inputs (updates with every change)", bold=True, color=NAVY)
put_calc(snw, f"A{LIVE_ROW}", "=Scenarios!$G$13", "@", bold=True, link=True)
LIVE_F = {"peak_eq_usd": H["peak_eq_usd"], "rev5_usd": f"KPIs!${col(YEARS)}${mb.r(K, 'rev_usd')}",
          "ebitda_m5": f"KPIs!${col(YEARS)}${mb.r(K, 'ebitda_m')}", "cr5": f"KPIs!${col(YEARS)}${mb.r(K, 'cr')}",
          "ev_usd": VAL["ev_usd"], "irr": VAL["irr"], "moic": VAL["moic"], "breach_months": H["breach_months"]}
for m, (key, text, scale, fmt) in enumerate(SENS_METRICS):
    ref_ = LIVE_F[key]
    f = f"=IF(ISNUMBER({ref_}),{ref_}*{scale},{ref_})" if scale != 1 else f"={ref_}"
    put_calc(snw, f"{gcl(2 + m)}{LIVE_ROW}", f, fmt, bold=True, link=True)

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
    ("Operational collection rate", "Instalments collected / instalments due in the period, excluding down payments. A cash conversion metric; "
     "not a PAYGo PERFORM KPI and never a substitute for the Repayment Rate."),
    ("Repayment Rate (PAYGo PERFORM 2026)", "Payments applied to due instalments / instalments due (PvP) or / total amount financed (PvFin), "
     "cumulative from contract start, on contract-level daily data; also at 90 days and at 2x contract term. Company-reported on PERFORM_2026."),
    ("Cohort repayment ratio (model)", "Cumulative collections / cumulative instalments due at a monthly checkpoint. Follows the logic of "
     "RR PvP but is not a PERFORM calculation."),
    ("Write-off rate", "Missed instalments written off / instalments due. The model writes off missed instalments as they fall due."),
    ("Receivables at risk (RaR)", "Carrying amount of receivables of accounts that have stopped paying (curve-based proxy). The 2021 PAYGo "
     "PERFORM guide (historical) defines RAR by consecutive days unpaid."),
    ("Expected credit loss (ECL)", "Lifetime expected loss recognised at origination from the scenario repayment curve "
     "(simplified, no staging). This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS."),
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
    ("DPD (days past due)", "Days since the account's oldest unpaid instalment. Buckets: current, 1-30, 31-60, 61-90, 91-180, 180+."),
    ("Stages 1 / 2 / 3", "Indicative IFRS 9-style staging by DPD thresholds (Credit_Assumptions). Used for the diagnostic ECL only."),
    ("Default EAD", "Exposure at default: receivables of accounts beyond the default definition (default 180 DPD)."),
    ("12-month PD proxy", "Proxy probability of default from the repayment curve (Proxy) or observed loss rate (Actual). NOT an audited IFRS 9 PD."),
    ("LGD proxy", "Loss given default proxy: 1 - net recoveries / exposure."),
    ("Proxy vs Actual data", "Proxy = model projection from curves. Actual = company data in Credit_Input / Vintage_Input. Never mixed silently."),
    ("Ownership Rate @2x (PAYGo PERFORM 2026)", "Contracts fully paid by twice the contract term / contracts that have reached 2x. "
     "Not modelled from proxies; company-reported on PERFORM_2026 or Vintage_Input."),
    ("RBF modes", "Sales-based (per unit sold), repayment-linked (scaled by repayment rate at verification), ownership-linked "
     "(paid on validated ownership at 2x tenor), hybrid (weighted)."),
    ("Warehouse vs securitisation", "Warehouse: revolving facility against eligible receivables. Securitisation: receivables financed through "
     "a term structure (here modelled on balance sheet with its own rate, advance haircut and fee)."),
    ("Evidence grades and status", "Grade of the source: A primary official or audited; B institutional or company disclosure; C reputable "
     "secondary; D unverified. Status: what has been verified (Source_Register). Only VERIFIED claims feed Calibration."),
    ("Investment readiness", "Progress against 23 evidence-based gates and a GO / CONDITIONAL GO / STOP rule driven only by those results. "
     "GO means the evidence file is complete for a decision; it is never an investment recommendation or a rating."),
    ("Provenance labels", "MODEL ASSUMPTION (set by the modeller), COMPANY DATA (supplied by the company), EXTERNAL EVIDENCE (from a "
     "VERIFIED source), CALIBRATED ASSUMPTION (re-estimated from company data or verified evidence), UNVERIFIED (source not yet read)."),
    ("Actual, assumption, forecast", "ACTUAL: company history on the input templates, never changed by scenario levers. ASSUMPTION: inputs. "
     "FORECAST: everything computed from the inputs under the active scenario."),
    ("Accounting treatment", "This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS. Revenue recognition, ECL, staging and tax are simplified (Chapter 8 of the book)."),
    ("RBF claim cycle", "Eligibility, claim, verification, disbursement. The working capital gap is subsidy claimed but not yet received (RBF_Engine)."),
    ("Transaction vs translation (FX)", "Transaction effects change LCY cash (USD hardware, USD debt service, USD RBF). Translation changes "
     "how LCY results look in USD. Remeasurement of USD debt is a non-cash entry (FX_Exposure)."),
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
label(iw, "A4", "Active case"); put_calc(iw, "B4", "=Scenarios!$G$13", "@", bold=True, link=True)
label(iw, "A5", "Master check"); put_calc(iw, "B5", f"={MASTER}", "@", bold=True, link=True)
label(iw, "D4", "Model version"); label(iw, "E4", VERSION, bold=True)
label(iw, "D5", "Currency"); put_calc(iw, "E5", f"={INP['currency']}", "@", link=True)
put_calc(iw, "A6", f"={READY}", "@", bold=True, link=True)
iw["A6"].font = Font(name=FONT, bold=True, color="C00000")
label(iw, "D6", "Credit data"); put_calc(iw, "E6", f"=IF({INP['credit_mode']}=1,\"PROXY\",\"ACTUAL\")", "@", bold=True, link=True)
r_ = 7
mb.section(iw, r_, "1. Operating & financial trajectory"); r_ += 1
header_row(iw, r_, ["Metric", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]); r_ += 1
for key, text, fmt in [("units", "Units sold", FMT_NUM), ("active", "Active PAYGo accounts (year end)", FMT_NUM),
                       ("asp_usd", "Average cash price per unit (USD)", FMT_NUM),
                       ("rev_usd", "Revenue (USD, average FX)", FMT_NUM), ("gm", "Gross margin", FMT_PCT),
                       ("ebitda_m", "EBITDA margin", FMT_PCT), ("ni", "Net income (LCY)", FMT_NUM),
                       ("cr", "Operational collection rate", FMT_PCT), ("rar", "Receivables at risk / gross receivables", FMT_PCT),
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
    ("Month from which operating cash flow stays positive", H["be_cfo"], FMT_INT)])
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
    ("Highest 30+ DPD ratio (projection)", f"Covenants!$C${mb.r(CV, 'dpd30')}", FMT_PCT),
    ("Highest 90+ DPD ratio (projection)", f"Covenants!$C${mb.r(CV, 'dpd90')}", FMT_PCT),
    ("RBF design mode", "RBF_Engine!$C$8", "@"),
    ("Receivables financing structure", f"IF({INP['fin_struct']}=1,\"Warehouse facility\",\"Securitisation\")", "@"),
    ("Months with any monthly covenant breach (DSCR is tested annually: next line)", H["breach_months"], FMT_INT),
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
dw = mb.sheet(D, "Dashboard: key metrics", "Active case. Each metric is labelled with its unit and source and rounded for reading; full precision "
              "stays on the source sheets.", tab="00B050")
label(dw, "A3", "Active case"); put_calc(dw, "B3", "=Scenarios!$G$13", "@", bold=True, link=True)
label(dw, "D3", "Master check"); put_calc(dw, "E3", f"={MASTER}", "@", bold=True, link=True)
dw.column_dimensions["A"].width = 58
dw.column_dimensions["B"].width = 12
for c_ in "CDEFG":
    dw.column_dimensions[c_].width = 12
dw.column_dimensions["H"].width = 48
header_row(dw, 5, ["Metric", "Unit", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Source / how to read"])
F_M = '#,##0.0,,;(#,##0.0,,);"-"'
F_P = '0.0%;(0.0%);"-"'
F_C = '#,##0;(#,##0);"-"'
kp = lambda k: (lambda y: f"=KPIs!{col(y)}{mb.r(K, k)}")
an = lambda k: (lambda y: f"=Annual!{col(y)}{mb.r(A, k)}")
one = lambda f: (lambda y: f if y == 1 else None)
fxe_row = lambda text: (lambda y: f"=FX_Exposure!{gcl(2 + y)}{FXR[text]}")
DASH = [
    ("Scale and customers", None),
    ("New customers (contracts originated in the year)", "#", kp("units"), F_C, "KPIs. One unit sold = one contract."),
    ("Customers: cumulative contracts originated", "#", lambda y: f"=SUMIFS({mb.range_(O, 'unitsT')},{TL_IDX},\"<=\"&{y * 12})", F_C, "Ops."),
    ("Active customers (accounts still paying, year end)", "#", kp("active"), F_C, "KPIs."),
    ("ARPU: revenue per average active account per month", "LCY",
     lambda y: (f"=IFERROR(KPIs!{col(y)}{mb.r(K, 'rev')}/((" + (f"KPIs!{col(y - 1)}{mb.r(K, 'active')}" if y > 1 else "0")
                + f"+KPIs!{col(y)}{mb.r(K, 'active')})/2)/12,\"n/a\")"), F_C,
     "Includes hardware revenue recognised at sale, so it is high in growth years."),
    ("Profitability", None),
    ("Revenue", "LCY m", kp("rev"), F_M, "KPIs. Revenue is not cash: see cash conversion."),
    ("Revenue", "USD m", kp("rev_usd"), F_M, "At average FX (FX_Exposure for translation)."),
    ("Gross margin", "%", kp("gm"), F_P, "KPIs."),
    ("EBITDA", "LCY m", kp("ebitda"), F_M, "KPIs. After expected credit losses and RBF income."),
    ("EBITDA margin", "%", kp("ebitda_m"), F_P, "KPIs."),
    ("Net income", "LCY m", kp("ni"), F_M, "KPIs."),
    ("Cash and portfolio", None),
    ("Cash balance (year end)", "LCY m", kp("cash"), F_M, "Held at the minimum by equity top-ups when needed."),
    ("PAYGo receivables, gross (year end)", "LCY m", an("grossrec"), F_M, "Annual."),
    ("PAYGo receivables, net of allowance (year end)", "LCY m", an("netrec"), F_M, "Annual."),
    ("Operational collection rate (not a PERFORM KPI)", "%", kp("cr"), F_P, "Collected / due, excluding deposits. Never the PERFORM Repayment Rate."),
    ("PAYGo PERFORM RR PvP, company-reported (portfolio, latest)", "%", one(f"={PF_OUT['pvp']}"), F_P,
     "PERFORM_2026. Blank in the model's own forecast; only company results count."),
    ("Receivables at risk / gross receivables (year end)", "%", kp("rar"), F_P, "Proxy; 2021 PERFORM logic (historical)."),
    ("30+ DPD / gross receivables (year end)", "%", kp("dpd30"), F_P, "Projection (Credit_Engine)."),
    ("90+ DPD / gross receivables (year end)", "%", kp("dpd90"), F_P, "Projection (Credit_Engine)."),
    ("Write-off rate (missed / due)", "%", kp("wo"), F_P, "KPIs."),
    ("Write-offs", "LCY m", lambda y: f"=SUMIFS({mb.range_(O, 'missedT')},{TL_YR},{y})", F_M, "Ops: missed instalments written off."),
    ("Cash conversion: operating cash flow / EBITDA", "x",
     lambda y: f"=IF(Annual!{col(y)}{mb.r(A, 'ebitda')}<=0,\"n/a\",Annual!{col(y)}{mb.r(A, 'cfo')}/Annual!{col(y)}{mb.r(A, 'ebitda')})",
     '0.00"x";(0.00"x")', "Below 1x while receivables grow; n/a when EBITDA is not positive."),
    ("Funding", None),
    ("Total debt (year end)", "LCY m", kp("debt"), F_M, "Term loan and receivables facility."),
    ("Book equity (year end)", "LCY m", an("te"), F_M, "Annual."),
    ("Cumulative equity invested", "LCY m", kp("eq_cum"), F_M, "Initial equity plus top-ups."),
    ("Funding requirement: equity top-ups in the year", "LCY m", kp("eq_top"), F_M, "Automatic top-up to hold minimum cash."),
    ("Peak equity requirement", "USD m", one(f"={H['peak_eq_usd']}"), F_M, "At opening FX (KPIs)."),
    ("RBF received", "LCY m", an("rbf"), F_M, "RBF_Engine, selected design; claim cycle and working capital gap there."),
    ("RBF dependency (RBF income / revenue)", "%", kp("rbf_share"), F_P, "KPIs."),
    ("Returns and timing", None),
    ("Investor IRR (USD)", "%", one(f"={VAL['irr']}"), F_P, "Valuation. Text when no IRR exists."),
    ("Investor MOIC (USD)", "x", one(f"={VAL['moic']}"), '0.00"x"', "Valuation."),
    ("NPV: DCF enterprise value at the discount rate", "USD m", one(f"={VAL['ev_usd']}"), F_M, "Valuation. Check the terminal value share."),
    ("Break-even: first month with positive EBITDA", "month #", one(f"={H['be_ebitda']}"), F_C, "KPIs."),
    ("Month from which operating cash flow stays positive", "month #", one(f"={H['be_cfo']}"), F_C, "KPIs."),
    ("Runway: months before the first equity top-up", "months",
     one(f"=IFERROR(MATCH(1,{mb.range_(S, 'eqtop_pos')},0)-1,\"No top-up in horizon\")"), F_C,
     "On initial equity and the debt modelled; 0 = top-up in month 1."),
    ("FX and readiness", None),
    ("LCY depreciation against USD (active scenario)", "% p.a.", one("=Scenarios!$G$10"), F_P, "Scenarios."),
    ("Share of debt in USD (year end)", "%", fxe_row("Share of debt in USD at year end"), F_P, "FX_Exposure."),
    ("Net FX transaction effect on costs and RBF (before price pass-through)", "LCY m",
     lambda y: f"=FX_Exposure!{gcl(2 + y)}{FXR['Net transaction effect on costs and RBF, before price pass-through (negative = cost)']}*1000000", F_M,
     "FX_Exposure. Negative = cost."),
    ("Investment readiness: gates met", "of 23", one("=Investment_Readiness!$C$4"), F_C, "Investment_Readiness."),
    ("Investment readiness: decision (evidence only)", "", one(f"={DECISION}"), "@", "GO / CONDITIONAL GO / STOP; never a recommendation."),
]
r_ = 6
for row_ in DASH:
    if row_[1] is None:
        mb.section(dw, r_, row_[0]); r_ += 1
        continue
    text, unit, fn, fmt, src = row_
    label(dw, f"A{r_}", text)
    label(dw, f"B{r_}", unit, size=9, color=GREY_TXT)
    for y in range(1, YEARS + 1):
        f = fn(y)
        if f is not None:
            put_calc(dw, f"{gcl(2 + y)}{r_}", f, fmt, link=True)
    label(dw, f"H{r_}", src, size=9, italic=True, color=GREY_TXT)
    dw[f"H{r_}"].alignment = Alignment(indent=2)
    r_ += 1
note(dw, f"A{r_ + 1}", "Rounded for reading: money in millions to one decimal, ratios to one decimal place, counts to the unit. Single values "
     "(returns, peaks, timing, readiness) are shown under Year 1.")
DASH_END = r_ + 1


def chart_rows(ch, ws_, keys, sheet_key, names=None):
    from openpyxl.chart.series import SeriesLabel
    for n_, key in enumerate(keys):
        ch.add_data(Reference(ws_, min_col=5, max_col=4 + YEARS, min_row=mb.r(sheet_key, key)), from_rows=True,
                    titles_from_data=False)
        if names:
            ch.series[-1].tx = SeriesLabel(v=names[n_])
    ch.set_categories(Reference(ws_, min_col=5, max_col=4 + YEARS, min_row=5))
    ch.height, ch.width = 8, 15


c1 = BarChart(); c1.title = "Revenue & EBITDA (LCY)"; chart_rows(c1, aw, ["rev", "ebitda"], A, ["Revenue", "EBITDA"]); dw.add_chart(c1, "J5")
c2 = BarChart(); c2.grouping = "stacked"; c2.overlap = 100
c2.title = "Units sold by tier"; chart_rows(c2, kpw, [f"units{j}" for j in range(NP)], K, [f"Tier {p['tier']}" for p in PRODUCTS]); dw.add_chart(c2, "S5")
c3 = LineChart(); c3.title = "Collection rate & write-off rate"; chart_rows(c3, kpw, ["cr", "wo"], K, ["Operational collection rate", "Write-off rate"])
c3.y_axis.number_format = "0%"; dw.add_chart(c3, "J22")
c4 = LineChart(); c4.title = "Cumulative equity vs total debt (LCY)"; chart_rows(c4, kpw, ["eq_cum", "debt"], K, ["Cumulative equity", "Total debt"])
dw.add_chart(c4, "S22")
note(dw, f"A{DASH_END + 1}", "Charts, series order: Revenue, EBITDA | Tier 1..5 | Collection, Write-off | Equity, Debt.")

# =====================================================================
# COVER
# =====================================================================
cts.column_dimensions["A"].width = 30
cts.column_dimensions["B"].width = 100
info = [("Model", "MODEL 2: PAYGo Company Financial & Investment Model (solar home systems, MTF Tiers 1-5), companion to Book 2, PAYGo Solar Finance"),
        ("Version", f"{VERSION} - development build, generated {date.today().isoformat()}"),
        ("Status", "Draft for expert review. Default inputs are illustrative. Readiness and decision: see Investment_Readiness."),
        ("Accounting", "This is an analytical modelling treatment and does not constitute a determination of the applicable accounting "
                       "treatment under IFRS."),
        ("Currency", "Model currency = LCY. Hardware, RBF and term debt in USD, converted at the Timeline FX path (FX_Exposure)."),
        ("Periodicity", f"Monthly over {MONTHS} months; annual roll-ups on Annual, KPIs and Valuation."),
        ("Master check", None)]
for k_, (a_, b_) in enumerate(info):
    label(cts, f"A{4 + k_}", a_, bold=True)
    if b_:
        label(cts, f"B{4 + k_}", b_)
        cts[f"B{4 + k_}"].alignment = Alignment(wrap_text=True, vertical="top")
MC_ROW = 4 + len(info) - 1
put_calc(cts, f"B{MC_ROW}", f"={MASTER}", "@", bold=True)
cts[f"B{MC_ROW}"].font = Font(name=FONT, bold=True, color="C00000")
r_c = MC_ROW + 2
label(cts, f"A{r_c}", "How to use", bold=True, color=NAVY, size=11)
steps = ["1. Start: what to input, what the model calculates, what it means and what an investor should look at.",
         "2. Inputs, Products, Credit_Assumptions, Scenarios (blue cells; yellow = review first; provenance label on every input).",
         "3. Company history (ACTUAL): Credit_Input, Vintage_Input and PERFORM_2026 section C. Scenario levers never change history.",
         "4. Read Investment_Summary, Dashboard and Investment_Readiness, then KPIs, Valuation, Covenants, FX_Exposure and Unit_Economics.",
         "5. Audit trail: FS > Ops > Cohort_T1..T5 > Curves. Every number traces back to an input.",
         "6. The master check must read OK before any output is used."]
for k_, s_ in enumerate(steps):
    label(cts, f"B{r_c + 1 + k_}", s_)
IDX_ROW = r_c + 1 + len(steps) + 1  # sheet index written after the tab order is fixed (write_index)
SHEET_DESC = {
    "Cover": "Title page and model status", "Start": "Start here: inputs, calculations, meaning, what to look at",
    "Contents": "This page: all sheets in tab order",
    "Investment_Summary": "One-page investment committee and lender summary",
    "Investment_Readiness": "23 evidence-based gates and the GO / CONDITIONAL GO / STOP rule",
    "Inputs": "Global inputs with provenance labels", "Products": "Tiers 1-5: specification, price plans, risk, with provenance",
    "Scenarios": "Stress levers, input set loaded and the scenario architecture",
    "Credit_Assumptions": "DPD buckets, stages, default definition, recovery, eligibility",
    "Consumer_Risk": "Affordability, APR, consumer-protection evidence",
    "Dashboard": "Key metrics by year, labelled and rounded, with charts", "KPIs": "Portfolio, financial and lender KPIs",
    "Credit_Portfolio": "Credit dashboard (selected data mode)", "Vintage_Dashboard": "Cohort coverage, M12 summary, vintage curve",
    "PERFORM_2026": "PAYGo PERFORM 2026 KPIs: company-reported results and labelled approximations",
    "Covenants": "Monthly covenant tests", "Valuation": "DCF and investor IRR / MOIC",
    "FX_Exposure": "Currency map, hedging, transaction and translation effects",
    "Unit_Economics": "Per-unit economics by tier", "Sensitivity": "Static scenario and sensitivity table, plus the live active case",
    "Benchmark_Compare": "Model against graded peers, with comparability warnings",
    "Benchmark_KPIs": "Derived financial and operational ratios", "Market_Benchmark": "Scaled PAYGo companies against this model (context)",
    "Calibration": "Diagnostics against VERIFIED references only", "Company_Cases": "Lessons from scaled PAYGo companies",
    "Source_Register": "Graded sources with verification status", "Benchmark_Matrix": "Company-year by line item",
    "Benchmark_DB": "Raw benchmark records with period, definition, page and status",
    "Annual": "Annual statements", "FS": "Monthly statements", "Ops": "Portfolio engine",
    "RBF_Engine": "RBF designs and the claim cycle (eligibility to disbursement, working capital gap)",
    "Credit_Engine": "Proxy and selected credit metrics by tier", "Vintage_Engine": "Cohort KPIs by checkpoint",
    "Costs": "Costs, working capital, capex", "Financing": "Equity, term loan, receivables facility",
    "Curves": "Per-unit repayment curves", "Credit_Input": "Company portfolio data template (ACTUAL)",
    "Vintage_Input": "Company cohort data template (ACTUAL)", "Timeline": "Dates, FX path, indices and monthly FX effects",
    "Glossary": "Terms as implemented in the model", "Checks": "Integrity checks and readiness flags",
}
for j in range(NP):
    SHEET_DESC[f"Cohort_T{j + 1}"] = f"Vintage matrices, Tier {PRODUCTS[j]['tier']}"


def write_index(order_):
    label(cts, f"A{IDX_ROW}", "Sheet index (tab order)", bold=True, color=NAVY, size=11)
    for k_, sh in enumerate(order_):
        r_ = IDX_ROW + 1 + k_
        cell = cts[f"A{r_}"]
        cell.value = f"{k_ + 1:02d}  {sh}"
        cell.hyperlink = f"#'{sh}'!A1"
        cell.font = Font(name=FONT, color="0563C1", underline="single")
        label(cts, f"B{r_}", SHEET_DESC[sh])
    base = IDX_ROW + len(order_) + 2
    label(cts, f"A{base}", "Colour code", bold=True, color=NAVY, size=11)
    label(cts, f"A{base + 1}", "1,000", color=BLUE); label(cts, f"B{base + 1}", "Blue = hard-coded input")
    cts[f"A{base + 2}"] = "1,000"; cts[f"A{base + 2}"].font = Font(name=FONT, color=BLUE)
    cts[f"A{base + 2}"].fill = PatternFill("solid", fgColor="FFFF00"); label(cts, f"B{base + 2}", "Yellow fill = key assumption")
    label(cts, f"A{base + 3}", "1,000"); label(cts, f"B{base + 3}", "Black = formula")
    label(cts, f"A{base + 4}", "1,000", color=GREEN); label(cts, f"B{base + 4}", "Green = link from another sheet")
    for n_, lab_ in enumerate(PROV_LABELS):
        r_ = base + 5 + n_
        cts[f"A{r_}"] = lab_
        cts[f"A{r_}"].font = Font(name=FONT, size=8, bold=True, color="404040")
        cts[f"A{r_}"].fill = PatternFill("solid", fgColor=PROV_FILL[lab_])
        label(cts, f"B{r_}", "Provenance label (see Start and Glossary)")
    label(cts, f"A{base + 11}", "Disclaimer", bold=True, color=NAVY, size=11)
    cts[f"B{base + 11}"] = ("Decision-support tool. Not investment, legal, tax or accounting advice. Default inputs are illustrative. "
                            "This is an analytical modelling treatment and does not constitute a determination of the applicable accounting "
                            "treatment under IFRS. Users are responsible for their inputs and conclusions.")
    cts[f"B{base + 11}"].alignment = Alignment(wrap_text=True, vertical="top")
    cts[f"B{base + 11}"].font = Font(name=FONT, size=9)
    cts.row_dimensions[base + 11].height = 40


# =====================================================================
# BRANDED COVER PAGE
# =====================================================================
from openpyxl.drawing.image import Image as XLImage  # noqa: E402

BRAND_GREEN, BRAND_GOLD, BRAND_CREAM, BRAND_GREY = "0B3020", "B07C0F", "F7F3E8", "6B6B6B"
LOGO = Path(__file__).resolve().parents[1] / "brand" / "aef_logo.png"
AUTHOR = "Emmanuel Boujieka Kamga"
cov.sheet_view.showGridLines = False
cov.sheet_view.zoomScale = 90
cov.sheet_properties.tabColor = BRAND_GREEN
for c_, w_ in zip("ABCDEFGHIJKLM", [3, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16, 4, 3]):
    cov.column_dimensions[c_].width = w_


def band(r1, r2, color, c1="B", c2="L"):
    for r_ in range(r1, r2 + 1):
        for c_ in range(ord(c1), ord(c2) + 1):
            cov[f"{chr(c_)}{r_}"].fill = PatternFill("solid", fgColor=color)


def ctext(cell, text, size=11, color="FFFFFF", bold=False, italic=False, align="left"):
    cov[cell] = text
    cov[cell].font = Font(name=FONT, size=size, color=color, bold=bold, italic=italic)
    cov[cell].alignment = Alignment(horizontal=align, vertical="center")


for r_ in range(1, 15):
    cov.row_dimensions[r_].height = 18
if LOGO.exists():
    img = XLImage(str(LOGO))
    ratio = img.height / img.width
    img.width = 600
    img.height = int(600 * ratio)
    cov.add_image(img, "C3")
band(15, 15, BRAND_GOLD); cov.row_dimensions[15].height = 5
band(16, 31, BRAND_GREEN)
for r_ in range(16, 32):
    cov.row_dimensions[r_].height = 20
ctext("C18", "MODEL 2  |  BOOK 2, PAYGo SOLAR FINANCE" + (f"  |  {CASE['title']}" if CASE else ""), 12, BRAND_GOLD, bold=True)
ctext("C20", "SOLAR HOME SYSTEMS", 30, bold=True); cov.row_dimensions[20].height = 40
ctext("C22", "PAYGo Company Financial & Investment Model", 18); cov.row_dimensions[22].height = 26
ctext("C24", "From business model to investment decision  |  MTF Tiers 1-5  |  Credit, vintage, PERFORM, RBF, FX and benchmark engines", 11, "E3C77A", italic=True)
ctext("C27", "AUTHOR & IDEATION", 9, BRAND_GOLD, bold=True)
ctext("C28", AUTHOR, 16, bold=True); cov.row_dimensions[28].height = 24
ctext("C30", f"Version {VERSION}  |  Development build  |  {date.today().strftime('%d %B %Y')}", 10, "D9D9D9")
band(32, 32, BRAND_GOLD); cov.row_dimensions[32].height = 5
band(33, 41, BRAND_CREAM)
ctext("C34", "MODEL STATUS", 9, BRAND_GREEN, bold=True)
status = [("Master check", f"={MASTER}"), ("Investment readiness", f"={READY}"),
          ("Active case", "=Scenarios!$G$13"),
          ("Credit data", f"=IF({INP['credit_mode']}=1,\"Proxy (model curves)\",\"Actual (company data)\")"),
          ("Currency", f"={INP['currency']}&\" (local), USD for hardware, RBF and term debt\"")]
for n_, (lab, f) in enumerate(status):
    r_ = 35 + n_
    ctext(f"C{r_}", lab, 10, BRAND_GREY)
    cov[f"E{r_}"] = f
    cov[f"E{r_}"].font = Font(name=FONT, size=10, bold=True, color=BRAND_GREEN)
    cov[f"E{r_}"].alignment = Alignment(horizontal="left", vertical="center")
for n_, (lab, target) in enumerate([("Start here: Contents  >", "Contents"), ("Investment summary  >", "Investment_Summary"),
                                     ("Investment readiness  >", "Investment_Readiness")]):
    cell = cov[f"{'CEH'[n_]}41"]
    cell.value = lab
    cell.hyperlink = f"#'{target}'!A1"
    cell.font = Font(name=FONT, size=10, bold=True, color=BRAND_GOLD, underline="single")
from openpyxl.formatting.rule import CellIsRule  # noqa: E402
cov.conditional_formatting.add("E35", CellIsRule(operator="equal", formula=['"OK"'], font=Font(name=FONT, bold=True, color="1E7B34")))
cov.conditional_formatting.add("E35", CellIsRule(operator="equal", formula=['"ERROR"'], font=Font(name=FONT, bold=True, color="C00000")))
cov.merge_cells("C43:K45")
cov["C43"] = ("Decision-support tool. Not investment, legal, tax or accounting advice. Default inputs are illustrative placeholders for a "
              "fictional company in a fictional market; market data are graded in Source_Register. This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS. "
              "Readiness is decided on evidence only (see Investment_Readiness).")
cov["C43"].font = Font(name=FONT, size=8, italic=True, color=BRAND_GREY)
cov["C43"].alignment = Alignment(wrap_text=True, vertical="top")
ctext("C47", f"(c) {date.today().year} {AUTHOR}. All rights reserved.  |  Africa Energy Finance - Business & Financial Models",
      8, BRAND_GREY)
cov.print_area = "A1:M48"
cov.page_setup.orientation = "landscape"
cov.page_setup.fitToWidth = 1
cov.page_setup.fitToHeight = 1
cov.sheet_properties.pageSetUpPr.fitToPage = True


# =====================================================================
# SCENARIO ARCHITECTURE (v0.8, M12): actual, assumption and forecast kept apart
# =====================================================================
hist_n = ("+".join(f"COUNT({ci_range(j, 'gross')})" for j in range(NP)) + "+" + "+".join(f"COUNT({vi_range(j, 'C')})" for j in range(NP))
          + "+" + "+".join(PF_COUNT))
mb.section(sw, 18, "Scenario architecture: ACTUAL is never changed by levers; ASSUMPTION is the input set; FORECAST is computed")
header_row(sw, 19, ["Layer", "Type", "Where it lives", "", "", "", "Status in this workbook"])
ARCH = [
    ("Actual (history)", "ACTUAL", "Credit_Input, Vintage_Input, PERFORM_2026 section C; read on Credit_Portfolio and Vintage_Dashboard",
     f"=IF(({hist_n})>0,\"Loaded (\"&({hist_n})&\" records; levers do not apply)\",\"Not loaded\")"),
    ("Management case", "ASSUMPTION", "Inputs, Products, Credit_Assumptions as submitted by management",
     f"=IF({INP['input_set']}=\"Management case\",\"Loaded on the input sheets\",\"Not loaded\")"),
    ("Calibrated case", "ASSUMPTION (calibrated)", "Same input sheets after re-estimation against actual data and VERIFIED sources (Calibration)",
     f"=IF({INP['input_set']}=\"Calibrated case\",\"Loaded on the input sheets\",\"Not loaded\")"),
    ("Base", "FORECAST", "Loaded input set with Base levers (column C)", f"=IF({INP['scenario']}=1,\"Active\",\"\")"),
    ("Downside", "FORECAST", "Loaded input set with Downside levers (column D)", f"=IF({INP['scenario']}=2,\"Active\",\"\")"),
    ("Severe stress", "FORECAST", "Loaded input set with Severe levers (column E)", f"=IF({INP['scenario']}=3,\"Active\",\"\")"),
]
for n_, (lay, typ, where, st) in enumerate(ARCH):
    r_ = 20 + n_
    label(sw, f"A{r_}", lay, bold=True); label(sw, f"B{r_}", typ, size=9)
    label(sw, f"C{r_}", where, size=9)
    put_calc(sw, f"G{r_}", st, "@", bold=True)
note(sw, "A27", "One input set is loaded at a time. The other set is kept outside the workbook (for the worked case: the case file and the "
     "book's comparison table). History is entered on the input templates only and is never overwritten by forecast levers.")

# =====================================================================
# START (v0.8, M7)
# =====================================================================
stw.column_dimensions["A"].width = 6
stw.column_dimensions["B"].width = 30
stw.column_dimensions["C"].width = 92
stw.column_dimensions["D"].width = 24
for n_, (lab, f) in enumerate([("Master check", f"={MASTER}"), ("Active case", "=Scenarios!$G$13"),
                               ("Credit data", f"=IF({INP['credit_mode']}=1,\"PROXY (model curves)\",\"ACTUAL (company data)\")"),
                               ("Readiness decision", f"={DECISION}&\": \"&{DECISION_WHY}")]):
    label(stw, f"B{4 + n_}", lab, bold=True)
    put_calc(stw, f"C{4 + n_}", f, "@", bold=True, link=True)


def start_block(r0, title, rows_):
    mb.section(stw, r0, title)
    for n_, (sheet_, text) in enumerate(rows_):
        r_ = r0 + 1 + n_
        put_calc(stw, f"A{r_}", n_ + 1, FMT_INT)
        if sheet_:
            cell = stw[f"B{r_}"]
            cell.value = sheet_.split(",")[0]
            cell.hyperlink = f"#'{sheet_.split(',')[0]}'!A1"
            cell.font = Font(name=FONT, color="0563C1", underline="single")
            if "," in sheet_:
                cell.value = sheet_
        label(stw, f"C{r_}", text)
        stw[f"C{r_}"].alignment = Alignment(wrap_text=True, vertical="top")
    return r0 + len(rows_) + 2


r_ = start_block(9, "1. WHAT TO INPUT (blue cells; every input carries a provenance label)", [
    ("Inputs", "Scenario selector, macro and FX, volumes, operating costs, RBF design, working capital, financing, covenants, valuation."),
    ("Products", "Five tiers: specification, price plan (cash price, deposit, daily rate, tenor), costs, credit risk, recovery, RBF, advance rate."),
    ("Credit_Assumptions", "Default definition, staging thresholds, borrowing-base eligibility, recovery cost, proxy DPD distribution."),
    ("Scenarios", "Base, Downside and Severe levers, and which input set is loaded (management or calibrated)."),
    ("Consumer_Risk", "Affordability review switch and the status of consumer-protection and PERFORM evidence."),
    ("Credit_Input", "ACTUAL: monthly portfolio history by tier (DPD buckets, write-offs, unlocks). Set the credit data mode to 2."),
    ("Vintage_Input", "ACTUAL: cohort checkpoints (collections and instalments due) and validated ownership at 2x if available."),
    ("PERFORM_2026", "ACTUAL: PAYGo PERFORM 2026 results computed by the company on contract-level data (section C)."),
    ("Investment_Readiness", "Manual gates: status, where the evidence is held, who signed it off and when."),
])
r_ = start_block(r_, "2. WHAT THE MODEL CALCULATES", [
    ("Curves", "Per-unit repayment, default and recovery by account age for each tier."),
    ("Ops", "Cohorts by month of sale (Cohort_T1..T5): collections, write-offs, receivables, active accounts, RBF."),
    ("FS", "Monthly income statement, balance sheet and cash flow; Annual rolls them up. The balance sheet balances every month (Checks)."),
    ("Financing", "Receivables facility drawn within the borrowing base, USD term loan, automatic equity top-up to hold minimum cash."),
    ("Credit_Engine", "DPD buckets, default, PD and LGD proxies, indicative ECL, borrowing-base eligibility."),
    ("RBF_Engine", "RBF under the selected design, and the claim cycle from eligibility to disbursement."),
    ("Valuation", "DCF and the investor's USD IRR and MOIC; Covenants tests the facility terms monthly; FX_Exposure isolates FX effects."),
])
r_ = start_block(r_, "3. WHAT THE RESULTS MEAN (read before quoting any number)", [
    (None, "Revenue is not cash. A PAYGo sale books revenue at once and collects over the tenor: read cash conversion and the funding requirement."),
    (None, "The operational collection rate is a cash measure. It is not the PAYGo PERFORM Repayment Rate, which only company data can produce."),
    (None, "ECL, PD and staging are analytical proxies. " + "This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS."),
    (None, "Every input is labelled: MODEL ASSUMPTION, COMPANY DATA, EXTERNAL EVIDENCE, CALIBRATED ASSUMPTION or UNVERIFIED (counts below)."),
    (None, "The readiness decision measures the evidence file. GO is never an investment recommendation; STOP on incomplete evidence is not a verdict on the business."),
])
r_ = start_block(r_, "4. WHAT AN INVESTOR SHOULD LOOK AT, IN THIS ORDER", [
    ("Investment_Summary", "Trajectory, funding requirement, returns, lender view and unit economics on one page."),
    ("Dashboard", "Key metrics by year, labelled and rounded."),
    ("Investment_Readiness", "Gates met, missing evidence and the decision with its reason."),
    ("Sensitivity", "Downside and Severe, and the single levers that move peak equity and IRR the most."),
    ("Vintage_Dashboard", "Cohort behaviour by tier; then PERFORM_2026 for company-reported KPIs."),
    ("Covenants", "Months with a breach and the tightest covenant."),
    ("FX_Exposure", "Which items sit in USD, the hedge position and the transaction effect on cash."),
    ("Unit_Economics", "Lifetime contribution, LTV / CAC and payback by tier."),
    ("Checks", "Master check OK and the readiness flags."),
])
mb.section(stw, r_, "5. PROVENANCE OF INPUTS (count of labelled inputs)"); r_ += 1
prov_ranges = sorted({(sh, re.sub(r"\d", "", c_)) for sh, c_ in PROV_CELLS})
for lab_ in PROV_LABELS:
    cnt = "+".join(f"COUNTIF({q(sh)}!${cl}$1:${cl}$200,\"{lab_}\")" for sh, cl in prov_ranges)
    stw[f"B{r_}"] = lab_
    stw[f"B{r_}"].font = Font(name=FONT, size=8, bold=True, color="404040")
    stw[f"B{r_}"].fill = PatternFill("solid", fgColor=PROV_FILL[lab_])
    put_calc(stw, f"D{r_}", "=" + cnt, FMT_INT, bold=True)
    r_ += 1
note(stw, f"C{r_ + 1}", "Labels describe where a value comes from. Change the label when you replace a value (for example, from MODEL ASSUMPTION to COMPANY DATA).")

# provenance cells accept the five labels only
dv_prov = DataValidation(type="list", formula1='"' + ",".join(PROV_LABELS) + '"', allow_blank=False)
for sh in {sh for sh, _c in PROV_CELLS}:
    dvp = copy.copy(dv_prov)
    wb[sh].add_data_validation(dvp)
    for sh2, c_ in PROV_CELLS:
        if sh2 == sh:
            dvp.add(c_)

# data-type tags (ACTUAL / ASSUMPTION / FORECAST) and the accounting statement on the credit sheets
TAGS = {"Inputs": "ASSUMPTION", "Products": "ASSUMPTION", "Scenarios": "ASSUMPTION", "Credit_Assumptions": "ASSUMPTION",
        "Consumer_Risk": "ASSUMPTION", "Credit_Input": "ACTUAL", "Vintage_Input": "ACTUAL", "PERFORM_2026": "ACTUAL (section C) and FORECAST approximations",
        "FS": "FORECAST", "Annual": "FORECAST", "KPIs": "FORECAST", "Ops": "FORECAST", "Costs": "FORECAST", "Financing": "FORECAST",
        "Valuation": "FORECAST", "Covenants": "FORECAST", "Unit_Economics": "FORECAST", "Curves": "FORECAST", "RBF_Engine": "FORECAST",
        "Credit_Engine": "FORECAST (Proxy) or ACTUAL (selected block in Actual mode)", "Credit_Portfolio": "FORECAST or ACTUAL (selected data mode)",
        "Vintage_Engine": "ACTUAL cohorts and FORECAST proxy", "Vintage_Dashboard": "ACTUAL cohorts and FORECAST proxy",
        "FX_Exposure": "FORECAST", "Dashboard": "FORECAST", "Timeline": "FORECAST"}
for j in range(NP):
    TAGS[f"Cohort_T{j + 1}"] = "FORECAST"
for sh, tag in TAGS.items():
    wb[sh]["A2"] = f"[{tag}]  " + (wb[sh]["A2"].value or "")
for sh in ("Credit_Engine", "Credit_Portfolio", "FS", "Annual"):  # Credit_Assumptions carries it in its own subtitle
    wb[sh]["A2"] = wb[sh]["A2"].value + "  This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS."


# =====================================================================
# ORDER, PRINT SETUP, SNAPSHOT, SAVE
# =====================================================================
order = ["Cover", "Start", "Contents", "Investment_Summary", "Investment_Readiness", "Inputs", "Products", "Scenarios", "Credit_Assumptions",
         "Consumer_Risk", "Dashboard", "KPIs", "Credit_Portfolio", "Vintage_Dashboard", "PERFORM_2026", "Covenants", "Valuation",
         "FX_Exposure", "Unit_Economics", "Sensitivity", "Benchmark_Compare", "Benchmark_KPIs", "Market_Benchmark", "Calibration",
         "Company_Cases", "Source_Register", "Benchmark_Matrix", "Benchmark_DB",
         "Annual", "FS", "Ops", "RBF_Engine", "Credit_Engine", "Vintage_Engine", "Costs", "Financing", "Curves"] + \
        [f"Cohort_T{j + 1}" for j in range(NP)] + ["Credit_Input", "Vintage_Input", "Timeline", "Glossary", "Checks"]
assert sorted(order) == sorted(wb.sheetnames), set(order) ^ set(wb.sheetnames)
wb._sheets = [wb[n] for n in order]
write_index(order)


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
    note(snw, f"A{end + 1}", f"Static table computed on {date.today().strftime('%d %B %Y')} at default inputs and recomputed inside this "
         "workbook for every case (largest relative difference below one in a billion). To test your own assumptions, read the LIVE row.")
    ch = BarChart(); ch.type = "bar"; ch.title = "Investor IRR by case (static)"
    ch.add_data(Reference(snw, min_col=7, max_col=7, min_row=SENS_ROW0, max_row=end - 1), titles_from_data=False)
    ch.series[-1].tx = SeriesLabel(v="Investor IRR (USD)")
    ch.set_categories(Reference(snw, min_col=1, max_col=1, min_row=SENS_ROW0, max_row=end - 1))
    ch.height, ch.width = 9, 18
    snw.add_chart(ch, f"A{LIVE_ROW + 3}")


if CASE:  # load the case's synthetic portfolio history into the data-input templates
    hist_credit, hist_vint = CASE_MOD.history(PRODUCTS, G)
    for j, rows in hist_credit.items():
        for i, rec in enumerate(rows):
            r_ = CI_R0(j) + i
            for k_, v in rec.items():
                cell = wb[CIN][f"{CI_COL[k_]}{r_}"]
                cell.value = (date.fromisoformat(v) if k_ == "date" else v)
    for j, cohorts in hist_vint.items():
        for ci, rec in cohorts.items():
            r_ = VI_R0(j) + ci - 1
            wb[VIN][f"B{r_}"] = 2
            wb[VIN][f"C{r_}"] = float(rec["units"])
            for k_idx, vals in rec["cp"].items():
                for mk, v in vals.items():
                    wb[VIN][f"{vi_col(mk, k_idx)}{r_}"] = float(v)
            if rec["own"] is not None:
                wb[VIN][f"{VI_OWN_COL}{r_}"] = rec["own"]
            wb[VIN][f"{VI_NOTE_COL}{r_}"] = "SYNTHETIC - teaching data"
if "--snapshot" in sys.argv:
    fill_snapshot()
else:
    note(snw, f"A{SENS_ROW0 + 12}", "Table not populated in this build.")

for wsx in wb.worksheets:
    set_font_all(wsx)
    if wsx.title == "Cover":
        continue
    wsx.page_setup.orientation = "landscape"
    wsx.page_setup.fitToWidth = 1
    wsx.page_setup.fitToHeight = 0
    wsx.sheet_properties.pageSetUpPr.fitToPage = True
DASH_FIX = [("\u2014", ", "), ("\u2013", " to "), (" - ", ": ")]


def _clean_text(t):
    for a, b in DASH_FIX:
        t = t.replace(a, b)
    return t


def _clean_formula(f):
    return re.sub(r'"([^"]*)"', lambda m: '"' + _clean_text(m.group(1)) + '"', f)


import re  # noqa: E402
for wsx in wb.worksheets:
    for row_ in wsx.iter_rows():
        for cell in row_:
            v = cell.value
            if isinstance(v, str) and v:
                cell.value = _clean_formula(v) if v.startswith("=") else _clean_text(v)
    wsx.oddFooter.left.text = f"Africa Energy Finance | MODEL 2 PAYGo {VERSION}"
    wsx.oddFooter.center.text = "&A"
    wsx.oddFooter.right.text = "Page &P of &N"
    for part in (wsx.oddFooter.left, wsx.oddFooter.center, wsx.oddFooter.right):
        part.size = 8
        part.font = "Arial"
wb.calculation = CalcProperties(fullCalcOnLoad=True)
wb.properties.title = "AEF Model 2: PAYGo Company Financial & Investment Model"
wb.properties.creator = "Emmanuel Boujieka Kamga"
wb.properties.subject = "Africa Energy Finance, Business & Financial Models, Book 2 (PAYGo Solar Finance)"
wb.properties.lastModifiedBy = "Emmanuel Boujieka Kamga"
OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)


def _neutral_app_metadata(path):
    """Replace the writer-library name in docProps/app.xml with the publisher name (Excel overwrites it on first save)."""
    import shutil
    import tempfile
    import zipfile
    tmp = Path(tempfile.mkstemp(suffix=".xlsx")[1])
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/app.xml":
                data = re.sub(rb"<Application>.*?</Application>", b"<Application>Africa Energy Finance</Application>", data)
            zout.writestr(item, data)
    shutil.move(tmp, path)


_neutral_app_metadata(OUT)
print(OUT)
