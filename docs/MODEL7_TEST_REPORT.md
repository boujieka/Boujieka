# MODEL 7 — Test Report (Bankable_Hydro_Model.xlsx)

Date: 2026-10-04. Tested file: `model/Bankable_Hydro_Model.xlsx` (38 sheets, 11,166 formulas), plus a fresh build from `model/build_model.py` made in the scratchpad. No repo file other than this report was changed. `git status` was clean after the build.
Engines: LibreOffice 24.2.7.2 (recalc.py) and the Python `formulas` 1.3.4 library as a second, independent engine. Microsoft Excel was **not** available, so every Excel statement below is inferred, not observed.
Scripts and outputs: `/tmp/claude-0/-home-user-Boujieka/92f87389-f945-55f4-b28c-902b8d98c6ca/scratchpad/modeltest/` (see Appendix).

## Summary verdict

**The numbers are right; the file as shipped is not yet safe to hand to an Excel user.**

- The calculation engine is sound. Two independent engines agree on all 11,166 formula cells of the base case (no cell differs by more than 1e‑6 relative). Both also agree on two stressed cases, except for one output (F‑02). There are no circular references. All 44 identity checks I computed in Python pass on the base case and on 25 of 31 scorable stressed copies. The other 6 fail only on F‑02. Eleven published snapshot scenarios reproduce exactly. 48 of 48 numbers spot-checked in the book match the model.
- **Excel compatibility issue (F‑01).** The shipped `.xlsx` was last saved by LibreOffice. In that save, 10,818 formulas and 4 charts refer to sheets whose names start with a digit (for example `=17A_STRUCTURES!$C$5`) **without the quotes Excel's formula grammar requires**. A strict Excel-grammar parser (`formulas`) refuses to load the file. The openpyxl build from `build_model.py` quotes these names correctly.
- **One output is wrong in several runs.** The developer IRR returns −1 (shown as −100%) in 6 of the published snapshot runs, even though a single valid IRR of 1.8–7.3% exists in each.

Findings by severity: **Critical 1 (still to be confirmed in Excel), High 1, Medium 3, Low 6.**

## Findings

| ID | Severity | Sheet/cell or name | Finding | Evidence | Recommended fix (in `build_model.py` terms) |
|---|---|---|---|---|---|
| F-01 | **Critical** (still to be confirmed in Excel) | All sheets; 10,818 / 11,166 formulas and chart series in `xl/charts/chart1-4.xml` | The shipped workbook was written by LibreOffice (`<fileVersion appName="Calc"/>`). LibreOffice drops the quotes around sheet names that begin with a digit: it writes `IFERROR(IRR(20_CASH_FLOW!$E$44:$AR$44,0.08),"n/a")`, where the build writes `'20_CASH_FLOW'!…`. Excel's grammar requires quotes for sheet names that begin with a digit (XlsxWriter's `quote_sheetname` applies the same rule). Excel will probably repair the file on open, drop the formulas, or give #REF!/#NAME?. The cause is that `tools/run_snapshots.py` ends with `subprocess.run([RECALC, MODEL])`, and the LibreOffice `store()` overwrites the quoted openpyxl file. | `formulas.ExcelModel().loads(shipped)` fails: `FormulaError: Not a valid formula: =17A_STRUCTURES!$C$5`. The same library loads the fresh openpyxl build and calculates it without error. A diff of the shipped file against the fresh build, after removing quotes, finds **0** formula or input differences. Only the quoting differs. | (a) Most robust: rename every sheet so that it starts with a letter (e.g. `S01_CONTROL_PANEL`, `M17_PROJECT_FINANCE`) wherever sheet names are created in `build_model.py` and in `REF`/`TSROW`; then any writer is safe. Or (b) in `run_snapshots.py`, recalculate a *copy* for verification and ship the openpyxl-saved file (it already has `calcPr fullCalcOnLoad="1"`). Or (c) post-process the LibreOffice output with a regex that quotes `(?<!')\b(\d\w*)!` references. Then open the file once in real Excel. |
| F-02 | **High** | `dev_irr` = `'01A_DEVELOPMENT'!C72` | `=IFERROR(IF(ABS(IRR(r,0.15))<1,IRR(r,0.15),IF(ABS(IRR(r,-0.05))<1,…,-1)),-1)`. The outer IFERROR catches the #N/A from the first guess and returns −1, so the −0.05 fallback runs only when guess 0.15 converges to \|r\|≥1. The developer cash flow has 3–5 sign changes but **one** root in [−50%, 100%]. The result also depends on the engine. | In LibreOffice, `IRR(r,0.15)` gives #N/A while `IRR(r,-0.05)`, `IRR(r,0.05)` and `npf.irr` converge (`irr_test.xlsx`). Snapshot `dev_irr = -1` vs true root: overrun96 4.04%, combined 7.02%, p90cf 7.32%, epc1_ov 6.51%, epc2_ov 4.02%, epc3_ov 1.78%. The second engine (`formulas`) gives 7.32% (p90cf) and 7.02% (combined) where LibreOffice gives −1. Book §"changes" (line 1809) says this formula was fixed for spurious roots. | Nest the fallbacks: `=IFERROR(IRR(rng,0.15),IFERROR(IRR(rng,0.05),IFERROR(IRR(rng,-0.05),"n/a")))`, optionally keeping the \|r\|<1 screen inside each branch. Return text `"n/a"`, not −1. Re-run the snapshots. |
| F-03 | Medium | `case`, `gen_case`, `lender_case` = `'01_CONTROL_PANEL'!C5:C7`; all data validations | One whole-number validation of 1–4 covers C5:C7 (`build_model.py` l.294–295), but `case` and `gen_case` accept only 1–3. A value of 4 passes validation. Every validation in the file also has `showErrorMessage="false"`, so Excel shows no error and accepts any value. | `case=4` → 8,349 `#VALUE!` cells and `chk_all` = "9 issue(s)"; `gen_case=4` → 6,647 `#VALUE!` cells. `lender_case=4` is valid (P90 ten-year) and runs cleanly. | Use separate validations: `C5:C6` between 1 and 3, `C7` between 1 and 4. Set `showErrorMessage=True, errorStyle="stop"` on every `DataValidation(...)`, including `dv_list`. |
| F-04 | Medium | `kpi_min_dscr` `'17_PROJECT_FINANCE'!C37`; `'30A_CLOSE_READINESS'!F22`; `'30_BANKABILITY'!C29/G29` | Placeholder values: min DSCR = **99** when there is no debt service, and IRRs = **−1** when they fail. The 99 flows into readiness gate F22 ("Minimum DSCR at or above the sizing target"), which then reads **MET**. Gate‑7 indicator G29 scores it 3/3. | `tariff_0` (debt sized to 0, revenue 0): `kpi_min_dscr = 99`, F22 = "MET". `flow_0`: the same. The gate verdict is saved only because other indicators fail. | In C37 return `"n/a"` when COUNT=0. In 30A F22 use `=IF(ISNUMBER(min_dscr),IF(min_dscr>=str_dscr,"MET","NOT MET"),"NOT MET")` (or "N/A" when debt_m+debt_c=0). In 30_BANKABILITY C29 treat non-numeric as 0 or "not applicable" explicitly. |
| F-05 | Medium | `kpi_avg_dscr` `'17_PROJECT_FINANCE'!C38`, `'32_DASHBOARD'!E11` | `=AVERAGE('20_CASH_FLOW'!E21:AR21)` gives `#DIV/0!` when there is no debt service. | `tariff_0`: recalculation status `errors_found`, 2 errors (C38, dashboard E11). | `=IF(COUNT(rng)=0,"n/a",AVERAGE(rng))`, the same pattern C37 already uses. |
| F-06 | Low | `'03_HYDROLOGY'!C42`, `'15_TARIFF'!E10:AR10`, `'17A_STRUCTURES'` rows 38/40/47/49/50, `'28_SENSITIVITY'`, `'30_BANKABILITY'!G5,H5,I5,B45:E45,C55`, `'32_DASHBOARD'` | With zero flow, the model does not degrade gracefully. | `flow_0`: 115 `#DIV/0!` (sized) and 113 (locked). Gate‑1 score, "lowest gate score" C55 and the dashboard top‑5 list all show errors. The overall verdict still prints because COUNTIF skips errors. | Guard the denominators: `IF(p50>0, p90/p50, 0)`, and `IF(energy>0, cost/energy*1000, "n/a")` on the LCOE row. Wrap the gate‑1 indicators in `IFERROR(...,0)` so that a degenerate resource scores CRITICAL rather than #DIV/0!. |
| F-07 | Low | `q_design` `'03_HYDROLOGY'!C5`, check `C43` | Design flow is not linked to installed MW or CAPEX. Raising Q from 57 to 70 m³/s changes nothing, because power is capped at `inst_mw`. Lowering it to 45 cuts P50 to 275.1 GWh (−5.9%) with CAPEX unchanged. Row C43 ("should be ≥ installed capacity") is not in 33_CHECKS: at Q=45 it is 47.8 MW against 60 MW, and `chk_all` still reads ALL OK. | Runs `qd_70` (identical to base) and `qd_45` (EIRR 13.76% → 11.81%). | Add a 33_CHECKS row: `=IF('03_HYDROLOGY'!C43>='02_PROJECT_INPUTS'!C15*0.98,"OK","WARNING")`. Either derive `inst_mw` from Q·H·η or label Q as a cap only. |
| F-08 | Low | `p90_10` `'03_HYDROLOGY'!C37` | The formula matches the specification exactly. It uses the large‑n AR(1) variance factor (1+ρ)/(1−ρ)/n. The exact finite‑n factor for n=10, ρ=0.3 gives 269.06 GWh, against 268.25 GWh in the model (−0.3%, so the model is slightly conservative). | `t5_identities.py` INFO line. | Document the approximation, or use `(1+2Σ(1−k/n)ρ^k)/n`. |
| F-09 | Low | `'30A_CLOSE_READINESS'!F22` label | The label says "in the base case", but the cell evaluates the live case, so `fc_met` moves with stresses (6 → 5 in p90cf, tar_m10_L and flow_x08_L). | `t4_results.json`. | Reword the label to "in the selected case", or point F22 at the base-case snapshot value. |
| F-10 | Low (design) | `'20_CASH_FLOW'`, `'24_CONTINGENT_LIABILITIES'` | With zero tariff and locked debt, the project runs a 468 USDm debt-service shortfall, funded entirely by sponsors (IPP `str_guar=0`). No default or termination is triggered, and consolidated fiscal NPV *improves* to +259 USDm (the utility gets free energy). The arithmetic is consistent, but readers should know that termination is never triggered by the model itself. | `tariff_0_L`. | Add a flag in 33_CHECKS or the dashboard when cumulative sponsor shortfall support > X% of equity ("project would default; termination exposure not modelled as called"). |
| F-11 | Low | Book `book7_resolved.md` l.1809 | The text says the developer IRR "could return a spurious root" and was replaced. The current formula returns −1 instead of a valid root in 6 scenarios (F‑02). No number printed in the book is affected: the book quotes only the base-case 16.0%. | F‑02 evidence; grep of the book. | Once F‑02 is fixed, re-run the snapshots and `prepare7.py`, and keep the sentence. |

## Test results (only tests actually run are listed)

### 1. Excel compatibility (static, `t1_compat.py`, `t1_circ.py`, `t1_implicit.py`)

**Functions used** (count of uses): IF 3279, MAX 1508, MIN 787, AND 524, SUM 461, CHOOSE 284, OR 122, PRODUCT 82, SIN 80, PI 80, INDEX 78, SUMPRODUCT 26, COUNTIFS 24, IFERROR 20, COUNTIF 18, ISNUMBER 17, MATCH 15, SMALL 15, NPV 10, IRR 9, ABS 8, SUMIF 4, COUNT 3, COLUMN 2, AVERAGE 2, LEFT 2, SQRT 1, ROWS 1, MEDIAN 1.

| Check | Result |
|---|---|
| LibreOffice-only, dynamic-array or Excel 2019/365-only functions (LET, LAMBDA, FILTER, XLOOKUP, IFS, SWITCH, TEXTJOIN, CONCAT, …) | None. PASS |
| Array (CSE) formulas | 0. PASS |
| Ranges in scalar context (implicit intersection or `@` risk) | 0. Every range sits inside SUM/MIN/MAX/SUMPRODUCT/INDEX/MATCH/IRR/NPV/COUNTIF(S)/… PASS |
| SUMPRODUCT with booleans | Every boolean use (9 formulas) multiplies, e.g. `(row=2)*range`. No bare boolean array arguments (which Excel would read as 0). PASS |
| IRR | Guesses given everywhere. kpi_eirr has a correctly nested IFERROR fallback chain; **dev_irr's chain is broken (F‑02)** |
| NPV | Excel convention (first flow discounted one period) used consistently. Model NPV and LCOE equal Python Σ CF/(1+r)^t for t=1..40. PASS |
| INDEX with 0 row/column | None. INDEX(…,1,opyr) in 18_DEBT row 35 is guarded by the loan-life flag. PASS |
| MATCH | All 15 uses exact (0). SMALL ties broken with a +0.01·k rank key. PASS |
| CHOOSE | 284 uses. The index comes from validated inputs, but the validation range is wrong (F‑03) |
| Text comparisons | Plain `=""`/`<>""`, `LEFT(x,2)="OK"`, case-insensitive in both engines. PASS |
| Volatile functions (OFFSET, INDIRECT, NOW, TODAY, RAND, CELL, INFO) | 0. PASS |
| Whole-column/row references | 0. PASS |
| External links | 0 (no `externalLink` parts, no `[n]` references). PASS |
| Defined names | 0. PASS |
| Circular references | 0 cyclic strongly connected components in the 11,166-node dependency graph (Tarjan). Shipped calcPr has `iterate="false"`. PASS |
| Data validation | 4 whole-number and 2 list (strings < 255 characters). Excel-valid, but **wrong range and non-blocking (F‑03)** |
| Conditional formats | 25 rules, all `cellIs equal "text"`. Excel accepts these. PASS |
| Sheet names | All ≤ 31 characters, no forbidden characters. Valid names, **but they start with digits, so they must be quoted in formulas (F‑01)** |
| Cell text > 32,767 chars | 0. PASS |
| Formula length > 8,192 | Longest is 652 characters (`01A_DEVELOPMENT!D51`). PASS |
| Nesting depth > 64 | Deepest parenthesis nesting is 6 (`17_PROJECT_FINANCE!C17`). PASS |

### 2. Independent recalculation (`t2_formulas.py`, `t2_compare.py`, `t2b_stress.py`)

- `formulas` 1.3.4 **cannot load the shipped file**. Its Excel-grammar parser rejects the unquoted digit-leading sheet references (F‑01).
- It loads and calculates the **fresh openpyxl build**, which has the same formulas and inputs, in 39 s. **All 11,166 formula cells match LibreOffice within 1e‑6 relative. 0 mismatches.**

| Output | LibreOffice | `formulas` |
|---|---|---|
| kpi_eirr | 0.137581200828486 | 0.1375812008284878 |
| kpi_pirr | 0.112182480312486 | 0.11218248031248668 |
| kpi_min_dscr | 1.52720627268227 | 1.5272062726822662 |
| debt_m | 145.352217909853 | 145.3522179098531 |
| uses | 214.960418914413 | 214.9604189144127 |
| fin_gap | 4.05435072721588 | 4.054350727215876 |
| dev_enpv | −0.952496487925857 | −0.9524964879258568 |
| dev_irr | 0.159572040576511 | 0.1595720405765082 |
| fis_npv_cons | −27.5809643867341 | −27.58096438673408 |
| cl_peak | 225.401649065097 | 225.40164906509665 |
| fc_met | 6 | 6 |
| p50 | 292.481378037504 | 292.481378037504 |
| p90_10 | 268.250752043978 | 268.2507520439778 |
| lcoe / kpi_npv / bk_overall / chk_all | 105.9489 / 16.3210 / "NOT BANKABLE…" / ALL OK | identical |

Stressed cases (`p90cf` and `combined`, debt locked) through `formulas`: all 14 key outputs match LibreOffice **except dev_irr**: 7.32% vs −1 (p90cf) and 7.02% vs −1 (combined). This is F‑02.

### 3. Error scan (recalc.py error count plus a cell-by-cell scan for `#VALUE!/#REF!/#DIV/0!/#NAME?/#N/A/#NUM!/#NULL!/Err:`)

- Base case (shipped file, recalculated): **0 errors / 11,166 formulas.** The fresh build gives 0 as well.
- 36 stressed or behavioural copies: **0 errors in 31**, including all-stresses-on (sized and locked), low/high case, P90 cash flows, structures 1/3/4/5, tenor 30, 6-year construction, and every developer-module variant.
- Errors appear only in the extreme or invalid input runs: `tariff_0` 2 (F‑05), `flow_0` 115 / `flow_0_L` 113 (F‑06), `case=4` 8,349 and `gen_case=4` 6,647 (F‑03).
- 12 snapshot re-runs: 0 errors, `chk_all` = ALL OK.

### 4. Behavioural tests (`t4_behaviour.py`, results in `t4_results.json`)

Base, debt sized: EIRR 13.76%, PIRR 11.22%, min DSCR 1.527, debt 145.35, uses 214.96, gap 4.05. "_L" = debt locked at base amounts and profile.

| Test | Expected | Actual | Verdict |
|---|---|---|---|
| Locked vs sized at base inputs | identical | All KPIs identical (EIRR 13.758%, DSCR 1.527, debt 145.35) | PASS |
| Tariff +10% (sized / locked) | EIRR↑, DSCR↑, fiscal cons. NPV↓ | 16.85% / 16.89%; DSCR 1.708 / 1.718; fis_npv_cons −27.6 → −52.7; debt unchanged (gearing cap 70% binds) | PASS |
| Tariff −10% (sized / locked) | EIRR↓; sized debt↓, gap↑; locked DSCR↓ | 10.47% / 10.68%; debt 145.4 → 130.0, gap 4.1 → 16.4; locked DSCR 1.335 | PASS |
| CAPEX +20% (sized / locked) | uses↑, EIRR↓, LCOE↑, gap↑ | uses 252.9 / 252.4; EIRR 9.38% / 9.35%; LCOE 105.9 → 122.7; gap 25.9 / 28.4 | PASS |
| Flows ×0.8 (monthly hydrograph) | P50 down by ~20%, EIRR↓, sized debt↓ | P50 292.5 → 232.6 (−20.5%, e-flow effect); EIRR 7.78%; debt 112.6; locked DSCR 1.141 | PASS |
| Generation flex −20% (cross-check) | ≈ flows ×0.8 | EIRR 7.90%, debt 113.4 (within 1% of the hydrograph run) | PASS |
| Design flow 57 → 45 | energy↓, EIRR↓ | P50 275.1, EIRR 11.81% | PASS (see F‑07) |
| Design flow 57 → 70 | no change (installed-MW cap) | identical to base | PASS (see F‑07) |
| Zero contingency | uses↓, EIRR↑ | uses 197.3, EIRR 16.07%, LCOE 99.1 | PASS |
| DSCR target 1.20 | debt ↑ or unchanged if gearing binds | unchanged (gearing 67.6% at cap) | PASS |
| DSCR target 1.50 | debt↓, min DSCR ≥ 1.5, EIRR↓ | debt 133.0, min DSCR 1.669, EIRR 13.32% | PASS |
| Tenor 12 / 20 years | 12: debt↓; 20: EIRR↑, DSCR↑ | 12: debt 126.3, gap 20.6; 20: EIRR 14.90%, min DSCR 1.696 | PASS |
| Tenor 30 (> 25-year concession) | check fails | "Commercial tenor within concession" = ERROR, `chk_all` = "1 issue(s)" | PASS |
| Hurdle 10% / 20% | EIRR unchanged; readiness and termination exposure change | EIRR unchanged; fc_met 7 at 10%; cl_peak 254.3 at 10% (termination value discounted at hurdle) | PASS |
| Development probabilities all 1.0 | dev_enpv = dev_npv_success | −0.99520 = −0.99520 | PASS |
| dev_rate = 0 | undiscounted ENPV | dev_enpv −1.033, success NPV +2.667; P(FC)=0.1457 | PASS |
| Tariff = 0 (sized / locked) | graceful | sized: debt 0, gap 121.7, EIRR −1, DSCR 99, 2 #DIV/0!; locked: shortfall 468, DSCR −0.56, 0 errors | PARTIAL (F‑04, F‑05, F‑10) |
| Flows = 0 | graceful | 115 / 113 #DIV/0! | FAIL (F‑06) |
| Invalid selector `case=4`, `gen_case=4` | blocked by validation | accepted; thousands of #VALUE! | FAIL (F‑03) |

**Integrity checks must fail when they should** (`t4b_checks.py`, by forcing an error into a copy):

| Forced fault | Check that should fire | Result |
|---|---|---|
| Concessional grace 10 + 20 > 25 | Concessional repayment within concession | ERROR, PASS |
| cons_years = 20 | Timeline fits horizon | ERROR, PASS |
| Max debt 30%, private equity 10% | Structure check | WARNING, PASS |
| 17_PF!C18 overwritten with 0 | Sources = uses | ERROR, PASS |
| 20_CF!L26 = −5 | DSRA never negative | ERROR, PASS |
| 06_CONSTRUCTION!E23 = 0.5 | CAPEX phasing = 100% | ERROR, PASS (balloon check also fires) |
| 18_DEBT!K36 principal = 0 | Debt fully repaid | still OK, because the final-year sweep repays; "no forced balloon" fires instead. Correct by design. |

Every non-negative-control run kept all 14 checks OK (except the tenor‑30 run, which was meant to fail).

### 5. Identity checks (`t5_identities.py`, 44 checks per file)

All 44 checks pass on the base case. The largest residual is 8e‑14.
- **Sources and uses:** sources = uses; uses components; annual uses, debt drawn and equity sum to the totals.
- **Waterfall:** each year, CFADS − DS + DSRA net + b/f + shortfall − claim repayment − distributions − c/f = 0. Lifetime distributions of 382.19 reconcile. DSRA: initial 7.314 − net releases leaves a final balance of 0.
- **Debt and DSCR:** DSCR row = CFADS/DS. Both debt roll-forwards hold (close = open + draw − principal; open(t) = close(t−1)). Σ principal = Σ drawn = debt_m (145.352). debt_m = PV of commercial DS at 8%.
- **Hydrology:** P90(1y), P75 and P90(10y) all match P50(1 − z·CV·√((1+0.3)/(1−0.3)/10)) to 1e‑15. P50 = Σ_m min(ρgQHη, 60 MW)·hours·availability = 292.4814 GWh. Days in the year = 365.25. CF = 55.65%.
- **Returns and valuation:** project IRR, equity IRR, project NPV, LCOE and LLCR match numpy-financial and Python recomputation. Developer IRR matches in the base case. Fiscal NPV discount factors and fiscal_npv_cons match. P(FC) = Π p_i. dev ENPV = P·PV(value) − PV(risk-weighted spend).
- **Stressed copies:** of 36 stressed copies, 25 pass all 44 checks. 6 fail only the developer IRR check (all_stress, all_stress_L, flow_x08, flow_x08_L, gen_m20, p90cf; F‑02). 5 degenerate runs (flow_0, flow_0_L, tariff_0, tariff_0_L, structure 1) could not be scored because IRR or DSCR is text or empty there.

**Snapshot reproducibility** (`t6_snap.py`): 11 published scenarios were re-run from the exact `run_snapshots.py` settings (base_locked, overrun96, combined, p90cf, epc2_ov, epc3_ov, offtaker_nobs, len1, s3, drought, dev_all). On all 15 KPIs compared, **every value equals `snapshot_results.json`**.

### 6. Book ↔ model consistency (`t7_book.py`, results in `t7_book.json`)

48 checks, covering more than 70 printed numbers, compared with model values rounded the way the book prints them. **48/48 match.** The checks cover:
- Table P.2: capacity factor 55.6%, P(close) 15%, developer IRR 16.0%, developer NPV −0.95, FC decision.
- §10.1 uses table: 165 / 18 / 4.7 / 187 / 17 / 2.9 / 7.3 / 215.
- §10.3 overrun table: 22; 68 / 5.7% / 1.49x; 24 / 10.1% / 1.55x.
- All 14 rows × 5 columns of Table 16.1, plus offtaker without backstop (−100% / −0.53x).
- EPC table §9.5: 12.6 / 13.8 / 14.9%; 7.4 / 5.6 / 3.8%; 43 / 65 / 96.
- §18 fact sheet: 292 GWh, 56%, 236 and 268 GWh, USD 157m and 2,614/kW, 145m and 68%, LCOE 106, 13.8% vs 15.0%, gap 4.1, 6 of 23.
- Fiscal: NPV 35, discount rate 8%, peak contingent 225.
- §18.3: 58%, 3.34 / 2.06 / 1.28.

The only text–model tension is F‑11.

## Appendix — reproduction

Directory: `/tmp/claude-0/-home-user-Boujieka/92f87389-f945-55f4-b28c-902b8d98c6ca/scratchpad/modeltest/`

| Script | Purpose |
|---|---|
| `lib.py` | Copies `base.xlsx` (= shipped model), sets named inputs via `model_map.json`, runs recalc.py, reads values, scans errors and 33_CHECKS |
| `t1_compat.py`, `t1_circ.py`, `t1_implicit.py` | Function inventory, structural checks, cycle detection (Tarjan on the fresh build), implicit-intersection scan |
| `t2_formulas.py <xlsx> <outdir>`, `t2_compare.py`, `t2b_stress.py {p90cf\|combined}` | Second-engine recalculation and cell-by-cell comparison |
| `t4_behaviour.py`, `t4b_checks.py` | Behavioural runs and negative controls for the checks |
| `t5_identities.py <recalculated.xlsx>` | 44 identity checks |
| `t6_snap.py` | Snapshot reproduction |
| `t7_book.py` | Book spot-checks |
| `irr_test.xlsx` | Isolated LibreOffice IRR guess test for F‑02 |
| `fresh/` | Scratch build of `build_model.py` (quoted references) |

Typical sequence:
```
pip install formulas
python3 t1_compat.py base.xlsx
python3 t2_formulas.py fresh.xlsx f_out_fresh
python3 t2_compare.py
python3 t4_behaviour.py
python3 t4b_checks.py
for f in runs/*.xlsx; do python3 t5_identities.py $f; done
python3 t6_snap.py
python3 t7_book.py
```

Key evidence for F‑01 (shipped XML, `xl/worksheets/sheet20.xml`, cell C31):
`<f aca="false">IFERROR(IRR(20_CASH_FLOW!$E$44:$AR$44,0.08),&quot;n/a&quot;)</f>`
The fresh build has `IFERROR(IRR('20_CASH_FLOW'!$E$41:$AR$41,0.1),…)`.

Limitations: there was no Microsoft Excel, so F‑01 and IRR convergence in Excel are inferred from the OOXML grammar, the XlsxWriter quoting rule and a strict third-party parser, not observed.
