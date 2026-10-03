# Annex A. PAYGo KPI dictionary

The dictionary has two parts. Part 1 lists the five PAYGo PERFORM KPIs as defined in the June 2026 technical guide, which is the current industry standard (Annex G, E2). Part 2 lists the operational, lender and model metrics used in this book and in the companion workbook; none of them is a PERFORM KPI under the 2026 standard, and several follow definitions from the July 2021 guide, which is historical.

**Part 1. PAYGo PERFORM KPIs (June 2026)**

| KPI | Formula | Key rules |
|---|---|---|
| RR, paid versus plan (PvP) | Payments applied to due instalments to date ÷ instalments due to date | Excludes deposits, prepayments, penalties, fees and subsidies; includes arrears payments and write offs; cumulative from contract start after any free use period; daily normalised, payments recognised when applied |
| RR, paid versus financed (PvFin) | Payments applied to due instalments to date ÷ total amount financed | As above; state the basis (PvP or PvFin) |
| RR PvP at 90 days | Payments applied to instalments due by day 90 ÷ instalments due by day 90 | Cohort milestone |
| RR PvP at twice the term | Payments applied by 2x the term ÷ instalments due over 1x the term | Standard outcome cut off |
| Ownership rate at twice the term | Contracts fully paid by 2x ÷ contracts that have reached at least 2x | Includes written off contracts; excludes contracts not yet at 2x, even if paid |

Results for cohorts and portfolios are built from contract level numerators and denominators. A collection rate, or days locked or enabled, may not be used as a substitute for the repayment rate.

**Part 2. Operational, lender and model metrics**

| KPI | Definition used in the workbook | Level | Comment |
|---|---|---|---|
| Collection rate (operational) | Instalments collected ÷ instalments due in the period, excluding deposits | Portfolio and cohort | Cash conversion in a period; defined in the 2021 PERFORM guide; not a substitute for the repayment rate |
| Trailing three month collection rate | Collections ÷ instalments due over the last three months | Portfolio | The usual covenant measure; smooths one off months |
| Cohort repayment ratio (model) | Cumulative collections ÷ cumulative instalments due, at a given account age, monthly | Cohort | Follows the logic of RR PvP but is not a PERFORM calculation (monthly, no payment allocation) |
| Receivables at risk (RaR) | Carrying amount of accounts that have stopped paying ÷ gross receivables | Portfolio | 2021 guide: balances more than a stated number of consecutive days unpaid; the model's Proxy mode uses a curve based carrying amount; Actual mode uses the company's figure |
| PAR30, PAR90 | Gross receivables of accounts more than 30 (90) days past due ÷ gross receivables | Portfolio | Growth in the denominator flatters the ratio in a young book |
| DPD exposure at 30+, 90+, 180+ (vintage) | Arrears of accounts at or beyond the threshold, including amounts already written off, plus their outstanding balance, ÷ instalments due | Cohort | Cumulative, so that a cohort's history stays visible after its plan ends |
| Write off ratio | Amounts written off in the last twelve months ÷ average gross receivables | Portfolio | 2021 guide definition; depends heavily on the write off policy |
| Default | Account 180 days past due (workbook default) | Account | Set on Credit_Assumptions |
| Recovery rate | Net resale proceeds of repossessed units ÷ defaulted exposure | Cohort | Net of recovery cost (15% of gross proceeds by default) |
| LGD proxy | 1 less net recoveries ÷ defaulted exposure | Portfolio | Not an IFRS 9 LGD |
| PD proxy, twelve months | Proxy mode 1 − (1 − h)^12; Actual mode trailing write offs ÷ average gross receivables | Portfolio | Not an IFRS 9 PD |
| Active ratio | Accounts that made a payment in the last 30 days ÷ accounts not yet paid off or written off | Portfolio | Read with the enabled rate (Chapter 7) |
| Unlock rate | Accounts fully repaid and unlocked ÷ accounts reaching the end of tenor | Cohort | The basis of ownership based results |
| Ownership at twice the tenor (input) | Company reported ownership rate at 2x, loaded in Vintage_Input | Cohort | Should follow the PERFORM OR @2x definition in Part 1; required for ownership linked RBF in the workbook |
| CAC | Commission plus marketing and acquisition cost per unit sold | Tier | A fully loaded CAC also carries agent management cost (Chapter 5) |
| LTV to CAC | Lifetime contribution before CAC ÷ CAC | Tier | Undiscounted; read with payback and unit IRR |
| Cash payback | Months after sale until cumulative unit cash turns positive | Tier | |
| Payment burden | Monthly instalment ÷ monthly household income of the target segment | Tier | The workbook's 10% threshold is a model policy assumption, not a rule (Chapter 2) |

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

This annex summarises the source register for this edition (the full register, with publisher, date, document, page, section, location and evidence for every claim, is kept with the workbook as the source register file and as the *Source_Register* sheet). The grade describes the source: A primary official, regulatory or audited; B institutional or company disclosure; C reputable secondary reporting; D unverified or informal. The status describes what has been checked for this edition. Only verified claims feed the workbook's diagnostics; every other claim appears in the text with its caveat. Pages are those of the document held; "page to verify" means the page has not been seen.

| Ref. | Claim as used in the text | Source | Grade | Status |
|---|---|---|---|---|
| E1 | Average PAYGo collection rate about 62% for 2021 to 2023 (top quartile 75% to 80%, bottom quartile below 50%); share of companies with write off ratio plus RAR30 of 30% to 50% about half in 2023 against 18% in 2021 | ESMAP and World Bank, Off-Grid Solar Market Trends Report 2024 (prepared with GOGLA and Dalberg, as reported) | B | Pending the primary document: figures from a client extraction of the report, pages and definitions to verify. An earlier wording, "about half of PAYGo customers written off or more than 30 days late", has been withdrawn because the extraction concerns companies, not customers. |
| E2 | The five PAYGo PERFORM KPIs (repayment rate on four bases and ownership rate at twice the contract term); collection rate not to be used as a substitute for the repayment rate | GOGLA, PAYGo PERFORM KPIs Technical Guide, June 2026, pages 8 to 10 and 16 to 18 | B | Verified |
| E2a | Collection rate, receivables at risk and write off ratio as portfolio quality KPIs | CGAP, GOGLA and IFC Lighting Global, PAYGo PERFORM Technical Guide, July 2021, pages 18 to 28 | B | Verified, historical: superseded by E2 |
| E3 | Multi-Tier Framework for household electricity access, Tiers 0 to 5 | ESMAP, Beyond Connections (2015) | B | Pending the primary document; numeric thresholds not quoted |
| E4 | M-KOPA FY2024 group revenue reported as about USD 416m and as USD 253.5m; net profit about USD 9.2m | TechCabal (October 2025) and a second outlet | C | Conflicting sources; not used in the workbook |
| E4 | M-KOPA UK LIMITED (10229661), year to 31 December 2024: revenue GBP 1,712,776 from sales of carbon credits; a research and development subsidiary with no employees | Audited accounts filed at Companies House, filing pages 8 and 16 | A | Verified; not a PAYGo benchmark (different entity and activity) |
| E5 | Sun King cumulative solar loans about USD 1.3bn to almost 10 million cumulative loan customers; Kenyan securitisations of about USD 130m (2023) and USD 156m (2025) | Company and bank announcements | B | Pending the primary documents |
| E6 | d.light securitisation purchasing capacity about USD 718m since 2020, including a USD 176m facility in 2024 | Secondary reporting | C | Pending; purchasing capacity, not debt raised |
| E7 | BBOXX LTD (07177839) recorded in administration from 19 May 2025; latest filed accounts made up to 2022 | The Gazette; Companies House register | A | Pending the primary documents: the date must be the date of appointment in the formal notice |
| E8 | Off-grid solar investment about USD 299m in 2024, down about 30% | GOGLA investment data | B | Pending the primary document |
| E9 | ZOLA Electric USD 90m round (USD 45m equity, USD 45m debt), September 2021 | Secondary reporting | C | Pending; not used |
| E10 | Universal Energy Facility pays per verified connection | SEforALL | B | Pending; amounts not quoted |

# Annex H. Glossary

| Term | Meaning |
|---|---|
| Advance rate | Share of eligible receivables a lender will fund |
| Borrowing base | Maximum facility drawing allowed by eligible receivables and advance rates |
| Cohort (vintage) | All accounts originated in the same month, for one product tier |
| Collection rate | Collections ÷ instalments due in a period, excluding deposits; an operational metric, not a PERFORM KPI |
| Cure | Return of a delinquent account to current status |
| Daily rate | Price of one day of service, paid in advance through mobile money |
| Deposit | Upfront payment that activates the device and screens customers |
| DPD | Days past due |
| ECL | Expected credit loss |
| Excess spread | Interest and fee income on securitised assets above the cost of the notes and expenses |
| First loss | Tranche or equity that absorbs losses before any other investor |
| Lockout | Remote disabling of a device when payments stop |
| LGD | Loss given default |
| Ownership rate @2x | PAYGo PERFORM 2026 KPI: contracts fully paid by twice the contract term ÷ contracts that have reached it |
| PAR30 | Portfolio at risk, more than 30 days past due |
| PD | Probability of default |
| RaR | Receivables at risk |
| Repayment rate (RR) | PAYGo PERFORM 2026 KPI family: payments applied to due instalments ÷ instalments due (PvP) or ÷ amount financed (PvFin), on contract data |
| RBF | Results based financing |
| SICR | Significant increase in credit risk (IFRS 9) |
| SPV | Special purpose vehicle |
| Tenor | Length of the payment plan |
| True sale | Transfer of receivables to an SPV that removes them from the originator's estate in insolvency |
| Unlock | Permanent release of the device once the plan is fully paid |
