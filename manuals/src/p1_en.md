## 1. Purpose of the calculator {#purpose}

The calculator assesses, at pre-feasibility stage, the economics of a hybrid solar PV, battery and diesel mini-grid built for rural electrification. It answers three questions that a developer, a funder and a lender ask in turn:

1. Does the project cover its costs from tariff revenue alone?
2. Can it carry senior debt while meeting a minimum DSCR?
3. How much subsidy, as an upfront capital grant or as results-based financing (RBF), does it need to reach the chosen hurdle rate?

The third question matters most in practice. In most energy-access projects, the tariff that households can pay does not cover the full cost of the kWh delivered. The calculator quantifies that shortfall as a viability gap, then checks whether the planned subsidies close it.

### What the tool is not

It is not a design tool. The automatic sizing relies on ratios and does not replace an hourly simulation (HOMER Pro or equivalent) or a site load study. It is not a full project-finance model either: it does not cover foreign exchange, VAT, working capital or financial statements. Chapter 9 sets out these limits.

### Intended users

Mini-grid developers at identification or application stage, consultants preparing a pre-feasibility study, programme teams testing the order of magnitude of a subsidy, students and analysts in energy finance.

## 2. Getting started {#getting-started}

### Requirements

The file is an .xlsx workbook with no macros. It works in Excel 2010 and later versions and opens in LibreOffice Calc. No sheet is protected, so any cell can be changed, including by mistake. Keep a clean copy before you start.

### Colour conventions

| Appearance | Meaning | Rule |
|---|---|---|
| Blue text on yellow fill | Input entered by the user | Edit |
| Black text | Formula | Do not overwrite |
| Green text | Link to another sheet | Do not overwrite |

All amounts use a single currency, whose name is entered in "Currency label". The label converts nothing: if you work in CFA francs, every monetary input must be in CFA francs.

### Suggested sequence

1. Enter the project and general financial parameters (section 1 of the "Inputs" sheet).
2. Enter the customer segments, then the connection ramp-up.
3. Check the proposed sizing and override it if you have a design.
4. Enter unit capital and operating costs.
5. Describe the financing structure: upfront grant, RBF, debt.
6. Read the "Dashboard", then confirm that the "Checks" sheet shows "ALL OK".
7. Test how well the result holds with the scenario levers.

## 3. Workbook structure {#structure}

| Sheet | Content | Input |
|---|---|---|
| "Start Here" | Short guide, simplifications, disclaimer | No |
| "Inputs" | All assumptions, sizing and levers | Yes |
| "Dashboard" | Indicators, viability gap, verdicts, charts | No |
| "Cash Flow" | 20-year annual engine | No |
| "Checks" | Integrity checks | No |

The engine works in annual steps. Year 0 is construction; years 1 to 20 are operations. In the "Cash Flow" sheet, column B shows either a total or an NPV at the hurdle rate. Rows of the second kind are marked [B = NPV].

## 4. Entering the inputs {#inputs}

### 4.1 Project and financial parameters

| Parameter | Role in the calculation | Guidance |
|---|---|---|
| "Project life" | Limits the operating cash flows | 20 years at most. Align with the licence or concession term |
| "Discount rate / hurdle rate (project)" | Discounts cash flows for NPV, LCOE and the viability gap | Nominal rate, consistent with escalation. Use the target cost of capital or the programme's reference rate |
| "Target equity IRR" | Used for the equity verdict | Return expected by shareholders, in nominal terms |
| "Minimum DSCR required by lender" | Covenant threshold | Use the value in the lender's letter of intent or term sheet |
| "Tariff escalation" | Moves the tariff each year | Stay within what the regulator or contract allows |
| "Cost escalation (OPEX, fuel)" | Moves operating costs and battery replacement cost | Local inflation or contractual indexation |
| "Corporate tax rate" | Tax on positive profit | Adjust the rate to reflect any tax holiday |
| "Tax depreciation period" | Straight-line depreciation of total CAPEX | Period accepted by the tax authority |

> The hurdle rate and escalation must be on the same basis. A 10% nominal rate with 3% escalation corresponds to a real rate of about 6.8%. Mixing a real rate with nominal cash flows distorts NPV and LCOE.

### 4.2 Scenario levers

The four multipliers in section 2 apply to tariff, consumption, CAPEX and OPEX. A value of 1.00 reproduces the inputs as entered. A demand multiplier of 0.85 simulates consumption 15% below forecast, with the system unchanged. Use them for a quick stress test before changing the inputs themselves.

### 4.3 Customers and demand

The table in section 3 takes five segments: households, productive users, commercial customers, institutions and one free segment. For each, enter the number of customers, monthly consumption per customer, tariff per kWh and connection fee.

Prefer consumption figures from a demand survey or from metering data of comparable projects in the same area. A theoretical value built from an appliance list usually overstates demand in the first years, because it assumes equipment that households have not yet bought.

Three parameters complete the demand side:

* the connection ramp-up (share of customers connected in year 1, year 2, then year 3 onwards);
* the "Annual growth in consumption per customer", applied to all segments;
* the "Collection rate (share of bills actually paid)", which turns billed revenue into cash collected. With prepaid meters, energy is paid before it is used and the rate can be set at 100%. With post-paid billing, use the rate observed on comparable grids.

### 4.4 Technical design and sizing

The calculator sizes the system from energy sold in year 3, once all customers are connected:

| Component | Sizing rule |
|---|---|
| PV array | Design generation × target solar fraction × storage loss factor ÷ PV specific yield × oversizing factor |
| Battery storage | Daily generation × night-time share ÷ usable depth of discharge |
| Diesel generator | Average load × peak-to-average ratio |

The "PV specific yield" comes from PVGIS or the site design study. The "Target solar fraction (max share of generation from PV)" is the ceiling on solar coverage that the storage allows; above it, the diesel generator takes over.

The "Battery round-trip efficiency" is the ratio of energy discharged to energy stored. Solar energy used at night passes through the battery and loses that difference. The calculator derives the "Storage loss factor on solar energy", which raises the PV production required.

If you have a design, enter your values in the "Override" column. The "Used" column then takes your value instead of the automatic sizing.

### 4.5 CAPEX

Costs are entered as unit costs (per kWp, per kWh of storage, per kW of generator, per connection) and as a lump sum for the powerhouse, balance of system and civil works. "Development costs (studies, permits, community)" and "Contingency" are percentages of hard CAPEX.

Batteries are replaced every n years, n being the "Battery life". With the maintenance reserve option on, the replacement cost is smoothed through annual contributions in CFADS. This works like a maintenance reserve account and prevents a replacement year from pulling the DSCR down.

### 4.6 OPEX

Operating costs cover fixed O&M (as a percentage of hard CAPEX), local staff, insurance, licences and fees, diesel generator maintenance, fuel, and customer management including mobile money fees (as a percentage of revenue). Fuel is calculated from diesel energy, the "Diesel generator efficiency" and the "Diesel price at Year 1", then escalated.

### 4.7 Financing and subsidies

| Parameter | Effect |
|---|---|
| "Upfront CAPEX grant" | Received in year 0. Reduces the base for debt and equity |
| "RBF per new connection" | Paid for each new connection, in the year it is made or the following year depending on the verification lag |
| "Debt share of CAPEX net of grant" | Sets the senior debt amount |
| "Interest rate", "Loan tenor (incl. grace)", "Grace period (interest only)" | Repayment profile: interest only during the grace period, then level annuities |

Equity covers the rest of the financing plan. RBF is not a construction source: it arrives after commissioning and connection verification, so the developer has to bridge it.

### 4.8 Impact

The "CO2 emission factor of diesel" (2.68 kgCO2 per litre in the example) estimates emissions avoided compared with a fully diesel-based supply. Check the value required by your funder's methodology.

## 5. Reading the results {#results}

### 5.1 Project economics

| Indicator | Reading |
|---|---|
| "Project IRR - before subsidies" | Intrinsic return of the project, from its own revenue only |
| "Project IRR - after subsidies" | Return once the grant and RBF are included |
| "Project NPV @ hurdle - before subsidies" | Value created or destroyed at the hurdle rate. A negative value means the project needs subsidy |
| "LCOE (cost per kWh sold)" | Discounted lifecycle cost per kWh sold |
| "Levelized collected revenue per kWh" | Revenue actually collected, discounted on the same basis as LCOE |

Always compare LCOE with levelized collected revenue rather than with the year 1 tariff. Both are discounted the same way and both reflect escalation and the collection rate.

### 5.2 Financing and bankability

DSCR is the ratio of CFADS to debt service for the year. The dashboard shows the minimum and the average over the loan life. The "Equity payback (years)" is the first year in which cumulative equity cash flow turns positive.

### 5.3 Viability gap and verdicts

The viability gap is the upfront subsidy, in present-value terms, that brings the pre-subsidy project NPV to zero. The dashboard compares it with the present value of planned subsidies (upfront grant plus RBF). The "Remaining funding gap after planned subsidies" shows what is still missing.

Five verdicts summarise the position: commercial viability without subsidy, viability after subsidies, debt covenant, equity IRR, and LCOE coverage by the collected tariff. A YES appears in green, a NO in red with its cause.

> RBF received in years 1 to 3 is worth less than a grant of the same amount paid in year 0, because it is discounted. To close a given gap, the nominal RBF amount must therefore exceed the gap expressed in present value.

## 6. Calculation method {#method}

### 6.1 Sequence

Connections, then energy sold, required generation, solar and diesel split, revenue, costs, EBITDA, tax, project cash flow, debt service, CFADS, DSCR and equity cash flow.

### 6.2 Main formulas

Gross generation = energy sold ÷ (1 − distribution and conversion losses)
{: .formula}

Solar delivered = MIN(available PV energy ÷ storage loss factor ; gross generation × target solar fraction). Diesel = gross generation − solar delivered
{: .formula}

Storage loss factor = 1 + night-time share × (1 ÷ round-trip efficiency − 1)
{: .formula}

Project cash flow before subsidies = − CAPEX + EBITDA − battery replacements − unlevered tax
{: .formula}

CFADS = EBITDA − maintenance reserve contribution (or replacement) − tax after interest + RBF received
{: .formula}

LCOE = PV(CAPEX + OPEX excluding customer management + replacements) ÷ PV(kWh sold)
{: .formula}

Viability gap = MAX(0 ; − NPV of project cash flow before subsidies)
{: .formula}

Tax is a flat rate on positive taxable profit, with no loss carry-forward. Grants and RBF are treated as non-taxable. LCOE excludes customer management costs, which are proportional to revenue, to avoid a circular link with the tariff.

## 7. Worked example {#example}

The workbook ships with a fictitious village of 970 customers (800 households, 60 productive users, 100 commercial customers and 10 institutions). Values are illustrative and are not market benchmarks.

| Item | Value |
|---|---|
| Sizing used | 367 kWp PV, 780 kWh storage, 145 kW diesel generator |
| Total CAPEX | USD 1,336,072, or USD 1,377 per connection |
| NPV before subsidies at 10% | negative, USD 879,325 |
| Viability gap | USD 879,325, or USD 907 per connection |
| Planned subsidies | USD 680,000 upfront grant and USD 250 RBF per connection, worth USD 889,705 in present value |
| NPV after subsidies | positive, USD 10,381 |
| Project IRR after subsidies | 10.3% |
| Minimum DSCR | 1.55x against a 1.30x covenant |
| Equity IRR | 8.0% against a 15% target |
| LCOE and levelized collected revenue | USD 0.632 and USD 0.438 per kWh |

Reading: without subsidy the project destroys value, which is expected for a rural mini-grid with a moderate tariff. The planned subsidies just close the gap at project level, and the debt is serviced with a comfortable margin. Equity IRR, however, stays well below target, so a private shareholder would not finance the project as it stands. The options are a larger RBF, a concessional debt tranche, or a tariff closer to cost where customers can afford it.

## 8. Integrity checks and troubleshooting {#checks}

| Check | Likely cause of an alert | Action |
|---|---|---|
| "Sources = uses at Year 0 (grant + debt + equity = CAPEX)" | Inconsistent financing inputs | Check the debt share and the grant |
| "Debt fully repaid by end of tenor" | Inconsistent tenor or grace period | Grace must be shorter than tenor |
| "Tenor within project life" | Loan longer than the project | Shorten the loan |
| "Maintenance reserve contributions = replacements (when reserve used)" | Battery life inconsistent with project life | Check battery life |
| "Energy balance: solar + diesel = generation" | A formula was overwritten in the engine | Restore it from a clean copy |
| "At least one customer entered" | Empty segment table | Enter at least one segment |

"ALL OK" must appear in the "Checks" sheet and at the top of the "Dashboard" before you use any result.

## 9. Limits of use {#limits}

The points below come from a critical review of the model. They are not hidden defects but deliberate simplifications, which you should know before presenting a result to a committee.

1. Annual time step. The solar and diesel split does not come from an hourly simulation but from a solar fraction ceiling. For an investment file, confirm the split with a simulation.
2. Fixed capacity. PV and battery are not extended over time. If consumption grows strongly, the diesel generator covers the difference and fuel cost rises. Cap growth or add an expansion through additional CAPEX.
3. Fractional connections. Ramp-up is applied as a percentage, so a year's connection count can be non-integer. This does not affect orders of magnitude.
4. Simplified tax. No loss carry-forward, depreciation on total CAPEX (including the subsidised part), non-taxable subsidies. Under some tax regimes the depreciable base must be reduced by grants.
5. IRR with changing signs. Battery replacements can create negative cash flows mid-life, which makes IRR unreliable. Base the decision on NPV and the viability gap.
6. Single loan. One senior loan with annuity repayment. No debt service reserve account, fees or sculpted profile.
7. Single currency. No foreign exchange risk, although debt is often in hard currency while revenue is in local currency.

## 10. Glossary {#glossary}

| Term | Definition |
|---|---|
| CAPEX | Initial capital expenditure |
| OPEX | Annual operating expenditure |
| EBITDA | Revenue less OPEX |
| CFADS | Cash flow available for debt service |
| DSCR | Debt service coverage ratio: CFADS divided by debt service for the year |
| NPV | Net present value at the hurdle rate |
| IRR | Internal rate of return |
| LCOE | Levelized cost of electricity over the lifecycle, per kWh sold |
| RBF | Results-based financing, paid after a result is verified, here a connection |
| Viability gap | Present-value subsidy that brings pre-subsidy NPV to zero |
| Solar fraction | Share of generation supplied by PV |
| Specific yield | Energy produced per installed kWp per year |
| Depth of discharge | Share of nominal battery capacity that can actually be used |
| Round-trip efficiency | Ratio of energy discharged by the battery to energy stored |

## 11. Disclaimer and licence {#licence}

The calculator is a screening and pre-feasibility tool for educational and planning use. It is not investment, legal, tax or engineering advice. Results depend entirely on the inputs entered. Independent technical and financial due diligence is required before any investment decision.

Example data are fictitious and do not describe any existing project, developer or programme.

The licence covers one user or one organisation. Resale, redistribution and publication of the file or of this manual are not permitted.
