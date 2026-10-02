# Volume 2 (SHS / PAYGo) — competitive benchmark v0.1

**Basis:** web scan of October 2026, using search-result snippets only. None of the tools below has been opened yet. Every "gap" is provisional until the files in `benchmarks/README.md` are uploaded and inspected.

## 1. Existing tools

| Tool | Publisher | Access | What it reportedly does | Provisional gaps (to verify) |
|---|---|---|---|---|
| PAYGO Financial Modeling Tool | Power Africa | Free | 10-year P&L, cash flow and balance sheet; unit economics; up to 5 product lines with different payment plans | Cohort engine? Securitisation / SPV? FX on hard-currency debt? IFRS 9 ECL? PERFORM KPIs? French version? |
| PAYGo PERFORM workbook | Lighting Global / CGAP / GOGLA | Free | Standard KPI definitions and benchmarking | A KPI framework, not a financial model |
| Solar-as-a-Service 10-yr model | SmartHelping (marketplace) | $65 | US-style subscription model | No credit risk, defaults or emerging-market FX |
| Generic solar / BESS templates | eFinancialModels, Eloquens, Etsy, Flevy | $59–260 | Utility-scale PPA / startup projections | No PAYGo receivables at all |

**Finding (provisional):** no paid PAYGo company model was found. The free Power Africa tool is the reference we must clearly beat.

## 2. Differentiators built into our model

| # | Feature | v0.1 | Planned |
|---|---|---|---|
| 1 | Monthly cohort (vintage) matrices: collections, active accounts, balance at risk | ✅ | |
| 2 | Per-unit repayment curves driven by default hazard and partial-payment rate | ✅ | Upload of actual curves from company data (v0.2) |
| 3 | Revenue split: cash price vs. financing income over tenor | ✅ | Effective-interest option (v0.3) |
| 4 | Lifetime ECL at origination and write-offs; loss allowance roll-forward | ✅ | IFRS 9 staging (v1.x) |
| 5 | PERFORM-style KPIs: collection rate, write-off rate, balance at risk | ✅ (approx.) | Full PERFORM KPI set incl. repayment rate (v0.2) |
| 6 | USD hardware costs and USD term loan with LCY depreciation and FX P&L | ✅ | Hedging cost option (v0.2) |
| 7 | Receivables-backed facility (advance rate × eligible receivables) | ✅ | Off-balance-sheet SPV with senior/mezzanine waterfall (v0.3) |
| 8 | Automatic funding gap and peak equity requirement | ✅ | |
| 9 | Unit economics: LTV/CAC, cash payback, unit IRR | ✅ | |
| 10 | Base / Downside / Severe scenarios (default, collection, volume, HW cost, FX) | ✅ | Sensitivity tornado (v0.2) |
| 11 | RBF per unit sold / verified | ❌ | v0.2 (engine RBF module) |
| 12 | Repossession and resale of returned units | ❌ | v0.2 |
| 13 | Affordability check against household income tiers | ❌ | v0.3 |
| 14 | Bilingual (FR) | ❌ | After the six English cores |

## 3. Next action

Upload the Power Africa tool and the PERFORM workbook. Then replace every "provisional" above with verified findings, and adjust the feature list so each claimed differentiator is real.
