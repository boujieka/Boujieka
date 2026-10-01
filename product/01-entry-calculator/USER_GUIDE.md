# Mini-Grid Financial Feasibility Calculator: User Guide

## 1. Quick start
1. Open `Inputs`. Change only the **yellow cells with blue text**.
2. Enter your customer segments: number of customers, kWh per month, tariff and connection fee.
3. Check the auto-sizing for PV, battery and diesel. Type a value in **Override** to use your own design.
4. Enter unit costs, OPEX and financing (grant, RBF per connection, debt terms).
5. Read `Dashboard`. Make sure `Checks` shows **ALL OK**.

## 2. Reading the results
| Output | Meaning |
|---|---|
| Project IRR before subsidies | Return of the project on commercial terms alone |
| Project IRR after subsidies | Return once the grant and RBF are counted |
| NPV @ hurdle | Value created at your discount rate. Negative means the project needs support |
| LCOE | Discounted lifecycle cost per kWh sold. Compare it with the levelized collected revenue per kWh |
| CFADS / DSCR | Cash available to repay the lender. Covenant breached if the minimum DSCR is below the required level |
| **Viability gap** | Upfront subsidy, in present-value terms, that brings the pre-subsidy NPV to zero |
| Remaining funding gap | Viability gap minus the present value of planned grant + RBF |

## 3. Method and simplifications
- Annual time step. Construction in Year 0, operations Years 1–20.
- Solar delivery = MIN(PV available, generation × target solar fraction). Diesel covers the rest. There is no hourly dispatch.
- PV and battery capacity are fixed. Demand growth beyond the design year increases the diesel share.
- Battery replacements happen every *battery life* years. With the maintenance reserve option, the cost is spread into CFADS ahead of each replacement. Project cash flow still records the actual replacement.
- Tax: flat rate on positive profit, no loss carry-forward. Grants and RBF are treated as non-taxable. Check local rules.
- Debt: annuity after interest-only grace years. No fees, DSRA or sculpting.
- IRR can be misleading when cash flows change sign (for example in replacement years). Use NPV and the viability gap as the primary metrics.

## 4. Worked example (illustrative only)
A village of 970 customers with 349 kWp PV, 780 kWh battery and 145 kW diesel. CAPEX is about $1.32m (about $1,363 per connection).
- Without subsidy: NPV of –$863k at 10%. Viability gap of about $889 per connection.
- With a $680k grant and RBF of $250 per connection: NPV is positive and minimum DSCR is 1.60x. Equity IRR is still below the 15% target.

These numbers come from the example inputs. They are not market benchmarks.

## 5. Disclaimer
This is a screening tool for educational and pre-feasibility use. It is not investment, legal, tax or engineering advice.
