# Annex A. PAYGo KPI dictionary

The definitions below are those used in the companion workbook. They follow the logic of the PAYGo PERFORM framework, but a company reporting under PERFORM should align each definition with the current published PERFORM documents, which take precedence.

| KPI | Definition used in the workbook | Level | Comment |
|---|---|---|---|
| Collection rate | Instalments collected ÷ instalments due in the period, excluding deposits | Portfolio and cohort | Deposits are excluded because they are collected with certainty at sale and flatter the ratio |
| Trailing three month collection rate | Collections ÷ instalments due over the last three months | Portfolio | The usual covenant measure; smooths one off months |
| Repayment rate (cumulative) | Cumulative collections ÷ cumulative instalments due, at a given account age | Cohort | The core vintage measure; compare cohorts at the same age |
| Receivables at risk (RaR) | Carrying amount of accounts that have stopped paying ÷ gross receivables | Portfolio | In Proxy mode, the carrying amount of accounts that have stopped paying; in Actual mode, the figure reported by the company in Credit_Input |
| PAR30, PAR90 | Gross receivables of accounts more than 30 (90) days past due ÷ gross receivables | Portfolio | Growth in the denominator flatters the ratio in a young book |
| DPD exposure at 30+, 90+, 180+ (vintage) | Arrears of accounts at or beyond the threshold, including amounts already written off, plus their outstanding balance, ÷ instalments due | Cohort | Cumulative, so that a cohort's history stays visible after its plan ends |
| Write off ratio | Amounts written off in the last twelve months ÷ average gross receivables | Portfolio | Depends heavily on the write off policy; read it with the policy |
| Default | Account 180 days past due (workbook default) | Account | Set on Credit_Assumptions |
| Recovery rate | Net resale proceeds of repossessed units ÷ defaulted exposure | Cohort | Net of recovery cost (15% of gross proceeds by default) |
| LGD proxy | 1 less net recoveries ÷ defaulted exposure | Portfolio | Not an IFRS 9 LGD |
| PD proxy, twelve months | Proxy mode 1 − (1 − h)^12; Actual mode trailing write offs ÷ average gross receivables | Portfolio | Not an IFRS 9 PD |
| Active ratio | Active (paying or within grace) accounts ÷ accounts sold and not yet unlocked | Portfolio | Read with the unlock rate |
| Unlock rate | Accounts fully repaid and unlocked ÷ accounts reaching the end of tenor | Cohort | The basis of ownership based results |
| Ownership at twice the tenor | Share of a cohort that owns its device at twice the original tenor | Cohort | Required for ownership linked RBF in the workbook |
| CAC | Commission plus marketing and acquisition cost per unit sold | Tier | A fully loaded CAC also carries agent management cost (Chapter 5) |
| LTV to CAC | Lifetime contribution before CAC ÷ CAC | Tier | Undiscounted; read with payback and unit IRR |
| Cash payback | Months after sale until cumulative unit cash turns positive | Tier | |
| Payment burden | Monthly instalment ÷ monthly household income of the target segment | Tier | 10% threshold in the workbook is a policy choice, not a rule |

# Annex B. Credit policy template

A credit policy for a PAYGo company should be short enough to be applied by field staff and specific enough to be audited. The outline below lists the sections that lenders and investors expect to see.

1. Scope and governance: products covered, approval authority, credit committee composition, frequency of review, exceptions log.
2. Eligibility: identification, minimum age, location within the service area, mobile money account, prohibited segments.
3. Affordability assessment: income evidence accepted, maximum payment burden by tier, deposit rules, treatment of existing PAYGo or digital loans.
4. Scoring and approval: data used, score cut offs by tier, manual review triggers, agent override rules.
5. Pricing and disclosure: price plans by tier, APR computation and disclosure, fees, early repayment terms.
6. Servicing: payment channels, reminders, grace periods, lockout rules and customer communication before lockout.
7. Collections: contact strategy by DPD bucket, restructuring and payment holidays, conduct standards for collectors, complaints handling.
8. Default, repossession and write off: default definition, repossession criteria, refurbishment and resale, write off triggers and approval.
9. Monitoring: KPIs by cohort, tier and agent, reporting calendar, early warning thresholds and actions.
10. Data and model governance: data retention, reconciliation of the servicing platform to the ledger, validation of scorecards and provisioning models.

# Annex C. Agent economics template

| Line | Unit | Notes |
|---|---|---|
| Units sold per agent per month | Units | By tier and territory |
| Upfront commission per unit | LCY | By tier |
| Deferred commission per unit | LCY | Paid on repayment milestones; clawed back on early default |
| Agent fixed allowance | LCY per month | Airtime, transport |
| Training and onboarding | LCY per new agent | Amortised over expected agent tenure |
| Agent supervision | LCY per month | Area manager cost divided by agents supervised |
| Agent churn | % per month | Drives onboarding cost |
| Fraud and ghost sales losses | % of units | From audit sampling |
| Cohort credit quality by agent | Repayment rate at M6 and M12 | Ranking used for commission tiers and offboarding |
| Fully loaded CAC | LCY per unit | Sum of the above per unit sold |

# Annex D. Investor due diligence checklist

| Workstream | Key requests | Typical red flags |
|---|---|---|
| Commercial | Sales by tier, territory and channel; price plan history; customer survey results | Sales growth driven by price cuts or deposit waivers |
| Credit and data tape | Account level tape with origination date, tier, price plan, payments, DPD, status; cohort curves; write off and repossession history | Tape that does not reconcile to the ledger; missing early cohorts; frequent restructuring |
| Operations and agents | Agent list with productivity and cohort quality; commission plans; fraud audits | Commission paid fully at sale with no clawback |
| Technology and lockout | Platform description, uptime, lockout logic, data security | Manual overrides of lockout without audit trail |
| Finance and accounting | Audited accounts, revenue recognition and ECL policies, management accounts, budget against actual | ECL policy unchanged while collections deteriorate |
| Legal and regulatory | Licences, consumer protection compliance, data protection, tax position, facility documents | Unlicensed lending activity; disputes with tax authorities |
| ESG and consumer protection | Complaints log, pricing disclosure, collection conduct, e-waste and battery take back | Aggressive collections; no complaints mechanism |
| Management and governance | Board composition, key person risk, incentive plans, related party transactions | Finance function too thin for the size of the book |

# Annex E. Investment memo template

1. Recommendation (Go, Conditional Go or Stop) and conditions.
2. Company, market and product range.
3. Unit economics by tier.
4. Portfolio quality and data: actual against proxy, cohort curves.
5. Financial projections and funding requirement.
6. Scenarios and stress tests.
7. Financing structure, borrowing base and covenants.
8. Valuation and returns.
9. Benchmarking and calibration.
10. Consumer protection and impact.
11. Readiness gates and outstanding diligence.
12. Risks and mitigants.

Each section should state the evidence it rests on (company data, model output or external source) and the confidence attached to it.

# Annex F. Receivables facility term sheet checklist

| Term | Points to settle |
|---|---|
| Borrower and structure | Operating company or SPV; security package; true sale or secured loan |
| Facility amount and tenor | Commitment, availability period, amortisation after availability ends |
| Currency and pricing | Local or hard currency; margin, fees, hedging cost |
| Borrowing base | Eligible receivables definition, advance rates by tier, concentration limits by product, region and agent |
| Eligibility criteria | Maximum DPD, minimum payments made, no restructured accounts, contracts compliant with consumer law |
| Cash management | Collection accounts, sweep mechanics, priority of payments |
| Portfolio covenants | Collection rate, RaR, PAR30 and PAR90, write off ratio, with definitions and calculation dates |
| Corporate covenants | Debt to equity, minimum liquidity, DSCR if any, equity cure rights |
| Cure periods and triggers | Cure mechanics; triggers for stop of advances and early amortisation |
| Reporting | Monthly tape and KPI report, audit rights, servicer reports |
| Conditions precedent | Legal opinions, data tape audit, platform review, insurance |
| Events of default | Payment default, covenant breach after cure, change of control, licence loss |

# Annex G. Sources and verification status

The rule applied in the AEF series is that a figure about a real company or about the sector may appear in a final edition only once the primary document has been opened and checked. In this draft, every external figure below rests on secondary reporting; each is quoted in the text with that caveat and must be checked against the original before publication.

| Ref. | Figure as used in the text | Source as reported | Status |
|---|---|---|---|
| E1 | Sector PAYGo collection rate about 62% in 2023; about half of PAYGo customers written off or more than 30 days late | ESMAP and World Bank, Off-Grid Solar Market Trends Report 2024 | Secondary reporting; primary report not yet reviewed |
| E2 | PAYGo PERFORM KPI framework and definitions | CGAP, GOGLA, Lighting Global | Definitions to be aligned with the current published documents |
| E3 | Multi-Tier Framework for household electricity access, Tiers 0 to 5 | ESMAP, Beyond Connections (2015) | Numeric thresholds not quoted; to be checked |
| E4 | M-KOPA FY2024 revenue about USD 416m, net profit about USD 9.2m; FY2023 loss about USD 24.7m. Conflicting report: FY2024 revenue USD 253.5m, FY2023 loss USD 20.6m | TechCabal (October 2025) citing UK filings; a second outlet for the conflicting figures | Conflict unresolved until the filings are read |
| E5 | Sun King cumulative solar loans about USD 1.3bn to almost 10 million cumulative loan customers; Kenyan securitisations of about USD 130m (2023) and about USD 156m (2025) | Company and bank announcements, secondary reporting | Secondary reporting |
| E6 | d.light securitisation purchasing capacity about USD 718m since 2020, including a USD 176m facility in 2024 | Secondary reporting | Purchasing capacity, not debt raised |
| E7 | BBOXX LTD (07177839) in administration from 19 May 2025; latest filed accounts FY2022 | UK public register and gazette, as reported | Primary documents not yet reviewed |
| E8 | Off-grid solar investment about USD 299m in 2024, down about 30% | GOGLA investment data report | Secondary; to check |
| E9 | ZOLA Electric USD 90m round (USD 45m equity, USD 45m debt), September 2021 | Secondary reporting | Secondary reporting |
| E10 | Universal Energy Facility pays per verified connection | SEforALL | Amounts not quoted |

# Annex H. Glossary

| Term | Meaning |
|---|---|
| Advance rate | Share of eligible receivables a lender will fund |
| Borrowing base | Maximum facility drawing allowed by eligible receivables and advance rates |
| Cohort (vintage) | All accounts originated in the same month, for one product tier |
| Collection rate | Collections ÷ instalments due, excluding deposits |
| Cure | Return of a delinquent account to current status |
| Daily rate | Price of one day of service, paid in advance through mobile money |
| Deposit | Upfront payment that activates the device and screens customers |
| DPD | Days past due |
| ECL | Expected credit loss |
| Excess spread | Interest and fee income on securitised assets above the cost of the notes and expenses |
| First loss | Tranche or equity that absorbs losses before any other investor |
| Lockout | Remote disabling of a device when payments stop |
| LGD | Loss given default |
| PAR30 | Portfolio at risk, more than 30 days past due |
| PD | Probability of default |
| RaR | Receivables at risk |
| RBF | Results based financing |
| SICR | Significant increase in credit risk (IFRS 9) |
| SPV | Special purpose vehicle |
| Tenor | Length of the payment plan |
| True sale | Transfer of receivables to an SPV that removes them from the originator's estate in insolvency |
| Unlock | Permanent release of the device once the plan is fully paid |
