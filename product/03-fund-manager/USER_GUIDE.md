# Energy Access Fund Manager Model (RBF & Portfolio Edition): User Guide

Files: `EnergyAccess_Fund_Manager_Model_v1.xlsx` (EN) · `Modele_Gestionnaire_Fonds_Acces_Energie_v1_FR.xlsx` (FR)

## 1. What it answers
*Which projects should the fund support, with how much RBF and grant, and what portfolio of connections, impact, leverage and risk does that buy?*

## 2. Workflow
1. **Fund Parameters**
   - Fund size, management and TA costs, over-commitment ratio, concentration limits, additionality tolerance.
   - **Fund profile**: RBF rate per customer type, CAPEX grant share, caps, RBF tranches. There are three generic profiles plus *Custom*.
   - Eligibility criteria (threshold plus an on/off switch), eligible countries, scoring weights (must total 100%), and expected delivery by risk rating.
2. **Pipeline**: one row per applicant, up to 25. CAPEX, viability gap and CO2 can be pasted from the **Developer Edition**.
3. **Eligibility & Scoring**: pass/fail tests, then maximum support, request, metrics, eight scores, weighted score and rank.
4. **Allocation**: funds projects in rank order within the envelope and the per-country limit, and names the binding constraint.
5. **Disbursements**: the grant is paid at commissioning. RBF is paid by tranche as connections are verified, scaled by expected delivery. The sheet also shows the fund's cash position.
6. **MRV Tracker**: verified connections and RBF paid to date, compared with the expected profile. Status is On track, Behind or Off track.
7. **Portfolio Dashboard**: commitments, pipeline, impact, leverage, cost-effectiveness, risk and concentration, verdicts and charts.
8. **Checks**: must show **ALL OK**.

## 3. Key methods
| Item | Method |
|---|---|
| Maximum support | MIN(RBF at profile rates + CAPEX grant, max share of CAPEX – other grants, max per project, max share of envelope) |
| Request | Developer's amount requested if given (capped), otherwise the maximum support |
| Scores | Relative to the best eligible project (cost per connection, leverage, productive-use share, CO2 per $); absolute (readiness, track record, risk); additionality 100/50/0 |
| Allocation | Sequential by rank, with no circular references. Partial funding on: MIN(request, envelope left, country room). Off: all or nothing |
| RBF disbursement in year t | RBF allocated × delivery × [tranche A × share verified (t – lag) + (1 – A) × share verified (t – lag – 1)] |
| Impact and leverage | Pro rata to the share of each request that the fund covers |

## 4. Worked example (illustrative, no real fund)
- Fund of $3.0m. After management and TA, $2.55m is available. With 110% over-commitment, the envelope is **$2.805m**.
- 14 applicants. **8 are eligible**; 6 are rejected for the reason shown (country, renewable share, readiness, CAPEX per connection, size, productive use).
- Eligible requests total $3.25m, so the fund is **1.16x oversubscribed**.
- Project N is partly funded because of the **country limit** (Country B reaches exactly 50%). Project I is partly funded because the **envelope is exhausted**.
- Impact bought: about 8,000 connections, 32,400 people and 50,800 tCO2. Leverage is 1.57x private capital per dollar allocated.
- **The model flags a real issue:** with 110% over-commitment, expected disbursements exceed available funds. Grants are paid in full and only RBF is haircut, so expected under-delivery only covers about **1.02x**. Lower the over-commitment, or raise the RBF share.

## 5. Tested behaviour
- 0 formula errors in EN and FR. EN and FR give identical numbers (3,032 values compared).
- Scenarios tested: partial funding off (a project that does not fit is skipped); another profile; all criteria off (14 eligible); larger fund (every project at its cap).

## 6. Simplifications
- Annual time step. Verification profile is common to all projects. Grants are paid in one go at commissioning.
- No FX, no fund-level returns (it is a grant/RBF fund), no reflows. Scores are a decision aid, not a substitute for the investment committee.

## 7. Disclaimer
Portfolio screening and planning tool. Not investment, legal or tax advice. Example data are fictitious.
