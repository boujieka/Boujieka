# AEF SHS PAYGo Model — change log

## v0.7 — PAYGo Financial Benchmark Database (started) and branded cover

**Branded cover.**
- New **Cover** page: the Africa Energy Finance logo (`brand/aef_logo.png`) on a deep-green title panel with gold rules, in the brand colours sampled from the logo (#0B3020 / #B07C0F).
- Credits "Author & ideation: Emmanuel Boujieka Kamga". The workbook author property is set to the same name.
- Live status panel: master check (green / red), investment readiness, scenario, credit data mode, currency. Hyperlinks to Contents, Investment summary and Investment readiness. Disclaimer and copyright line.
- The former cover content (how to use, sheet index, colour code) moved to a new **Contents** sheet.
- Logo hygiene: the transparent PNG had about 12,000 near-invisible coloured fringe pixels (alpha ≤ 7). They are cleared in the working copy; the original is kept as `brand/aef_logo_original.png`.

**Benchmark database (v0.7).**
- **Single source of truth:** `benchmarks/db/paygo_financial_db.csv`. Schema in `docs/benchmark-database-schema.md`.
- **New sheets:**
  - `Benchmark_DB`: raw records with normalisation to USD m / count / ratio.
  - `Benchmark_Matrix`: company-year × 37 line items, plus live model rows Y1–Y5.
  - `Benchmark_KPIs`: 23 derived ratios, including margins, growth, receivables / inventory / payables days, cash conversion cycle, debt / receivables, debt / EBITDA, ECL ratios, per-customer metrics and active ratio.
  - `Benchmark_Compare`: the model against graded peers (n, min, median, max, position, with an "n<3: anecdotal" warning).
- **First load:** 37 records on M-KOPA, Sun King, d.light, Bboxx, ZOLA, Engie Energy Access (Fenix) and Watu (an asset-finance comparable, not solar).
  - 23 usable.
  - 14 kept but excluded, because they conflict, have no period, are half-year only, are D-grade or differ in definition.

**Conflicts found and NOT resolved (excluded until primary filings are read)**

| Item | Source 1 | Source 2 |
|---|---|---|
| M-KOPA FY2024 revenue | USD 416m / KES 53.7bn (TechCabal) | USD 253.5m (Kenyan Wall Street) |
| M-KOPA FY2023 net loss | USD 24.7m (TechCabal) | USD 20.6m (Kenyan Wall Street) |
| Bboxx FY2022 revenue | GBP 31.9m (Tracxn) | USD 21.34m (CB Insights) |
| Watu revenue | FY2025 "revenue" KES 28.3bn (+92.7%) | FY2024 "gross revenue" KES 29.9bn (different definitions) |

**Consequence for v0.6 items:**
- Source_Register SR01 is now flagged as a conflict.
- The Calibration net-margin reference (2.2%) is marked provisional, because it would be 3.6% with the other revenue figure.

**Primary filings needed (Companies House was not reachable from the build environment)**
1. M-KOPA Holdings Ltd (10891868): full accounts FY2023 and FY2024.
2. BBOXX LTD (07177839): full accounts FY2020–FY2022, and the administrators' statement of affairs and progress reports.

Download the PDFs into `benchmarks/filings/`. The line items will then be extracted into the CSV at grade A.

## v0.2 → v0.6

**Starting point.** The specification ("Change Log — From Initial Model to v0.6 Market Benchmark") describes a v0.3–v0.6 workbook. That workbook is **not in this repository** (no branch contains it), and the cells it cites (`Inputs!C71:C73`) are empty in v0.2. Its v0.3 section matches v0.2 exactly (same covenants, valuation inputs, lags and FX pass-through), so v0.2 was treated as the existing model.

**Approach.** v0.4–v0.6 were applied as **extensions** of the v0.2 generator (`tools/build_shs_model.py`). Every v0.2 sheet, formula chain and check was kept. Nothing was rebuilt from scratch.

**If you hold a separately edited v0.6 workbook:** upload it to `volumes/02-solar-home-systems/model/archive/`. It will then be reconciled line by line against this build.

## Pre-modification steps (spec §29)

| Step | Result |
|---|---|
| Inspect workbook, inventory sheets, formulas and cross-sheet dependencies | `model/INVENTORY_v0.2.md`: 25 sheets, 58,675 formulas, dependency map per sheet |
| Named ranges | 0. The generator registers row keys instead (documented in `engine/engine-spec.md` §2) |
| Hard-coded cells | Only on Inputs / Products / Scenarios (blue font) |
| Excel errors | 0 (formulas-engine evaluation, Base and Severe) |
| Backup | `model/archive/AEF_SHS_PAYGo_Model_v0.2.xlsx`, plus git tag `shs-model-v0.2` |

## Implementation map

| Spec § | Item | Implemented as | Notes / deviations |
|---|---|---|---|
| 2 | 5 tiers; T4 36 m, T5 48 m | Unchanged from v0.2 | |
| 2 | Fix `Inputs!C73 = 2*C72` (PERFORM 2x for T5) | `Products` row *PERFORM ownership horizon (2 x tenor)*, one formula per tier column, each referencing its own tenor. Check: *PERFORM horizon = 2 x tenor for every tier* | The cross-tier error cannot occur in this layout. The check catches any manual override. |
| 3–6 | v0.3 executive summary, lender layer, investor layer, credit realism | Present since v0.2 | Hypotheses identical to the spec |
| 7 | Credit_Assumptions | New sheet. Includes data mode, default 180 DPD, Stage 2 30 / Stage 3 90, BB max DPD, recovery cost, cure rate, ECL discount rate, proxy DPD shares and a derived bucket table | Repossession lag stays on Inputs (single source), linked here |
| 8 | Credit_Input | New sheet: 5 tier blocks × 60 monthly observations × 19 variables | ERP → Credit_Input → Credit_Engine |
| 9 | Credit_Engine | New sheet. A PROXY block (projection) and a SELECTED block (Proxy or Actual) per tier | **Design decision:** company history (Actual) is used for reporting and diagnostics. Projections, the P&L and the facility always run on the proxy curves, so actual history is never mixed into forecasts. The PD proxy is labelled "NOT an audited IFRS 9 PD" everywhere. |
| 9 | Proxy DPD buckets | Paying-account balances split current / 1–30 by input share. Receivables at risk split 31–60 / 61–90 / 91–180 / 180+ by input shares | Reconciles exactly to gross receivables (check). The proxy engine has no cures. |
| 10 | Credit_Portfolio | New dashboard, consolidated, selected mode | |
| 11 | RBF engine, 4 modes | New `RBF_Engine` sheet. Modes: sales-based, repayment-linked (payout = repayment rate at verification ÷ target, capped at 100%), ownership-linked, hybrid. Outputs selected RBF, variance vs sales-based, and design mode. | Ownership-linked pays **0** unless the evidence switch = 1 **and** validated ownership data exist in Vintage_Input |
| 12 | Consumer_Risk | New sheet. Per tier: income, instalment, burden, down payment / income, APR, affordability flag, PERFORM and consumer-protection evidence status | Incomes are labelled "ILLUSTRATIVE — TO BE REPLACED" |
| 13 | Covenants v0.4+ | Added 30+ DPD, 90+ DPD, borrowing-base headroom and breach, indicative ECL and coverage, and a composite credit flag (part of "any covenant") | Tested on the projection |
| 14 | Checks | 13 new integrity checks (25 in total) feeding the master check, plus 5 **readiness flags** kept outside the master check | Affordability review and data horizon are readiness flags, so a default model reads OK. Master check has no circularity. |
| 15 | Investment-grade gates | New `Investment_Readiness` sheet: 23 gates (auto + manual). Banner: "INVESTMENT READINESS: x/23 gates met — NOT investment grade" | Never claims investment grade (Rule 3). Wording removed from READMEs too. |
| 16 | Vintage_Input | New sheet: 5 tiers × 60 cohorts, mode per cohort, checkpoints M3–M60 for collections, due, 30+, 90+, 180+ default, recoveries and active accounts, plus ownership at 2x | |
| 17 | Vintage_Engine | New sheet. Proxy table per tier and checkpoint, plus cohort rows selected per cohort mode | Ownership = 0 in Proxy mode. An Actual cohort with no data shows blank, never a silent proxy. |
| 18 | Vintage_Dashboard | New sheet: mode, coverage, ownership evidence, M12 tier summary, mix-weighted vintage curve with chart, readiness flags | |
| 19–21 | Market data | New in-workbook `Source_Register` with 23 graded entries, each fact-checked by web search on 2026-10-02 | **Corrections to the spec's data:** see below |
| 22 | Market_Benchmark | New matrix pulled from Source_Register by key, plus a "This model, Year 5" row with derived diagnostics | Unconfirmed figures are shown but flagged |
| 23 | Calibration | New sheet: growth, margin, debt / receivables, portfolio maturity, credit, receivables financing, revenue mix. Each row has a model value, reference, grade, guidance and diagnostic text | Diagnostics flag questions. They never change inputs. |
| 23 | Revenue beyond hardware/financing | New inputs for digital loans / other services (net take rate per active account, margin) | Default 0. Simplification: no on-balance-sheet lending. |
| 23 | Securitisation option | New input: structure 1 = warehouse, 2 = securitisation (own rate, advance-rate haircut, upfront fee) | Fee is paid the month after a drawing, to avoid a circular reference |
| 24 | Company_Cases | New sheet, 6 companies. Facts cite Source_Register IDs only. | Lessons and implications are labelled as analysis |
| 25 | Sector sources | Listed in Source_Register (SR21–SR23) | GOGLA guidance documents and IFC/AFC: URLs still to be added |
| 27 | Rules 1–8 | See "Rules compliance" below | |

## Corrections to the market data in the specification (fact-check 2026-10-02)

| Item in spec | Finding | Treatment |
|---|---|---|
| M-KOPA FY2024 revenue $416m, +66%, net profit $9.2m, FY2023 loss $24.7m | Matched, but only via a secondary source (TechCabal, 7 Oct 2025, citing UK filings) | Grade C. Upgrade to A when the filing is retrieved. |
| Sun King ~10m customers | Source wording is "almost 10 million" **cumulative loan customers**, not active customers | Labelled cumulative |
| Sun King $6.5m MSME bond (2024) | **Not confirmed.** Found instead: Symbiotics green bonds totalling $17m and a separate $10m Proparco bond | Grade D; excluded from benchmark and calibration |
| d.light "~$718m debt raised since 2020" | It is the **securitisation purchasing capacity** of five facilities, not total debt | Relabelled |
| d.light revenue ≈ $301m | Third-party database estimate, method not stated | Grade D; "ESTIMATE — DO NOT USE AS HARD BENCHMARK" |
| Bboxx accounts | BBOXX LTD (07177839). Latest filed accounts are FY2022; FY2023 overdue. In administration since 19 May 2025. | Grade A (filings, via search snippets) |
| Pawame 18,700 financed / ~16,000 active | **Not confirmed** by any source found | Grade D; excluded. Active/originated ratio not used. |
| ZOLA ≈ $90m "recent" financing | The round was **September 2021** ($45m equity + $45m debt) | Grade C; labelled 2021 |

Most verifications rest on search-engine snippets, because direct page fetches were blocked in the build environment. Open each source before external use.

## Rules compliance

1. **No fabricated data.** Every market figure has an ID, value, unit, period, grade, status, publisher and URL (or "no source found"). Unconfirmed figures are shaded and excluded.
2. **Proxy ≠ Actual.** A single data-mode switch for credit; a mode per cohort for vintages. Labels on every dashboard. Actual cohorts without data show blank.
3. **No false investment-grade claim.** Readiness banner only.
4. **Credit engine central.** The borrowing base now flows from Credit_Engine (max-DPD eligibility) into the facility.
5. **Cohort data > generic assumptions.** Calibration guidance says so, and Actual cohorts override proxies on the dashboards.
6. **Outcome-aware RBF.** Four modes; ownership-linked blocked without validated data.
7. **Consumer protection = financial risk.** Consumer_Risk feeds readiness gates and flags.
8. **Lender vs investor views.** Lender: Covenants, Credit_Portfolio, borrowing base, DSCR, liquidity, ECL. Investor: Valuation, IRR/MOIC, exit.

## Post-modification verification (spec §29)

See "QA performed on v0.6" in the volume README.
