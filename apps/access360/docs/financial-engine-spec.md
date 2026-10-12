# ACCESS FINANCE: financial engine specification (engine 0.1.0)

Code: `backend/app/engine/` (pure Python and NumPy, no database). Tests: `backend/tests/engine/`.

The engine is deterministic. The same inputs always give the same outputs, and every run stores a SHA-256 hash of its inputs. Monte Carlo simulation is not implemented. It will be added only after the deterministic engine has been reviewed independently.

This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS.

## 1. Timeline and conventions

| Item | Rule |
|---|---|
| Period | Quarter |
| Default horizon | Construction quarters (default 2), then 20 operating years |
| Quarter 0 | Financial close |
| COD | First operating quarter (index C) |
| Timing convention | End of period for discounting; t = 0 is discounted one quarter |
| Annual rates | Converted to quarterly as (1 + r)^(1/4) - 1 |
| IRRs | Reported annualised as (1 + r_q)^4 - 1 |
| Model currency | Local currency (LCY) |
| USD items | Converted at the quarter's rate: fx_t = fx_0 × (1 + depreciation)^(t/4) |
| Inflation | Opex index (1 + inflation)^(q/4), where q = operating quarter |
| Tariff index | (1 + inflation × tariff_indexation)^(q/4) |

## 2. Demand and energy (site economics)

**Connections.** For each customer class: connections_q = target × clip((q - start + 1) / ramp, 0, 1). New connections are the positive increments.

**Demand.** Demand_q = connections × kWh per month × 3 × (1 + growth)^(q/4) × demand factor. The demand factor is 1, except after grid interconnection.

**Capacity.** Capacity to customers = deliverable energy a year ÷ 4 × (1 - technical loss). Deliverable energy is an input taken from the engineering study. The engine does not size or dispatch the system, and a quarterly model does not replace hourly simulation.

**Energy balance.**
* Supplied = min(demand, capacity).
* Unserved = demand - supplied.
* Generated = supplied ÷ (1 - technical loss).
* Billed = supplied × (1 - commercial loss).
* Supplied energy is allocated to classes pro rata to their demand.

## 3. Revenue, opex and EBITDA

**Revenue.**
* Energy revenue = billed kWh × tariff × tariff index × tariff factor.
* Fixed revenue = connections × fixed charge × 3 × index.
* Connection fees are recognised and received at connection.

**Collection.**
* Collections = (energy + fixed revenue) × collection efficiency + connection fees.
* The uncollected share is a bad debt in the same quarter, so no receivable is carried. This is a simplification.

**Operating subsidy.** Tariff support = billed kWh × support per kWh, nominal, for the stated years.

**Opex.**
* Fixed opex ÷ 4 × index.
* Per connection cost ÷ 4 × connections × index.
* Insurance = rate × initial capex ÷ 4 × index.
* Diesel fuel = generated × diesel share × fuel cost per kWh × index.

**EBITDA** = revenue + tariff support - opex - bad debt.

## 4. Capex, replacements, maintenance reserve, depreciation

**Initial capex.** Each item is spread evenly over the construction quarters. USD items are converted at each quarter's rate.

**Battery replacement.**
* Occurs every battery life (rounded to quarters) after COD, while the site is operating and within the horizon.
* Cost = battery kWh × USD per kWh × (1 - real decline)^(years) × fx.

**Maintenance reserve.** When enabled (the default), each replacement is funded evenly from the previous replacement (or COD) up to the quarter before it. The reserve is released at the replacement, and CFADS deducts the contributions instead of the lumpy capex.

**Depreciation.** Straight line by vintage:
* initial items from COD over their life;
* replacements from the following quarter over the battery life;
* capitalised interest during construction and upfront fees over the capex weighted asset life.

## 5. Financing

**Sizing.** Each tranche's commitment = share of capex × debt basis. The debt basis is either total capex net of the capital grant (default) or gross capex.

**Draws.** Drawn pro rata to capex spend. USD tranches are tracked in USD and translated at fx_t.

**Interest.** Interest = opening balance × quarterly rate. During construction it is paid by equity and capitalised (no circularity).

**Repayment.** After COD plus grace quarters:
* annuity (level debt service), or straight line;
* over tenor × 4 - grace quarters;
* the final instalment clears the balance.

**FX.** FX loss on USD tranches = opening USD balance × change in rate, charged to P&L.

**Upfront fees.** Paid at financial close by equity and capitalised.

**DSRA.**
* Target = scheduled debt service of the next N quarters (default 2).
* Funded during construction by equity, then adjusted every quarter from cash.
* The target falls to zero when operations end.

**Lock up.** No distribution in a quarter whose DSCR is below the lock up level, except in the final quarter.

**Liquidity.** Unrestricted cash is kept at or above the minimum cash level by equity support. Equity support is reported as the liquidity requirement.

## 6. Subsidies and RBF

| Instrument | Rule |
|---|---|
| Capital grant | Paid on milestone quarters (shares add to 100%). Without milestones, paid at COD. |
| RBF | Payment = new connections × rate, paid after the verification lag, within the programme cap, only while the site operates |
| Deferred grant | Grant and RBF receipts are held as deferred income and released straight line over the remaining weighted asset life from COD |
| Disposal | Any remaining deferred grant is released on disposal |
| Tax | Grant income is not taxable unless `grant_income_taxable` is set |

**Liquidity effect of delays.** A later disbursement raises equity during construction, or equity support after COD. The subsidy delay sensitivity shows the effect.

## 7. Grid arrival

The grid arrives at the start of the stated operating year. Each treatment must cite its country rule (`regulatory_source`); without it the model reports missing inputs.

| Treatment | Effect |
|---|---|
| Interconnect | Tariff and demand multipliers apply from that quarter |
| Asset transfer | Operations stop; compensation = % of net book value; the remaining NBV is written off; debt is prepaid; the deferred grant is released |
| Stranded | As asset transfer, with no compensation |

## 8. Tax

**Levered tax.** Taxable = EBT, less grant income where it is not taxable. Losses are carried forward without limit, and tax is paid in the same quarter.

**EBT** = EBITDA + grant income - depreciation - interest (operations) - FX loss + disposal gain.

**Unlevered tax** (for project cash flows) uses EBITDA - depreciation, excluding capitalised finance costs, with its own loss pool.

## 9. Statements and reconciliations

**Balance sheet**

| Side | Lines |
|---|---|
| Assets | Cash + DSRA + maintenance reserve + net book value |
| Liabilities | Debt (LCY) + deferred grant |
| Equity | Paid in capital (initial equity + equity support) + retained earnings (cumulative net income - distributions) |

Distributions are on a cash basis and are not limited to accumulated profits. That is an analytical simplification.

**Cash flow statement**

| Section | Content |
|---|---|
| CFO | Cash from operations before tax, less tax |
| CFI | Capex, replacements and capitalised finance costs; disposal proceeds; reserve account movements |
| CFF | Debt draws and repayments; interest paid in operations; equity in and out; grant and RBF receipts |

## 10. Metrics

| Metric | Definition |
|---|---|
| Project IRR before subsidy | IRR of the unlevered flows: -capex in construction; collections + fees - opex - unlevered tax - replacements in operations; disposal proceeds |
| Project IRR after subsidy | Same flows plus tariff support, grant and RBF receipts |
| Equity IRR | IRR of -(equity + equity support) + distributions |
| NPV | At the project discount rate, to financial close |
| DSCR | Annual CFADS ÷ annual scheduled debt service (interest + principal, excluding prepayment), for operating years with debt service. CFADS = collections + fees + tariff support - opex - tax - replacements + reserve release - reserve contributions |
| LLCR at COD | PV of CFADS to the last maturity at the commitment weighted debt rate ÷ debt outstanding at COD |
| Payback | Years from COD to the first quarter in which cumulative post subsidy project cash flow is non negative; reported only when it is also non negative at the horizon |
| LCOE per kWh sold | PV(capex + replacements + opex) ÷ PV(billed kWh) |
| Minimum revenue requirement | PV(capex + replacements + opex) ÷ PV of one LCY a year over operations |
| Viability gap | max(0, -NPV before subsidy), in total and per connection |
| Subsidy per connection | Nominal grant + RBF + tariff support ÷ target connections |
| Minimum capital grant | Smallest grant meeting a minimum DSCR and/or equity IRR, by bisection on the full engine. It is checked at the end, and reported infeasible when even the maximum fails |

## 11. Integrity checks and status

**Integrity checks** (each must pass for every quarter):
* sources = uses + cash at COD;
* balance sheet, recomputed from its components;
* cash roll forward;
* debt roll forward per tranche, and repayment by the horizon;
* fixed asset roll forward;
* deferred grant roll forward;
* DSRA = target;
* maintenance reserve never negative and fully used at each replacement;
* no negative unrestricted cash;
* energy balance;
* collections ≤ billing;
* RBF within the cap and within verified connections × rate;
* NPV at the reported IRR = 0.

**Warnings:**
* DSCR below lock up;
* equity support needed;
* unserved energy > 5%;
* a bill above 10% of income (a model policy threshold);
* equity IRR not computable;
* grid arrival without a cited rule;
* illustrative inputs;
* assumptions not reviewed.

**Status:**

| Status | Condition |
|---|---|
| INCOMPLETE INPUTS | Essential inputs are missing |
| FAILED CHECKS | An integrity check failed |
| WARNING | Checks pass, but a warning remains or there is no named review |
| VALIDATED | Checks pass, no warning, and a named person has reviewed the assumptions |

Running without errors never gives VALIDATED.

**Fault injection.** The tests plant faults (balance sheet, cash, debt, fixed assets, deferred grant, DSRA, maintenance reserve, negative cash, energy, collections, RBF, sources and uses), and each one must be caught by its check.

## 12. Sensitivities

Each sensitivity case changes the inputs and reruns the full engine with its checks:
* CAPEX ±10%, ±20% and ±30%;
* demand growth ±2 points;
* uptake (20%);
* tariff ±10%;
* collection (10) points;
* battery replacement cost +30%;
* interest rates +2 points;
* LCY depreciation +5 points;
* subsidy payments 4 quarters later;
* construction 2 quarters longer;
* grid arrival in year 8 (with the configured treatment, else stranded).

The tornado chart sorts the input groups by swing.

## 13. Known simplifications

See `known-limitations.md`.
