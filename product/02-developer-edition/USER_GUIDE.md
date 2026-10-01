# Energy Access Project Financial Model (Developer Edition): User Guide

## 1. What it answers
*Can this energy-access project be made bankable, and what combination of grant, RBF, concessional debt, senior debt and equity does it need?*

## 2. Workflow (about 30 minutes for a first pass)
1. **Inputs**
   - Project data, then pick the active scenario (Base, Conservative, Optimistic or Custom).
   - Customer segments with tariff, connection fee, **RBF per connection** and **monthly income**.
   - Technical data, CAPEX, OPEX (including MRV costs), and the funding structure (grant, senior debt, concessional debt, DSRA).
2. **Load Profile**: the hourly shape of each segment. It sets the night-time share (battery size) and the peak ratio (generator size).
3. **Productive Use**: the appliance inventory. With `UsePUE = 1`, it sets the consumption of productive users.
4. **Dashboard**: the KPIs, the verdict (YES/NO) and affordability by segment.
5. **Funding Gap & RBF**: how big the gap is, which grant or RBF closes it, and how much debt the project can carry.
6. **Sensitivity**: a live tornado at ±20% (adjustable).
7. **Impact & MRV**: annual indicators and cost-effectiveness ratios.
8. **Financing Request**: auto-written paragraphs and sources & uses, ready for a concept note.
9. **Checks**: must show **ALL OK**.

## 3. Key methods
| Output | Method |
|---|---|
| Viability gap | MAX(0, –NPV of pre-subsidy project cash flow at the hurdle rate) |
| Grant needed | Viability gap – PV(planned RBF) |
| RBF needed for NPV = 0 | (Viability gap – grant) / PV(verified connections, with lag) |
| RBF needed for the equity target | –(equity NPV at target – PV(RBF) at target) / PV(connections) at target |
| Maximum senior debt | MIN over years of (CFADS / min DSCR – concessional debt service) / senior debt service per $1 |
| Tornado | Hidden copies of the engine (`S_*` sheets), one per variable and direction |

The RBF results are **exact**: cash flows are linear in RBF. This was tested by entering the computed RBF; project NPV came out at 0 and equity IRR at exactly 15.0%. The maximum senior debt uses the current CFADS, so interest-driven tax effects are approximated.

## 4. Reading the worked example (illustrative values)
- 970 customers. CAPEX is $1.15m. The viability gap is $793k (about $818 per connection).
- A $600k grant plus RBF of about $260 per connection closes the project-level gap: NPV after subsidies is +$25k.
- Debt covenant is met (minimum DSCR 1.37x). The binding year is when the RBF has stopped and both loans are amortising.
- **Equity IRR is 10.7%, below the 15% target.** The model computes that a uniform RBF of about **$334 per connection** would meet it.
- The tornado shows that **+20% demand reduces NPV**. The system is sized for base demand, so extra kWh come from diesel, which costs more than the tariff collected. Size for expected growth, or plan an expansion.

## 5. Simplifications
- Annual time step. No hourly dispatch.
- Sizing uses base inputs.
- Flat tax rate with unlimited loss carry-forward. Grants and RBF are not taxed.
- Annuity debt with no fees or sculpting. No FX, VAT, working capital or balance sheet.

If you need those features, use a full project-finance model alongside this one. This model focuses on **subsidy sizing, affordability and impact**.

## 6. Disclaimer
Screening and pre-feasibility tool. Not investment, legal, tax or engineering advice. Example values are not benchmarks.
