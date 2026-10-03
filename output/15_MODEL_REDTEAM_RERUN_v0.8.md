# 15 Model red-team rerun: MODEL 2, v0.8 (development build)

Status: rerun of the full battery in report 14 on the workbooks rebuilt at generator commit 813c3d5, carried out on 3 October 2026. The model, the generator and the repository were not modified. The deliverables are this report, `15_MODEL_REDTEAM_RERUN_v0.8_evidence.xlsx` and a replaced `14_ExcelQA_Replay.bas`.

| File | MD5 tested |
|---|---|
| `volumes/02-solar-home-systems/model/AEF_SHS_PAYGo_Model_v0.8-dev.xlsx` | 7df769c7f4d75d1c83f33ab8ead1c933 |
| `volumes/02-solar-home-systems/case-study/SolaraPay_Case_Model_v0.8-dev.xlsx` | d71be26651028f00cf8880e9211d2aeb |

## 1. Verdict

**The fixes work in LibreOffice and the second engine.** Of the seven High and Medium findings in report 14, five are closed (H1, M2, M4, M5, M6), M1 is closed in mechanism, and M3 is partly closed. The five Low findings are unchanged.

**The rebuild introduces one new High risk for Excel.**

* Checks!C26 is now 9,656 characters long, above Excel's 8,192-character formula limit.
* LibreOffice and the Python engine accept it, so none of the tests in this rerun can show the effect.
* Excel is expected to refuse or strip the formula on opening. That would remove every range test added for M4, and the master check could then read OK on invalid inputs.

**Not certified for Microsoft Excel**, which was not run.

## 2. Counts

| Item | Count |
|---|---|
| Recalculated runs with changed inputs (UNO), both workbooks | 644 (302 default, 342 SolaraPay); all 644 restores reproduced the baseline |
| PASS / GAP / OBSERVATION | 639 / 2 / 3 |
| Mode grid (scenario x structure x RBF mode x credit mode x DSCR basis 0 to 2) | 288 (144 per workbook) |
| Invalid-input runs that must read ERROR | 140 of 140 ERROR on master check and Cover, decision STOP |
| Extended inputs (14 M4 inputs, 6 valid boundaries and others) | 52 PASS, 2 GAP (household income 0, both workbooks) |
| Economic direction assertions | 148, all PASS |
| Sensitivity rows recomputed live | 30, worst relative difference 1.2e-12 |
| Formula cells compared across engines | 203,034 (2 x 101,517) |
| File-level recalculations and save cycles | 6, with 0 value differences |
| VBA replay cases (rebuilt module, LibreOffice dry run only) | 79: 77 MATCH; 2 differ only in LibreOffice's error-cell count |

## 3. Status of the findings in report 14

| ID | Finding | Status | Evidence |
|---|---|---|---|
| H1 | Release-path copy stale | **Closed** | output/02 MD5 now equals the default model (7df769c7...). |
| M1 | Gate 10 unreachable with debt | **Closed (mechanism), with an observation** | See note below the table. |
| M2 | Stale QA statements | **Closed** | 06 (line 36) and FINAL_QA_REPORT (line 32) state 2 of 23 and 4 of 23, STOP on the failed DSCR test; 06 line 78 qualifies the old CONDITIONAL GO test. |
| M3 | Validation not blocking; error cascades | **Partly closed** | See note below the table. |
| M4 | Fourteen nonsensical inputs accepted | **Closed for 13 of 14** | 13 now read ERROR (row 26, or 16, 20, 25), including amortisation 0, drawdown month 0 or 61, hazard 150%, advance rate 150%, collection rate 120%, negative daily rate, negative tax, current share 150% and a negative RaR share. Six valid boundaries stay OK: tax 0, advance rate 100%, amortisation 60, drawdown month 60, RBF lag 0, hazard 0. Still accepted: Consumer_Risk!C8 = 0 (N3). |
| M5 | Actual history on the forecast timeline; dates unread | **Closed** | See note below the table. |
| M6 | Seven planted data faults passed | **Closed** | All 7 read ERROR through the intended row (see below). Six false-positive probes on the case's real data stay OK (see below). |
| L1 | Peak equity equals initial equity | Open | Unchanged: USD 10.0m (default) and 9.0m (case) wherever no top-up occurs. |
| L2 | Weak evidence rules | Open | A single-space "where held" and "signed off", lower-case "met" and one Credit_Input observation per tier each still give GO 23 of 23 on the case. |
| L3 | Stranded inventory | Open | In the default sales collapse, inventory stays at LCY 13.2m with no further sales. |
| L4 | Engine difference on SUMIFS "<>" | Open | Same 4 cells: PERFORM_2026!C21:E21 and C22. |
| L5 | LibreOffice save re-encoding | Open (information only) | Validation rules now survive saving, with the Stop style. |

**M1 note.** Inputs!C88 is the new DSCR covenant basis (validated 0 to 2; any other value sets Checks row 26).

* Basis 0 gives 0 years below the minimum in all 96 basis-0 mode runs. With every gate evidenced on the case, it reaches GO (23 of 23); with gate 21 or gate 3 open it reaches CONDITIONAL GO (22 of 23). The default with all manual gates met reads STOP at 19 of 23, because gates 18, 20 and 22 need actual data.
* Basis 1 (the default) is unchanged: 2 of 23 and 4 of 23, STOP on a failed test.
* Basis 2 (cash basis) still gives 2 to 5 years below 1.20x in every mode run. The case DSCR for Years 1 to 5 is (18.85), (2.10), 0.49, 1.96 and 3.81, so gate 10 still fails.
* The decision remains STOP in all 288 mode runs. Only basis 0 allows the readiness paths to open.

**M3 note.**

* All 17 validation rules now have `showErrorMessage="1"` and the Stop style. New rules cover Inputs!C32, C39, C83 and C88, and Consumer_Risk!C5.
* The scenario and RBF mode selectors are clamped. Invalid values (0, 4 or 5, text, blank, (1)) now produce 0 error cells, against 77,069 and 4,782 before, and the master check still reads ERROR.
* Other invalid inputs still cascade, although the master check reads ERROR in each case:

| Invalid input | Error cells |
|---|---|
| RBF switch set to text | 8,684 |
| Tenor 0 | 7,630 |
| FX 0 or blank | 52,460 |
| Depreciation life 0 or blank | 3,399 |
| RBF lag (1) | 343 |

**M5 note.**

* Credit_Portfolio row 9 now shows the period end of the data. In the case, E9 = 31 January 2024 under model month 1.
* Checks row 19 fires when Credit_Input!B9 is earlier than B8, and when the Tier 2 date B72 is moved by 3 days or by one month.
* The data still sits in model-month columns, but it is now labelled.

**M6 note.** The intended rows fire for each planted fault:

* Row 36: a blank checkpoint gap, and negative units.
* Row 41: M43 above C43, and the PvFin numerator above its denominator.
* Row 19: negative balances, collections at 10 times the instalments due, and dates out of order.

The six false-positive probes that stay OK are:

* a history of 24 months in every tier;
* one tier shorter than the others;
* blanks at the later checkpoints of a young cohort;
* flat collections;
* 100% repayment;
* a month with zero balances.

## 4. New findings

### N1 (High). Checks!C26 exceeds the Excel formula length limit

* **Reproduce:** Checks!C26 is 9,656 characters in both workbooks. Excel's limit is 8,192, and no other formula exceeds 6,193 (Checks!C19).
* **Expected effect in Excel (not observed, because Excel was not run):** a repair prompt on opening, with the formula removed. That would remove the structural and range tests (M4) and the DSCR basis test. Because the file stores no cached values, the master check could then read OK on invalid inputs.
* **Fix:** split row 26 into two or three check rows, each under 8,192 characters, or move the range tests to helper cells. Add a formula length assertion to `build_shs_model.py`.

### N2 (Low). Clamped selectors show a valid-looking case

* **Reproduce:** Inputs!C5 = 0, text or blank makes Cover!E37 read "Calibrated case, Base"; with 4 it reads "Severe". All outputs show that case.
* **Why it matters:** only the master status reads ERROR (Cover E35, Start C4, Contents B10, Investment_Summary B5, Dashboard E3), so a reader can mistake the result for a valid run.
* **Fix:** show "INVALID SELECTOR" in Scenarios!G12 and on Cover when Checks row 14 is not 0.

### N3 (Low). Household income 0 clears the affordability flag

* **Reproduce:** Consumer_Risk!C8 = 0 makes C10 = IFERROR(C9/C8,0) = 0, so the C13 flag is 0 and the master check stays OK.
* **Fix:** make income at or below 0 invalid in row 26, or set the flag.

## 5. Regression checks

* **Baseline unchanged.** The default reads IRR 46.4%, EV USD 15.6m, 2 of 23 STOP; the case reads IRR 29.0%, 4 of 23 STOP. The Sensitivity table is reproduced exactly.
* **No false positives** from the new data checks on the case's real data (section 3, M6).
* **Selector clamping hides no error value.** The master check, the Cover status and the decision all read ERROR and STOP in every invalid run. The residual risk is N2.
* **Formula count is 101,517 in both files**, with no volatile functions, array formulas, functions newer than Excel 2010 or external links, and no circular reference (cell graph and LibreOffice).
* **Formula length breaks the Excel limit** (N1).
* **Cross-engine agreement:**
  * Default: 101,515 of 101,517 cells equal; the other 2 differ by the known residue of LCY 0.0000011.
  * Case: 101,513 of 101,517 equal; the other 4 differ in the known SUMIFS cells (L4).
* **Save cycles:** two LibreOffice saves change no value; the formulas, the 17 validation rules (with Stop style) and the 6 named-series charts are preserved.

## 6. Replay module

`14_ExcelQA_Replay.bas` was regenerated from this rerun. It now has 79 cases: 34 default, 45 SolaraPay. It includes DSCR basis 0, 1 and 2, the GO and CONDITIONAL GO paths with basis 0, invalid basis values, the M4 inputs and the M6 faults, with expected values from LibreOffice on this build.

It has not been run in Excel. Its dry run in LibreOffice VBA-compatibility mode completed with 77 of 79 cases matching; the other 2 differ only in the error-cell count. It is also the quickest way to confirm N1: if Excel strips Checks!C26, the M4 cases will show "OK" where "ERROR" is expected.

## 7. Not tested

Same scope as report 14, section 7: no Microsoft Excel, no locale variants, no review of the generator code or of the realism of the assumptions, and no other products.
