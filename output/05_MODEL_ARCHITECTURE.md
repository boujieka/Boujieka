# Model architecture: AEF SHS PAYGo Model v0.7 (MODEL 2)

Status: audit of the v0.7 workbook as found. No change made. Prepared 3 October 2026.

## Summary

| Item | Finding | Evidence |
|---|---|---|
| Sheets | 44, all visible | Workbook inspection |
| Formulas | 99,438 | Count of formula cells |
| Named ranges | None | Workbook inspection |
| External links | None | Package inspection (no externalLink parts) |
| Macros | None (no VBA part) | Package inspection |
| Circular references | None detected | LibreOffice 24.2 full recalculation returned no Err:522 or other error, default and case workbooks |
| Error values | None | Formula engine evaluation (125,769 cells) and LibreOffice recalculation (99,438 formula cells) |
| Agreement between engines | All formula cells agree; largest difference 1.1e-6 LCY (FS!C64, Financing!C10) | LibreOffice against the formula engine |
| Hardcoded numbers on calculation sheets | None apart from structural period indices | Scan of numeric constants outside label columns |
| Static outputs | Sensitivity (104 values), produced outside the workbook | Sheet inspection; recomputed in the workbook on 3 Oct 2026, all 15 cases match |
| Excel | Not tested (Microsoft Excel not available here) | Readiness gate 17 open |

## Calculation flow

Inputs, Products, Scenarios, Credit_Assumptions and Consumer_Risk feed Timeline (dates, FX path) and Curves (survival and repayment by tier). Curves and Ops drive Cohort_T1 to Cohort_T5, Credit_Engine and RBF_Engine. Costs and Financing complete the monthly statements on FS. FS feeds Annual, KPIs, Covenants and Valuation, which feed Investment_Summary, Investment_Readiness, Dashboard and the Cover status panel. Credit_Input and Vintage_Input carry company history into Credit_Engine and Vintage_Engine when the credit data mode is Actual. The benchmark block (Benchmark_DB, Benchmark_Matrix, Benchmark_KPIs, Benchmark_Compare, Market_Benchmark, Calibration) reads the model's outputs and the Source_Register but does not feed the projections.

## Sheet register

| # | Sheet | Class | Purpose | Formulas | Numeric constants | Feeds from (other sheets) | Feeds into | Main functions | Key outputs | Risk | Status and action |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cover | OUTPUT | Branded cover with live status panel: master check, readiness banner, scenario, credit data mode, currency | 5 | 0 | Checks, Investment_Readiness, Scenarios, Credit_Assumptions, Inputs | none | IF | Status panel | Low | Keep. Wording 'not investment grade' to be reviewed (the model never grades). |
| 2 | Contents | DOCUMENTATION | Sheet index with hyperlinks and colour code | 1 | 0 | Checks | none | none | Index | Low | Fix: index not in tab order; lists only Cohort_T1 of the five cohort sheets. |
| 3 | Investment_Summary | OUTPUT | One page committee and lender view: trajectory, funding need, valuation, lender view, unit economics, scenario snapshot | 126 | 0 | KPIs, Unit_Economics, Sensitivity, Valuation, Inputs, Covenants | none | IF | All headline outputs | Medium | Keep. Scenario snapshot reads the static Sensitivity table. |
| 4 | Investment_Readiness | OUTPUT / CONTROL | 23 readiness gates (8 automatic, 15 manual) and the readiness banner | 33 | 0 | Consumer_Risk, Checks, Unit_Economics, Credit_Assumptions, KPIs, Vintage_Dashboard | Cover, Investment_Summary | IF, AND, SUM, MIN | Gates met (C4): 3 default, 5 case | Medium | Keep counts. Add evidence fields and a GO / CONDITIONAL GO / STOP layer kept separate from judgement. |
| 5 | Inputs | INPUT | Global inputs: scenario selector, dates, currency, macro, RBF, costs, financing, valuation | 1 | 59 | none | Checks, Costs, Covenants, Cover, Credit_Assumptions, Credit_Portfolio | DATE | 59 numeric inputs | Medium | Add provenance label per input (MODEL ASSUMPTION, COMPANY DATA, EXTERNAL EVIDENCE, CALIBRATED ASSUMPTION, UNVERIFIED). |
| 6 | Products | INPUT / CALCULATION | Five tiers: specification, price plan, cost to serve, credit, recovery, RBF, advance rate; derived instalment, contract value, premium, APR | 70 | 95 | Inputs, Scenarios | Checks, Consumer_Risk, Credit_Engine, Curves, Ops, RBF_Engine | IF, IFERROR, RATE, MIN | Instalment, contract value, APR, PERFORM horizon | Medium | Keep. MTF tier labels unverified (SR20). |
| 7 | Scenarios | INPUT | Stress levers for Base, Downside, Severe and the active selection | 6 | 15 | Inputs | Cover, Dashboard, Investment_Summary, Ops, Products, Timeline | CHOOSE | Active levers (column G) | Low | Extend to the scenario architecture: Actual, Management, Calibrated, Base, Downside, Severe. |
| 8 | Credit_Assumptions | INPUT | Credit data mode, default definition, staging thresholds, borrowing base eligibility, recovery, proxy DPD distribution | 37 | 19 | Inputs | Checks, Cover, Credit_Engine, Credit_Portfolio, Curves, Investment_Readiness | IF | Credit parameters | Medium | Keep. Staging is 'IFRS 9 style'; label as analytical treatment. |
| 9 | Consumer_Risk | INPUT / CALCULATION | Affordability: illustrative incomes, payment burden, APR, threshold flag, consumer protection evidence | 25 | 7 | Products | Checks, Investment_Readiness | IFERROR, IF | Burden by tier, flags | Medium | Label 10% threshold as a model policy assumption; add the affordability drivers listed in the brief. |
| 10 | Dashboard | OUTPUT | Charts of revenue, EBITDA, mix, collection and write off, equity and debt | 2 | 0 | Scenarios, Checks | none | none | Charts only | Medium | Rebuild: the requested metric set is not shown. |
| 11 | KPIs | OUTPUT | Annual portfolio, financial and lender KPIs; headline metrics (peak equity, first positive EBITDA, CFO month, lowest trailing collection rate) | 215 | 5 | Timeline, FS, Ops, Covenants, Financing, Inputs | Benchmark_Matrix, Calibration, Investment_Readiness, Investment_Summary, Market_Benchmark | SUMIFS, IFERROR, INDEX, AVERAGEIFS, IF | Collection rate, write off rate, RaR, debt, DSCR, peak equity | High | Collection rate kept as an operational metric; add PERFORM 2026 repayment rate metrics where data allow. |
| 12 | Credit_Portfolio | OUTPUT | Monthly DPD buckets, collection ratio, PD and LGD proxies, indicative ECL, borrowing base | 1,523 | 0 | Credit_Engine, Timeline, Financing, Inputs, Credit_Assumptions | none | IFERROR, IF, OR, MAX | Monthly credit view | Medium | Keep. PD proxy labelled 'not an IFRS 9 PD'. |
| 13 | Vintage_Dashboard | OUTPUT | Portfolio vintage mode, cohort coverage, ownership evidence, M12 tier summary, vintage curve | 71 | 0 | Vintage_Engine, Products, Vintage_Input, Unit_Economics, Inputs | Checks, Investment_Readiness | IFERROR, AVERAGE, COUNTIF, IF, COUNT | Repayment rate at M12, ownership evidence | High | Repayment rate to be rebuilt to PERFORM 2026 rules or renamed. |
| 14 | Covenants | OUTPUT / CONTROL | Monthly covenant tests: trailing collection rate, RaR, leverage, liquidity, 30+ and 90+ DPD | 1,339 | 0 | Credit_Engine, Ops, Financing, Inputs, FS, Timeline | Investment_Summary, KPIs | IF, AND, IFERROR, SUM, MAX | Breach flags | Medium | Keep. Covenant definitions illustrative. |
| 15 | Valuation | CALCULATION / OUTPUT | DCF on normalised FCFF, terminal value, exit equity, investor IRR and MOIC | 72 | 7 | FS, Timeline, Inputs, Costs | Investment_Summary | SUMIFS, INDEX, AVERAGEIFS, IFERROR, IF | EV, exit equity, IRR, MOIC | High | Fix IRR convergence (Downside returns n/a in LibreOffice). Label as illustrative, not a market valuation. |
| 16 | Unit_Economics | OUTPUT | Per tier unit economics: expected collections, loss, contribution, LTV/CAC, payback, unit IRR and NPV | 100 | 0 | Curves, Products, Inputs | Investment_Readiness, Investment_Summary, Vintage_Dashboard | IFERROR, COUNTIF, SUM, IF, IRR | Unit metrics | Medium | Keep. |
| 17 | Sensitivity | REFERENCE (static) | Static table of 15 cases computed by the secondary calculation | 0 | 104 | none | Investment_Summary | none | 15 x 8 values | High | Values do not update. All 15 cases recomputed in the workbook (LibreOffice) on 3 Oct 2026 and match to 1e-13. Replace by a documented refresh procedure or in-workbook case table. |
| 18 | Benchmark_Compare | OUTPUT | Model against benchmark KPIs (median, range, flags) | 230 | 0 | Benchmark_KPIs | none | IF, COUNT, MIN, MEDIAN, MAX | Comparison flags | Medium | Definition and period alignment warnings to be added. |
| 19 | Benchmark_KPIs | CALCULATION | Derived financial and operational ratios from the benchmark matrix | 589 | 0 | Benchmark_Matrix | Benchmark_Compare | IF, IFERROR, AND, ISNUMBER, SUMIFS | Ratios | Medium | Keep; inherits source quality of Benchmark_DB. |
| 20 | Market_Benchmark | OUTPUT | Model against market references (Source_Register) | 77 | 0 | Source_Register, Timeline, KPIs, Annual, Ops, Financing | Calibration | IFERROR, INDEX, MATCH, SUM, AVERAGEIFS | Comparisons | High | Depends on SR01 to SR04 (M-KOPA) and SR19 (ESMAP): both unverified. |
| 21 | Calibration | OUTPUT | Benchmark based diagnostics (net margin, collection rate and others) | 21 | 0 | Source_Register, Market_Benchmark, KPIs | none | IFERROR, INDEX, MATCH, IF, TEXT | Diagnostic flags | High | Suspend M-KOPA reference; mark ESMAP reference UNVERIFIED. |
| 22 | Company_Cases | REFERENCE | Lessons from scaled PAYGo companies (text) | 0 | 0 | none | none | none | Text | Medium | Each statement to be sourced or removed. |
| 23 | Source_Register | REFERENCE | 23 graded sources (A to E scale) | 23 | 17 | none | Calibration, Market_Benchmark | none | SR01 to SR23 | High | Replace by the A to D register with the full field list; fix SR14 and SR15 grade. |
| 24 | Benchmark_Matrix | CALCULATION | Company-year by line item matrix from Benchmark_DB | 550 | 5 | Benchmark_DB, Timeline, FS, KPIs, Financing, Ops | Benchmark_KPIs | SUMIFS, IF, COUNTIFS, INDEX, AVERAGEIFS | Matrix | Medium | Keep. |
| 25 | Benchmark_DB | REFERENCE | Raw benchmark records loaded from CSV (37 records, 23 usable) | 37 | 208 | none | Benchmark_Matrix | IF | Records | High | Add period, definition, page and status per record. |
| 26 | Annual | OUTPUT | Annual income statement, balance sheet and cash flow from FS | 250 | 5 | FS, Timeline | Market_Benchmark | SUMIFS, INDEX | Annual statements | Medium | Keep. |
| 27 | FS | CALCULATION | Monthly integrated statements: income statement, balance sheet, cash flow | 3,593 | 0 | Financing, Ops, Costs, Timeline, Inputs | Annual, Benchmark_Matrix, Checks, Covenants, Financing, KPIs | MAX, IF, SUM, ROUND, MIN | Statements, cash, equity | High | Add explicit roll forward checks (equity, debt, receivables). |
| 28 | Ops | CALCULATION | Portfolio engine: units, active accounts, due, collected, receivables, write offs, recoveries by tier and month | 8,966 | 0 | Products, Timeline, Curves, Inputs, RBF_Engine, Credit_Engine | Benchmark_Matrix, Cohort_T1, Cohort_T2, Cohort_T3, Cohort_T4, Cohort_T5 | IF, SUMIFS, INDEX, SUM | Portfolio flows | High | Core engine; add cohort to portfolio reconciliation check. |
| 29 | RBF_Engine | CALCULATION | Sales, repayment linked, ownership linked and hybrid RBF; verification lag; receipts | 2,214 | 0 | Inputs, Timeline, Products, Ops, Curves, Vintage_Input | Investment_Summary, Ops | IF, INDEX, CHOOSE, AND, SUM | RBF receipts | High | Separate claim, verification and disbursement; confirm RBF never enters customer collections. |
| 30 | Credit_Engine | CALCULATION | Proxy and actual DPD buckets, staging, indicative ECL, borrowing base by tier | 16,010 | 0 | Credit_Assumptions, Credit_Input, Products, Ops, Timeline | Checks, Covenants, Credit_Portfolio, Ops | IF, INDEX, CHOOSE, SUM, IFERROR | Credit metrics | High | Keep; label ECL as analytical. |
| 31 | Vintage_Engine | CALCULATION | Cohort KPIs by checkpoint from Vintage_Input | 17,980 | 0 | Vintage_Input, Products, Curves, Credit_Assumptions | Vintage_Dashboard | IF, IFERROR, MIN, MAX, SUMIFS | Cohort metrics | High | Rebuild repayment rate to PERFORM 2026 where data allow. |
| 32 | Costs | CALCULATION | Operating costs, working capital, capex | 1,278 | 0 | Ops, Inputs, Timeline | FS, Valuation | SUM, SUMIFS | Costs | Medium | Keep. |
| 33 | Financing | CALCULATION | Equity, USD term loan, receivables facility or securitisation, borrowing base, equity top up | 1,217 | 0 | Inputs, Timeline, FS, Ops | Benchmark_Matrix, Checks, Covenants, Credit_Portfolio, FS, Investment_Summary | IF, MAX, MIN, AND, SUM | Debt, equity, facility | High | Add debt roll forward check. |
| 34 | Curves | CALCULATION | Per unit survival and repayment curves by tier and scenario | 3,685 | 0 | Products, Inputs, Credit_Assumptions | Cohort_T1, Cohort_T2, Cohort_T3, Cohort_T4, Cohort_T5, Ops | IF, AND, MAX, INDEX, SUM | Curves | High | Keep. |
| 35 | Cohort_T1 | CALCULATION | Vintage matrix for Tier 1 | 7,740 | 0 | Curves, Ops, Timeline | Ops | INDEX, SUM | Cohort flows | Medium | Keep. |
| 36 | Cohort_T2 | CALCULATION | Vintage matrix for Tier 2 | 7,740 | 0 | Curves, Ops, Timeline | Ops | INDEX, SUM | Cohort flows | Medium | Keep. |
| 37 | Cohort_T3 | CALCULATION | Vintage matrix for Tier 3 | 7,740 | 0 | Curves, Ops, Timeline | Ops | INDEX, SUM | Cohort flows | Medium | Keep. |
| 38 | Cohort_T4 | CALCULATION | Vintage matrix for Tier 4 | 7,740 | 0 | Curves, Ops, Timeline | Ops | INDEX, SUM | Cohort flows | Medium | Keep. |
| 39 | Cohort_T5 | CALCULATION | Vintage matrix for Tier 5 | 7,740 | 0 | Curves, Ops, Timeline | Ops | INDEX, SUM | Cohort flows | Medium | Keep. |
| 40 | Credit_Input | INPUT (company data) | Template for company monthly DPD history by tier (empty in the default model; synthetic history in the case) | 0 | 0 | none | Checks, Credit_Engine | none | Company data | Medium | Label COMPANY DATA; add a history summary (collection rate by history year). |
| 41 | Vintage_Input | INPUT (company data) | Template for company cohort history (empty by default) | 0 | 0 | none | Checks, RBF_Engine, Vintage_Dashboard, Vintage_Engine | none | Company data | Medium | Add PERFORM 2026 input fields (applied payments, free use period). |
| 42 | Timeline | CALCULATION | Dates, FX path, indices | 362 | 60 | Inputs, Scenarios | Annual, Benchmark_Matrix, Cohort_T1, Cohort_T2, Cohort_T3, Cohort_T4 | EOMONTH, INT, CHOOSE, SUM | FX path | Medium | Keep; document FX translation and transaction effects. |
| 43 | Glossary | DOCUMENTATION | PAYGo and SHS terms | 0 | 0 | none | none | none | Definitions | High | Align with PERFORM 2026; mark 2021 terms as historical. |
| 44 | Checks | CONTROL | 24 integrity checks and the master check; 5 readiness flags | 30 | 0 | Products, Credit_Engine, Inputs, Vintage_Input, Credit_Assumptions, FS | Contents, Cover, Dashboard, Investment_Readiness, Investment_Summary | IF, MIN, ABS, SUMPRODUCT, COUNTIF | Master check | High | Add the requested reconciliations (see 01_PROJECT_AUDIT section 6). |

Numeric constants are counted outside the label columns A and B. On KPIs, Annual, Valuation, Benchmark_Matrix and Timeline they are period indices (year or month numbers), not assumptions.

## Classification

| Class | Sheets |
|---|---|
| INPUT | Inputs, Products, Scenarios, Credit_Assumptions, Consumer_Risk, Credit_Input, Vintage_Input |
| CALCULATION | Timeline, Curves, Ops, Cohort_T1 to T5, Credit_Engine, Vintage_Engine, RBF_Engine, Costs, Financing, FS, Valuation, Benchmark_Matrix, Benchmark_KPIs |
| OUTPUT | Cover, Investment_Summary, Investment_Readiness, Dashboard, KPIs, Credit_Portfolio, Vintage_Dashboard, Covenants, Unit_Economics, Annual, Benchmark_Compare, Market_Benchmark, Calibration |
| CONTROL | Checks (and the automatic gates on Investment_Readiness) |
| REFERENCE | Source_Register, Benchmark_DB, Company_Cases, Sensitivity (static) |
| DOCUMENTATION | Contents, Glossary |

Sheets named in the master context but not present in v0.7: PERFORM_2026, Sources_Standards, Investment_Grade, Disclaimer. Their functions are partly covered by Vintage_Dashboard, Source_Register, Investment_Readiness and the Cover notes. Whether to add them is a v0.8 design decision (see CHANGE_PLAN.md).

## Engine map (brief section 19)

| Engine | Sheets | Reconciles to the next engine through | Explicit check today |
|---|---|---|---|
| A Customer economics | Consumer_Risk, Products | Instalment and burden by tier | Affordability flags (informational) |
| B Product economics | Products | Price plan to Curves and Ops | Down payment not above cash price; tenor within horizon |
| C Unit economics | Unit_Economics, Curves | Unit flows; not reconciled to Ops totals | None |
| D Credit | Credit_Assumptions, Credit_Engine, Credit_Portfolio | DPD buckets to gross receivables | Yes (proxy and actual) |
| E Portfolio | Ops | Due, collected, write offs to FS | Gross receivables never negative |
| F Cohort / vintage | Cohort_T1 to T5, Vintage_Engine | Cohort sums to Ops | None explicit |
| G Receivables | Ops, FS | Opening + additions - collections - write offs = closing | None explicit |
| H Cash flow | FS | Cash flow to balance sheet cash | Final month only (FS!BL33 vs BL65) |
| I FX | Timeline, FS | Translation of USD debt and hardware | None |
| J RBF | RBF_Engine | Claims, verification and receipts to FS other income | Mode and weights only |
| K Financing | Financing | Drawdowns, repayments, balances | Facility within limit and borrowing base |
| L Valuation | Valuation | FCFF from FS; equity flows to IRR | Terminal growth below discount rate |
| M Investment readiness | Investment_Readiness | Automatic gates from Checks, Covenants, Unit_Economics, Credit and Vintage | Itself |
| N Benchmarking | Benchmark block | Reads outputs; no feedback | None |
| O Scenarios | Scenarios, Inputs | CHOOSE on the selector | Selector valid |
| P Stress testing | Sensitivity (static) | Outside the workbook | Recomputed 3 Oct 2026 |

## Addendum: architecture of v0.8 (development build), 3 October 2026

The audit above describes v0.7 as found and is kept unchanged. v0.8 has 47 sheets (44 plus three). It also adds blocks to existing sheets. No sheet was deleted.

| Sheet or block | Class | Purpose | Inputs | Outputs | Risk | Status |
|---|---|---|---|---|---|---|
| Start (new) | DOCUMENTATION / OUTPUT | What to input, what is calculated, what it means, what to look at; provenance counts | Links only | Status lines, counts | Low | New in step 4 |
| PERFORM_2026 (new) | INPUT / OUTPUT | Company-reported PAYGo PERFORM 2026 KPIs, aggregated by summing numerators and denominators; labelled approximations | Section C template (company data) | KPIs by tier and portfolio; flags | Medium (data entry) | New in step 3; Checks row 41 |
| FX_Exposure (new) | OUTPUT | Currency map; transaction, remeasurement and translation effects by year | Timeline FX effect rows | Annual table | Low (presentation) | New in step 4 |
| Timeline, rows 13 to 24 | CALCULATION | Monthly FX effects | Costs, Financing, Ops, FS | FX_Exposure | Low | New in step 4 |
| RBF_Engine, claim cycle | CALCULATION | Eligibility, claims, verification, disbursement, working capital gap | Ops units, Products RBF | Gap in USD and LCY | Low | New in step 4; Checks row 38 |
| Investment_Readiness, columns G to L and decision block | CONTROL | Evidence per gate; GO / CONDITIONAL GO / STOP rule | Manual evidence fields | Decision and reason | Medium (rule design) | New in step 4 |
| Provenance columns (Inputs E, Products I, Credit_Assumptions E, Scenarios I) | INPUT | Data provenance labels | Label lists | Counts on Start | Low | New in step 4 |
| Scenarios rows 13 and 18 to 26 | INPUT / DOCUMENTATION | Input set loaded; scenario architecture | Input set selector | Active case label | Low | New in step 4 |
| Dashboard | OUTPUT | 39 labelled metrics by year, plus charts | Annual, KPIs, Valuation, FX_Exposure, readiness | Display only | Low | Rebuilt in step 4 |
| Checks | CONTROL | 38 tests (24 in v0.7); master check on C44; 7 readiness flags | All engines | Master check | Low | Steps 2 to 4 |
| Credit_Portfolio, rows 34 to 41 | CALCULATION | Company history summary (collection rate by history year) | Credit_Input | History block | Low | New in step 2 |
