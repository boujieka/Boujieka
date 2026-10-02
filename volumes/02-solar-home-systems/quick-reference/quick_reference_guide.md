# How to use this guide

This guide condenses Volume 2 into reference cards for the desk: the formulas, definitions, defaults, thresholds and checklists that a PAYGo analyst, lender or investor needs within reach. Each card stands alone. The reasoning behind every rule is in the book; the calculations are in the model and the tools.

| Product | Use it for | File |
|---|---|---|
| Book | The reasoning: why each number matters and how to read it | AEF_Volume2_SHS_PAYGo_Book_Draft_v0.1.pdf |
| Model | The integrated five year plan, credit engine, covenants, valuation, readiness gates | AEF_SHS_PAYGo_Model_v0.7.xlsx |
| User manual | Twelve step workflow through the model; methodology reference | AEF_SHS_PAYGo_User_Manual_v0.7.pdf |
| Case study | SolaraPay Ltd: an end to end investment decision on synthetic data | SolaraPay_Case_Study_v0.7.pdf and case workbook |
| Templates | Memo, diligence checklist, credit policy, agent economics, lender report, loan tape, borrowing base, canvas | templates/AEF_V2_T01 to T08 |
| Decision tools | Price plan and APR, unit economics, calibration, financing, screening, returns | decision-tools/AEF_V2_D1 to D6 |

All example figures refer either to the book's illustrations or to the fictional SolaraPay case, and are flagged as such. Default model inputs describe a fictional market. Negative figures are shown in parentheses.

# The PAYGo business on one page

A PAYGo solar company is three businesses in one legal entity: a retailer that books hardware margin at sale, a service provider that keeps the device working for two to four years, and a consumer lender that waits for the cash. Its income statement can show a profit while it runs out of cash, so it must be read through cohorts and the receivables book, not through the sales line.

| Read first | Why | Where |
|---|---|---|
| Cohort repayment against plan at the same age | Earliest honest signal of credit quality | Vintage_Dashboard; T05 Vintage |
| Collection rate, trailing 3 months, deposits excluded | The usual covenant measure | Credit_Portfolio; T05 |
| PAR30, reported and lagged 3 months | Growth flatters the reported figure | T05 KPIs |
| Peak equity requirement in USD | The real funding need of the plan | Investment_Summary; D4 |
| Investor IRR and multiple in USD, Base and Downside | The return after currency | Valuation; D6 |

## How PAYGo companies fail

| Failure mode | What it looks like first | Test |
|---|---|---|
| Growth outruns funding | Funding need rises faster than profit; facility delayed or in breach | Peak equity; months of runway; facility start date |
| Credit drift | Each new cohort a little below the last; portfolio ratios stable for a year | Cohort curves at M3, M6, M12 against plan |
| Currency | Hardware and debt in USD, collections in local currency | FX pass through; dollar debt share; depreciation sensitivity |

None of the three shows first on the income statement. All three show first in the cohort curves, the funding plan and the FX bridge.

# Core formulas

| Quantity | Formula | Notes |
|---|---|---|
| Monthly instalment | Daily rate × 365 ÷ 12 | |
| Total contract value | Deposit + instalment × tenor | |
| PAYGo premium | Total contract value less cash price | Financing income, straight line over the tenor in the model |
| Amount financed | Cash price less deposit | |
| Implied monthly rate r | Solves amount financed = instalment × [1 − (1 + r)^(−T)] ÷ r | Spreadsheet: RATE(T, −instalment, amount financed) |
| Nominal APR | 12 × r | State the convention used in any disclosure |
| Effective annual rate | (1 + r)^12 − 1 | |
| Flat rate | Premium ÷ amount financed ÷ (T ÷ 12) | Understates the true cost |
| Payment burden | Instalment ÷ monthly household income | Test on lean month income |
| Survival to age a | S(a) = (1 − h)^a, with h the monthly default hazard | Constant hazard |
| Collection at age a | Instalment × c × S(a), with c the collection rate on paying accounts | |
| Expected share of instalments collected over the tenor | c × q × (1 − q^T) ÷ (h × T), with q = 1 − h | |
| Cumulative repayment at age m | c × q × (1 − q^m) ÷ (h × m), for m within the tenor | Vintage measure |
| Receivable at risk (proxy) | (1 − S(a)) × (T − a) × (instalment − premium ÷ T) | Carrying amount of accounts that stopped paying |
| Net recovery | Defaults at age (a − lag) × repossession rate × resale share × cash price × (1 − recovery cost) | |
| ECL at origination (model) | Lifetime expected missed instalments | Consumed as instalments are missed |
| Borrowing base | Σ advance rate × eligible receivables, less concentration excess | Eligible: lower DPD bound at or below the maximum |
| Facility drawn (model) | max(0, min(limit, borrowing base, previous balance + minimum cash − cash before facility)) | Cash sweep; no circularity |
| FX loss on USD debt | Opening USD balance × change in exchange rate | Through the income statement |
| Break even depreciation | (1 + local currency rate) ÷ (1 + dollar rate) − 1 | Above it, dollar debt costs more |
| Terminal value (normalised) | [(EBITDA − tax − capex) × (1 + g) − g × NWC] ÷ (r − g), Year 5 values | Avoids capitalising a growth year |
| Investor stake | Ticket ÷ (pre money valuation + ticket) | |
| Investor IRR, single exit, no follow on | (stake × exit equity in USD ÷ ticket)^(1 ÷ n) − 1 | Exit equity floored at zero |
| Maximum pre money for a target IRR | Exit equity in USD ÷ (1 + target)^n − ticket | No follow on equity |

# Portfolio KPIs

| KPI | Definition | Common error |
|---|---|---|
| Collection rate | Instalments collected ÷ instalments due, both excluding deposits | Deposits in the numerator |
| Trailing 3 month collection rate | Collections ÷ instalments due over 3 months | Covenant tested on a single month |
| PAR30, PAR90 | Balance of accounts more than 30 (90) DPD ÷ gross receivables | Arrears instead of whole balances |
| PAR30 lagged 3 months | Balance more than 30 DPD ÷ gross receivables 3 months earlier | Not reported in fast growing books |
| Receivables at risk | Company definition, aligned with current PAYGo PERFORM documents | Definition not printed beside the figure |
| Write off ratio | Write offs (12 months) ÷ average gross receivables | Read without the write off policy |
| Recovery rate | Recoveries net of costs ÷ write offs | Assumed rather than observed |
| Repayment rate (cohort) | Cumulative collections ÷ cumulative instalments due at a given age | Comparing cohorts at different ages |
| Ownership rate | Share of a cohort owning its device at twice the tenor | Claimed without unlock evidence |
| Active ratio | Accounts paying in the last 30 days ÷ accounts not paid off or written off | |
| Enabled rate | Share of active accounts with credit at period end | Called "unlock rate" in operations; not the permanent unlock |
| DPD | Schedule shortfall in days of the daily rate | Days without credit used without disclosure |

Every DPD distribution must add up to gross receivables. A report that does not reconcile is not used.

# Numbers worth remembering

These are results from the book's illustrations and the default model, not sector standards. They show the size of the effects.

| Effect | Illustration | Source |
|---|---|---|
| Survival on a 2.6% monthly hazard | 72.9% still paying at month 12; 53.1% at month 24 | Chapter 6 |
| Tenor and collection | 69.2% of instalments collected over 18 months against 64.4% over 24 months (hazard 2.6%, collection 88%) | Chapter 4 |
| Growth and the collection rate | Same customers: 64.4% at zero growth, 68.3% at 5% a month, 71.6% at 10% a month | Chapter 6; D3 |
| Growth and PAR30 | New lending of LCY 400m on an LCY 800m book with 20% PAR30 shows 14.3% reported, 21.5% lagged | Chapter 7 |
| Margin against cash | A Tier 2 sale booking LCY 14,000 of contribution at sale is LCY (22,000) in cash and pays back in month 14 | Chapter 1; D2 |
| Loss rate and value | Ten points more expected loss cut unit contribution by 41% and unit IRR from about 49% to about 28% | Chapter 9 |
| Fully loaded CAC | About 1.86 times the narrow CAC in the Chapter 5 territory example | Chapter 5; T04 |
| Borrowing base headroom | A 3.4% migration from 1 to 30 to 31 to 60 DPD removed 71% of headroom | Chapter 11; T07 |
| Currency | 20% a year depreciation turns a 46.4% Base IRR into (16.0%); no price increase on new contracts gives 7.9% | Default sensitivities |
| Volume | 20% lower volume lowers the Base IRR from 46.4% to 37.8%, with no covenant breach | Default sensitivities |

# Model defaults and scenarios

## Product tiers (fictional market, LCY, opening rate 130 per USD)

| Tier | Product | Tenor | Monthly hazard | Collection on paying accounts | Repossession rate | Advance rate |
|---|---|---|---|---|---|---|
| 1 | Pico solar kit, 10 Wp | 12 | 3.5% | 88% | 0% | 50% |
| 2 | SHS with TV, 80 Wp | 24 | 2.6% | 88% | 20% | 70% |
| 3 | Large SHS with DC fridge, 300 Wp | 30 | 1.9% | 90% | 40% | 70% |
| 4 | Inverter with lithium, about 1.2 kWp | 36 | 1.3% | 92% | 60% | 75% |
| 5 | Inverter with lithium, about 3 kWp | 48 | 1.0% | 93% | 70% | 75% |

## Scenario levers

| Lever | Base | Downside | Severe |
|---|---|---|---|
| Default hazard multiplier | 1.00 | 1.30 | 1.75 |
| Collection rate multiplier | 1.00 | 0.97 | 0.92 |
| Volume multiplier | 1.00 | 0.90 | 0.75 |
| Hardware cost multiplier | 1.00 | 1.05 | 1.10 |
| Local currency depreciation per year | 5% | 12% | 25% |

## Default results (fictional company, USD 4.0m ticket)

| Case | Peak equity (USD m) | Y5 EBITDA margin | Investor IRR | Multiple | Breach months |
|---|---|---|---|---|---|
| Base | 10.0 | 21.6% | 46.4% | 6.7x | 0 |
| Downside | 10.0 | 7.3% | (22.9%) | 0.3x | 44 |
| Severe | 46.6 | (18.4%) | Total loss | 0.0x | 48 |

Credit definitions: default at 180 DPD; Stage 2 from 30 DPD and Stage 3 from 90 DPD for the indicative ECL; borrowing base eligibility to 30 DPD; recovery cost 15% of resale proceeds; cure rate 30% (indicative ECL only); ECL discount rate 20%. Other defaults: inflation 6%, price increase on new contracts 5% a year, FX pass through 50%, tax 30% with unlimited loss carry forward, payment burden threshold 10%.

# Covenants and facility terms

## Default covenants in the model

| Covenant | Threshold | Design note |
|---|---|---|
| Trailing 3 month collection rate | At least 70% | Set from the company's own history, with a cure period |
| Receivables at risk | At most 15% | Definition aligned with current PERFORM documents |
| 30+ DPD | At most 25% | |
| 90+ DPD | At most 18% | |
| Borrowing base headroom | At least zero | Tested monthly |
| Debt to book equity | At most 3.0x | Book equity depends on ECL methodology |
| Annual DSCR | At least 1.20x | Ill suited to a growing book; prefer portfolio covenants |

## Rules for setting them

1. A covenant breached on the day it is signed is a waiver waiting to be requested. Set the level the book can meet on its own history and step it up as performance improves.
2. Equity cures make sense for leverage covenants, not for collection or PAR covenants: new equity does not change how customers pay.
3. Eligibility beyond 30 DPD adds little in a healthy book and puts advances against the receivables most likely to default.
4. Cap unproven products in the borrowing base until twelve months of cohort data sit within an agreed tolerance of plan.
5. Prefer local currency debt for the receivables book; size dollar debt against the depreciation the company can absorb.
6. Ask for a monthly borrowing base certificate by tier and DPD bucket, and a vintage block in every report.

## Terms to settle in a facility term sheet

Borrower and structure; amount and tenor; currency and pricing; borrowing base; eligibility criteria; cash management and sweep; portfolio covenants; corporate covenants; cure periods and triggers; reporting; conditions precedent; events of default (Template T07).

# Diligence essentials

## Data request: the first ten items

1. Account level loan tape since launch (Template T06 structure).
2. Monthly portfolio data by tier for at least 24 months: buckets, due, collected, write offs, recoveries.
3. Cohort observations by tier at fixed ages.
4. Reconciliation of DPD buckets and gross receivables to the ledger at each month end.
5. Credit, write off, restructuring and repossession policies with version dates.
6. Price plan history by tier, including promotions.
7. Agent register, commissions, clawbacks and sales by agent.
8. Unlock logs separated between full payment and other unlocks.
9. Audited and monthly management accounts and budget.
10. Financing agreements, compliance certificates and waivers.

## Red flags

| Red flag | Why it matters |
|---|---|
| DPD buckets that do not reconcile to gross receivables or the ledger | Every ratio built on them is unreliable |
| Collection rate including deposits | Rises with sales, not with repayment |
| Restructurings that reset DPD, clustered before reporting dates | Re-ageing hides arrears |
| Unlocks without matching payment | Weak platform control; ownership overstated |
| Loss allowance flat while PAR30 rises | Profit overstated |
| Write off policy changed during the history | Ratios not comparable over time |
| Recovery assumptions above observed resale proceeds | LGD understated; SolaraPay observed about 99% |
| Sales concentrated in agents or regions with weak cohorts | Origination quality problem |
| Commission paid fully at activation, no clawback | Incentive to sign marginal customers |
| Case that clears the hurdle only with RBF, untested tiers or a high exit multiple | Return rests on assumptions outside the company's control |
| Cohort data not produced within two weeks | The company is unlikely to be managing to it |

# Decision map

| Question | Book | Model | Template | Tool |
|---|---|---|---|---|
| What business am I in? | 1 | Dashboard, Unit_Economics | T08 canvas | D2 |
| Can the customer pay? | 2 | Consumer_Risk | T03 credit policy | D1 |
| What could stop me operating? | 3 | Inputs, Scenarios | T02 checklist | |
| Which price plan? | 4 | Products | | D1 |
| What does a customer cost? | 5 | Products, Unit_Economics | T04 agent economics | D2 |
| How will customers pay? | 6 | Curves, Vintage_Dashboard | T05 Vintage | D3 |
| Is the portfolio healthy? | 7 | Credit_Portfolio | T05 lender report | |
| What profit am I making? | 8 | FS, Credit_Engine | | |
| Does each sale create value? | 9 | Unit_Economics | | D2 |
| Why do we run out of cash? | 10 | FS, Financing | | D4 |
| How should growth be financed? | 11 | Financing, Covenants | T07 borrowing base | D4 |
| Is a securitisation feasible? | 12 | Inputs (structure 2) | T07 term sheet | |
| How should subsidies be used? | 13 | RBF_Engine | | |
| What can kill the company? | 14 | Scenarios, Sensitivity | | D4, D6 |
| Would I invest or lend? | 15 | Valuation, Investment_Readiness | T01 memo, T02 checklist | D5, D6 |

# The model in twelve steps

| Step | Sheets | Key action | Check before moving on |
|---|---|---|---|
| 1 Start | Cover, Contents, Checks | Save a copy; set currency and first month | Master check OK |
| 2 Business | Products, Consumer_Risk | Catalogue, segments, surveyed incomes | Tier labels match capacity |
| 3 Market | Inputs, Scenarios | FX, inflation, price increase, pass through | Depreciation not set to zero |
| 4 Demand | Inputs, Products | Units by year; mix | Mix totals 100% |
| 5 Revenue | Products, RBF_Engine | Price plans; RBF design | Daily rate not entered as monthly |
| 6 Hardware and capex | Products, Inputs | FOB cost in USD, duty, installation | No double count of FX |
| 7 Operating costs | Products, Inputs | Commission, marketing, servicing, central costs | Central costs sized for the volume |
| 8 Financing | Inputs, Credit_Assumptions | Equity, term loan, facility, eligibility | Borrowing base, not limit, binds |
| 9 Statements | FS, Annual | Read balance, revenue mix, credit losses, cash | Balance check zero every month |
| 10 Scenarios | Scenarios, Sensitivity | Base, Downside, Severe | Selector back to Base before saving |
| 11 Bankability | Credit_Portfolio, Covenants, Credit_Input, Vintage_Input | Load actual history; recalibrate | DPD buckets reconcile |
| 12 Memo | Valuation, Unit_Economics, Benchmark_Compare, Investment_Readiness | Valuation, benchmarks, readiness | Never "investment grade" |

# Investment memo and readiness

## Memo structure (Template T01)

1. Recommendation and conditions.
2. Company, market and products.
3. Unit economics by tier.
4. Portfolio quality and data.
5. Projections and funding requirement.
6. Scenarios and stress tests.
7. Financing structure, borrowing base and covenants.
8. Valuation and returns.
9. Benchmarking and calibration.
10. Consumer protection and impact.
11. Readiness gates and outstanding diligence.
12. Risks and mitigants.

## Writing conditions

| Type | Use for | Example |
|---|---|---|
| Condition precedent | What must be true before money moves | Reconciled data tape; board approved pricing policy |
| Covenant | What must stay true | Trailing collection rate with cure period |
| Structural feature | How risk is shared | Tranches tied to cohort performance; valuation ratchet; tier caps |
| Post closing undertaking | What must be built | Ownership tracking; independent ECL review |

## Readiness gates

The model's Investment_Readiness sheet holds 23 gates. Automatic gates test integrity, covenant compliance, unit contribution, actual credit data, consumer protection evidence, outcome linked RBF support and data reconciliation. Manual gates record management sign off, term sheets, legal review, the Excel test and auditor review of ECL. The banner never claims investment grade; at most it reads "ready for independent validation". Default inputs meet 3 gates; the SolaraPay case meets 5.

# SolaraPay at a glance

| Item | Value |
|---|---|
| Company | SolaraPay Ltd, Republic of Kivara (fictional); currency KVS, 135 per USD at entry |
| Ask | USD 4.0m equity at USD 8.0m pre money (33.3% stake); KVS 4.5bn receivables facility at 16% |
| History (synthetic) | Collection rate 77.4% in year 1, 69.3% in year 2; latest month 66.5%; PAR30 17.0%; LGD proxy about 99% |
| Cohorts at M12 | Tier 1 64.6% against 70.3%; Tier 2 69.4% against 74.5%; Tier 3 76.3% against 79.6% |
| Recalibration | Hazards × 1.30 for Tiers 1 to 3; collection rates down 1 to 2 points |
| Calibrated Base | Revenue USD 8.1m to 51.2m; EBITDA margin 16.4% in Year 5; EBITDA positive from month 29 |
| Returns | IRR 29.0%, multiple 3.6x (management plan 33.1%, 4.2x); Downside total loss |
| Mitigants | Full FX price indexation lifts the Downside to 23.6%; entry at USD 6m pre money lifts the Base to 33.8% |
| Lender view | Lowest projected trailing collection rate 70.0% against a 70% covenant; proposed 65% with cure period |
| Recommendation | Conditional Go with seven conditions; 5 of 23 readiness gates |

# Glossary

| Term | Meaning |
|---|---|
| Advance rate | Share of eligible receivables a lender funds |
| Borrowing base | Maximum facility drawing allowed by eligible receivables and advance rates |
| CAC | Customer acquisition cost; narrow (commission and marketing) or fully loaded (with field organisation) |
| Cohort or vintage | Accounts originated in the same month, for one tier |
| Cure | Return of a delinquent account to current status |
| Daily rate | Price of one day of service, prepaid by mobile money |
| Deposit | Upfront payment that activates the device and screens the customer |
| DPD | Days past due, as schedule shortfall |
| ECL | Expected credit loss |
| First loss | Tranche or equity that absorbs losses before any other investor |
| Hazard | Monthly share of paying accounts that stop paying for good |
| LGD, PD | Loss given default; probability of default (indicative proxies in the model) |
| Lockout | Remote disabling of a device when credit runs out |
| LTV to CAC | Lifetime contribution before CAC ÷ CAC; undiscounted |
| PAR30 | Portfolio more than 30 days past due |
| RBF | Results based financing |
| SICR | Significant increase in credit risk (IFRS 9) |
| True sale | Transfer of receivables to an SPV that removes them from the originator's estate in insolvency |
| Unlock | Permanent release of the device when the plan is fully paid |

## Status of external figures

Sector and company figures quoted in Volume 2 rest on secondary reporting and are listed with their status in Annex G of the book. None has yet been checked against its primary document; the M-KOPA FY2024 figures conflict between sources and are provisional. Check the original before quoting any of them. Nothing in this guide is investment, legal, tax or accounting advice.
