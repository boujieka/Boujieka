# Project audit: Book 2, PAYGo Solar Finance, and MODEL 2 (v0.1 book, v0.7 model)

Prepared 3 October 2026. Audit only: no existing book, model, manual or case file has been modified. Companion documents: `05_MODEL_ARCHITECTURE.md`, `07_SOURCE_VERIFICATION_REPORT.md`, `08_MKOPA_SOURCE_RECONCILIATION.md`, `09_BOOK_MODEL_CROSS_REFERENCE.xlsx`, `CHANGE_PLAN.md`.

## 1. What was tested, and how

| Test | Method | Result |
|---|---|---|
| Workbook opens and recalculates outside the generator | LibreOffice 24.2 headless, full recalculation forced on load, default model and SolaraPay case | Both open; 99,438 formula cells each; no error values |
| Formula results | LibreOffice values against the independent formula engine used in earlier QA | All cells agree; largest difference 1.1e-6 LCY in one cell (FS!C64, Financing!C10) |
| Circular references | LibreOffice reports a circular reference as an error (Err:522) when iteration is off | None, at default and case inputs |
| Macros and external links | Package inspection | None |
| Hardcoded numbers on calculation sheets | Scan of numeric constants outside label columns | None apart from period indices |
| Sensitivity table (15 cases) | Each case set up in the workbook and recalculated in LibreOffice | All 15 match the static table to 1e-13; master check OK in every case; one IRR convergence defect (Downside) |
| Book figures | Extraction of all 3,242 figures from the 18 source files; match against 253,000 evaluated cells; 28 headline claims checked by hand against LibreOffice values | See section 4 and the cross-reference workbook |
| External sources | Reading of the eight documents provided | See 07_SOURCE_VERIFICATION_REPORT.md |
| Microsoft Excel | Not available in this environment | NOT TESTED |

Two claims in the book were tested rather than repeated. "No macros and no circular references" holds in LibreOffice. "Reproduced to rounding precision by an independent shadow calculation" needs rewording: the shadow was written by the same developer, so it is a secondary calculation check. The LibreOffice recalculation is now an independent engine check of the formulas, though not of the modelling logic.

## 2. Current architecture

**Book v0.1.** 103 pages, about 52,000 words: front matter, sixteen chapters, Annexes A to H. Each chapter ends with points for the investment committee and a section on working with the model. The analytical chain is present in the order of the chapters (customer and affordability in Ch 2, product in Ch 4, cohorts and credit in Ch 6 to 8, receivables, cash and FX in Ch 10, funding in Ch 11 and 12, RBF in Ch 13, stress in Ch 14, investor view in Ch 15, the case in Ch 16), but it is never drawn or named as a chain, and valuation has no chapter of its own.

**Model v0.7.** 44 sheets in seven groups (input, calculation, output, control, benchmarking, reference, documentation). The detail is in `05_MODEL_ARCHITECTURE.md`.

**Case.** SolaraPay Ltd, Republic of Kivara, both fictional, with a synthetic 24 month history loaded into Credit_Input. The case workbook is the v0.7 model with the case inputs and history.

**Satellite products.** Manual (15 pages), case study (15 pages), templates T01 to T08, decision tools D1 to D6, quick reference guide, video course (18 modules). Several carry a v1.0 label, which conflicts with the rule that nothing is 1.0 before full verification.

## 3. Strengths to preserve

1. The model is formula driven end to end: no hardcoded numbers on calculation sheets, no macros, no circular references, a master check, and full agreement between two calculation engines.
2. Proxy and Actual credit modes, with company history templates and reconciliation of DPD buckets to gross receivables.
3. Readiness gates that never award an "investment grade" label and that report unattractive results as they are (3 of 23 by default, 5 of 23 for SolaraPay).
4. The book's honesty conventions: SolaraPay is declared fictional; external figures carry secondary-reporting caveats; the 10% affordability threshold is described in Chapter 2.3 as "a policy choice ... not a law, a regulatory standard or an empirical boundary".
5. The M-KOPA conflict was already flagged as unresolved in the book and the register rather than silently resolved.
6. The book's treatment of growth distortion in portfolio ratios (Chapter 6.6, 7.3), lagged PAR, and the gap between booked margin and cash (Chapter 1.4).

## 4. Inconsistencies and errors found

| # | Finding | Where | Evidence | Severity |
|---|---|---|---|---|
| 1 | Downside investor IRR returns "n/a" when the workbook is recalculated in LibreOffice; the book and the static table give (22.9%) | Valuation!C39, formula `IFERROR(IRR(D20:I20,0.1),"n/a")` | Cash flows (4.0m) then 1.09m in Year 5 give (22.9%); with a second guess of (20%) LibreOffice returns (22.9%). Excel behaviour untested. | High (a quoted output does not appear in the workbook in at least one spreadsheet engine) |
| 2 | Sensitivity outputs are static values produced outside the workbook | Sensitivity, Investment_Summary rows 59 to 61 | Generated by the secondary calculation; now confirmed in the workbook, but they do not update with inputs | Medium |
| 3 | Manual and video say the Checks sheet runs 25 integrity tests; the workbook has 24; the volume README says 13 | manual/user_manual.md line 73; video Module 17; README line 113 | Checks rows 5 to 28 | Medium (factual error in published material) |
| 4 | SolaraPay historical collection rates (77.4%, 69.3%) are computed outside the workbook, over windows of 11 and 12 months | tools/case_exhibits.py lines 94 to 95 | No cell in the case workbook holds either figure | Medium (traceability) |
| 5 | Chapter 1.7 calls the shadow calculation "independent" | ch01.md | Same developer | Medium (wording) |
| 6 | The master context describes the 20% FX case as a "Severe FX case"; the book correctly calls it a Base case with a 20% depreciation lever | Master context section 5 | Sensitivity row 13 | Low (context note; book is right) |
| 7 | Contents index lists sheets out of tab order and only Cohort_T1 of the five cohort sheets | Contents | Sheet inspection | Low |
| 8 | Readiness sheet note says the model is "NOT investment grade until company data are loaded and independently validated", implying it could become investment grade | Investment_Readiness!A2 | Wording | Low |
| 9 | Source_Register grades SR14 and SR15 (BBOXX) as A while saying the original was not reviewed; SR19 (ESMAP) graded B while unverified | Source_Register | Register text | Medium |
| 10 | Chapter 2.3 calls the SolaraPay plan "its real plan"; the case is fictional | ch02.md | Wording | Low |
| 11 | The book's illustrative "Tier 2 plan" (cash price LCY 40,000, daily rate 72) differs from the model's default Tier 2 (39,000, daily rate 77) and the instalments differ (2,190 against 2,342) | Ch 1.4, 2.3, 9 | Products!D13 to D16, D33 | Low (both labelled, but the shared name invites confusion) |

The automated extraction flagged eight "model default" figures that match no cell. All eight are worked examples in the text whose sentence mentions the workbook; each was checked and its arithmetic is correct (for example 820 × 70% = 574; 1 ÷ 1.20^0.5 = 0.9129; 14,000 ÷ 130 = USD 108 against 14,100 ÷ 156 = USD 90, a fall of about 16%).

## 5. Unsupported or unverified claims

See `07_SOURCE_VERIFICATION_REPORT.md` for the full list. The material ones:

* **ESMAP 62% collection rate (2023)**: unverified; definition unknown; used in Calibration as a reference.
* **M-KOPA FY2024 revenue**: the filing provided is a UK subsidiary whose revenue is GBP 1.7m of carbon credit sales. Neither USD 416m nor USD 253.5m is supported. Calibration's net margin reference rests on these figures.
* **BBOXX administration date (19 May 2025)**: pending the Gazette notice.
* **MTF thresholds, GOGLA investment (USD 299m), Sun King and d.light securitisation figures, SEforALL UEF**: pending primary documents; all already carry secondary caveats in the book.

## 6. Model logic and control risks

| Area | Finding | Risk |
|---|---|---|
| Checks coverage | 24 tests. Present: balance sheet balances (all months), cash ties to balance sheet (final month only), facility within limit and borrowing base, DPD buckets reconcile (proxy and actual), non-negative receivables and ECL, input validity. Missing as explicit tests: cash flow reconciliation every month; receivables roll forward (opening + originations − collections − write offs = closing); debt roll forward; equity roll forward; cohort totals = portfolio totals; vintage engine reconciliation; RBF claims to receipts; valuation reconciliation (FCFF to FS); scenario consistency | Medium. Several of these identities are probably true by construction, but they are not tested. |
| IRR robustness | Single guess of 10% | High (see finding 1) |
| PERFORM alignment | Collection rate is the headline credit metric; repayment rate on Vintage_Dashboard not built to 2026 rules; no PvFin, no @90 days | High |
| Accounting labels | "Simplified IFRS 9: no staging", "IFRS 9-style staging", "not an IFRS 9 PD" are present; there is no general statement that the model treatment is analytical and is not a determination of accounting treatment | Medium |
| Provenance | Inputs carry "Illustrative placeholder" notes, but there is no consistent MODEL ASSUMPTION / COMPANY DATA / EXTERNAL EVIDENCE / CALIBRATED ASSUMPTION / UNVERIFIED label | Medium |
| Scenario architecture | Base, Downside, Severe plus Proxy and Actual modes. No explicit Management Case and Calibrated Case layers; the SolaraPay distinction lives in two separate workbooks | Medium |
| FX | Translation of USD debt and USD hardware cost are modelled; there is no single FX exposure table (revenue, cost, debt and equity currencies, hedges, translation against transaction effect) | Medium |
| RBF | RBF is recognised as other income on a cash basis and does not enter customer collections (to be confirmed formula by formula in Phase 9); claim, verification and disbursement are not shown as separate steps | Medium |
| Benchmarks | Records carry source and grade but not page, definition alignment or a comparability warning | Medium |

## 7. Accounting and KPI definition risks (book)

* IFRS appears 20 times. The book explains the model's simplifications (Ch 8.4) and points readers to auditors (Ch 8.8), but it has no statement that the model treatment does not constitute a determination of the accounting treatment under IFRS. Chapter 8.4 also characterises the simplifications as "conservative", which is an analytical judgement and should be framed as such.
* Chapter 7.1 to 7.2 present collection rate, receivables at risk and write offs as PERFORM's standard metrics, with repayment and ownership rates as later additions. Under the 2026 standard the five KPIs are the four Repayment Rate variants and Ownership Rate @2x, and the collection rate must not be used as a substitute. The chapter needs restructuring, not a footnote.
* The book's repayment rate (cumulative collections over cumulative instalments due) is close to RR Paid vs Plan but omits the 2026 rules: payments applied to due instalments, daily normalisation, exclusion of prepayments, inclusion of write offs, start after any free-use period.

## 8. UX and publication issues

* Dashboard holds charts and two status cells; the requested metric set is not there.
* No Start or Instructions sheet; the Contents sheet does part of that job.
* Book: few figures; the chain and the six-way distinction (viability, accounting profit, cash, portfolio quality, funding capacity, readiness) are not visualised.
* Title, series and numbering in all products still read "Africa Energy Finance, Volume 2, Solar Home Systems". The target is BOOK 2, PAYGo SOLAR FINANCE, within the Africa Energy Finance / Business & Financial Models family. The repository README lists a six-volume plan that conflicts with the fixed three-book series.

## 9. Commercial product issues

* Satellite products labelled v1.0 before verification.
* Product names not aligned with the MODEL 2, MANUAL 2, CASE 2 architecture.
* The narrated video course uses a synthetic voice; it should be presented as a draft until a human recording is made.

## 10. What this audit did not yet do

* A line-by-line read of every paragraph for wording and accounting precision (Phase 2 proper). The 3,242 extracted figures include 206 classed as text arithmetic to check in place and 1,448 weak or round-number matches that a script cannot settle.
* Formula-by-formula review of the sixteen engines (Phase 9). This audit tested results, controls and dependencies, not each formula's logic.
* A test in Microsoft Excel.
