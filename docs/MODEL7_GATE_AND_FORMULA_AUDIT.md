# MODEL 7: financial close gates and critical formulas audit

Workbook tested: a fresh, uncalculated build from `model/build_model.py` (`rc1_fresh.xlsx`, 11,260 formulas). Each test copy was recalculated in LibreOffice with `recalc.py`, and every run recalculated with 0 errors unless stated otherwise. The shipped `model/Bankable_Hydro_Model.xlsx` was not opened or changed.

Scripts and raw results are in `/tmp/claude-0/-home-user-Boujieka/92f87389-f945-55f4-b28c-902b8d98c6ca/scratchpad/gatetest/`:

- `lib.py` is the earlier tester's helper, pointed at `rc1_fresh.xlsx`.
- `partA.py` runs the gate tests and writes `A_results.json`.
- `partB.py` runs the recomputations and writes `B_results.json`.
- `partB2.py` finds the true break-even premium and runs the developer IRR timing test.

## Verdict

**The gate logic and the core financial formulas are correct.** Two outputs need attention before the book is relied on: the close decision when an evidence status is missing, and the break-even premium.

- All 12 automatic gates change status exactly at their thresholds. `fc_met`, `fc_crit_fail`, `fc_crit_noev`, `fc_crit_part` and `fc_decision` matched an independent Python evaluation in all 54 runs.
- In those runs the following always matched the gate statuses: the 8-question framework block (30A rows 40–47), the dashboard block (32_DASHBOARD G17:H26 and H15), and the status column of 34_FRAMEWORK_MAP.
- The decision ladder gives all five outcomes as specified. I built a full-GO case: 23 of 23 gates MET, decision "GO".
- 35_BOOK_CHECK reads ALL PASS in the default case. It reads "n TO CHECK" whenever a printed figure or the decision changes.
- 25 critical outputs were recomputed independently from the workbook's own rows in 5 cases. All matched to within 1e‑13 (relative).
- **One High finding (G‑01).** If a critical evidence status is blank or unrecognised, the gate is silently dropped and the decision can read CONDITIONAL GO. **Three Medium findings:**
  - G‑02: the break-even premium is a static approximation (18.9% shown; the true value is 26.5% of CAPEX).
  - G‑03: the stage‑1 value in the D2 table does not equal `dev_enpv`, although both value the same position at the same date.
  - G‑04: three composite gates can pass without the signed document their label requires.

Counts: **High 1, Medium 3, Low 5, Info 2.**

## Findings

| ID | Severity | Item | Evidence | Recommended fix (in `build_model.py` terms) |
|---|---|---|---|---|
| G-01 | **High** | 30A evidence gates: `F = E` (GATES_FC loop, `put(ws, f"F{r}", f"=E{r}")`) | If E12 (gate 8, land rights, critical) is cleared, F12 = 0. The gate is then counted nowhere. Run L11: `fc_met`=22, `fc_crit_*`=0/0/0, decision **"CONDITIONAL GO: all critical gates met"**. The same happens with a value like `"MET "` (trailing space, run L12). Data validation (`dv_list`, now `errorStyle="stop"`) blocks typed typos in Excel. It does not stop a cleared cell, a paste or a programmatic write. | In the evidence branch use `put(ws, f"F{r}", f'=IF(OR(TRIM(E{r})="MET",TRIM(E{r})="PARTIAL",TRIM(E{r})="NOT MET"),TRIM(E{r}),"NO EVIDENCE")')`. Add a 33_CHECKS row: `=IF(COUNTIF(F5:F27,"MET")+COUNTIF(F5:F27,"PARTIAL")+COUNTIF(F5:F27,"NOT MET")+COUNTIF(F5:F27,"NO EVIDENCE")=fc_n,"OK","ERROR")`. |
| G-02 | Medium | `dev_be_prem` / `dev_be_prem_pct` ('01A_DEVELOPMENT'!C45:C46) | The formula `prem − enpv·(1+dr)^T/pfc` assumes the premium does not change the project. In fact the premium enters `uses` (`u_devprem`), which raises private equity and lowers the developer's equity NPV. Round trip: with `dev_prem_pct` set to the shown 18.90%, `dev_enpv` = **−0.30** (not 0), and the cell then shows 24.0%. Iterating (secant method, `partB2.py`) gives the true break-even of **26.46% of CAPEX** (enpv = 0.0000). The formula is exact only at that fixed point. The book prints this figure (Chapters 1, 14, 18). | Either relabel as "first-order break-even (project financing held fixed)" and print the iterated 26.5% in the book, or compute it with feedback: in the formula, scale the slope by the share of a premium dollar that reaches the developer net of its extra equity, `(1 − dev_stake·∂NPV_eq/∂prem)`. Simplest robust option: tabulate `dev_enpv` against the premium in 28_SENSITIVITY and interpolate the zero. |
| G-03 | Medium | D2 table, row 51 (`sv1`) vs `dev_enpv` | Both are "the risk-weighted value of the development position before stage 1 starts". Base case: sv1 = **−1.198**, dev_enpv = **−0.952**. The difference holds in every case (capex+20%: −1.579 vs −1.333; P90: −1.556 vs −1.310; all stresses: −2.011 vs −1.766). Cause: D2 column D uses **real** budgets (column D) with mid-stage timing. `dev_pv_cost_rw` uses **nominal** spend (rows 27–32, deflated by CPI for 2021–25) in annual end-year buckets. A month-exact nominal version of dev_enpv gives −1.098, so about 0.15 of the gap is timing and about 0.10 is real vs nominal. The book quotes both dev_enpv (−0.95) and sv4 (1.28). | Use one convention. In the D2 loop, discount the nominal stage rows (`SPEND0+k`) with the same factors as `dev_pv_cost_rw`, or define `dev_enpv` as `E{SV0}`. Add a 33_CHECKS identity `ABS(sv1 − dev_enpv) < 0.005`. |
| G-04 | Medium | Composite gates 11, 19 and 21 | Gate 11 "Grid connection agreement **signed** and transmission financed" tests only `tx_fin=1`. Gate 19 "Equity **commitments signed** and equity IRR ≥ target" tests only the IRR. Gate 21 "Government support **approved by the finance ministry**; fiscal screen not HIGH" tests only the screen (MODERATE passes: runs g21_dsa2_thc0 and g21_dsa3_flags0). GO was reached (L1) with no evidence entry for any of these documents. | Make these gates "model test AND evidence": keep column E as an input and set `F = IF(NOT(test),"NOT MET",<normalised E>)`. Or split each into an evidence gate and a model-test gate (25 gates). |
| G-05 | Low | Framework summary 30A F40:F47; dashboard H18:H25 ("critical open") | The count includes only critical NOT MET and NO EVIDENCE gates. Critical PARTIAL gates are left out. Default case: Q6 reads "0 of 3 met; **0 critical open**" although gate 13 (EPC, critical) is PARTIAL. Q8 reads "7 critical open" while 13 critical gates are not MET. | Add `+COUNTIFS(...,"PARTIAL")` to the F-column formula, or relabel the column "Critical NOT MET or NO EVIDENCE" and add a "critical partial" column. |
| G-06 | Low (convention) | Developer success-path cash flow (01A row 71): `dev_irr`, `dev_mult` | The reimbursement plus premium (13.3 USDm) sits in the first model column (2027), one period after the last development spend (2026). `dev_success_value`/`dev_enpv` value it **at close**, which is the end of the 2026 column. If it is placed at close, the IRR is **17.9%** instead of 16.0%. | Put `dev_reimb+dev_prem` in the last development column (`DCOLS[-1]`), or state the convention in the note. |
| G-07 | Low | 35_BOOK_CHECK overall cell E32 | `COUNTIF(E5:E30,"CHECK")` ignores error results. In run flow0, the LCOE line returns #DIV/0! and is not counted ("19 TO CHECK" where 20 differ). A run whose only discrepancy is an error would read ALL PASS. | `=IF(COUNTIF(E5:E{BC1},"PASS")=ROWS(E5:E{BC1}),"ALL PASS",ROWS(E5:E{BC1})-COUNTIF(E5:E{BC1},"PASS")&" TO CHECK")`. |
| G-08 | Low | Placeholder 99 in `ut_ratio10` (and `kpi_min_dscr`, `kpi_avg_dscr`) | With zero tariff (`en_chg=cap_chg=0`) there is no PPA bill, so `ut_ratio10` = 99 and gate 16 reads MET. Gate 18 is correctly guarded by `debt_m+debt_c>0`. | Return "n/a" and have gate 16 test `ISNUMBER()`, or document 99 as "not applicable". |
| G-09 | Low | Gate 17 threshold | The label says "no financing gap", but the test is `fin_gap<=0.5` (a hard-coded USDm tolerance). At exactly 0.5 the computed gap is 0.500000000000028, so the gate reads NOT MET (floating point). | Make the tolerance a named input (e.g. `fc_gap_tol`) and show it in the label. |
| G-10 | Info | Conventions a lender will ask about | See the "Conventions" section below. | Document them in 00_README and the book's model annex. |
| G-11 | Info | Case of status text | `"met"` in lower case is counted as MET, because COUNTIF ignores case (run L13). This is harmless. | None. |

## Part A: boundary tests (all were run)

Thresholds are those in `GATES_FC`. The default structure is IPP (`structure`=2), so `str_dscr`=1.35, `str_hurdle`=0.15 and `str_privmax`=0.35 are in 17A column F. "Issues" is the count of mismatches against an independent Python evaluation of every gate, the counts, the decision, framework rows 40–47, dashboard H15/H18:H26 and 34_FRAMEWORK_MAP I5:I27.

| Run | Input change | Gate | Status | fc_met | crit fail/noev/part | Decision | 35_BOOK_CHECK | Issues |
|---|---|---|---|---|---|---|---|---|
| base | none | — | — | 6 | 7/0/6 | STOP: a critical gate is not met | **ALL PASS** | 0 |
| g1 | rec_years 14, hyd_study 3 | 1 | NOT MET | 6 | 7/0/6 | STOP not met | ALL PASS | 0 |
| g1 | rec_years 15, hyd_study 3 | 1 | **MET** | 7 | 6/0/6 | STOP not met | 1 TO CHECK | 0 |
| g1 | rec_years 16, hyd_study 3 | 1 | MET | 7 | 6/0/6 | STOP not met | 1 TO CHECK | 0 |
| g1 | rec_years 16, hyd_study 2 | 1 | NOT MET | 6 | 7/0/6 | STOP not met | ALL PASS | 0 |
| g3 | fs_level 2 / 3 | 3 | NOT MET / **MET** | 6 / 7 | 7 / 6 crit fail | STOP not met | ALL PASS / 1 TO CHECK | 0 |
| g5 | es_level 2 / 3 | 5 | NOT MET / **MET** | 6 / 7 | 7 / 6 | STOP not met | ALL PASS / 1 TO CHECK | 0 |
| g6 | rap_level 1 / 2 / 3 | 6 | NOT MET / **MET** / MET | 5 / 6 / 6 | 8 / 7 / 7 | STOP not met | 1 TO CHECK / ALL PASS / ALL PASS | 0 |
| g11 | tx_fin 0 / 1 | 11 | NOT MET / **MET** | 5 / 6 | 8 / 7 | STOP not met | 1 TO CHECK / ALL PASS | 0 |
| g12 | tx_lag −1 / 0 / +1 (tx_gap_yrs −1 / 0 / 1) | 12 (non-crit.) | MET / **MET** / NOT MET | 6 / 6 / 4 | 7 / 7 / 8 | STOP not met | 6 / 0 / 12 TO CHECK | 0 |
| g15 | lc_months 5 / 6 / 7 | 15 | NOT MET / **MET** / MET | 6 / 7 / 7 | 7 / 6 / 6 | STOP not met | ALL PASS / 1 / 1 TO CHECK | 0 |
| g16 | ut_cov set so ut_ratio10 = 1.19 / 1.20 / 1.21 | 16 | NOT MET / **MET** / MET | 5 / 6 / 6 | 8 / 7 / 7 | STOP not met | 2 / 1 / 1 TO CHECK | 0 |
| g17 | str_privmax set so fin_gap = 0.49 / 0.50(0.500000000000028) / 0.51 | 17 | **MET** / NOT MET / NOT MET | 7 / 6 / 6 | 6 / 7 / 7 | STOP not met | 2 / 1 / 1 TO CHECK | 0 |
| g18 | locked debt; str_dscr = min DSCR −1e‑6 / = / +1e‑6 | 18 | MET / **MET** / NOT MET | 6 / 6 / 5 | 7 / 7 / 8 | STOP not met | ALL PASS / ALL PASS / 1 TO CHECK | 0 |
| g18 | sized debt, str_dscr 1.53 | 18 | MET (min DSCR re-sizes to ≥ target) | 6 | 7/0/6 | STOP not met | 13 TO CHECK | 0 |
| g19 | str_hurdle = EIRR −1e‑6 / = / +1e‑6 | 19 | MET / **MET** / NOT MET | 7 / 7 / 6 | 6 / 6 / 7 | STOP not met | 1 / 1 TO CHECK / ALL PASS | 0 |
| g21 | th_cash=th_cl=0 (1 flag), dsa 2 → MODERATE | 21 | MET | 6 | 7/0/6 | STOP not met | 1 TO CHECK | 0 |
| g21 | same, dsa 3 → **HIGH** | 21 | **NOT MET** | 5 | 8/0/6 | STOP not met | 2 TO CHECK | 0 |
| g21 | dsa 3, 0 flags → MODERATE | 21 | MET | 6 | 7/0/6 | STOP not met | 1 TO CHECK | 0 |
| Degenerate | en_chg=cap_chg=0 (no debt) | 16, 18, 19 | MET (ratio 99), NOT MET, NOT MET | 5 | — | STOP not met | 15 TO CHECK | 0 |

At tx_lag +1, two gates fail: gate 12, and gate 18 because min DSCR is 0.9999 in the year without evacuation.

**Decision ladder.** These runs use the full-pass automatic inputs listed below, with evidence statuses varied:

| Run | Evidence statuses | fc_met | fail/noev/part | Decision |
|---|---|---|---|---|
| L0 | automatic pass, default evidence | 12 | 1/0/6 | STOP: a critical gate is not met (gate 8 NOT MET) |
| **L1 (full GO)** | all 11 evidence = MET | **23** | 0/0/0 | **GO: evidence complete for a close decision** |
| L2 | gate 20 (non-critical) NOT MET | 22 | 0/0/0 | CONDITIONAL GO |
| L3 | gate 23 (non-critical) NO EVIDENCE | 22 | 0/0/0 | CONDITIONAL GO |
| L4 | gate 14 (non-critical) PARTIAL | 22 | 0/0/0 | CONDITIONAL GO |
| L5 | gate 2 (critical) PARTIAL | 22 | 0/0/1 | NOT READY: critical gates partly met |
| L6 | gate 2 PARTIAL + gate 4 NO EVIDENCE | 21 | 0/1/1 | STOP: critical evidence missing |
| L7 | L6 + gate 8 NOT MET | 20 | 1/1/1 | STOP: a critical gate is not met |
| L8 | gate 9 NO EVIDENCE only | 22 | 0/1/0 | STOP: critical evidence missing |
| L9 / L10 | all evidence MET, but lc_months 5 / rec_years 14 | 22 | 1/0/0 | STOP: a critical gate is not met |
| L11 | gate 8 status **blank** | 22 | 0/0/0 | **CONDITIONAL GO** (G‑01) |
| L12 | gate 8 status `"MET "` | 22 | 0/0/0 | **CONDITIONAL GO** (G‑01) |
| L13 | gate 8 status `"met"` | 23 | 0/0/0 | GO (G‑11) |
| L14 | full-GO inputs + gen_case 3 (P90) | 21 | 2/0/0 | STOP (min DSCR 1.165 < 1.35; EIRR 8.05% < 13%) |

**Full-GO case (L1).** These are the input changes from default:

- rec_years 15, hyd_study 3, fs_level 3, es_level 3, lc_months 6.
- `str_hurdle` for IPP ('17A_STRUCTURES'!F23) lowered from 0.15 to 0.13. The base EIRR of 13.76% is below the default 15% target, so gate 19 cannot pass without a lower hurdle or higher returns.
- `str_privmax` ('17A_STRUCTURES'!F10) raised from 0.35 to 0.3816, which takes fin_gap from 4.05 to 0.
- All 11 evidence statuses set to MET.

rap_level 2, tx_fin 1 and tx_lag 0 stay at their defaults. Results:

- `fc_met` 23 of 23, decision "GO".
- Every framework row reads "n of n met; 0 critical open". The dashboard H26 and H15 cells and 34_FRAMEWORK_MAP agree.
- 35_BOOK_CHECK reads "4 TO CHECK", as expected for non-default inputs.

## Part B: independent recomputation

Method: I read each run's recalculated rows (TSROW) and recomputed every output in Python, without using the workbook's own result cells. The independent parts are:

- an Excel NPV convention, with the first value discounted one period;
- an IRR root scan over [−95%, 200%] with Brent refinement, which lists every root;
- my own development spend schedule built from the stage durations, budgets and CPI;
- my own developer cash flow.

The cases were: base; capex +20% (`fx_capex`=0.2); P90 generation (`gen_case`=3); all nine stresses on; and base with `dev_prem_pct` set to the shown break-even. The table shows the base case. In the four other cases every item also matched to within 1e‑13 relative (`B_results.json`).

| Output | Formula used | Workbook | Recomputed | Difference |
|---|---|---|---|---|
| kpi_pirr | IRR of `ucf` (20_CASH_FLOW r44), annual, t=0 at the first model column | 11.2182% | 11.2182% | 5e‑16. 1 sign change, 1 root |
| kpi_eirr | IRR of `eq_priv_cf` (r41) | 13.7581% | 13.7581% | −2e‑16. 1 sign change in base, 3 under all stresses; 1 root in every case |
| kpi_npv | Σ ucf_t/(1.10)^t, t=1..40 | 16.3210 | 16.3210 | 1e‑14 |
| DSCR row | cfads/ds where ds>0.001 (16 years) | — | — | max row difference 8e‑15 |
| kpi_min_dscr / kpi_avg_dscr | min / mean of the DSCR row | 1.52721 / 1.60321 | 1.52721 / 1.60321 | <5e‑16 |
| kpi_llcr | Σ cfads·inloan_all/(1+rw)^opyr ÷ (debt_c+debt_m) | 1.59054 | 1.59054 | 2e‑16. Denominator equals the debt balance at COD (145.35) |
| lcoe (plant) | NPV(10%, lc_cost)/NPV(10%, delivered+deemed)×1000 | 105.949 | 105.949 | 7e‑14 |
| lcoe_sys | NPV(10%, lc_cost_sys)/NPV(10%, delivered×(1−tx_loss))×1000 | 108.111 | 108.111 | −5e‑14 |
| fis_npv | Σ f_net_t/(1.08)^t | 34.788 | 34.788 | 0 |
| fis_npv_cons | Σ f_net_cons_t/(1.08)^t | −27.581 | −27.581 | 4e‑15 |
| dev_pfc | Π p_k | 0.145656 | 0.145656 | 0 |
| Development spend row (01A r33) | own schedule: even monthly spread, ×(1+CPI)^(year−2026) | — | — | max 4e‑15 |
| dev_success_value | reimb + prem + stake·NPV(15%, eq_priv_cf) | 11.2723 | 11.2723 | 2e‑15 |
| dev_pv_success | success value/(1.25)^(72/12) | 2.95496 | 2.95496 | −8e‑16 |
| dev_pv_cost_rw | Σ_y Σ_k spend_k,y·P(reach k)/(1.25)^(y−y0+1) | 1.38290 | 1.38290 | 4e‑16 |
| **dev_enpv** | pfc·PV(success) − PV(risk-weighted spend) | −0.95250 | −0.95250 | −1e‑16 |
| dev_npv_success | PV(success) − PV(unweighted spend) | −0.99523 | −0.99523 | −4e‑16 |
| dev_be_prem | prem − enpv·(1.25)^6/pfc (formula reproduced) | 29.651 (18.9%) | 29.651 | 5e‑15. **Iterated true break-even is 26.46% (G‑02)** |
| Developer cash flow (01A r71) | own build: −spend; reimb+prem in t=1; stake·eq_cf·(1−sell) in operations; sale at last construction year | — | — | max 2e‑14 |
| dev_irr | IRR of the developer flow | 15.957% | 15.957% | −2e‑16. 3 sign changes (5 under all stresses); a **single** root in every case. F‑02 from the earlier report no longer occurs |
| dev_mult | Σ inflows / Σ outflows | 4.9715 | 4.9715 | −5e‑16 |
| v_cod_nom | Σ opflag·eq_cf/(1.11)^(t−cons_eff) | 97.484 | 97.484 | 1e‑14 |
| sell_proceeds | 0.5 × 0.4 × v_cod_nom | 19.4968 | 19.4968 | −4e‑15 |
| val_step_cod | v_cod/(1.15)^cons − Σ opflag·eq/(1.15)^t | 18.288 | 18.288 | 0 |
| D2 B, D, E (6 stages) | B = Π p_k..p_6; C = B·SV/(1.25)^((T−start_k)/12); D = Σ_j budget_j·P(j given k)/(1.25)^((start_j−start_k+dur_j/2)/12) | sv1…sv6 = −1.198, −2.057, −3.167, 1.277, 2.931, 5.697 | identical | <3e‑14 (but sv1 ≠ dev_enpv: G‑03) |

Other cases, workbook values (all matched to within 1e‑13):

| Case | Project IRR | Equity IRR | Min DSCR | LLCR | LCOE | Fiscal NPV | Developer IRR | dev_enpv |
|---|---|---|---|---|---|---|---|---|
| capex +20% | 9.08% | 9.37% | 1.503 | 1.568 | 122.74 | 31.11 | 9.32% | −1.333 |
| P90 | 8.32% | 8.05% | 1.165 | 1.262 | 130.11 | 20.97 | 7.32% | −1.310 |
| All stresses | 6.61% | 5.32% | 0.661 | 1.398 | 156.99 | −222.01 | 3.67% | −1.766 |
| Premium 18.9% | 9.67% | 10.42% | 1.502 | 1.566 | 117.49 | 32.60 | 32.46% | −0.304 |

## Conventions a lender will question (G‑10)

1. **Discounting is end-year.** Each NPV (project, LCOE, fiscal, equity at close) values the flows as at the start of the financial close year (2027), with each annual flow at year-end. A mid-year convention would raise the project NPV from 16.32 to 17.12 USDm. Because construction CAPEX is also treated as end-year, the NPV is slightly flattered. State the convention in 00_README.
2. **Everything is nominal USD.** The model's LCOE is a nominal-levelised 105.9 USD/MWh. The equivalent real 2026 LCOE (costs deflated by US CPI, discounted at the real rate) is **83.6 USD/MWh**. Lenders compare LCOE with the first-year real tariff, so show both.
3. **LCOE denominator.** It includes deemed (paid but not generated) energy, which is zero in the base case. Taxes and financing costs are excluded. This is acceptable for a plant LCOE but should be labelled.
4. **Development spend is treated as history.** Development runs from 2021 to 2026, so spend before 2026 is *deflated* (a 2026-real budget spent in 2021 becomes 0.906×). The developer NPV is therefore a value at the start of 2021, not at today's date.
5. **IRRs with several sign changes.** The developer flow has 3–5 sign changes, and the equity flow has 3 under all stresses. In every case tested, the root scan found one root in [−95%, 200%], and the workbook's guess chain returned it. The −1 fallback is still a number (not "n/a") and would flow into gate 19 and the book check as a real value.
6. **Mixed timing in developer outputs.** See G‑06 (reimbursement one period after close in the IRR) and G‑03 (D2 uses real budgets with mid-stage timing; dev_enpv uses nominal spend with end-year timing).

## Not tested

Microsoft Excel was not available, so every result above comes from LibreOffice and Python. The second engine (`formulas`) was not re-run on this build.
