## 7. Scenarios, stresses, sensitivities and the snapshot runner

### 7.1 Cases (mutually exclusive)

Set with `case` on *01_CONTROL_PANEL*; parameters on *27_SCENARIOS*.

| Parameter | Base | Low | High |
|---|---|---|---|
| Flow factor | 1.00 | 0.93 | 1.04 |
| CAPEX factor | 1.00 | 1.10 | 0.95 |
| Demand growth adjustment | 0.0 pp | −1.5 pp | +1.0 pp |
| OPEX factor | 1.00 | 1.10 | 0.95 |

Demand segments also switch growth rate by case.

### 7.2 Stress toggles (combinable)

| Toggle | Default parameter | Effect in the engine | Basis noted in the model |
|---|---|---|---|
| `st_drought` | Flow × 0.55 for 3 years from operating year 4 | `drought` factor on generation (not on lender-case generation) | Kariba 2024 allocation cut of about 47% [CL-04] |
| `st_capex` | +27% | `eff_capex`, scaled by the owner's share `epc_owner` | Ansar et al. 2014 median real overrun [HY-08]; mean +96% |
| `st_delay` | +2 years | Longer construction; delay cost 4% a year scaled by `epc_owner_d` | Ansar et al. 2014 mean 2.3 years [HY-08] |
| `st_demand` | Demand level × 0.80 from COD | `eff_dem` | Assumption |
| `st_offtaker` | Collection −8 pp, transfers −30%, retail tariff frozen 5 years from COD | `eff_coll_adj`, `eff_sub`, `eff_freeze` | Assumption |
| `st_fx` | One-off 50% step devaluation at COD | `eff_fxshock` | Recent large devaluations |
| `st_rate` | +300 bp on commercial debt | Applied to the unhedged share only | Concessional debt fixed-rate |
| `st_trans` | Line 2 years late | `eff_tdelay`; cost penalty | Assumption |
| `st_climate` | −3% mean flow per decade | `climate` factor | Illustrative; needs a basin study |

### 7.3 Sensitivity flexes

`fx_capex`, `fx_gen`, `fx_tariff`, `fx_opex` and `fx_rate` on *01_CONTROL_PANEL* apply on top of the case and stresses. The effective levers that the engine uses are listed at the foot of *27_SCENARIOS*.

### 7.4 Live tornado (28_SENSITIVITY)

A closed-form screening LCOE on the funding base plus IDC, at the project discount rate over the PPA term:

```
lc_crf  = disc_rate/(1-(1+disc_rate)^-ops_years)
lc_base = ((fund_base+u_idc)*lc_crf+opex_y2)/p50*1000
```

Each driver is flexed both ways: CAPEX ±20%, generation ±10%, discount rate ±2 pp, OPEX ±20%, delivered share (curtailment 0 to 15%). Kasiri screening LCOE is USD 97.8/MWh, with CAPEX the widest swing. The tornado ignores tax, financing and timing; financing results come from the full engine.

### 7.5 The snapshot runner

`tools/run_snapshots.py` reruns the complete workbook for each case, recalculating a temporary copy in LibreOffice headless each time, and writes the results as dated static tables. Live formulas are not changed.

**What it runs.**

| Group | Runs | Debt |
|---|---|---|
| Base | Debt sized in the model; debt locked | Sized; locked |
| Scenarios | Low, High, Drought, Overrun 27%, Overrun 96%, Delay, Low demand, Offtaker, Offtaker without backstop, FX step, High rate, Transmission delay, Climate, Combined (overrun, delay, offtaker, FX) | Locked |
| Structures | Structures 1 to 5 | Sized |
| Sensitivities | CAPEX ±20%, generation ±10%, tariff ±10%, OPEX +20%, rate +200 bp, P90 in the cash flows | Locked |
| Contracting | EPC 1, 2, 3 base and with a 96% overrun | Sized |
| Developer | Discount rate 18%, premium 6%, stage odds +10 pp, grant for half of feasibility, tariff +10%, all four levers | Sized |
| Lender case | One-year P90 | Sized |
| Solves | Tariff flex giving each structure's target equity IRR (structures 2 to 5, nine bisection steps); flow flex at which the locked minimum DSCR reaches 1.0 | As above |

For the locked runs, the runner first runs the base with debt sized, then writes the base `debt_m`, `debt_c`, `s_grant`, `s_goveq` and the commercial principal by operating year into the locked inputs of each copy.

**What it writes.** Static tables in *27_SCENARIOS* (scenarios), *17A_STRUCTURES* (structures) and *28_SENSITIVITY* (sensitivities), each with the run date, and `model/snapshot_results.json` with all key results, the gate statuses and selected time series for every run. Results are keyed by short names (for example `base_sized`, `drought`, `offtaker_nobs`, `s3`, `epc2_ov`, `dev_all`, `len1`); the required tariff flexes are stored as `req_tariff_flex` on `s2` to `s5` and the break-even flow as `be_flow_flex` on `base_locked`.

**Selected snapshot results (debt locked unless stated).**

| Run | Equity IRR | Min DSCR | Financing gap (USDm) | Consolidated fiscal NPV (USDm) |
|---|---|---|---|---|
| Base | 13.8% | 1.53 | 4.1 | −28 |
| Drought | 11.0% | 0.69 | 4.1 | −27 |
| Overrun 96% | 5.7% | 1.49 | 68.3 | −37 |
| Offtaker, backstop | 13.8% | 1.53 | 4.1 | −125 |
| Offtaker, no backstop | −100% | −0.53 | 4.1 | −152 |
| FX step | 13.8% | 1.53 | 4.1 | −111 |
| Combined | 7.8% | 1.54 | 43.1 | −157 |
| One-year P90 lender case (sized) | 13.2% | 1.76 | 18.7 | −27 |

The break-even flow flex is about −28%. The tariff flex that gives the IPP structure its 15% target is about +3.9% (about USD 116/MWh against 112).

**How to rerun.** From the repository root, with LibreOffice (Calc), Python 3 and openpyxl installed, and a LibreOffice recalculation script (`recalc.py`) that takes a file and a timeout and prints a JSON status:

```
python3 model/build_model.py                                  # optional: rebuild from the generator
RECALC=/path/to/recalc.py python3 tools/run_snapshots.py       # rerun all cases, write tables and JSON
python3 tools/model/check_cycles.py model/Bankable_Hydro_Model.xlsx
```

The runner stops if any recalculation reports a formula error. At the end it recalculates the workbook itself in LibreOffice and then runs `tools/model/excel_quote_fix.py` on it.

### 7.6 The LibreOffice recalculation and the Excel quote fix

LibreOffice, when it saves a recalculated workbook, writes references to sheets whose names begin with a digit without quotation marks (for example `17_PROJECT_FINANCE!$C$31` instead of `'17_PROJECT_FINANCE'!$C$31`). Excel's formula grammar requires the quotes. `tools/model/excel_quote_fix.py` rewrites every formula, defined name, data validation and conditional format in the package to restore them, leaving cached values unchanged:

```
python3 tools/model/excel_quote_fix.py model/Bankable_Hydro_Model.xlsx
```

Run it after every LibreOffice recalculation that saves the shipped file, including a manual one. The snapshot runner does so automatically when it completes. A workbook written directly by `build_model.py` (openpyxl) is already quoted and is set to recalculate fully on load.

---

## 8. The two levels of gates and the framework map

### 8.1 Two levels, two stages

| | 9-gate screen | 23-gate close readiness |
|---|---|---|
| Sheet | *30_BANKABILITY* | *30A_CLOSE_READINESS* |
| Stage | Development: should we keep spending? | Transaction: does the evidence file support financial close? |
| Basis | Metrics against three thresholds | Automatic tests plus evidence statuses |
| Scoring | Weakest test sets the gate; weakest gate sets the verdict | Critical flags and the decision ladder |
| Output | NOT BANKABLE to READY FOR FINANCIAL CLOSE, with ranked actions | STOP, NOT READY, CONDITIONAL GO or GO |
| Kasiri | NOT BANKABLE (Gate 6) | STOP (7 critical gates not met) |

The two levels can disagree, and that is informative. The screen can read well while the close test reads STOP, because the close test counts only evidence that exists. The dashboard shows both on row 4 and side by side in its lower blocks.

### 8.2 The framework map (34_FRAMEWORK_MAP)

For each of the 23 gates the map gives the gate, its framework question, the party that must accept it, whether it is critical, the model sheet or sheets that test it (derived from the names in the automatic test, or from the gate's area for evidence gates), the metric or evidence required, the type (automatic or evidence), the live status from *30A_CLOSE_READINESS*, and the book chapters for the question:

| Question | Book chapters |
|---|---|
| Q1 | 2, 3, 9, Annexes N to P |
| Q2 | 5, 7, 8, Annex R |
| Q3 | 3, 4 |
| Q4 | 6, 14 |
| Q5 | 12, 13 |
| Q6 | 9, 10, Annexes O and Q |
| Q7 | 15 |
| Q8 | 17, 18 |

The second table on the sheet maps each screen gate to its main question, with live status: Gates 1 and 3 to Q1; Gates 6 and 9 to Q2; Gates 2 and 4 to Q3; Gate 7 to Q5; Gates 5 and 8 to Q7.

Use the screen while developing to decide whether to keep spending, and the 23 gates at the transaction stage to decide whether the evidence supports close.

---

## 9. Integrity checks and the book check

### 9.1 33_CHECKS

| # | Check | Fails as |
|---|---|---|
| 1 | Sources = uses (within 0.01) | ERROR |
| 2 | Construction funding balances (uses = grants + debt + equity) | ERROR |
| 3 | CAPEX phasing sums to 100% | ERROR |
| 4 | Concessional debt fully repaid by the end of the horizon | ERROR |
| 5 | Commercial debt fully repaid by the end of the horizon | ERROR |
| 6 | Concessional grace plus term within the concession | ERROR |
| 7 | Commercial tenor within the concession | ERROR |
| 8 | Construction plus concession within 40 periods | ERROR |
| 9 | Delivered energy not above generation | ERROR |
| 10 | Unpaid amounts not negative | ERROR |
| 11 | No forced balloon in the final commercial repayment year (forced principal above target by less than USD 0.5m) | WARNING |
| 12 | DSRA balance never negative | ERROR |
| 13 | Project-funded transmission fully funded (construction plus CFADS) | ERROR |
| 14 | Structure check on *17A_STRUCTURES* | WARNING |

`chk_all` reads ALL OK or "n issue(s)". The independent test forced each check to fail on a copy and each fired. The checks confirm internal consistency, not the realism of the inputs. Do not use outputs unless ALL OK is shown.

### 9.2 35_BOOK_CHECK

The sheet compares the live model with the Kasiri figures printed in Book 7: 24 numeric figures with a tolerance each, and two text results.

| Figure | Printed | Tolerance |
|---|---|---|
| Installed capacity (MW) | 60 | 0.5 |
| P50 generation (GWh) | 292 | 0.5 |
| Capacity factor | 55.6% | 0.05 pp |
| P90 one-year / ten-year (GWh) | 236 / 268 | 0.5 |
| Plant cost real 2026 (USDm) / unit cost (USD/kW) | 157 / 2,614 | 0.5 |
| Total uses / senior debt (USDm) | 215 / 145 | 0.5 |
| Gearing on total uses | 68% | 0.5 pp |
| LCOE (USD/MWh) | 106 | 0.5 |
| Private equity IRR / developer IRR | 13.8% / 16.0% | 0.05 pp |
| Minimum DSCR / LLCR | 1.53 / 1.59 | 0.005 |
| Financing gap (USDm) | 4.1 | 0.05 |
| Risk-weighted developer NPV (USDm) | −0.95 | 0.005 |
| Probability of close | 15% | 0.5 pp |
| Value of the position at permitting (USDm) | 1.28 | 0.005 |
| Fiscal NPV central / consolidated (USDm) | 35 / −28 | 0.5 |
| Peak contingent exposure (USDm) | 225 | 0.5 |
| Buyer payment capacity, worst early year | 6.0x | 0.05 |
| Gates met (of 23) | 6 | 0 |
| Financial close decision | STOP: a critical gate is not met | exact |
| Fiscal screen | LOW additional fiscal pressure | exact |

Each line reads PASS or CHECK, and the sheet reads ALL PASS or "n TO CHECK". The check is valid only with default inputs (base case, IPP structure, debt sized in the model). After changing inputs, CHECK lines are expected.

---

## 10. Audit checklist for reviewers

1. *33_CHECKS* reads ALL OK in the case being reviewed, and *35_BOOK_CHECK* reads ALL PASS with default inputs.
2. The workbook opens in Excel without repair. If it was saved by LibreOffice, `excel_quote_fix.py` has been run on it.
3. `check_cycles.py` reports no cycle after any change to `build_model.py`.
4. Every blue input has a source or an explicit assumption note; fictional values (Navaria country data, benchmark unit cost, line cost, utility accounts, regulatory statuses, development stages) have been replaced.
5. The lender case matches the case agreed with the lenders' technical adviser, and a multi-year drought has been tested separately.
6. Stress results were read with the financing locked, and the locked inputs on *18_DEBT* (C6 to C9 and row 12) hold the base-case values, not the shipped placeholders.
7. Which constraint sizes the debt (gearing or cover) is stated, with the gearing cap and the sizing DSCR.
8. Utility inputs reconcile to audited accounts; the counterfactual is understood; the consolidated fiscal NPV is reported next to the central one.
9. Call probabilities on *24_CONTINGENT_LIABILITIES*, stage probabilities, the development premium and discount rates are documented as judgements.
10. Fiscal thresholds on *26_DEBT_SUSTAINABILITY* and gate thresholds on *30_BANKABILITY* have been reviewed against the client's policy and the lenders' term sheet.
11. Every evidence status on *30A_CLOSE_READINESS* entered as MET has a document, signatory and date in column G.
12. Snapshot tables were regenerated after the last input change; the date stamp is recorded.
13. The developer IRR is not −100% unless the cash flow truly has no rate; if it is, inspect the cash flow on *01A_DEVELOPMENT* section F.
14. The minimum and average DSCR are not the placeholder 99 (no debt service).

---

## 11. Known limitations

### 11.1 What the model does not do (Book 7, Annex K)

- It is annual: no monthly construction draws, no seasonal dispatch, no peak or off-peak pricing.
- Debt and equity are drawn pro rata with spending, not equity first, which slightly flatters the equity return.
- There is no developer promote or carried interest, and no shareholder loans.
- There is no refinancing; the step-up after commercial operation is valued directly.
- The currency step is permanent in real terms, with no pass-through to local prices.
- The utility model has no balance sheet.
- Stresses are deterministic: no Monte Carlo over hydrology and currency, no joint distribution of drought, currency and utility distress.
- Stage probabilities, the development premium and the developer's discount rate are user judgements; no public data were found to calibrate them for African hydro.
- The model has been recalculated in LibreOffice and reproduced by a second engine; a test in Microsoft Excel is outstanding.

### 11.2 Further simplifications

- P-values use a normal approximation from the CV. Energy is computed from long-term mean monthly flows, which overstates energy when flows exceed the design flow in some years.
- The ten-year P90 uses the large-sample persistence factor (1+ρ)/(1−ρ)/n; the exact finite-sample factor for n = 10 and ρ = 0.3 gives about 0.3% more energy, so the model is slightly conservative.
- Curtailment is proportional: delivered energy is generation times MIN(1, evacuation MW / installed MW).
- The lender case uses unlevered tax and depreciation without IDC and fees.
- Tax is computed on cash revenue, not on billed revenue.
- Utility operating cost is half fixed and half volume-related; the cost of other supply is half USD-linked.
- Guarantee calls are deterministic within a scenario; expected loss is only as good as the probabilities entered.
- The termination amount is simplified to debt plus the larger of unrecovered equity with a premium and the value of remaining distributions at the target IRR.
- The fiscal screen is a project-level screen and does not replace IMF and World Bank DSA or PFRAM. Other PPAs and guarantees of the same government are not aggregated.
- Q3 (economic for the system) is tested only through the grid and transmission gates; a comparison with the utility's least-cost plan sits outside the model (Book 7, Chapter 17).
- Development costs enter plant cost at their real budget (USD 9.0m), phased and escalated with construction spending, while the developer's cash flow receives the nominal success-path spend (USD 8.6m) at close; the two amounts are not reconciled.
- The utility payment headroom per MWh on *17A_STRUCTURES* (about USD 956/MWh for Kasiri) divides the utility's whole sustainable payment capacity by the project's energy; it is large for a small plant and is a capacity measure, not a price.

### 11.3 Open low points from the independent test

The independent test (`docs/MODEL7_TEST_REPORT.md`) found five faults that were corrected (Excel quoting, developer IRR fallbacks, selector validation, the DSCR placeholder on Gate 18, the average DSCR error). Points that remain open:

1. At zero river flow the model does not degrade gracefully: division errors appear (P90/P50, LCOE, Gate 1 and the dashboard ranking).
2. Design flow is not linked to installed capacity or cost: raising it changes nothing because power is capped at installed MW, and lowering it cuts energy without cutting cost. The "theoretical power at design flow" row on *03_HYDROLOGY* is not part of *33_CHECKS*.
3. With a zero tariff and locked debt, sponsors fund the debt-service shortfall indefinitely; the model never triggers default or termination itself.
4. With no debt service, the minimum and average DSCR show a placeholder of 99. Gate 18 is protected by its debt test, but the DSCR test of screen Gate 7 would score it as READY.
5. The developer IRR returns −1 if the first starting value converges to a rate of absolute value 1 or more, without trying the other two.

The fourth open point listed in Annex K, the label of Gate 18, is closed in the workbook: the label now reads "in the selected case".

### 11.4 Open items in this release candidate (4 October 2026)

1. *35_BOOK_CHECK* returns `#VALUE!` on the private equity IRR line when that IRR is "n/a" (structure 1, which has no private equity). Because the snapshot runner stops on any recalculation error, a full rerun stops at "Structure 1". The scenario tables on *27_SCENARIOS*, *17A_STRUCTURES* and *28_SENSITIVITY* are empty in the current workbook, and `model/snapshot_results.json` comes from the previous complete run, made before *34_FRAMEWORK_MAP* and *35_BOOK_CHECK* were added; its base results match the book check.
2. The shipped workbook was last saved by LibreOffice and its formulas are not quoted; run `excel_quote_fix.py` before opening it in Excel.
3. The snapshot table header written by the runner describes the locked commercial debt as an "annuity profile"; the locked schedule is in fact the base-case sculpted principal.

---

## 12. Rebuilding or extending the model

### 12.1 The generator

`model/build_model.py` is the single source of truth. Run it from the repository root; it writes `model/Bankable_Hydro_Model.xlsx` with formulas only (no cached values, full recalculation on load) and `model/model_map.json`.

Every cell is created through one of three helpers:

| Helper | Creates | Registers |
|---|---|---|
| `inp(ws, r, name, label, value, unit, note, fmt, key)` | A blue input in column C (yellow fill if `key`) | Scalar name |
| `calc(ws, r, name, label, template, unit, fmt, note, out)` | A formula in column C (green fill if `out`) | Scalar name |
| `ts(ws, r, name, label, unit, template, fmt, total, bold)` | A formula in each of columns E to AR, optional total in C (`sum`, `max`, `min` or a formula) | Time-series name |

Formulas are written once as templates and resolved after every sheet is built, so sheets can refer to each other regardless of build order:

| Template | Resolves to |
|---|---|
| `{name}` | Absolute reference to a scalar cell |
| `[name]` | Same-column cell of a time-series row |
| `[name@p]` / `[name@n]` | Previous / next column of a time-series row |
| `[RNG:name]` | Full absolute range E to AR of a time-series row |
| `[C:name]` | Column C (total or key) of a time-series row |
| `#T#` | Period index t of the current column |

Names are unique: the helpers assert on any collision. Formulas that link one cell on another sheet are coloured green automatically.

### 12.2 Adding or changing a line

1. Add an `inp()`, `calc()` or `ts()` call on the right sheet, using existing names in the template.
2. If the line feeds a gate, add it to the `GATES` list (screen) or `GATES_FC` and `GATE_Q` (close readiness); the framework map is generated from them.
3. If the line should be tracked by the runner, add its name to `KPIS`, `EXTRA` or `TS_SAVE` in `tools/run_snapshots.py`.
4. If a printed Kasiri figure changes, update the `BOOK_CHECKS` list that builds *35_BOOK_CHECK*, and the book.
5. Rebuild, then run `tools/model/check_cycles.py` on the new file to confirm there is no circular reference.
6. Recalculate (LibreOffice through the runner, or open and save in Excel), run `excel_quote_fix.py` if LibreOffice saved the file, and confirm *33_CHECKS* ALL OK and *35_BOOK_CHECK* ALL PASS.
7. Rerun the snapshots and record the date.

### 12.3 Design rules to keep

- No macros, no data tables, no circular references. Interest during construction and fees stay closed-form; the DSRA stays equity-funded; the lender case keeps unlevered tax.
- Inputs only in blue cells; no hard-coded numbers inside formulas except physical constants and labelled conventions.
- Every new output that a reader might quote needs a definition on the sheet and, if it is printed in Book 7, a line on *35_BOOK_CHECK*.
- Use only functions available in Excel 2010 and LibreOffice; avoid dynamic arrays, LET, LAMBDA, XLOOKUP and volatile functions.

---

*The Kasiri River Hydro case, the Republic of Navaria, Tamarind Hydro and the Navaria Electricity Company are fictional. Nothing in MODEL 7 or this manual is investment, legal, tax or accounting advice.*
