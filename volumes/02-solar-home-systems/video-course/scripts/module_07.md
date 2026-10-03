# Module 7. Portfolio KPIs and PAYGo PERFORM

Duration: about 9 minutes. Book: Chapter 7. Model sheets: PERFORM_2026, Credit_Portfolio, KPIs, Covenants, Vintage_Dashboard, Credit_Input, Vintage_Input, Checks. Templates and tools: T05 Lender KPI report, T06 Loan tape and data request.

## Learning objectives
1. Define the five PAYGo PERFORM 2026 KPIs and the operational and lender metrics (collection rate, receivables at risk, PAR30 and PAR90, write offs), and state what sits in each denominator.
2. Explain how growth distorts portfolio ratios, and use lagged and vintage measures to correct for it.
3. Design a monthly lender dashboard that reconciles DPD buckets to gross receivables and reports covenant headroom.

## Scene 1. Is the portfolio healthy
On screen: Title "Is my portfolio healthy?" with three words: definition, denominator, growth.

A board, an investor and a lender all take the same decision every month: whether the portfolio is healthy. The answer depends less on which ratios are reported than on how they are defined, what sits in the denominator and how fast the book is growing.

A portfolio can show improving ratios while its customers behave worse.

## Scene 2. Why a common framework matters
On screen: PAYGo PERFORM 2026: five KPIs on repayment and ownership, from company contract data. The 2021 guide is historical.

Before common frameworks took hold, PAYGo companies, PAYGo meaning pay as you go, often defined their own metrics. A collection rate might include deposits or not. Default might mean 60, 90 or 180 days without payment.

PAYGo PERFORM is the industry's answer. Its first technical guide, published in July 2021 by CGAP, GOGLA and IFC Lighting Global, set out portfolio indicators such as the collection rate, receivables at risk and the write off ratio. That guide is now historical. The current standard is the PAYGo PERFORM KPIs technical guide published by GOGLA in June 2026. It narrows the standard to repayment and ownership, with five key performance indicators, or KPIs. They are the repayment rate paid versus plan, the repayment rate paid versus financed, paid versus plan at 90 days, paid versus plan at twice the contract term, and the ownership rate at twice the contract term.

These KPIs are calculated on contract data, day by day, and they exclude deposits and subsidies. They come only from the company's own data. The workbook is a planning model with monthly cohorts, so it does not compute them. Its PERFORM_2026 sheet holds them as the company reports them, adds up numerators and denominators as the standard requires, and shows the model's approximations beside them, labelled as such. The older ratios remain useful as operational and lender metrics, each with its definition printed beside it, but never in place of a repayment rate.

## Scene 3. Collection rate and receivables at risk
On screen: Collection rate example: 74 collected against 100 due gives 74.0 per cent. Adding deposits of 12 gives a misleading 86.0 per cent.

The operational collection rate, which is not a PERFORM KPI, is cash collected against scheduled instalments, divided by the instalments that fell due in the period. Deposits are excluded from both sides. Take a month in which instalments due are one hundred million local currency units, collections seventy four million and deposits twelve million. The collection rate is 74.0 per cent. Adding deposits to the top line alone would show 86.0 per cent, a figure that rises whenever the company simply sells more.

Receivables at risk measures the share of the book sitting on accounts that have stopped paying or are seriously late. The workbook computes it from the unit curve, as the carrying amount of accounts that have left the paying pool, divided by gross receivables. Operational definitions usually apply a lateness threshold, commonly 30 days, to the full outstanding balance of the account. The workbook's default covenant caps receivables at risk at 15 per cent.

PAR30 and PAR90, portfolio at risk over 30 and over 90 days, are the outstanding balance of accounts more than 30 or 90 days past due, divided by gross receivables. The whole balance of a late account counts, not only the arrears.

## Scene 4. Write offs, repayment and ownership
On screen: Write off ratio, cohort repayment ratio, ownership rate at twice the term from company data, active ratio, enabled rate.

The write off ratio is the amount written off divided by average gross receivables, annualised. A company that writes off at 180 days past due shows lower write offs, and higher PAR90, than one that writes off at 90 days with the same customers.

The workbook's Vintage_Dashboard reports a cohort repayment ratio: cumulative collections over cumulative instalments due, at a given account age. It follows the logic of the PERFORM repayment rate paid versus plan, but it is not a PERFORM calculation, because it is monthly and does not allocate payments to instalments. The ownership rate is the share of contracts fully paid by twice the contract term, so a 24 month contract is measured at month 48. Most companies cannot yet evidence it. The workbook accepts it only from company data and will not derive it from its own curves.

The active ratio and the enabled rate complete the set. Neither has one accepted definition, so print the definition beside the figure.

## Scene 5. Growth flatters the ratios
On screen: PAR30 falls from 20.0 to 14.3 per cent after new sales, while lagged PAR30 reads 21.5 per cent.

Portfolio metrics tell a lender how much of today's collateral is performing. Vintage metrics, by cohort and account age, tell an analyst whether recent customers behave better or worse than earlier ones.

Portfolio metrics are distorted by growth. Take an illustrative seasoned book of eight hundred million local currency units, with PAR30 of 20 per cent, so one hundred and sixty million at risk. Next quarter the company adds four hundred million of new receivables, of which 3 per cent, twelve million, is already more than 30 days late. Hold the old book constant. Reported PAR30 falls to 14.3 per cent. No customer behaved better. The denominator grew faster than arrears can form.

A lagged ratio corrects much of this. Divide today's late balance by gross receivables three months earlier gives 21.5 per cent, close to the seasoned book's true condition. The same effect runs in reverse as growth slows. In the workbook's Base case the collection rate falls from 84.5 per cent in Year 1 to 73.3 per cent in Year 5, with no change in assumptions. Covenants set on a fast growing borrower's Year 1 ratios are set on the most flattering numbers it will ever produce.

## Scene 6. A monthly dashboard for lenders
On screen: Dashboard blocks: book, performance, risk, losses, vintage, facility, covenants, integrity. Sheets: Credit_Portfolio, KPIs, Covenants, Vintage_Dashboard, Checks.

A lender report should let the reader judge four things without asking for more data: whether the collateral performs, whether newer cohorts are better or worse, the covenant headroom, and whether the numbers reconcile.

The pack fits on two pages. It shows the PERFORM 2026 KPIs once the company computes them on its contract data, gross receivables by tier, the collection rate for the month and the trailing three months, the days past due buckets, PAR30, PAR90 and lagged PAR30, write offs and recoveries, and the indicative expected credit loss.

The vintage block is the one most often missing, and it gives the earliest warning. It sets repayment by cohort against plan at months three, six and twelve. The covenant block should show headroom, not only pass or fail. The calibrated SolaraPay case, a fictional company, passes its 70 per cent trailing collection covenant with a lowest reading of exactly 70.0 per cent. That is a pass with no headroom.

## Scene 7. Reconciling buckets to gross receivables
On screen: Bucket table in millions: current 700, 1 to 30 days 120, 31 to 60 days 50, 61 to 90 days 40, 91 to 180 days 60, over 180 days 30, total 1,000.

The buckets must add up to gross receivables. Platform exports often omit written off accounts or report arrears instead of balances. The Checks sheet enforces the reconciliation in Actual mode.

Take an illustrative month end with one billion local currency units of gross receivables. Seven hundred million is current and one hundred and twenty million is 1 to 30 days late. The buckets beyond 30 days add to one hundred and eighty million, so PAR30 is 18.0 per cent. Beyond 90 days sits ninety million, so PAR90 is 9.0 per cent. Eligible receivables up to 30 days are eight hundred and twenty million. At a 70 per cent advance rate, the borrowing base is five hundred and seventy four million.

The table also tests the write off policy. A large over 180 bucket means defaulted balances are still on the books. Either policy is acceptable if disclosed, but not if it changes from month to month.

## Scene 8. Reading the SolaraPay history
On screen: SolaraPay: collection 77.4 then 69.3 per cent, latest month 66.5 per cent, PAR30 17.0 per cent, ECL coverage 36.5 per cent. Sector collection rate about 62 per cent for 2021 to 2023, reported, pending the primary document.

SolaraPay's 24 months of history are synthetic. The portfolio collection rate was 77.4 per cent in the first year and 69.3 per cent in the second. The latest month read 66.5 per cent, with PAR30 at 17.0 per cent and indicative ECL, or expected credit loss, coverage of 36.5 per cent.

Sector figures offer context only. The ESMAP and World Bank market trends report for 2024 is reported to give an average PAYGo collection rate of about 62 per cent for 2021 to 2023. Its page and definition are still to be checked against the report, and it is a collection rate, not a PERFORM repayment rate. Against that, 69.3 per cent might pass. Read with the cohort data, it shows customers repaying below plan in every tier with history, and a book whose ratios will drift as growth slows. The case responds with a collections plan and a 65 per cent trailing collection covenant with a cure period, not a covenant the company would breach in its first quarter.

The case also shows the gap impact funders care about: no ownership evidence yet. Paid off customers should be tracked now, so the evidence exists when cohorts reach the checkpoint.

## Scene 9. Recap and exercise
On screen: Template T05 Lender KPI report: input, KPIs, covenants, vintage, dashboard.

Ask for the PERFORM 2026 KPIs computed on contract data, and refuse a collection rate offered in their place. Print the definition beside every operational and lender metric. Exclude deposits from the collection rate. Read portfolio ratios beside lagged and vintage measures, because growth flatters them. Reconcile the buckets and report covenant headroom, not just compliance.

Your exercise: open template T05 and load the SolaraPay history. Confirm the latest collection rate of 66.5 per cent and PAR30 of 17.0 per cent. Then compare PAR30 with PAR30 lagged by three months, and mark every covenant whose headroom is under a tenth of its threshold as a watch item.
