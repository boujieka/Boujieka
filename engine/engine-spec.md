# Master Financial Modelling Engine — specification v0.1

The engine is the set of mechanics shared by all six volumes. Every model is built from Python with `tools/aef_engine.py`, so each mechanic is implemented and tested once, then reused.

The engine can save about 30–40% of the work. Each volume still needs its own domain core (see §3).

## 1. Shared modules

| Module | Purpose | Status |
|---|---|---|
| **Timeline** | Monthly period-end dates, year index, opex inflation index, price index | Done (SHS v0.1) |
| **Scenario manager** | Base / Downside / Severe levers; one selector; an `ACTIVE` column referenced by formulas | Done |
| **FX** | Opening rate plus annual depreciation path; USD→LCY conversion of costs; hard-currency debt translation and unrealised FX P&L | Done |
| **Term debt (hard currency)** | Drawdown, grace, straight-line amortisation, interest on opening balance | Done |
| **Asset-backed facility** | Borrowing base = advance rate × eligible assets, capped at the limit; draws and repays automatically | Done |
| **Equity and funding gap** | Scheduled equity plus an automatic top-up to keep minimum cash; peak equity requirement output | Done |
| **Tax** | Corporate tax with unlimited loss carry-forward, paid when due (simplified) | Done |
| **Working capital** | Inventory cover, supplier credit | Done |
| **Capex and depreciation** | Straight-line by vintage | Done |
| **3 statements** | P&L, balance sheet, indirect cash flow, balance check | Done |
| **Annual roll-up** | Flows by `SUMIFS` on year; balances at year end | Done |
| **Checks** | Integrity checks and master check on Cover | Done |
| **Dashboard** | Standard charts | Basic |
| **RBF / grants** | Results-based payments per verified unit, verification lag, P&L treatment (grant income vs. deferred) | **Next** (needed by SHS v0.2, Clean Cooking, Mini-grids) |
| **Carbon revenue** | Methodology selector, crediting, issuance lag, price tiers, host-country share of proceeds | Planned (Vol 3) |
| **Project-finance debt** | Debt sculpting to target DSCR, DSRA, LLCR, cash sweep | Planned (Vol 1, 4) |
| **Off-balance-sheet SPV** | True-sale of receivables to an SPV with a senior/mezzanine waterfall | Planned (SHS v0.3) |
| **Valuation** | Company DCF, equity IRR, exit multiple | Planned |

## 2. Interfaces (naming)

- Row keys are registered in `ModelBook.rows[(sheet, key)]`. Formulas reference them by key, never by hard-coded row number.
- Every module exposes the same standard output keys, e.g. `Financing.tl_bal`, `FS.cash_end`, `FS.netrec`.

## 3. Domain cores (not shared)

| Volume | Domain core |
|---|---|
| 2 SHS | Product price plans, per-unit repayment curves, cohort matrices, receivables roll-forward, ECL |
| 3 Clean cooking | Technology library, fuel economics, usage decay, carbon engine |
| 1 Mini-grids | Site build-out, connections, demand per tier, tariff regulation, grid arrival |
| 4 C&I | Load and diesel baseline, PV/BESS dispatch (simplified), PPA/lease/ESCO structures |
| 5 Fund | Capital calls, deployment, portfolio, NAV, distribution waterfall, carry |
| 6 Utility | Cost of service, revenue requirement, losses, collection, unbundling |

## 4. Known simplifications in v0.1 (to be resolved or documented in manuals)

1. **Revenue recognition (SHS).** The cash price is recognised at sale and the financing mark-up straight-line over the tenor. An effective-interest method under IFRS 15/IFRS 9 is a later option.
2. **ECL.** Lifetime expected loss is recognised at origination from the scenario repayment curve, and missed instalments are written off as they fall due. This is not a full IFRS 9 staging model.
3. **Tax.** Tax is paid in the month it arises. There is no deferred tax and no minimum tax.
4. **Interest on opening balances.** This avoids circularity, at the cost of a small timing approximation.
