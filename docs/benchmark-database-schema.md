# PAYGo Financial Benchmark Database — schema v0.7

**Question it answers:** *How does this PAYGo company compare, financially and operationally, with real companies operating at scale?*

**Single source of truth:** `benchmarks/db/paygo_financial_db.csv`, one row per company × fiscal year × line item.

`python tools/build_shs_model.py` loads it into the workbook:
- **Benchmark_DB**: raw records.
- **Benchmark_Matrix**: company-year × line item, built by formula.
- **Benchmark_KPIs**: derived ratios.
- **Benchmark_Compare**: this model against the graded peers.

To add data, edit the CSV and rebuild. Never type benchmark numbers into the workbook.

## Record fields

| Field | Meaning |
|---|---|
| `id` | Unique record ID (DB001…) |
| `company`, `entity` | Brand and legal entity (e.g. BBOXX LTD, 07177839) |
| `fiscal_year`, `period_end`, `period_months` | Fiscal year label (integer), end date, length in months (12 = full year; 6 = half year, never mixed into annual KPIs) |
| `statement` | `IS` income statement · `BS` balance sheet · `CF` cash flow · `OP` operational · `KPI` reported ratio |
| `item` | Line-item code (taxonomy below) |
| `value`, `currency`, `scale` | Reported value, reporting currency, multiplier (1, 1e3, 1e6, 1e9) |
| `fx_to_usd`, `fx_note` | USD per one unit of reporting currency, and its source. Money items are normalised to USD m. |
| `publisher`, `url`, `date_published` | Where the figure was seen |
| `status` | `PRIMARY filing` · `company release` · `secondary` · `snippet` · `NOT CONFIRMED` · `ESTIMATE` |
| `grade` | A audited/regulatory · B company disclosure · C reliable secondary · D estimate/weak/unconfirmed · E contextual |
| `notes` | Definitions, caveats |

**Rules**
1. Only grades A–C enter the graded peer ranges (min / median / max). D and E are displayed, flagged and excluded.
2. Never derive a "reported" figure. A value calculated from other figures is either computed in Benchmark_KPIs, or recorded with status `derived` and the formula in `notes`.
3. Half-year or quarterly figures are never annualised silently.
4. Every money figure carries its currency and FX basis. If the source gives both local currency and USD, store the source's USD figure and note the local-currency amount.

## Line-item taxonomy

| Statement | Codes |
|---|---|
| IS | `REV` revenue · `COGS` cost of sales · `GP` gross profit · `OPEX` operating expenses · `EBITDA` · `DA` depreciation & amortisation · `FIN_COST` finance costs · `ECL` impairment / expected credit losses · `TAX` · `NI` net income |
| BS | `CASH` · `INV` inventory · `AP` trade payables · `TRADE_REC` trade receivables · `PAYGO_REC_GROSS` / `PAYGO_REC_NET` PAYGo receivables · `CONTRACT_ASSETS` · `PPE` · `DEBT` borrowings · `LEASE` lease liabilities · `EQUITY` |
| CF | `CFO` operating cash flow · `CF_INV` inventory investment · `CF_REC` receivables investment · `CAPEX` · `DEBT_DRAW` · `DEBT_REPAY` · `EQUITY_RAISED` |
| OP | `CUST_ACTIVE` · `CUST_CUM` cumulative customers · `UNITS` units sold · `LOANS_CUM` cumulative financing disbursed (USD m) |
| KPI | `REV_GROWTH` · `REPAY_RATE` · `OWNERSHIP_RATE` · `PAR30` · `COLL_RATE` (reported ratios, stored as fractions) |

## Derived KPIs (Benchmark_KPIs)

| KPI | Formula | Note |
|---|---|---|
| Gross margin | GP / REV | |
| EBITDA margin | EBITDA / REV | |
| Net margin | NI / REV | |
| Revenue growth | REV / REV(prior year) − 1, or reported `REV_GROWTH` | Reported value used when no prior-year revenue is recorded |
| Receivables days | PAYGO_REC_NET (else TRADE_REC) / REV × 365 | PAYGo books make this structurally high |
| Inventory days | INV / COGS × 365 | |
| Payables days | AP / COGS × 365 | |
| Cash conversion cycle | Receivables days + inventory days − payables days | |
| Debt / receivables | DEBT / PAYGO_REC_NET | Receivables-financing intensity |
| Debt / EBITDA | DEBT / EBITDA | Blank when EBITDA ≤ 0 |
| Revenue per active customer (USD) | REV / CUST_ACTIVE | |
| Receivables per active customer (USD) | PAYGO_REC_NET / CUST_ACTIVE | |
| ECL / receivables | ECL / PAYGO_REC_GROSS | |
| Active customer ratio | CUST_ACTIVE / CUST_CUM | Diagnostic only |
| Customer ownership rate, repayment rate | Reported KPI | |
| CAC payback | Not disclosed by companies | Model only (Unit_Economics) |

## The model in the comparison

"This model" rows are computed live from the active scenario for Years 1–5:
- flows are converted at the year's average FX, balances at year-end FX;
- each row is labelled "Model (illustrative)" and is never mixed into peer ranges.
