# About this manual

This is MANUAL 2, the user manual of MODEL 2, the *PAYGo Company Financial and Investment Model* (file `AEF_SHS_PAYGo_Model_v0.8-dev.xlsx`). MODEL 2 is the companion workbook to Book 2, *PAYGo Solar Finance*, in the Africa Energy Finance collection, Business & Financial Models. The manual is written for four audiences, and each will want to enter the document at a different point.

| Reader | The question they bring | Where to start |
|---|---|---|
| PAYGo developer or CFO | Can the business plan be financed, and how much equity does it need? | Steps 2 to 9 |
| Lender | Is the receivables book acceptable collateral, and will the covenants hold? | Steps 8 and 11 |
| Equity investor | What is the company worth, and what return is realistic? | Steps 10 and 12 |
| Investment committee | Does the plan pass its tests, is the evidence file complete enough for a decision, and on what conditions? | Step 12 and the readiness gates |

Part A describes how the workbook is built. Part B walks through a twelve step workflow; for each step it gives the sheets involved, the inputs to set, the outputs to read, the mistakes we see most often and the way an experienced analyst would read the result. Part C is the methodology reference, including every simplification a reviewer should know about.

> **Edition note.** This edition describes each sheet by its layout and row labels. Screen captures will be added in a later edition, once the workbook has completed its test cycle in Microsoft Excel.

> **Status of the default inputs.** The default inputs describe a fictional company in a fictional market. They are placeholders chosen to make the mechanics visible, not benchmarks, and each carries the provenance label MODEL ASSUMPTION (one is UNVERIFIED). No result should be quoted as a view on a real company until real company data have been loaded and labelled and the workbook has been independently validated. The *Investment_Readiness* sheet records how complete the evidence file is for a given case.

## Scope of the model

The workbook is a monthly, five year, integrated three statement model of a PAYGo solar company that sells five product tiers on credit. Around that core sit a cohort (vintage) credit engine, a lender toolkit (borrowing base, portfolio covenants, debt service cover), an investor toolkit (discounted cash flow, exit valuation, IRR and multiple on invested capital), an outcome based RBF engine with its claim cycle, an FX exposure view, a consumer risk layer, a sheet for company-reported PAYGo PERFORM 2026 KPIs and a graded database of published figures on PAYGo companies.

The credit loss, staging and revenue treatments are analytical. This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS. The workbook does not compute tax under any specific code, and it does not replace legal or regulatory advice. Probability of default, loss given default and expected credit loss are reported as indicative proxies throughout. Part C lists each simplification.

## Version and status

| Item | Value |
|---|---|
| Model version | v0.8 (development build); the file name stays `v0.8-dev` until the Excel test is complete |
| Size | 47 sheets, about 100,900 formulas, no macros, no external links |
| Integrity | Master check OK on 38 tests; no circular references. Outputs agree with a secondary calculation of the full model to rounding precision, with an independent formula engine, and with a full recalculation in LibreOffice. The test in Microsoft Excel is pending |
| Projections | Identical to v0.7: at default inputs, Base investor IRR 46.4% and MOIC 6.72x |
| Readiness at default inputs | 2 of 23 gates met (2 of 13 critical). Decision: STOP (failed test: gate 10, covenant breach, because the annual DSCR is below 1.2x in Years 1 to 4) |

# Part A. Model architecture

## Calculation chain

Calculation runs in one direction:

Inputs → Products → Sales → Customers → PAYGo receivables → Credit engine → Vintage engine → Collections and recoveries → RBF engine → Working capital → Financing → Financial statements → Covenants → Valuation → Investor returns → Market benchmark → Calibration → Investment readiness.

No output sheet feeds back into a calculation. Interest accrues on opening balances, and the receivables facility is sized on cash before the facility, so the workbook has no circular references and never needs iterative calculation.

## Sheet map

| Layer | Sheets | Purpose |
|---|---|---|
| Front | Cover, Start, Contents, Investment_Summary, Investment_Readiness | Title page and model status, start page, sheet index, one page summary, 23 evidence based readiness gates and the decision rule |
| Inputs | Inputs, Products, Scenarios, Credit_Assumptions, Consumer_Risk | All hard coded assumptions, each with a provenance label (together with the three company data templates) |
| Outputs | Dashboard, KPIs, Credit_Portfolio, Vintage_Dashboard, PERFORM_2026, Covenants, Valuation, FX_Exposure, Unit_Economics, Sensitivity | Results; nothing to type here except section C of PERFORM_2026 |
| Benchmark | Benchmark_Compare, Benchmark_KPIs, Market_Benchmark, Calibration, Company_Cases, Source_Register, Benchmark_Matrix, Benchmark_DB | External evidence, its grade and status, and diagnostics |
| Statements | Annual, FS | Annual and monthly income statement, balance sheet and cash flow |
| Engines | Ops, RBF_Engine, Credit_Engine, Vintage_Engine, Costs, Financing, Curves, Cohort_T1 to Cohort_T5, Timeline | Calculations |
| Data templates | Credit_Input, Vintage_Input, PERFORM_2026 (section C) | Company portfolio, cohort and PERFORM data (ACTUAL) |
| Control | Glossary, Checks | Definitions, integrity checks and readiness flags |

### Tab order

The *Contents* sheet numbers the 47 sheets in tab order, with a hyperlink and a one line description for each:

| # | Sheet | # | Sheet | # | Sheet |
|---|---|---|---|---|---|
| 01 | Cover | 17 | Valuation | 33 | Credit_Engine |
| 02 | Start | 18 | FX_Exposure | 34 | Vintage_Engine |
| 03 | Contents | 19 | Unit_Economics | 35 | Costs |
| 04 | Investment_Summary | 20 | Sensitivity | 36 | Financing |
| 05 | Investment_Readiness | 21 | Benchmark_Compare | 37 | Curves |
| 06 | Inputs | 22 | Benchmark_KPIs | 38 | Cohort_T1 |
| 07 | Products | 23 | Market_Benchmark | 39 | Cohort_T2 |
| 08 | Scenarios | 24 | Calibration | 40 | Cohort_T3 |
| 09 | Credit_Assumptions | 25 | Company_Cases | 41 | Cohort_T4 |
| 10 | Consumer_Risk | 26 | Source_Register | 42 | Cohort_T5 |
| 11 | Dashboard | 27 | Benchmark_Matrix | 43 | Credit_Input |
| 12 | KPIs | 28 | Benchmark_DB | 44 | Vintage_Input |
| 13 | Credit_Portfolio | 29 | Annual | 45 | Timeline |
| 14 | Vintage_Dashboard | 30 | FS | 46 | Glossary |
| 15 | PERFORM_2026 | 31 | Ops | 47 | Checks |
| 16 | Covenants | 32 | RBF_Engine | | |

Every page of the workbook carries a printed footer with the sheet name and page number, so a printed pack can be referenced by sheet and page.

### New sheets and blocks in v0.8

**Start** (sheet 02). The first page to read. A status block shows the master check, the active case, the credit data mode and the readiness decision. Five sections follow: (1) what to input, sheet by sheet, with the ACTUAL templates marked; (2) what the model calculates; (3) what the results mean, read before quoting any number (revenue is not cash; the operational collection rate is not the PAYGo PERFORM Repayment Rate; ECL, PD and staging are analytical proxies; every input is labelled; the readiness decision measures the evidence file); (4) what an investor should look at, in order; (5) the count of inputs under each provenance label.

**PERFORM_2026** (sheet 15). PAYGo PERFORM KPIs under the GOGLA Technical Guide of June 2026. Section A reports the five KPIs by tier and portfolio from company data: Repayment Rate paid vs plan (RR PvP) to date, RR paid vs financed (PvFin) to date, RR PvP at 90 days, RR PvP at 2x contract term and the Ownership Rate at 2x contract term (OR @2x). Portfolio values sum numerators and denominators; a blank reads "not provided". It also counts cohorts, contracts and cohorts with fewer than 100 contracts. Section B shows labelled approximations from the *Vintage_Input* checkpoints (cohort repayment ratio at about 90 days and at 2x term, ownership at 2x), which are not PERFORM KPIs and read "not available: proxy data only" without actual cohorts. Section C is the input template (see Step 11).

**FX_Exposure** (sheet 18). Section A is a currency map: where each item sits (revenue, collections, receivables, hardware, operating costs, RBF, USD term loan, facility, equity) and how the model treats it, with Year 5 amounts; hedging reads "None" because no forward, swap or option is modelled. Section B gives, by year for the active scenario: the depreciation path, year end FX rate, pass through, share of debt in USD; transaction effects on cash (USD hardware, USD interest, USD principal, USD RBF) and their net; the unrealised remeasurement loss on USD debt (non cash); translation of revenue and EBITDA into USD; and a memo of hardware revenue added by price pass through. Monthly detail sits on *Timeline*.

**RBF claim cycle** (block on *RBF_Engine*, rows 62 to 70). Five rows by month: eligible units sold, claims submitted at sale (USD), claims reaching verification after the lag, amounts disbursed under the selected design (equal to RBF income in the statements), and the cumulative RBF working capital gap (claimed but not yet received), in USD and at the month's FX in local currency. The company finances that gap until disbursement. RBF is cash from the programme, never a customer payment.

**Investment_Readiness evidence columns and decision rule.** For each of the 23 gates the sheet now shows the evidence required, whether the gate is critical (13 are), where the evidence is held, who signed it off, the date and an evidence check. The decision rule below the gates is described in Step 12.

**Dashboard metric table.** The Dashboard is now a table of 39 labelled metrics by year, each with its unit and its source sheet, rounded for reading (full precision stays on the source sheets), with the charts beside it. Groups: scale and customers; profitability; cash and portfolio (including the operational collection rate, not a PERFORM KPI, and the company-reported RR PvP, which reads "not provided" until section C of *PERFORM_2026* is filled); funding; returns and timing; FX and readiness.

**Sensitivity LIVE row.** The static table is dated and stated as recomputed in the workbook for every case before release. Below it, a LIVE row shows the active case with the current inputs and updates with every change (Step 10).

**Scenario architecture and input set selector** (*Scenarios*, rows 13 and 18 to 26). Row 13 holds a selector for the input set loaded on *Inputs*, *Products* and *Credit_Assumptions*: Illustrative (model assumptions), Management case or Calibrated case. With the scenario name it forms the active case label shown on Start, Dashboard, Cover and the LIVE row. Rows 18 to 26 list six layers, each with its type, where it lives and its status in the workbook: Actual history (ACTUAL), Management case (ASSUMPTION), Calibrated case (ASSUMPTION, calibrated), Base, Downside and Severe stress (FORECAST). The Actual row reads "Loaded" with a record count once company data are entered, and "Not loaded" otherwise.

**Provenance columns.** Every input carries a provenance label: column E on *Inputs*, the Provenance column (column I) on *Products*, column E on *Credit_Assumptions* and column I on the *Scenarios* levers.

**Company history block on Credit_Portfolio** (rows 34 to 41). Months of history loaded in *Credit_Input* and the operational collection rate for history months 1 to 12, 13 to 24, 25 to 36 and the latest 12 months, independent of the selected data mode; "n/a" when the history is shorter.

## Conventions

| Convention | Meaning |
|---|---|
| Blue font | Hard coded input. These are the only cells a user should change. |
| Blue font on yellow | Key assumption. Review these first. |
| Black font | Formula. Never overwrite. |
| Green font | Link from another sheet. |
| Cream shading | Data entry templates (Credit_Input, Vintage_Input, PERFORM_2026 section C). |
| Provenance label | Drop down next to every input: MODEL ASSUMPTION, COMPANY DATA, EXTERNAL EVIDENCE, CALIBRATED ASSUMPTION or UNVERIFIED. |
| Type tag | The subtitle of each input, output and engine sheet opens with its type in brackets: [ASSUMPTION], [FORECAST] or [ACTUAL], or a combination where a sheet mixes them. |
| Monthly sheets | Column A label, B unit, C total or closing value, D opening balance, E onwards months 1 to 60. |
| Currency | The model currency is the local currency, labelled on *Inputs*. Hardware, RBF and the term loan are denominated in USD and translated along the FX path on *Timeline*; *FX_Exposure* isolates the effects. |
| Signs | Revenue and assets positive; costs negative on the statements; percentages stored as fractions. |

### Provenance labels

| Label | Meaning (Glossary) |
|---|---|
| MODEL ASSUMPTION | Set by the modeller |
| COMPANY DATA | Supplied by the company |
| EXTERNAL EVIDENCE | From a VERIFIED source in *Source_Register* |
| CALIBRATED ASSUMPTION | Re-estimated from company data or verified evidence |
| UNVERIFIED | Source not yet read |

**How to change a label.** When you replace a value, select the provenance cell on the same row and choose the new label from the drop down list, for example from MODEL ASSUMPTION to COMPANY DATA when the figure comes from the company's management accounts. The cells accept only the five values above. *Start* (section 5) counts the inputs under each label; at default inputs it reads 100 MODEL ASSUMPTION and 1 UNVERIFIED (the MTF tier labels on *Products*). A label describes where a value comes from; it does not make the value right.

### ACTUAL, ASSUMPTION and FORECAST

ACTUAL is company history on the input templates (*Credit_Input*, *Vintage_Input*, *PERFORM_2026* section C) and is never changed by scenario levers. ASSUMPTION is the input set. FORECAST is everything computed from the inputs under the active scenario. *Credit_Portfolio* and *Credit_Engine* are FORECAST or ACTUAL depending on the credit data mode; *Vintage_Dashboard* and *Vintage_Engine* combine ACTUAL cohorts and FORECAST proxy cohorts.

## Integrity controls

The *Checks* sheet runs 38 integrity tests. Each returns 0 when it passes, and they roll up into a master check (*Checks* cell C44) displayed on the Cover, Start, Contents, the Dashboard and the Investment summary.

| # | Test |
|---|---|
| 1 | Balance sheet balances (maximum absolute difference, all months) |
| 2 | Sales mix sums to 100% |
| 3 | Closing cash never below minimum cash |
| 4 | Gross receivables never negative |
| 5 | Loss allowance never positive (contra asset) |
| 6 | Facility within limit |
| 7 | Cash flow reconciles to balance sheet cash every month (opening cash plus net cash flow equals closing cash) |
| 8 | Tenors within curve horizon (at most 60 months) |
| 9 | Down payment not above cash price |
| 10 | Scenario selector valid (1 to 3) |
| 11 | Investor ticket within initial equity |
| 12 | Terminal growth below discount rate |
| 13 | Credit data mode valid (1 or 2) |
| 14 | Proxy DPD buckets reconcile to gross receivables (all tiers, all months) |
| 15 | Actual DPD buckets reconcile to gross receivables (Actual mode only) |
| 16 | Indicative ECL not negative |
| 17 | Facility drawn within borrowing base and limit |
| 18 | Proxy shares of receivables at risk sum to 100% |
| 19 | Hybrid RBF weights sum to 100% |
| 20 | RBF mode valid (1 to 4) |
| 21 | Stage thresholds ordered (Stage 2 below Stage 3, Stage 3 at most the default definition) |
| 22 | Financing structure valid (1 or 2) |
| 23 | PERFORM horizon equals 2 x tenor for every tier |
| 24 | Vintage cohort modes valid (1 or 2) |
| 25 | Receivables roll forward every month (opening plus originations and financing income, less collections and write offs, equals closing; Ops equals FS) |
| 26 | Loss allowance roll forward (opening, less ECL charged, plus amounts written off, equals closing) |
| 27 | USD term loan roll forward in USD and in local currency (translation at month end FX; FS equals Financing) |
| 28 | Receivables facility roll forward (opening plus net drawdown equals closing; FS equals Financing) |
| 29 | Equity roll forward (opening plus net income plus equity injected equals closing; no dividends) |
| 30 | Cohort totals equal portfolio totals (cohort sizes equal units sold; tier rows sum to totals for collections, instalments due, receivables) |
| 31 | Vintage engine carries cohort units from Vintage_Input (all tiers) |
| 32 | Vintage_Input: cumulative collections never fall between checkpoints |
| 33 | Vintage_Input: cumulative instalments due never fall between checkpoints |
| 34 | RBF: statements equal the engine's selected design, RBF not negative, cumulative disbursements never above cumulative claims (RBF is never part of customer collections, which come from the cohorts only) |
| 35 | Valuation reconciles to the statements (EBITDA, tax, capex, Year 5 working capital) |
| 36 | Scenario levers in use equal the selected scenario column (no overwritten lever) |
| 37 | PERFORM_2026 inputs: no negative values, numerators within denominators (RR PvP, at 90 days, at 2x; ownership) |
| 38 | No impossible negative balances (inventory, fixed assets, payables, active accounts, units, debt, cumulative equity) |

> **Rule.** Do not use any output while the master check reads ERROR. Open *Checks*, find the line showing 1 or a non zero difference, and correct the input that causes it (see *Troubleshooting* in Part C).

Seven readiness flags sit below the checks. They are kept outside the master check on purpose: they measure the maturity of the analysis, not the arithmetic.

| Readiness flag | Default value |
|---|---|
| Consumer affordability assumptions not yet reviewed | 1 |
| Tiers above the affordability threshold | 3 |
| Actual credit data horizon not supplied (Actual mode) | 0 |
| Ownership evidence switch set without ownership data | 0 |
| Credit and vintage analysis rely on proxy data only | 1 |
| PERFORM evidence marked Validated on Consumer_Risk without PERFORM_2026 results (tiers) | 0 |
| PERFORM_2026 cohorts with fewer than 100 contracts | 0 |

# Part B. Using the model in twelve steps

## Step 1. Start here

**Sheets:** Cover, Start, Contents, Checks, Inputs (top section).

1. Open the workbook in Excel 2016 or later; Microsoft 365 is recommended. The file is set to recalculate fully when it opens, so let the calculation finish before reading anything.
2. On the Cover or *Start*, confirm that the master check reads OK, and note the active case, the credit data mode and the readiness decision.
3. Read *Start* from top to bottom: what to input, what the model calculates, what the results mean, what an investor should look at, and the provenance counts. *Contents* holds the operating guide, the numbered sheet index in tab order with hyperlinks and the colour code.
4. Save a working copy under a new name before you change anything, for example `CompanyName_Model_v0.8-dev_2026-10-15.xlsx`, and keep the original as a reference.
5. On *Inputs*, set the local currency label and the first model month. On *Scenarios* row 13, choose the input set you are about to load (Management case when you enter the company's plan).

The inputs at this step are the scenario selector (1 Base, 2 Downside, 3 Severe), the input set selector, the first model month and the currency label. The outputs are the master check, the active case label and the readiness decision.

**Common mistakes.** Users work in the original file rather than a copy; paste values over black formula cells (if in doubt, undo and paste into blue cells only); leave the selector on Downside and then read the results as if they were Base; or load the company's plan without changing the input set selector and the provenance labels, so the workbook still describes it as illustrative. The Cover, *Start*, the Dashboard and the Investment summary always show the active case.

**Reading the result.** A master check of OK means the arithmetic is internally consistent. It says nothing about whether the assumptions are realistic; Steps 10 to 12 deal with that.

## Step 2. Define the business

**Sheets:** Products (specification block), Consumer_Risk.

The model carries five product tiers, labelled by the capacity attribute of the ESMAP Multi Tier Framework:

| Tier | Default product | PV and storage | Default tenor | Segment |
|---|---|---|---|---|
| 1 | Pico solar kit | 10 Wp, 40 Wh | 12 months | Rural, first time PAYGo customers |
| 2 | Solar home system with TV | 80 Wp, 300 Wh | 24 months | Rural and peri urban households |
| 3 | Large SHS with DC fridge | 300 Wp, 1.5 kWh | 30 months | Peri urban households, kiosks |
| 4 | Solar inverter with lithium battery | about 1.2 kWp, 5 kWh | 36 months | Urban households and small businesses on a weak grid |
| 5 | Solar inverter with lithium battery | about 3 kWp, 10 kWh | 48 months | Upper income households, SMEs, productive use |

1. Replace the product names, PV size, storage, loads and target segments with the company's own catalogue, and change the provenance label of each row you replace to COMPANY DATA. Keep all five columns; a company that sells fewer tiers sets the sales mix of the unused tier to 0%.
2. Check each tier label against the product's actual capacity. The label refers to the capacity attribute only; a full Multi Tier Framework assessment also covers duration, reliability, quality, affordability, legality, and health and safety. The tier label row is marked UNVERIFIED because the framework report has not yet been read (Source_Register E3).
3. On *Consumer_Risk*, replace the illustrative household incomes with survey or customer data, set the maximum payment burden from the credit policy, and record the evidence status (Not provided, Provided, Validated) for PAYGo PERFORM reporting and for consumer protection.

The sheet returns, by tier, the payment burden (instalment as a share of income), the down payment as a share of income, the implied consumer APR and an affordability flag. The default maximum burden of 10% is the model's policy threshold, not a standard.

**Common mistakes.** Leaving the illustrative incomes in place (a readiness flag stays raised until "affordability reviewed" is set to 1); labelling a product one tier above what its capacity supports; and marking PERFORM evidence Validated before company results are entered on *PERFORM_2026*, which raises a readiness flag and keeps gate 20 open.

**Reading the result.** Affordability is a credit risk before it is a social one. A high payment burden is an early predictor of default and can disqualify a portfolio from RBF programmes. The implied APR is the figure a regulator or a journalist will compute, and management should know it first.

## Step 3. Enter market assumptions

**Sheets:** Inputs (macro block), Scenarios, FX_Exposure.

| Input | Default | What it drives |
|---|---|---|
| Opening FX rate (local currency per USD) | 130 | Local cost of USD hardware, RBF receipts and term debt |
| Depreciation of the local currency against the USD (Scenarios) | 5% Base, 12% Downside, 25% Severe, per year | FX path on *Timeline* |
| Local inflation | 6% | Indexation of operating and per unit costs |
| Annual price increase on new contracts | 5% | Price index of new cohorts |
| Pass through of FX depreciation into new contract prices | 50% | Share of the currency move recovered from new customers |
| Corporate tax rate | 30% | Tax, with unlimited loss carry forward |

**Common mistakes.** Setting depreciation to zero because the currency has been stable. A PAYGo company buys hardware and borrows in USD while it collects in local currency, and depreciation is the most damaging single lever in the default sensitivity table. A second error is to assume full pass through without evidence that customers can absorb it; higher prices feed straight back into affordability (Step 2).

**Reading the result.** Compare two rows of the *Sensitivity* sheet. At default inputs, local currency depreciation of 20% a year turns a Base investor IRR of 46.4% into a loss (IRR of (16.0%)), and freezing prices on new contracts cuts it to 7.9%. Pricing power is a valuation driver in this sector, not a detail of the commercial plan. *FX_Exposure* shows where the effect comes from: in Base at default inputs the net transaction effect on costs and RBF reaches LCY (928)m in Year 5, partly offset by LCY 877m of hardware revenue added by price pass through on new contracts.

## Step 4. Build demand

**Sheets:** Inputs (sales volume), Products (sales mix), Scenarios (volume multiplier).

1. Enter total units sold across all tiers for Years 1 to 5.
2. Set the sales mix by tier on *Products*. It must total 100%, and a check enforces this.
3. Leave the volume multiplier at 1.00 for Base. Downside and Severe apply 0.90 and 0.75 by default.

Monthly sales equal the annual total divided by twelve, multiplied by the scenario volume multiplier and split by mix. The model does not represent seasonality.

The results appear on *Ops* (units by tier and month), on *KPIs* (units sold, active accounts, unlocked accounts) and in the scale block of the *Dashboard*.

**Common mistakes.** Growing volumes faster than the agent and installer network, and the working capital line, can carry; the funding requirement in Step 8 will show it. The other frequent error is shifting the mix towards Tiers 4 and 5 because it lifts value, which it does sharply, without evidence that those customers repay as assumed.

**Reading the result.** Volume matters less than most plans assume. In the default sensitivity table, a 20% cut in volume lowers the investor IRR from 46.4% to 37.8%, whereas currency depreciation or weak pricing can eliminate it. Growth amplifies the unit economics the company already has, good or bad.

## Step 5. Build revenue

**Sheets:** Products (price plan), Inputs (RBF, other revenue), RBF_Engine.

The price plan for each tier has four inputs: cash price, down payment, daily rate and tenor. From these the model derives the monthly instalment (daily rate × 365 ÷ 12), the total contract value, the PAYGo premium over the cash price and the implied APR.

Revenue follows a simplified analytical treatment. Hardware revenue equals the cash price times units and is recognised at the date of sale. PAYGo financing income equals the premium divided by the tenor and is spread straight line over the tenor of each cohort. Other revenue (digital loans, add on services) is a net take rate per active account per month and is switched off by default. RBF and subsidy income sits below gross profit and is recognised when the cash is received. This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS.

The *RBF_Engine* sheet supports four programme designs:

| Mode | Payment basis | Data required |
|---|---|---|
| 1 Sales based | USD per verified unit sold, after a verification lag | Sales verification only |
| 2 Repayment linked | Sales based amount × (cohort repayment ratio at verification ÷ target), capped at 100%; the ratio comes from the model curve and is not a PERFORM KPI | Repayment data |
| 3 Ownership linked | Paid at twice the tenor on the share of customers who own their device | Validated ownership data at twice the tenor in *Vintage_Input*, with the evidence switch set to 1 |
| 4 Hybrid | Weighted combination of modes 1 to 3 | Weights totalling 100% |

Below the designs, the claim cycle block follows each claim from eligibility to disbursement and shows the cumulative working capital gap. At default inputs (sales based design) the eligible units over five years are 141,950, claims submitted USD 1.96m, claims verified and disbursed USD 1.67m, and USD 0.29m is claimed but not yet received at the end of the horizon (LCY 48.7m at the month's FX).

**Common mistakes.** Expecting the ownership linked design to pay out on proxy data. It pays zero by design until validated evidence exists, because the workbook will not manufacture that KPI. Treating RBF as a customer collection; it is programme cash, received with a lag, and the gap must be funded. Entering a monthly instalment in the daily rate field is the other recurring error.

**Reading the result.** The APR row is the company's consumer protection disclosure. Whether each price plan recovers acquisition and hardware cost is answered on *Unit_Economics* (Step 12). The *RBF dependency* row on the Dashboard and the "RBF programme off" row of *Sensitivity* (investor IRR 44.7% instead of 46.4%) show how much the case relies on subsidy.

## Step 6. Enter hardware and capital costs

**Sheets:** Products (cost to serve), Inputs (freight and duty, working capital, capex).

| Input | Level | Notes |
|---|---|---|
| Hardware FOB cost | USD per unit, by tier | Translated at the month's FX rate and scaled by the scenario hardware cost lever |
| Freight, duty and clearing | % of FOB | Applied to all tiers |
| Installation and last mile logistics | Local currency per unit | Part of cost of sales; indexed to inflation |
| Warranty and after sales | % of landed cost, by tier | Provision expensed at sale |
| Inventory cover | Months of hardware cost | Drives inventory and purchases |
| Supplier credit | Days | Drives trade payables |
| Fixed capex | Per month | Vehicles, IT, depots; depreciated straight line over the stated life |

**Common mistakes.** Entering a local currency hardware price converted at today's rate instead of the USD FOB cost, which double counts depreciation; and omitting installation for Tiers 4 and 5, where it is material.

**Reading the result.** The largest investment a PAYGo company makes is not in fixed assets but in its receivables book: each unit sold on credit ties up cash for the whole tenor. That is why capex looks small while the funding requirement looks large.

## Step 7. Enter operating costs

**Sheets:** Products (commission, marketing), Inputs (operating costs).

| Cost | Driver |
|---|---|
| Agent and installer commission | Per unit sold, by tier |
| Marketing and acquisition | Per unit sold, by tier |
| Mobile money and payment fees | % of cash collected (deposits and instalments) |
| Customer service and collections | Per active account per month |
| Staff | Fixed monthly amount, indexed to inflation |
| General and administrative, rent, IT, licences | Fixed monthly amount, indexed to inflation |

**Common mistakes.** Under sizing central costs for the volume plan; a book of 70,000 active accounts needs a collections team, a call centre and a data function. Commissions, for their part, are variable and scale with sales.

**Reading the result.** Commission plus marketing is the customer acquisition cost (CAC) reported on *Unit_Economics*. The ratio of lifetime value to CAC and the cash payback by tier show whether growth creates or destroys value.

## Step 8. Define the financing structure

**Sheets:** Inputs (financing, financing structure, covenants), Credit_Assumptions, Products (advance rates).

The model draws on four sources of funds:

1. Initial equity, paid in month 1.
2. A USD term loan, defined by amount, drawdown month, rate, grace period and amortisation. It is revalued at each month's FX rate, and the revaluation runs through the income statement as an unrealised FX gain or loss (shown separately on *FX_Exposure*).
3. A local currency receivables facility, structured either as a warehouse line (structure 1) or as a securitisation or term ABS (structure 2, with its own rate, an advance rate haircut and an upfront fee paid in the month after each drawing).
4. An automatic equity top up. Whenever cash would fall below the minimum balance, the model injects equity, and the cumulative top up is the funding requirement.

The facility is drawn only to hold cash at the minimum balance (a cash sweep), up to the lower of the facility limit and the borrowing base. The borrowing base is the sum, over tiers, of the advance rate times eligible receivables, and eligibility follows the maximum DPD rule on *Credit_Assumptions* (by default, receivables up to 30 days past due). When the borrowing base contracts, the facility is repaid.

| Credit assumption | Default |
|---|---|
| Default definition | 180 days past due |
| Stage 2 and Stage 3 thresholds | 30 and 90 days past due |
| Borrowing base maximum DPD | 30 days |
| Recovery cost | 15% of gross resale proceeds |
| Cure rate | 30% (indicative ECL only) |
| ECL discount rate | 20% |
| Proxy DPD distribution | 85% of paying account balances current, the remainder 1 to 30 DPD; receivables at risk split 25%, 20%, 25% and 30% across 31 to 60, 61 to 90, 91 to 180 and over 180 DPD |

**Common mistakes.** Treating the full facility limit as available, when the binding constraint is usually the borrowing base, which shrinks as credit quality deteriorates. Forgetting that the term loan is in USD, so depreciation raises both principal and interest in local currency. Reading the automatic top up as free money: it is equity the company must raise, and it dilutes existing shareholders.

**Reading the result.** The *Investment_Summary* reports the peak equity requirement in USD. At default inputs it is USD 10.0m in Base and about USD 46.6m in Severe. The Dashboard also shows the runway (months before the first equity top up; "No top-up in horizon" in Base). A plan that works only if the whole facility is available is, in substance, a bet on credit quality.

## Step 9. Review the financial statements

**Sheets:** FS (monthly), Annual.

Review the statements in this order:

1. The balance check row, which should read 0 in every month, and the master check.
2. The revenue mix between hardware, financing income and other revenue.
3. Credit losses. Expected credit loss is charged when each contract is originated (lifetime expected missed instalments from the scenario curve); recoveries on repossessed units are shown separately; missed instalments are written off as they fall due. This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS.
4. EBITDA and net income. Tax becomes payable only once accumulated losses have been absorbed.
5. Cash flow. Operating cash flow is normally negative while the book grows; the line *cash before equity top up* shows the true funding gap.
6. Balance sheet: net PAYGo receivables (gross less loss allowance), the term loan in local currency, the receivables facility and equity.

**Common mistakes.** Reading positive EBITDA as positive cash. In PAYGo, profit arrives before cash, because hardware revenue is recognised at sale and the cash comes in over the tenor (the Dashboard row "cash conversion: operating cash flow / EBITDA" makes this visible). Users also confuse three different credit figures: the loss allowance on the balance sheet, write offs of missed instalments, and the indicative stage based ECL on *Credit_Engine*, which is a diagnostic and is not booked.

**Reading the result.** A PAYGo company can report a profit and still run out of cash. The cash flow statement and the funding requirement are the figures to trust.

## Step 10. Run scenarios

**Sheets:** Scenarios, Inputs (selector), Sensitivity.

| Lever | Base | Downside | Severe |
|---|---|---|---|
| Default hazard multiplier | 1.00 | 1.30 | 1.75 |
| Collection rate multiplier (paying accounts) | 1.00 | 0.97 | 0.92 |
| Sales volume multiplier | 1.00 | 0.90 | 0.75 |
| Hardware cost multiplier (USD) | 1.00 | 1.05 | 1.10 |
| Local currency depreciation against the USD, per year | 5% | 12% | 25% |

The levers apply to the input set loaded (row 13 of *Scenarios*). They never reach company history: ACTUAL data on the input templates stay as entered whatever scenario is selected, and a check (test 36) confirms that the levers in use equal the selected column.

1. Switch the selector on *Inputs* between 1, 2 and 3 and read the *Investment_Summary* and the Dashboard each time.
2. Read the *Sensitivity* sheet. Its static table holds the three scenarios and twelve single lever cases away from Base. It was computed at default inputs on 3 October 2026 and recomputed inside the workbook for every case before release; it does not update when inputs change.
3. Read the LIVE row below the static table: it shows the active case with the current inputs (peak equity, Year 5 revenue, EBITDA margin and operational collection rate, DCF value, investor IRR and MOIC, covenant breach months) and updates with every change. At default inputs it equals the Base row.
4. For company specific sensitivities, change one input at a time, record the LIVE row, and restore the input before the next test.

At default inputs the three scenarios give the following results:

| Case | Peak equity (USD m) | Year 5 EBITDA margin | Investor IRR | Months in covenant breach |
|---|---|---|---|---|
| Base | 10.0 | 21.6% | 46.4% | 0 |
| Downside | 10.0 | 7.3% | (22.9%) | 44 |
| Severe | 46.6 | (18.4%) | None: total loss (the workbook shows "n/a: no sign change") | 48 |

**Common mistakes.** Presenting Base alone; building a Downside that moves one variable when real stress moves credit, currency and volume together; reading the static table as if it reflected the company's inputs (read the LIVE row); and saving the file with the selector away from 1.

**Reading the result.** An investment case is only as strong as its Downside. When the Downside calls for unplanned equity or breaches covenants for most of the horizon, the structure needs mitigants: price indexation, lower leverage, slower growth or tighter credit policy.

## Step 11. Test the lender case and load company data

**Sheets:** Credit_Portfolio, Credit_Engine, Covenants, Vintage_Dashboard, PERFORM_2026, Credit_Input, Vintage_Input.

**11a. The credit portfolio.** *Credit_Portfolio* consolidates all tiers. It shows gross receivables by DPD bucket and default exposure, the operational collection rate (not a PERFORM KPI), weighted twelve month PD and LGD proxies, the indicative stage based ECL and its coverage, eligible receivables and the borrowing base with headroom against the facility, the 30+ and 90+ DPD ratios and a composite credit risk flag. A block below (rows 34 to 41) summarises the company history loaded in *Credit_Input*, whatever the selected mode.

**11b. Covenants.** *Covenants* tests each month against the following default limits: trailing three month operational collection rate of at least 70%; receivables at risk of no more than 15%; 30+ DPD of no more than 25% and 90+ DPD of no more than 18%; positive borrowing base headroom; debt to book equity of no more than 3.0x; and liquidity before new equity. The annual DSCR test (minimum 1.20x) sits on *KPIs* (row 51 flags each year below the minimum; the summary below counts the years) and also counts in readiness gate 10. A composite credit flag and an "any covenant" flag feed the breach counts. Receivables at risk follows the logic of the 2021 PERFORM guide, which is historical; under the 2026 standard it is an operational and lender metric, not a PERFORM KPI.

**11c. Loading the company's own data.** This is the single most useful thing a user can do with the model.

1. Export the portfolio from the servicing platform or ERP, month by month and tier by tier, and paste it into *Credit_Input* (one block per tier, up to 60 months). Stocks are entered at month end: balances, DPD buckets, default exposure. Flows are entered for the month: originations, repossessions, resale proceeds and costs, cures, write offs, collections, instalments due, unlocks.
2. The DPD buckets must add up to gross receivables. A check enforces this in Actual mode.
3. Set *Credit data mode* on *Credit_Assumptions* to 2 (Actual). *Credit_Portfolio* and the selected block of *Credit_Engine* then report company history, while projections and the facility continue to run on the curves. History is never blended into the forecast without the user knowing.
4. Enter cohort observations in *Vintage_Input*: one row per monthly cohort, mode 2 for actual cohorts, and cumulative collections, instalments due, 30+, 90+ and 180+ exposure, recoveries and active accounts at M3, M6, M12, M18, M24, M36, M48 and M60, with ownership at twice the tenor where available. Cumulative collections and instalments due must never fall between checkpoints (tests 32 and 33).
5. Compare *Vintage_Dashboard* (company data) with the proxy curves. Where cohort repayment ratios and DPD curves diverge, recalibrate the default hazard and collection rates on *Products*, mark the recalibrated rows CALIBRATED ASSUMPTION, and set the input set selector on *Scenarios* to Calibrated case. The SolaraPay case study (CASE 2) works through this calibration in full.

**11d. PAYGo PERFORM 2026 results (section C of PERFORM_2026).** PAYGo PERFORM KPIs come only from the company's contract level data, computed by the company under the GOGLA Technical Guide of June 2026. The model does not compute them, and the operational collection rate, the cohort repayment ratio or any other collection metric may not be substituted for the Repayment Rate. Section C has one block per tier with 60 rows, one per monthly cohort, and the following columns:

| Column | Content |
|---|---|
| Cohort #, Origination month | Monthly cohort identifier |
| Contracts | Number of contracts in the cohort |
| RR PvP | Payments applied to due instalments; instalments due to date |
| RR PvFin | Payments applied to due instalments; total amount financed |
| RR @90 days | Payments applied; instalments due by day 90 |
| RR @2x | Payments applied by 2x term; instalments due over 1x term |
| OR @2x | Contracts fully paid by 2x; contracts that reached 2x |
| Data as of, Notes | Reporting date and comments |

Enter numerators and denominators, not ratios. The rules printed on the sheet (Technical Guide, pages 8 to 10) apply: exclude deposits, prepayments, penalties, fees and subsidies; include arrears payments and written off contracts; cumulate from contract start after any free use period; use original contract terms and daily normalised instalments; recognise payments when applied to due instalments. Section A then aggregates by summing numerators and denominators across cohorts and tiers. Test 37 rejects negative values and numerators above their denominators; a readiness flag counts cohorts below the 100 contracts per monthly cohort that the guide recommends. Mark the cells COMPANY DATA in your evidence file and keep the company's calculation file with the data room.

**Common mistakes.** Pasting DPD buckets that do not reconcile; mixing stock and flow definitions; reading the twelve month PD proxy as an accounting PD (it is derived from the curve in Proxy mode and from observed loss rates in Actual mode); setting the ownership evidence switch to 1 without ownership data, which a readiness flag will catch; and typing the model's collection rate or the section B approximations into section C.

**Reading the result.** Lenders price data, not narratives. The fastest route to better terms is twelve or more months of clean cohort and DPD history that reconciles to the accounts, with PERFORM 2026 results computed by the company on contract level data.

## Step 12. Prepare the investment memo

**Sheets:** Investment_Summary, Dashboard, Valuation, Unit_Economics, Benchmark_Compare, Calibration, Source_Register, Investment_Readiness.

**12a. Valuation and returns.** *Valuation* holds three views. The first is a DCF of unlevered free cash flow in local currency. Because free cash flow includes the investment in net working capital, which in PAYGo is mainly receivables, it stays negative while the book grows; the terminal value therefore uses a normalised cash flow that reinvests only the long run growth rate times working capital. The second is an exit valuation at the end of Year 5, either an EV/EBITDA multiple less net debt or a price to book multiple. The third is the investor IRR and multiple in USD: the investor buys a stake equal to ticket ÷ (pre money valuation + ticket), funds its pro rata share of any equity top up and receives its share of exit equity at the exit FX rate.

**12b. Unit economics.** For each tier, *Unit_Economics* sets out lifetime customer cash, expected loss rate, recoveries, RBF, hardware, installation, warranty, CAC and servicing cost, and derives contribution, LTV to CAC, cash payback, unit IRR and unit NPV.

**12c. External evidence.** *Source_Register* records each claim with a grade for the source (A primary official or audited, B institutional or company disclosure, C reputable secondary, D unverified) and, separately, a status for what has been checked: VERIFIED, VERIFIED (HISTORICAL), PENDING PRIMARY DOCUMENT, UNVERIFIED, CONFLICTING SOURCES or NOT USED. *Calibration* compares the active scenario only with references whose source is VERIFIED; any other reference is suspended and the diagnostic reads "Reference suspended: source not VERIFIED". In this build every sourced calibration reference is suspended. For example, the ESMAP Off-Grid Solar Market Trends Report 2024 is reported to give an average PAYGo collection rate of about 62% for 2021 to 2023, but that figure is PENDING PRIMARY DOCUMENT and is a collection rate, not a Repayment Rate. The M-KOPA group revenue figures are CONFLICTING SOURCES and the filing held is that of M-KOPA UK LIMITED, a subsidiary, so no M-KOPA ratio is used as a benchmark until the group's consolidated accounts are read. *Benchmark_Compare* places the model's ratios against graded peer records and carries a comparability warning per KPI; *Benchmark_DB* shows the definition of each item and whether it is comparable with the model. Ranges built on fewer than three peers are flagged as anecdotal.

**12d. Readiness.** *Investment_Readiness* lists 23 gates, 13 of them critical. Automatic gates cover integrity, covenant compliance (no month in breach of a monthly covenant and no year with DSCR below the 1.2x minimum), positive contribution, actual credit data, consumer protection evidence (including PERFORM_2026 results), support for outcome linked RBF and data reconciliation. Manual gates cover management sign off, term sheets, legal review, the Excel test, the review of the accounting treatment and similar items. A manual gate counts only when its status is Met and the sheet records where the evidence is held and who signed it off; a gate marked Met without both is not counted.

The decision rule uses these results only:

| Condition | Decision |
|---|---|
| Any failed test: master check ERROR, covenant breach in the active scenario (monthly covenants or annual DSCR), or negative lifetime contribution in a tier | STOP (failed test) |
| All 23 gates met with evidence | GO |
| All 13 critical gates met | CONDITIONAL GO (the open gates become conditions) |
| Otherwise | STOP: evidence incomplete |

At default inputs the sheet reads 2 of 23 gates met (gates 1 and 13; 2 of 13 critical), decision STOP (Failed test: No covenant breach in the active scenario (monthly covenants and annual DSCR)). In the SolaraPay case it reads 4 of 23 (gates 1, 13, 18 and 22; 4 of 13 critical), with the same STOP on a failed test. In both files the Base DSCR is below the 1.2x minimum in Years 1 to 4 (*KPIs*, years below minimum: 4). GO is never an investment recommendation, and a STOP on incomplete evidence is not a verdict on the business; a STOP on a failed test is: it is a finding against the business plan as modelled, here that the projection fails the lender's DSCR test in Years 1 to 4. The recommendation is the analyst's judgement: in Book 2 (Chapter 16.11) the analyst recommends a Conditional Go for SolaraPay beside the workbook's STOP, explicitly conditional on the DSCR covenant being replaced or reset with the lender (Chapter 16.9 proposes portfolio covenants instead) and on the critical gates being evidenced before disbursement.

**12e. Structure of the memo.** The following order works well, with model outputs cited throughout:

1. Recommendation (Go, Conditional Go or Stop) and conditions, shown beside the workbook's evidence decision.
2. Company, market and product range (Step 2).
3. Unit economics by tier (12b).
4. Portfolio quality and data: actual against proxy, cohort curves, PERFORM 2026 results (Step 11).
5. Financial projections and funding requirement (Steps 8 and 9).
6. Scenarios and stress tests (Step 10).
7. Financing structure, borrowing base, covenants and FX exposure (Steps 3, 8 and 11).
8. Valuation and returns (12a).
9. Benchmarking and calibration (12c).
10. Consumer protection and impact (Step 2, RBF).
11. Readiness gates and outstanding diligence (12d).
12. Risks and mitigants.

**Common mistakes.** Quoting the DCF value on its own; for a growing PAYGo book it is usually well below exit based values, and the memo should present both and explain the gap. Presenting a peer median built on one or two companies as "the market". Using any figure whose status in *Source_Register* is not VERIFIED, or any *Benchmark_DB* record flagged as not comparable or excluded. Presenting the workbook's GO or STOP as the investment recommendation.

# Part C. Methodology reference

## Repayment curves and cohorts

For each tier, *Curves* computes the behaviour of a single unit by account age *a*, measured in months since sale. With a monthly default hazard *h* and a tenor *T*:

| Quantity | Definition |
|---|---|
| Survival (still paying) | S(a) = (1 − h)^a |
| Instalment due | The instalment, for 1 ≤ a ≤ T |
| Collected | Instalment × collection rate on paying accounts × S(a) |
| Missed | Due less collected |
| Receivable at risk | (1 − S(a)) × (T − a) × (instalment − premium ÷ T), the carrying amount of accounts that have stopped paying |
| Net recovery | Defaults at age (a − lag) × repossession rate × gross resale share × cash price × (1 − recovery cost) |

The cohort sheets (*Cohort_T1* to *Cohort_T5*) apply these unit curves to each monthly cohort, scaled by the price index for monetary items and by units for account counts. *Ops* aggregates the cohorts by calendar month.

## Receivables, ECL and write offs

Gross PAYGo receivables roll forward by tier: opening balance, plus amount financed on new sales (cash price less down payment), plus financing income, less collections, less missed instalments.

The loss allowance is set up at origination at the lifetime expected missed instalments and is drawn down as instalments are missed. If actual behaviour follows the curve, the allowance is exactly consumed over each cohort's life. Three simplifications apply: the booked allowance is not staged; financing income is recognised straight line rather than under the effective interest method; and missed instalments are written off as they fall due rather than at the default date. This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS.

## Credit engine

In Proxy mode, balances on paying accounts are split between current and 1 to 30 DPD by an input share, and receivables at risk are split across the 31 to 60, 61 to 90, 91 to 180 and over 180 DPD buckets by input shares that reconcile exactly to gross receivables.

Staging follows the thresholds on *Credit_Assumptions*. A bucket whose lower bound exceeds the Stage 3 threshold is Stage 3; one whose lower bound exceeds the Stage 2 threshold is Stage 2; all others are Stage 1. The indicative ECL is the sum over buckets of the balance times the stage loss factor: PD12 × LGD × discount factor for Stage 1, (1 − cure rate) × LGD × discount factor for Stage 2, and LGD for Stage 3. The discount factor is (1 + ECL discount rate)^(−0.5). The staging and ECL are analytical proxies, not accounting measures.

| Proxy | Proxy mode | Actual mode |
|---|---|---|
| Twelve month PD | 1 − (1 − h)^12 | Trailing twelve month write offs ÷ average gross receivables |
| LGD | 1 − repossession rate × resale share × (1 − recovery cost) × cash price ÷ amount financed | 1 − (resale proceeds − recovery costs) ÷ write offs, trailing twelve months |

Eligible receivables are the buckets whose lower DPD bound is at or below the borrowing base maximum.

## Vintage engine

Vintage KPIs are cumulative at each checkpoint: cohort repayment ratio (collections ÷ instalments due; it follows the logic of RR PvP but is a monthly approximation without payment allocation and is not a PERFORM calculation); DPD exposure ÷ instalments due at 30+, 90+ and 180+; recoveries ÷ defaults; active share; and cumulative contribution per unit. DPD exposure is defined as the arrears of accounts at or beyond the threshold, including amounts already written off, plus their outstanding balance. This keeps a cohort's credit history visible after its payment plan has ended.

Proxy cohorts are identical within a tier. An actual cohort without data shows a blank cell; it is never filled silently with a proxy.

## PAYGo PERFORM 2026

Under the 2026 standard the five KPIs are RR PvP, RR PvFin, RR PvP at 90 days, RR PvP at 2x contract term and OR @2x. *PERFORM_2026* section A aggregates the company's section C entries by summing numerators and denominators, as the guide requires, rather than averaging cohort or tier ratios. Section B approximations use the *Vintage_Input* checkpoints and are labelled as not PERFORM KPIs. The collection rate, receivables at risk and write off ratio of the 2021 guide (historical) are operational and lender metrics in this model, not current PERFORM KPIs.

## Financing, FX and tax

The term loan is tracked in USD and translated monthly; the FX loss equals the opening USD balance times the change in the exchange rate. The facility drawing equals max(0, min(limit, borrowing base, previous balance + minimum cash − cash before facility)). Tax equals the tax rate times the increase in the running maximum of cumulative pre tax profit, which is equivalent to unlimited loss carry forward with tax paid in the month it arises.

*FX_Exposure* presents these existing calculations without changing them. Transaction effects compare each local currency amount with what it would have been at the opening rate, and change cash. Remeasurement of USD debt is a non cash entry. Translation changes how local currency results look in USD and drives the USD IRR, but does not move local currency cash.

## Valuation and returns

Free cash flow equals EBITDA less tax, less capex, less the increase in net working capital (net receivables plus inventory less payables). Cash flows are discounted at mid year. The terminal value equals [(EBITDA − tax − capex) in Year 5 × (1 + g) − g × net working capital in Year 5] ÷ (discount rate − g). Investor cash flows in USD are the ticket at Year 0, the investor's share of each year's equity top ups translated at the average FX rate of that year, and its share of exit equity translated at the exit FX rate in Year 5.

The investor IRR tries starting guesses of 10%, (20%) and 50%. It returns "n/a: no sign change" when the flows have no positive or no negative value (for example the Severe case, where every investor flow is negative) and "n/a: no convergence" otherwise. The unit IRR on *Unit_Economics* follows the same pattern with monthly guesses.

## Covenants and readiness

Every covenant threshold is an input. A flag reads 1 when the covenant is breached and is tested only while the relevant debt is outstanding. Readiness gates are automatic where the model can test them and manual, with a drop down status (Not started, In progress, Met) and evidence columns, where they rest on external evidence. The decision rule is set out in Step 12d.

## Benchmark database

The benchmark records are maintained in a controlled database outside the workbook and loaded into *Benchmark_DB* at each release. Each record carries its source, country, page, a definition of what the figure measures, a grade, a verification status, a use flag and a "comparable with the model?" flag; country and page read TO VERIFY or PAGE TO VERIFY until the source has been read. Records that conflict, carry no period, cover a half year only or are graded D are kept for transparency but excluded from the ranges. Peer ranges draw only on usable records graded A to C. Benchmark figures should not be typed into the workbook; new evidence goes to the model owner, with its source, for grading and loading at the next release.

## Troubleshooting

| Symptom | Likely cause | Remedy |
|---|---|---|
| Master check ERROR on "Sales mix sums to 100%" | Mix changed on one tier only | Bring the five tiers back to a total of 100% |
| "Balance sheet balances" shows a difference | A formula has been overwritten | Restore from the clean copy and change blue cells only |
| "Actual DPD buckets reconcile" reads 1 | Credit_Input buckets do not equal gross receivables | Correct the export; buckets are month end stocks |
| "Proxy shares of receivables at risk sum to 100%" reads 1 | Shares on Credit_Assumptions changed | Bring the four shares back to 100% |
| "Hybrid RBF weights" reads 1 | Weights do not total 100% | Correct the weights on Inputs |
| RBF check reads 1 | Cumulative disbursements above cumulative claims, or RBF overwritten in the statements | Review the RBF inputs on Inputs and Products; restore overwritten formulas |
| PERFORM_2026 check reads 1 | A negative entry, or a numerator above its denominator, in section C | Correct the company's entries; enter numerators and denominators, not ratios |
| Vintage_Input check reads 1 | Cumulative collections or instalments due fall between checkpoints | Correct the cohort data; values are cumulative |
| Scenario lever check reads 1 | A value in the ACTIVE column of Scenarios has been overwritten | Restore the formula from the clean copy |
| Facility stays at zero | Start month beyond the horizon, or a zero borrowing base (advance rates at 0%, or maximum DPD below 1) | Review Inputs and Products |
| Investor IRR shows "n/a: no sign change" | No positive investor cash flow (exit equity of zero) | Expected in severe cases; read the multiple and the peak equity instead |
| Investor IRR shows "n/a: no convergence" | Unusual flows for which no starting guess converges | Read the multiple; review the flows on Valuation |
| A manual readiness gate marked Met is not counted | Evidence location or sign off missing | Complete both columns on Investment_Readiness |
| Static Sensitivity rows do not move | They are computed at default inputs for each release | Read the LIVE row, or run one at a time tests on a copy (Step 10) |
| Excel reports a circular reference | This should not occur | Report it to the model owner; each release is tested for zero cycles |

## Limitations

1. Monthly granularity, no seasonality, one country and one currency.
2. The proxy credit engine assumes that an account which stops paying never resumes; cures enter the indicative ECL only.
3. Revenue recognition, ECL and tax are simplified as described above, and audited accounts will differ. This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS.
4. Ownership at twice the tenor and the PAYGo PERFORM 2026 KPIs must come from company contract level data; the model does not compute them.
5. Securitisation is modelled on balance sheet. True sale structures through a special purpose vehicle are planned for a later version.
6. Peer benchmarks remain thin until primary filings are read. Several published figures conflict and are excluded; every sourced calibration reference is suspended in this build because no source is yet VERIFIED for it.
7. No FX hedging instrument is modelled.
8. The workbook has not yet been tested in Microsoft Excel.

## Version history

| Version | Main changes |
|---|---|
| v0.1 | First build: three products, cohort engine, ECL, FX, receivables facility, three statements |
| v0.2 | Tiers 1 to 5, recoveries, RBF, cash sweep facility, covenants, valuation, investment summary |
| v0.6 | Credit, vintage, RBF, consumer risk and benchmark layers; readiness gates |
| v0.7 | Branded cover; PAYGo financial benchmark database; SolaraPay worked case; numbered contents and page footers |
| v0.8 (development build) | MODEL 2 branding, companion to Book 2; 47 sheets in an indexed tab order. Source register rebuilt with grade (A to D) separate from status; only VERIFIED references feed Calibration. Robust IRR (Downside (22.9%) now computed; Severe "n/a: no sign change"). Checks raised from 24 to 38 (monthly cash, roll forwards of receivables, allowance, term loan, facility and equity, cohort, vintage, RBF, valuation, scenario lever and PERFORM_2026 tests). Company history block on Credit_Portfolio. New PERFORM_2026 sheet; collection rate relabelled "operational collection rate (not a PERFORM KPI)". New Start sheet, provenance label on every input, Dashboard table of 39 metrics, FX_Exposure sheet, RBF claim cycle, scenario architecture with input set selector, dated Sensitivity table with LIVE row. Investment_Readiness evidence columns and evidence based decision rule. Accounting statement on Cover, Contents, Start, Glossary and the credit sheets. Benchmark country, page, definition and comparability fields. Projections and valuation unchanged from v0.7. Readiness gate 10 now also tests the annual DSCR, so the decision at default inputs and for SolaraPay is STOP on a failed test (2 and 4 of 23 gates met) |
