# Independent review: ACCESS FINANCE mini grid engine 0.1.0

Scope: `apps/access360/backend/app/engine/` (inputs, model, checks, finance, sensitivity, optimizer, demo), the spec at `docs/financial-engine-spec.md` and `docs/known-limitations.md`. The existing suite (`pytest tests/engine`, 40 tests) passes. I edited no repository file. Every probe is in this folder (`pNN_*.py`) with its captured output (`pNN_*.out`). To run one: `cd <this folder> && /home/user/Boujieka/apps/access360/backend/.venv/bin/python pNN_x.py`.

Summary: **2 critical, 7 major, 12 minor.** The balance sheet, cash, debt and fixed asset roll forwards are internally consistent, and the timing spot checks in p13 (grace, tenor, RBF lag, ramp, replacements, level annuity, milestones) are correct. The defects sit in places that no reconciliation reaches: metric definitions, the solver, input validation and the optimizer. The integrity checks miss 12 of 13 planted formula errors (F06).

Legend: **P** = proven defect (reproduced by a probe). **D** = design choice consistent with the spec but economically misleading, and not listed in known-limitations. **S** = already covered by a spec simplification or a known limitation (mentioned only where it matters).

---

## Critical

### F01 (P): pre-subsidy project cash flow pays tax on the tariff support
* **Where:** `model.py:331` (`unlev_taxable = ebitda - unlev_dep`, where `ebitda` includes `tariff_support`, line 160) and `model.py:405` (`pre_sub` deducts `unlev_tax`).
* **What is wrong:** the "before subsidy" cash flows exclude the tariff support but still pay the tax on it. The project IRR before subsidy, the NPV before subsidy and the viability gap all fall as the subsidy grows, which inverts the purpose of the metric.
* **Repro:** `p02_presubsidy_tax.py`. Demo with 150 LCY/kWh support for 10 years:
  * NPV before subsidy goes from -22.96 M to -55.82 M;
  * the viability gap goes from 22.96 M to 55.82 M (×2.4);
  * IRR before subsidy goes from 13.8% to 12.2%;
  * the sum of the changes in the pre-subsidy cash flows is -71.9 M (it should be 0).
* **Fix:** compute a separate unlevered tax for the pre-subsidy case on `ebitda - tariff_support - unlev_dep`. Use the current one, plus grant income when `grant_income_taxable` is set, for the post-subsidy case.

### F02 (P): the minimum grant solver reports "infeasible" when it is feasible, even when no grant is needed
* **Where:** `sensitivity.py:369-372`. The solver tests `ok(hi)` first and returns infeasible before it tests `ok(0)`. `equity_irr` is `None` when equity input is about zero or the IRR is above 1000% a quarter (`finance.py` bracket).
* **What is wrong:** when the grant is paid in construction and debt is sized net of grant, the maximum grant (= capex) leaves no equity cash flow. The equity IRR is then `None`, so the test fails. The solver then says "Thresholds not met even at the maximum grant":
  * when 0 grant already meets the target (equity IRR 84% against a 15% target);
  * when the true answer is about 390k (equity IRR 16.0% at 400k).
* **Repro:** `p05_solver_false_infeasible.py`.
* **Fix:** test `ok(0)` first. Treat "equity IRR not computable because equity input is about 0 and distributions are positive" as passing, or cap `max_grant` at the grant that keeps equity input above 0. Better still, scan a coarse grid for the feasible region before bisecting, and report a non-monotone result when one is found.

## Major

### F03 (P): capex items with a life shorter than the horizon are never replaced
* **Where:** `model.py:131-141`. Only `technical.battery_*` generates replacements.
* **What is wrong:** in the demo, the diesel genset (10 years) and the smart meters (10 years) run for 20 years at no cost. PV inverters (typically 10 to 12 years) cannot be represented at all. A second storage item, or a battery `CapexItem` whose life differs from `battery_life_years`, is depreciated over a different life from the one used for replacement. In p03, with battery life set to 12 years, the battery bank item still depreciates over 8 years. LCOE, the IRRs and the minimum revenue requirement are flattered.
* **Repro:** `p03_short_life_assets.py`. The missing year-11 replacement of the genset and meters is 71.9 M LCY nominal, or 16.0 M PV at 15%.
* **Not in the limitations register.**
* **Fix:** give every `CapexItem` a replacement rule (`replace_at_end_of_life: bool`, a replacement cost share, and real price drift). Drive the battery replacement from its CapexItem, so that depreciation and replacement use one life.

### F04 (P): construction-period tax is missing from sources and uses, so the SU check fails on a valid input
* **Where:** `model.py:364` puts `tax[i]` in construction uses. `model.py:411-422` (`uses_total`) omits it.
* **What is wrong:** with LCY appreciation (negative depreciation, allowed down to -0.5), a USD tranche produces an FX gain during construction. That gain is taxed in cash and funded by equity, but it is not shown as a use. Any such project gets FAILED_CHECKS.
* **Economic point:** the gain is an unrealised translation gain on debt revaluation, taxed in cash before COD. Most regimes would defer it, or offset it against the loss pool.
* **Repro:** `p01_construction_tax_su.py` (SU residual 1.59 M, status `failed_checks`). `p08` also shows it on the demo with -10% a year.
* **Fix:** add `tax_during_construction` to S&U `uses_total`. Consider taxing unrealised FX only when it is realised (on repayment), or at least flag it.

### F05 (P): grant milestones outside the horizon, or at a negative quarter, are dropped silently, while debt stays sized net of the full grant
* **Where:** `inputs.py:129` (`quarter` has no `ge=0`, and there is no check against the horizon), `model.py:255` (out-of-range milestones skipped) and `model.py:166`.
* **Repro:** `p08_edge_cases.py`.
  * Milestone at quarter 500: 50 M of the 100 M grant is never received, the senior commitment stays 74.7 M, and the status is WARNING with no message.
  * Milestone at quarter -3: none of the grant is received.
  * The "subsidy 4 quarters later" sensitivity can push a late milestone past the horizon in the same way.
* **Fix:** validate `0 <= quarter < T` against the horizon. Report undisbursed grant (including grant skipped after closure) as a warning, and add a check that `grant_receipts.sum() == capital_grant` unless closure explains the difference.

### F06 (P): the integrity checks cannot see formula errors that stay double-entry consistent
* **Where:** `checks.py:39-91`.
* **What is wrong:** every check is a roll forward of series computed from the same flows. The DSRA check (`dsra == dsra_target`) and the MRA check are tautological, because `dsra` is built from `dsra_target` and MRA releases are built from the replacements. Nothing checks the project or equity cash flow series, the tax base, the metrics, or any value against an independent recomputation.
* **Repro:** `p10_mutation_checks.py` plants 13 plausible errors in a copy of `model.py`. 12 pass every check:
  * interest on the closing balance ×1.5;
  * tax charged twice;
  * tariff support double counted;
  * unlevered tax or replacements dropped from the project cash flows;
  * grant released in one quarter;
  * collection forced to 100%;
  * fuel ×10;
  * depreciation lives halved;
  * annuity sized on 110% of the balance (the final balloon clears the remainder);
  * DSRA sized on 1 quarter;
  * lock-up never applied.

  Only "CFADS excludes tax" is caught.
* **Fix:** add independent recomputation checks:
  * interest = opening balance × rate per tranche;
  * tax = rate × max(0, taxable − loss pool), recomputed;
  * DSRA target recomputed from the debt schedule and compared;
  * project cash flow = collections + fees − opex − tax − replacements (+ subsidies), recomputed from primitives;
  * EBITDA = cash from operations;
  * Σ depreciation over life = additions;
  * lock-up: no distribution where the quarterly DSCR is below the lock-up level;
  * annuity level within tolerance before the final instalment.

  Keep a golden-file regression of the demo, cross-checked once by hand or in Excel.

### F07 (P): closure year DSCR is 0, which makes dscr_min and the solver meaningless for every grid arrival case
* **Where:** `model.py:223` (`sched_ds` includes interest and scheduled principal in the closure quarter, when CFADS = 0) and `model.py:446-450`.
* **Repro:** `p12_grid_closure_dscr.py`.
  * Asset transfer in year 8: annual DSCR is [1.93, 2.02, **0.0**, nan], and `dscr_min` = 0. The grid sensitivity row always shows a DSCR of 0.
  * `minimum_capital_grant(min_dscr=1.2)` returns a grant equal to 100% of capex (286.9 M), because only zero debt passes. Without grid arrival it returns 251.5 M.
* **Fix:** in the closure quarter, treat all debt service as prepayment (or exclude the closure quarter from the DSCR). Report the closure-year cash cover separately.

### F08 (P): the optimizer recommends a household-only SHS option that leaves 71% of demand unserved
* **Where:** `optimizer.py:168-179` (E serves households only, capped at `shs_kwh_month_capacity`), `:193-195` (LCOE per kWh *served*) and `:236-254`. There is no gate and no penalty on unserved share; the only penalty is a 10% productive-use weight.
* **Repro:** `p11_optimizer.py`. With SHS at 40k/household, option E is both "least cost" and "recommended" (LCOE 174 against 276 for C). It serves 43,200 of 149,520 kWh. The businesses, the productive users, the institutions and the anchor are left unserved. Its subsidy per connection divides by households only.
* **Fix:** compare options on the same served basket. Either:
  * add a cost of unserved energy (a value of lost load per kWh), or complement every partial option with a costed solution for the remaining users; or
  * gate options whose unserved share exceeds a threshold.

  Rank on PV cost per kWh *demanded*, or add unserved share as an explicit objective.

### F09 (P): the optimizer's affordability tariff is mis-specified, so cost recovery and the subsidy requirement are nonsense
* **Where:** `optimizer.py:196-199`.
* **What is wrong:** `afford_tariff = 10% × household income / household kWh` is applied to **all** served kWh, including the anchor, the businesses and the productive users. The formula is inversely proportional to consumption.
* **Repro:** `p11_optimizer.py`.
  * Demo: the affordability tariff is 667 LCY/kWh against a grid cost of supply of 150, so the subsidy requirement is 0 for every option.
  * At 1 kWh/month household use, it becomes 6,000 LCY/kWh: option D's cost recovery is 14.3× and its subsidy is 0.
* **Fix:** use explicit tariffs by customer class, capped at the regulated tariff. Apply the affordability cap to household revenue only, at min(cap, cost-reflective tariff). Compute the subsidy as PV cost minus PV of revenue by class.

## Minor

### F10 (P, D): the DSRA is never drawn, and shortfalls go to equity support while the reserve stays full
* **Where:** `model.py:357-385`.
* **What is wrong:** the reported liquidity requirement is overstated by up to the DSRA balance, and the DSRA is equity-funded dead money.
* **Repro:** `p07_dsra_never_drawn.py`. In operating quarter 0, the DSRA holds 6.42 M while equity support is 11.15 M.
* **Status:** consistent with spec §5 ("DSRA = target"), but not in known-limitations.
* **Fix:** draw the DSRA before equity support, and refill it from cash ahead of distributions.

### F11 (P): the minimum cash balance is first funded at COD as "equity support"
* **What is wrong:** it should be funded in construction. It inflates `equity_support_total` and triggers `W_SUPPORT` on any project with `min_cash > 0`.
* **Repro:** `p09` (exactly 5.0 M of the 11.15 M at operating quarter 0).
* **Fix:** add min cash to construction uses (S&U).

### F12 (P): the deferred grant is not released when the residual value disposes of the NBV at the horizon end
* **Where:** `model.py:294-298`.
* **What is wrong:** it remains a liability (20.7 M on a 15 year horizon), contrary to spec §6. With residual value 0, the NBV (67.5 M) also stays on the closing balance sheet with no write-off.
* **Repro:** `p04`.
* **Effect:** P&L only, unless the grant is taxable.
* **Fix:** release the deferred grant on any disposal, and write off the NBV at the horizon end.

### F13 (P): the unlevered tax omits disposal gains and losses, and grant income when it is taxable
* **Where:** `model.py:331`.
* **What is wrong:** the project IRRs are inconsistent with the levered tax in closure and residual value cases (p12 shows the unlevered tax ignoring the closure).
* **Fix:** include `disposal_gain`, and grant income when taxable, in the post-subsidy unlevered base.

### F14 (P): tenor longer than the horizon, or grace at least as long as the tenor, is not rejected at input
* **What happens:**
  * tenor longer than the horizon gives FAILED_CHECKS (`REPAID`) instead of an input error;
  * grace ≥ tenor silently extends maturity: `n_amort = max(...,1)` (`model.py:178`) makes a bullet at COD + grace, beyond the stated tenor.
* **Repro:** `p08`.
* **Fix:** validate grace < tenor×4 and tenor ≤ operating years.

### F15 (P): a battery life under 0.125 years produces no replacements at all
* **Where:** `step == 0`, `model.py:133-135`.
* **Repro:** `p08` gives the same result as a 40 year life.
* **Fix:** validate `battery_life_years >= 0.25` (or `ceil`).

### F16 (P): the optimizer crashes when a feasible option has zero lifecycle cost
* **Where:** `cost_recovery_ratio=None` reaches `min()` in `_score`.
* **Repro:** `p11`, last block (TypeError).

### F17 (P, D): the optimizer's D and F options are asymmetric
* **What is wrong:** F is D plus a daytime-anchor credit on battery sizing (battery 257 against 284 kWh). D on the same settlement does not get that credit, so F dominates D by construction rather than by technology.
* **Repro:** `p11`.

### F18 (D): grid options serve 100% of demand regardless of supply hours
* **What is wrong:** with 8 hours a day, the only effect is the service tier. This is partly covered by L10 ("generation adequacy").

### F19 (D): asset transfer compensation is applied to an NBV that includes capitalised IDC and fees
* **Where:** `model.py:289`.
* **Repro:** `p12` (2.9 M of financing costs in the base).
* **Fix:** confirm the treatment against the cited rule, or use the NBV of physical assets.

### F20 (D): a replacement can fall in the last quarters with no salvage credit when `residual_value_pct_nbv = 0`
* **Example:** a battery life of 19.75 years places a full replacement in quarter T-1.
* **Effect:** LCOE and the minimum revenue requirement also ignore residual value.

### F21 (D): definitions to note
* **Minimum revenue requirement:** excludes tax, bad debt and commercial losses, so it is the revenue *collected* before tax, not the revenue billed. Label it as such.
* **LLCR:** discounts at a share-weighted rate that mixes USD and LCY rates on LCY CFADS, and excludes the DSRA balance. This is acceptable if stated.

## Checked and found correct (no finding)
* **Timing (p13):**
  * grace and tenor give first and last principal at operating quarters 4 and 31;
  * annuity is level and computed on the post-grace opening balance (in USD for USD tranches);
  * the final instalment clears the balance;
  * RBF lag 2 means first payment at operating quarter 2;
  * linear ramp;
  * replacements at operating quarters 32 and 64;
  * milestones on the stated quarters;
  * annual DSCR grouped from COD;
  * payback as specified;
  * the final quarter distributes all cash.
* **Treatments:** IDC and fees are equity-funded, capitalised and excluded from unlevered depreciation. The FX revaluation on the opening balance reconciles the debt roll forward. The MRA nets the lumpy replacement out of CFADS.
* **Edge cases (p08)** that run cleanly: zero debt, 1 construction quarter, 30 operating years, battery life longer than the horizon, collection 1.0, `rbf_cap` 0, grant greater than capex, grid arrival in year 1 (all treatments, interconnect factors 0), tariff 0 and zero customers (INCOMPLETE).
* **Pareto logic:** the dominance test is correct.
