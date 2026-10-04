
# About this manual

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

# 1. What the model does and its place with Book 7

## 1.1 The question

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

## 1.2 The engine

The workbook is a single integrated engine that runs in this order: hydro resource, plant, transmission, grid, demand, utility, regulation, PPA, finance, PPP or IPP structure, government support, fiscal exposure, and finally the two levels of gates. A change anywhere flows through to every later link.

| Property | MODEL 7 |
|---|---|
| Sheets | 40 |
| Live formulas | about 11,260 |
| Periodicity | Annual, 40 periods (t = 1 to 40), plus ten development-year columns on *01A_DEVELOPMENT* |
| Macros, data tables, defined names, volatile functions, external links | None |
| Circular references | None (checked with `tools/model/check_cycles.py`) |
| Scenario tables | Written as static values by `tools/run_snapshots.py` |

## 1.3 The Kasiri case

The reference project is Kasiri River Hydro, a 60 MW run-of-river plant with small daily pondage on the fictional Kasiri River in the fictional Republic of Navaria. In Book 7 it is developed by the fictional Tamarind Hydro Ltd. The buyer is the fictional state-owned Navaria Electricity Company. Every input is illustrative, chosen to make the mechanics visible and to sit inside ranges found in public sources. Replace every input before using the model on a real project. The Lumora Falls scheme that appears in Book 7 as a contrast is not in the workbook.

## 1.4 Versions

| Product | Version |
|---|---|
| Book 7 | v1.0 release candidate 1 |
| MODEL 7 | v1.0 release candidate 1 |
| MANUAL 7 (this document) | v1.0 release candidate 1 |
| Case 7 (Kasiri River Hydro) | v1.0 release candidate 1 |

Version 1.0 is fixed after the workbook has been tested in Microsoft Excel and the open items in `docs/BOOK7_V04_QA_SUMMARY.md` are closed (*00_README*, "Versions").

Nothing in the model or this manual is investment, legal, tax or accounting advice.

---

# 2. Conventions

## 2.1 Colours and formats

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

## 2.2 Units

Money is in USD million (USDm), nominal, unless the label says "real 2026". Real inputs are in 2026 US dollars and are escalated by the US CPI or the capital cost escalation index. Energy is in GWh, capacity in MW, tariffs in USD/MWh. Utility local-currency flows are converted to USD equivalents at the model exchange rate (Navarian lira, NVL per USD). Negative amounts are costs or outflows unless the label says otherwise; on *25_FISCAL_IMPACT* a negative fiscal NPV is a net cost to government.

## 2.3 Timeline and layout

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

## 2.4 Model time for the Kasiri case

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

# 3. Sheet map

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

# 4. Quick start (15 minutes) on the Kasiri case

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

# 5. Workflows by user

Each workflow starts from the framework question the user must answer and names the sheets that answer it. All users should finish on *33_CHECKS* (ALL OK) and should record which inputs they changed.

## 5.1 Developer (Q1, Q2, Q4, with Q6)

1. Replace the hydrology on *03_HYDROLOGY* (monthly flows, head, design flow, efficiencies, e-flow, availability, CV, record length, study maturity). Q1 depends on `rec_years` and `hyd_study`.
2. Replace the cost build-up on *05_PLANT_CAPEX* and choose the contracting structure on *05A_CONTRACTING*.
3. Enter the six stages on *01A_DEVELOPMENT* (duration, real budget, probability of success) and the developer terms (premium, stake, discount rates, sell-down share).
4. Read section D: the risk-weighted NPV answers whether to start; the success-path NPV says whether the project creates value even if it closes; the break-even premium and probability say what would make the start worthwhile. If the success-path NPV is negative, the break-even probability reads "n/a: negative on the success path"; fix the value at close (tariff, premium, cost) before spending on better odds.
5. Read section F: success-path IRR, cash multiple and peak cash at risk.
6. Use `fx_tariff` on *01_CONTROL_PANEL* to see the tariff that brings the equity IRR to the target in *17A_STRUCTURES* (`str_hurdle`) and closes the financing gap. Check the effect on the utility (*12_UTILITY*) and on the consolidated fiscal NPV (*25_FISCAL_IMPACT*).
7. Enter evidence statuses for the gates without an automatic test on *30A_CLOSE_READINESS* and keep the document reference in column G.

## 5.2 Co-developer (Q4, Q2)

1. Identify the stage at which you would enter. Section D2 of *01A_DEVELOPMENT* gives, for each stage about to start, the probability of close from there (column B), the PV of value at close (C), the PV of remaining spend (D) and the risk-weighted value of the whole position (E).
2. Price entry from column E at your stage, never from the developer's sunk costs. For Kasiri at the start of permitting (stage 4): probability of close 57.8%, PV of value at close USD 3.34m, PV of remaining spend USD 2.06m, position value USD 1.28m.
3. Book 7 (Chapter 18) derives a fair share for a co-developer that funds all remaining spend as column D divided by column C at the stage of entry, about 62% for Kasiri at stage 4. Rerun with your own discount rate (`dev_rate`) and probabilities.
4. Test the levers the book uses (snapshot runs "Dev: ..."): development discount rate, premium, stage odds, grant for the feasibility stage, tariff.

## 5.3 Lender or DFI (Q5, with Q1 and Q6)

1. Choose the lender case on *01_CONTROL_PANEL*: `lender_case` 1 (P50), 2 (P75), 3 (one-year P90) or 4 (ten-year P90, default). Keep `gen_case` = 1 for the sponsor view, or set 3 to see P90 in every year of the cash flows.
2. Read *18_DEBT* (lender-case CFADS, sculpting, tranches) and *17_PROJECT_FINANCE* (debt capacity, which constraint binds, gearing, ratios). At Kasiri the gearing cap binds: debt USD 145.4m against a sculpted capacity of USD 147.8m.
3. Lock the package before stressing it. Set `debt_mode` = 2 after entering the base-case `debt_m`, `debt_c`, `s_grant` and `s_goveq` in *18_DEBT* C6 to C9 and the base-case commercial principal by operating year in row 12 (column E = operating year 1). The shipped values in these cells (USD 90m and a zero schedule) are placeholders, not the base case; with a zero schedule the commercial debt is repaid in one balloon and the balloon check on *33_CHECKS* reads WARNING. The snapshot runner fills these inputs automatically in its own copies.
4. Run the stresses one at a time, then combined (section 7). Read minimum DSCR, LLCR, the cumulative debt-service shortfall (`kpi_short`), DSRA movements on *20_CASH_FLOW* and the financing gap.
5. Check Gates 17, 18, 20 and 23 on *30A_CLOSE_READINESS* and Gates 1, 4, 5 and 7 of the screen on *30_BANKABILITY*.

## 5.4 Ministry of finance or PPP unit (Q7, with Q3)

1. Replace the country data on *26_DEBT_SUSTAINABILITY* with the latest published IMF and World Bank DSA data, and set the four screening thresholds to your fiscal risk policy.
2. Enter your own call probabilities and loss given call on *24_CONTINGENT_LIABILITIES*. They are judgements, not forecasts.
3. Set the structure on *01_CONTROL_PANEL* and read *22_GOVERNMENT_SUPPORT* (direct cash), *23_GUARANTEES* (exposure by instrument), *24_CONTINGENT_LIABILITIES* (maximum simultaneous exposure, calls, expected loss), *25_FISCAL_IMPACT* (central and consolidated fiscal NPV, peak cash need) and *26_DEBT_SUSTAINABILITY* (screen).
4. Test the routing of a shortfall with `st_offtaker`, `backstop` and `bs_share`, and the size of the PPA guarantee with `ppag_months` on *23_GUARANTEES*.
5. Use the consolidated fiscal NPV as the headline public-sector measure: it includes the state utility through the no-project counterfactual.
6. Gate 21 on *30A_CLOSE_READINESS* is met when the screen is not HIGH; ministry approval itself is evidence to be recorded outside the model.

## 5.5 Utility (Q7, Q3)

1. Replace the inputs on *12_UTILITY* with audited figures: customers, tariff, pass-through, technical and commercial losses, collection, cost of other supply and its USD share, operating cost, transfers, existing debt service, receivables.
2. Replace segment demand and other supply on *10_DEMAND*, and system data on *09_GRID*.
3. Read the maximum sustainable PPA payment against the PPA bill, the payment capacity ratio, unserved demand, the utility DSCR on existing debt, receivable days, and the incremental cash from the project (`f_soe`).
4. On *15_TARIFF*, compare the blended PPA tariff with collected revenue per MWh sent out. A negative headroom means each MWh bought costs the utility cash.

## 5.6 Transaction adviser (Q8)

1. Work through the chain in book order and keep a log of every input changed and its source.
2. Run the full engine with `tools/run_snapshots.py` (section 7.5) to obtain the scenario, structure, sensitivity, contracting and developer tables, the required tariff by structure and the break-even flow.
3. Use *29_RISK_ALLOCATION* to agree who carries what, *30_BANKABILITY* for the development-stage action list, and *30A_CLOSE_READINESS* with *34_FRAMEWORK_MAP* to turn open gates into a work programme by party.
4. Before any committee paper, confirm *33_CHECKS* ALL OK and record the snapshot date stamp.

---

# 6. Methodology and key formulas

Formulas are quoted from `model/build_model.py`, with template references replaced by the model's plain cell names. A name such as `p50` is the name used in `model/model_map.json`. "Row" in a time-series formula means the value in the same year.

## 6.1 Hydrology and P-values (03_HYDROLOGY)

Monthly long-term mean flows (Jan to Dec, m³/s): 24, 20, 28, 52, 70, 58, 40, 28, 22, 30, 46, 36. February has 28.25 days, so the year has 365.25. For each month:

```
usable flow = MIN(MAX(flow-eflow,0),q_design)
power (MW)  = MIN(rho*grav*usable*head*eta_t*eta_g/1000000,inst_mw)
energy gross= power*days*24/1000
energy net  = energy gross*avail
spill       = MAX(flow-eflow-q_design,0)
```

Annual statistics:

```
p50    = sum of monthly net energy
p75    = p50*(1-z75*cv)                 z75 = 0.6745
p90    = p50*(1-z90*cv)                 z90 = 1.2816 (one-year P90)
p90_10 = p50*(1-z90*cv*SQRT((1+rho1)/(1-rho1)/10))
cf     = p50/(inst_mw*8.76)
firm_mw= lowest monthly power*avail
```

The ten-year P90 is the P90 of the ten-year average energy. Year-to-year correlation `rho1` (default 0.3) represents the persistence of dry years: it inflates the variance of the average through the factor (1+ρ)/(1−ρ)/n. With CV 15% the Kasiri values are P50 292.5 GWh, P75 262.9, one-year P90 236.3 and ten-year P90 268.3 GWh; P90/P50 is 0.81 and the capacity factor 55.6%. The check row "theoretical power at design flow" (60.5 MW) should be at least the installed capacity.

The sheet notes that energy computed from long-term mean monthly flows overstates energy when flows exceed design flow in some years, and should be replaced by a simulation over the full record when one exists.

## 6.2 Energy (04_GENERATION)

```
p_sel     = CHOOSE(gen_case,p50,p75,p90)
p_len     = CHOOSE(lender_case,p50,p75,p90,p90_10)
drought   = IF(AND(st_drought=1,opyr>=p_drought_start,opyr<p_drought_start+p_drought_len),p_drought,1)
climate   = (1+eff_climate)^((year-base_year)/10)
rampf     = IF(opyr=1,ramp,1)
gen       = opflag*p_sel*eff_flow*drought*climate*rampf
gen_p50   = opflag*p50*eff_flow*climate*rampf
evacuable = gen*evac_ratio
delivered = MIN(evacuable,d_absorb)
gen_len   = opflag*p_len*eff_flow*climate*rampf
```

Installed, available, generated, evacuable, delivered and contracted energy are kept distinct. Curtailment for transmission or grid is `gen-evacuable`; curtailment for lack of demand is `evacuable-delivered`. Contracted energy is the P50 reference `gen_p50`. The lender-case generation `gen_len` does not include the drought factor: the drought is tested separately.

The evacuation ratio comes from *09_GRID*:

```
peak       = peak0*d_dom/base-year domestic demand
absorb_mw  = MAX(0,peak*minload-mustrun)+ic_mw
line_mw    = IF(tx_ready=1,tx_mw,tx_interim)
evac_mw    = MIN(line_mw,absorb_mw)
evac_ratio = MIN(1,evac_mw/inst_mw)
```

Demand on *10_DEMAND* grows by segment with the case growth rate, plus `eff_demg`, and is multiplied by `eff_dem` from COD. Absorbable project energy is the supply gap plus displaceable thermal generation plus contracted exports. Bankable demand is `opflag*MIN(contracted,absorbable*commercial/(domestic+exp_con))`; the worst ratio of bankable to contracted demand in operating years 1 to 5 feeds Gate 2.

## 6.3 Capital cost build-up (05_PLANT_CAPEX, 06_CONSTRUCTION, 08_TRANSMISSION)

Plant cost in real 2026 USD:

| Line | Kasiri (USDm) | Formula or source |
|---|---|---|
| Civil works | 68.0 | Input |
| Hydro-mechanical | 9.0 | Input |
| Electro-mechanical | 33.0 | Input |
| Environmental and social | 5.0 | Input |
| Engineering and supervision | 8.0 | Input |
| Owner's costs | 4.0 | Input |
| Development costs reimbursed at close | 9.0 | `cx_dev = dev_total` from *01A_DEVELOPMENT* |
| Contractor risk premium | 6.6 | `cx_epcprem = (cx_civil+cx_hm+cx_em)*epc_prem` |
| Subtotal | 142.6 | Sum |
| Physical contingency 10% | 14.3 | `capex_base = cx_sub*(1+cont)` |
| Base plant cost | 156.9 | USD 2,614/kW; 1.04x the benchmark of USD 2,515/kW |

The effective plant cost applies the case, the overrun stress, the owner's share of overruns and delay costs, and the flex:

```
eff_capex  = case_capex*(1+st_capex*p_overrun*epc_owner)*(1+fx_capex)
capex_real = capex_base*eff_capex*(1+delay_cost*eff_delay*epc_owner_d)
```

Phasing uses a sine S-curve over the effective construction period N that sums exactly to one for any N, and escalation at `capex_esc`:

```
share_t   = IF(consflag=1,SIN(PI()*(t-0.5)/N)*SIN(PI()/(2*N)),0)
capex_nom = capex_real*share*escidx       escidx = (1+capex_esc)^(year-base_year)
```

Transmission cost is `(tx_km*tx_cost_km+tx_sub+tx_reinf)*eff_capex` (USD 16.7m real for Kasiri), spent over `tx_build` years before the planned transmission COD, with a delay penalty `(1+delay_cost*eff_tdelay)` spread over `tx_build+eff_tdelay` years. `tx_party` = 1 puts the spend on government, 2 on the project. Transmission COD is `start_year+cons_years+tx_lag+eff_tdelay`; the readiness gap is transmission COD less plant COD.

## 6.4 Construction contracting (05A_CONTRACTING)

`epc_struct` selects a column of indicative parameters:

| Parameter | 1 Turnkey EPC | 2 Split packages | 3 Multi-contract |
|---|---|---|---|
| Contractor premium on civil, HM and E&M (`epc_prem`) | 12% | 6% | 0% |
| Owner's share of a cost overrun (`epc_owner`) | 30% | 55% | 90% |
| Owner's share of delay cost after LDs (`epc_owner_d`) | 35% | 60% | 90% |
| Interface risk (1 low to 3 high) | 1 | 2 | 3 |

The premium enters base cost; the owner's shares scale the overrun and delay stresses in `eff_capex` and `capex_real`. A turnkey contract therefore costs more in the base case and less under an overrun. The snapshot runs "EPC 1/2/3 base" and "EPC 1/2/3 overrun 96%" compare them with debt resized for each structure.

## 6.5 Operating costs (07_OPEX)

Real inputs are escalated by the US CPI index:

```
o_fix  = opflag*om_fix*eff_opex*uscpi
o_var  = gen*om_var*eff_opex*uscpi/1000
o_ins  = opflag*capex_real*ins*uscpi
o_mmr  = opflag*capex_real*mmr*uscpi
o_oth  = opflag*om_other*eff_opex*uscpi
o_txprj= IF(tx_party=2,tx_omc,0)+tx_wheelc
opex   = o_fix+o_var+o_ins+o_mmr+o_oth+o_txprj
o_roy  = delivered*royalty*uscpi/1000        (water royalty, paid to government)
```

The major maintenance reserve is carried as an operating cost, not as a separate reserve account.

## 6.6 PPA, tariff and revenue (14_PPA, 15_TARIFF, 16_REVENUE)

The Kasiri tariff is energy-only: capacity charge 0, energy charge USD 112/MWh (2026), half indexed to US CPI, fully in USD, with deemed energy payable for curtailment the seller did not cause.

```
fxfac   = (1-lc_share)+lc_share*lccpi/fxidx/uscpi
capc    = cap_chg*((1-cap_idx)+cap_idx*uscpi)*fxfac*eff_tariff
enc     = en_chg*((1-en_idx)+en_idx*uscpi)*fxfac*eff_tariff
deemed  = deemed flag*(curt_tx+curt_dem)
topshort= MAX(0,top*contracted-delivered-deemed)
epaid   = delivered+deemed+topshort
rev_cap = opflag*capc*inst_mw*12/1000*avail_ratio*rampf
rev_en  = enc*delivered/1000
rev_deem= enc*(deemed+topshort)/1000
rev_bill= rev_cap+rev_en+rev_deem
```

The utility shortfall is routed through three doors in order:

```
cov_backstop = IF(backstop=1,u_gap*bs_share,0)
ppag_lim     = str_ppag*ppag_months/12*rev_util
ppag_reimb   = opflag*MIN(previous ppag_out,MAX(0,u_maxppa-u_ppa))
cov_guar     = MIN(u_gap-cov_backstop,MAX(0,ppag_lim-previous ppag_out+ppag_reimb))
ppag_out     = previous ppag_out+cov_guar-ppag_reimb
unpaid       = u_gap-cov_backstop-cov_guar
rev_cash     = rev_bill-unpaid
```

The guarantee is capped at `ppag_months` of utility billing (12 by default) and is reimbursed by the utility from spare payment capacity; anything beyond becomes arrears to the project.

Lender-case revenue uses the lender generation case:

```
rev_len = rev_cap+enc*IF(deemed=1,gen_len,MIN(gen_len*evac_ratio,d_absorb))/1000
```

Revenue quality measures: fixed share of billed revenue (`rev_fixed`, 0% for Kasiri), revenue at risk between P50 and P90 in operating year 2, utility share of revenue, and lifetime support needed to sustain PPA payments. On *15_TARIFF*, affordability headroom is collected utility revenue per MWh sent out less the blended PPA tariff.

## 6.7 Development module (01A_DEVELOPMENT)

**Stages.** Six stages with duration, real budget and probability of success to the next stage:

| Stage | Months | Budget (USDm real) | P(success) |
|---|---|---|---|
| 1 Site identification and reconnaissance | 6 | 0.10 | 60% |
| 2 Pre-feasibility and start of flow gauging | 12 | 0.60 | 60% |
| 3 Feasibility study, ESIA, geotechnical and grid studies | 18 | 4.50 | 70% |
| 4 Licences, water rights, land and permits | 12 | 0.80 | 85% |
| 5 PPA, implementation agreement and tariff approval | 12 | 0.80 | 80% |
| 6 Financing: advisers, legal, insurance, close | 12 | 2.20 | 85% |
| Total | 72 | 9.00 | 14.6% |

```
dev_total = sum of budgets
dev_years = sum of months/12
dev_pfc   = PRODUCT(p1:p6)
dev_pct   = dev_total/capex_real
```

**Spend profile.** Stages run back to back and end at financial close. Each stage's budget is spread evenly over its months and allocated to the ten development-year columns before close (2017 to 2026), then escalated by `(1+us_cpi)^(year-base_year)`. For Kasiri, spend runs from 2021 to 2026 and totals USD 8.6m nominal.

**P(alive).** For each development year, the probability that the project is still alive when the money is spent is the spend-weighted average over stages of the probability of reaching that stage, `PRODUCT(p1:pk)/pk`.

**Risk-weighted NPV.** With r = `dev_rate` (25%) and all PVs taken at the start of development:

```
dev_reimb        = total nominal development spend
dev_prem         = dev_prem_pct*capex_real
dev_eq_npv_fc    = dev_stake*NPV(r_fc,eq_priv_cf)
dev_success_value= dev_reimb+dev_prem+dev_eq_npv_fc
dev_pv_cost_unw  = NPV(r,spend)*(1+r)^(10-dev_months/12)
dev_pv_cost_rw   = SUMPRODUCT(spend,P(alive),1/(1+r)^column)*(1+r)^(10-dev_months/12)
dev_pv_success   = dev_success_value/(1+r)^(dev_months/12)
dev_npv_success  = dev_pv_success-dev_pv_cost_unw
dev_enpv         = dev_pfc*dev_pv_success-dev_pv_cost_rw
```

Kasiri: value at close on the success path USD 11.27m; success-path NPV USD -1.00m; risk-weighted NPV USD -0.95m.

**Break-even premium and probability.**

```
dev_be_prem = MAX(0,dev_prem-dev_enpv*(1+r)^(dev_months/12)/dev_pfc)
dev_be_p    = IF(dev_npv_success<=0,"n/a: negative on the success path",dev_pv_cost_rw/dev_pv_success)
```

Kasiri needs a premium of USD 29.7m (18.9% of plant cost) for a zero risk-weighted NPV, and has no break-even probability because the success path itself loses value at 25%.

**Value by stage (section D2).** For the stage k about to start, with real budgets c and durations d, and start month s:

```
B (P close from here) = PRODUCT(pk:p6)
C (PV value at close) = B*dev_success_value/(1+r)^((dev_months-s_k)/12)
D (PV remaining spend)= sum over j>=k of c_j*PRODUCT(pk:p(j-1))/(1+r)^((s_j-s_k+0.5*d_j)/12)
E (position value)    = C-D
```

| Stage about to start | P(close) | Value at close | Remaining spend | Position value |
|---|---|---|---|---|
| 1 | 14.6% | 0.43 | 1.63 | -1.20 |
| 2 | 24.3% | 0.80 | 2.86 | -2.06 |
| 3 | 40.5% | 1.67 | 4.84 | -3.17 |
| 4 | 57.8% | 3.34 | 2.06 | 1.28 |
| 5 | 68.0% | 4.91 | 1.98 | 2.93 |
| 6 | 85.0% | 7.67 | 1.97 | 5.70 |

The NPV in section D (nominal spend, year by year) and the value at stage 1 in D2 (real budgets at mid-stage) answer the same question by different routes; Book 7 uses the first for the decision to start and the second for pricing entry.

**Step-ups (section E), private equity at 100%.**

```
val_fc       = NPV(r_fc,eq_priv_cf)+NPV(r_fc,eq_priv_in)
val_step_fc  = NPV(r_fc,eq_priv_cf)
val_cod      = SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_cod)^(t-cons_eff))/(1+r_fc)^cons_eff
val_step_cod = val_cod-SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_fc)^t)
```

Kasiri: value created at close USD -5.1m (the equity IRR is below the 15% close-stage rate); de-risking step-up from close to COD USD 18.3m.

**Sell-down (section F).**

```
v_cod_nom     = SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_cod)^(t-cons_eff))
sell_proceeds = sell_pct*dev_stake*v_cod_nom
```

The developer's cash flow runs over 50 columns (ten development years and the 40 model years): minus development spend; at t = 1 the reimbursement plus the premium; in every model year `dev_stake` times the private equity cash flow, reduced by `(1-sell_pct)` in operating years; and the sale proceeds in the last construction year. Kasiri: sale proceeds USD 19.5m, cash multiple 4.97x, peak cumulative cash at risk USD 10.2m.

**Developer IRR with three starting values.**

```
dev_irr = IF(ISNUMBER(IRR(cf,0.15)),IF(ABS(IRR(cf,0.15))<1,IRR(cf,0.15),-1),
          IF(ISNUMBER(IRR(cf,0.05)),IF(ABS(IRR(cf,0.05))<1,IRR(cf,0.05),-1),
          IF(ISNUMBER(IRR(cf,-0.05)),IF(ABS(IRR(cf,-0.05))<1,IRR(cf,-0.05),-1),-1)))
```

The developer cash flow changes sign several times, so the starting value matters. The formula tries 15%, then 5%, then -5%, moving to the next only when the previous one returns an error; a result of absolute value 1 or more is treated as spurious and reported as -1 (-100%). Kasiri: 16.0%. Promotes and carried interest are not modelled.

## 6.8 Financing structures (17A_STRUCTURES)

Column C reads the selected structure from columns E to I with `INDEX(E:I,structure)`.

| Parameter | 1 Public | 2 IPP | 3 PPP | 4 Hybrid | 5 Blended |
|---|---|---|---|---|---|
| Government equity | 15% | 0% | 10% | 0% | 5% |
| Grants, VGF, public capital | 0% | 0% | 5% | 35% | 8% |
| Concessional debt | 55% | 0% | 30% | 25% | 35% |
| Gearing cap (total senior debt) | 85% | 70% | 75% | 55% | 72% |
| Maximum private equity | 0% | 35% | 20% | 25% | 25% |
| Residual equity provider | Government | Private | Private | Private | Private |
| Senior debt guaranteed by sovereign | 100% | 0% | 40% | 20% | 15% |
| Senior debt recorded as public debt | 100% | 0% | 0% | 0% | 0% |
| Sovereign PPA guarantee | No | Yes | Yes | Yes | Yes |
| Termination payment obligation | No | Yes | Yes | Yes | Yes |
| FX convertibility cover | 0% | 100% | 100% | 100% | 50% |
| Concessional rate / grace / term | 2.0% / 5 / 20 | 3.0% / 5 / 20 | 3.0% / 5 / 20 | 3.0% / 5 / 20 | 2.5% / 5 / 20 |
| Commercial rate / tenor | 7.5% / 15 | 8.0% / 16 | 7.5% / 16 | 7.5% / 16 | 7.2% / 18 |
| Sizing DSCR | 1.20 | 1.35 | 1.30 | 1.30 | 1.30 |
| Private equity target IRR | 10% | 15% | 14% | 14% | 13% |

Percentages are of the funding base. Common terms: lock-up DSCR 1.10x, upfront and commitment fees 2% of senior debt, DSRA six months of next-year debt service. A structure check confirms that grants, government equity, maximum debt and maximum private equity can cover 100%.

The live closed-form comparison is a screen, not a substitute for the full engine:

```
WACC     = (goveq+govx)*gov_disc+conc*rc+comm*rm+priv*hurdle/(1-tax_rate)
WACC_ex  = WACC/(1-grant)
CRF      = WACC_ex/(1-(1+WACC_ex)^-ops_years)
tariff   = (fund_base*(1+maxdebt*(idc_km+upfront_fee))*(1-grant)*CRF+opex_y2)/p50*1000
exposure = public capital+on-budget debt+MAX(guaranteed debt+PPA guarantee,termination)
```

where commercial debt is assumed at the gearing cap less concessional debt. The full-engine snapshot on the same sheet, and the required tariff solved by the runner for structures 2 to 5, are the figures to quote.

## 6.9 Debt sizing (17_PROJECT_FINANCE, 18_DEBT)

**Funding base and uses.**

```
fund_base = u_capex+u_tx+u_devprem        (plant cost nominal, project transmission in construction, development premium)
uses      = fund_base+u_idc+u_fee+u_dsra
u_fee     = upfront_fee*(debt_c+debt_m)
```

Kasiri: 164.8 + 17.8 + 4.7 = funding base 187.3; IDC 17.4; fees 2.9; initial DSRA 7.3; total uses 215.0.

**Closed-form IDC factors.** Debt is drawn pro rata with the plant spending share, and interest accrues on the opening balance plus half the year's draw. The IDC per dollar of each tranche is therefore a constant:

```
idc_kc = str_rc*SUMPRODUCT(consflag,cumsh-0.5*share)
idc_km = rm_eff*SUMPRODUCT(consflag,cumsh-0.5*share)
rm_eff = str_rm+eff_rate_add*(1-hedge)
```

For Kasiri the sum is 1.5, so `idc_km` = 0.12.

**Lender-case CFADS and sculpting.** The lender case uses unlevered tax and depreciation without IDC and fees, which keeps the sizing free of circularity:

```
cfads_len = rev_len-opex-o_roy_len-IF(opyr>tax_hol,tax_rate*MAX(0,rev_len-opex-o_roy_len-dep_len),0)
inloan    = IF(AND(opyr>=1,opyr<=str_nm),1,0)
dfm       = IF(opyr>=1,1/(1+rm_eff)^opyr,0)
sculpt    = inloan*MAX(0,cfads_len/str_dscr-c_ds)
comm_cap  = SUMPRODUCT(sculpt,dfm)
```

Commercial debt service is sculpted to the target DSCR after concessional debt service, and capacity is its present value at the commercial rate, discounted to COD.

**Gearing cap.** Total senior debt may not exceed the cap times the funding base plus debt-funded IDC and fees. Solving for commercial debt gives a closed form:

```
gearing amount = MAX(0,(str_maxdebt*(fund_base+debt_c*(idc_kc+upfront_fee))-debt_c)/(1-str_maxdebt*(idc_km+upfront_fee)))
debt_c (sized) = MIN(str_conc,str_maxdebt)*fund_base
debt_m (sized) = MIN(comm_cap,gearing amount)
```

Kasiri: gearing amount 0.70 × 187.3 / (1 − 0.70 × 0.14) = 145.4, just below the sculpted capacity of 147.8, so the gearing cap binds. Gearing on total uses is 67.6%.

**Locked mode (`debt_mode` = 2).** Grant, government equity and concessional debt take the locked inputs `lock_grant`, `lock_goveq` and `lock_c`. Commercial debt is `MIN(lock_m,gearing amount)`, and its target debt service follows the locked principal schedule by operating year, scaled if the amount differs:

```
m_target = IF(inloan=1,IF(debt_mode=1,IF(comm_cap>0,sculpt*debt_m/comm_cap,0),
           IF(lock_m>0,INDEX(lock_ds,1,opyr)*debt_m/lock_m,0)+m_int),0)
m_prin   = IF(inloan=1,MAX(0,MIN(m_open,IF(opyr=str_nm,m_open,m_target-m_int))),0)
```

Interest floats only on the unhedged share through `rm_eff`. Equity absorbs any difference in uses.

**Tranches.**

```
c_draw = debt_c*share       c_int = str_rc*(c_open+0.5*c_draw*consflag)
c_prin = IF(AND(opyr>str_gc,opyr<=str_gc+str_nc),MIN(c_open,debt_c/str_nc),0)
m_draw = debt_m*share       m_int = rm_eff*(m_open+0.5*m_draw*consflag)
ds     = c_ds+m_ds          c_ds, m_ds = opflag*(interest+principal)
idc    = consflag*(c_int+m_int)
```

**DSRA.** The target is `IF(OR(opflag=1,lastcons=1),dsra_m/12*next-year ds,0)`. The initial balance is funded at the end of construction from equity (it sits in uses).

**Ratios.**

```
kpi_min_dscr = IF(COUNT(dscr)=0,99,MIN(dscr))
kpi_avg_dscr = IF(COUNT(dscr)=0,99,AVERAGE(dscr))
kpi_llcr     = SUMPRODUCT(cfads,dfw,inloan_all)/(debt_c+debt_m)
kpi_plcr     = SUMPRODUCT(cfads,dfm)/(debt_c+debt_m)
```

`dfw` discounts at the weighted senior rate; `inloan_all` covers the longest tranche life. The value 99 means there is no debt service.

## 6.10 Waterfall (20_CASH_FLOW)

**Construction funding.** Uses each year are plant cost, project transmission, IDC, fees and premium at t = 1, and the initial DSRA. Grants and debt are drawn pro rata with the spending share; equity is the balance, split between government and private holders by their shares.

**Operations.**

```
ebitda     = rev_cash-opex-o_roy
cfads      = opflag*(ebitda-tax-tx_spend_prj)
dscr       = IF(ds>0.001,cfads/ds,"")
avail0     = cfads-ds+cash_bf
dsra_draw  = opflag*MIN(previous dsra_act,MAX(0,-avail0))
dsra_relx  = opflag*MAX(0,previous dsra_act-dsra_draw-dsra_tgt)
dsra_top   = opflag*MIN(MAX(0,dsra_tgt-previous dsra_act+dsra_draw),MAX(0,avail0))
cash_avail = cfads-ds+dsra_draw+dsra_relx-dsra_top
shortfall  = MAX(0,-(cash_avail+cash_bf))
lock_ok    = IF(opflag=1,IF(ds>0.001,IF(dscr>=lockup,1,0),1),0)
pool       = cash_avail+cash_bf+shortfall
grepay     = IF(OR(lock_ok=1,opyr=ops_years),MIN(previous gclaim,MAX(0,pool)),0)
dist       = IF(OR(lock_ok=1,opyr=ops_years),MAX(0,pool-grepay),0)
cash_cf    = pool-grepay-dist
```

The DSRA is drawn first in a shortfall, releases only its excess over target, and is topped up only from available cash. A remaining shortfall is funded by the sovereign guarantee (share `str_guar`) and by sponsors (the rest). The sovereign's claim is repaid from later cash ahead of distributions. Cash is trapped when the DSCR is below the lock-up and released in the final operating year.

## 6.11 Tax (21_TAX)

```
dep_base = fund_base+u_idc+u_fee-s_grant
dep      = IF(AND(opyr>=1,opyr<=dep_yrs),dep_base/dep_yrs,0)
taxable  = ebitda-dep-interest in operations
loss_use = IF(AND(taxable>0,opyr>tax_hol),MIN(taxable,loss_bf),0)
tax      = IF(opyr>tax_hol,tax_rate*MAX(0,taxable-loss_use),0)
tax_unlev= IF(opyr>tax_hol,tax_rate*MAX(0,ebitda-dep),0)
```

Losses are carried forward and not used during the holiday. Tax forgone through the holiday is reported (USD 8.6m nominal for Kasiri).

## 6.12 Returns (17_PROJECT_FINANCE, 19_EQUITY)

```
ucf      = -capex_nom-tx_spend_prj-premium at t=1+opflag*(ebitda-tax_unlev)
kpi_pirr = IFERROR(IRR(ucf,0.08),"n/a")
kpi_npv  = NPV(disc_rate,ucf)
kpi_eirr = IF(s_priv>0,IFERROR(IRR(eq_priv_cf,0.1),IFERROR(IRR(eq_priv_cf,-0.1),IFERROR(IRR(eq_priv_cf,-0.5),-1))),"n/a")
eq_priv_cf = -eq_priv_in+(dist-sf_eq)*(1-gov_eq_share)
lcoe     = NPV(disc_rate,lc_cost)/NPV(disc_rate,delivered+deemed)*1000
lcoe_sys = NPV(disc_rate,lc_cost_sys)/NPV(disc_rate,delivered*(1-tx_loss))*1000
```

`lc_cost` is plant and project transmission spending, the premium, OPEX and royalty; `lc_cost_sys` adds public transmission spending and O&M. NPV follows the Excel convention (the first flow is discounted one period).

For termination, *19_EQUITY* computes the value of remaining private distributions at the target IRR by backward recursion, `e_pvfwd = (next e_out+next e_pvfwd)/(1+str_hurdle)`, and unrecovered private equity `e_unrec = MAX(0,-cumulative private equity cash flow)`.

The financing gap is the private equity required beyond what is available:

```
priv_avail = str_privmax*fund_base
fin_gap    = IF(str_resid=1,MAX(0,s_priv-priv_avail),0)
```

Kasiri: private equity 69.6 against 65.6 available, gap USD 4.1m (1.9% of uses).

## 6.13 Utility payment capacity and counterfactual (12_UTILITY)

The utility model tests whether the buyer can pay, rather than assuming it.

**Energy balance.** Utility demand is domestic demand less any mining load the project serves directly. The project supplies its utility share net of transmission losses; other supply is capped at the supply available (`d_sup`); demand above the cap is unserved.

**Cash and capacity.**

```
u_tar     = previous tariff*(1+lc_cpi*IF(AND(opyr>=1,opyr<=eff_freeze),0,ut_pt))
u_bill    = u_sales*u_tar/fx
u_collr   = MAX(0,MIN(1,ut_coll+IF(year>=cod_year,eff_coll_adj,0)))
u_subs    = ut_sub*IF(year>=cod_year,eff_sub,1)*lccpi/fxidx
u_opex    = -ut_opex*lccpi/fxidx*(0.5+0.5*u_sales/base-year demand)
u_supcost = -u_other*ut_supc*(ut_supusd*uscpi+(1-ut_supusd)*lccpi/fxidx)/1000
u_cash_pre= u_bill*u_collr+u_subs+u_opex+u_supcost-ut_ds
u_maxppa  = MAX(0,u_cash_pre)/ut_cov
u_gap     = opflag*MAX(0,u_ppa-u_maxppa)
u_ratio   = IF(u_ppa>0,u_maxppa/u_ppa,99)
```

`ut_ratio10` is the worst ratio in operating years 1 to 10 (5.96x for Kasiri). The FX rate is `fx0*(1+fx_dep)^(year-base_year)`, times `(1+eff_fxshock)` from COD.

**Counterfactual.** The model recomputes the utility's cash without the project (`u_cash_np`), buying from other supply up to its cap. The incremental cash of the state utility is:

```
f_soe = u_cash_post-u_cash_np-unpaid
```

so new arrears count as a cost to the public sector. This term carries the utility into the consolidated fiscal NPV.

## 6.14 Government support, guarantees and contingent liabilities (22 to 24)

**Direct support** (*22_GOVERNMENT_SUPPORT*): government equity, grants, public transmission capital and O&M, and the budget backstop of the PPA shortfall.

**Exposure by instrument** (*23_GUARANTEES*):

```
x_debt  = (1-str_onbud)*str_guar*debt_bal
x_ppa   = str_ppag*ppag_months/12*rev_util
x_term  = str_term*(opflag+consflag>0)*(debt_bal+MAX(e_unrec*(1+term_prem),e_pvfwd))
x_fx    = str_fxg*(ds+e_out)
x_mrg   = opflag*MAX(0,mrg*rev_cap/MAX(0.0001,rampf)-rev_cash)
x_onbud = str_onbud*debt_bal
```

**Maximum simultaneous exposure** (*24_CONTINGENT_LIABILITIES*) avoids adding the termination amount to the guarantees it would replace:

```
cl_max = MAX(x_term,x_debt+x_ppa+x_fx)
```

**Deterministic calls** in the active scenario are PPA guarantee calls, debt guarantee calls (shortfall times guaranteed share) and minimum revenue guarantee calls.

**Expected loss** uses user-judgement probabilities and a loss given call:

```
el = (pr_debt*x_debt+pr_ppa*MAX(0,x_ppa-cov_guar)+pr_term*MAX(0,x_term-x_debt))*lgd
cl_pv_el = SUMPRODUCT(el,gdf)          gdf = 1/(1+gov_disc)^t
```

Kasiri: peak exposure USD 225.4m, mostly the termination amount; PV of expected loss USD 20.4m at the default probabilities (2%, 8%, 0.5% a year; LGD 60%).

## 6.15 Fiscal NPV, central and consolidated (25_FISCAL_IMPACT)

```
f_direct  = -g_direct
f_calls   = -call_tot
f_tax     = tax
f_roy     = o_roy
f_div     = e_g_out-sf_eq*gov_eq_share
f_grep    = grepay+ppag_reimb
f_net     = f_direct+f_calls+f_tax+f_roy+f_div+f_grep
f_net_cons= f_net+f_soe
fis_npv      = SUMPRODUCT(f_net,gdf)
fis_npv_cons = SUMPRODUCT(f_net_cons,gdf)
fis_npv_el   = fis_npv-cl_pv_el
```

Kasiri at 8%: central NPV USD +34.8m from taxes and royalties; consolidated NPV USD -27.6m, because the utility pays more for Kasiri's energy than it collects per MWh. The sheet also reports the peak annual cash need, the peak need as a share of government revenue, the deepest cumulative outlay and tax forgone.

## 6.16 Fiscal screen (26_DEBT_SUSTAINABILITY)

The screen asks whether this one project adds material fiscal pressure. It is not a debt sustainability analysis.

```
s_onbud = x_onbud/gdp          s_cl   = cl_max/gdp
s_cash  = f_need/gov_rev       s_cumout = MAX(0,-f_cum)/gdp
s_arr   = u_arrears/gdp        s_inc  = s_onbud+s_cumout+s_arr
sc_debt = MAX(s_inc)   sc_cl = MAX(s_cl)   sc_cash = MAX(s_cash)
sc_post = debt_gdp+sc_debt
sc_flags= (sc_debt>th_incr)+(sc_cl>th_cl)+(sc_cash>th_cash)+AND(sc_post>th_debt,debt_gdp<=th_debt)
```

Default thresholds: material increment 1% of GDP, material contingent exposure 2% of GDP, material cash need 1% of revenue, debt benchmark 55% of GDP. The result:

| Condition | Result |
|---|---|
| No flag and DSA rating 1 or 2 | LOW additional fiscal pressure |
| Three or more flags, or at least one flag with a DSA rating of 3 or 4 or public debt already above the benchmark | HIGH additional fiscal pressure, with an instruction to escalate to the finance ministry and DSA team |
| Otherwise | MODERATE additional fiscal pressure |

Kasiri: no flag, DSA rating 2, result LOW.

## 6.17 The 9-gate development screen (30_BANKABILITY)

Each test maps a metric to a score using three explicit, editable thresholds. Direction H means higher is better:

```
H: score = IF(metric>=READY,3,IF(metric>=COND,2,IF(metric>=DEV,1,0)))
L: score = IF(metric<=READY,3,IF(metric<=COND,2,IF(metric<=DEV,1,0)))
```

Scores map to READY (3), CONDITIONAL (2), DEVELOPMENT GAP (1) and CRITICAL GAP (0). A gate's score is the minimum of its tests: no averaging and no weights.

| Gate | Test | Dir. | READY | COND. | DEV. GAP | Kasiri |
|---|---|---|---|---|---|---|
| 1 Resource | Reliable flow record (years) | H | 25 | 15 | 8 | 12 |
| | P90/P50 energy ratio | H | 0.85 | 0.78 | 0.70 | 0.81 |
| | Hydrology study maturity (1 to 3) | H | 3 | 2 | 1 | 2 |
| 2 Demand | Bankable/contracted demand, worst of years 1 to 5 | H | 1.0 | 0.9 | 0.7 | 1.0 |
| | Share of system peak at COD | L | 15% | 25% | 35% | 3.3% |
| 3 Configuration | Unit cost / benchmark | L | 1.00 | 1.25 | 1.50 | 1.04 |
| | Capacity factor (P50) | H | 45% | 35% | 25% | 55.6% |
| | Feasibility maturity (1 to 3) | H | 3 | 2 | 1 | 2 |
| 4 Transmission | Evacuation at COD / installed | H | 1.0 | 0.8 | 0.5 | 2.0 |
| | Transmission lag (years) | L | 0 | 1 | 2 | 0 |
| | Transmission financing secured | H | 1 | 1 | 0 | 1 |
| 5 Offtaker | Payment capacity / PPA, worst of years 1 to 10 | H | 1.2 | 1.0 | 0.8 | 5.96 |
| | Collection rate | H | 95% | 90% | 80% | 88% |
| | Payment security (months) | H | 6 | 3 | 1 | 3 |
| 6 Regulation/PPA | Items at CRITICAL GAP | L | 0 | 0 | 0 | 0 |
| | Items at GAP | L | 1 | 3 | 5 | 4 |
| | Fixed (capacity) share of revenue | H | 60% | 40% | 20% | 0% |
| 7 Financing | Minimum DSCR, actual case | H | `str_dscr` | `lockup` | 1.0 | 1.53 |
| | Financing gap / uses | L | 0% | 5% | 15% | 1.9% |
| | Private equity IRR vs target | H | hurdle | hurdle −2pp | hurdle −5pp | 13.8% |
| 8 Public finance | Peak cash need / revenue | L | 0.5% | 1% | 2% | 0% |
| | Peak contingent exposure / GDP | L | 1% | 2% | 4% | 0.56% |
| | Peak on-budget increment / GDP | L | 0.5% | 1% | 2% | 0% |
| | Consolidated fiscal NPV / GDP | H | 0% | −0.5% | −2% | −0.08% |
| | DSA risk rating (1 to 4) | L | 1 | 2 | 3 | 2 |
| 9 E&S | ESIA and lender-standard compliance | H | 3 | 2 | 1 | 2 |
| | Resettlement plan status | H | 3 | 2 | 1 | 2 |
| | Transboundary issues | H | 3 | 2 | 1 | 3 |

The equity IRR test uses `IF(ISNUMBER(kpi_eirr),kpi_eirr,IF(s_priv>0,-1,str_hurdle))`, so a structure without private equity passes it. The overall verdict:

| Condition | Verdict |
|---|---|
| Any gate at CRITICAL GAP | NOT BANKABLE (critical gap(s) must be closed) |
| Otherwise any DEVELOPMENT GAP | NOT YET BANKABLE (development gaps remain) |
| Otherwise lowest score 2 | BANKABLE SUBJECT TO CONDITIONS |
| All gates READY | READY FOR FINANCIAL CLOSE |

Each gate carries a pre-written action: a gap action when the score is 0 or 1, a conditional action when it is 2. The dashboard ranks gates by a key equal to the score plus the gate number divided by 100, so ties are broken in gate order, and lists the five lowest with their actions.

Reading note for Kasiri: Gate 6 is at CRITICAL GAP only because the tariff is energy-only, so the fixed share of revenue is 0%, below the 20% development-gap threshold. The threshold is illustrative; an energy-only tariff can be bankable if hydrology risk is otherwise covered, and the user should calibrate this test to the lenders' view.

## 6.18 The 23-gate close readiness and the decision ladder (30A_CLOSE_READINESS)

Each gate has an area, a critical flag and either an automatic model test or an evidence status entered by the user (MET, PARTIAL, NOT MET or NO EVIDENCE). Automatic tests return MET or NOT MET.

| # | Gate | Critical | Test or default evidence | Question |
|---|---|---|---|---|
| 1 | Flow record of at least 15 years and independent hydrology review | Y | `AND(rec_years>=15,hyd_study=3)` | Q1 |
| 2 | P90 energy confirmed by the lenders' technical adviser | Y | PARTIAL | Q1 |
| 3 | Bankable feasibility study signed off by the lenders' technical adviser | Y | `fs_level=3` | Q1 |
| 4 | Geotechnical investigation sufficient for a baseline report | Y | PARTIAL | Q1 |
| 5 | ESIA approved and compliant with lender standards | Y | `es_level=3` | Q2 |
| 6 | Resettlement action plan approved and funded | Y | `rap_level>=2` | Q2 |
| 7 | Generation licence and water-use permit granted | Y | PARTIAL | Q2 |
| 8 | Land rights secured for all project areas | Y | NOT MET | Q2 |
| 9 | PPA signed and approved by the regulator | Y | PARTIAL | Q2 |
| 10 | Implementation or concession agreement signed | Y | PARTIAL | Q2 |
| 11 | Grid connection agreement signed and transmission financed | Y | `tx_fin=1` | Q3 |
| 12 | Transmission in service no later than plant COD | N | `tx_gap_yrs<=0` | Q3 |
| 13 | EPC contract(s) signed with fixed price, completion date and LDs | Y | PARTIAL | Q6 |
| 14 | O&M arrangements and owner's team in place | N | PARTIAL | Q6 |
| 15 | Payment security of at least 6 months in place | Y | `lc_months>=6` | Q7 |
| 16 | Offtaker payment capacity at least 1.2x the PPA bill (worst of first 10 years) | Y | `ut_ratio10>=1.2` | Q7 |
| 17 | Financing plan fully committed (no financing gap) | Y | `fin_gap<=0.5` | Q5 |
| 18 | Minimum DSCR at or above the sizing target in the selected case | Y | `AND(debt_m+debt_c>0,kpi_min_dscr>=str_dscr)` | Q5 |
| 19 | Equity commitments signed and equity IRR at or above target | Y | `IF(ISNUMBER(kpi_eirr),kpi_eirr>=str_hurdle,s_priv<=0)` | Q4 |
| 20 | Political risk cover or guarantees signed | N | NO EVIDENCE | Q5 |
| 21 | Government support approved by the finance ministry; fiscal screen not HIGH | Y | `LEFT(sc_result,4)<>"HIGH"` | Q7 |
| 22 | Insurance programme placed (construction all risks, DSU) | N | PARTIAL | Q6 |
| 23 | Independent model audit completed | N | NO EVIDENCE | Q5 |

Gate 17 allows a financing gap of up to USD 0.5m. Gate 18 requires debt to exist, so a structure without senior debt does not pass it on the placeholder DSCR of 99. Gate 18 reads the selected case, so it moves with stresses.

**Decision ladder**, evaluated in this order:

```
IF fc_crit_fail>0     "STOP: a critical gate is not met"
ELSE IF fc_crit_noev>0 "STOP: critical evidence missing"
ELSE IF fc_crit_part>0 "NOT READY: critical gates partly met"
ELSE IF fc_met=fc_n    "GO: evidence complete for a close decision"
ELSE                   "CONDITIONAL GO: all critical gates met"
```

A GO says the evidence file is complete for lenders and sponsors to decide; it is not an investment recommendation. Kasiri: 6 of 23 met, 7 critical not met, 6 critical partly met, decision STOP.

The summary at the foot of the sheet counts, for each question, the gates, those met and the critical gates not met or without evidence. Q8 is the total. For Kasiri: Q1 0 of 4 met (2 critical open), Q2 1 of 6 (2), Q3 2 of 2 (0), Q4 0 of 1 (1), Q5 1 of 4 (1), Q6 0 of 3 (0), Q7 2 of 3 (1), Q8 6 of 23 (7).

---

# 7. Scenarios, stresses, sensitivities and the snapshot runner

## 7.1 Cases (mutually exclusive)

Set with `case` on *01_CONTROL_PANEL*; parameters on *27_SCENARIOS*.

| Parameter | Base | Low | High |
|---|---|---|---|
| Flow factor | 1.00 | 0.93 | 1.04 |
| CAPEX factor | 1.00 | 1.10 | 0.95 |
| Demand growth adjustment | 0.0 pp | −1.5 pp | +1.0 pp |
| OPEX factor | 1.00 | 1.10 | 0.95 |

Demand segments also switch growth rate by case.

## 7.2 Stress toggles (combinable)

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

## 7.3 Sensitivity flexes

`fx_capex`, `fx_gen`, `fx_tariff`, `fx_opex` and `fx_rate` on *01_CONTROL_PANEL* apply on top of the case and stresses. The effective levers that the engine uses are listed at the foot of *27_SCENARIOS*.

## 7.4 Live tornado (28_SENSITIVITY)

A closed-form screening LCOE on the funding base plus IDC, at the project discount rate over the PPA term:

```
lc_crf  = disc_rate/(1-(1+disc_rate)^-ops_years)
lc_base = ((fund_base+u_idc)*lc_crf+opex_y2)/p50*1000
```

Each driver is flexed both ways: CAPEX ±20%, generation ±10%, discount rate ±2 pp, OPEX ±20%, delivered share (curtailment 0 to 15%). Kasiri screening LCOE is USD 97.8/MWh, with CAPEX the widest swing. The tornado ignores tax, financing and timing; financing results come from the full engine.

## 7.5 The snapshot runner

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

## 7.6 The LibreOffice recalculation and the Excel quote fix

LibreOffice, when it saves a recalculated workbook, writes references to sheets whose names begin with a digit without quotation marks (for example `17_PROJECT_FINANCE!$C$31` instead of `'17_PROJECT_FINANCE'!$C$31`). Excel's formula grammar requires the quotes. `tools/model/excel_quote_fix.py` rewrites every formula, defined name, data validation and conditional format in the package to restore them, leaving cached values unchanged:

```
python3 tools/model/excel_quote_fix.py model/Bankable_Hydro_Model.xlsx
```

Run it after every LibreOffice recalculation that saves the shipped file, including a manual one. The snapshot runner does so automatically when it completes. A workbook written directly by `build_model.py` (openpyxl) is already quoted and is set to recalculate fully on load.

---

# 8. The two levels of gates and the framework map

## 8.1 Two levels, two stages

| | 9-gate screen | 23-gate close readiness |
|---|---|---|
| Sheet | *30_BANKABILITY* | *30A_CLOSE_READINESS* |
| Stage | Development: should we keep spending? | Transaction: does the evidence file support financial close? |
| Basis | Metrics against three thresholds | Automatic tests plus evidence statuses |
| Scoring | Weakest test sets the gate; weakest gate sets the verdict | Critical flags and the decision ladder |
| Output | NOT BANKABLE to READY FOR FINANCIAL CLOSE, with ranked actions | STOP, NOT READY, CONDITIONAL GO or GO |
| Kasiri | NOT BANKABLE (Gate 6) | STOP (7 critical gates not met) |

The two levels can disagree, and that is informative. The screen can read well while the close test reads STOP, because the close test counts only evidence that exists. The dashboard shows both on row 4 and side by side in its lower blocks.

## 8.2 The framework map (34_FRAMEWORK_MAP)

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

# 9. Integrity checks and the book check

## 9.1 33_CHECKS

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

## 9.2 35_BOOK_CHECK

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

# 10. Audit checklist for reviewers

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

# 11. Known limitations

## 11.1 What the model does not do (Book 7, Annex K)

- It is annual: no monthly construction draws, no seasonal dispatch, no peak or off-peak pricing.
- Debt and equity are drawn pro rata with spending, not equity first, which slightly flatters the equity return.
- There is no developer promote or carried interest, and no shareholder loans.
- There is no refinancing; the step-up after commercial operation is valued directly.
- The currency step is permanent in real terms, with no pass-through to local prices.
- The utility model has no balance sheet.
- Stresses are deterministic: no Monte Carlo over hydrology and currency, no joint distribution of drought, currency and utility distress.
- Stage probabilities, the development premium and the developer's discount rate are user judgements; no public data were found to calibrate them for African hydro.
- The model has been recalculated in LibreOffice and reproduced by a second engine; a test in Microsoft Excel is outstanding.

## 11.2 Further simplifications

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

## 11.3 Open low points from the independent test

The independent test (`docs/MODEL7_TEST_REPORT.md`) found five faults that were corrected (Excel quoting, developer IRR fallbacks, selector validation, the DSCR placeholder on Gate 18, the average DSCR error). Points that remain open:

1. At zero river flow the model does not degrade gracefully: division errors appear (P90/P50, LCOE, Gate 1 and the dashboard ranking).
2. Design flow is not linked to installed capacity or cost: raising it changes nothing because power is capped at installed MW, and lowering it cuts energy without cutting cost. The "theoretical power at design flow" row on *03_HYDROLOGY* is not part of *33_CHECKS*.
3. With a zero tariff and locked debt, sponsors fund the debt-service shortfall indefinitely; the model never triggers default or termination itself.
4. With no debt service, the minimum and average DSCR show a placeholder of 99. Gate 18 is protected by its debt test, but the DSCR test of screen Gate 7 would score it as READY.
5. The developer IRR returns −1 if the first starting value converges to a rate of absolute value 1 or more, without trying the other two.

The fourth open point listed in Annex K, the label of Gate 18, is closed in the workbook: the label now reads "in the selected case".

## 11.4 Open items in this release candidate (4 October 2026)

1. *35_BOOK_CHECK* returns `#VALUE!` on the private equity IRR line when that IRR is "n/a" (structure 1, which has no private equity). Because the snapshot runner stops on any recalculation error, a full rerun stops at "Structure 1". The scenario tables on *27_SCENARIOS*, *17A_STRUCTURES* and *28_SENSITIVITY* are empty in the current workbook, and `model/snapshot_results.json` comes from the previous complete run, made before *34_FRAMEWORK_MAP* and *35_BOOK_CHECK* were added; its base results match the book check.
2. The shipped workbook was last saved by LibreOffice and its formulas are not quoted; run `excel_quote_fix.py` before opening it in Excel.
3. The snapshot table header written by the runner describes the locked commercial debt as an "annuity profile"; the locked schedule is in fact the base-case sculpted principal.

---

# 12. Rebuilding or extending the model

## 12.1 The generator

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

## 12.2 Adding or changing a line

1. Add an `inp()`, `calc()` or `ts()` call on the right sheet, using existing names in the template.
2. If the line feeds a gate, add it to the `GATES` list (screen) or `GATES_FC` and `GATE_Q` (close readiness); the framework map is generated from them.
3. If the line should be tracked by the runner, add its name to `KPIS`, `EXTRA` or `TS_SAVE` in `tools/run_snapshots.py`.
4. If a printed Kasiri figure changes, update the `BOOK_CHECKS` list that builds *35_BOOK_CHECK*, and the book.
5. Rebuild, then run `tools/model/check_cycles.py` on the new file to confirm there is no circular reference.
6. Recalculate (LibreOffice through the runner, or open and save in Excel), run `excel_quote_fix.py` if LibreOffice saved the file, and confirm *33_CHECKS* ALL OK and *35_BOOK_CHECK* ALL PASS.
7. Rerun the snapshots and record the date.

## 12.3 Design rules to keep

- No macros, no data tables, no circular references. Interest during construction and fees stay closed-form; the DSRA stays equity-funded; the lender case keeps unlevered tax.
- Inputs only in blue cells; no hard-coded numbers inside formulas except physical constants and labelled conventions.
- Every new output that a reader might quote needs a definition on the sheet and, if it is printed in Book 7, a line on *35_BOOK_CHECK*.
- Use only functions available in Excel 2010 and LibreOffice; avoid dynamic arrays, LET, LAMBDA, XLOOKUP and volatile functions.

---

*The Kasiri River Hydro case, the Republic of Navaria, Tamarind Hydro and the Navaria Electricity Company are fictional. Nothing in MODEL 7 or this manual is investment, legal, tax or accounting advice.*
