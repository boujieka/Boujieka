# About the Templates Pack

The Book 2 Templates Pack, issued as version 0.9 (pre-release), holds eight working documents for the people who build, finance and invest in PAYGo solar companies. They are the documents a deal team actually exchanges during a transaction: the data request, the loan tape, the diligence checklist, the monthly lender report, the borrowing base certificate, the credit policy, the canvas and the investment committee memo. Each one uses the definitions of MODEL 2, the PAYGo Company Financial and Investment Model, and of Book 2, PAYGo Solar Finance, so that a number read in one document means the same thing in all the others.

| No. | Template | Format | Main user | Book |
|---|---|---|---|---|
| T01 | Investment committee memorandum | Word | Investment team | Chapter 15; Annex E |
| T02 | Investor due diligence checklist | Excel | Investment and credit teams | Chapter 15; Annex D |
| T03 | Customer credit policy | Word | Company management; lenders reviewing it | Chapters 2, 6, 7; Annex B |
| T04 | Agent economics and fully loaded CAC | Excel | Company finance team | Chapter 5; Annex C |
| T05 | Lender KPI report | Excel | Company finance team; lenders | Chapters 6, 7, 11; Annex A |
| T06 | Loan tape specification and data request | Excel | Investors, lenders, rating analysts | Chapters 12, 15 |
| T07 | Borrowing base certificate and term sheet checklist | Excel | Company treasury; lenders | Chapter 11; Annex F |
| T08 | PAYGo business model canvas | Word | Founders; investment teams | Chapter 1 |

## Conventions

The Excel templates follow the colour code of the model. Blue figures on a cream background are inputs and are the only cells to change; black figures are formulas. Every sheet prints with the house name, the sheet name and "Page x of y" in the footer. The Word templates open with a contents list that Word refreshes, with page numbers, when the document is opened; if it does not, select the contents and press F9. Text in square brackets is to be replaced, and grey italic paragraphs are guidance to delete before a document is issued.

Example values are illustrative. Where a template needs data to show how it works, it uses CASE 2, the fictional SolaraPay case of Book 2, whose 24 month history is synthetic teaching data. None of the examples describes a real company.

# Using the pack through a transaction

The templates are designed to be used in sequence. A typical equity or debt transaction with a PAYGo company runs through six stages, and each stage has its document.

| Stage | What happens | Templates |
|---|---|---|
| 1. Screening | Understand the business model and decide whether to spend diligence time | T08 canvas |
| 2. Data request | Ask for the account level tape and the monthly portfolio history on day one | T06 data request and tape specification |
| 3. Diligence | Rebuild the KPIs from the tape, test the credit policy, cost the distribution model | T02 checklist, T05 KPI report, T03 credit policy, T04 agent economics |
| 4. Structuring | Size the facility, agree eligibility, advance rates, covenants and conditions | T07 borrowing base and term sheet |
| 5. Decision | Present the recommendation and its conditions to the committee | T01 memo |
| 6. Monitoring | Monthly reporting against covenants and cohort plan | T05 KPI report, T07 certificate |

The order matters. The data request goes out before the commercial work, because the company's own cohort history is the evidence that settles most of the questions in the memo. In the SolaraPay case, the finding that decided the lender's position, an operational collection rate already below the proposed covenant level, came from the history alone.

# The templates one by one

## T01 Investment committee memorandum

A twelve section memo in the order the book recommends: recommendation and conditions first, then the company, unit economics, portfolio quality, projections, stress tests, financing structure, valuation, benchmarks, consumer protection, readiness gates and risks. Each section carries the tables a committee member expects to see, with the model sheet that supplies each figure, and a table of input provenance as counted on the model's Start sheet. The readiness section records the workbook's decision on evidence (23 gates, 13 critical; STOP on a failed test, GO when all 23 are met, CONDITIONAL GO when all 13 critical gates are met, otherwise STOP on incomplete evidence) beside the deal team's recommendation, and asks for the reason when the two differ; a manual gate counts only with the place the evidence is held and who signed it off. Benchmarks are used as tests only when their source is VERIFIED, with grade and status shown separately. The conditions table forces every condition to be written as a condition precedent, a covenant or a structural feature. The risk matrix lists the eight risks that most often decide a PAYGo case. Annex A records the grade and the verification status of every external figure quoted. Where revenue or credit losses are discussed, the memo carries the statement: "This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS."

## T02 Investor due diligence checklist

Fifty items across eight workstreams: commercial, credit and data tape, operations and agents, technology and lockout, finance and accounting, legal and regulatory, ESG and consumer protection, management and governance. Each item names the evidence to request and the red flag to look for, including a collection rate presented as the PERFORM repayment rate and PAYGo PERFORM 2026 KPIs not computed on contract data. Priority and status are chosen from drop down lists, and the Summary sheet counts open items, issues found and high priority items still open by workstream. The case is ready for the committee only when no high priority item remains open and every issue found has been explained.

## T03 Customer credit policy

A policy in ten sections that field staff can apply and an auditor can test: scope and governance, eligibility, affordability, scoring and approval, pricing and disclosure, servicing and lockout, collections, default and write off, monitoring, and data governance. Monitoring sets the operational collection rate beside the PERFORM 2026 repayment rate at 90 days by cohort, and the definitions annex keeps the two apart. Parameters that a credit committee must set (maximum payment burden by tier, minimum deposit, maximum tenor, score bands, collection actions by DPD bucket, default and write off thresholds, early warning levels) are laid out in tables. Every rule must be confirmed against the law of each country of operation with local counsel before the policy is adopted.

## T04 Agent economics and fully loaded CAC

Builds customer acquisition cost for a territory on two definitions. The narrow definition covers upfront commission, expected deferred commission and marketing; the fully loaded definition adds field supervision, recruitment to replace leavers, transport, verification and fraud losses. With the example inputs the fully loaded figure is about one and a half times the narrow one across the tier mix. An agent ranking sheet scores each agent on the cohort repayment ratio at month 6 and the share of deposit only accounts, and a new territory sheet shows how the fixed cost per unit falls as sales ramp up, with stop criteria to set before opening.

## T05 Lender KPI report

A monthly reporting pack in two parts. The PERFORM_2026 sheet carries the five PAYGo PERFORM 2026 KPIs (RR PvP, RR PvFin, RR PvP at 90 days, RR PvP at twice the term and the ownership rate at twice the term) as company reported lines: the company enters the numerators and denominators it has computed on contract data under the GOGLA Technical Guide (June 2026), by tier, and the sheet adds them up as the standard requires, shows "not provided" where they are blank and checks that no numerator exceeds its denominator. The report does not compute them from monthly data. The second part holds operational and lender metrics, each with its definition: the input sheet takes month end DPD buckets, instalments due and collected (deposits excluded), write offs and recoveries for up to 24 months, and the KPI sheet reconciles the buckets to reported gross receivables, then computes the monthly and trailing operational collection rates (not PERFORM KPIs), PAR30 and PAR90, PAR30 lagged by three months, the annualised write off ratio, the recovery rate and the borrowing base. The covenant sheet tests each threshold month by month and classifies the latest month as compliant, watch or breach. The vintage sheet sets the cohort repayment ratio against plan, and the dashboard summarises the latest position with charts, the PERFORM 2026 lines shown apart from the operational metrics. Loaded with the SolaraPay history, the report shows a latest monthly operational collection rate of 66.5%, PAR30 of 17.0% and Tier 2 repayment at month 12 of 69.4% against a plan of 74.5%, the figures used in the case study.

## T06 Loan tape specification and data request

The schema defines 27 fields, from account identifier and price plan to days past due, status, write off, repossession and unlock type. The tape sheet holds up to 1,000 accounts with drop down lists for coded fields, and nine checks computed per account: missing mandatory values, tier and status outside their lists, deposit above cash price, payments above scheduled instalments, origination after the report date, full payment unlocks without full payment, negative days past due and duplicate identifiers. The validation sheet totals the checks, and the tape is ready for use only when every count is zero. The data request sheet lists the thirteen standard requests with owners and dates.

## T07 Borrowing base certificate and term sheet checklist

The certificate takes gross receivables by tier and DPD bucket, applies the eligibility threshold, advance rates by tier and a concentration limit on tiers without history, deducts ineligible accounts and compares the result with the drawn balance. The example reproduces the worked borrowing base of Chapter 11 of the book: a base of 1,611 and headroom of 111 on a drawn balance of 1,500, falling to 32 when 100 of Tier 2 receivables move from 1 to 30 DPD to 31 to 60 DPD. The term sheet checklist records the company's and the lender's positions on the twelve terms to settle, and which of them are conditions precedent.

## T08 PAYGo business model canvas

The nine blocks of the classic canvas, plus four blocks that a PAYGo company needs: the credit engine, the funding stack, impact and consumer protection, and the key metrics. The first page carries guiding questions; the second is filled with the SolaraPay example. Three tests close the document: a cash test, a credit test and a customer test.

# Quality and limitations

Every formula in the five Excel templates has been recalculated in LibreOffice with no error values, and the results have been checked against the figures of the book and the case study; the rebuild for version 0.9 changed no example value. The PERFORM_2026 sheet was tested with sample cohorts (a portfolio result built from summed numerators and denominators, and a numerator above its denominator, which the check flags). The validation checks of the loan tape were tested by injecting faulty rows, each of which was caught. The Word templates have been checked for structure, fields and document properties. A full test in Microsoft Excel and Microsoft Word, including printing, has not yet been done; it is required before the pack leaves pre-release.

The templates support professional judgement; they do not replace it. PERFORM KPIs should follow the GOGLA Technical Guide (June 2026), and the definition of every operational or lender metric should be written out in full before it enters a facility agreement, and every legal or regulatory position must be confirmed with local counsel. Nothing in this pack is investment, legal, tax or accounting advice.
