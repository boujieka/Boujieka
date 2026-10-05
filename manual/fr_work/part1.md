# MANUAL 7: User and Methodology Manual

## MODEL 7, Hydropower Development and Finance Model

Version 1.0 release candidate 1. Companion to Book 7, *Hydropower Development and Finance*.

| Item | File |
|---|---|
| Workbook | `model/Bankable_Hydro_Model.xlsx` |
| Generator (single source of truth) | `model/build_model.py` |
| Cell map written by the generator | `model/model_map.json` |
| Full-engine scenario results | `model/snapshot_results.json` |
| Scenario runner | `tools/run_snapshots.py` |
| Excel quoting repair | `tools/model/excel_quote_fix.py` |
| Circularity check | `tools/model/check_cycles.py` |
| Independent test report | `docs/MODEL7_TEST_REPORT.md` |
| Validation summary in the book | Book 7, Annex K |

This manual replaces `manual/USER_MANUAL.md`, which describes an earlier model built around the Lumora Falls case. Every sheet name, input, formula and figure below refers to the current MODEL 7 and its default Kasiri case. Figures quoted as "base case" are the workbook's values with default inputs; figures quoted as "snapshot" come from `model/snapshot_results.json`.

---

## 1. What the model does and its place with Book 7

### 1.1 The question

The workbook opens with one question: can this project deliver bankable power without creating unsustainable public liabilities? Book 7 breaks that question into the decisions taken between a river site and financial close, and MODEL 7 is the engine that gives each decision numbers.

Book 7 rests on three ideas that the model reproduces.

1. A hydro project is three investments in one asset: a development option (site to close), a construction contract (close to commercial operation) and an operating annuity (commercial operation to end of concession). The model values each: *01A_DEVELOPMENT* for the option, *05A_CONTRACTING*, *05_PLANT_CAPEX* and *06_CONSTRUCTION* for the build, and the operating sheets for the annuity.
2. Three parties must each accept the project: the developer, the lenders and the state. The model reports each party's measures side by side on *32_DASHBOARD*.
3. The Hydro Readiness Framework asks eight questions, tested by 23 financial close gates, and ends in one close decision. The model applies the 23 gates on *30A_CLOSE_READINESS* and maps them to the book on *34_FRAMEWORK_MAP*.

| Question | Must be accepted by | Gates on 30A |
|---|---|---|
| Q1 Technically viable | Developer, lenders | 1 to 4 |
| Q2 Developable | Developer, state | 5 to 10 |
| Q3 Economic for the system | State | 11, 12 |
| Q4 Investable for the developer | Developer | 19 |
| Q5 Bankable | Lenders | 17, 18, 20, 23 |
| Q6 Buildable on budget | Developer, lenders | 13, 14, 22 |
| Q7 Affordable for buyer and state | State | 15, 16, 21 |
| Q8 Ready to close | Developer, lenders, state | All 23 |

### 1.2 The engine

The workbook is a single integrated engine that runs in this order: hydro resource, plant, transmission, grid, demand, utility, regulation, PPA, finance, PPP or IPP structure, government support, fiscal exposure, and finally the two levels of gates. A change anywhere flows through to every later link.

| Property | MODEL 7 |
|---|---|
| Sheets | 40 |
| Live formulas | about 11,260 |
| Periodicity | Annual, 40 periods (t = 1 to 40), plus ten development-year columns on *01A_DEVELOPMENT* |
| Macros, data tables, defined names, volatile functions, external links | None |
| Circular references | None (checked with `tools/model/check_cycles.py`) |
| Scenario tables | Written as static values by `tools/run_snapshots.py` |

### 1.3 The Kasiri case

The reference project is Kasiri River Hydro, a 60 MW run-of-river plant with small daily pondage on the fictional Kasiri River in the fictional Republic of Navaria. In Book 7 it is developed by the fictional Tamarind Hydro Ltd. The buyer is the fictional state-owned Navaria Electricity Company. Every input is illustrative, chosen to make the mechanics visible and to sit inside ranges found in public sources. Replace every input before using the model on a real project. The Lumora Falls scheme that appears in Book 7 as a contrast is not in the workbook.

### 1.4 Versions

| Product | Version |
|---|---|
| Book 7 | v1.0 release candidate 1 |
| MODEL 7 | v1.0 release candidate 1 |
| MANUAL 7 (this document) | v1.0 release candidate 1 |
| Case 7 (Kasiri River Hydro) | v1.0 release candidate 1 |

Version 1.0 is fixed after the workbook has been tested in Microsoft Excel and the open items in `docs/BOOK7_V04_QA_SUMMARY.md` are closed (*00_README*, "Versions").

Nothing in the model or this manual is investment, legal, tax or accounting advice.

---

## 2. Conventions

### 2.1 Colours and formats

| Convention | Meaning |
|---|---|
| Blue font | Hard-coded input |
| Light yellow fill | Ordinary input |
| Bright yellow fill | Key lever |
| Black font | Formula |
| Green font | Direct link to a cell on another sheet |
| Green shaded cell | Key output |
| Dark blue header bar | Sheet title and subtitle |
| Light blue bar | Section heading |
| Tab colours | 00 dark blue; 01 to 19 blue; 20 to 29 green; 30 to 35 red |

Status cells on *13_REGULATION*, *30_BANKABILITY*, *30A_CLOSE_READINESS*, *32_DASHBOARD*, *33_CHECKS* and *35_BOOK_CHECK* are coloured by conditional formatting: green for READY, MET, OK and PASS; amber for CONDITIONAL, PARTIAL and CHECK; orange for GAP and DEVELOPMENT GAP; red for CRITICAL GAP, NOT MET and ERROR; grey for NO EVIDENCE.

Selector inputs carry data validation that stops an invalid entry with an error message: *case* and *gen_case* accept 1 to 3, *lender_case* 1 to 4, *structure* 1 to 5, *debt_mode* 1 to 2, *backstop* and the nine stress toggles 0 or 1. Status inputs on *13_REGULATION* and *30A_CLOSE_READINESS* are drop-down lists.

### 2.2 Units

Money is in USD million (USDm), nominal, unless the label says "real 2026". Real inputs are in 2026 US dollars and are escalated by the US CPI or the capital cost escalation index. Energy is in GWh, capacity in MW, tariffs in USD/MWh. Utility local-currency flows are converted to USD equivalents at the model exchange rate (Navarian lira, NVL per USD). Negative amounts are costs or outflows unless the label says otherwise; on *25_FISCAL_IMPACT* a negative fiscal NPV is a net cost to government.

### 2.3 Timeline and layout

Time-series sheets share one layout: column A label, column B unit, column C total or key value, column D blank, columns E to AR periods t = 1 to 40. Rows 4 and 5 show the calendar year and the operating year (0 during construction and after the concession). Panes are frozen at E6.

*06_CONSTRUCTION* is the timeline master. Its flags drive every other time-series sheet:

```
year       = start_year+t-1
cons_eff   = cons_years+eff_delay
cod_year   = start_year+cons_eff
consflag   = IF(t<=cons_eff,1,0)
opflag     = IF(AND(t>cons_eff,t<=cons_eff+ops_years),1,0)
lastcons   = IF(t=cons_eff,1,0)
opyr       = IF(opflag=1,t-cons_eff,0)
```

Construction plus the concession must fit within the 40 periods; *33_CHECKS* tests it.

### 2.4 Model time for the Kasiri case

The Kasiri case runs on model time, not on calendar dates.

| Event | Model year | Source |
|---|---|---|
| Development starts (reconnaissance) | 2021 | Six stages totalling 72 months end at financial close |
| Financial close, model start (t = 1) | 2027 | `start_year` on *02_PROJECT_INPUTS* |
| Construction | 2027 to 2029 | `cons_years` = 3 |
| Commercial operation (first full operating year) | 2030 | `cod_year` |
| End of the 25-year PPA term | 2054 | `ops_years` = 25 |
| End of model horizon | 2066 | t = 40 |
| Price base year for real inputs | 2026 | `base_year` |

When Book 7 says Tamarind is "at the start of permitting", it means the stage reached (stage 4 on *01A_DEVELOPMENT*), not a calendar date.

---

## 3. Sheet map

All 41 sheets: the cover sheet, then the 40 working sheets grouped as on *00_README*.

**Orientation and control**

| Sheet | Purpose |
|---|---|
| COVER | Title, version, live status (close decision, gates met, 9-gate screen, fiscal screen, checks, book check) and links to the main sheets |
| 00_README | Purpose, philosophy, users, colour code, units, circularity, versions, limitations, sheet map |
| 01_CONTROL_PANEL | Case, generation case, lender case, structure, debt mode, budget backstop, nine stress toggles, five flexes, and an active-scenario read-out |
| 01A_DEVELOPMENT | Six development stages, budget, attrition, risk-weighted developer NPV, break-even premium, value by stage, step-ups, sell-down, developer IRR |

**Project (02 to 07, with 05A)**

| Sheet | Purpose |
|---|---|
| 02_PROJECT_INPUTS | Project identity, timing, plant size, macro and discount rates |
| 03_HYDROLOGY | Plant hydraulics, monthly flows to monthly power and energy, P50, P75, one-year P90 and ten-year P90 |
| 04_GENERATION | Installed, available, generated, evacuable, delivered and contracted energy; lender-case generation |
| 05_PLANT_CAPEX | Cost build-up including development costs, contractor premium and contingency; benchmark comparison |
| 05A_CONTRACTING | Turnkey, split-package or multi-contract structure: contractor premium and owner's share of overruns and delay |
| 06_CONSTRUCTION | Timeline master, CPI and FX indices, escalation, S-curve phasing of plant cost |
| 07_OPEX | O&M, insurance, major maintenance reserve, G&A, project transmission O&M, water royalty |

**Power system (08 to 10)**

| Sheet | Purpose |
|---|---|
| 08_TRANSMISSION | Line, substation and reinforcement cost, who builds, transmission COD, readiness gap |
| 09_GRID | System peak, absorption limit at minimum load, evacuation capacity, share of peak |
| 10_DEMAND | Segment demand, potential, commercial, contracted and bankable demand |

**Offtaker and utility (11, 12)**

| Sheet | Purpose |
|---|---|
| 11_OFFTAKER | Offtake split, payment security in months of billing |
| 12_UTILITY | Simplified utility cash model, maximum sustainable PPA payment, payment gap, no-project counterfactual |

**Regulation, PPA, tariff and revenue (13 to 16)**

| Sheet | Purpose |
|---|---|
| 13_REGULATION | Regulatory readiness matrix (16 items) and E&S readiness inputs |
| 14_PPA | Capacity and energy charges, indexation, currency share, deemed energy, take-or-pay, termination premium |
| 15_TARIFF | Escalated tariff, blended tariff, LCOE row, affordability headroom |
| 16_REVENUE | Energy paid, billed revenue, routing of the utility shortfall, cash revenue, lender-case revenue, revenue quality |

**Finance (17 to 21, with 17A)**

| Sheet | Purpose |
|---|---|
| 17_PROJECT_FINANCE | Funding base, sources and uses, debt capacity, financing gap, key results |
| 17A_STRUCTURES | Five structures for the same project, live closed-form comparison, full-engine snapshot |
| 18_DEBT | Locked-mode inputs, closed-form IDC factors, lender-case CFADS, sculpting, two tranches, DSRA target |
| 19_EQUITY | Equity totals, returns by holder, termination value of private equity |
| 20_CASH_FLOW | Construction funding, operating waterfall, DSRA movements, distributions, equity cash flows, LCOE streams |
| 21_TAX | Depreciation, loss carry-forward, tax holiday, unlevered tax |

**Public finance (22 to 26)**

| Sheet | Purpose |
|---|---|
| 22_GOVERNMENT_SUPPORT | Direct government cash exposure |
| 23_GUARANTEES | Exposure by instrument, year by year |
| 24_CONTINGENT_LIABILITIES | Maximum simultaneous exposure, deterministic calls, expected loss |
| 25_FISCAL_IMPACT | Net fiscal cash flow, central and consolidated fiscal NPV |
| 26_DEBT_SUSTAINABILITY | Project-level fiscal exposure screening (not a debt sustainability analysis) |

**Scenarios and risk (27 to 29)**

| Sheet | Purpose |
|---|---|
| 27_SCENARIOS | Case table, stress parameters, effective levers, full-engine scenario snapshot |
| 28_SENSITIVITY | Live closed-form LCOE tornado, full-engine sensitivity snapshot |
| 29_RISK_ALLOCATION | 16 risks against 8 parties, mitigability and instruments |

**Gates, results and assurance (30 to 35)**

| Sheet | Purpose |
|---|---|
| 30_BANKABILITY | 9-gate bankability screen for the development stage, weakest-link scoring, ranked actions |
| 30A_CLOSE_READINESS | 23 financial close gates, evidence first; decision ladder; summary by framework question |
| 31_CASE_STUDY | Kasiri against 15 public benchmark cases (unit cost as published, unadjusted) |
| 32_DASHBOARD | Headline results for project, finance, developer, power system, utility, public finance; both gate levels; top five gaps and actions; four charts |
| 33_CHECKS | 14 integrity checks |
| 34_FRAMEWORK_MAP | Each of the 23 gates mapped to its question, accepting party, model sheet, metric and book chapters; the 9-gate screen mapped to questions |
| 35_BOOK_CHECK | Live model against the Kasiri figures printed in Book 7 |

---

## 4. Quick start (15 minutes) on the Kasiri case

Open the workbook with default inputs. If it was last saved by LibreOffice, run `tools/model/excel_quote_fix.py` on it before opening it in Excel (section 7.6).

**Step 1. Check the defaults (2 minutes).** On *01_CONTROL_PANEL*:

| Input | Default | Meaning |
|---|---|---|
| `case` | 1 | Base case |
| `gen_case` | 1 | P50 in the cash flows |
| `lender_case` | 4 | Debt sized on the ten-year P90 |
| `structure` | 2 | IPP (private BOOT) |
| `debt_mode` | 1 | Debt sculpted in the model |
| `backstop` | 1 | Budget covers any utility PPA shortfall |
| `bs_share` | 100% | Share of the shortfall the budget covers |
| Nine stress toggles | 0 | No stress |
| Five flexes | 0% | No sensitivity |

On *05A_CONTRACTING*, `epc_struct` = 2 (split civil and E&M packages).

**Step 2. Confirm integrity (1 minute).** *33_CHECKS* should read ALL OK and *35_BOOK_CHECK* ALL PASS. Do not read any output until both do.

**Step 3. Read the dashboard (4 minutes).** Row 4 of *32_DASHBOARD* gives the three verdicts: the 9-gate screen reads NOT BANKABLE (a critical gap must be closed), the 23-gate close readiness reads "STOP: a critical gate is not met", and the fiscal screen reads "LOW additional fiscal pressure". The blocks below show:

| Block | Base case values |
|---|---|
| Project | 60 MW; P50 292 GWh; capacity factor 55.6%; plant cost USD 156.9m real; USD 2,614/kW; COD 2030; blended tariff in operating year 2 USD 117.8/MWh; plant LCOE USD 105.9/MWh; delivered system LCOE USD 108.1/MWh |
| Financial | Project IRR 11.2%; private equity IRR 13.8% (target 15.0%); project NPV USD 16.3m; minimum DSCR 1.53x; average DSCR 1.60x; LLCR 1.59x; debt capacity USD 147.8m; debt raised USD 145.4m; financing gap USD 4.1m |
| Developer | Budget USD 9.0m real over 6.0 years; probability of close 14.6%; risk-weighted NPV USD -0.95m; success-path IRR 16.0%; cash multiple 4.97x; break-even premium 18.9% of plant cost; equity step-up close to COD USD 18.3m |
| Power system | No transmission gap; 120 MW evacuation at COD; 3.3% of system peak; no curtailment |
| Utility | Collection 88%; receivable days about 120; payment capacity 5.96x the PPA bill in the worst of the first ten years; no payment gap |
| Public finance | No upfront contribution; peak contingent exposure USD 225.4m (0.56% of GDP); PV of expected loss USD 20.4m; fiscal NPV USD 34.8m central and USD -27.6m consolidated |
| 23 gates | 6 of 23 met; 7 critical gates not met |

The top-five lists rank the nine screen gates by score: Gate 6 (critical gap), Gates 1 and 5 (development gaps), then Gates 3 and 7.

**Step 4. Read why the close decision is STOP (2 minutes).** On *30A_CLOSE_READINESS*, the seven critical gates not met are 1 (flow record and review), 3 (bankable feasibility sign-off), 5 (ESIA to lender standards), 8 (land rights), 15 (six months of payment security), 17 (financing plan committed) and 19 (equity IRR at target). The summary by question at the foot of the sheet, repeated on the dashboard, shows which party is waiting for what.

**Step 5. Stress the river (2 minutes).** Set `st_drought` to 1. Debt sizing does not change, because the lender case excludes the drought window by design (section 6.9). The minimum DSCR falls below 1.0 (snapshot: 0.69x, with the DSRA drawn) and the drought-years shortfall appears on *20_CASH_FLOW*. Set it back to 0.

**Step 6. Stress the buyer (2 minutes).** Set `st_offtaker` to 1. Payment capacity falls to zero within ten years; with the backstop on, the project is paid in full and the cost moves to the budget (snapshot consolidated fiscal NPV about USD -125m). Then set `backstop` to 0: the twelve-month PPA guarantee is exhausted, the rest becomes arrears to the project, and the minimum DSCR goes negative (snapshot -0.53x). Reset both to their defaults.

**Step 7. Compare structures (2 minutes).** Set `structure` to 1, 3, 4 and 5 in turn and read *17A_STRUCTURES*, the dashboard and *30A_CLOSE_READINESS*. Reset to 2. With any change from the defaults, *35_BOOK_CHECK* will show CHECK lines; that is expected.

---

## 5. Workflows by user

Each workflow starts from the framework question the user must answer and names the sheets that answer it. All users should finish on *33_CHECKS* (ALL OK) and should record which inputs they changed.

### 5.1 Developer (Q1, Q2, Q4, with Q6)

1. Replace the hydrology on *03_HYDROLOGY* (monthly flows, head, design flow, efficiencies, e-flow, availability, CV, record length, study maturity). Q1 depends on `rec_years` and `hyd_study`.
2. Replace the cost build-up on *05_PLANT_CAPEX* and choose the contracting structure on *05A_CONTRACTING*.
3. Enter the six stages on *01A_DEVELOPMENT* (duration, real budget, probability of success) and the developer terms (premium, stake, discount rates, sell-down share).
4. Read section D: the risk-weighted NPV answers whether to start; the success-path NPV says whether the project creates value even if it closes; the break-even premium and probability say what would make the start worthwhile. If the success-path NPV is negative, the break-even probability reads "n/a: negative on the success path"; fix the value at close (tariff, premium, cost) before spending on better odds.
5. Read section F: success-path IRR, cash multiple and peak cash at risk.
6. Use `fx_tariff` on *01_CONTROL_PANEL* to see the tariff that brings the equity IRR to the target in *17A_STRUCTURES* (`str_hurdle`) and closes the financing gap. Check the effect on the utility (*12_UTILITY*) and on the consolidated fiscal NPV (*25_FISCAL_IMPACT*).
7. Enter evidence statuses for the gates without an automatic test on *30A_CLOSE_READINESS* and keep the document reference in column G.

### 5.2 Co-developer (Q4, Q2)

1. Identify the stage at which you would enter. Section D2 of *01A_DEVELOPMENT* gives, for each stage about to start, the probability of close from there (column B), the PV of value at close (C), the PV of remaining spend (D) and the risk-weighted value of the whole position (E).
2. Price entry from column E at your stage, never from the developer's sunk costs. For Kasiri at the start of permitting (stage 4): probability of close 57.8%, PV of value at close USD 3.34m, PV of remaining spend USD 2.06m, position value USD 1.28m.
3. Book 7 (Chapter 18) derives a fair share for a co-developer that funds all remaining spend as column D divided by column C at the stage of entry, about 62% for Kasiri at stage 4. Rerun with your own discount rate (`dev_rate`) and probabilities.
4. Test the levers the book uses (snapshot runs "Dev: ..."): development discount rate, premium, stage odds, grant for the feasibility stage, tariff.

### 5.3 Lender or DFI (Q5, with Q1 and Q6)

1. Choose the lender case on *01_CONTROL_PANEL*: `lender_case` 1 (P50), 2 (P75), 3 (one-year P90) or 4 (ten-year P90, default). Keep `gen_case` = 1 for the sponsor view, or set 3 to see P90 in every year of the cash flows.
2. Read *18_DEBT* (lender-case CFADS, sculpting, tranches) and *17_PROJECT_FINANCE* (debt capacity, which constraint binds, gearing, ratios). At Kasiri the gearing cap binds: debt USD 145.4m against a sculpted capacity of USD 147.8m.
3. Lock the package before stressing it. Set `debt_mode` = 2 after entering the base-case `debt_m`, `debt_c`, `s_grant` and `s_goveq` in *18_DEBT* C6 to C9 and the base-case commercial principal by operating year in row 12 (column E = operating year 1). The shipped values in these cells (USD 90m and a zero schedule) are placeholders, not the base case; with a zero schedule the commercial debt is repaid in one balloon and the balloon check on *33_CHECKS* reads WARNING. The snapshot runner fills these inputs automatically in its own copies.
4. Run the stresses one at a time, then combined (section 7). Read minimum DSCR, LLCR, the cumulative debt-service shortfall (`kpi_short`), DSRA movements on *20_CASH_FLOW* and the financing gap.
5. Check Gates 17, 18, 20 and 23 on *30A_CLOSE_READINESS* and Gates 1, 4, 5 and 7 of the screen on *30_BANKABILITY*.

### 5.4 Ministry of finance or PPP unit (Q7, with Q3)

1. Replace the country data on *26_DEBT_SUSTAINABILITY* with the latest published IMF and World Bank DSA data, and set the four screening thresholds to your fiscal risk policy.
2. Enter your own call probabilities and loss given call on *24_CONTINGENT_LIABILITIES*. They are judgements, not forecasts.
3. Set the structure on *01_CONTROL_PANEL* and read *22_GOVERNMENT_SUPPORT* (direct cash), *23_GUARANTEES* (exposure by instrument), *24_CONTINGENT_LIABILITIES* (maximum simultaneous exposure, calls, expected loss), *25_FISCAL_IMPACT* (central and consolidated fiscal NPV, peak cash need) and *26_DEBT_SUSTAINABILITY* (screen).
4. Test the routing of a shortfall with `st_offtaker`, `backstop` and `bs_share`, and the size of the PPA guarantee with `ppag_months` on *23_GUARANTEES*.
5. Use the consolidated fiscal NPV as the headline public-sector measure: it includes the state utility through the no-project counterfactual.
6. Gate 21 on *30A_CLOSE_READINESS* is met when the screen is not HIGH; ministry approval itself is evidence to be recorded outside the model.

### 5.5 Utility (Q7, Q3)

1. Replace the inputs on *12_UTILITY* with audited figures: customers, tariff, pass-through, technical and commercial losses, collection, cost of other supply and its USD share, operating cost, transfers, existing debt service, receivables.
2. Replace segment demand and other supply on *10_DEMAND*, and system data on *09_GRID*.
3. Read the maximum sustainable PPA payment against the PPA bill, the payment capacity ratio, unserved demand, the utility DSCR on existing debt, receivable days, and the incremental cash from the project (`f_soe`).
4. On *15_TARIFF*, compare the blended PPA tariff with collected revenue per MWh sent out. A negative headroom means each MWh bought costs the utility cash.

### 5.6 Transaction adviser (Q8)

1. Work through the chain in book order and keep a log of every input changed and its source.
2. Run the full engine with `tools/run_snapshots.py` (section 7.5) to obtain the scenario, structure, sensitivity, contracting and developer tables, the required tariff by structure and the break-even flow.
3. Use *29_RISK_ALLOCATION* to agree who carries what, *30_BANKABILITY* for the development-stage action list, and *30A_CLOSE_READINESS* with *34_FRAMEWORK_MAP* to turn open gates into a work programme by party.
4. Before any committee paper, confirm *33_CHECKS* ALL OK and record the snapshot date stamp.

---
