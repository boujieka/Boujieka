# BANKABLE HYDRO: Practical Video Course and Model Walkthrough
## Curriculum, lesson scripts and exercises (v1.0)

**Format:** 8 modules, 32 lessons, about 6.5 hours of video plus exercises.
**Recording status:** scripts and screen-action notes only. Not yet recorded.
**Tools:** `model/Bankable_Hydro_Model.xlsx`, `book/BANKABLE_HYDRO_Manuscript.md`.

### Each lesson has

- **Objective.** One sentence.
- **Script outline.** Talking points, 6–15 minutes.
- **Screen actions.** Exactly what to click in the model.
- **Check-your-understanding question.**

---

## Module 0: Orientation (20 min)

| # | Lesson | Objective | Screen actions |
|---|---|---|---|
| 0.1 | Why hydro projects stall | Name the three failure points: no lender, risk shifted to the state, liability emerges later | Dashboard verdict line |
| 0.2 | The five layers and the value chain | Map river → financial close | `00_README` sheet map |
| 0.3 | Model conventions | Read the colour codes and the time-series layout | `02`, `06` (rows 4–5), `33_CHECKS` |

**Script excerpt (0.1):** "Technical feasibility is not bankability, and bankability is not sustainable public finance. In this course we will take one fictional project, Lumora Falls, and test whether it can deliver bankable power without leaving the Republic of Navaria with a liability it cannot afford."

## Module 1: Resource and plant (60 min)

| # | Lesson | Screen actions | Question |
|---|---|---|---|
| 1.1 | From flow to MW | `03` monthly table; change design flow 450 → 400 | Why does energy fall less than design flow? |
| 1.2 | P50, P75, P90 | Change CV 12% → 18%; read P90/P50 and Gate 1 | Which gate test changes status? |
| 1.3 | Four kinds of capacity | `04` rows: installed, available, generation, delivered, contracted | Give an example where delivered < generation |
| 1.4 | Drought and climate | Toggle `st_drought`, then `st_climate` | Why does DSCR fall only modestly? (two-part tariff) |
| 1.5 | CAPEX and the reference class | `05` benchmark; toggle `st_capex` | What overrun does the reference class suggest, median and mean? |
| 1.6 | Delay | Toggle `st_delay`; read COD, IDC, financing gap | Why does delay increase the financing gap? |

## Module 2: Transmission and demand (50 min)

| # | Lesson | Screen actions | Question |
|---|---|---|---|
| 2.1 | Cost of the evacuation line | `08` inputs; switch `tx_party` 1 ↔ 2 | How do the fiscal numbers move when the project builds the line? |
| 2.2 | Transmission readiness gap | Toggle `st_trans`; read `tx_gap_yrs`, deemed energy, Gate 4 | Who pays for deemed energy? |
| 2.3 | Grid absorption | `09` absorption limit; reduce `minload` | When does the grid, not the line, constrain? |
| 2.4 | Four kinds of demand | `10` rows: potential, commercial, contracted, bankable | Why is "potential" demand not bankable? |
| 2.5 | Low demand | Toggle `st_demand` | Which party absorbs the demand risk under deemed energy? |

## Module 3: The offtaker (55 min). Core module

| # | Lesson | Screen actions | Question |
|---|---|---|---|
| 3.1 | Building the utility cash model | `12` sections A–C | Which three inputs move cash fastest? |
| 3.2 | Maximum sustainable PPA payment | Change `ut_cov` 1.2 → 1.0 | What does the coverage buffer represent? |
| 3.3 | Offtaker stress | Toggle `st_offtaker`; read `u_gap`, Gate 5, fiscal NPV | Why do the project's lenders not see the problem? |
| 3.4 | Routing the gap | Set `backstop` = 0; then structure 2 vs 3 | Where does the shortfall land in each case? |
| 3.5 | FX: the silent transfer | Toggle `st_fx`; then set `lc_share` = 0.3 | How does partial local-currency pricing change the utility ratio? |

## Module 4: Regulation and the PPA (45 min)

| # | Lesson | Screen actions | Question |
|---|---|---|---|
| 4.1 | Regulatory Bankability Matrix | `13`: change "FX convertibility" GAP → CRITICAL GAP | What happens to the overall verdict? |
| 4.2 | E&S readiness | `13` E&S inputs; Gate 9 | Why is E&S a bankability gate? |
| 4.3 | Two-part tariff design | `14`: move value from the energy charge to the capacity charge | How do hydrology risk and utility risk trade off? |
| 4.4 | Deemed energy and take-or-pay | `deemed` 1 → 0 with `st_trans` ON | Who now bears transmission delay? |
| 4.5 | Termination | `23` `x_term` row | Why is termination usually the largest contingent liability? |

## Module 5: Project finance (60 min)

| # | Lesson | Screen actions | Question |
|---|---|---|---|
| 5.1 | Sources and uses | `17` sections A–B | Why are IDC and DSRA equity-funded here? |
| 5.2 | Sculpting and debt capacity | `18` sculpt row; change `str_dscr` | What limits debt: gearing or DSCR? |
| 5.3 | Lender case vs equity case | `lender_case` 3, `gen_case` 1 → 3 | Why do lenders use P90? |
| 5.4 | Locking debt for stress tests | Copy `debt_m` to `lock_m`; `debt_mode` = 2 | Why must debt be locked before stresses? |
| 5.5 | Tenor as a tariff lever | Change `str_nm` 18 → 25 (check `33`) | How much does tenor move the financing gap? |
| 5.6 | IRR, NPV, LCOE (plant vs system) | `17` KPIs | What explains the gap between plant and system LCOE? |

## Module 6: Five structures (40 min)

| # | Lesson | Screen actions | Question |
|---|---|---|---|
| 6.1 | Structure library | `17A` columns E–I | Which structure has the lowest required tariff, and why? |
| 6.2 | Closed-form comparison | `17A` comparison block | Why does gross public exposure barely change? |
| 6.3 | Full-engine snapshot | `17A` snapshot table | Why does the hybrid structure give a 26% equity IRR at the same tariff? |
| 6.4 | Designing a grant properly | Exercise: cut `fx_tariff` until the hybrid equity IRR = target | What tariff cut matches the grant? |

## Module 7: Public finance (50 min)

| # | Lesson | Screen actions | Question |
|---|---|---|---|
| 7.1 | Direct support | `22` | Which line dominates in the base case? |
| 7.2 | Guarantees and contingent liabilities | `23`, `24` | Why are exposures not additive? |
| 7.3 | Expected loss: use with care | `24`: change `pr_ppa` | Why must probabilities be labelled judgements? |
| 7.4 | Fiscal NPV and annual cash need | `25` | How can fiscal NPV improve while the project gets worse? (transmission delay) |
| 7.5 | Project-level fiscal exposure screening | `26`: change `dsa_rating`, `debt_gdp` | Why is this not a DSA? |

## Module 8: Bankability and decision (40 min)

| # | Lesson | Screen actions | Question |
|---|---|---|---|
| 8.1 | The nine gates | `30` tests and thresholds | Why weakest-link rather than weighted average? |
| 8.2 | Top 5 gaps and actions | `32` lower panel | Draft a pre-close action plan |
| 8.3 | Capstone: rescue Lumora | See below | – |
| 8.4 | Ten rules for financial close | Book Chapter 17 | – |

### Capstone exercise (8.3)

**Starting position:** Combined stress ON (overrun + delay + offtaker + FX), structure 3.

**Task:** Using only legitimate levers, reach a verdict of at least "NOT YET BANKABLE" with fiscal screen ≤ MODERATE. Legitimate levers are:

- structure choice;
- tenor;
- concessional share;
- local-currency tariff share;
- tariff level;
- payment security;
- transmission financing;
- regulatory fixes.

*(Not tested by the author as achievable; concluding that it cannot be done without unacceptable public exposure is a valid answer.)*

**Deliverable:** a 1-page memo covering:

- the levers chosen;
- the residual public exposure;
- who bears each remaining risk.

**Marking guide:**
- Verdict and fiscal-screen improvement: 30%.
- Honesty about residual risk: 30%.
- Rejection of "magic" levers, such as unrealistic flows or zero CAPEX: 20%.
- Clarity: 20%.

---

## Production notes

- **Screen capture:** zoom 110%, freeze panes on, with the dashboard in a second window.
- **Use only the fictional project on screen.** When citing real cases, show the source ID from `research/` on screen.
- **On-screen disclaimer** in every module: "Educational; not investment, legal or tax advice."
