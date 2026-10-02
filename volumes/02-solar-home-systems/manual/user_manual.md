# About this manual

This manual accompanies the Africa Energy Finance Volume 2 workbook, the *Solar Home Systems PAYGo Company Financial and Investment Model* (file `AEF_SHS_PAYGo_Model_v0.7.xlsx`). It is written for four audiences, and each will want to enter the document at a different point.

| Reader | The question they bring | Where to start |
|---|---|---|
| PAYGo developer or CFO | Can the business plan be financed, and how much equity does it need? | Steps 2 to 9 |
| Lender | Is the receivables book acceptable collateral, and will the covenants hold? | Steps 8 and 11 |
| Equity investor | What is the company worth, and what return is realistic? | Steps 10 and 12 |
| Investment committee | Is the case ready for a decision, and on what conditions? | Step 12 and the readiness gates |

Part A describes how the workbook is built. Part B walks through a twelve step workflow; for each step it gives the sheets involved, the inputs to set, the outputs to read, the mistakes we see most often and the way an experienced analyst would read the result. Part C is the methodology reference, including every simplification a reviewer should know about.

> **Edition note.** This edition describes each sheet by its layout and row labels. Screen captures will be added in the v1.0 edition, once the workbook has completed its test cycle in Microsoft Excel.

> **Status of the default inputs.** The default inputs describe a fictional company in a fictional market. They are placeholders chosen to make the mechanics visible, not benchmarks. The model should not be described as investment grade until real company data have been loaded and the workbook has been independently validated; the *Investment_Readiness* sheet records how far a given case has progressed.

## Scope of the model

The workbook is a monthly, five year, integrated three statement model of a PAYGo solar company that sells five product tiers on credit. Around that core sit a cohort (vintage) credit engine, a lender toolkit (borrowing base, portfolio covenants, debt service cover), an investor toolkit (discounted cash flow, exit valuation, IRR and multiple on invested capital), an outcome based RBF engine, a consumer risk layer and a graded database of published figures on PAYGo companies.

It is not an audited IFRS 9 model, it does not compute tax under any specific code, and it does not replace legal or regulatory advice. Probability of default, loss given default and expected credit loss are reported as indicative proxies throughout. Part C lists each simplification.

## Version and status

| Item | Value |
|---|---|
| Model version | v0.7, development release |
| Size | 44 sheets, about 99,000 formulas, no macros, no external links |
| Integrity | Master check OK; no circular references; every output reproduced to rounding precision by an independent shadow calculation of the full model |
| Readiness at default inputs | 3 of 23 gates met; not investment grade |

# Part A. Model architecture

## Calculation chain

Calculation runs in one direction:

Inputs → Products → Sales → Customers → PAYGo receivables → Credit engine → Vintage engine → Collections and recoveries → RBF engine → Working capital → Financing → Financial statements → Covenants → Valuation → Investor returns → Market benchmark → Calibration → Investment readiness.

No output sheet feeds back into a calculation. Interest accrues on opening balances, and the receivables facility is sized on cash before the facility, so the workbook has no circular references and never needs iterative calculation.

## Sheet map

| Layer | Sheets | Purpose |
|---|---|---|
| Front | Cover, Contents, Investment_Summary, Investment_Readiness | Title page, guide and sheet index, one page summary, 23 readiness gates |
| Inputs | Inputs, Products, Scenarios, Credit_Assumptions, Consumer_Risk | All hard coded assumptions (together with the two data templates) |
| Outputs | Dashboard, KPIs, Credit_Portfolio, Vintage_Dashboard, Covenants, Valuation, Unit_Economics, Sensitivity | Results; nothing to type here |
| Benchmark | Benchmark_Compare, Benchmark_KPIs, Market_Benchmark, Calibration, Company_Cases, Source_Register, Benchmark_Matrix, Benchmark_DB | External evidence and diagnostics |
| Statements | Annual, FS | Annual and monthly income statement, balance sheet and cash flow |
| Engines | Ops, RBF_Engine, Credit_Engine, Vintage_Engine, Costs, Financing, Curves, Cohort_T1 to Cohort_T5, Timeline | Calculations |
| Data templates | Credit_Input, Vintage_Input | Company portfolio and cohort data |
| Control | Glossary, Checks | Definitions, integrity checks and readiness flags |

Every page of the workbook carries a printed footer with the sheet name and page number, and the *Contents* sheet numbers the sheets in the order above, so a printed pack can be referenced by sheet and page.

## Conventions

| Convention | Meaning |
|---|---|
| Blue font | Hard coded input. These are the only cells a user should change. |
| Blue font on yellow | Key assumption. Review these first. |
| Black font | Formula. Never overwrite. |
| Green font | Link from another sheet. |
| Cream shading | Data entry templates (Credit_Input, Vintage_Input). |
| Monthly sheets | Column A label, B unit, C total or closing value, D opening balance, E onwards months 1 to 60. |
| Currency | The model currency is the local currency, labelled on *Inputs*. Hardware, RBF and the term loan are denominated in USD and translated along the FX path on *Timeline*. |
| Signs | Revenue and assets positive; costs negative on the statements; percentages stored as fractions. |

## Integrity controls

The *Checks* sheet runs 25 integrity tests: the balance sheet balances, cash ties out, DPD buckets reconcile to gross receivables, limits are respected, inputs are within valid ranges. They roll up into a master check displayed on the Cover, the Contents sheet, the Dashboard and the Investment summary.

> **Rule.** Do not use any output while the master check reads ERROR. Open *Checks*, find the line showing 1 or a non zero difference, and correct the input that causes it (see *Troubleshooting* in Part C).

Five readiness flags sit below the checks, for example "affordability assumptions not yet reviewed". They are kept outside the master check on purpose: they measure the maturity of the analysis, not the arithmetic.

# Part B. Using the model in twelve steps

## Step 1. Start here

**Sheets:** Cover, Contents, Checks, Inputs (top section).

1. Open the workbook in Excel 2016 or later; Microsoft 365 is recommended. The file is set to recalculate fully when it opens, so let the calculation finish before reading anything.
2. On the Cover, confirm that the master check reads OK, and note the active scenario and the credit data mode.
3. Read the Contents sheet, which holds the operating guide, the numbered sheet index with hyperlinks and the colour code.
4. Save a working copy under a new name before you change anything, for example `CompanyName_Model_v0.7_2026-10-15.xlsx`, and keep the original as a reference.
5. On *Inputs*, set the local currency label and the first model month.

The inputs at this step are the scenario selector (1 Base, 2 Downside, 3 Severe), the first model month and the currency label. The outputs are the master check and the readiness banner.

**Common mistakes.** Users work in the original file rather than a copy; paste values over black formula cells (if in doubt, undo and paste into blue cells only); or leave the selector on Downside and then read the results as if they were Base. The Cover and the Investment summary always show the active scenario.

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

1. Replace the product names, PV size, storage, loads and target segments with the company's own catalogue. Keep all five columns; a company that sells fewer tiers sets the sales mix of the unused tier to 0%.
2. Check each tier label against the product's actual capacity. The label refers to the capacity attribute only; a full Multi Tier Framework assessment also covers duration, reliability, quality, affordability, legality, and health and safety.
3. On *Consumer_Risk*, replace the illustrative household incomes with survey or customer data, set the maximum payment burden from the credit policy, and record the evidence status (Not provided, Provided, Validated) for PAYGo PERFORM reporting and for consumer protection.

The sheet returns, by tier, the payment burden (instalment as a share of income), the down payment as a share of income, the implied consumer APR and an affordability flag.

**Common mistakes.** Leaving the illustrative incomes in place (a readiness flag stays raised until "affordability reviewed" is set to 1), and labelling a product one tier above what its capacity supports.

**Reading the result.** Affordability is a credit risk before it is a social one. A high payment burden is an early predictor of default and can disqualify a portfolio from RBF programmes. The implied APR is the figure a regulator or a journalist will compute, and management should know it first.

## Step 3. Enter market assumptions

**Sheets:** Inputs (macro block), Scenarios.

| Input | Default | What it drives |
|---|---|---|
| Opening FX rate (local currency per USD) | 130 | Local cost of USD hardware, RBF receipts and term debt |
| Depreciation of the local currency against the USD (Scenarios) | 5% Base, 12% Downside, 25% Severe, per year | FX path on *Timeline* |
| Local inflation | 6% | Indexation of operating and per unit costs |
| Annual price increase on new contracts | 5% | Price index of new cohorts |
| Pass through of FX depreciation into new contract prices | 50% | Share of the currency move recovered from new customers |
| Corporate tax rate | 30% | Tax, with unlimited loss carry forward |

**Common mistakes.** Setting depreciation to zero because the currency has been stable. A PAYGo company buys hardware and borrows in USD while it collects in local currency, and depreciation is the most damaging single lever in the default sensitivity table. A second error is to assume full pass through without evidence that customers can absorb it; higher prices feed straight back into affordability (Step 2).

**Reading the result.** Compare two rows of the *Sensitivity* sheet. At default inputs, local currency depreciation of 20% a year turns a Base investor IRR of 46.4% into a loss (IRR of (16.0%)), and freezing prices on new contracts cuts it to 7.9%. Pricing power is a valuation driver in this sector, not a detail of the commercial plan.

## Step 4. Build demand

**Sheets:** Inputs (sales volume), Products (sales mix), Scenarios (volume multiplier).

1. Enter total units sold across all tiers for Years 1 to 5.
2. Set the sales mix by tier on *Products*. It must total 100%, and a check enforces this.
3. Leave the volume multiplier at 1.00 for Base. Downside and Severe apply 0.90 and 0.75 by default.

Monthly sales equal the annual total divided by twelve, multiplied by the scenario volume multiplier and split by mix. Version 0.7 does not model seasonality.

The results appear on *Ops* (units by tier and month) and on *KPIs* (units sold, active accounts, unlocked accounts).

**Common mistakes.** Growing volumes faster than the agent and installer network, and the working capital line, can carry; the funding requirement in Step 8 will show it. The other frequent error is shifting the mix towards Tiers 4 and 5 because it lifts value, which it does sharply, without evidence that those customers repay as assumed.

**Reading the result.** Volume matters less than most plans assume. In the default sensitivity table, a 20% cut in volume lowers the investor IRR from 46.4% to 37.8%, whereas currency depreciation or weak pricing can eliminate it. Growth amplifies the unit economics the company already has, good or bad.

## Step 5. Build revenue

**Sheets:** Products (price plan), Inputs (RBF, other revenue), RBF_Engine.

The price plan for each tier has four inputs: cash price, down payment, daily rate and tenor. From these the model derives the monthly instalment (daily rate × 365 ÷ 12), the total contract value, the PAYGo premium over the cash price and the implied APR.

Revenue recognition follows a simplified IFRS 15 logic. Hardware revenue equals the cash price times units and is recognised at the date of sale. PAYGo financing income equals the premium divided by the tenor and is spread straight line over the tenor of each cohort. Other revenue (digital loans, add on services) is a net take rate per active account per month and is switched off by default. RBF and subsidy income sits below gross profit and is recognised when the cash is received.

The *RBF_Engine* sheet supports four programme designs:

| Mode | Payment basis | Data required |
|---|---|---|
| 1 Sales based | USD per verified unit sold, after a verification lag | Sales verification only |
| 2 Repayment linked | Sales based amount × (repayment rate at verification ÷ target), capped at 100% | Repayment rate data |
| 3 Ownership linked | Paid at twice the tenor on the share of customers who own their device | Validated ownership data at twice the tenor in *Vintage_Input*, with the evidence switch set to 1 |
| 4 Hybrid | Weighted combination of modes 1 to 3 | Weights totalling 100% |

**Common mistakes.** Expecting the ownership linked design to pay out on proxy data. It pays zero by design until validated evidence exists, because the workbook will not manufacture that KPI. Entering a monthly instalment in the daily rate field is the other recurring error.

**Reading the result.** The APR row is the company's consumer protection disclosure. Whether each price plan recovers acquisition and hardware cost is answered on *Unit_Economics* (Step 12).

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
2. A USD term loan, defined by amount, drawdown month, rate, grace period and amortisation. It is revalued at each month's FX rate, and the revaluation runs through the income statement as an unrealised FX gain or loss.
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

**Reading the result.** The *Investment_Summary* reports the peak equity requirement in USD. At default inputs it is USD 10.0m in Base and about USD 46.6m in Severe. A plan that works only if the whole facility is available is, in substance, a bet on credit quality.

## Step 9. Review the financial statements

**Sheets:** FS (monthly), Annual.

Review the statements in this order:

1. The balance check row, which should read 0 in every month, and the master check.
2. The revenue mix between hardware, financing income and other revenue.
3. Credit losses. Expected credit loss is charged when each contract is originated (lifetime expected missed instalments from the scenario curve); recoveries on repossessed units are shown separately; missed instalments are written off as they fall due.
4. EBITDA and net income. Tax becomes payable only once accumulated losses have been absorbed.
5. Cash flow. Operating cash flow is normally negative while the book grows; the line *cash before equity top up* shows the true funding gap.
6. Balance sheet: net PAYGo receivables (gross less loss allowance), the term loan in local currency, the receivables facility and equity.

**Common mistakes.** Reading positive EBITDA as positive cash. In PAYGo, profit arrives before cash, because hardware revenue is recognised at sale and the cash comes in over the tenor. Users also confuse three different credit figures: the loss allowance on the balance sheet, write offs of missed instalments, and the indicative stage based ECL on *Credit_Engine*, which is a diagnostic and is not booked.

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

1. Switch the selector on *Inputs* between 1, 2 and 3 and read the *Investment_Summary* each time.
2. Read the *Sensitivity* sheet, which holds fifteen cases, each moving one lever away from Base. The table is computed at default inputs for each release and does not recalculate when inputs change.
3. For company specific sensitivities, change one input at a time, record the result, and restore the input before the next test.

At default inputs the three scenarios give the following results:

| Case | Peak equity (USD m) | Year 5 EBITDA margin | Investor IRR | Months in covenant breach |
|---|---|---|---|---|
| Base | 10.0 | 21.6% | 46.4% | 0 |
| Downside | 10.0 | 7.3% | (22.9%) | 44 |
| Severe | 46.6 | (18.4%) | Not meaningful (total loss) | 48 |

**Common mistakes.** Presenting Base alone; building a Downside that moves one variable when real stress moves credit, currency and volume together; and saving the file with the selector away from 1.

**Reading the result.** An investment case is only as strong as its Downside. When the Downside calls for unplanned equity or breaches covenants for most of the horizon, the structure needs mitigants: price indexation, lower leverage, slower growth or tighter credit policy.

## Step 11. Test bankability

**Sheets:** Credit_Portfolio, Credit_Engine, Covenants, Vintage_Dashboard, Credit_Input, Vintage_Input.

**11a. The credit portfolio.** *Credit_Portfolio* consolidates all tiers. It shows gross receivables by DPD bucket and default exposure, the collection ratio, weighted twelve month PD and LGD proxies, the indicative stage based ECL and its coverage, eligible receivables and the borrowing base with headroom against the facility, the 30+ and 90+ DPD ratios and a composite credit risk flag.

**11b. Covenants.** *Covenants* tests each month against the following default limits: trailing three month collection rate of at least 70%; receivables at risk of no more than 15%; 30+ DPD of no more than 25% and 90+ DPD of no more than 18%; positive borrowing base headroom; debt to book equity of no more than 3.0x; and liquidity before new equity. The annual DSCR test (minimum 1.20x) sits on *KPIs*. A composite credit flag and an "any covenant" flag feed the breach counts.

**11c. Loading the company's own data.** This is the single most useful thing a user can do with the model.

1. Export the portfolio from the servicing platform or ERP, month by month and tier by tier, and paste it into *Credit_Input* (one block per tier, up to 60 months). Stocks are entered at month end: balances, DPD buckets, default exposure. Flows are entered for the month: originations, repossessions, resale proceeds and costs, cures, write offs, collections, instalments due, unlocks.
2. The DPD buckets must add up to gross receivables. A check enforces this in Actual mode.
3. Set *Credit data mode* on *Credit_Assumptions* to 2 (Actual). *Credit_Portfolio* and the selected block of *Credit_Engine* then report company history, while projections and the facility continue to run on the curves. History is never blended into the forecast without the user knowing.
4. Enter cohort observations in *Vintage_Input*: one row per monthly cohort, mode 2 for actual cohorts, and cumulative collections, instalments due, 30+, 90+ and 180+ exposure, recoveries and active accounts at M3, M6, M12, M18, M24, M36, M48 and M60, with ownership at twice the tenor where available.
5. Compare *Vintage_Dashboard* (company data) with the proxy curves. Where repayment and DPD curves diverge, recalibrate the default hazard and collection rates on *Products*. The SolaraPay case study works through this calibration in full.

**Common mistakes.** Pasting DPD buckets that do not reconcile; mixing stock and flow definitions; reading the twelve month PD proxy as an IFRS 9 PD (it is derived from the curve in Proxy mode and from observed loss rates in Actual mode); and setting the ownership evidence switch to 1 without ownership data, which a readiness flag will catch.

**Reading the result.** Lenders price data, not narratives. The fastest route to better terms is twelve or more months of clean cohort and DPD history that reconciles to the accounts.

## Step 12. Prepare the investment memo

**Sheets:** Investment_Summary, Valuation, Unit_Economics, Benchmark_Compare, Calibration, Investment_Readiness.

**12a. Valuation and returns.** *Valuation* holds three views. The first is a DCF of unlevered free cash flow in local currency. Because free cash flow includes the investment in net working capital, which in PAYGo is mainly receivables, it stays negative while the book grows; the terminal value therefore uses a normalised cash flow that reinvests only the long run growth rate times working capital. The second is an exit valuation at the end of Year 5, either an EV/EBITDA multiple less net debt or a price to book multiple. The third is the investor IRR and multiple in USD: the investor buys a stake equal to ticket ÷ (pre money valuation + ticket), funds its pro rata share of any equity top up and receives its share of exit equity at the exit FX rate.

**12b. Unit economics.** For each tier, *Unit_Economics* sets out lifetime customer cash, expected loss rate, recoveries, RBF, hardware, installation, warranty, CAC and servicing cost, and derives contribution, LTV to CAC, cash payback, unit IRR and unit NPV.

**12c. External evidence.** *Benchmark_Compare* places the model's ratios (margins, growth, credit losses, leverage, per customer metrics) against graded records of PAYGo and asset finance companies, showing the count, minimum, median and maximum and where Year 5 of the plan falls. *Calibration* turns those references into diagnostic messages; at default inputs, for instance, it reports that the Year 5 net margin is several times the scale reference and asks for the cost and credit assumptions to be justified. Ranges built on fewer than three peers are flagged as anecdotal, and source conflicts that remain unresolved are excluded until primary filings are read.

**12d. Readiness.** *Investment_Readiness* lists 23 gates. Automatic gates cover integrity, covenant compliance, positive contribution, actual credit data, consumer protection evidence, support for outcome linked RBF and data reconciliation. Manual gates cover management sign off, term sheets, legal review, the Excel test, auditor review of the ECL approach and similar items. The banner reads "INVESTMENT READINESS: x/23 gates met; not investment grade" until every gate is met, and even then it claims only that the case is ready for independent validation.

**12e. Structure of the memo.** The following order works well, with model outputs cited throughout:

1. Recommendation (Go, Conditional Go or Stop) and conditions.
2. Company, market and product range (Step 2).
3. Unit economics by tier (12b).
4. Portfolio quality and data: actual against proxy, cohort curves (Step 11).
5. Financial projections and funding requirement (Steps 8 and 9).
6. Scenarios and stress tests (Step 10).
7. Financing structure, borrowing base and covenants (Steps 8 and 11).
8. Valuation and returns (12a).
9. Benchmarking and calibration (12c).
10. Consumer protection and impact (Step 2, RBF).
11. Readiness gates and outstanding diligence (12d).
12. Risks and mitigants.

**Common mistakes.** Quoting the DCF value on its own; for a growing PAYGo book it is usually well below exit based values, and the memo should present both and explain the gap. Presenting a peer median built on one or two companies as "the market". Using any figure marked ESTIMATE, NOT CONFIRMED or CONFLICT in *Source_Register* or *Benchmark_DB*.

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

The loss allowance is set up at origination at the lifetime expected missed instalments and is drawn down as instalments are missed. If actual behaviour follows the curve, the allowance is exactly consumed over each cohort's life. Three simplifications apply: the booked allowance is not staged under IFRS 9; financing income is recognised straight line rather than under the effective interest method; and missed instalments are written off as they fall due rather than at the default date.

## Credit engine

In Proxy mode, balances on paying accounts are split between current and 1 to 30 DPD by an input share, and receivables at risk are split across the 31 to 60, 61 to 90, 91 to 180 and over 180 DPD buckets by input shares that reconcile exactly to gross receivables.

Staging follows the thresholds on *Credit_Assumptions*. A bucket whose lower bound exceeds the Stage 3 threshold is Stage 3; one whose lower bound exceeds the Stage 2 threshold is Stage 2; all others are Stage 1. The indicative ECL is the sum over buckets of the balance times the stage loss factor: PD12 × LGD × discount factor for Stage 1, (1 − cure rate) × LGD × discount factor for Stage 2, and LGD for Stage 3. The discount factor is (1 + ECL discount rate)^(−0.5).

| Proxy | Proxy mode | Actual mode |
|---|---|---|
| Twelve month PD | 1 − (1 − h)^12 | Trailing twelve month write offs ÷ average gross receivables |
| LGD | 1 − repossession rate × resale share × (1 − recovery cost) × cash price ÷ amount financed | 1 − (resale proceeds − recovery costs) ÷ write offs, trailing twelve months |

Eligible receivables are the buckets whose lower DPD bound is at or below the borrowing base maximum.

## Vintage engine

Vintage KPIs are cumulative at each checkpoint: repayment rate (collections ÷ instalments due); DPD exposure ÷ instalments due at 30+, 90+ and 180+; recoveries ÷ defaults; active share; and cumulative contribution per unit. DPD exposure is defined as the arrears of accounts at or beyond the threshold, including amounts already written off, plus their outstanding balance. This keeps a cohort's credit history visible after its payment plan has ended.

Proxy cohorts are identical within a tier. An actual cohort without data shows a blank cell; it is never filled silently with a proxy.

## Financing, FX and tax

The term loan is tracked in USD and translated monthly; the FX loss equals the opening USD balance times the change in the exchange rate. The facility drawing equals max(0, min(limit, borrowing base, previous balance + minimum cash − cash before facility)). Tax equals the tax rate times the increase in the running maximum of cumulative pre tax profit, which is equivalent to unlimited loss carry forward with tax paid in the month it arises.

## Valuation and returns

Free cash flow equals EBITDA less tax, less capex, less the increase in net working capital (net receivables plus inventory less payables). Cash flows are discounted at mid year. The terminal value equals [(EBITDA − tax − capex) in Year 5 × (1 + g) − g × net working capital in Year 5] ÷ (discount rate − g). Investor cash flows in USD are the ticket at Year 0, the investor's share of each year's equity top ups translated at the average FX rate of that year, and its share of exit equity translated at the exit FX rate in Year 5.

## Covenants and readiness

Every covenant threshold is an input. A flag reads 1 when the covenant is breached and is tested only while the relevant debt is outstanding. Readiness gates are automatic where the model can test them and manual, with a drop down status, where they rest on external evidence.

## Benchmark database

The benchmark records are maintained in a controlled database outside the workbook and loaded into *Benchmark_DB* at each release. Each record carries its source, a grade from A (audited or regulatory filing) to E (contextual), a verification status and a use flag. Records that conflict, carry no period, cover a half year only or are graded D are kept for transparency but excluded from the ranges. Peer ranges draw only on usable records graded A to C. Benchmark figures should not be typed into the workbook; new evidence goes to the model owner, with its source, for grading and loading at the next release.

## Troubleshooting

| Symptom | Likely cause | Remedy |
|---|---|---|
| Master check ERROR on "Sales mix sums to 100%" | Mix changed on one tier only | Bring the five tiers back to a total of 100% |
| "Balance sheet balances" shows a difference | A formula has been overwritten | Restore from the clean copy and change blue cells only |
| "Actual DPD buckets reconcile" reads 1 | Credit_Input buckets do not equal gross receivables | Correct the export; buckets are month end stocks |
| "Proxy shares of receivables at risk sum to 100%" reads 1 | Shares on Credit_Assumptions changed | Bring the four shares back to 100% |
| "Hybrid RBF weights" reads 1 | Weights do not total 100% | Correct the weights on Inputs |
| Facility stays at zero | Start month beyond the horizon, or a zero borrowing base (advance rates at 0%, or maximum DPD below 1) | Review Inputs and Products |
| Investor IRR shows "n/a" | No positive investor cash flow (exit equity of zero) | Expected in severe cases; read the multiple and the peak equity instead |
| Sensitivity table does not move | It is computed at default inputs for each release | Run one at a time tests on a copy (Step 10) |
| Excel reports a circular reference | This should not occur | Report it to the model owner; each release is tested for zero cycles |

## Limitations

1. Monthly granularity, no seasonality, one country and one currency.
2. The proxy credit engine assumes that an account which stops paying never resumes; cures enter the indicative ECL only.
3. Revenue recognition, ECL and tax are simplified as described above, and audited accounts will differ.
4. Ownership at twice the tenor and the PAYGo PERFORM KPIs must come from company data.
5. Securitisation is modelled on balance sheet. True sale structures through a special purpose vehicle are planned for a later version.
6. Peer benchmarks remain thin until primary filings are added, and several published figures conflict and are excluded.

## Version history

| Version | Main changes |
|---|---|
| v0.1 | First build: three products, cohort engine, ECL, FX, receivables facility, three statements |
| v0.2 | Tiers 1 to 5, recoveries, RBF, cash sweep facility, covenants, valuation, investment summary |
| v0.6 | Credit, vintage, RBF, consumer risk and benchmark layers; readiness gates |
| v0.7 | Branded cover; PAYGo financial benchmark database; SolaraPay worked case; numbered contents and page footers |
