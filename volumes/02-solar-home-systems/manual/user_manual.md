# About this manual

This manual explains how to use the **Africa Energy Finance — Volume 2 Solar Home Systems PAYGo Company Financial & Investment Model** (workbook `AEF_SHS_PAYGo_Model_v0.7.xlsx`). It is written for four kinds of reader:

| Reader | Typical question | Where to start |
|---|---|---|
| PAYGo developer / CFO | Can my business plan be financed, and how much equity do I need? | Steps 2–9 |
| Lender | Is the receivables book good collateral? Will covenants hold? | Steps 8 and 11 |
| Equity investor | What is the company worth and what return can I expect? | Steps 10 and 12 |
| Investment committee | Is the case ready for a decision, and on what conditions? | Step 12 and *Investment readiness* |

The manual follows a twelve-step workflow. Each step tells you **where** to work, which **inputs** to set, which **outputs** to read, the **common mistakes**, and how to **interpret** the results. Part C is the methodology reference: how each number is calculated, and the simplifications you should know about.

> **Screen captures.** This edition describes each sheet by layout and cell labels. Screen captures will be added in the v1.0 edition, after the workbook has been tested in Microsoft Excel.

> **Important.** All default inputs describe a **fictional company in a fictional market** and are illustrative placeholders, not benchmarks. The model is **not investment grade** until real company data are loaded and independently validated. The *Investment_Readiness* sheet tracks how close you are.

## What the model is — and is not

**It is** a monthly, five-year, three-statement model of a PAYGo solar company selling five product tiers on credit. Around that core sit:
- a **cohort (vintage) credit engine**;
- lender tools: borrowing base, covenants, DSCR;
- investor tools: DCF, exit valuation, IRR and MOIC;
- an outcome-aware RBF engine;
- a consumer-risk layer;
- a graded benchmark database of real PAYGo companies.

**It is not**:
- an audited IFRS 9 model;
- a tax computation;
- a substitute for legal or regulatory advice.

The credit metrics (PD, LGD, ECL) are *indicative proxies*. Part C lists every simplification.

## Version and status

| Item | Value |
|---|---|
| Model version | v0.7 (development build) |
| Sheets / formulas | 44 sheets, about 99,000 formulas, no macros, no external links |
| Integrity | Master check OK. Results reproduced exactly by an independent Python re-implementation. No circular references. |
| Default readiness | 3 of 23 readiness gates met — *not investment grade* |

# Part A — Model architecture

## The logic chain

The model follows one direction of calculation:

**Inputs → Products → Sales → Customers → PAYGo receivables → Credit engine → Vintage engine → Collections and recoveries → RBF engine → Working capital → Financing → Financial statements → Covenants → Valuation → Investor returns → Market benchmark → Calibration → Investment readiness.**

Nothing on an output sheet feeds back into a calculation. Interest is computed on opening balances and the receivables facility is drawn on cash *before* the facility, so the workbook contains **no circular references**. You never need to enable iterative calculation.

## Sheet map

| Layer | Sheets | Purpose |
|---|---|---|
| Front | Cover, Contents, Investment_Summary, Investment_Readiness | Title page, guide and sheet index, one-page summary, 23 readiness gates |
| Inputs | Inputs, Products, Scenarios, Credit_Assumptions, Consumer_Risk | Every hard-coded assumption lives here (plus the two data templates) |
| Outputs | Dashboard, KPIs, Credit_Portfolio, Vintage_Dashboard, Covenants, Valuation, Unit_Economics, Sensitivity | Read-only results |
| Benchmark | Benchmark_Compare, Benchmark_KPIs, Market_Benchmark, Calibration, Company_Cases, Source_Register, Benchmark_Matrix, Benchmark_DB | External evidence and diagnostics |
| Statements | Annual, FS | Annual and monthly P&L, balance sheet and cash flow |
| Engines | Ops, RBF_Engine, Credit_Engine, Vintage_Engine, Costs, Financing, Curves, Cohort_T1 … Cohort_T5, Timeline | Calculations |
| Data templates | Credit_Input, Vintage_Input | Paste company portfolio data here |
| Control | Glossary, Checks | Definitions; integrity checks and readiness flags |

## Conventions you must know

| Convention | Meaning |
|---|---|
| **Blue font** | Hard-coded input — the only cells you should change |
| **Blue font on yellow** | Key assumption — review these first |
| **Black font** | Formula — never overwrite |
| **Green font** | Link from another sheet |
| Shaded cream cells | Data-entry templates (Credit_Input, Vintage_Input) |
| Monthly sheets | Column A label, B unit, C total or last value, D opening balance, E onwards = months 1–60 |
| Currency | Model currency is local currency (label set on *Inputs*). Hardware, RBF and the term loan are in USD and converted at the *Timeline* FX path. |
| Signs | Revenues and assets positive; costs shown negative on statements; percentages stored as fractions |

## How the workbook protects you

The *Checks* sheet runs 25 integrity tests: balance sheet balances, cash ties, buckets reconcile, limits are respected, inputs are valid, and so on. They feed a **master check** shown on the Cover, the Contents sheet, the Dashboard and the Investment summary.

> **Rule:** never use an output while the master check reads **ERROR**. Go to *Checks*, find the line showing 1 (or a non-zero difference), and fix the input that causes it (Part C, *Troubleshooting*).

Five **readiness flags** sit below the checks, for example "affordability assumptions not yet reviewed". They are deliberately **not** part of the master check: they describe how mature the analysis is, not whether the arithmetic is correct.

# Part B — Using the model in twelve steps

## Step 1 — Start here

**Where:** *Cover*, *Contents*, *Checks*, *Inputs* (top section).

**What to do**
1. Open the workbook in Excel 2016 or later (Microsoft 365 recommended). The file is set to recalculate fully on opening; allow it to finish.
2. On the **Cover**, confirm the master check reads **OK** and note the active scenario and credit-data mode.
3. Read the **Contents** sheet: how-to, clickable sheet index, colour code.
4. **Save a copy under a new name** before changing anything (for example `CompanyName_Model_v0.7_2026-10-15.xlsx`). Keep the original as your reference.
5. On **Inputs**, set the *local currency label* and the *first model month*.

**Inputs:** scenario selector (1 Base, 2 Downside, 3 Severe), first model month, currency label.

**Outputs:** master check, readiness banner.

**Common mistakes**
- Working in the original file instead of a copy.
- Pasting values over formula cells (black font). If in doubt, undo and paste into blue cells only.
- Changing the scenario selector and forgetting it is not Base when reading results. The Cover and Investment summary always display the active scenario.

**Interpretation:** a master check of OK means the arithmetic is internally consistent. It says nothing about whether the assumptions are realistic. That is the purpose of Steps 10–12.

## Step 2 — Define the business

**Where:** *Products* (specification block), *Consumer_Risk*.

The model sells five product tiers, labelled by the **ESMAP Multi-Tier Framework capacity attribute**:

| Tier | Default product | PV / battery | Default tenor | Segment |
|---|---|---|---|---|
| 1 | Pico solar kit | 10 Wp / 40 Wh | 12 months | Rural, first-time PAYGo |
| 2 | Solar home system with TV | 80 Wp / 300 Wh | 24 months | Rural and peri-urban households |
| 3 | Large SHS + DC fridge | 300 Wp / 1.5 kWh | 30 months | Peri-urban households, kiosks |
| 4 | Solar inverter + lithium | ~1.2 kWp / 5 kWh | 36 months | Urban households and SMEs with weak grid |
| 5 | Solar inverter + lithium | ~3 kWp / 10 kWh | 48 months | Upper-income households, SMEs, productive use |

**What to do**
1. Replace product names, PV size, battery capacity, loads and segments with your own catalogue. Keep five columns: if you sell fewer tiers, set the unused tier's sales mix to 0%.
2. Check the MTF tier label against the product's real capacity. The tier refers to the *capacity* attribute only; a full MTF assessment also covers duration, reliability, quality, affordability, legality, and health and safety.
3. On **Consumer_Risk**:
   - replace the **illustrative** household incomes with survey or customer data;
   - set the maximum payment burden from your credit policy;
   - record evidence status ("Not provided / Provided / Validated") for PAYGo PERFORM reporting and for consumer protection.

**Outputs:** the payment burden (instalment ÷ income), down payment ÷ income, implied consumer APR and an affordability flag per tier.

**Common mistakes**
- Leaving the illustrative incomes in place. A readiness flag stays raised until "affordability reviewed" is set to 1.
- Labelling a product with a higher MTF tier than its capacity supports.

**Interpretation:** affordability is a *financial* risk, not only a social one. A high payment burden predicts higher default and can block RBF eligibility. The implied APR is what a regulator or journalist will compute, so know it before they do.

## Step 3 — Enter market assumptions

**Where:** *Inputs* (Macro), *Scenarios*.

**Inputs**

| Input | Default | What it drives |
|---|---|---|
| Opening FX rate (local per USD) | 130 | Cost of USD hardware, RBF and term debt |
| LCY depreciation vs USD (Scenarios) | Base 5% / Downside 12% / Severe 25% p.a. | FX path on *Timeline* |
| Local inflation | 6% | Indexation of opex and per-unit costs |
| Annual price increase on new contracts | 5% | Price index of new cohorts |
| Pass-through of FX depreciation into new-contract prices | 50% | How much of the currency fall you can pass on to new customers |
| Corporate tax rate | 30% | Tax with unlimited loss carry-forward |

**Common mistakes**
- Setting depreciation to zero "because the currency has been stable". PAYGo companies buy hardware and borrow in USD while collecting in local currency, and depreciation is the single largest risk in the default sensitivity table.
- Assuming 100% pass-through without evidence that customers can absorb it. Higher prices reduce affordability (Step 2).

**Interpretation:** compare the *Sensitivity* rows "LCY depreciation 20% p.a." and "no price increase on new contracts". With default inputs, either one can turn a 46% investor IRR into a loss or a single-digit return. Pricing power is a valuation driver, not a detail.

## Step 4 — Build demand

**Where:** *Inputs* (Sales volume), *Products* (sales mix), *Scenarios* (volume multiplier).

**What to do**
1. Enter total units sold for Years 1–5 across all tiers.
2. Set the sales mix per tier on *Products*; it must total 100% (checked).
3. Leave the volume multiplier at 1.00 for Base; Downside and Severe apply 0.90 and 0.75 by default.

Monthly sales are the annual total ÷ 12, multiplied by the scenario volume multiplier and split by mix. Seasonality is not modelled in v0.7.

**Outputs:** *Ops* (units by tier and month); *KPIs* (units sold, active accounts, unlocked accounts).

**Common mistakes**
- Growing volumes faster than the distribution network (agents, installers) and working capital can support. Check the funding requirement in Step 8.
- Shifting mix towards Tiers 4–5 because it raises value (it does, sharply) without evidence that those customers repay as assumed.

**Interpretation:** volume matters less than you might expect. In the default sensitivity table, −20% volume lowers investor IRR from about 46% to 38%, while FX depreciation or weak pricing destroy it. Growth amplifies whatever unit economics you have, good or bad.

## Step 5 — Build revenue

**Where:** *Products* (price plan), *Inputs* (RBF, other revenue), *RBF_Engine*.

**Price plan inputs per tier:** cash price, down payment (deposit), daily rate and tenor. The model derives:
- the monthly instalment (daily rate × 365 ÷ 12);
- the total contract value;
- the PAYGo premium over the cash price;
- the implied APR.

**How revenue is recognised (simplified IFRS 15 style)**
- *Hardware revenue* = cash price × units, at the date of sale.
- *PAYGo financing income* = premium ÷ tenor, straight-line over the tenor of each cohort.
- *Other revenue* (digital loans, services) = net take rate per active account per month. Off by default.
- *RBF / subsidy income* is shown below gross profit when cash is received.

**RBF design (RBF_Engine)**

| Mode | Payment | Requires |
|---|---|---|
| 1 Sales-based | USD per unit sold, after a verification lag | Nothing beyond sales verification |
| 2 Repayment-linked | Sales-based × (repayment rate at verification ÷ target), capped at 100% | Repayment-rate data |
| 3 Ownership-linked | Paid at 2 × tenor on the share of customers who own their device | **Validated ownership-at-2x data** in *Vintage_Input*, with the evidence switch set to 1 |
| 4 Hybrid | Weighted mix of 1–3 | Weights summing to 100% |

**Common mistakes**
- Expecting ownership-linked RBF to pay with proxy data. It pays **zero** by design until validated evidence exists. The model will not invent this KPI.
- Entering the daily rate as a monthly instalment.

**Interpretation:** the APR row is your consumer-protection disclosure. The *Unit_Economics* sheet shows whether each tier's price plan pays back acquisition and hardware cost (Step 12).

## Step 6 — Enter CAPEX and hardware costs

**Where:** *Products* (cost to serve), *Inputs* (freight and duty, working capital and capex).

| Input | Level | Notes |
|---|---|---|
| Hardware FOB cost | USD per unit, per tier | Converted at the month's FX rate and multiplied by the scenario hardware-cost lever |
| Freight, duty and clearing | % of FOB | Applied to all tiers |
| Installation and last-mile logistics | Local currency per unit | Part of cost of sales; indexed to inflation |
| Warranty and after-sales | % of landed cost, per tier | Provision expensed at sale |
| Inventory cover | Months of hardware cost | Drives inventory and purchases |
| Supplier credit | Days | Drives payables |
| Fixed capex | Per month | Vehicles, IT, depots; straight-line depreciation over the life entered |

**Common mistakes**
- Using an FX-converted local hardware price instead of the USD FOB cost. That double-counts depreciation.
- Forgetting installation for Tiers 4–5, where it is material.

**Interpretation:** for a PAYGo company the largest "capital expenditure" is not fixed assets but the **receivables book**: every unit sold on credit ties up cash for its whole tenor. That is why capex looks small and the funding need still looks large.

## Step 7 — Enter OPEX

**Where:** *Products* (commission, marketing), *Inputs* (operating costs).

| Cost | Driver |
|---|---|
| Agent / installer commission | Per unit sold, per tier |
| Marketing and acquisition | Per unit sold, per tier |
| Mobile-money / payment fees | % of cash collected (deposits + instalments) |
| Customer service and collections | Per active account per month |
| Staff | Fixed monthly amount, indexed to inflation |
| G&A, rent, IT, licences | Fixed monthly amount, indexed to inflation |

**Common mistakes**
- Under-sizing central costs for the volume plan. A company serving 70,000 active accounts needs a collections, customer-service and data team.
- Treating commissions as fixed. They are per sale and scale with growth.

**Interpretation:** commission plus marketing is the customer acquisition cost (CAC) shown on *Unit_Economics*. The LTV/CAC ratio and cash payback per tier tell you whether growth creates or destroys value.

## Step 8 — Define financing

**Where:** *Inputs* (Financing, financing structure, covenants), *Credit_Assumptions*, *Products* (advance rates).

**Sources of funds**
1. **Initial equity** (month 1).
2. **USD term loan**: amount, drawdown month, rate, grace period and amortisation. It is revalued at each month's FX rate, and the revaluation goes to P&L as unrealised FX loss or gain.
3. **Receivables facility** in local currency, either:
   - *warehouse* (structure 1); or
   - *securitisation / term ABS* (structure 2: its own rate, an advance-rate haircut and an upfront fee paid the month after each drawing).
4. **Automatic equity top-up**: whenever cash would fall below the minimum, the model injects equity. The cumulative top-up is your **funding requirement**.

**How the facility behaves**
- It is drawn only to keep cash at the minimum balance (cash sweep), up to the lower of the limit and the borrowing base.
- The borrowing base is Σ by tier of advance rate × eligible receivables.
- Eligibility follows the **maximum-DPD rule** on *Credit_Assumptions* (default: receivables up to 30 days past due).
- If the borrowing base shrinks, the facility is repaid.

**Credit assumptions (Credit_Assumptions)**

| Input | Default |
|---|---|
| Default definition | 180 days past due |
| Stage 2 / Stage 3 thresholds | 30 / 90 days past due |
| Borrowing-base max DPD | 30 days |
| Recovery cost | 15% of gross resale proceeds |
| Cure rate | 30% (indicative ECL only) |
| ECL discount rate | 20% |
| Proxy DPD distribution | Current 85% of paying-account balances, the rest 1–30 DPD; receivables at risk split 25 / 20 / 25 / 30% across 31–60, 61–90, 91–180 and 180+ DPD |

**Common mistakes**
- Assuming the full facility limit is available. The binding constraint is usually the borrowing base, and it shrinks as credit quality deteriorates.
- Forgetting that the term loan is in USD: depreciation increases both the debt and the interest in local currency.
- Reading the automatic equity top-up as "free" money. It is equity you must raise, and it dilutes existing shareholders.

**Interpretation:** the *Investment_Summary* shows the **peak equity requirement** in USD. With default inputs it is USD 10m in Base, but about USD 47m in Severe. A plan that only works if the facility is fully available is a plan that depends on credit quality.

## Step 9 — Review the financial statements

**Where:** *FS* (monthly), *Annual*.

**What to check, in order**
1. **Balance check** row (should be 0 every month) and the master check.
2. **Revenue mix:** hardware vs financing income vs other revenue.
3. **Credit losses:**
   - expected credit loss is charged **when each contract is originated** (lifetime expected missed instalments from the scenario curve);
   - recoveries from repossessed units are shown separately;
   - missed instalments are written off as they fall due.
4. **EBITDA and net income.** Tax arises only after accumulated losses are used.
5. **Cash flow:** operating cash flow is usually negative while the receivables book grows. Look at *cash before equity top-up* to see the true funding gap.
6. **Balance sheet:**
   - net PAYGo receivables (gross less loss allowance);
   - term loan in local currency;
   - receivables facility;
   - equity.

**Common mistakes**
- Reading positive EBITDA as positive cash. In PAYGo, profit arrives before cash because revenue is recognised at sale while cash comes over the tenor.
- Confusing the *loss allowance* (balance sheet) with *write-offs* (missed instalments) and with the *indicative stage-based ECL* on *Credit_Engine*, which is a diagnostic and is **not booked**.

**Interpretation:** a PAYGo company can be profitable and still run out of cash. The cash-flow statement and the funding requirement are the truth tellers.

## Step 10 — Run scenarios

**Where:** *Scenarios*, *Inputs* (selector), *Sensitivity*.

**Scenario levers**

| Lever | Base | Downside | Severe |
|---|---|---|---|
| Default hazard multiplier | 1.00 | 1.30 | 1.75 |
| Collection-rate multiplier (paying accounts) | 1.00 | 0.97 | 0.92 |
| Sales volume multiplier | 1.00 | 0.90 | 0.75 |
| Hardware cost multiplier (USD) | 1.00 | 1.05 | 1.10 |
| LCY depreciation vs USD (p.a.) | 5% | 12% | 25% |

**What to do**
1. Switch the selector on *Inputs* between 1, 2 and 3 and read the *Investment_Summary* each time.
2. Read the **Sensitivity** sheet: fifteen pre-computed cases, each changing one lever from Base.
   - The table is a **static snapshot** produced by the verified Python twin of the model at default inputs.
   - It does not update when you change inputs.
   - To refresh it after changing the defaults, run `python tools/build_shs_model.py --snapshot`.
3. For your own sensitivities, change one input at a time, record the result, and restore it.

**Default results (illustrative inputs)**

| Case | Peak equity (USD m) | Year 5 EBITDA margin | Investor IRR | Covenant-breach months |
|---|---|---|---|---|
| Base | 10.0 | 21.6% | 46.4% | 0 |
| Downside | 10.0 | 7.3% | −22.9% | 44 |
| Severe | 46.6 | −18.4% | n/a (total loss) | 48 |

**Common mistakes**
- Presenting only Base.
- Building a Downside that changes one variable when real stress hits several at once (credit, FX, volume).
- Forgetting to reset the selector to 1 before saving.

**Interpretation:** an investment case is as strong as its Downside. If the Downside needs unplanned equity or breaches covenants for most of the horizon, the structure needs mitigants: price indexation, lower leverage, slower growth, or credit tightening.

## Step 11 — Test bankability

**Where:** *Credit_Portfolio*, *Credit_Engine*, *Covenants*, *Vintage_Dashboard*, *Credit_Input*, *Vintage_Input*.

**11a — Read the credit portfolio.** *Credit_Portfolio* consolidates all tiers. It shows:
- gross receivables by DPD bucket and default exposure;
- the collection ratio;
- weighted 12-month PD and LGD proxies;
- the indicative stage-based ECL and its coverage;
- eligible receivables and the borrowing base, with headroom against the facility;
- 30+ and 90+ DPD ratios, and a credit-risk flag.

**11b — Test covenants.** *Covenants* tests every month:
- trailing three-month collection rate (minimum 70% by default);
- receivables at risk (maximum 15%);
- 30+ DPD (maximum 25%) and 90+ DPD (maximum 18%);
- borrowing-base headroom;
- debt to book equity (maximum 3.0x);
- liquidity before new equity.

The annual DSCR test (minimum 1.20x) is on *KPIs*. A composite credit flag and an "any covenant" flag feed the breach counts.

**11c — Load your company's actual data (strongly recommended).**
1. Export your portfolio from the servicing / ERP system, month by month and tier by tier. Paste it into **Credit_Input** (one block per tier, up to 60 months). Stocks go at month end: balances, DPD buckets, default exposure. Flows go for the month: originations, repossessions, proceeds, costs, cures, write-offs, collections, instalments due, unlocks.
2. **DPD buckets must add up to gross receivables.** A check enforces this in Actual mode.
3. Set *Credit data mode* on *Credit_Assumptions* to **2 (Actual)**. *Credit_Portfolio* and the selected block of *Credit_Engine* now report your history. Projections and the facility continue to use the curves, so history is never silently mixed into forecasts.
4. Enter cohort observations in **Vintage_Input**:
   - one row per monthly cohort and mode 2 for actual cohorts;
   - cumulative collections, instalments due, 30+ / 90+ / 180+ exposure, recoveries and active accounts at M3, M6, M12, M18, M24, M36, M48 and M60;
   - ownership at 2 × tenor when available.
5. Compare *Vintage_Dashboard* (your data) with the proxy curves. If your repayment and DPD curves differ, **recalibrate** the default hazard and collection rates on *Products*. The SolaraPay case study shows how.

**Common mistakes**
- Pasting DPD buckets that do not reconcile.
- Mixing stock and flow definitions.
- Reading the 12-month PD proxy as an IFRS 9 PD. It is a proxy from the curve (Proxy mode) or from observed loss rates (Actual mode).
- Setting the ownership evidence switch to 1 without ownership data. A readiness flag catches this.

**Interpretation:** lenders lend against data, not narratives. The fastest way to improve your terms is to show twelve or more months of clean cohort and DPD history that reconciles to your accounts.

## Step 12 — Prepare the investment memo

**Where:** *Investment_Summary*, *Valuation*, *Unit_Economics*, *Benchmark_Compare*, *Calibration*, *Investment_Readiness*.

**12a — Valuation and returns (Valuation)**
- **DCF** of unlevered free cash flow in local currency.
  - Free cash flow includes the investment in net working capital, mainly receivables, so it is negative while the book grows.
  - The terminal value therefore uses a **normalised** cash flow that reinvests only the long-term growth rate × working capital.
- **Exit valuation** at the end of Year 5: EV/EBITDA multiple less net debt, or price-to-book.
- **Investor IRR and MOIC in USD.**
  - The investor buys a stake equal to ticket ÷ (pre-money + ticket).
  - It funds its pro-rata share of any equity top-up.
  - It receives its share of exit equity, converted at the exit FX rate.

**12b — Unit economics (Unit_Economics):** per tier, the lifetime customer cash, expected loss rate, recoveries, RBF, hardware, installation, warranty, CAC and servicing; then contribution, LTV/CAC, cash payback, unit IRR and unit NPV.

**12c — External evidence**
- **Benchmark_Compare** sets your model's ratios (margins, growth, credit losses, leverage, per-customer metrics) against **graded** records of real PAYGo and asset-finance companies: count, minimum, median, maximum, and where your Year 5 sits.
- **Calibration** turns the references into diagnostic messages, such as "model margin is 6.1x the scale reference — justify cost and credit assumptions".
- Ranges with fewer than three peers are flagged as anecdotal. Unresolved source conflicts are excluded until primary filings are read.

**12d — Readiness (Investment_Readiness):** 23 gates.
- Automatic gates: integrity, covenant compliance, positive contribution, actual credit data loaded, consumer protection evidenced, outcome-linked RBF supported, data reconciliation.
- Manual gates: management sign-off, term sheets, legal review, Excel test, auditor review of ECL, and so on.
- The banner reads "INVESTMENT READINESS: x/23 gates met — NOT investment grade" until all gates are met. Even then it says only "ready for independent validation".

**12e — Investment memo structure.** We recommend this order, using model outputs throughout:
1. Recommendation (Go / Conditional Go / Stop) and conditions.
2. Company, market and product range (Step 2).
3. Unit economics by tier (12b).
4. Portfolio quality and data (Step 11): actual vs proxy, cohort curves.
5. Financial projections and funding requirement (Steps 8–9).
6. Scenarios and stress tests (Step 10).
7. Financing structure, borrowing base and covenants (Steps 8 and 11).
8. Valuation and returns (12a).
9. Benchmarking and calibration (12c).
10. Consumer protection and impact (Step 2, RBF).
11. Readiness gates and remaining diligence (12d).
12. Risks and mitigants.

**Common mistakes**
- Quoting the DCF value alone. For a growing PAYGo book it is usually far below exit-based values; present both and explain why.
- Quoting peer medians based on one or two companies as "the market".
- Using any figure flagged *ESTIMATE*, *NOT CONFIRMED* or *CONFLICT* in the *Source_Register* or *Benchmark_DB*.

# Part C — Methodology reference

## Repayment curves and cohorts

For each tier, *Curves* computes the per-unit behaviour by account age *a* (months since sale). With a monthly default hazard *h* and tenor *T*:
- **survival** (still paying) S(a) = (1 − h)^a;
- **instalment due** = instalment for 1 ≤ a ≤ T;
- **collected** = instalment × collection rate on paying accounts × S(a);
- **missed** = due − collected;
- **receivable at risk** = (1 − S(a)) × (T − a) × (instalment − premium ÷ T), the carrying amount of accounts that stopped paying;
- **net recovery** = defaults at age (a − lag) × repossession rate × gross resale % × cash price × (1 − recovery cost).

The cohort sheets (*Cohort_T1…T5*) multiply these per-unit curves by each monthly cohort. Cohorts are scaled by the price index for monetary items, and by units for account counts. *Ops* sums the cohorts by calendar month.

## Receivables, ECL and write-offs

Gross PAYGo receivables per tier roll forward: opening + (cash price − deposit) on new sales + financing income − collections − missed instalments.

The loss allowance is built at origination with the lifetime expected missed instalments, and consumed as instalments are missed. If actual behaviour matches the curve, the allowance is exactly consumed over each cohort's life.

**Simplifications**
- No IFRS 9 staging in the booked allowance.
- No effective-interest method (financing income is straight-line).
- Missed instalments are written off as they fall due, rather than at the default date.

## Credit engine (proxy definitions)

- Balances of paying accounts are split between *current* and *1–30 DPD* by an input share.
- Receivables at risk are split across *31–60, 61–90, 91–180, 180+* by input shares, which reconcile exactly to gross receivables.
- **Stage** follows the thresholds on *Credit_Assumptions*: a bucket whose lower bound exceeds the Stage 3 threshold is Stage 3; above the Stage 2 threshold is Stage 2; otherwise Stage 1.
- **Indicative ECL** = Σ buckets × (Stage 1: PD12 × LGD × discount factor; Stage 2: (1 − cure) × LGD × discount factor; Stage 3: LGD). The discount factor is (1 + ECL discount rate)^−0.5.
- **PD12 proxy:**
  - Proxy mode: 1 − (1 − h)^12.
  - Actual mode: trailing 12-month write-offs ÷ average gross receivables.
- **LGD proxy:**
  - Proxy mode: 1 − repossession rate × resale % × (1 − cost) × cash price ÷ amount financed.
  - Actual mode: 1 − (proceeds − costs) ÷ write-offs (trailing 12 months).
- **Eligible receivables** are buckets whose lower DPD bound is at or below the borrowing-base maximum.

## Vintage engine

Vintage KPIs at each checkpoint are **cumulative**:
- repayment rate (collections ÷ due);
- **DPD exposure ÷ due** for 30+, 90+ and 180+. Exposure is the arrears of accounts at or beyond the threshold, *including amounts already written off*, plus their outstanding balance. This keeps a cohort's history visible after its plan ends.
- recovery ÷ default;
- active share;
- cumulative contribution per unit.

Proxy cohorts are identical within a tier. Actual cohorts with no data show blank, never a silent proxy.

## Financing, FX and tax

- The term loan is tracked in USD and translated monthly. The FX loss = opening USD balance × change in FX rate.
- The facility is drawn = max(0, min(limit, borrowing base, previous balance + minimum cash − cash before facility)).
- Tax = rate × increase in the running maximum of cumulative pre-tax profit. This is unlimited loss carry-forward, paid in the month it arises.

## Valuation and returns

- Free cash flow = EBITDA − tax − capex − increase in net working capital (net receivables + inventory − payables).
- Mid-year discounting at the input discount rate.
- Terminal value = [(EBITDA − tax − capex) of Year 5 × (1 + g) − g × NWC of Year 5] ÷ (discount rate − g).
- Investor cash flows in USD:
  - −ticket at Year 0;
  - −stake × equity top-ups ÷ average FX each year;
  - +stake × exit equity ÷ exit FX in Year 5.

## Covenants and readiness

All covenant thresholds are inputs. Flags are 1 when breached, and are tested only while the relevant debt is outstanding. Readiness gates are automatic where the model can test them, and manual (with a drop-down status) where they require external evidence.

## Benchmark database

**Single source:** `benchmarks/db/paygo_financial_db.csv` (schema in `docs/benchmark-database-schema.md`).

Each record carries:
- its source;
- a grade (A audited/regulatory to E contextual);
- a status;
- a *use* flag. Conflicting, undated, half-year-only or D-grade records are kept but excluded.

Peer ranges use only usable A–C records. Edit the CSV and rebuild; never type benchmark figures into the workbook.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Master check ERROR, "Sales mix sums to 100%" | Mix changed on one tier only | Make the five tiers total 100% |
| "Balance sheet balances" non-zero | A formula was overwritten | Restore from your clean copy; change blue cells only |
| "Actual DPD buckets reconcile" = 1 | Credit_Input buckets ≠ gross receivables | Correct the export; buckets are stocks at month end |
| "Proxy shares of receivables at risk sum to 100%" = 1 | Credit_Assumptions shares changed | Make the four shares total 100% |
| "Hybrid RBF weights" = 1 | Weights do not total 100% | Fix weights on Inputs |
| Facility always at zero | Start month after horizon, or borrowing base zero (advance rates 0%, or max DPD below 1) | Check Inputs and Products |
| Investor IRR "n/a" | No positive investor cash flow (exit equity zero) | Expected in severe cases; read MOIC and peak equity |
| Sensitivity table does not change | It is a static snapshot by design | Regenerate with the build script |
| Excel warns about circular references | Should not happen | Report it; the build is tested for zero cycles |

## Limitations

1. Monthly granularity; no seasonality; one country and currency.
2. The proxy credit engine assumes accounts that stop paying never resume; cures enter the indicative ECL only.
3. Revenue recognition, ECL and tax are simplified (see above). Audited accounts will differ.
4. Ownership-at-2x and PERFORM KPIs must come from company data.
5. Securitisation is modelled on balance sheet. True-sale SPV structures are planned for a later version.
6. Benchmarks are thin until primary filings are added. Several public figures conflict and are excluded.

## Version history

| Version | Main changes |
|---|---|
| v0.1 | First build: 3 products, cohort engine, ECL, FX, facility, 3 statements |
| v0.2 | Tiers 1–5, recoveries, RBF, cash-sweep facility, covenants, valuation, investment summary |
| v0.6 | Credit, vintage, RBF, consumer-risk and benchmark layers; readiness gates |
| v0.7 | Branded cover; PAYGo financial benchmark database; SolaraPay worked case |
