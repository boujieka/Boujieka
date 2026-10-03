# 06 Model validation report: MODEL 2, v0.8 (development build)

Status: prepared 3 October 2026 on the files committed to branch `ccr-d5d6abff-p7fc0j`. This report covers mechanical validation: whether the workbook computes what it says it computes. It does not validate the realism of any assumption, which is the subject of the book.

## 1. Objects validated

| Object | File | Formulas | Sheets |
|---|---|---|---|
| Default model (illustrative inputs, fictional company) | `volumes/02-solar-home-systems/model/AEF_SHS_PAYGo_Model_v0.8-dev.xlsx` (copied to `output/02_PAYGO_SOLAR_FINANCE_MODEL_v0.8-dev.xlsx`) | 100,857 | 47 |
| SolaraPay case (calibrated inputs, synthetic 24 month history) | `volumes/02-solar-home-systems/case-study/SolaraPay_Case_Model_v0.8-dev.xlsx` | 100,857 | 47 |

Both files are built from one generator, so the formula structure is identical. They differ only in their inputs and the loaded history. No macros. No external links. No circular references.

The file keeps the suffix "-dev". It will take the release name `02_PAYGO_SOLAR_FINANCE_MODEL_v0.8.xlsx` only after the test in Microsoft Excel (section 7).

## 2. Methods

| # | Method | What it establishes | Limits |
|---|---|---|---|
| M1 | Full recalculation in LibreOffice Calc (headless), then a scan of every formula cell for error values | The workbook opens and recalculates in a second spreadsheet engine without #REF!, #DIV/0!, #VALUE!, #NAME? or circularity errors (Err:522) | LibreOffice is not Excel |
| M2 | Independent formula engine (the evaluator used since v0.6) on the same file, compared cell by cell with M1 | Two engines agree on every formula cell | Both read the same formulas: a wrong formula computed correctly passes |
| M3 | Secondary calculation written separately by the model's developer, compared on 15 headline outputs | The formulas implement the intended logic | Same developer as the workbook, so it is not an independent review |
| M4 | The 38 integrity tests on *Checks* (master check on Checks!C44) | Internal consistency of statements, roll forwards and engines, month by month | Tests only what they test |
| M5 | Fault injection: a known error is planted and the intended test must fire | The tests detect what they claim to detect | Done on a sample of faults (section 5) |
| M6 | 15 stress and sensitivity cases recomputed inside the workbook and compared with the static table | The static Sensitivity table equals what the workbook itself produces | Default and case inputs only |

## 3. Results

| Test | Default model | SolaraPay case |
|---|---|---|
| M1 error values after recalculation | 0 of 100,857 | 0 of 100,857 |
| Master check | OK | OK |
| M2 engine against LibreOffice | Agreement on every formula cell except one value. The equity top-up total (FS!C64 and Financing!C10) shows LCY 0.0000011 in the engine and 0 in LibreOffice: a floating point residue of MAX(0, minimum cash less cash) | Not run on the case (same formulas; see section 6) |
| M3 secondary calculation | Worst relative difference 2.49e-14 across revenue, EBITDA, net income, cash, receivables, facility, collection rate, DSCR, FCFF, peak equity, EV, exit equity, IRR, MOIC and covenant months | Not run in the v0.8 cycle; the case's 15 cases are reproduced by M6 |
| M6 static Sensitivity against the workbook | 15 cases, worst relative difference 1.1e-13, master check OK in every case | 15 cases, worst relative difference 1.2e-12, master check OK in every case |
| Readiness gates (gate 10 includes the annual DSCR since 3 October) | 2 of 23; decision STOP on a failed test (gate 10: DSCR below 1.2x in Years 1 to 4) | 4 of 23; decision STOP on a failed test (gate 10, same reason) |
| Headline outputs | Investor IRR 46.4%, MOIC 6.72x, DCF EV USD 15.6m, peak equity USD 10.0m | Investor IRR 29.0%, MOIC 3.57x, DCF EV USD 6.1m, peak equity USD 9.0m |

The runway flag added in step 4 was given a threshold of LCY 1 so that the residue in M2 cannot make one engine report an equity top-up that the other does not.

## 4. The brief's 20 model QA tests

| # | Required test | Where it is tested | Result |
|---|---|---|---|
| 1 | Balance sheet balance | Checks row 5 (every month) | OK |
| 2 | Cash flow reconciliation | Checks row 11 | OK |
| 3 | Opening cash + movement = closing cash | Checks row 11 (every month; balance sheet cash equals closing cash) | OK |
| 4 | Receivables roll forward | Checks row 29 (Ops and FS, every month) | OK |
| 5 | Debt roll forward | Checks rows 31 (USD term loan in USD and LCY) and 32 (receivables facility) | OK |
| 6 | Equity roll forward | Checks row 33 | OK |
| 7 | Cohort totals = portfolio totals | Checks row 34 | OK |
| 8 | Vintage engine reconciliation | Checks rows 35 to 37 | OK |
| 9 | RBF claims and payments reconciliation | Checks row 38 (statements equal the engine; disbursements never above claims) | OK |
| 10 | Financing reconciliation | Checks rows 10, 21, 31, 32 | OK |
| 11 | Valuation reconciliation | Checks row 39 (EBITDA, tax, capex, Year 5 working capital) | OK |
| 12 | Scenario consistency | Checks rows 14, 40 | OK |
| 13 | No impossible negative balances | Checks rows 8, 9, 42 | OK |
| 14 | No unexplained hardcoded outputs | Inputs are blue cells with a provenance label; outputs are formulas. The static Sensitivity table is the one hardcoded output: it is dated, labelled static and reproduced by M6 | OK, documented |
| 15 | No broken references | M1: no #REF! | OK |
| 16 | No circular references unless documented | M1: no Err:522; the securitisation fee is lagged one month to avoid a circularity (Inputs note) | OK |
| 17 | No #REF! | M1 | OK |
| 18 | No #DIV/0! | M1 | OK |
| 19 | No #VALUE! | M1 | OK |
| 20 | No hidden material formula errors | M1 and M2 on every formula cell, M3 on headline outputs | OK, with the residue noted in section 3 |

## 5. Fault injection (M5)

* **Step 2 (12 faults):** cash, receivables, allowance, term loan, facility, equity, cohort size, Vintage_Input, RBF, valuation EBITDA, scenario lever and negative inventory. Each one switched the master check to ERROR through the intended test.
* **Step 3 (PERFORM_2026):**
  * a numerator above its denominator set the master check to ERROR;
  * an ownership count above the contracts at 2x set the master check to ERROR;
  * a cohort of 90 contracts raised the small cohort flag;
  * a tier marked Validated without data raised the conflict flag;
  * aggregation was checked by hand at 73.3%, 47.8% and 88.9%.
* **Step 4 (on the case):**
  * RBF claims understated for 12 months set the master check to ERROR through row 38, and the decision to STOP (failed test);
  * a manual gate marked Met without evidence was not counted, and was counted once the location and sign off were entered;
  * all critical gates evidenced gave CONDITIONAL GO (tested before gate 10 included the DSCR; at default covenants gate 10 now fails, so CONDITIONAL GO and GO need a different DSCR covenant: see 14, finding M1);
  * all 23 gates gave GO;
  * a failed master check gave STOP.

## 6. Engines and how they reconcile

| Engine (brief section 19) | Sheets | Reconciled by |
|---|---|---|
| A to C Customer, product and unit economics | Products, Curves, Unit_Economics, Consumer_Risk | Checks rows 6, 12, 13, 27; M3 on unit IRR |
| D Credit | Credit_Assumptions, Credit_Engine, Credit_Portfolio | Checks rows 9, 18 to 22, 25, 30 |
| E to G Portfolio, cohort and vintage, receivables | Ops, Cohort_T1 to T5, Vintage_Input, Vintage_Engine, PERFORM_2026 | Checks rows 29, 34 to 37, 41 |
| H Cash flow | FS, Annual | Checks rows 5, 7, 11 |
| I FX | Timeline, Financing, FX_Exposure | Checks row 31 (USD loan in USD and LCY); FX_Exposure presents existing calculations only |
| J RBF | RBF_Engine | Checks rows 23, 24, 38 |
| K Financing | Financing | Checks rows 10, 21, 26, 31 to 33 |
| L Valuation | Valuation | Checks rows 15, 16, 39; M3 |
| M Investment readiness | Investment_Readiness, readiness flags | Fault injection (section 5) |
| N Benchmarking | Source_Register, Market_Benchmark, Benchmark_*, Calibration | Only VERIFIED claims feed Calibration (all references suspended today) |
| O, P Scenarios and stress | Scenarios, Sensitivity | Checks rows 14, 40; M6 |

The case was not run through M2 or M3 in the v0.8 cycle. Its formulas are identical to the default model's, and it passes M1, M4 and M6. Running M2 on the case is listed as an open item.

## 7. What is not validated

1. **Microsoft Excel.**
   * The workbook has not been opened in Excel.
   * Behaviour that may differ: the IRR solver (three starting guesses are used), full recalculation on load, conditional formatting, chart rendering and data validation lists.
   * The test log required by readiness gate 17 does not exist yet.
2. **Assumption realism.** No test here says whether a hazard, price, cost or multiple is right. The defaults are illustrative and the SolaraPay history is synthetic.
3. **PERFORM 2026 calculations.** The workbook does not compute PERFORM KPIs. It aggregates company results and shows labelled approximations, which are not PERFORM figures.
4. **Accounting.** This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS. No accountant has reviewed it.
5. **Independence.** The secondary calculation (M3) was written by the model's developer. An external model review has not been done.
6. **Readiness rule.** The rule itself is a design choice, not a test result. That covers the choice of 13 critical gates and of three failed tests.

## 8. Conclusion

The workbook is mechanically sound in LibreOffice and in the independent engine. Its 38 tests detect the faults planted in them, and its static tables are reproduced by the workbook itself.

It is not validated for release. That needs the Excel test, an external model review and the readiness evidence that only a real company can supply.
