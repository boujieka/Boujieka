"""Build the Energy Access Project Financial Model - Developer Edition (product 2).

Usage: python tools/build_developer_edition.py [output.xlsx]
Then recalculate (open in Excel, or LibreOffice headless) so cached values exist.

Design notes
- One cash-flow engine is written by build_engine(). The base case is the visible 'Cash Flow'
  sheet; sensitivity cases are hidden copies of the same engine with different case levers,
  which gives a live tornado without data tables or macros.
- Technical sizing is done once on base inputs. Scenario and sensitivity levers represent
  out-turn risk on a project that has already been built (demand, tariff, costs, collection).
"""
import sys
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

import i18n
import print_areas

LANG, OUT = i18n.setup(sys.argv)
T = i18n.T
if OUT is None:
    OUT = {"en": "product/02-developer-edition/EnergyAccess_Developer_Model_v1.xlsx",
           "fr": "product/02-developer-edition/Modele_Financier_Acces_Energie_Developpeur_v1_FR.xlsx"}[LANG]

MAX_YEARS = 20
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
fill_bad = PatternFill("solid", fgColor="F8D7DA")
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
top_line = Border(top=Side(style="thin", color="000000"))

USD = i18n.money('$#,##0;($#,##0);"-"')
USD2 = i18n.money('$#,##0.00;($#,##0.00);"-"')
USD3 = i18n.money('$#,##0.000;($#,##0.000);"-"')
NUM = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%;(0.0%);"-"'
MULT = '0.00"x";(0.00"x");"-"'

wb = Workbook()
NAMES = {}


def addr(cell):
    col = "".join(c for c in cell if c.isalpha())
    row = "".join(c for c in cell if c.isdigit())
    return col, row


def define(name, ws, cell):
    col, row = addr(cell)
    ref = f"'{ws.title}'!${col}${row}"
    wb.defined_names[name] = DefinedName(name, attr_text=ref)
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


def style_calc(c, fmt, bold=False):
    c.font = f_bold if bold else f_txt
    c.number_format = fmt
    c.border = box


# ====================================================================== Start Here
ws0 = wb.active
ws0.title = "Start Here"
ws0.sheet_view.showGridLines = False
ws0.column_dimensions["A"].width = 3
ws0.column_dimensions["B"].width = 120
guide = [
    ("Energy Access Project Financial Model - Developer Edition", f_title),
    ("From community demand to a bankable funding request  |  Solar PV + battery + diesel mini-grids  |  20-year annual model", f_h2),
    ("", None),
    ("THE QUESTION THIS MODEL ANSWERS", f_h2),
    ("Can this energy-access project be made bankable, and what combination of grant, RBF, concessional debt, senior debt and equity does it need?", f_txt),
    ("", None),
    ("WORKFLOW", f_h2),
    ("1. Inputs           - project, scenarios, customer segments (tariff, RBF, income), technical, CAPEX, OPEX, financing, impact.", f_txt),
    ("2. Load Profile     - hourly load shape per segment. Drives the night-time energy share (battery size) and the peak ratio (generator size).", f_txt),
    ("3. Productive Use   - appliance inventory (mills, welding, cold rooms, pumps...). Can drive productive users' consumption.", f_txt),
    ("4. Dashboard        - KPIs, bankability verdict, affordability by segment, charts.", f_txt),
    ("5. Funding Gap & RBF - viability gap, grant needed, RBF per connection needed for the project hurdle and the equity target, debt capacity.", f_txt),
    ("6. Sensitivity      - live tornado: tariff, demand, CAPEX, OPEX, collection, diesel price, interest rate.", f_txt),
    ("7. Impact & MRV     - connections, people, productive users, energy, CO2, RBF disbursements, cost-effectiveness ratios.", f_txt),
    ("8. Financing Request - auto-written project summary, sources & uses, key metrics. Copy into your concept note.", f_txt),
    ("9. Cash Flow / Checks - the engine and the integrity checks (all should read OK).", f_txt),
    ("", None),
    ("COLOUR LEGEND", f_h2),
    ("Blue text on yellow = input   |   Black = formula (do not overwrite)   |   Green = link from another sheet", f_txt),
    ("", None),
    ("METHOD AND SIMPLIFICATIONS", f_h2),
    ("- Annual time step. Construction in Year 0, operation Years 1-20. No hourly dispatch: solar delivery is capped by the target solar fraction.", f_txt),
    ("- Night-time solar energy passes through the battery: the round-trip efficiency loss is charged to PV production.", f_txt),
    ("- Sizing uses base inputs. Scenario and sensitivity levers model out-turn risk on the built system (the design does not change).", f_txt),
    ("- PV and battery capacity are fixed after Year 0. If demand keeps growing, diesel covers the difference and fuel cost rises.", f_txt),
    ("- Tax: flat rate with unlimited loss carry-forward. Grants and RBF are treated as non-taxable. Check local tax treatment.", f_txt),
    ("- Debt: senior and concessional tranches, each an annuity after interest-only grace years. DSRA funded by equity. No fees, no sculpting.", f_txt),
    ("- RBF is paid per verified new connection, by segment, with an optional verification lag. RBF is not a construction source: bridge it.", f_txt),
    ("- RBF and grant needs are solved in closed form (cash flows are linear in RBF), so no Goal Seek is required.", f_txt),
    ("- Battery replacements create negative cash-flow years, so IRR can mislead. Use NPV and the funding-gap metrics as primary decision tools.", f_txt),
    ("- Pre-filled values are ILLUSTRATIVE ONLY, not market benchmarks. Replace them with your project data, quotes and programme rules.", f_txt),
    ("", None),
    ("DISCLAIMER & LICENCE", f_h2),
    ("Screening and pre-feasibility tool for educational and planning purposes. Not investment, legal, tax or engineering advice.", f_note),
    ("Perform independent technical and financial due diligence before any investment decision. Licence: single user / single organisation. No resale.", f_note),
]
for i, (t, fnt) in enumerate(guide, start=2):
    c = ws0.cell(row=i, column=2, value=t)
    if fnt:
        c.font = fnt
    c.alignment = Alignment(wrap_text=True, vertical="top")

# ====================================================================== Inputs
wi = wb.create_sheet("Inputs")
wi.sheet_view.showGridLines = False
widths = [46, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13]
for j, w in enumerate(widths, start=1):
    wi.column_dimensions[get_column_letter(j)].width = w
wi["A1"] = "INPUTS"
wi["A1"].font = f_title
wi["A2"] = "Edit yellow cells only. Example values are illustrative, not benchmarks."
wi["A2"].font = f_note
R = [4]


def section(title, ncol=11):
    R[0] += 1
    bar(wi, R[0], title, 1, ncol)
    R[0] += 1


def inp(label, name, value, fmt, unit="", note=""):
    r = R[0]
    wi.cell(row=r, column=1, value=label).font = f_txt
    style_in(wi.cell(row=r, column=3, value=value), fmt)
    if unit:
        wi.cell(row=r, column=4, value=unit).font = f_note
    if note:
        wi.cell(row=r, column=6, value=note).font = f_note
    define(name, wi, f"C{r}")
    R[0] += 1


def calc(label, name, formula, fmt, unit="", note="", bold=False):
    r = R[0]
    wi.cell(row=r, column=1, value=label).font = f_bold if bold else f_txt
    style_calc(wi.cell(row=r, column=3, value=formula), fmt, bold)
    if unit:
        wi.cell(row=r, column=4, value=unit).font = f_note
    if note:
        wi.cell(row=r, column=6, value=note).font = f_note
    define(name, wi, f"C{r}")
    R[0] += 1


def table_header(headers, start_col=1):
    for j, h in enumerate(headers, start=start_col):
        c = wi.cell(row=R[0], column=j, value=h)
        c.font = f_h2
        c.fill = fill_sec
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    wi.row_dimensions[R[0]].height = 28
    R[0] += 1


section("1. PROJECT")
inp("Project name", "ProjectName", "Example village mini-grid", "@")
inp("Country / site", "Site", "Example site", "@")
inp("Developer / sponsor", "Sponsor", "Example Energy Ltd", "@")
inp("Currency label", "Currency", "USD", "@", note="Label only. Enter every amount in this currency.")
inp("First operating year", "StartYear", 2027, "0", "year")
inp("Project life", "Life", 20, "0", "years", f"1 to {MAX_YEARS}.")
inp("Project hurdle rate (discount rate)", "Hurdle", 0.10, PCT, "", "Used for NPV, LCOE, viability gap and RBF calibration.")
inp("Target equity IRR", "TargetEqIRR", 0.15, PCT)
inp("Minimum DSCR required by lenders", "MinDSCR", 1.30, MULT)
inp("Tariff escalation", "TariffEsc", 0.03, PCT, "per year")
inp("Cost escalation (OPEX, fuel, replacements)", "CostEsc", 0.03, PCT, "per year")
inp("Corporate tax rate", "TaxRate", 0.25, PCT)
inp("Tax depreciation period", "DepYears", 15, "0", "years", "Straight-line on total CAPEX.")

section("2. SCENARIOS (multipliers on the inputs below; 1.00 = as entered)")
r = R[0]
wi.cell(row=r, column=1, value="Active scenario").font = f_bold
c = wi.cell(row=r, column=3, value="Base")
style_in(c, "@")
define("ScenarioName", wi, f"C{r}")
dv_s = DataValidation(type="list", formula1='"' + ",".join(T(x) for x in ["Base", "Conservative", "Optimistic", "Custom"]) + '"', allow_blank=False)
wi.add_data_validation(dv_s)
dv_s.add(f"C{r}")
wi.cell(row=r, column=6, value="Select from the drop-down list.").font = f_note
R[0] += 2
table_header(["Lever", "Active", "Base", "Conservative", "Optimistic", "Custom"])
SC_HDR = R[0] - 1
levers = [
    ("Tariff", "LevTariff", [1.00, 1.00, 1.00, 1.00]),
    ("Demand (consumption per customer)", "LevDemand", [1.00, 0.85, 1.10, 1.00]),
    ("CAPEX", "LevCapex", [1.00, 1.15, 0.95, 1.00]),
    ("OPEX", "LevOpex", [1.00, 1.10, 0.95, 1.00]),
    ("Collection rate", "LevColl", [1.00, 0.95, 1.03, 1.00]),
    ("Diesel price", "LevFuel", [1.00, 1.25, 0.90, 1.00]),
]
for lab, nm, vals in levers:
    r = R[0]
    wi.cell(row=r, column=1, value=lab).font = f_txt
    for j, v in enumerate(vals, start=3):
        style_in(wi.cell(row=r, column=j, value=v), MULT)
    c = wi.cell(row=r, column=2, value=f"=INDEX(C{r}:F{r},1,MATCH(ScenarioName,$C${SC_HDR}:$F${SC_HDR},0))")
    style_calc(c, MULT, True)
    define(nm, wi, f"B{r}")
    R[0] += 1
wi.cell(row=R[0], column=1, value="Collection lever multiplies the collection rate (capped at 100%). Scenario values are illustrative.").font = f_note
R[0] += 1
inp("Sensitivity range (+/- applied to each variable)", "SensDelta", 0.20, PCT, "", "Used by the tornado on the 'Sensitivity' sheet.")

section("3. CUSTOMER SEGMENTS, TARIFFS, RBF AND AFFORDABILITY")
table_header(["Segment", "Customers", "kWh/month (entered)", "Tariff per kWh", "Connection fee",
              "RBF per new connection", "Monthly income or revenue", "kWh/month (used)", "Monthly bill (Yr 1)",
              "Bill as % of income", "Affordable?"])
segments = [
    ("Households", 800, 15, 0.40, 10, 250, 120),
    ("Productive users (mills, welding, cold rooms)", 60, 250, 0.35, 25, 400, 1500),
    ("Commercial (shops, bars, kiosks)", 100, 50, 0.40, 15, 250, 400),
    ("Institutions (health centre, school, water)", 10, 300, 0.35, 50, 300, 0),
    ("Other / custom", 0, 0, 0, 0, 0, 0),
]
NSEG = len(segments)
SEG_FIRST = R[0]
for i, (lab, n, kwh, tar, fee, rbf, inc) in enumerate(segments, start=1):
    r = R[0]
    c = wi.cell(row=r, column=1, value=lab)
    c.font = f_input
    c.fill = fill_in
    for j, (v, fmt) in enumerate([(n, NUM), (kwh, NUM1), (tar, USD3), (fee, USD), (rbf, USD), (inc, USD)], start=2):
        style_in(wi.cell(row=r, column=j, value=v), fmt)
    used = f"=IF(AND(UsePUE=1,{i}=2),PUE_kWhPerUser,C{r})" if i == 2 else f"=C{r}"
    style_calc(wi.cell(row=r, column=8, value=used), NUM1, True)
    style_calc(wi.cell(row=r, column=9, value=f"=H{r}*D{r}*LevTariff"), USD2)
    style_calc(wi.cell(row=r, column=10, value=f'=IF(G{r}>0,I{r}/G{r},"")'), PCT)
    style_calc(wi.cell(row=r, column=11, value=f'=IF(B{r}=0,"",IF(G{r}<=0,"n/a",IF(J{r}<=AffordThreshold,"YES","NO")))'), "@")
    wi.cell(row=r, column=11).alignment = Alignment(horizontal="center")
    for suf, col in [("Name", "A"), ("N", "B"), ("kWh", "H"), ("Tariff", "D"), ("Fee", "E"), ("RBF", "F"), ("Income", "G"),
                     ("Bill", "I"), ("BillPct", "J"), ("Afford", "K")]:
        define(f"Seg{i}_{suf}", wi, f"{col}{r}")
    R[0] += 1
SEG_LAST = R[0] - 1
r = R[0]
wi.cell(row=r, column=1, value="Total / weighted average").font = f_bold
wi.cell(row=r, column=2, value=f"=SUM(B{SEG_FIRST}:B{SEG_LAST})").number_format = NUM
wi.cell(row=r, column=8, value=f"=IFERROR(SUMPRODUCT(B{SEG_FIRST}:B{SEG_LAST},H{SEG_FIRST}:H{SEG_LAST})/B{r},0)").number_format = NUM1
wi.cell(row=r, column=4, value=f"=IFERROR(SUMPRODUCT(B{SEG_FIRST}:B{SEG_LAST},H{SEG_FIRST}:H{SEG_LAST},D{SEG_FIRST}:D{SEG_LAST})/SUMPRODUCT(B{SEG_FIRST}:B{SEG_LAST},H{SEG_FIRST}:H{SEG_LAST}),0)").number_format = USD3
wi.cell(row=r, column=6, value=f"=IFERROR(SUMPRODUCT(B{SEG_FIRST}:B{SEG_LAST},F{SEG_FIRST}:F{SEG_LAST})/B{r},0)").number_format = USD
for j in range(1, 12):
    wi.cell(row=r, column=j).font = f_bold
    wi.cell(row=r, column=j).border = top_line
define("TotalCustomers", wi, f"B{r}")
define("AvgTariffInput", wi, f"D{r}")
define("AvgRBFperConn", wi, f"F{r}")
R[0] += 1
wi.cell(row=R[0], column=1, value="Monthly income: household income, or business revenue for productive/commercial users. Leave 0 for institutions.").font = f_note
R[0] += 2
inp("Use 'Productive Use' sheet for productive users' kWh? (1 = yes)", "UsePUE", 1, "0", "", "1 = kWh/month of productive users comes from the appliance inventory.")
inp("Affordability threshold (max bill as % of income)", "AffordThreshold", 0.05, PCT, "", "Set to your programme's own definition. Example value only.")
inp("Connection ramp - Year 1 (% of customers connected)", "Ramp1", 0.60, PCT)
inp("Connection ramp - Year 2", "Ramp2", 0.85, PCT)
inp("Connection ramp - Year 3 onwards", "Ramp3", 1.00, PCT)
inp("Annual growth in consumption per customer", "DemandGrowth", 0.03, PCT, "per year")
inp("Collection rate (share of bills paid)", "Collection", 0.92, PCT)

section("4. TECHNICAL DESIGN & AUTO-SIZING")
inp("PV specific yield", "SpecYield", 1500, NUM, "kWh/kWp/yr", "Use PVGIS or your design study for the site.")
inp("PV degradation", "Degradation", 0.005, PCT, "per year")
inp("Distribution & conversion losses", "Losses", 0.12, PCT)
inp("Target solar fraction (max share of generation from PV)", "SolarFraction", 0.90, PCT, "", "Storage-limited cap. Diesel supplies the rest.")
inp("PV oversizing factor", "PVOversize", 1.15, MULT)
inp("Battery usable depth of discharge", "DoD", 0.80, PCT)
inp("Battery round-trip efficiency", "RTE", 0.90, PCT, "", "Energy out / energy in. Applies to the solar energy stored for night-time use.")
inp("Diesel generator efficiency", "DieselEff", 3.0, NUM1, "kWh/litre")
inp("Diesel price, Year 1", "FuelPrice", 1.20, USD2, "per litre")
calc("Night-time share of daily energy (from Load Profile)", "NightShareUsed", "=NightShare", PCT)
calc("Peak-to-average load ratio (from Load Profile)", "PeakRatioUsed", "=PeakRatio", MULT)
for rr_ in (R[0] - 2, R[0] - 1):
    wi.cell(row=rr_, column=3).font = f_link
calc("Storage loss factor on solar energy", "StorageFactor", "=1+NightShareUsed*(1/RTE-1)", "0.000", "",
     "PV must produce this much energy per kWh of solar delivered, because night-time solar passes through the battery.")
R[0] += 1
table_header(["Component", "Auto-size", "Override", "Used", "Unit"])
seg_energy = "+".join(f"Seg{i}_N*Seg{i}_kWh" for i in range(1, NSEG + 1))
r = R[0]
wi.cell(row=r, column=1, value="Design energy sold (Year 3, full connection, base inputs)").font = f_txt
wi.cell(row=r, column=2, value=f"=({seg_energy})*12*Ramp3*(1+DemandGrowth)^2").number_format = NUM
wi.cell(row=r, column=5, value="kWh/yr").font = f_note
define("DesignEnergy", wi, f"B{r}")
R[0] += 1
r = R[0]
wi.cell(row=r, column=1, value="Design generation (incl. losses)").font = f_txt
wi.cell(row=r, column=2, value="=DesignEnergy/(1-Losses)").number_format = NUM
wi.cell(row=r, column=5, value="kWh/yr").font = f_note
define("DesignGen", wi, f"B{r}")
R[0] += 1
for lab, nm, f, unit in [
    ("PV array", "PV_kWp", "=DesignGen*SolarFraction*StorageFactor/SpecYield*PVOversize", "kWp"),
    ("Battery storage (nameplate)", "BESS_kWh", "=DesignGen/365*NightShareUsed/DoD", "kWh"),
    ("Diesel generator (covers peak)", "Diesel_kW", "=DesignGen/8760*PeakRatioUsed", "kW"),
]:
    r = R[0]
    wi.cell(row=r, column=1, value=lab).font = f_txt
    style_calc(wi.cell(row=r, column=2, value=f), NUM1)
    style_in(wi.cell(row=r, column=3), NUM1)
    style_calc(wi.cell(row=r, column=4, value=f"=IF(ISNUMBER(C{r}),C{r},B{r})"), NUM1, True)
    wi.cell(row=r, column=5, value=unit).font = f_note
    define(nm, wi, f"D{r}")
    R[0] += 1
wi.cell(row=R[0], column=1, value="Leave Override blank to use the auto-size. This is a screening rule of thumb, not an engineering design.").font = f_note
R[0] += 1

section("5. CAPEX (Year 0)")
inp("PV modules, structures & inverters", "C_PV", 700, USD, "per kWp")
inp("Battery storage system", "C_BESS", 350, USD, "per kWh")
inp("Diesel generator", "C_Diesel", 400, USD, "per kW")
inp("Distribution network", "C_Network", 450, USD, "per connection")
inp("Smart meters & service drops", "C_Meter", 80, USD, "per connection")
inp("Powerhouse, BOS, civil works (lump sum)", "C_BOS", 60000, USD)
inp("Productive-use equipment financed by the project", "C_PUEquip", 0, USD, "", "Optional: appliances the developer buys and leases or sells to users.")
inp("Development costs (studies, permits, community)", "C_DevPct", 0.08, PCT, "of hard CAPEX")
inp("Contingency", "C_ContPct", 0.07, PCT, "of hard CAPEX")
inp("Battery life", "BattLife", 8, "0", "years")
inp("Battery replacement cost (Year-0 terms)", "C_BattRepl", 250, USD, "per kWh")
inp("Fund replacements via maintenance reserve? (1 = yes)", "UseMRA", 1, "0", "", "1 = reserve contributions smooth replacements in CFADS (lender practice).")
R[0] += 1
calc("Hard CAPEX (base, before scenario lever)", "HardCapexBase",
     "=PV_kWp*C_PV+BESS_kWh*C_BESS+Diesel_kW*C_Diesel+TotalCustomers*(C_Network+C_Meter)+C_BOS+C_PUEquip", USD)
calc("Total CAPEX (base, before scenario lever)", "TotalCapexBase", "=HardCapexBase*(1+C_DevPct+C_ContPct)", USD, bold=True)

section("6. OPEX (Year-1 values, escalated)")
inp("Fixed O&M", "O_FixedPct", 0.025, PCT, "of hard CAPEX / yr")
inp("Local staff & operator", "O_Staff", 18000, USD, "per year")
inp("Insurance", "O_InsPct", 0.005, PCT, "of total CAPEX / yr")
inp("Licences, land, regulatory fees", "O_Fees", 3000, USD, "per year")
inp("Diesel generator O&M", "O_DieselOM", 0.03, USD3, "per kWh diesel")
inp("Customer management & mobile money fees", "O_CustPct", 0.03, PCT, "of revenue")
inp("MRV & reporting costs (programme compliance)", "O_MRV", 4000, USD, "per year", "Verification, data platform, audits.")

section("7. FUNDING STRUCTURE")
inp("Upfront CAPEX grant", "Grant", 600000, USD, "", "Capital subsidy received in Year 0.")
inp("RBF verification lag", "RBFLag", 0, "0", "years", "0 = paid in the year of connection, 1 = next year. RBF amounts per segment are in section 3.")
inp("Senior debt - share of CAPEX net of grant", "SenPct", 0.20, PCT)
inp("Senior debt - interest rate", "SenRate", 0.10, PCT)
inp("Senior debt - tenor (incl. grace)", "SenTenor", 10, "0", "years")
inp("Senior debt - grace period (interest only)", "SenGrace", 2, "0", "years")
inp("Concessional debt - share of CAPEX net of grant", "ConPct", 0.20, PCT, "", "For example a DFI or climate-fund loan.")
inp("Concessional debt - interest rate", "ConRate", 0.03, PCT)
inp("Concessional debt - tenor (incl. grace)", "ConTenor", 15, "0", "years")
inp("Concessional debt - grace period", "ConGrace", 5, "0", "years")
inp("DSRA target (share of next year's debt service)", "DSRAPct", 0.50, PCT, "", "0.5 = 6 months. Funded by equity, released when the debt is repaid.")

section("8. IMPACT & MRV")
inp("Average household size", "HHSize", 5, NUM1, "people")
inp("Jobs supported per productive user connected", "JobsPerPU", 1.5, NUM1, "jobs", "Use your own survey data. Example value only.")
inp("Diesel CO2 emission factor", "CO2perL", 2.68, "0.00", "kgCO2/litre", "Combustion factor. Verify against your funder's standard.")
inp("Baseline: share of households' energy otherwise from diesel/kerosene", "BaselineShare", 1.0, PCT, "", "1 = counterfactual is fully diesel-based supply.")

# validations
dv_p = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", showErrorMessage=True,
                      error=T("Enter a value between 0% and 100%."))
wi.add_data_validation(dv_p)
for nm in ["Ramp1", "Ramp2", "Ramp3", "Collection", "SolarFraction", "DoD", "RTE", "Losses", "SenPct", "ConPct", "TaxRate",
           "AffordThreshold", "BaselineShare"]:
    dv_p.add(NAMES[nm][1])
dv_l = DataValidation(type="whole", operator="between", formula1="1", formula2=str(MAX_YEARS), showErrorMessage=True,
                      error=T(f"Project life must be 1-{MAX_YEARS} years."))
wi.add_data_validation(dv_l)
dv_l.add(NAMES["Life"][1])
dv_b = DataValidation(type="list", formula1='"0,1"')
wi.add_data_validation(dv_b)
for nm in ["UsePUE", "UseMRA"]:
    dv_b.add(NAMES[nm][1])
wi.freeze_panes = "A4"

# ====================================================================== Load Profile
wl = wb.create_sheet("Load Profile")
wl.sheet_view.showGridLines = False
wl.column_dimensions["A"].width = 10
for j in range(2, 10):
    wl.column_dimensions[get_column_letter(j)].width = 15
wl["A1"] = "LOAD PROFILE (share of each segment's daily energy, by hour)"
wl["A1"].font = f_title
wl["A2"] = "Each segment column must sum to 100%. Shapes are illustrative; replace them with metered data or survey results where you have them."
wl["A2"].font = f_note
wl["A4"] = "Sunrise hour (PV starts)"
wl["A5"] = "Sunset hour (PV stops)"
for rr_ in (4, 5):
    wl[f"A{rr_}"].font = f_txt
style_in(wl["D4"], "0")
style_in(wl["D5"], "0")
wl["D4"] = 6
wl["D5"] = 18
define("Sunrise", wl, "D4")
define("Sunset", wl, "D5")
LP_H = 7
heads = ["Hour"] + [f"Seg {i}" for i in range(1, NSEG + 1)] + ["Weighted (all)", "Night hour?"]
for j, h in enumerate(heads, start=1):
    c = wl.cell(row=LP_H, column=j, value=h)
    c.font = f_h2
    c.fill = fill_sec
    c.alignment = Alignment(horizontal="center", wrap_text=True)
for i in range(1, NSEG + 1):
    wl.cell(row=LP_H - 1, column=1 + i, value=f"=Seg{i}_Name").font = f_note
    wl.cell(row=LP_H - 1, column=1 + i).alignment = Alignment(wrap_text=True, vertical="bottom")
wl.row_dimensions[LP_H - 1].height = 40


def shape(weights):
    tot = sum(weights)
    vals = [round(w / tot, 4) for w in weights]
    vals[-1] = round(1 - sum(vals[:-1]), 4)
    return vals


hh = shape([1, 1, 1, 1, 1, 2, 4, 4, 3, 2, 2, 2, 2, 2, 2, 2, 3, 5, 10, 12, 11, 8, 5, 2])
pu = shape([0.5, 0.5, 0.5, 0.5, 0.5, 1, 3, 7, 10, 11, 11, 10, 8, 9, 10, 9, 6, 3, 2, 1, 1, 0.5, 0.5, 0.5])
co = shape([1, 1, 1, 1, 1, 1, 2, 3, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 8, 8, 7, 5, 3, 2])
ins = shape([2, 2, 2, 2, 2, 2, 3, 6, 9, 9, 9, 8, 8, 8, 8, 7, 4, 3, 3, 3, 2, 2, 2, 2])
ot = shape([1] * 24)
profiles = [hh, pu, co, ins, ot]
LP_F = LP_H + 1
for h in range(24):
    rr_ = LP_F + h
    wl.cell(row=rr_, column=1, value=h).number_format = '00":00"'
    for i in range(NSEG):
        style_in(wl.cell(row=rr_, column=2 + i, value=profiles[i][h]), PCT)
    seg_e = [f"Seg{i}_N*Seg{i}_kWh" for i in range(1, NSEG + 1)]
    num = "+".join(f"{get_column_letter(2 + i)}{rr_}*{seg_e[i]}" for i in range(NSEG))
    den = "+".join(seg_e)
    style_calc(wl.cell(row=rr_, column=2 + NSEG, value=f"=IFERROR(({num})/({den}),0)"), PCT, True)
    style_calc(wl.cell(row=rr_, column=3 + NSEG, value=f"=IF(OR(A{rr_}<Sunrise,A{rr_}>=Sunset),1,0)"), "0")
LP_L = LP_F + 23
tr = LP_L + 1
wl.cell(row=tr, column=1, value="Total").font = f_bold
for j in range(2, 3 + NSEG):
    c = wl.cell(row=tr, column=j, value=f"=SUM({get_column_letter(j)}{LP_F}:{get_column_letter(j)}{LP_L})")
    style_calc(c, PCT, True)
WCOL = get_column_letter(2 + NSEG)
NCOL = get_column_letter(3 + NSEG)
wl.cell(row=tr + 2, column=1, value="Night-time share of daily energy").font = f_bold
style_calc(wl.cell(row=tr + 2, column=4, value=f"=SUMPRODUCT({WCOL}{LP_F}:{WCOL}{LP_L},{NCOL}{LP_F}:{NCOL}{LP_L})"), PCT, True)
define("NightShare", wl, f"D{tr+2}")
wl.cell(row=tr + 3, column=1, value="Peak-to-average ratio (peak hour share x 24)").font = f_bold
style_calc(wl.cell(row=tr + 3, column=4, value=f"=MAX({WCOL}{LP_F}:{WCOL}{LP_L})*24"), MULT, True)
define("PeakRatio", wl, f"D{tr+3}")
define("LP_SumCheck", wl, f"{WCOL}{tr}")
wl.cell(row=tr + 4, column=1, value="Segment totals check").font = f_bold
style_calc(wl.cell(row=tr + 4, column=4, value=f'=IF(SUMPRODUCT(ABS(B{tr}:{get_column_letter(1+NSEG)}{tr}-1)*(B{tr}:{get_column_letter(1+NSEG)}{tr}>0))<0.001,"OK","CHECK")'), "@", True)
define("LP_Check", wl, f"D{tr+4}")
ch = LineChart()
ch.title = T("Weighted daily load shape")
ch.y_axis.title = T("Share of daily energy")
ch.y_axis.number_format = "0%"
ch.add_data(Reference(wl, min_col=2 + NSEG, min_row=LP_H, max_row=LP_L), titles_from_data=True)
ch.set_categories(Reference(wl, min_col=1, min_row=LP_F, max_row=LP_L))
ch.height, ch.width = 8, 16
wl.add_chart(ch, "J7")

# ====================================================================== Productive Use
wp = wb.create_sheet("Productive Use")
wp.sheet_view.showGridLines = False
for j, w in enumerate([40, 12, 12, 12, 12, 14, 16], start=1):
    wp.column_dimensions[get_column_letter(j)].width = w
wp["A1"] = "PRODUCTIVE USE OF ENERGY (appliance inventory)"
wp["A1"].font = f_title
wp["A2"] = "Inventory of productive appliances expected in the community. Values are illustrative; use your demand survey."
wp["A2"].font = f_note
hdr = ["Appliance / activity", "Units", "Rated kW", "Hours / day", "Days / month", "Load factor", "kWh / month"]
for j, h in enumerate(hdr, start=1):
    c = wp.cell(row=4, column=j, value=h)
    c.font = f_h2
    c.fill = fill_sec
    c.alignment = Alignment(horizontal="center", wrap_text=True)
pue = [
    ("Grain mill / huller", 8, 7.5, 4, 26, 0.70),
    ("Welding workshop", 4, 5.0, 3, 22, 0.50),
    ("Cold room / commercial refrigeration", 6, 1.5, 24, 30, 0.35),
    ("Irrigation pump", 10, 1.1, 5, 20, 0.80),
    ("Tailoring (electric sewing machines)", 12, 0.3, 6, 26, 0.60),
    ("Hair salon / barber", 10, 1.0, 4, 26, 0.40),
    ("Carpentry tools", 3, 3.0, 4, 22, 0.50),
    ("", 0, 0, 0, 0, 0),
    ("", 0, 0, 0, 0, 0),
]
for k, row in enumerate(pue):
    rr_ = 5 + k
    c = wp.cell(row=rr_, column=1, value=row[0])
    c.font = f_input
    c.fill = fill_in
    for j, (v, fmt) in enumerate(zip(row[1:], [NUM, NUM1, NUM1, NUM, PCT]), start=2):
        style_in(wp.cell(row=rr_, column=j, value=v), fmt)
    style_calc(wp.cell(row=rr_, column=7, value=f"=B{rr_}*C{rr_}*D{rr_}*E{rr_}*F{rr_}"), NUM, True)
PL = 5 + len(pue) - 1
wp.cell(row=PL + 1, column=1, value="Total productive demand").font = f_bold
style_calc(wp.cell(row=PL + 1, column=7, value=f"=SUM(G5:G{PL})"), NUM, True)
define("PUE_Total", wp, f"G{PL+1}")
wp.cell(row=PL + 2, column=1, value="Productive users (from Inputs, segment 2)").font = f_txt
style_calc(wp.cell(row=PL + 2, column=7, value="=Seg2_N"), NUM)
wp.cell(row=PL + 2, column=7).font = f_link
wp.cell(row=PL + 3, column=1, value="kWh / month per productive user").font = f_bold
style_calc(wp.cell(row=PL + 3, column=7, value="=IFERROR(PUE_Total/Seg2_N,0)"), NUM1, True)
define("PUE_kWhPerUser", wp, f"G{PL+3}")
wp.cell(row=PL + 4, column=1, value="Share of total demand from productive use (Year 3)").font = f_txt
style_calc(wp.cell(row=PL + 4, column=7, value=f"=IFERROR(Seg2_N*Seg2_kWh*12*Ramp3*(1+DemandGrowth)^2/DesignEnergy,0)"), PCT)
wp.cell(row=PL + 6, column=1, value="Why it matters: daytime productive load uses solar directly, improves the load factor and lowers LCOE. Funders often track it as an impact indicator.").font = f_note


# ====================================================================== ENGINE
FC = 3
LC = FC + MAX_YEARS


def L(y):
    return get_column_letter(FC + y)


def build_engine(ws, levers, visible=True):
    """Write the full cash-flow engine on ws. levers: dict of formula strings for case multipliers.
    Returns (ROW dict, S dict of summary cell refs)."""
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 50
    ws.column_dimensions["B"].width = 15
    for col in range(FC, LC + 1):
        ws.column_dimensions[get_column_letter(col)].width = 11
    ws["A1"] = "CASH FLOW ENGINE (annual, nominal)"
    ws["A1"].font = f_title
    ws["A2"] = "All cells are formulas. Column B = total, or NPV at the hurdle rate where marked [B = NPV]."
    ws["A2"].font = f_note
    # case levers
    bar(ws, 4, "CASE LEVERS (relative to the active scenario)", 1, 2)
    lever_keys = ["kTariff", "kDemand", "kCapex", "kOpex", "kColl", "kFuel", "kRate"]
    lever_labels = ["Tariff", "Demand", "CAPEX", "OPEX", "Collection", "Diesel price", "Interest rates"]
    K = {}
    for n, (k, lab) in enumerate(zip(lever_keys, lever_labels)):
        rr_ = 5 + n
        ws.cell(row=rr_, column=1, value=lab).font = f_txt
        c = ws.cell(row=rr_, column=2, value=levers.get(k, 1))
        c.number_format = MULT
        c.font = f_bold
        K[k] = f"$B${rr_}"
    # summary block rows reserved
    SUM_TOP = 13
    bar(ws, SUM_TOP, "CASE SUMMARY", 1, 2)
    summary_keys = [
        ("CapexE", "Total CAPEX (case)", USD), ("HardE", "Hard CAPEX (case)", USD),
        ("SenAmt", "Senior debt", USD), ("ConAmt", "Concessional debt", USD), ("EqAmt", "Equity at construction", USD),
        ("DSRA0", "Initial DSRA funding (equity)", USD),
        ("NPV_Pre", "Project NPV before subsidies", USD), ("NPV_Post", "Project NPV after subsidies", USD),
        ("IRR_Pre", "Project IRR before subsidies", PCT), ("IRR_Post", "Project IRR after subsidies", PCT),
        ("VGF", "Viability gap (PV)", USD), ("EqIRR", "Equity IRR", PCT), ("EqNPV", "Equity NPV at target equity IRR", USD),
        ("MinDSCR", "Minimum DSCR", MULT), ("AvgDSCR", "Average DSCR", MULT), ("LCOE", "LCOE", USD3),
        ("LevRev", "Levelized collected revenue per kWh", USD3),
        ("PVConn", "PV of verified connections (hurdle)", NUM1), ("PVRBF", "PV of RBF received (hurdle)", USD),
        ("PVConnEq", "PV of verified connections (equity rate)", NUM1), ("PVRBFEq", "PV of RBF received (equity rate)", USD),
        ("DebtCap", "Max senior debt at min DSCR (annuity)", USD), ("Payback", "Equity payback (years)", "0"),
    ]
    S = {}
    SROW = {}
    for n, (k, lab, fmt) in enumerate(summary_keys):
        rr_ = SUM_TOP + 1 + n
        ws.cell(row=rr_, column=1, value=lab).font = f_txt
        ws.cell(row=rr_, column=2).number_format = fmt
        ws.cell(row=rr_, column=2).font = f_bold
        S[k] = f"'{ws.title}'!$B${rr_}"
        SROW[k] = rr_
    ROW = {}
    ptr = [SUM_TOP + len(summary_keys) + 3]

    def ref(name, y):
        return f"{L(y)}{ROW[name]}"

    def line(name, label, fn, fmt=USD, total=None, bold=False, start=0):
        rr_ = ptr[0]
        ROW[name] = rr_
        lab = label + ("  [B = NPV]" if total == "npv" else "")
        ws.cell(row=rr_, column=1, value=lab).font = f_bold if bold else f_txt
        for y in range(0, MAX_YEARS + 1):
            c = ws.cell(row=rr_, column=FC + y, value=(fn(y) if y >= start else 0))
            c.number_format = fmt
            c.font = f_bold if bold else f_txt
            if bold:
                c.border = top_line
        if total == "sum":
            c = ws.cell(row=rr_, column=2, value=f"=SUM({L(0)}{rr_}:{L(MAX_YEARS)}{rr_})")
        elif total == "npv":
            c = ws.cell(row=rr_, column=2, value=f"={L(0)}{rr_}+NPV(Hurdle,{L(1)}{rr_}:{L(MAX_YEARS)}{rr_})")
        else:
            c = None
        if c is not None:
            c.number_format = fmt
            c.font = f_bold
        ptr[0] += 1
        return rr_

    def blank():
        ptr[0] += 1

    def sec(title):
        bar(ws, ptr[0], title, 1, LC)
        ptr[0] += 1

    def rowrng(name, y0=0):
        return f"${L(y0)}${ROW[name]}:${L(MAX_YEARS)}${ROW[name]}"

    rr_ = ptr[0]
    ROW["year"] = rr_
    ws.cell(row=rr_, column=1, value="Project year").font = f_bold
    ws.cell(row=rr_, column=2, value="Total / NPV").font = f_bold
    ws.cell(row=rr_, column=2).fill = fill_sec
    for y in range(0, MAX_YEARS + 1):
        c = ws.cell(row=rr_, column=FC + y, value=y)
        c.font = f_bold
        c.fill = fill_sec
        c.alignment = Alignment(horizontal="center")
    ptr[0] += 1
    line("cal", "Calendar year", lambda y: f"=StartYear-1+{ref('year', y)}", fmt="0")
    line("op", "Operating flag", lambda y: f"=IF(AND({ref('year', y)}>=1,{ref('year', y)}<=Life),1,0)", fmt="0")
    line("ramp", "Connection ramp", lambda y: f"=IF({ref('year', y)}=1,Ramp1,IF({ref('year', y)}=2,Ramp2,Ramp3))*{ref('op', y)}", fmt=PCT, start=1)
    line("tesc", "Tariff index", lambda y: f"=(1+TariffEsc)^({ref('year', y)}-1)", fmt="0.000", start=1)
    line("cesc", "Cost index", lambda y: f"=(1+CostEsc)^({ref('year', y)}-1)", fmt="0.000", start=1)
    line("dgrow", "Consumption index (growth x levers)", lambda y: f"=(1+DemandGrowth)^({ref('year', y)}-1)*LevDemand*{K['kDemand']}", fmt="0.000", start=1)
    blank()

    sec("DEMAND & CONNECTIONS")
    for i in range(1, NSEG + 1):
        line(f"conn{i}", "", lambda y, i=i: f"=Seg{i}_N*{ref('ramp', y)}", fmt=NUM, start=1)
        ws.cell(row=ROW[f"conn{i}"], column=1, value=f'="Connections - "&Seg{i}_Name')
    line("conn", "Total connections", lambda y: "=" + "+".join(ref(f"conn{i}", y) for i in range(1, NSEG + 1)), fmt=NUM, bold=True)
    for i in range(1, NSEG + 1):
        line(f"new{i}", "", lambda y, i=i: f"=MAX(0,{ref(f'conn{i}', y)}-{ref(f'conn{i}', y-1)})", fmt=NUM1, total="sum", start=1)
        ws.cell(row=ROW[f"new{i}"], column=1, value=f'="New connections - "&Seg{i}_Name')
    line("newconn", "Total new (verified) connections", lambda y: "=" + "+".join(ref(f"new{i}", y) for i in range(1, NSEG + 1)), fmt=NUM, total="sum", bold=True)
    blank()
    for i in range(1, NSEG + 1):
        line(f"kwh{i}", "", lambda y, i=i: f"={ref(f'conn{i}', y)}*Seg{i}_kWh*12*{ref('dgrow', y)}", fmt=NUM, total="sum", start=1)
        ws.cell(row=ROW[f"kwh{i}"], column=1, value=f'="Energy sold (kWh) - "&Seg{i}_Name')
    line("kwh", "Total energy sold (kWh)", lambda y: "=" + "+".join(ref(f"kwh{i}", y) for i in range(1, NSEG + 1)), fmt=NUM, total="sum", bold=True)
    blank()

    sec("GENERATION MIX")
    line("gen", "Gross generation required (kWh)", lambda y: f"={ref('kwh', y)}/(1-Losses)", fmt=NUM, total="sum", start=1)
    line("pvavail", "PV energy available (kWh)", lambda y: f"=PV_kWp*SpecYield*(1-Degradation)^({ref('year', y)}-1)*{ref('op', y)}", fmt=NUM, total="sum", start=1)
    line("solar", "Solar energy delivered (kWh)", lambda y: f"=MIN({ref('pvavail', y)}/StorageFactor,{ref('gen', y)}*SolarFraction)", fmt=NUM, total="sum", start=1)
    line("diesel", "Diesel energy delivered (kWh)", lambda y: f"={ref('gen', y)}-{ref('solar', y)}", fmt=NUM, total="sum", start=1)
    line("sf", "Actual solar fraction", lambda y: f"=IFERROR({ref('solar', y)}/{ref('gen', y)},0)", fmt=PCT, start=1)
    line("litres", "Diesel consumed (litres)", lambda y: f"={ref('diesel', y)}/DieselEff", fmt=NUM, total="sum", start=1)
    blank()

    sec("REVENUE")
    for i in range(1, NSEG + 1):
        line(f"rev{i}", "", lambda y, i=i: f"={ref(f'kwh{i}', y)}*Seg{i}_Tariff*LevTariff*{K['kTariff']}*{ref('tesc', y)}", total="sum", start=1)
        ws.cell(row=ROW[f"rev{i}"], column=1, value=f'="Billed revenue - "&Seg{i}_Name')
    line("billed", "Total billed energy revenue", lambda y: "=" + "+".join(ref(f"rev{i}", y) for i in range(1, NSEG + 1)), total="sum", bold=True)
    line("collected", "Collected energy revenue", lambda y: f"={ref('billed', y)}*MIN(1,Collection*LevColl*{K['kColl']})", total="sum", start=1)
    line("fees", "Connection fees", lambda y: "=" + "+".join(f"{ref(f'new{i}', y)}*Seg{i}_Fee" for i in range(1, NSEG + 1)), total="sum", start=1)
    line("rev", "TOTAL OPERATING REVENUE", lambda y: f"={ref('collected', y)}+{ref('fees', y)}", total="sum", bold=True)
    blank()

    sec("OPERATING COSTS")
    ox = f"LevOpex*{K['kOpex']}"
    line("o_fixed", "Fixed O&M", lambda y: f"={S['HardE']}*O_FixedPct*{ref('cesc', y)}*{ox}*{ref('op', y)}", total="sum", start=1)
    line("o_staff", "Staff & operator", lambda y: f"=O_Staff*{ref('cesc', y)}*{ox}*{ref('op', y)}", total="sum", start=1)
    line("o_ins", "Insurance", lambda y: f"={S['CapexE']}*O_InsPct*{ref('cesc', y)}*{ox}*{ref('op', y)}", total="sum", start=1)
    line("o_fees", "Licences & fees", lambda y: f"=O_Fees*{ref('cesc', y)}*{ox}*{ref('op', y)}", total="sum", start=1)
    line("o_mrv", "MRV & reporting", lambda y: f"=O_MRV*{ref('cesc', y)}*{ox}*{ref('op', y)}", total="sum", start=1)
    line("o_cust", "Customer management", lambda y: f"={ref('rev', y)}*O_CustPct", total="sum", start=1)
    line("o_dom", "Diesel O&M", lambda y: f"={ref('diesel', y)}*O_DieselOM*{ref('cesc', y)}*{ox}", total="sum", start=1)
    line("o_fuel", "Diesel fuel", lambda y: f"={ref('litres', y)}*FuelPrice*LevFuel*{K['kFuel']}*{ref('cesc', y)}", total="sum", start=1)
    okeys = ["o_fixed", "o_staff", "o_ins", "o_fees", "o_mrv", "o_cust", "o_dom", "o_fuel"]
    line("opex", "TOTAL OPEX", lambda y: "=" + "+".join(ref(k, y) for k in okeys), total="sum", bold=True)
    blank()
    line("ebitda", "EBITDA", lambda y: f"={ref('rev', y)}-{ref('opex', y)}", total="sum", bold=True)
    line("margin", "EBITDA margin", lambda y: f"=IFERROR({ref('ebitda', y)}/{ref('rev', y)},0)", fmt=PCT, start=1)
    blank()

    sec("CAPEX, REPLACEMENTS & SUBSIDIES")
    line("capex", "Initial CAPEX", lambda y: f"={S['CapexE']}" if y == 0 else "=0", total="npv")
    replcost = f"BESS_kWh*C_BattRepl*LevCapex*{K['kCapex']}"
    line("repl", "Battery replacement",
         lambda y: f"=IF(AND({ref('op', y)}=1,MOD({ref('year', y)},BattLife)=0,{ref('year', y)}<Life),{replcost}*{ref('cesc', y)},0)",
         total="npv", start=1)
    line("mra", "Maintenance reserve contribution",
         lambda y: (f"=IF(AND(UseMRA=1,{ref('op', y)}=1,CEILING({ref('year', y)},BattLife)<Life),"
                    f"{replcost}*(1+CostEsc)^(CEILING({ref('year', y)},BattLife)-1)/BattLife,0)"), total="sum", start=1)
    line("repl_cfads", "Replacement cost charged to CFADS", lambda y: f"=IF(UseMRA=1,{ref('mra', y)},{ref('repl', y)})", total="sum", start=1)
    line("grant", "Upfront CAPEX grant", lambda y: "=Grant" if y == 0 else "=0", total="sum")
    line("rbf_due", "RBF earned (new connections x RBF by segment)",
         lambda y: "=" + "+".join(f"{ref(f'new{i}', y)}*Seg{i}_RBF" for i in range(1, NSEG + 1)), total="sum", start=1)
    line("rbf", "RBF received (after verification lag)",
         lambda y: f"=IF({ref('year', y)}-RBFLag>=1,INDEX({rowrng('rbf_due')},1,{ref('year', y)}-RBFLag+1),0)", total="sum", start=1)
    line("conn_lag", "Verified connections paid (after lag)",
         lambda y: f"=IF({ref('year', y)}-RBFLag>=1,INDEX({rowrng('newconn')},1,{ref('year', y)}-RBFLag+1),0)", fmt=NUM, total="sum", start=1)
    blank()

    sec("SENIOR DEBT")
    sr = f"SenRate*{K['kRate']}"
    line("s_open", "Opening balance", lambda y: "=0", start=1)
    line("s_draw", "Drawdown", lambda y: f"={S['SenAmt']}" if y == 0 else "=0", total="sum")
    line("s_int", "Interest", lambda y: f"={ref('s_open', y)}*{sr}", total="sum", start=1)
    line("s_prin", "Principal",
         lambda y: f"=IF(AND({ref('year', y)}>SenGrace,{ref('year', y)}<=SenTenor),PMT({sr},SenTenor-SenGrace,-{S['SenAmt']})-{ref('s_int', y)},0)",
         total="sum", start=1)
    line("s_close", "Closing balance", lambda y: "=0")
    blank()
    sec("CONCESSIONAL DEBT")
    cr = f"ConRate*{K['kRate']}"
    line("c_open", "Opening balance", lambda y: "=0", start=1)
    line("c_draw", "Drawdown", lambda y: f"={S['ConAmt']}" if y == 0 else "=0", total="sum")
    line("c_int", "Interest", lambda y: f"={ref('c_open', y)}*{cr}", total="sum", start=1)
    line("c_prin", "Principal",
         lambda y: f"=IF(AND({ref('year', y)}>ConGrace,{ref('year', y)}<=ConTenor),PMT({cr},ConTenor-ConGrace,-{S['ConAmt']})-{ref('c_int', y)},0)",
         total="sum", start=1)
    line("c_close", "Closing balance", lambda y: "=0")
    blank()
    line("ds", "TOTAL DEBT SERVICE", lambda y: f"={ref('s_int', y)}+{ref('s_prin', y)}+{ref('c_int', y)}+{ref('c_prin', y)}", total="sum", bold=True, start=1)
    line("sen_f", "Senior debt service per $1 of senior debt",
         lambda y: f"=IF({ref('year', y)}<=SenGrace,{sr},IF({ref('year', y)}<=SenTenor,PMT({sr},SenTenor-SenGrace,-1),0))", fmt="0.0000", start=1)
    line("sen_cap", "Max senior debt allowed by this year's CFADS at min DSCR",
         lambda y: f"=IF({ref('sen_f', y)}>0,({{cfads}}/MinDSCR-{ref('c_int', y)}-{ref('c_prin', y)})/{ref('sen_f', y)},1E+12)", start=1)
    line("dsra", "DSRA target balance", lambda y: (f"=DSRAPct*{ref('ds', y+1)}" if y < MAX_YEARS else "=0"))
    line("dsra_mv", "DSRA funding (+) / release (-)", lambda y: (f"={ref('dsra', y)}" if y == 0 else f"={ref('dsra', y)}-{ref('dsra', y-1)}"), total="sum")
    for y in range(0, MAX_YEARS + 1):
        col = FC + y
        for t in ("s", "c"):
            if y >= 1:
                ws.cell(row=ROW[f"{t}_open"], column=col).value = f"={ref(f'{t}_close', y-1)}"
            op_ = ref(f"{t}_open", y) if y >= 1 else "0"
            pr_ = ref(f"{t}_prin", y) if y >= 1 else "0"
            ws.cell(row=ROW[f"{t}_close"], column=col).value = f"={op_}+{ref(f'{t}_draw', y)}-{pr_}"
    blank()

    sec("TAX (loss carry-forward)")
    line("dep", "Tax depreciation", lambda y: f"=IF({ref('year', y)}<=MIN(DepYears,Life),{S['CapexE']}/DepYears,0)", total="sum", start=1)
    for tag, lab, interest in [("u", "unlevered (project IRR)", None), ("l", "levered (after interest)", True)]:
        line(f"ebt_{tag}", f"Taxable result before losses - {lab}",
             (lambda y, interest=interest: f"={ref('ebitda', y)}-{ref('dep', y)}" + (f"-{ref('s_int', y)}-{ref('c_int', y)}" if interest else "")),
             total="sum", start=1)
        line(f"lo_{tag}", "  Tax losses brought forward", lambda y: "=0", start=1)
        line(f"lu_{tag}", "  Losses used", lambda y, tag=tag: f"=MIN({ref(f'lo_{tag}', y)},MAX({ref(f'ebt_{tag}', y)},0))", start=1)
        line(f"lc_{tag}", "  Tax losses carried forward", lambda y, tag=tag: f"={ref(f'lo_{tag}', y)}-{ref(f'lu_{tag}', y)}+MAX(-{ref(f'ebt_{tag}', y)},0)", start=1)
        line(f"tax_{tag}", f"Tax paid - {lab}", lambda y, tag=tag: f"=(MAX({ref(f'ebt_{tag}', y)},0)-{ref(f'lu_{tag}', y)})*TaxRate", total="sum", start=1)
        for y in range(2, MAX_YEARS + 1):
            ws.cell(row=ROW[f"lo_{tag}"], column=FC + y).value = f"={ref(f'lc_{tag}', y-1)}"
    blank()

    sec("CASH FLOWS")
    line("cf_pre", "Project cash flow BEFORE subsidies", lambda y: f"=-{ref('capex', y)}+{ref('ebitda', y)}-{ref('repl', y)}-{ref('tax_u', y)}", total="npv", bold=True)
    line("cf_post", "Project cash flow AFTER subsidies", lambda y: f"={ref('cf_pre', y)}+{ref('grant', y)}+{ref('rbf', y)}", total="npv", bold=True)
    line("cfads", "CFADS", lambda y: f"={ref('ebitda', y)}-{ref('repl_cfads', y)}-{ref('tax_l', y)}+{ref('rbf', y)}", total="sum", start=1)
    for y in range(1, MAX_YEARS + 1):
        c_ = ws.cell(row=ROW["sen_cap"], column=FC + y)
        c_.value = c_.value.replace("{cfads}", ref("cfads", y))
    line("dscr", "DSCR", lambda y: f'=IF({ref("ds", y)}>0,{ref("cfads", y)}/{ref("ds", y)},"")', fmt=MULT, start=1)
    line("cf_eq", "Equity cash flow",
         lambda y: (f"=-{S['EqAmt']}-{ref('dsra_mv', y)}" if y == 0 else f"={ref('cfads', y)}-{ref('ds', y)}-{ref('dsra_mv', y)}"), total="npv", bold=True)
    line("cf_eq_cum", "Cumulative equity cash flow", lambda y: (f"={ref('cf_eq', 0)}" if y == 0 else f"={ref('cf_eq_cum', y-1)}+{ref('cf_eq', y)}"))
    blank()
    sec("LEVELIZED METRICS INPUTS (discounted at hurdle)")
    line("lc_cost", "Lifecycle cost (CAPEX + OPEX excl. revenue-linked + replacements)",
         lambda y: f"={ref('capex', y)}+{ref('opex', y)}-{ref('o_cust', y)}+{ref('repl', y)}", total="npv")
    line("lc_kwh", "Energy sold (kWh)", lambda y: f"={ref('kwh', y)}", fmt=NUM, total="npv")
    line("lc_rev", "Collected energy revenue", lambda y: f"={ref('collected', y)}", total="npv")

    # summary formulas
    def put(k, f):
        ws.cell(row=SROW[k], column=2, value=f)

    tot = lambda n: f"$B${ROW[n]}"
    put("HardE", f"=HardCapexBase*LevCapex*{K['kCapex']}")
    put("CapexE", f"=TotalCapexBase*LevCapex*{K['kCapex']}")
    put("SenAmt", f"=MAX(0,{S['CapexE']}-Grant)*SenPct")
    put("ConAmt", f"=MAX(0,{S['CapexE']}-Grant)*ConPct")
    put("EqAmt", f"=MAX(0,{S['CapexE']}-Grant-{S['SenAmt']}-{S['ConAmt']})")
    put("DSRA0", f"={L(0)}{ROW['dsra']}")
    put("NPV_Pre", f"={tot('cf_pre')}")
    put("NPV_Post", f"={tot('cf_post')}")
    put("IRR_Pre", f'=IFERROR(IRR({rowrng("cf_pre")}),"n/a")')
    put("IRR_Post", f'=IFERROR(IRR({rowrng("cf_post")}),"n/a")')
    put("VGF", f"=MAX(0,-{tot('cf_pre')})")
    put("EqIRR", f'=IFERROR(IRR({rowrng("cf_eq")}),"n/a")')
    put("EqNPV", f"={L(0)}{ROW['cf_eq']}+NPV(TargetEqIRR,{L(1)}{ROW['cf_eq']}:{L(MAX_YEARS)}{ROW['cf_eq']})")
    has_debt = f"({S['SenAmt']}+{S['ConAmt']})>0"
    put("MinDSCR", f'=IF({has_debt},MIN({rowrng("dscr", 1)}),"no debt")')
    put("AvgDSCR", f'=IF({has_debt},AVERAGE({rowrng("dscr", 1)}),"no debt")')
    put("LCOE", f"=IFERROR({tot('lc_cost')}/{tot('lc_kwh')},0)")
    put("LevRev", f"=IFERROR({tot('lc_rev')}/{tot('lc_kwh')},0)")
    put("PVConn", f"=NPV(Hurdle,{L(1)}{ROW['conn_lag']}:{L(MAX_YEARS)}{ROW['conn_lag']})")
    put("PVRBF", f"=NPV(Hurdle,{L(1)}{ROW['rbf']}:{L(MAX_YEARS)}{ROW['rbf']})")
    put("PVConnEq", f"=NPV(TargetEqIRR,{L(1)}{ROW['conn_lag']}:{L(MAX_YEARS)}{ROW['conn_lag']})")
    put("PVRBFEq", f"=NPV(TargetEqIRR,{L(1)}{ROW['rbf']}:{L(MAX_YEARS)}{ROW['rbf']})")
    put("DebtCap", f"=MAX(0,MIN({rowrng('sen_cap', 1)}))")
    put("Payback", f'=IFERROR(MATCH(TRUE,INDEX({rowrng("cf_eq_cum")}>=0,0),0)-1,"> life")')

    # formatting rules
    dr = f"{L(1)}{ROW['dscr']}:{L(MAX_YEARS)}{ROW['dscr']}"
    ws.conditional_formatting.add(dr, FormulaRule(formula=[f'AND(ISNUMBER({L(1)}{ROW["dscr"]}),{L(1)}{ROW["dscr"]}<MinDSCR)'],
                                                  font=Font(name=FONT, color="C00000", bold=True), fill=fill_bad))
    ws.conditional_formatting.add(f"{L(0)}{ROW['cf_eq_cum']}:{L(MAX_YEARS)}{ROW['cf_eq_cum']}",
                                  CellIsRule(operator="lessThan", formula=["0"], font=Font(name=FONT, color="C00000")))
    ws.freeze_panes = f"C{ROW['year']+1}"
    if not visible:
        ws.sheet_state = "hidden"
    return ROW, S


# base engine
wc = wb.create_sheet("Cash Flow")
ROW, S = build_engine(wc, {})


def cf(name, y):
    return f"'Cash Flow'!{L(y)}{ROW[name]}"


def cfrng(name, y0=0):
    return f"'Cash Flow'!${L(y0)}${ROW[name]}:${L(MAX_YEARS)}${ROW[name]}"


def cftot(name):
    return f"'Cash Flow'!$B${ROW[name]}"


# sensitivity engines
SENS_VARS = [("Tariff", "kTariff"), ("Demand", "kDemand"), ("CAPEX", "kCapex"), ("OPEX", "kOpex"),
             ("Collection rate", "kColl"), ("Diesel price", "kFuel"), ("Interest rates", "kRate")]
SENS = []
for nm, k in SENS_VARS:
    pair = {}
    for side, sign in (("Lo", "-"), ("Hi", "+")):
        title = f"S_{k[1:]}_{side}"
        wsx = wb.create_sheet(title)
        _, Sx = build_engine(wsx, {k: f"=1{sign}SensDelta"}, visible=False)
        pair[side] = Sx
    SENS.append((nm, k, pair))


# ====================================================================== Dashboard
wd = wb.create_sheet("Dashboard")
wd.sheet_view.showGridLines = False
for col, w in zip("ABCDEFGHIJKL", [2, 42, 28, 2, 42, 16, 2, 14, 12, 12, 12, 12]):
    wd.column_dimensions[col].width = w
wd["B1"] = '="DASHBOARD - "&ProjectName'
wd["B1"].font = f_title
wd["B2"] = ('=Site&"  |  "&TEXT(TotalCustomers,"#,##0")&" customers  |  "&TEXT(PV_kWp,"#,##0")&" kWp PV / "&TEXT(BESS_kWh,"#,##0")'
            '&" kWh battery / "&TEXT(Diesel_kW,"#,##0")&" kW diesel  |  scenario: "&ScenarioName&"  |  "&Currency')
wd["B2"].font = f_h2
wd["E3"] = '="Model checks: "&ChecksOverall'
wd["E3"].font = f_h2


def kpis(ws, col, row, title, items):
    lc, vc = get_column_letter(col), get_column_letter(col + 1)
    bar(ws, row, title, col, col + 1)
    r_ = row + 1
    for lab, f, fmt, nm in items:
        a = ws[f"{lc}{r_}"]
        a.value = lab
        a.font = f_txt
        a.border = box
        b = ws[f"{vc}{r_}"]
        b.value = f
        b.number_format = fmt
        b.font = f_bold
        b.fill = fill_kpi
        b.border = box
        b.alignment = Alignment(horizontal="right")
        if nm:
            define(nm, ws, f"{vc}{r_}")
        r_ += 1
    return r_


e1 = kpis(wd, 2, 5, "PROJECT ECONOMICS", [
    ("Total CAPEX", f"={S['CapexE']}", USD, "TotalCapex"),
    ("CAPEX per connection", "=IFERROR(TotalCapex/TotalCustomers,0)", USD, "CapexPerConn"),
    ("Project IRR - before subsidies", f"={S['IRR_Pre']}", PCT, "IRR_Pre"),
    ("Project IRR - after subsidies", f"={S['IRR_Post']}", PCT, "IRR_Post"),
    ("Project NPV @ hurdle - before subsidies", f"={S['NPV_Pre']}", USD, "NPV_Pre"),
    ("Project NPV @ hurdle - after subsidies", f"={S['NPV_Post']}", USD, "NPV_Post"),
    ("LCOE (per kWh sold)", f"={S['LCOE']}", USD3, "LCOE"),
    ("Levelized collected revenue per kWh", f"={S['LevRev']}", USD3, "LevRev"),
    ("Average tariff billed, Year 1", f"=IFERROR({cf('billed', 1)}/{cf('kwh', 1)},0)", USD3, "AvgTariff"),
    ("Year-1 EBITDA margin", f"={cf('margin', 1)}", PCT, None),
    ("Average solar fraction (life)", f"=IFERROR({cftot('solar')}/{cftot('gen')},0)", PCT, None),
])
e2 = kpis(wd, 5, 5, "FUNDING & BANKABILITY", [
    ("Upfront grant", "=Grant", USD, None),
    ("RBF received (nominal, life)", f"={cftot('rbf')}", USD, "RBFTotal"),
    ("Senior debt", f"={S['SenAmt']}", USD, "SenAmt"),
    ("Concessional debt", f"={S['ConAmt']}", USD, "ConAmt"),
    ("Equity (construction + initial DSRA)", f"={S['EqAmt']}+{S['DSRA0']}", USD, "EquityTotal"),
    ("Minimum DSCR", f"={S['MinDSCR']}", MULT, "DSCR_Min"),
    ("Average DSCR", f"={S['AvgDSCR']}", MULT, None),
    ("Equity IRR", f"={S['EqIRR']}", PCT, "IRR_Eq"),
    ("Equity NPV at target equity IRR", f"={S['EqNPV']}", USD, "EqNPV"),
    ("Equity payback (years)", f"={S['Payback']}", "0", None),
    ("Viability gap (PV, before subsidies)", f"={S['VGF']}", USD, "VGF"),
])
vr = max(e1, e2) + 1
bar(wd, vr, "BANKABILITY VERDICT", 2, 6)
verdicts = [
    ("Commercially viable without subsidy?", '=IF(NPV_Pre>=0,"YES","NO - needs subsidy")'),
    ("Project viable at hurdle after planned subsidies?", '=IF(NPV_Post>=0,"YES","NO - gap remains")'),
    ("Debt covenant met (min DSCR >= required)?", '=IF(SenAmt+ConAmt=0,"No debt",IF(DSCR_Min>=MinDSCR,"YES","NO - resize debt"))'),
    ("Equity IRR meets target?", '=IF(EqNPV>=0,"YES","NO - see RBF needed")'),
    ("Collected tariff covers LCOE?", '=IF(LevRev>=LCOE,"YES","NO - tariff below cost")'),
    ("Household bills affordable?", '=IF(Seg1_N=0,"n/a",IF(Seg1_Afford="YES","YES","NO - above threshold"))'),
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
wd.conditional_formatting.add(vrng, FormulaRule(formula=[f'OR(LEFT(C{vr+1},LEN("NO - "))="NO - ",C{vr+1}="NO")'], fill=fill_bad, font=Font(name=FONT, bold=True, color="721C24")))
wd[f"B{r_}"] = "Equity IRR test uses equity NPV at the target rate (robust when cash flows change sign)."
wd[f"B{r_}"].font = f_note

# affordability table
bar(wd, vr, "AFFORDABILITY BY SEGMENT (Year 1)", 5, 6)
wd[f"E{vr+1}"] = "Segment  ->  bill as % of income"
wd[f"E{vr+1}"].font = f_h2
for i in range(1, NSEG + 1):
    rr_ = vr + 1 + i
    wd[f"E{rr_}"] = f'=Seg{i}_Name&"  ("&TEXT(Seg{i}_Bill,"$#,##0.00")&"/month)"'
    wd[f"E{rr_}"].font = f_link
    wd[f"E{rr_}"].border = box
    c = wd[f"F{rr_}"]
    c.value = f'=IF(ISNUMBER(Seg{i}_BillPct),Seg{i}_BillPct,"n/a")'
    c.number_format = PCT
    c.font = f_bold
    c.border = box
    c.alignment = Alignment(horizontal="right")
arng = f"F{vr+2}:F{vr+1+NSEG}"
wd.conditional_formatting.add(arng, FormulaRule(formula=[f"AND(ISNUMBER(F{vr+2}),F{vr+2}>AffordThreshold)"], fill=fill_bad))
wd.conditional_formatting.add(arng, FormulaRule(formula=[f"AND(ISNUMBER(F{vr+2}),F{vr+2}<=AffordThreshold)"], fill=fill_ok))
wd[f"E{vr+2+NSEG}"] = '="Threshold: "&TEXT(AffordThreshold,"0.0%")&" of monthly income"'
wd[f"E{vr+2+NSEG}"].font = f_note

# chart data
cd_row = 5
wd.cell(row=cd_row - 1, column=8, value="Chart data (linked from Cash Flow)").font = f_note
for j, h in enumerate(["Year", "Revenue", "OPEX", "CFADS", "Debt service", "Solar kWh", "Diesel kWh"]):
    wd.cell(row=cd_row, column=8 + j, value=h).font = f_h2
for y in range(1, MAX_YEARS + 1):
    rr_ = cd_row + y
    wd.cell(row=rr_, column=8, value=f"={cf('cal', y)}").font = f_link
    for j, key in enumerate(["rev", "opex", "cfads", "ds", "solar", "diesel"], start=1):
        c = wd.cell(row=rr_, column=8 + j, value=f"={cf(key, y)}")
        c.font = f_link
        c.number_format = NUM
for j in range(8, 15):
    wd.column_dimensions[get_column_letter(j)].width = 12
# sources of funds (pie)
src_r = cd_row + MAX_YEARS + 3
wd.cell(row=src_r - 1, column=8, value="Sources of funds (construction)").font = f_h2
src_items = [("Grant", "=MIN(Grant,TotalCapex)"), ("Senior debt", "=SenAmt"), ("Concessional debt", "=ConAmt"), ("Equity", f"={S['EqAmt']}")]
for k, (lab, f) in enumerate(src_items):
    wd.cell(row=src_r + k, column=8, value=lab).font = f_txt
    c = wd.cell(row=src_r + k, column=9, value=f)
    c.number_format = NUM
    c.font = f_link

chart_row = r_ + 3
ch1 = BarChart()
ch1.type = "col"
ch1.title = T("Revenue, OPEX, CFADS, debt service")
ch1.add_data(Reference(wd, min_col=9, max_col=11, min_row=cd_row, max_row=cd_row + MAX_YEARS), titles_from_data=True)
cats = Reference(wd, min_col=8, min_row=cd_row + 1, max_row=cd_row + MAX_YEARS)
ch1.set_categories(cats)
ln = LineChart()
ln.add_data(Reference(wd, min_col=12, min_row=cd_row, max_row=cd_row + MAX_YEARS), titles_from_data=True)
ch1 += ln
ch1.height, ch1.width = 8, 11.5
wd.add_chart(ch1, f"B{chart_row}")
pie = PieChart()
pie.title = T("Sources of funds")
pie.add_data(Reference(wd, min_col=9, min_row=src_r, max_row=src_r + 3))
pie.set_categories(Reference(wd, min_col=8, min_row=src_r, max_row=src_r + 3))
pie.dataLabels = DataLabelList()
pie.dataLabels.showPercent = True
pie.dataLabels.showVal = False
pie.dataLabels.showCatName = False
pie.dataLabels.showSerName = False
pie.dataLabels.showLeaderLines = False
pie.height, pie.width = 8, 11
wd.add_chart(pie, f"E{chart_row}")
ch2 = BarChart()
ch2.type = "col"
ch2.grouping = "stacked"
ch2.overlap = 100
ch2.title = T("Generation mix (kWh)")
ch2.add_data(Reference(wd, min_col=13, max_col=14, min_row=cd_row, max_row=cd_row + MAX_YEARS), titles_from_data=True)
ch2.set_categories(cats)
ch2.height, ch2.width = 8, 11.5
wd.add_chart(ch2, f"B{chart_row+17}")

# ====================================================================== Funding Gap & RBF
wg = wb.create_sheet("Funding Gap & RBF")
wg.sheet_view.showGridLines = False
for col, w in zip("ABCDE", [2, 66, 18, 2, 70]):
    wg.column_dimensions[col].width = w
wg["B1"] = "FUNDING GAP & RBF CALIBRATION"
wg["B1"].font = f_title
wg["B2"] = "Closed-form solutions: project and equity cash flows are linear in the RBF amount, so these results are exact. No Goal Seek is needed."
wg["B2"].font = f_note
blocks = [
    ("1. HOW BIG IS THE GAP?", [
        ("Viability gap: PV subsidy needed for project NPV = 0 at the hurdle rate", "=VGF", USD, None,
         "Present-value subsidy needed with no grant and no RBF."),
        ("Viability gap per connection", "=IFERROR(VGF/TotalCustomers,0)", USD, None, ""),
        ("Planned subsidies, PV at hurdle (grant + RBF)", f"=Grant+{S['PVRBF']}", USD, "PlannedSubsidyPV", ""),
        ("Remaining project-level gap", "=MAX(0,VGF-PlannedSubsidyPV)", USD, "RemainingGap", "0 means the planned subsidies close the gap at the hurdle rate."),
    ]),
    ("2. WHAT GRANT IS NEEDED? (given the planned RBF)", [
        ("Upfront grant needed for project NPV = 0", f"=MAX(0,VGF-{S['PVRBF']})", USD, "GrantNeeded", "Compare with the grant entered on Inputs."),
        ("Planned grant (Inputs)", "=Grant", USD, None, ""),
        ("Grant surplus (+) / shortfall (-)", "=Grant-GrantNeeded", USD, None, ""),
    ]),
    ("3. WHAT RBF IS NEEDED? (given the planned grant)", [
        ("Uniform RBF per connection for project NPV = 0 at hurdle", f"=IFERROR(MAX(0,(VGF-Grant)/{S['PVConn']}),0)", USD, "RBFNeededProj",
         "Same amount for every segment, paid with the verification lag."),
        ("Uniform RBF per connection for equity IRR = target", f"=IFERROR(MAX(0,-(EqNPV-{S['PVRBFEq']})/{S['PVConnEq']}),0)", USD, "RBFNeededEq",
         "Developer's view: RBF needed for equity to earn its target return with the current debt."),
        ("Planned RBF per connection (customer-weighted average)", "=AvgRBFperConn", USD, None, ""),
        ("Scale factor on planned RBF to reach the equity target", f'=IFERROR(MAX(0,-(EqNPV-{S["PVRBFEq"]})/{S["PVRBFEq"]}),"n/a")', MULT, None,
         "Multiply every segment's RBF on Inputs by this factor."),
        ("Total RBF budget at the equity-target level (nominal)", f"=RBFNeededEq*{cftot('conn_lag')}", USD, None, "Useful for a programme's budget envelope."),
    ]),
    ("4. HOW MUCH DEBT CAN THE PROJECT CARRY?", [
        ("Maximum senior debt sized on min DSCR (annuity, binding year)", f"={S['DebtCap']}", USD, "DebtCap",
         "Largest senior loan whose annuity keeps DSCR >= minimum in every year, given current CFADS and concessional debt service."),
        ("Senior debt planned", "=SenAmt", USD, None, ""),
        ("Headroom (+) / excess (-)", "=DebtCap-SenAmt", USD, None, "Negative: reduce senior debt, extend tenor or grace, or add RBF/grant."),
        ("Binding year (lowest DSCR)", f'=IF(ISNUMBER(DSCR_Min),INDEX({cfrng("cal", 1)},1,MATCH(DSCR_Min,{cfrng("dscr", 1)},0)),"n/a")', "0", None,
         "Typical cause: RBF ends while principal repayments of both tranches overlap."),
    ]),
    ("5. RBF CASH TIMING (bridge requirement)", [
        ("RBF received in Years 1-3 (nominal)", f"=SUM({cf('rbf', 1)}:{cf('rbf', 3)})", USD, None,
         "RBF arrives after connections are verified. CAPEX is spent in Year 0, so this amount must be bridged."),
        ("RBF as share of total CAPEX", f"=IFERROR({cftot('rbf')}/TotalCapex,0)", PCT, None, ""),
    ]),
]
r_ = 4
for title, items in blocks:
    bar(wg, r_, title, 2, 3)
    r_ += 1
    for lab, f, fmt, nm, note in items:
        wg[f"B{r_}"] = lab
        wg[f"B{r_}"].font = f_txt
        wg[f"B{r_}"].border = box
        c = wg[f"C{r_}"]
        c.value = f
        c.number_format = fmt
        c.font = f_bold
        c.fill = fill_kpi
        c.border = box
        if nm:
            define(nm, wg, f"C{r_}")
        if note:
            wg[f"E{r_}"] = note
            wg[f"E{r_}"].font = f_note
        r_ += 1
    r_ += 1

# ====================================================================== Sensitivity
wsn = wb.create_sheet("Sensitivity")
wsn.sheet_view.showGridLines = False
for col, w in zip("ABCDEFGHIJKLMNO", [2, 22, 14, 14, 14, 14, 14, 13, 13, 13, 13, 3, 22, 14, 14]):
    wsn.column_dimensions[col].width = w
wsn["B1"] = "SENSITIVITY ANALYSIS (live)"
wsn["B1"].font = f_title
wsn["B2"] = '="Each variable is moved by -/+ "&TEXT(SensDelta,"0%")&" around the active scenario ("&ScenarioName&"), one at a time. Computed by hidden copies of the cash-flow engine."'
wsn["B2"].font = f_note
hdr = ["Variable", "NPV after subs. (low)", "NPV after subs. (high)", "Swing", "Viability gap (low)", "Viability gap (high)",
       "Min DSCR (low)", "Min DSCR (high)", "Equity IRR (low)", "Equity IRR (high)"]
for j, h in enumerate(hdr, start=2):
    c = wsn.cell(row=4, column=j, value=h)
    c.font = f_h2
    c.fill = fill_sec
    c.alignment = Alignment(horizontal="center", wrap_text=True)
wsn.row_dimensions[4].height = 30
wsn["B5"] = "Base case"
wsn["B5"].font = f_bold
for col, f, fmt in [("C", "=NPV_Post", USD), ("D", "=NPV_Post", USD), ("F", "=VGF", USD), ("G", "=VGF", USD), ("H", "=DSCR_Min", MULT), ("I", "=DSCR_Min", MULT),
                    ("J", "=IRR_Eq", PCT), ("K", "=IRR_Eq", PCT)]:
    c = wsn[f"{col}5"]
    c.value = f
    c.number_format = fmt
    c.font = f_bold
SN_F = 6
for n, (nm, k, pair) in enumerate(SENS):
    rr_ = SN_F + n
    wsn[f"B{rr_}"] = nm
    wsn[f"B{rr_}"].font = f_txt
    for col, f, fmt in [
        ("C", f"={pair['Lo']['NPV_Post']}", USD), ("D", f"={pair['Hi']['NPV_Post']}", USD),
        ("E", f"=ABS(D{rr_}-C{rr_})+ROW()/1000000", USD),
        ("F", f"={pair['Lo']['VGF']}", USD), ("G", f"={pair['Hi']['VGF']}", USD),
        ("H", f"={pair['Lo']['MinDSCR']}", MULT), ("I", f"={pair['Hi']['MinDSCR']}", MULT),
        ("J", f"={pair['Lo']['EqIRR']}", PCT), ("K", f"={pair['Hi']['EqIRR']}", PCT),
    ]:
        c = wsn[f"{col}{rr_}"]
        c.value = f
        c.number_format = fmt
        c.font = f_link if col != "E" else f_txt
        c.border = box
SN_L = SN_F + len(SENS) - 1
wsn[f"B{SN_L+1}"] = "Low = variable x (1 - range); High = variable x (1 + range). Collection rate is capped at 100%. Interest rates do not change project NPV (unlevered); see DSCR and equity IRR."
wsn[f"B{SN_L+1}"].font = f_note
# tornado table sorted by swing (largest first)
bar(wsn, 4, "TORNADO (chart order)", 13, 15)
for j, h in enumerate(["Variable", "Low vs base", "High vs base"], start=13):
    c = wsn.cell(row=5, column=j, value=h)
    c.font = f_h2
    c.fill = fill_sec
for n in range(len(SENS)):
    rr_ = 6 + n
    m = f"MATCH(LARGE($E${SN_F}:$E${SN_L},{len(SENS)-n}),$E${SN_F}:$E${SN_L},0)"
    wsn[f"M{rr_}"] = f"=INDEX($B${SN_F}:$B${SN_L},{m})"
    wsn[f"N{rr_}"] = f"=INDEX($C${SN_F}:$C${SN_L},{m})-NPV_Post"
    wsn[f"O{rr_}"] = f"=INDEX($D${SN_F}:$D${SN_L},{m})-NPV_Post"
    for col in "NO":
        wsn[f"{col}{rr_}"].number_format = USD
tor = BarChart()
tor.type = "bar"
tor.grouping = "clustered"
tor.overlap = 100
tor.title = T("Change in project NPV after subsidies vs base")
tor.add_data(Reference(wsn, min_col=14, max_col=15, min_row=5, max_row=5 + len(SENS)), titles_from_data=True)
tor.set_categories(Reference(wsn, min_col=13, min_row=6, max_row=5 + len(SENS)))
tor.height, tor.width = 9, 20
tor.x_axis.tickLblPos = "low"
tor.y_axis.number_format = "#,##0"
wsn.add_chart(tor, f"B{SN_L+4}")
be = SN_L + 23
bar(wsn, be, "BREAK-EVEN INDICATORS (approximate, linear interpolation)", 2, 4)
tar_pair = SENS[0][2]
wsn[f"B{be+1}"] = "Tariff multiplier for NPV before subsidies = 0"
wsn[f"D{be+1}"] = (f"=IFERROR(1+(0-NPV_Pre)/(({tar_pair['Hi']['NPV_Pre']}-{tar_pair['Lo']['NPV_Pre']})/(2*SensDelta)),\"n/a\")")
wsn[f"D{be+1}"].number_format = MULT
wsn[f"B{be+2}"] = "Implied break-even average tariff (no subsidy), Year 1"
wsn[f"D{be+2}"] = f'=IFERROR(D{be+1}*AvgTariff,"n/a")'
wsn[f"D{be+2}"].number_format = USD3
define("BreakEvenTariff", wsn, f"D{be+2}")
for rr_ in (be + 1, be + 2):
    wsn[f"B{rr_}"].font = f_txt
    wsn[f"D{rr_}"].font = f_bold
    wsn[f"D{rr_}"].fill = fill_kpi
wsn[f"B{be+3}"] = "Approximation: tax and the solar/diesel split make NPV slightly non-linear in tariff. Confirm by entering the tariff on Inputs."
wsn[f"B{be+3}"].font = f_note

# ====================================================================== Impact & MRV
wm = wb.create_sheet("Impact & MRV")
wm.sheet_view.showGridLines = False
wm.column_dimensions["A"].width = 50
wm.column_dimensions["B"].width = 15
for col in range(FC + 1, LC + 1):
    wm.column_dimensions[get_column_letter(col)].width = 11
wm["A1"] = "IMPACT & MRV INDICATORS"
wm["A1"].font = f_title
wm["A2"] = "Annual indicators for results verification and impact reporting. Adapt definitions to your programme's MRV framework."
wm["A2"].font = f_note
r_ = 4
wm.cell(row=r_, column=1, value="Year").font = f_bold
wm.cell(row=r_, column=2, value="Total / end").font = f_bold
for y in range(1, MAX_YEARS + 1):
    c = wm.cell(row=r_, column=FC + y, value=f"={cf('cal', y)}")
    c.font = f_bold
    c.fill = fill_sec
wm.cell(row=r_, column=2).fill = fill_sec
IM = {}


def mline(key, label, fn, fmt=NUM, total="sum"):
    global r_
    r_ += 1
    IM[key] = r_
    wm.cell(row=r_, column=1, value=label).font = f_txt
    for y in range(1, MAX_YEARS + 1):
        c = wm.cell(row=r_, column=FC + y, value=fn(y))
        c.number_format = fmt
        c.font = f_link
    if total == "sum":
        wm.cell(row=r_, column=2, value=f"=SUM({L(1)}{r_}:{L(MAX_YEARS)}{r_})")
    elif total == "max":
        wm.cell(row=r_, column=2, value=f"=MAX({L(1)}{r_}:{L(MAX_YEARS)}{r_})")
    wm.cell(row=r_, column=2).number_format = fmt
    wm.cell(row=r_, column=2).font = f_bold


bar(wm, r_ + 1, "ACCESS", 1, LC)
r_ += 1
for i in range(1, NSEG + 1):
    mline(f"new{i}", "", lambda y, i=i: f"={cf(f'new{i}', y)}")
    wm.cell(row=IM[f"new{i}"], column=1, value=f'="Verified new connections - "&Seg{i}_Name')
mline("conn", "Customers connected (end of year)", lambda y: f"={cf('conn', y)}", total="max")
mline("people", "People with electricity access (households x household size)", lambda y: f"={cf('conn1', y)}*HHSize", total="max")
mline("pu", "Productive users connected", lambda y: f"={cf('conn2', y)}", total="max")
mline("jobs", "Jobs supported (productive users x jobs per user)", lambda y: f"={cf('conn2', y)}*JobsPerPU", NUM, total="max")
mline("inst", "Public institutions connected", lambda y: f"={cf('conn4', y)}", total="max")
r_ += 1
bar(wm, r_ + 1, "ENERGY & CLIMATE", 1, LC)
r_ += 1
mline("mwh", "Energy delivered (MWh)", lambda y: f"={cf('kwh', y)}/1000", NUM1)
mline("pumwh", "Energy to productive users (MWh)", lambda y: f"={cf('kwh2', y)}/1000", NUM1)
mline("solar", "Renewable generation delivered (MWh)", lambda y: f"={cf('solar', y)}/1000", NUM1)
mline("sf", "Renewable share of generation", lambda y: f"={cf('sf', y)}", PCT, total=None)
mline("co2", "CO2 avoided vs diesel baseline (tCO2)", lambda y: f"={cf('solar', y)}/DieselEff*CO2perL/1000*BaselineShare", NUM1)
r_ += 1
bar(wm, r_ + 1, "RESULTS-BASED FINANCE", 1, LC)
r_ += 1
mline("rbf_due", "RBF earned (verified)", lambda y: f"={cf('rbf_due', y)}", USD)
mline("rbf", "RBF disbursed (after lag)", lambda y: f"={cf('rbf', y)}", USD)
r_ += 2
bar(wm, r_, "COST-EFFECTIVENESS (life of project)", 1, 2)
eff = [
    ("Public grant funding (grant + RBF, nominal)", f"=Grant+{cftot('rbf')}", USD, "PublicGrant"),
    ("Private capital mobilised (senior debt + equity incl. DSRA)", f"=SenAmt+{S['EqAmt']}+{S['DSRA0']}", USD, "PrivateCap"),
    ("Concessional debt", "=ConAmt", USD, None),
    ("Leverage: private capital per $ of public grant", "=IFERROR(PrivateCap/PublicGrant,0)", MULT, None),
    ("Public grant per connection", "=IFERROR(PublicGrant/TotalCustomers,0)", USD, "GrantPerConn"),
    ("Public grant per person with access", f"=IFERROR(PublicGrant/$B${IM['people']},0)", USD, None),
    ("Public grant per tCO2 avoided", f"=IFERROR(PublicGrant/$B${IM['co2']},0)", USD, None),
    ("People with access (peak)", f"=$B${IM['people']}", NUM, "People"),
    ("Lifetime CO2 avoided (tCO2)", f"=$B${IM['co2']}", NUM, "CO2Total"),
    ("Jobs supported (peak)", f"=$B${IM['jobs']}", NUM, "Jobs"),
]
for lab, f, fmt, nm in eff:
    r_ += 1
    wm.cell(row=r_, column=1, value=lab).font = f_txt
    wm.cell(row=r_, column=1).border = box
    c = wm.cell(row=r_, column=2, value=f)
    c.number_format = fmt
    c.font = f_bold
    c.fill = fill_kpi
    c.border = box
    if nm:
        define(nm, wm, f"B{r_}")
wm.freeze_panes = "C5"

# ====================================================================== Financing Request
wf = wb.create_sheet("Financing Request")
wf.sheet_view.showGridLines = False
wf.column_dimensions["A"].width = 2
wf.column_dimensions["B"].width = 50
wf.column_dimensions["C"].width = 18
wf.column_dimensions["D"].width = 12
wf.column_dimensions["E"].width = 50
wf.column_dimensions["F"].width = 18
wf["B1"] = '="FINANCING REQUEST - "&ProjectName'
wf["B1"].font = f_title
wf["B2"] = "Auto-generated from the model. Copy the paragraphs into your concept note and edit the wording. Check every figure before submission."
wf["B2"].font = f_note
paras = [
    ("PROJECT SUMMARY",
     '=Sponsor&" will build and operate a solar PV-battery-diesel mini-grid in "&Site&", connecting "&TEXT(TotalCustomers,"#,##0")'
     '&" customers ("&TEXT(Seg1_N,"#,##0")&" households, "&TEXT(Seg2_N,"#,##0")&" productive users, "&TEXT(Seg3_N,"#,##0")'
     '&" businesses and "&TEXT(Seg4_N,"#,##0")&" public institutions) and giving about "&TEXT(People,"#,##0")&" people access to electricity."'),
    ("TECHNICAL SOLUTION",
     '="The system combines "&TEXT(PV_kWp,"#,##0")&" kWp of solar PV, "&TEXT(BESS_kWh,"#,##0")&" kWh of battery storage and "'
     '&TEXT(Diesel_kW,"#,##0")&" kW of backup diesel capacity. It delivers "&TEXT(SUM(\'Cash Flow\'!$D$' + str(ROW['kwh']) + ':$W$' + str(ROW['kwh']) + ')/1000,"#,##0")'
     '&" MWh over its life with an average renewable share of "&TEXT(\'Cash Flow\'!$B$' + str(ROW['solar']) + '/\'Cash Flow\'!$B$' + str(ROW['gen']) + ',"0%")&"."'),
    ("INVESTMENT AND FUNDING GAP",
     '="Total investment is "&Currency&" "&TEXT(TotalCapex,"#,##0")&" ("&Currency&" "&TEXT(CapexPerConn,"#,##0")&" per connection). On tariff revenue alone the project NPV at "'
     '&TEXT(Hurdle,"0%")&" is "&Currency&" "&TEXT(NPV_Pre,"#,##0;(#,##0)")&", a viability gap of "&Currency&" "&TEXT(VGF,"#,##0")&" in present-value terms ("&Currency&" "'
     '&TEXT(VGF/TotalCustomers,"#,##0")&" per connection). The levelized cost of electricity is "&Currency&" "&TEXT(LCOE,"0.00")&"/kWh against an average tariff of "&Currency&" "&TEXT(AvgTariff,"0.00")&"/kWh."'),
    ("FUNDING REQUEST",
     '="We request an upfront grant of "&Currency&" "&TEXT(Grant,"#,##0")&" and results-based financing averaging "&Currency&" "&TEXT(AvgRBFperConn,"#,##0")'
     '&" per verified connection ("&Currency&" "&TEXT(RBFTotal,"#,##0")&" in total), alongside "&Currency&" "&TEXT(ConAmt,"#,##0")&" of concessional debt. These leverage "'
     '&Currency&" "&TEXT(SenAmt,"#,##0")&" of senior debt and "&Currency&" "&TEXT(EquityTotal,"#,##0")&" of sponsor equity."'),
    ("BANKABILITY",
     '="With this structure the project NPV after subsidies is "&Currency&" "&TEXT(NPV_Post,"#,##0")&", the minimum DSCR is "&IF(ISNUMBER(DSCR_Min),TEXT(DSCR_Min,"0.00")&"x","n/a")'
     '&" (lender requirement "&TEXT(MinDSCR,"0.00")&"x) and the equity IRR is "&IF(ISNUMBER(IRR_Eq),TEXT(IRR_Eq,"0.0%"),"n/a")&" (target "&TEXT(TargetEqIRR,"0%")&")."'),
    ("IMPACT",
     '="Over its life the project avoids about "&TEXT(CO2Total,"#,##0")&" tCO2 relative to diesel supply and supports about "&TEXT(Jobs,"#,##0")'
     '&" jobs in productive enterprises. Public grant funding amounts to "&Currency&" "&TEXT(GrantPerConn,"#,##0")&" per connection."'),
]
r_ = 4
for title, f in paras:
    wf[f"B{r_}"] = title
    wf[f"B{r_}"].font = f_h2
    wf.merge_cells(start_row=r_ + 1, start_column=2, end_row=r_ + 1, end_column=6)
    c = wf[f"B{r_+1}"]
    c.value = f
    c.font = f_txt
    c.alignment = Alignment(wrap_text=True, vertical="top")
    wf.row_dimensions[r_ + 1].height = 44
    r_ += 3
# sources and uses
su = r_ + 1
bar(wf, su, "USES OF FUNDS", 2, 3)
bar(wf, su, "SOURCES OF FUNDS", 5, 6)
uses = [
    ("Solar PV", "=PV_kWp*C_PV*LevCapex"), ("Battery storage", "=BESS_kWh*C_BESS*LevCapex"), ("Diesel generator", "=Diesel_kW*C_Diesel*LevCapex"),
    ("Distribution network & meters", "=TotalCustomers*(C_Network+C_Meter)*LevCapex"), ("Powerhouse, BOS, civil works", "=C_BOS*LevCapex"),
    ("Productive-use equipment", "=C_PUEquip*LevCapex"), ("Development costs", "=HardCapexBase*C_DevPct*LevCapex"),
    ("Contingency", "=HardCapexBase*C_ContPct*LevCapex"), ("Initial DSRA funding", f"={S['DSRA0']}"),
]
sources = [("Upfront grant", "=MIN(Grant,TotalCapex)"), ("Senior debt", "=SenAmt"), ("Concessional debt", "=ConAmt"),
           ("Sponsor equity (incl. DSRA)", f"={S['EqAmt']}+{S['DSRA0']}")]
for k, (lab, f) in enumerate(uses):
    wf[f"B{su+1+k}"] = lab
    wf[f"B{su+1+k}"].font = f_txt
    wf[f"C{su+1+k}"] = f
    wf[f"C{su+1+k}"].font = f_txt
    wf[f"C{su+1+k}"].number_format = USD
    wf[f"B{su+1+k}"].border = box
    wf[f"C{su+1+k}"].border = box
for k, (lab, f) in enumerate(sources):
    wf[f"E{su+1+k}"] = lab
    wf[f"E{su+1+k}"].font = f_txt
    wf[f"F{su+1+k}"] = f
    wf[f"F{su+1+k}"].font = f_txt
    wf[f"F{su+1+k}"].number_format = USD
    wf[f"E{su+1+k}"].border = box
    wf[f"F{su+1+k}"].border = box
tu = su + 1 + len(uses)
wf[f"B{tu}"] = "TOTAL USES"
wf[f"C{tu}"] = f"=SUM(C{su+1}:C{tu-1})"
wf[f"E{tu}"] = "TOTAL SOURCES"
wf[f"F{tu}"] = f"=SUM(F{su+1}:F{su+len(sources)})"
for cc in (f"B{tu}", f"C{tu}", f"E{tu}", f"F{tu}"):
    wf[cc].font = f_bold
    wf[cc].border = top_line
wf[f"C{tu}"].number_format = USD
wf[f"F{tu}"].number_format = USD
define("UsesTotal", wf, f"C{tu}")
define("SourcesTotal", wf, f"F{tu}")
wf[f"E{su+len(sources)+2}"] = '="Plus RBF of "&Currency&" "&TEXT(RBFTotal,"#,##0")&" received after verification (bridge required)."'
wf[f"E{su+len(sources)+2}"].font = f_note
km = tu + 2
bar(wf, km, "KEY METRICS", 2, 3)
for k, (lab, f, fmt) in enumerate([
    ("Project IRR before / after subsidies", '=IF(ISNUMBER(IRR_Pre),TEXT(IRR_Pre,"0.0%"),"n/a")&"  /  "&IF(ISNUMBER(IRR_Post),TEXT(IRR_Post,"0.0%"),"n/a")', "@"),
    ("Equity IRR", "=IRR_Eq", PCT), ("Minimum DSCR", "=DSCR_Min", MULT), ("LCOE (per kWh)", "=LCOE", USD3),
    ("Viability gap (PV)", "=VGF", USD), ("Uniform RBF needed for equity target (per connection)", "=RBFNeededEq", USD),
    ("Leverage: private capital per $ of public grant", "=IFERROR(PrivateCap/PublicGrant,0)", MULT),
]):
    rr_ = km + 1 + k
    wf[f"B{rr_}"] = lab
    wf[f"B{rr_}"].font = f_txt
    wf[f"C{rr_}"] = f
    wf[f"C{rr_}"].number_format = fmt
    wf[f"C{rr_}"].alignment = Alignment(horizontal="right")
    wf[f"B{rr_}"].border = box
    wf[f"C{rr_}"].border = box
    wf[f"C{rr_}"].font = f_bold

# ====================================================================== Checks
wk = wb.create_sheet("Checks")
wk.sheet_view.showGridLines = False
wk.column_dimensions["A"].width = 80
wk.column_dimensions["B"].width = 12
wk["A1"] = "INTEGRITY CHECKS"
wk["A1"].font = f_title
ROWc = ROW
checks = [
    ("Sources = uses at construction", "=ABS(SourcesTotal-UsesTotal)<1"),
    ("Senior + concessional share <= 100%", "=SenPct+ConPct<=1"),
    ("Senior debt repaid by end of tenor", f"=ABS(INDEX({cfrng('s_close')},1,MIN(SenTenor,{MAX_YEARS})+1))<1"),
    ("Concessional debt repaid by end of tenor", f"=ABS(INDEX({cfrng('c_close')},1,MIN(ConTenor,{MAX_YEARS})+1))<1"),
    ("Debt tenors within project life", "=AND(SenTenor<=Life,ConTenor<=Life)"),
    ("Grace periods shorter than tenors", "=AND(SenGrace<SenTenor,ConGrace<ConTenor)"),
    ("Project life within modelled horizon", f"=AND(Life>=1,Life<={MAX_YEARS})"),
    ("Load profile: each segment sums to 100%", '=LP_Check="OK"'),
    ("Energy balance: solar + diesel = generation", f"=ABS({cftot('solar')}+{cftot('diesel')}-{cftot('gen')})<1"),
    ("Maintenance reserve contributions = replacements (when used)", f"=OR(UseMRA=0,ABS({cftot('mra')}-SUM({cfrng('repl')}))<1)"),
    ("DSRA fully released at end", f"=ABS({cftot('dsra_mv')})<1"),
    ("Subsidy identity: NPV after = NPV before + grant + PV(RBF)", f"=ABS(NPV_Post-NPV_Pre-Grant-{S['PVRBF']})<1"),
    ("RBF calibration reproduces equity target (identity check)", f"=OR(RBFNeededEq=0,ABS(EqNPV-{S['PVRBFEq']}+RBFNeededEq*{S['PVConnEq']})<1)"),
    ("Tax losses never negative", f"=MIN({cfrng('lc_u')})>=-0.01"),
    ("At least one customer", "=TotalCustomers>0"),
    ("Sensitivity engines reproduce base at zero range (base row = Cash Flow)", f"=ABS({S['NPV_Post']}-NPV_Post)<1"),
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
order = ["Start Here", "Inputs", "Load Profile", "Productive Use", "Dashboard", "Funding Gap & RBF", "Sensitivity",
         "Impact & MRV", "Financing Request", "Cash Flow", "Checks"]
order = [T(n) for n in order]
visible = [wb[n] for n in order]
hidden = [ws for ws in wb.worksheets if ws.title not in order]
wb._sheets = visible + hidden
tabs = {"Start Here": NAVY, "Inputs": "FFC000", "Load Profile": "FFC000", "Productive Use": "FFC000", "Dashboard": TEAL,
        "Funding Gap & RBF": TEAL, "Sensitivity": TEAL, "Impact & MRV": TEAL, "Financing Request": TEAL}
for ws in wb.worksheets:
    ws.sheet_properties.tabColor = {T(k): v for k, v in tabs.items()}.get(ws.title, "7F7F7F")
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
wb.active = 0
print_areas.apply(wb)
wb.save(OUT)
print("saved", OUT)
i18n.report()
