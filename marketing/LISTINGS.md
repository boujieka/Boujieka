# Marketplace listings: Mini-Grid Financial Feasibility Calculator

Product file: `product/01-entry-calculator/MiniGrid_Feasibility_Calculator_v1.xlsx`
Suggested launch price: **$24** (test range $19–29). Bundle and upsell prices are set in `docs/STRATEGIE_POSITIONNEMENT.md`.

> Before publishing: check the current Etsy and Gumroad rules on digital downloads, fees and VAT in your seller account. Do not add claims about sales, users or certifications you cannot prove.

---

## ETSY

**Title** (Etsy limit: 140 characters, checked by `tools/check_listing.py`)
```
Mini-Grid Financial Model Excel, Solar Battery Diesel Feasibility Calculator, Energy Access, RBF Subsidy, IRR NPV LCOE DSCR
```

**Tags** (13 tags, max 20 characters each)
```
mini grid model
solar finance model
energy access
project finance
excel template
LCOE calculator
IRR NPV template
off grid solar
renewable energy
feasibility study
DSCR debt model
battery storage
africa energy
```

**Description**
```
Is your mini-grid viable, can it carry debt, and how much subsidy does it really need?

This Excel model answers those three questions in about 10 minutes. It is built for energy-access projects (rural mini-grids with solar PV, batteries and diesel backup), not for utility-scale solar farms.

WHAT YOU GET
- Excel workbook (.xlsx), fully unlocked, formula-driven, no macros
- Pre-filled worked example (illustrative values) so you can see every output immediately
- Built-in quick guide, integrity checks and a 15-page PDF user manual (English and French)

WHAT MAKES IT DIFFERENT
Most solar models stop at "what is my IRR?". This one also calculates the VIABILITY GAP: the upfront subsidy needed for the project to reach your hurdle rate. It then shows how much of that gap your planned grant and results-based financing (RBF per connection) actually cover.

FEATURES
- Customer segments: households, productive users, commercial, institutions
- Connection ramp-up, consumption growth and collection rate
- Automatic sizing of PV (kWp), battery (kWh) and diesel generator (kW), with manual override
- CAPEX per connection, OPEX, fuel and battery replacements
- Maintenance reserve option that smooths battery replacements, as lenders expect
- Upfront grant and RBF per verified connection (with verification lag)
- Senior debt with grace period: CFADS, minimum and average DSCR
- Project IRR before and after subsidies, equity IRR, NPV, LCOE, payback
- Bankability verdict: viable without subsidy? debt covenant met? tariff covers cost?
- Scenario levers: tariff, demand, CAPEX, OPEX
- CO2 avoided compared with diesel-only supply
- 20-year annual cash flow, charts and dashboard

WHO IT IS FOR
Mini-grid developers, energy-access consultants, NGO and programme staff, students and analysts preparing a pre-feasibility study or funding application.

IMPORTANT
This is a screening and pre-feasibility tool. It does not replace engineering design or investment due diligence. Example values are illustrative, not market benchmarks.

FORMAT
Instant digital download. Works in Microsoft Excel 2010 or later. LibreOffice also opens it. Google Sheets may display some formatting differently. No physical item will be shipped.

LICENCE
Single user or single organisation. Not for resale or redistribution.
```

---

## GUMROAD

**Name:** Mini-Grid Financial Feasibility Calculator (Energy Access Edition)

**Short summary (one line):**
Find out whether your solar mini-grid is viable, bankable, and how much grant or RBF closes the funding gap.

**Page body:**
```
From community demand to funding gap, in one Excel model.

THE PROBLEM
Rural mini-grids rarely pass a commercial investment test on tariffs alone. Developers and programme teams need one number: how much subsidy makes this project work, and in what form (upfront grant or results-based financing)?

WHAT THIS MODEL DOES
1. Demand: customer segments, connection ramp-up, consumption growth, collection rate
2. Design: auto-sizes PV, battery and diesel (override with your own design)
3. Costs: CAPEX per connection, OPEX, fuel, battery replacement with maintenance reserve
4. Finance: grant, RBF per connection, senior debt with grace period
5. Results: project and equity IRR, NPV, LCOE, CFADS, DSCR, payback, CO2 avoided
6. Verdict: VIABILITY GAP, the subsidy needed to reach your hurdle rate, and the share your planned subsidies already cover

INCLUDED
- .xlsx workbook, unlocked, no macros
- Worked example of a 970-customer village mini-grid (illustrative values)
- Built-in guide, colour-coded inputs, integrity checks, PDF user manual (EN and FR)

NOT INCLUDED
Engineering-grade hourly dispatch (use dedicated design software for that), legal or tax advice.

COMING NEXT
Developer Edition (affordability, RBF calibration, sensitivities, MRV, financing request) and Fund Manager Edition (portfolio allocation of RBF and catalytic capital). Buyers of this calculator receive a launch discount.
```

**Gumroad tiers (optional):**
- Calculator: $24
- Calculator + 30-minute walkthrough call: price to be set by you. Only offer this if you can deliver it.

---

## Listing images to produce (5–7)
1. Dashboard screenshot with the verdict table (YES/NO colour codes)
2. "Viability gap" close-up: $879,325 needed vs $889,705 planned (from the worked example)
3. Inputs sheet showing the yellow input cells
4. Charts: revenue vs OPEX vs CFADS; generation mix
5. Feature list graphic: "Not just IRR: viability gap, RBF, DSCR"
6. Who it is for: developers, consultants, programmes

Screenshots must come from the real file. Do not use mock-up numbers that differ from the workbook.

---

# Developer Edition: Energy Access Project Financial Model

Product file: `product/02-developer-edition/EnergyAccess_Developer_Model_v1.xlsx`
Suggested launch price: **$99** (test range $79–129). Offer a discount code to buyers of the entry calculator.

## ETSY

**Title**
```
Energy Access Financial Model Excel, Mini-Grid RBF Subsidy Calculator, Viability Gap, Blended Finance, DSCR IRR, Funding Request
```

**Tags**
```
mini grid model
energy access
RBF subsidy
blended finance
viability gap
project finance
solar finance model
DSCR debt model
off grid solar
impact reporting
excel finance model
funding proposal
africa energy
```

**Description**
```
How much grant or results-based financing does your mini-grid really need? This model computes it, exactly.

BUILT FOR
Mini-grid developers applying to RBF or grant programmes, energy-access consultants, and programme and fund teams who need to size subsidies.

WHAT IT CALCULATES
- Viability gap: the subsidy needed for the project to reach your hurdle rate
- Grant needed, given your planned RBF
- RBF per connection needed for project NPV = 0, and for your target equity IRR (solved in closed form, no Goal Seek)
- Maximum senior debt the project can carry at your minimum DSCR, and the binding year
- RBF cash timing and the bridge you need

FEATURES
- 5 customer segments with their own tariff, connection fee, RBF amount and income (affordability test)
- Hourly load profile that sizes the battery and the generator
- Productive-use appliance inventory (mills, welding, cold rooms, pumps)
- Auto-sizing of PV, battery and diesel, with manual override
- Blended finance: grant, RBF, concessional debt, senior debt, equity and DSRA
- Maintenance reserve for battery replacements, and tax losses carried forward
- Scenarios (Base, Conservative, Optimistic, Custom) and a live tornado sensitivity
- Impact & MRV: verified connections, people with access, productive users, jobs, MWh, CO2 avoided, grant per connection, per person and per tCO2, private capital leverage
- Financing Request sheet: auto-written project summary, funding request, sources & uses, ready to paste into a concept note
- 16 automatic integrity checks

WHAT IT IS NOT
A full corporate model: no FX, VAT, working capital or balance sheet, and no debt sculpting. It focuses on subsidy sizing, affordability and impact, and can be used alongside a full project-finance model.

FORMAT
.xlsx, no macros, fully unlocked. Excel 2010 or later. Includes a worked example (illustrative values) and a 16-page PDF user manual in English and French. Instant digital download.

LICENCE
Single user or single organisation. No resale.
```

## GUMROAD

**Name:** Energy Access Project Financial Model (Developer Edition)
**Summary:** From community demand to a bankable funding request: size the grant, RBF and debt your mini-grid needs.
**Page body:** reuse the Etsy description. Add a screenshot of "Funding Gap & RBF" and one of the tornado.

---

# Fund Manager Edition: Energy Access Fund Manager Model (RBF & Portfolio)

Product files: `product/03-fund-manager/EnergyAccess_Fund_Manager_Model_v1.xlsx` (EN) and `..._FR.xlsx` (FR).
Suggested launch price: **$249** (test range $199–299). Better sold through Gumroad + LinkedIn than Etsy (see strategy doc). Consider offering configuration to a fund's own rules as a paid service.

## ETSY

**Title**
```
Energy Access Fund Manager Excel Model, RBF Portfolio Allocation, Project Scoring, Mini-Grid Subsidy Fund, Disbursement and MRV Tracker
```

**Tags**
```
fund management
RBF subsidy
energy access
portfolio model
project scoring
grant allocation
mini grid fund
impact investing
MRV tracker
blended finance
DFI programme
excel finance model
africa energy
```

**Description**
```
Allocate results-based financing and grants across an energy-access project pipeline, transparently and with live constraints.

BUILT FOR
Fund managers, programme teams, DFIs, foundations and consultants who run or design RBF and grant windows for mini-grids and energy access.

WHAT IT DOES
- Fund set-up: size, management and TA costs, over-commitment, per-project and per-country limits
- Fund profiles: RBF rate by customer type, CAPEX grant share, caps, RBF tranches (3 generic profiles + Custom)
- Eligibility screening: 8 switchable criteria with the rejection reason for each project
- Scoring: cost-effectiveness, leverage, productive use, climate, readiness, track record, risk, additionality (request vs viability gap)
- Allocation in rank order within the envelope and country limits, partial funding on/off, binding constraint shown
- Disbursements by year: grants at commissioning, RBF by tranche as connections are verified, delivery haircut by risk rating, fund cash position
- MRV Tracker: verified connections vs targets, RBF earned and outstanding, On track / Behind / Off track
- Portfolio dashboard: connections, people, CO2, private capital mobilised, leverage, cost per connection/person/tCO2, concentration, verdicts
- 12 automatic integrity checks; up to 25 projects; 10-year fund horizon

WORKS WITH THE DEVELOPER EDITION
Paste each project's CAPEX, viability gap and CO2 from our Developer Edition to test additionality, meaning whether the fund pays more than the project needs.

WHAT IT IS NOT
Not a replacement for an investment committee, due diligence or legal documentation. No FX and no reflows. The example fund, countries and projects are fictitious.

FORMAT
.xlsx, no macros, unlocked, English and French versions included, with a 15-page PDF user manual in each language. Excel 2010 or later. Instant digital download.

LICENCE
Single user or single organisation. No resale.
```

## GUMROAD
**Name:** Energy Access Fund Manager Model (RBF & Portfolio Edition)
**Summary:** From funding to impact: screen, score and allocate RBF and grants across your energy-access pipeline.
**Tiers (suggestion):** Model EN+FR $249 · Model + configuration to your fund's published rules (service, price on request; offer it only if you can deliver it).
