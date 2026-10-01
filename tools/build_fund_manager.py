"""Build the Energy Access Fund Manager Model - RBF & Portfolio Edition (product 3).

Usage: python tools/build_fund_manager.py [output.xlsx] [--lang fr]
Then recalculate (open in Excel, or LibreOffice headless) so cached values exist.

Design notes
- Project-indexed sheets (Pipeline, Eligibility & Scoring, Disbursements, MRV Tracker) share the same
  row for a given project, so every cross-sheet reference is row-aligned.
- Allocation is sequential in rank order on its own sheet: each row only looks at rows above it,
  so envelope and country-concentration limits are enforced without circular references.
- Scores are normalised against the best eligible project using helper columns (plain MAX), so the
  workbook needs no MAXIFS/MINIFS and works in Excel 2010+.
"""
import sys
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

import i18n
import print_areas

LANG, OUT = i18n.setup(sys.argv)
T = i18n.T
if OUT is None:
    OUT = {"en": "product/03-fund-manager/EnergyAccess_Fund_Manager_Model_v1.xlsx",
           "fr": "product/03-fund-manager/Modele_Gestionnaire_Fonds_Acces_Energie_v1_FR.xlsx"}[LANG]

NP = 25           # project rows
FY = 10           # fund years
FIRST = 7         # first project row on project-indexed sheets
LAST = FIRST + NP - 1
FONT = "Arial"
NAVY, TEAL, LIGHT, YELLOW = "1F3A5F", "1B7F79", "EEF3F8", "FFF2CC"

f_title = Font(name=FONT, size=16, bold=True, color=NAVY)
f_h1 = Font(name=FONT, size=11, bold=True, color="FFFFFF")
f_h2 = Font(name=FONT, size=10, bold=True, color=NAVY)
f_txt = Font(name=FONT, size=10)
f_bold = Font(name=FONT, size=10, bold=True)
f_note = Font(name=FONT, size=9, italic=True, color="666666")
f_input = Font(name=FONT, size=10, color="0000FF")
f_link = Font(name=FONT, size=10, color="008000")
fill_h1 = PatternFill("solid", fgColor=NAVY)
fill_sec = PatternFill("solid", fgColor=LIGHT)
fill_in = PatternFill("solid", fgColor=YELLOW)
fill_kpi = PatternFill("solid", fgColor="E2F0EE")
fill_ok = PatternFill("solid", fgColor="D4EDDA")
fill_warn = PatternFill("solid", fgColor="FFF3CD")
fill_bad = PatternFill("solid", fgColor="F8D7DA")
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
top_line = Border(top=Side(style="thin", color="000000"))

USD = i18n.money('$#,##0;($#,##0);"-"')
NUM = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%;(0.0%);"-"'
MULT = '0.00"x";(0.00"x");"-"'
SC = '0;(0);"-"'

wb = Workbook()
NAMES = {}


def q(sheet):
    return f"'{sheet}'!"


def define(name, ws, cell):
    col = "".join(c for c in cell if c.isalpha())
    row = "".join(c for c in cell if c.isdigit())
    wb.defined_names[name] = DefinedName(name, attr_text=f"'{ws.title}'!${col}${row}")
    NAMES[name] = (ws.title, f"{col}{row}")


def bar(ws, row, text, c1, c2):
    ws.cell(row=row, column=c1, value=text).font = f_h1
    for c in range(c1, c2 + 1):
        ws.cell(row=row, column=c).fill = fill_h1


def style_in(c, fmt):
    c.font = f_input
    c.fill = fill_in
    c.number_format = fmt
    c.border = box


def style_calc(c, fmt, bold=False, link=False):
    c.font = f_link if link else (f_bold if bold else f_txt)
    c.number_format = fmt
    c.border = box


def header_row(ws, row, headers, start_col=1, height=42):
    for j, h in enumerate(headers, start=start_col):
        c = ws.cell(row=row, column=j, value=h)
        c.font = f_h2
        c.fill = fill_sec
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = box
    ws.row_dimensions[row].height = height


# ====================================================================== Start Here
ws0 = wb.active
ws0.title = "Start Here"
ws0.sheet_view.showGridLines = False
ws0.column_dimensions["A"].width = 3
ws0.column_dimensions["B"].width = 125
guide = [
    ("Energy Access Fund Manager Model - RBF & Portfolio Edition", f_title),
    ("From funding to impact  |  Screen, score and allocate RBF and grant funding across an energy-access project pipeline", f_h2),
    ("", None),
    ("THE QUESTION THIS MODEL ANSWERS", f_h2),
    ("Which projects should the fund support, with how much RBF and grant, and what portfolio of connections, impact, leverage and risk does that buy?", f_txt),
    ("", None),
    ("WORKFLOW", f_h2),
    ("1. Fund Parameters    - envelope, costs, fund profile (RBF rates, grant share, caps, tranches), eligibility rules, scoring weights, limits.", f_txt),
    ("2. Pipeline           - one row per applicant project. Outputs of the Developer Edition (CAPEX, viability gap, CO2) can be pasted here.", f_txt),
    ("3. Eligibility & Scoring - eligibility tests, maximum support, request, cost-effectiveness, leverage, additionality and weighted score.", f_txt),
    ("4. Allocation         - projects funded in rank order until the envelope is used, within project and country concentration limits.", f_txt),
    ("5. Disbursements      - grant at commissioning, RBF by tranche as connections are verified, adjusted for expected delivery by risk rating.", f_txt),
    ("6. MRV Tracker        - verified connections to date against targets, RBF earned and outstanding, status per project.", f_txt),
    ("7. Portfolio Dashboard - commitments, disbursements, connections, people, CO2, leverage, cost per connection, concentration and risk.", f_txt),
    ("8. Checks             - integrity checks (all should read OK).", f_txt),
    ("", None),
    ("COLOUR LEGEND", f_h2),
    ("Blue text on yellow = input   |   Black = formula (do not overwrite)   |   Green = link from another sheet", f_txt),
    ("", None),
    ("METHOD AND SIMPLIFICATIONS", f_h2),
    ("- Maximum support per project = RBF (connections x rate by customer type) + CAPEX grant, capped at a share of CAPEX, an amount per project and a share of the envelope.", f_txt),
    ("- Eligibility is pass/fail on each active criterion. Only eligible projects are scored, ranked and funded.", f_txt),
    ("- Scores (0-100) are relative to the best eligible project for cost-effectiveness, leverage, productive use and CO2; absolute for readiness, track record and risk.", f_txt),
    ("- Additionality: a request at or below the project's viability gap (+ tolerance) scores 100; above it scores 0; no viability-gap data scores 50.", f_txt),
    ("- Allocation is greedy by rank. With partial funding off, a project that does not fit is skipped and the next one is tested.", f_txt),
    ("- Disbursements: annual time step. Connections are verified over three years from commissioning; RBF is paid in two tranches.", f_txt),
    ("- Expected delivery by risk rating reduces RBF disbursements (connections not delivered are not paid). Grants are assumed paid in full at commissioning.", f_txt),
    ("- Impact and leverage of funded projects are attributed pro rata to the share of their request that the fund covers.", f_txt),
    ("- Pre-filled projects, countries and parameters are ILLUSTRATIVE ONLY. They do not describe any real fund, programme or project.", f_txt),
    ("", None),
    ("DISCLAIMER & LICENCE", f_h2),
    ("Portfolio screening and planning tool. It does not replace a fund's investment committee, due diligence, procurement rules or legal documentation.", f_note),
    ("Not investment, legal or tax advice. Licence: single user / single organisation. No resale or redistribution.", f_note),
]
for i, (t, fnt) in enumerate(guide, start=2):
    c = ws0.cell(row=i, column=2, value=t)
    if fnt:
        c.font = fnt
    c.alignment = Alignment(wrap_text=True, vertical="top")

# ====================================================================== Fund Parameters
wf = wb.create_sheet("Fund Parameters")
wf.sheet_view.showGridLines = False
for j, w in enumerate([50, 15, 15, 15, 15, 15, 3, 60], start=1):
    wf.column_dimensions[get_column_letter(j)].width = w
wf["A1"] = "FUND PARAMETERS"
wf["A1"].font = f_title
wf["A2"] = "Edit yellow cells only. All values are illustrative and do not describe any real fund."
wf["A2"].font = f_note
R = [3]


def section(title, ncol=6):
    R[0] += 1
    bar(wf, R[0], title, 1, ncol)
    R[0] += 1


def inp(label, name, value, fmt, note=""):
    r = R[0]
    wf.cell(row=r, column=1, value=label).font = f_txt
    style_in(wf.cell(row=r, column=2, value=value), fmt)
    if note:
        wf.cell(row=r, column=8, value=note).font = f_note
    define(name, wf, f"B{r}")
    R[0] += 1


def calc(label, name, formula, fmt, note="", bold=False):
    r = R[0]
    wf.cell(row=r, column=1, value=label).font = f_bold if bold else f_txt
    style_calc(wf.cell(row=r, column=2, value=formula), fmt, bold)
    if note:
        wf.cell(row=r, column=8, value=note).font = f_note
    define(name, wf, f"B{r}")
    R[0] += 1


section("1. FUND")
inp("Fund name", "FundName", "Example Energy Access Fund", "@")
inp("Fund manager", "FundManager", "Example Fund Manager", "@")
inp("Currency label", "Currency", "USD", "@", "Label only. Enter every amount in this currency.")
inp("First fund year (calendar)", "FundStart", 2027, "0")
inp("Total fund size", "FundSize", 3000000, USD)
inp("Fund management & MRV costs", "MgmtPct", 0.07, PCT, "Share of fund size.")
inp("Technical assistance window", "TAPct", 0.08, PCT, "Share of fund size, not allocated to projects.")
calc("Funds available for project allocation", "Available", "=FundSize*(1-MgmtPct-TAPct)", USD, bold=True)
inp("Over-commitment ratio", "Overcommit", 1.00, MULT, "Commit above available funds to offset expected under-delivery of connections.")
calc("Allocation envelope (commitment limit)", "Envelope", "=Available*Overcommit", USD, bold=True)
inp("Allow partial funding of the marginal project? (1 = yes)", "AllowPartial", 1, "0")
inp("Maximum share of the envelope per project", "MaxProjShare", 0.15, PCT)
inp("Maximum share of the envelope per country", "MaxCountryShare", 0.50, PCT)
inp("Additionality tolerance above the viability gap", "VGFTol", 0.10, PCT, "A request up to viability gap x (1 + tolerance) counts as additional.")
inp("Average household size", "HHSize", 5, NUM1)

section("2. FUND PROFILE (support rules)")
r = R[0]
wf.cell(row=r, column=1, value="Active profile").font = f_bold
c = wf.cell(row=r, column=2, value="Capex grant + RBF")
style_in(c, "@")
define("ProfileName", wf, f"B{r}")
profiles = ["Per-connection RBF", "Capex grant + RBF", "Productive-use focus", "Custom"]
dvp = DataValidation(type="list", formula1='"' + ",".join(T(p) for p in profiles) + '"', allow_blank=False)
wf.add_data_validation(dvp)
dvp.add(f"B{r}")
wf.cell(row=r, column=8, value="Generic profiles. Configure 'Custom' to mirror a specific programme's published rules.").font = f_note
R[0] += 2
header_row(wf, R[0], ["Rule", "Active"] + profiles)
PH = R[0]
R[0] += 1
rules = [
    ("RBF per household connection", "RBF_HH", USD, [150, 100, 100, 150]),
    ("RBF per productive-use connection", "RBF_PU", USD, [400, 300, 600, 400]),
    ("RBF per commercial connection", "RBF_COM", USD, [250, 200, 250, 250]),
    ("RBF per institution connection", "RBF_INST", USD, [300, 250, 300, 300]),
    ("CAPEX grant (share of project CAPEX)", "GrantPct", PCT, [0.0, 0.25, 0.10, 0.0]),
    ("Maximum public support (share of CAPEX, all sources)", "MaxSupportPct", PCT, [0.50, 0.60, 0.55, 0.50]),
    ("Maximum support per project", "MaxPerProject", USD, [600000, 750000, 700000, 600000]),
    ("RBF tranche paid at verification", "TrancheA", PCT, [0.80, 0.70, 0.70, 0.80]),
    ("RBF verification lag (years)", "VerifLag", "0", [0, 0, 0, 0]),
]
for lab, nm, fmt, vals in rules:
    r = R[0]
    wf.cell(row=r, column=1, value=lab).font = f_txt
    for j, v in enumerate(vals, start=3):
        style_in(wf.cell(row=r, column=j, value=v), fmt)
    style_calc(wf.cell(row=r, column=2, value=f"=INDEX(C{r}:F{r},1,MATCH(ProfileName,$C${PH}:$F${PH},0))"), fmt, True)
    define(nm, wf, f"B{r}")
    R[0] += 1
wf.cell(row=R[0], column=1, value="The remaining RBF tranche (1 - tranche at verification) is paid one year later, after a service-continuity check.").font = f_note
R[0] += 1
inp("Connections verified in commissioning year (share of target)", "RampV1", 0.60, PCT)
inp("Connections verified by end of the following year (cumulative)", "RampV2", 0.90, PCT, "The rest is verified in the third year.")

section("3. ELIGIBILITY CRITERIA (1 = apply)")
header_row(wf, R[0], ["Criterion", "Threshold", "Apply?"], height=28)
R[0] += 1
criteria = [
    ("Minimum number of connections", "E_MinConn", 200, NUM),
    ("Maximum CAPEX per connection", "E_MaxCapexConn", 2000, USD),
    ("Minimum renewable share of generation", "E_MinRE", 0.60, PCT),
    ("Minimum private co-finance (equity + debt) / CAPEX", "E_MinPrivate", 0.20, PCT),
    ("Minimum readiness stage (1-5)", "E_MinReady", 3, "0"),
    ("Maximum average tariff per kWh (affordability)", "E_MaxTariff", 0.60, '0.000'),
    ("Minimum productive-use share of connections", "E_MinPU", 0.04, PCT),
    ("Country must be listed as eligible (table below)", "E_Country", 1, "0"),
]
CRIT = []
for lab, nm, v, fmt in criteria:
    r = R[0]
    wf.cell(row=r, column=1, value=lab).font = f_txt
    if nm == "E_Country":
        wf.cell(row=r, column=2, value="-").font = f_note
    else:
        style_in(wf.cell(row=r, column=2, value=v), fmt)
        define(nm, wf, f"B{r}")
    style_in(wf.cell(row=r, column=3, value=1), "0")
    define(nm + "_On", wf, f"C{r}")
    CRIT.append((lab, nm))
    R[0] += 1

section("4. ELIGIBLE COUNTRIES")
header_row(wf, R[0], ["Country", "Eligible? (Y/N)"], height=28)
R[0] += 1
COUNTRY_FIRST = R[0]
countries = [("Country A", "Y"), ("Country B", "Y"), ("Country C", "N"), ("Country D", "Y"), ("", ""), ("", ""), ("", ""), ("", "")]
for name, el in countries:
    r = R[0]
    c = wf.cell(row=r, column=1, value=name if name else None)
    c.font = f_input
    c.fill = fill_in
    style_in(wf.cell(row=r, column=2, value=el if el else None), "@")
    R[0] += 1
COUNTRY_LAST = R[0] - 1
CTRY_NAMES = f"{q(wf.title)}$A${COUNTRY_FIRST}:$A${COUNTRY_LAST}"
CTRY_ELIG = f"{q(wf.title)}$B${COUNTRY_FIRST}:$B${COUNTRY_LAST}"
dvy = DataValidation(type="list", formula1='"' + T("Y") + "," + T("N") + '"')
wf.add_data_validation(dvy)
dvy.add(f"B{COUNTRY_FIRST}:B{COUNTRY_LAST}")

section("5. SCORING WEIGHTS (must total 100%)")
header_row(wf, R[0], ["Criterion", "Weight"], height=28)
R[0] += 1
WFIRST = R[0]
weights = [
    ("Cost-effectiveness (fund support per connection, lower is better)", "W_Cost", 0.25),
    ("Leverage (private capital per $ of fund support)", "W_Lev", 0.15),
    ("Productive-use share of connections", "W_PU", 0.15),
    ("Climate (lifetime CO2 avoided per $ of fund support)", "W_CO2", 0.10),
    ("Readiness stage", "W_Ready", 0.10),
    ("Developer track record", "W_Track", 0.10),
    ("Risk rating (lower risk is better)", "W_Risk", 0.05),
    ("Additionality (request within viability gap)", "W_Add", 0.10),
]
for lab, nm, v in weights:
    r = R[0]
    wf.cell(row=r, column=1, value=lab).font = f_txt
    style_in(wf.cell(row=r, column=2, value=v), PCT)
    define(nm, wf, f"B{r}")
    R[0] += 1
calc("Total weights", "W_Total", f"=SUM(B{WFIRST}:B{R[0]-1})", PCT, bold=True)

section("6. EXPECTED DELIVERY BY RISK RATING")
header_row(wf, R[0], ["Risk rating", "Expected share of target connections delivered"], height=42)
R[0] += 1
DFIRST = R[0]
for k, v in enumerate([1.00, 0.95, 0.90, 0.80, 0.70], start=1):
    wf.cell(row=R[0], column=1, value=k).font = f_txt
    style_in(wf.cell(row=R[0], column=2, value=v), PCT)
    R[0] += 1
DELIV = f"{q(wf.title)}$B${DFIRST}:$B${DFIRST+4}"
wf.cell(row=R[0], column=1, value="1 = lowest risk, 5 = highest. Calibrate on the fund's own delivery history where available.").font = f_note

dv_p = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", showErrorMessage=True, error=T("Enter a value between 0% and 100%."))
wf.add_data_validation(dv_p)
for nm in ["MgmtPct", "TAPct", "MaxProjShare", "MaxCountryShare", "RampV1", "RampV2"]:
    dv_p.add(NAMES[nm][1])
dv_b = DataValidation(type="list", formula1='"0,1"')
wf.add_data_validation(dv_b)
dv_b.add(NAMES["AllowPartial"][1])
for _, nm in CRIT:
    dv_b.add(NAMES[nm + "_On"][1])

# ====================================================================== Pipeline
wp = wb.create_sheet("Pipeline")
wp.sheet_view.showGridLines = False
PCOLS = [
    ("#", 5, "0"), ("Project", 30, "@"), ("Country", 13, "@"), ("Developer", 16, "@"), ("Technology", 13, "@"),
    ("Readiness (1-5)", 10, "0"), ("Track record (1-5)", 10, "0"), ("Risk rating (1-5)", 10, "0"), ("Commissioning (fund year)", 12, "0"),
    ("Household connections", 12, NUM), ("Productive-use connections", 12, NUM), ("Commercial connections", 12, NUM),
    ("Institution connections", 12, NUM), ("Project CAPEX", 13, USD), ("Developer equity", 13, USD), ("Debt secured", 13, USD),
    ("Other grants", 12, USD), ("Average tariff per kWh", 10, "0.000"), ("Renewable share", 10, PCT),
    ("Lifetime CO2 avoided (tCO2)", 12, NUM), ("Viability gap (from Developer model)", 14, USD), ("Amount requested (optional)", 14, USD),
]
PC = {}
for j, (h, w, fmt) in enumerate(PCOLS, start=1):
    wp.column_dimensions[get_column_letter(j)].width = w
    PC[h] = get_column_letter(j)
wp["A1"] = "PROJECT PIPELINE"
wp["A1"].font = f_title
wp["A2"] = "One row per applicant. Projects and figures are illustrative. Paste CAPEX, viability gap and CO2 from the Developer Edition where available."
wp["A2"].font = f_note
wp["A3"] = "Viability gap and amount requested are optional: leave blank if unknown. Technology is descriptive only."
wp["A3"].font = f_note
header_row(wp, FIRST - 1, [h for h, _, _ in PCOLS], height=56)
pipeline = [
    ("Project A - Lake village cluster", "Country A", "Developer 1", "Mini-grid", 4, 4, 2, 1, 900, 60, 110, 10, 1300000, 300000, 250000, 0, 0.38, 0.75, 7000, 820000, None),
    ("Project B - River towns", "Country A", "Developer 2", "Mini-grid", 3, 3, 3, 2, 600, 30, 60, 6, 950000, 200000, 150000, 0, 0.42, 0.85, 4500, 600000, None),
    ("Project C - Northern corridor", "Country B", "Developer 3", "Mini-grid", 5, 5, 1, 1, 1400, 120, 180, 14, 2000000, 500000, 500000, 100000, 0.35, 0.90, 12000, 1100000, None),
    ("Project D - Island grids", "Country B", "Developer 1", "Hybrid", 2, 4, 3, 3, 500, 40, 50, 5, 900000, 150000, 100000, 0, 0.45, 0.70, 3500, None, None),
    ("Project E - Highland villages", "Country C", "Developer 4", "Mini-grid", 4, 3, 3, 2, 700, 50, 70, 8, 1050000, 200000, 200000, 0, 0.40, 0.80, 5200, 650000, None),
    ("Project F - Market towns", "Country A", "Developer 5", "Hybrid", 4, 2, 4, 2, 800, 60, 120, 8, 1100000, 250000, 200000, 0, 0.36, 0.50, 3000, None, None),
    ("Project G - Remote valley", "Country D", "Developer 6", "Mini-grid", 3, 3, 4, 3, 300, 20, 30, 4, 900000, 150000, 50000, 0, 0.55, 0.90, 2500, 700000, None),
    ("Project H - Agro-processing hub", "Country B", "Developer 2", "Mini-grid", 4, 3, 2, 2, 650, 140, 80, 6, 1200000, 300000, 300000, 0, 0.33, 0.85, 6500, 550000, None),
    ("Project I - Fishing communities", "Country D", "Developer 7", "Mini-grid", 3, 2, 3, 2, 750, 70, 90, 7, 1150000, 200000, 150000, 50000, 0.40, 0.80, 5000, 700000, 450000),
    ("Project J - Health and schools first", "Country A", "Developer 8", "Mini-grid", 4, 4, 2, 1, 550, 25, 50, 25, 900000, 200000, 150000, 0, 0.39, 0.95, 4200, 520000, None),
    ("Project K - Peri-urban extension", "Country B", "Developer 9", "Mini-grid", 5, 4, 2, 1, 1200, 90, 160, 10, 1500000, 400000, 400000, 0, 0.32, 0.80, 8000, 450000, None),
    ("Project L - Mining belt", "Country D", "Developer 3", "Hybrid", 3, 5, 3, 2, 1000, 150, 140, 8, 1700000, 400000, 300000, 0, 0.41, 0.75, 7500, 900000, None),
    ("Project M - Small pilot", "Country A", "Developer 10", "Mini-grid", 3, 2, 4, 2, 150, 10, 20, 2, 300000, 50000, 0, 0, 0.50, 0.90, 900, None, None),
    ("Project N - Lakeside expansion", "Country B", "Developer 1", "Mini-grid", 4, 4, 2, 2, 850, 55, 100, 9, 1250000, 300000, 250000, 0, 0.37, 0.85, 6800, 750000, None),
]
for p in range(1, NP + 1):
    r = FIRST + p - 1
    wp.cell(row=r, column=1, value=p).font = f_bold
    row = pipeline[p - 1] if p <= len(pipeline) else (None,) * 21
    for j, v in enumerate(row, start=2):
        style_in(wp.cell(row=r, column=j, value=v), PCOLS[j - 1][2])
dv_t = DataValidation(type="list", formula1='"' + ",".join(T(x) for x in ["Mini-grid", "Hybrid", "Solar home systems", "Productive use", "Other"]) + '"')
wp.add_data_validation(dv_t)
dv_t.add(f"{PC['Technology']}{FIRST}:{PC['Technology']}{LAST}")
dv_15 = DataValidation(type="whole", operator="between", formula1="1", formula2="5", showErrorMessage=True, error=T("Enter a whole number from 1 to 5."))
wp.add_data_validation(dv_15)
for h in ["Readiness (1-5)", "Track record (1-5)", "Risk rating (1-5)"]:
    dv_15.add(f"{PC[h]}{FIRST}:{PC[h]}{LAST}")
dv_cod = DataValidation(type="whole", operator="between", formula1="1", formula2=str(FY - 3), showErrorMessage=True,
                        error=T(f"Commissioning must be in fund years 1 to {FY - 3} so that RBF is paid within the fund life."))
wp.add_data_validation(dv_cod)
dv_cod.add(f"{PC['Commissioning (fund year)']}{FIRST}:{PC['Commissioning (fund year)']}{LAST}")
wp.freeze_panes = f"C{FIRST}"


def P(h, r):
    return f"{q('Pipeline')}${PC[h]}{r}"


def Prng(h):
    return f"{q('Pipeline')}${PC[h]}${FIRST}:${PC[h]}${LAST}"


# ====================================================================== Eligibility & Scoring
we = wb.create_sheet("Eligibility & Scoring")
we.sheet_view.showGridLines = False
we["A1"] = "ELIGIBILITY & SCORING"
we["A1"].font = f_title
we["A2"] = "All cells are formulas. 1 = criterion met. Only eligible projects receive a score, a rank and an allocation."
we["A2"].font = f_note
ECOLS = []  # (key, header, fmt, width)


def ecol(key, header, fmt, width=11):
    ECOLS.append((key, header, fmt, width))


ecol("n", "#", "0", 5)
ecol("name", "Project", "@", 30)
ecol("conn", "Total connections", NUM)
ecol("cpc", "CAPEX per connection", USD)
ecol("priv", "Private co-finance / CAPEX", PCT)
ecol("pu", "Productive-use share", PCT)
for lab, nm in CRIT:
    ecol("t_" + nm, {"E_MinConn": "Min. connections", "E_MaxCapexConn": "Max. CAPEX / connection", "E_MinRE": "Min. renewable share",
                    "E_MinPrivate": "Min. private co-finance", "E_MinReady": "Min. readiness", "E_MaxTariff": "Max. tariff",
                    "E_MinPU": "Min. productive use", "E_Country": "Eligible country"}[nm], "0", 9)
ecol("elig", "ELIGIBLE", "0", 9)
ecol("why", "Eligibility status", "@", 24)
ecol("rbfmax", "RBF at profile rates", USD, 12)
ecol("grantmax", "CAPEX grant at profile rate", USD, 12)
ecol("cap", "Maximum support (after caps)", USD, 12)
ecol("req", "Request considered", USD, 12)
ecol("rbfshare", "RBF share of request", PCT, 10)
ecol("fpc", "Fund support per connection", USD, 11)
ecol("lev", "Leverage (private / fund)", MULT, 10)
ecol("co2", "tCO2 per $1,000 of support", '0.00', 10)
ecol("add", "Additionality check", "@", 16)
for k, h in [("s_cost", "Score: cost-effectiveness"), ("s_lev", "Score: leverage"), ("s_pu", "Score: productive use"), ("s_co2", "Score: climate"),
             ("s_ready", "Score: readiness"), ("s_track", "Score: track record"), ("s_risk", "Score: risk"), ("s_add", "Score: additionality")]:
    ecol(k, h, SC, 10)
ecol("score", "WEIGHTED SCORE", '0.0', 10)
ecol("rankkey", "Rank key", '0.000000', 10)
ecol("rank", "RANK", "0", 8)
ecol("alloc", "Allocated", USD, 12)
ecol("frac", "Share of request funded", PCT, 10)
ecol("astat", "Allocation status", "@", 18)
ecol("h_cost", "helper: 1 / support per connection", '0.000000', 10)
ecol("h_lev", "helper: leverage", '0.00', 9)
ecol("h_pu", "helper: productive share", '0.000', 9)
ecol("h_co2", "helper: CO2 per $", '0.000000', 10)
EC = {}
for j, (k, h, fmt, w) in enumerate(ECOLS, start=1):
    EC[k] = get_column_letter(j)
    we.column_dimensions[get_column_letter(j)].width = w
header_row(we, FIRST - 1, [h for _, h, _, _ in ECOLS], height=66)
bar(we, FIRST - 2, "ELIGIBILITY TESTS", 7, 6 + len(CRIT) + 2)


def E(k, r):
    return f"${EC[k]}{r}"


def Erng(k):
    return f"${EC[k]}${FIRST}:${EC[k]}${LAST}"


def Eq(k, r):
    return f"{q('Eligibility & Scoring')}${EC[k]}{r}"


def Eqrng(k):
    return f"{q('Eligibility & Scoring')}${EC[k]}${FIRST}:${EC[k]}${LAST}"


crit_formula = {
    "E_MinConn": lambda r: f"{E('conn', r)}>=E_MinConn",
    "E_MaxCapexConn": lambda r: f"{E('cpc', r)}<=E_MaxCapexConn",
    "E_MinRE": lambda r: f"{P('Renewable share', r)}>=E_MinRE",
    "E_MinPrivate": lambda r: f"{E('priv', r)}>=E_MinPrivate",
    "E_MinReady": lambda r: f"{P('Readiness (1-5)', r)}>=E_MinReady",
    "E_MaxTariff": lambda r: f"{P('Average tariff per kWh', r)}<=E_MaxTariff",
    "E_MinPU": lambda r: f"{E('pu', r)}>=E_MinPU",
    "E_Country": lambda r: f'IFERROR(INDEX({CTRY_ELIG},MATCH({P("Country", r)},{CTRY_NAMES},0))="Y",FALSE)',
}
crit_reason = {"E_MinConn": "Too few connections", "E_MaxCapexConn": "CAPEX per connection too high", "E_MinRE": "Renewable share too low",
               "E_MinPrivate": "Private co-finance too low", "E_MinReady": "Not ready enough", "E_MaxTariff": "Tariff above cap",
               "E_MinPU": "Productive use too low", "E_Country": "Country not eligible"}

for p in range(1, NP + 1):
    r = FIRST + p - 1
    has = f'{P("Project", r)}<>""'
    F = {}
    F["n"] = f"={p}"
    F["name"] = f'=IF({has},{P("Project", r)},"")'
    F["conn"] = f"=SUM({P('Household connections', r)}:{P('Institution connections', r)})".replace(f"{q('Pipeline')}${PC['Institution connections']}",
                                                                                               f"${PC['Institution connections']}")
    F["cpc"] = f"=IFERROR({P('Project CAPEX', r)}/{E('conn', r)},0)"
    F["priv"] = f"=IFERROR(({P('Developer equity', r)}+{P('Debt secured', r)})/{P('Project CAPEX', r)},0)"
    F["pu"] = f"=IFERROR({P('Productive-use connections', r)}/{E('conn', r)},0)"
    for _, nm in CRIT:
        F["t_" + nm] = f"=IF(NOT({has}),0,IF({nm}_On=1,IF({crit_formula[nm](r)},1,0),1))"
    tests = [E("t_" + nm, r) for _, nm in CRIT]
    F["elig"] = f"=IF(AND({has},{'*'.join(tests)}=1),1,0)"
    why = '""'
    for _, nm in reversed(CRIT):
        why = f'IF({E("t_" + nm, r)}=0,"{crit_reason[nm]}",{why})'
    F["why"] = f'=IF(NOT({has}),"",IF({E("elig", r)}=1,"Eligible",{why}))'
    F["rbfmax"] = (f"={P('Household connections', r)}*RBF_HH+{P('Productive-use connections', r)}*RBF_PU"
                   f"+{P('Commercial connections', r)}*RBF_COM+{P('Institution connections', r)}*RBF_INST")
    F["grantmax"] = f"={P('Project CAPEX', r)}*GrantPct"
    F["cap"] = (f"=MAX(0,MIN({E('rbfmax', r)}+{E('grantmax', r)},MaxSupportPct*{P('Project CAPEX', r)}-{P('Other grants', r)},"
                f"MaxPerProject,MaxProjShare*Envelope))")
    F["req"] = f"=IF({E('elig', r)}=1,IF({P('Amount requested (optional)', r)}>0,MIN({P('Amount requested (optional)', r)},{E('cap', r)}),{E('cap', r)}),0)"
    F["rbfshare"] = f"=IFERROR({E('rbfmax', r)}/({E('rbfmax', r)}+{E('grantmax', r)}),1)"
    F["fpc"] = f"=IFERROR({E('req', r)}/{E('conn', r)},0)"
    F["lev"] = f"=IFERROR(({P('Developer equity', r)}+{P('Debt secured', r)})/{E('req', r)},0)"
    F["co2"] = f"=IFERROR({P('Lifetime CO2 avoided (tCO2)', r)}/{E('req', r)}*1000,0)"
    vg = P("Viability gap (from Developer model)", r)
    F["add"] = f'=IF({E("elig", r)}=0,"",IF(NOT(ISNUMBER({vg})),"No viability-gap data",IF({vg}<=0,"No viability-gap data",IF({E("req", r)}<={vg}*(1+VGFTol),"Within viability gap","Above viability gap"))))'
    el = E("elig", r)
    F["h_cost"] = f"=IF(AND({el}=1,{E('fpc', r)}>0),1/{E('fpc', r)},0)"
    F["h_lev"] = f"=IF({el}=1,{E('lev', r)},0)"
    F["h_pu"] = f"=IF({el}=1,{E('pu', r)},0)"
    F["h_co2"] = f"=IF(AND({el}=1,{E('req', r)}>0),{P('Lifetime CO2 avoided (tCO2)', r)}/{E('req', r)},0)"
    F["s_cost"] = f"=IF({el}=1,IFERROR({E('h_cost', r)}/MAX({Erng('h_cost')})*100,0),0)"
    F["s_lev"] = f"=IF({el}=1,IFERROR({E('h_lev', r)}/MAX({Erng('h_lev')})*100,0),0)"
    F["s_pu"] = f"=IF({el}=1,IFERROR({E('h_pu', r)}/MAX({Erng('h_pu')})*100,0),0)"
    F["s_co2"] = f"=IF({el}=1,IFERROR({E('h_co2', r)}/MAX({Erng('h_co2')})*100,0),0)"
    F["s_ready"] = f"=IF({el}=1,{P('Readiness (1-5)', r)}/5*100,0)"
    F["s_track"] = f"=IF({el}=1,{P('Track record (1-5)', r)}/5*100,0)"
    F["s_risk"] = f"=IF({el}=1,(6-{P('Risk rating (1-5)', r)})/5*100,0)"
    F["s_add"] = f'=IF({el}=1,IF({E("add", r)}="Within viability gap",100,IF({E("add", r)}="Above viability gap",0,50)),0)'
    F["score"] = (f"={E('s_cost', r)}*W_Cost+{E('s_lev', r)}*W_Lev+{E('s_pu', r)}*W_PU+{E('s_co2', r)}*W_CO2"
                  f"+{E('s_ready', r)}*W_Ready+{E('s_track', r)}*W_Track+{E('s_risk', r)}*W_Risk+{E('s_add', r)}*W_Add")
    F["rankkey"] = f"=IF({el}=1,{E('score', r)}+({NP + 1}-{E('n', r)})/1000000,-1)"
    F["rank"] = f'=IF({el}=1,COUNTIF({Erng("rankkey")},">"&{E("rankkey", r)})+1,"")'
    F["alloc"] = "=0"  # set after Allocation sheet exists
    F["frac"] = f"=IFERROR({E('alloc', r)}/{E('req', r)},0)"
    F["astat"] = f'=IF({el}=0,"",IF({E("frac", r)}>=0.999,"Funded",IF({E("alloc", r)}>0,"Partially funded","Not funded")))'
    for k, h, fmt, w in ECOLS:
        c = we[f"{EC[k]}{r}"]
        c.value = F[k]
        c.number_format = fmt
        c.border = box
        c.font = f_bold if k in ("elig", "score", "rank", "alloc") else (f_link if k == "name" else f_txt)
        if k.startswith("h_"):
            c.font = f_note
we.conditional_formatting.add(f"{EC['t_E_MinConn']}{FIRST}:{EC['elig']}{LAST}",
                              FormulaRule(formula=[f'AND({EC["t_E_MinConn"]}{FIRST}=0,${EC["name"]}{FIRST}<>"")'], fill=fill_bad))
we.conditional_formatting.add(f"{EC['elig']}{FIRST}:{EC['elig']}{LAST}", FormulaRule(formula=[f"{EC['elig']}{FIRST}=1"], fill=fill_ok))
we.conditional_formatting.add(f"{EC['add']}{FIRST}:{EC['add']}{LAST}", FormulaRule(formula=[f'{EC["add"]}{FIRST}="Above viability gap"'], fill=fill_bad))
we.conditional_formatting.add(f"{EC['astat']}{FIRST}:{EC['astat']}{LAST}", FormulaRule(formula=[f'{EC["astat"]}{FIRST}="Funded"'], fill=fill_ok))
we.conditional_formatting.add(f"{EC['astat']}{FIRST}:{EC['astat']}{LAST}", FormulaRule(formula=[f'{EC["astat"]}{FIRST}="Partially funded"'], fill=fill_warn))
we.freeze_panes = f"C{FIRST}"
for k in ("h_cost", "h_lev", "h_pu", "h_co2", "rankkey"):
    we.column_dimensions[EC[k]].hidden = True

# ====================================================================== Allocation
wa = wb.create_sheet("Allocation")
wa.sheet_view.showGridLines = False
for j, w in enumerate([7, 7, 32, 14, 10, 14, 14, 14, 14, 18, 24], start=1):
    wa.column_dimensions[get_column_letter(j)].width = w
wa["A1"] = "ALLOCATION (in rank order)"
wa["A1"].font = f_title
wa["A2"] = ('="Envelope: "&Currency&" "&TEXT(Envelope,"#,##0")&"  |  Partial funding: "&IF(AllowPartial=1,"allowed","not allowed")'
            '&"  |  Max per country: "&TEXT(MaxCountryShare,"0%")&" of envelope"')
wa["A2"].font = f_h2
wa["A3"] = "Each row only looks at the rows above it: the envelope and country limits are applied in rank order, without circular references."
wa["A3"].font = f_note
header_row(wa, FIRST - 1, ["Rank", "#", "Project", "Country", "Score", "Request", "Envelope remaining before", "Country room remaining",
                           "ALLOCATED", "Status", "Binding constraint"], height=42)
for k in range(1, NP + 1):
    r = FIRST + k - 1
    F = {
        "A": f"={k}",
        "B": f'=IFERROR(MATCH({k},{Eqrng("rank")},0),"")',
        "C": f'=IF(B{r}="","",INDEX({Eqrng("name")},B{r}))',
        "D": f'=IF(B{r}="","",INDEX({Prng("Country")},B{r}))',
        "E": f'=IF(B{r}="",0,INDEX({Eqrng("score")},B{r}))',
        "F": f'=IF(B{r}="",0,INDEX({Eqrng("req")},B{r}))',
        "G": f'=IF(B{r}="","",Envelope)' if k == 1 else f'=IF(B{r}="","",Envelope-SUM($I${FIRST}:I{r-1}))',
        "H": f'=IF(B{r}="","",MaxCountryShare*Envelope)' if k == 1 else f'=IF(B{r}="","",MaxCountryShare*Envelope-SUMIF($D${FIRST}:D{r-1},D{r},$I${FIRST}:I{r-1}))',

        "I": f"=IF(B{r}=\"\",0,IF(AllowPartial=1,MAX(0,MIN(F{r},G{r},H{r})),IF(F{r}<=MIN(G{r},H{r}),F{r},0)))",
        "J": f'=IF(B{r}="","",IF(I{r}>=F{r}-0.5,"Funded",IF(I{r}>0,"Partially funded","Not funded")))',
        "K": f'=IF(OR(B{r}="",I{r}>=F{r}-0.5),"",IF(H{r}<G{r},"Country limit","Envelope exhausted"))',
    }
    fmts = {"A": "0", "B": "0", "C": "@", "D": "@", "E": "0.0", "F": USD, "G": USD, "H": USD, "I": USD, "J": "@", "K": "@"}
    for col, f in F.items():
        c = wa[f"{col}{r}"]
        c.value = f
        c.number_format = fmts[col]
        c.border = box
        c.font = f_bold if col == "I" else (f_link if col in "CDEF" else f_txt)
tr = LAST + 1
wa[f"C{tr}"] = "TOTAL"
wa[f"F{tr}"] = f"=SUM(F{FIRST}:F{LAST})"
wa[f"I{tr}"] = f"=SUM(I{FIRST}:I{LAST})"
for cc in (f"C{tr}", f"F{tr}", f"I{tr}"):
    wa[cc].font = f_bold
    wa[cc].border = top_line
wa[f"F{tr}"].number_format = USD
wa[f"I{tr}"].number_format = USD
define("TotalRequested", wa, f"F{tr}")
define("TotalAllocated", wa, f"I{tr}")
wa.conditional_formatting.add(f"J{FIRST}:J{LAST}", FormulaRule(formula=[f'J{FIRST}="Funded"'], fill=fill_ok))
wa.conditional_formatting.add(f"J{FIRST}:J{LAST}", FormulaRule(formula=[f'J{FIRST}="Partially funded"'], fill=fill_warn))
wa.conditional_formatting.add(f"J{FIRST}:J{LAST}", FormulaRule(formula=[f'J{FIRST}="Not funded"'], fill=fill_bad))
wa.freeze_panes = f"D{FIRST}"
ALLOC_IDX = f"{q('Allocation')}$B${FIRST}:$B${LAST}"
ALLOC_AMT = f"{q('Allocation')}$I${FIRST}:$I${LAST}"
for p in range(1, NP + 1):
    r = FIRST + p - 1
    we[f"{EC['alloc']}{r}"].value = f"=SUMIF({ALLOC_IDX},{p},{ALLOC_AMT})"
    we[f"{EC['alloc']}{r}"].font = f_link

# ====================================================================== Disbursements
wdb = wb.create_sheet("Disbursements")
wdb.sheet_view.showGridLines = False
wdb.column_dimensions["A"].width = 5
wdb.column_dimensions["B"].width = 30
for j in range(3, 7):
    wdb.column_dimensions[get_column_letter(j)].width = 12
YC = 7  # first fund-year column
for t in range(FY + 1):
    wdb.column_dimensions[get_column_letter(YC + t)].width = 11
wdb["A1"] = "DISBURSEMENTS (expected, by fund year)"
wdb["A1"].font = f_title
wdb["A2"] = "Grant: paid at commissioning. RBF: paid as connections are verified (tranche at verification, balance one year later), scaled by expected delivery."
wdb["A2"].font = f_note


def Y(t):
    return get_column_letter(YC + t - 1)


def share(expr, cod):
    return f"IF({expr}={cod},RampV1,IF({expr}={cod}+1,RampV2-RampV1,IF({expr}={cod}+2,1-RampV2,0)))"


def block(title, top, kind):
    bar(wdb, top, title, 1, YC + FY)
    hdr = ["#", "Project", "Allocated RBF", "Allocated grant", "Expected delivery", "Expected total"] + \
          [f"=FundStart-1+{t}" for t in range(1, FY + 1)] + ["Total"]
    for j, h in enumerate(hdr, start=1):
        c = wdb.cell(row=top + 1, column=j, value=h)
        c.font = f_h2
        c.fill = fill_sec
        c.border = box
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        if j > 6 and j < YC + FY:
            c.number_format = "0"
    wdb.row_dimensions[top + 1].height = 30
    first = top + 2
    for p in range(1, NP + 1):
        r = first + p - 1
        er = FIRST + p - 1
        cod = P("Commissioning (fund year)", er)
        wdb.cell(row=r, column=1, value=p).font = f_txt
        wdb.cell(row=r, column=2, value=f"={Eq('name', er)}").font = f_link
        style_calc(wdb.cell(row=r, column=3, value=f"={Eq('alloc', er)}*{Eq('rbfshare', er)}"), USD)
        style_calc(wdb.cell(row=r, column=4, value=f"={Eq('alloc', er)}-C{r}"), USD)
        style_calc(wdb.cell(row=r, column=5, value=f"=IF(C{r}+D{r}=0,0,IFERROR(INDEX({DELIV},{P('Risk rating (1-5)', er)}),1))"), PCT)
        tot = {"rbf": f"=C{r}*E{r}", "grant": f"=D{r}", "all": f"=C{r}*E{r}+D{r}"}[kind]
        style_calc(wdb.cell(row=r, column=6, value=tot), USD)
        for t in range(1, FY + 1):
            col = Y(t)
            if kind == "rbf":
                f = f"=$C{r}*$E{r}*(TrancheA*{share(f'{t}-VerifLag', cod)}+(1-TrancheA)*{share(f'{t}-VerifLag-1', cod)})"
            elif kind == "grant":
                f = f"=IF({t}={cod},$D{r},0)"
            else:
                f = f"={col}{r - 2 * (NP + 4)}+{col}{r - (NP + 4)}"
            c = wdb[f"{col}{r}"]
            c.value = f
            c.number_format = USD
            c.font = f_txt
        tc = wdb.cell(row=r, column=YC + FY, value=f"=SUM({Y(1)}{r}:{Y(FY)}{r})")
        tc.number_format = USD
        tc.font = f_bold
    tr_ = first + NP
    wdb.cell(row=tr_, column=2, value="TOTAL").font = f_bold
    for col in range(3, YC + FY + 1):
        if col == 5:
            continue
        L_ = get_column_letter(col)
        c = wdb.cell(row=tr_, column=col, value=f"=SUM({L_}{first}:{L_}{first+NP-1})")
        c.number_format = USD
        c.font = f_bold
        c.border = top_line
    return first, tr_


b1_first, b1_tot = block("RBF DISBURSEMENTS", 4, "rbf")
b2_first, b2_tot = block("GRANT DISBURSEMENTS", 4 + NP + 4, "grant")
b3_first, b3_tot = block("TOTAL DISBURSEMENTS", 4 + 2 * (NP + 4), "all")
sm = b3_tot + 3
bar(wdb, sm, "FUND CASH POSITION", 1, YC + FY)
rows_sm = [
    ("Expected disbursements", lambda t: f"={Y(t)}{b3_tot}"),
    ("Cumulative disbursements", lambda t: f"={Y(t)}{sm+1}" if t == 1 else f"={Y(t-1)}{sm+2}+{Y(t)}{sm+1}"),
    ("Funds available for projects, remaining", lambda t: f"=Available-{Y(t)}{sm+2}"),
    ("Undisbursed commitments", lambda t: f"=TotalAllocated-{Y(t)}{sm+2}"),
]
for k, (lab, fn) in enumerate(rows_sm, start=1):
    rr = sm + k
    wdb.cell(row=rr, column=2, value=lab).font = f_bold if k == 3 else f_txt
    for t in range(1, FY + 1):
        c = wdb[f"{Y(t)}{rr}"]
        c.value = fn(t)
        c.number_format = USD
        c.font = f_bold if k == 3 else f_txt
wdb.cell(row=sm + 5, column=2, value="Expected decommitment (RBF not earned)").font = f_txt
c = wdb.cell(row=sm + 5, column=3, value=f"=SUM(C{b1_first}:C{b1_first+NP-1})-{get_column_letter(YC+FY)}{b1_tot}")
c.number_format = USD
c.font = f_bold
define("ExpectedDecommit", wdb, f"C{sm+5}")
wdb.cell(row=sm + 6, column=2, value="Lowest remaining balance over fund life").font = f_txt
c = wdb.cell(row=sm + 6, column=3, value=f"=MIN({Y(1)}{sm+3}:{Y(FY)}{sm+3})")
c.number_format = USD
c.font = f_bold
define("MinCashBalance", wdb, f"C{sm+6}")
define("TotalExpectedDisb", wdb, f"{get_column_letter(YC+FY)}{b3_tot}")
wdb.conditional_formatting.add(f"{Y(1)}{sm+3}:{Y(FY)}{sm+3}", FormulaRule(formula=[f"{Y(1)}{sm+3}<0"], fill=fill_bad))
DISB_YEARS_ROW = b3_first - 1
DISB_RBF_ROW, DISB_GRANT_ROW, DISB_CUM_ROW = b1_tot, b2_tot, sm + 2
wdb.freeze_panes = f"C{b1_first}"

# ====================================================================== MRV Tracker
wm = wb.create_sheet("MRV Tracker")
wm.sheet_view.showGridLines = False
for j, w in enumerate([5, 30, 12, 13, 14, 12, 12, 12, 16, 14, 14, 14], start=1):
    wm.column_dimensions[get_column_letter(j)].width = w
wm["A1"] = "MRV TRACKER"
wm["A1"].font = f_title
wm["A2"] = "Enter verified connections and RBF paid to date (yellow). Status compares progress with the expected verification profile."
wm["A2"].font = f_note
wm["A4"] = "Reporting fund year"
wm["A4"].font = f_bold
style_in(wm["D4"], "0")
wm["D4"] = 3
define("RepYear", wm, "D4")
wm["E4"] = '="= calendar year "&(FundStart-1+RepYear)'
wm["E4"].font = f_note
header_row(wm, FIRST - 1, ["#", "Project", "Target connections", "Allocated RBF", "Verified connections to date", "Achieved", "Expected by now",
                           "Status", "RBF earned to date (all tranches)", "RBF paid to date", "Outstanding RBF"], height=56)
# illustrative progress (share of target connections verified) for projects likely to be funded
progress = {1: 0.97, 2: 0.70, 3: 0.80, 8: 0.85, 9: 0.40, 11: 1.0, 12: 0.75, 14: 0.88}
verified_example = [round(progress.get(i + 1, 0) * sum(pipeline[i][8:12])) for i in range(len(pipeline))]
paid_example = [None] * len(pipeline)
for p in range(1, NP + 1):
    r = FIRST + p - 1
    cod = P("Commissioning (fund year)", r)
    vals = {
        "A": p,
        "B": f"={Eq('name', r)}",
        "C": f"={Eq('conn', r)}",
        "D": f"={q('Disbursements')}$C${b1_first + p - 1}",
        "E": verified_example[p - 1] if p <= len(verified_example) else None,
        "F": f"=IFERROR(MIN(1,E{r}/C{r}),0)",
        "G": f'=IF(D{r}=0,0,IF(RepYear<{cod},0,IF(RepYear={cod},RampV1,IF(RepYear={cod}+1,RampV2,1))))',
        "H": f'=IF(B{r}="","",IF(D{r}=0,"Not funded",IF(G{r}=0,"Not started",IF(F{r}>=0.9*G{r},"On track",IF(F{r}>=0.6*G{r},"Behind","Off track")))))',
        "I": f"=IFERROR(MIN(D{r},E{r}/C{r}*D{r}),0)",
        "J": paid_example[p - 1] if p <= len(paid_example) else None,
        "K": f"=MAX(0,I{r}*TrancheA-J{r})",
    }
    fm = {"A": "0", "B": "@", "C": NUM, "D": USD, "E": NUM, "F": PCT, "G": PCT, "H": "@", "I": USD, "J": USD, "K": USD}
    for col, v in vals.items():
        c = wm[f"{col}{r}"]
        c.value = v
        if col in "EJ":
            style_in(c, fm[col])
        else:
            style_calc(c, fm[col], bold=(col == "H"), link=(col in "BCD"))
tr = LAST + 1
wm[f"B{tr}"] = "TOTAL"
wm[f"B{tr}"].font = f_bold
for col in "CDEIJK":
    c = wm[f"{col}{tr}"]
    c.value = f"=SUM({col}{FIRST}:{col}{LAST})"
    c.number_format = USD if col in "DIJK" else NUM
    c.font = f_bold
    c.border = top_line
define("MRV_Verified", wm, f"E{tr}")
define("MRV_Earned", wm, f"I{tr}")
define("MRV_Paid", wm, f"J{tr}")
define("MRV_Outstanding", wm, f"K{tr}")
wm[f"B{tr+2}"] = "Outstanding RBF = RBF earned x tranche at verification - RBF paid. The balance tranche falls due after the service-continuity check."
wm[f"B{tr+2}"].font = f_note
for status, fill in [("On track", fill_ok), ("Behind", fill_warn), ("Off track", fill_bad)]:
    wm.conditional_formatting.add(f"H{FIRST}:H{LAST}", FormulaRule(formula=[f'H{FIRST}="{status}"'], fill=fill))
wm.freeze_panes = f"C{FIRST}"

# ====================================================================== Portfolio Dashboard
wd = wb.create_sheet("Portfolio Dashboard")
wd.sheet_view.showGridLines = False
for col, w in zip("ABCDEFGHIJKLMN", [2, 46, 30, 2, 46, 17, 2, 22, 14, 12, 12, 12, 12, 12]):
    wd.column_dimensions[col].width = w
wd["B1"] = '="PORTFOLIO DASHBOARD - "&FundName'
wd["B1"].font = f_title
wd["B2"] = '=FundManager&"  |  profile: "&ProfileName&"  |  fund size "&Currency&" "&TEXT(FundSize,"#,##0")&"  |  "&TEXT(FundStart,"0")&"-"&TEXT(FundStart+' + str(FY - 1) + ',"0")'
wd["B2"].font = f_h2
wd["E3"] = '="Model checks: "&ChecksOverall'
wd["E3"].font = f_h2

frac = Eqrng("frac")


def wsum(expr_rng):
    return f"SUMPRODUCT({expr_rng},{frac})"


def kpis(col, row, title, items):
    lc, vc = get_column_letter(col), get_column_letter(col + 1)
    bar(wd, row, title, col, col + 1)
    r_ = row + 1
    for lab, f, fmt, nm in items:
        a = wd[f"{lc}{r_}"]
        a.value = lab
        a.font = f_txt
        a.border = box
        b = wd[f"{vc}{r_}"]
        b.value = f
        b.number_format = fmt
        b.font = f_bold
        b.fill = fill_kpi
        b.border = box
        b.alignment = Alignment(horizontal="right")
        if nm:
            define(nm, wd, f"{vc}{r_}")
        r_ += 1
    return r_


e1 = kpis(2, 5, "COMMITMENTS", [
    ("Fund size", "=FundSize", USD, None),
    ("Available for projects (after management and TA)", "=Available", USD, None),
    ("Allocation envelope (with over-commitment)", "=Envelope", USD, None),
    ("Requested by eligible projects", "=TotalRequested", USD, None),
    ("Oversubscription (requested / envelope)", "=IFERROR(TotalRequested/Envelope,0)", MULT, None),
    ("Allocated", "=TotalAllocated", USD, None),
    ("  of which RBF", f"={q('Disbursements')}$C${b1_tot}", USD, "AllocRBF"),
    ("  of which CAPEX grants", f"={q('Disbursements')}$D${b1_tot}", USD, "AllocGrant"),
    ("Envelope used", "=IFERROR(TotalAllocated/Envelope,0)", PCT, "EnvelopeUsed"),
    ("Expected disbursements (after delivery haircut)", "=TotalExpectedDisb", USD, None),
    ("Expected decommitment (RBF not earned)", "=ExpectedDecommit", USD, None),
    ("Lowest remaining fund balance", "=MinCashBalance", USD, None),
    ("Over-commitment covered by expected under-delivery (indicative)", "=IFERROR(TotalAllocated/TotalExpectedDisb,0)", MULT, None),
])
e2 = kpis(5, 5, "PIPELINE", [
    ("Projects in pipeline", f'=COUNTIF({Prng("Project")},"?*")', "0", "NApplied"),
    ("Eligible projects", f"=SUM({Eqrng('elig')})", "0", "NEligible"),
    ("Projects funded (fully or partly)", f'=COUNTIF({ALLOC_AMT},">0")', "0", "NFunded"),
    ("Projects fully funded", f'=COUNTIF({Eqrng("astat")},"Funded")', "0", None),
    ("Eligible projects not funded", "=NEligible-NFunded", "0", None),
    ("Projects above their viability gap (funded)", f'=SUMPRODUCT(({Eqrng("add")}="Above viability gap")*({Eqrng("alloc")}>0))', "0", "NAboveVGF"),
    ("Average weighted score of funded projects", f"=IFERROR(SUMPRODUCT({Eqrng('score')},{Eqrng('alloc')})/TotalAllocated,0)", "0.0", None),
])
e3 = kpis(2, max(e1, e2) + 1, "IMPACT BOUGHT (pro rata to funding share)", [
    ("Connections funded", f"={wsum(Eqrng('conn'))}", NUM, "ConnFunded"),
    ("  household connections", f"={wsum(Prng('Household connections'))}", NUM, "HHFunded"),
    ("  productive-use connections", f"={wsum(Prng('Productive-use connections'))}", NUM, "PUFunded"),
    ("  commercial and institution connections", f"={wsum(Prng('Commercial connections'))}+{wsum(Prng('Institution connections'))}", NUM, None),
    ("People with access (households x household size)", "=HHFunded*HHSize", NUM, "PeopleFunded"),
    ("Lifetime CO2 avoided (tCO2)", f"={wsum(Prng('Lifetime CO2 avoided (tCO2)'))}", NUM, "CO2Funded"),
    ("Verified connections to date (MRV Tracker)", "=MRV_Verified", NUM, None),
])
e4 = kpis(5, max(e1, e2) + 1, "LEVERAGE & COST-EFFECTIVENESS", [
    ("Total project investment mobilised", f"={wsum(Prng('Project CAPEX'))}", USD, "InvestMobilised"),
    ("Private capital mobilised (equity + debt)", f"={wsum(Prng('Developer equity'))}+{wsum(Prng('Debt secured'))}", USD, "PrivateMobilised"),
    ("Leverage: private capital per $ allocated", "=IFERROR(PrivateMobilised/TotalAllocated,0)", MULT, None),
    ("Investment per $ allocated", "=IFERROR(InvestMobilised/TotalAllocated,0)", MULT, None),
    ("Fund allocation per connection", "=IFERROR(TotalAllocated/ConnFunded,0)", USD, None),
    ("Fund allocation per person with access", "=IFERROR(TotalAllocated/PeopleFunded,0)", USD, None),
    ("Fund allocation per tCO2 avoided", "=IFERROR(TotalAllocated/CO2Funded,0)", USD, None),
])
e5 = kpis(2, max(e3, e4) + 1, "RISK & CONCENTRATION", [
    ("Allocation-weighted risk rating (1-5)", f"=IFERROR(SUMPRODUCT({Prng('Risk rating (1-5)')},{Eqrng('alloc')})/TotalAllocated,0)", "0.00", None),
    ("Expected delivery of RBF connections", "=IFERROR((TotalExpectedDisb-AllocGrant)/AllocRBF,0)", PCT, None),
    ("Largest single project (share of allocation)", f"=IFERROR(MAX({ALLOC_AMT})/TotalAllocated,0)", PCT, "TopProjShare"),
    ("Top 3 projects (share of allocation)", f"=IFERROR((LARGE({ALLOC_AMT},1)+LARGE({ALLOC_AMT},2)+LARGE({ALLOC_AMT},3))/TotalAllocated,0)", PCT, None),
    ("Largest country (share of envelope)", "=IFERROR(MaxCountryAlloc/Envelope,0)", PCT, "TopCountryShare"),
])
vr = e5 + 1
bar(wd, vr, "PORTFOLIO VERDICT", 2, 3)
verdicts = [
    ("Envelope at least 90% committed?", '=IF(EnvelopeUsed>=0.9,"YES","NO - pipeline too thin")'),
    ("Expected disbursements within available funds?", '=IF(MinCashBalance>=0,"YES","NO - reduce over-commitment")'),
    ("Country concentration within limit?", '=IF(TopCountryShare<=MaxCountryShare+0.0001,"YES","NO - rebalance")'),
    ("All funded projects within their viability gap?", '=IF(NAboveVGF=0,"YES","NO - review additionality")'),
]
r_ = vr + 1
for lab, f in verdicts:
    wd[f"B{r_}"] = lab
    wd[f"B{r_}"].font = f_txt
    wd[f"B{r_}"].border = box
    c = wd[f"C{r_}"]
    c.value = f
    c.font = f_bold
    c.border = box
    c.alignment = Alignment(horizontal="center")
    r_ += 1
vrng = f"C{vr+1}:C{r_-1}"
wd.conditional_formatting.add(vrng, FormulaRule(formula=[f'LEFT(C{vr+1},LEN("YES"))="YES"'], fill=fill_ok, font=Font(name=FONT, bold=True, color="155724")))
wd.conditional_formatting.add(vrng, FormulaRule(formula=[f'LEFT(C{vr+1},LEN("NO - "))="NO - "'], fill=fill_bad, font=Font(name=FONT, bold=True, color="721C24")))
VEND = r_

# country table (H:J)
ct = 5
bar(wd, ct, "ALLOCATION BY COUNTRY", 8, 10)
for j, h in enumerate(["Country", "Allocated", "Share of envelope"], start=8):
    c = wd.cell(row=ct + 1, column=j, value=h)
    c.font = f_h2
    c.fill = fill_sec
for k in range(COUNTRY_LAST - COUNTRY_FIRST + 1):
    rr = ct + 2 + k
    wd[f"H{rr}"] = f'=IF({q(wf.title)}$A${COUNTRY_FIRST + k}="","",{q(wf.title)}$A${COUNTRY_FIRST + k})'
    wd[f"H{rr}"].font = f_link
    wd[f"I{rr}"] = f'=IF(H{rr}="",0,SUMIF({Prng("Country")},H{rr},{Eqrng("alloc")}))'
    wd[f"J{rr}"] = f"=IFERROR(I{rr}/Envelope,0)"
    wd[f"I{rr}"].number_format = USD
    wd[f"J{rr}"].number_format = PCT
CT_FIRST, CT_LAST = ct + 2, ct + 1 + (COUNTRY_LAST - COUNTRY_FIRST + 1)
rr = CT_LAST + 1
wd[f"H{rr}"] = "Other / unlisted"
wd[f"I{rr}"] = f"=TotalAllocated-SUM(I{CT_FIRST}:I{CT_LAST})"
wd[f"I{rr}"].number_format = USD
wd[f"J{rr}"] = f"=IFERROR(I{rr}/Envelope,0)"
wd[f"J{rr}"].number_format = PCT
define("UnlistedAlloc", wd, f"I{rr}")
wd[f"H{rr+1}"] = "Largest country allocation"
wd[f"I{rr+1}"] = f"=MAX(I{CT_FIRST}:I{rr})"
wd[f"I{rr+1}"].number_format = USD
wd[f"I{rr+1}"].font = f_bold
define("MaxCountryAlloc", wd, f"I{rr+1}")
# disbursement chart data
dd = rr + 4
wd.cell(row=dd - 1, column=8, value="Disbursement profile (linked)").font = f_h2
for j, h in enumerate(["Year", "RBF", "Grants", "Cumulative"], start=8):
    wd.cell(row=dd, column=j, value=h).font = f_h2
for t in range(1, FY + 1):
    r2 = dd + t
    wd.cell(row=r2, column=8, value=f"=FundStart-1+{t}").font = f_link
    for j, src in [(9, DISB_RBF_ROW), (10, DISB_GRANT_ROW), (11, DISB_CUM_ROW)]:
        c = wd.cell(row=r2, column=j, value=f"={q('Disbursements')}${Y(t)}${src}")
        c.number_format = NUM
        c.font = f_link

chart_top = VEND + 2
ch1 = BarChart()
ch1.type = "bar"
ch1.title = T("Allocation by project (rank order)")
ch1.add_data(Reference(wa, min_col=9, min_row=FIRST - 1, max_row=FIRST + 14), titles_from_data=True)
ch1.set_categories(Reference(wa, min_col=3, min_row=FIRST, max_row=FIRST + 14))
ch1.y_axis.number_format = "#,##0"
ch1.x_axis.scaling.orientation = "maxMin"
ch1.legend = None
ch1.height, ch1.width = 10, 15
wd.add_chart(ch1, f"B{chart_top}")
ch2 = BarChart()
ch2.type = "col"
ch2.grouping = "stacked"
ch2.overlap = 100
ch2.title = T("Expected disbursements by year")
ch2.add_data(Reference(wd, min_col=9, max_col=10, min_row=dd, max_row=dd + FY), titles_from_data=True)
ch2.set_categories(Reference(wd, min_col=8, min_row=dd + 1, max_row=dd + FY))
ln = LineChart()
ln.add_data(Reference(wd, min_col=11, min_row=dd, max_row=dd + FY), titles_from_data=True)
ln.y_axis.axId = 200
ln.y_axis.title = T("Cumulative")
ln.y_axis.crosses = "max"
ch2 += ln
ch2.height, ch2.width = 10, 15
wd.add_chart(ch2, f"E{chart_top}")
pie = PieChart()
pie.title = T("Allocation by country")
pie.add_data(Reference(wd, min_col=9, min_row=CT_FIRST, max_row=CT_LAST + 1))
pie.set_categories(Reference(wd, min_col=8, min_row=CT_FIRST, max_row=CT_LAST + 1))
pie.dataLabels = DataLabelList()
pie.dataLabels.showPercent = True
pie.dataLabels.showVal = False
pie.dataLabels.showCatName = False
pie.dataLabels.showSerName = False
pie.height, pie.width = 8, 11
wd.add_chart(pie, f"H{chart_top}")

# ====================================================================== Checks
wk = wb.create_sheet("Checks")
wk.sheet_view.showGridLines = False
wk.column_dimensions["A"].width = 84
wk.column_dimensions["B"].width = 12
wk["A1"] = "INTEGRITY CHECKS"
wk["A1"].font = f_title
checks = [
    ("Scoring weights total 100%", "=ABS(W_Total-1)<0.0001"),
    ("Allocation within envelope", "=TotalAllocated<=Envelope+0.5"),
    ("No allocation above a project's request", f"=SUMPRODUCT(({Eqrng('alloc')}>{Eqrng('req')}+0.5)*1)=0"),
    ("No allocation to ineligible projects", f"=SUMPRODUCT(({Eqrng('elig')}=0)*({Eqrng('alloc')}>0))=0"),
    ("Each eligible project ranked exactly once", f"=SUMPRODUCT(({Eqrng('elig')}=1)*1)=COUNT({ALLOC_IDX})"),
    ("Country allocations add up to total allocation", f"=ABS(SUM('Portfolio Dashboard'!$I${CT_FIRST}:$I${CT_LAST})+UnlistedAlloc-TotalAllocated)<1"),
    ("Country limit respected", "=MaxCountryAlloc<=MaxCountryShare*Envelope+0.5"),
    ("Expected disbursements by year = grants + RBF x expected delivery (all paid within the fund life)",
     f"=ABS(TotalExpectedDisb-SUM({q('Disbursements')}$F${b3_first}:$F${b3_first+NP-1}))<1"),
    ("Expected disbursements do not exceed allocations", "=TotalExpectedDisb<=TotalAllocated+0.5"),
    ("Verification profile valid (0 <= year 1 <= cumulative year 2 <= 100%)", "=AND(RampV1>=0,RampV1<=RampV2,RampV2<=1)"),
    ("Management + TA below 100%", "=MgmtPct+TAPct<1"),
    ("At least one project in pipeline", "=NApplied>0"),
]
for i, (lab, f) in enumerate(checks, start=3):
    wk[f"A{i}"] = lab
    wk[f"A{i}"].border = box
    c = wk[f"B{i}"]
    c.value = f'=IF({f[1:]},"OK","CHECK")'
    c.font = f_bold
    c.border = box
    c.alignment = Alignment(horizontal="center")
last = 2 + len(checks)
wk[f"A{last+2}"] = "OVERALL"
wk[f"A{last+2}"].font = f_bold
wk[f"B{last+2}"] = f'=IF(COUNTIF(B3:B{last},"OK")={len(checks)},"ALL OK","REVIEW")'
wk[f"B{last+2}"].font = f_bold
define("ChecksOverall", wk, f"B{last+2}")
wk.conditional_formatting.add(f"B3:B{last+2}", FormulaRule(formula=['OR(B3="OK",B3="ALL OK")'], fill=fill_ok))
wk.conditional_formatting.add(f"B3:B{last+2}", FormulaRule(formula=['OR(B3="CHECK",B3="REVIEW")'], fill=fill_bad))

# ====================================================================== order, print, save
order = [T(n) for n in ["Start Here", "Fund Parameters", "Pipeline", "Eligibility & Scoring", "Allocation", "Disbursements",
                        "MRV Tracker", "Portfolio Dashboard", "Checks"]]
wb._sheets = [wb[n] for n in order]
tabs = {"Start Here": NAVY, "Fund Parameters": "FFC000", "Pipeline": "FFC000", "MRV Tracker": "FFC000", "Portfolio Dashboard": TEAL,
        "Allocation": TEAL, "Eligibility & Scoring": "7F7F7F", "Disbursements": "7F7F7F", "Checks": "7F7F7F"}
tabs = {T(k): v for k, v in tabs.items()}
for ws in wb.worksheets:
    ws.sheet_properties.tabColor = tabs.get(ws.title, "7F7F7F")
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
wb.active = 0
print_areas.apply(wb)
wb.save(OUT)
print("saved", OUT)
i18n.report()
