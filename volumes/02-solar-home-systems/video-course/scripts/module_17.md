# Module 17. Using MODEL 2, step by step

Duration: about 20 minutes. Book: Chapters 1 to 16. Model: MODEL 2, version 0.8 (development build), file AEF_SHS_PAYGo_Model_v0.8-dev.xlsx. User manual: Steps 1 to 12.

## Learning objectives
1. Work through the model in the order an analyst should.
2. Know which sheet holds each input and which sheet answers each question.
3. Read the integrity checks, the readiness gates and the investment summary correctly.

## Scene 1. Using MODEL 2, step by step
On screen: PAYGo Company Financial and Investment Model, in twelve steps

This tutorial walks you through MODEL 2, the PAYGo Company Financial and Investment Model, in twelve steps, in the order an analyst should work. Every screen you will see is the real workbook, version 0.8, a development build, with its default inputs. Those inputs describe a fictional company in a fictional market. They are there to make the mechanics visible, not to describe any real business. Keep the user manual open beside you. It follows the same twelve steps.

## Scene 2. Start here: Cover
On screen: Open the workbook, let it recalculate, and read the status panel before anything else. Sheet Cover, range B16:J44.

Open the workbook in Excel 2016 or later and let it recalculate fully. The cover carries a live status panel. First, the master check. It must read OK before you rely on any output. Below it, the readiness line: two of twenty three gates are met at default inputs, and the decision reads STOP, on a failed test. The covenant gate fails, as Step 11 shows. The model never rates a company. Then the active case, the illustrative model assumptions in the Base scenario, and the credit data mode, Proxy, which means the credit figures come from the model's curves. Before you change anything, save a copy under a new name and keep the original as your reference.

## Scene 3. Start here: Start
On screen: One page: what to input, what the model calculates, what the results mean and what an investor should look at. Sheet Start, range A1:D40.

Next, the Start sheet. It sets out on one page what to input, what the model calculates, what the results mean, and what an investor should look at, in that order. Every input carries a provenance label: model assumption, company data, external evidence, calibrated assumption or unverified. Read the third block before you quote any number. Revenue is not cash. The operational collection rate is not a PAYGo PERFORM KPI. The credit loss figures are analytical proxies. And the readiness decision measures the evidence file, not the business.

## Scene 4. Start here: Checks
On screen: Thirty eight integrity tests roll up into the master check. Readiness flags sit apart. Sheet Checks, range A1:C54.

The Checks sheet runs thirty eight integrity tests. The balance sheet balances, cash reconciles every month, the DPD buckets reconcile to gross receivables, and receivables, the loss allowance, debt and equity roll forward from month to month. Limits are respected and inputs are valid. Each test returns zero when it passes, and together they drive the master check. Below them sit seven readiness flags, such as affordability assumptions not yet reviewed. They are kept outside the master check on purpose. They tell you how mature the analysis is, not whether the arithmetic is right.

## Scene 5. Start here: Inputs
On screen: Blue cells are inputs, each with a provenance label. Set the scenario selector, the first model month and the currency label. Sheet Inputs, range A1:E14.

All hard coded assumptions live on a handful of sheets, and the colour code tells you where. Blue font is an input, the only kind of cell you should change. Black font is a formula. Never overwrite it. On the Inputs sheet, start with three settings. The first is the scenario selector, where one is Base, two is Downside and three is Severe. Then come the first model month and the local currency label. The last column gives each input's provenance. At default inputs every one reads model assumption, because the defaults describe a fictional market.

## Scene 6. Define the business: Products
On screen: Five tiers, labelled by the capacity attribute of the Multi Tier Framework. Replace them with your own catalogue. Sheet Products, range A4:G16.

The Products sheet holds one column per tier. Tier one is a pico solar kit on a twelve month plan. Tier five is a three kilowatt peak inverter system on a forty eight month plan. Replace the names, sizes, loads and segments with your own catalogue. Keep all five columns. If you sell fewer tiers, set the sales mix of the unused tier to zero. The tier label refers to capacity only, so check it against the product's real specification.

## Scene 7. Define the business: Consumer_Risk
On screen: Affordability is a credit risk. Replace the illustrative incomes with surveyed incomes. Sheet Consumer_Risk, range A1:G15.

Consumer Risk sets each tier's instalment against the household income of its target segment. The incomes shown are illustrative placeholders and must be replaced with survey or customer data. With the defaults, three tiers sit above the model's ten per cent policy threshold for payment burden: Tier 2 at 13.0 per cent, Tier 3 at 13.2 per cent and Tier 4 at 11.3 per cent. A high burden predicts higher default, so treat these flags as credit warnings, not only as social ones.

## Scene 8. Market assumptions: Inputs
On screen: FX, inflation, tax, the price increase on new contracts and FX pass through. Sheet Inputs, range A9:D14.

The macro block sets the opening exchange rate, 130 local currency units per dollar, local inflation of six per cent, a tax rate of thirty per cent, an annual price increase of five per cent on new contracts, and a pass through of fifty per cent of currency depreciation into new contract prices. Do not set depreciation to zero because the currency has been stable. A PAYGo company buys hardware and borrows in dollars while it collects in local currency.

## Scene 9. Market assumptions: Scenarios
On screen: Downside and Severe move credit, collections, volume, hardware cost and the currency together. Sheet Scenarios, range A4:E12.

The Scenarios sheet scales five levers. The Downside raises the default hazard by thirty per cent, trims collections and volume, raises hardware cost and sets depreciation at twelve per cent a year. The Severe case goes further, with a hazard 1.75 times Base and twenty five per cent depreciation. Real stress moves several variables at once, and so do these scenarios.

## Scene 10. Build demand: Inputs
On screen: Total units sold for Years 1 to 5 across all tiers. Sheet Inputs, range A16:D21.

Enter the total units sold in each of the five years. The defaults run from twelve thousand units in Year 1 to fifty thousand in Year 5. The model divides each year by twelve, applies the scenario volume multiplier and splits the sales by tier. Version 0.8 does not model seasonality, so read monthly results as averages.

## Scene 11. Build demand: Products
On screen: The sales mix must total 100 per cent. A check enforces it. Sheet Products, range A4:G23.

The sales mix sits on Products, and it must total one hundred per cent. A check enforces it. Be careful when you shift the mix towards Tiers 4 and 5. It raises value sharply, but those tiers usually have the least repayment history behind them.

## Scene 12. Build revenue: Products
On screen: Cash price, deposit, daily rate and tenor; the model derives the instalment, the premium and the implied APR. Sheet Products, range A12:G39.

Each price plan has four inputs: cash price, deposit, daily rate and tenor. Take Tier 2. A cash price of 39,000, a deposit of 4,000 and a daily rate of 77 over 24 months give a monthly instalment of 2,342 and a total contract value of 60,210. The PAYGo premium over the cash price is 21,210, and the implied annual rate is about fifty per cent. That rate is the figure a regulator or a journalist will compute, so know it first. Hardware revenue is booked at the cash price at sale, and the premium is earned as financing income over the tenor.

## Scene 13. Build revenue: Inputs
On screen: Four RBF designs. Ownership linked RBF pays nothing until validated ownership data exist. Sheet Inputs, range A30:D39.

Results based financing has four designs: sales based, repayment linked, ownership linked and hybrid. Ownership linked RBF pays zero by design until validated ownership data have been loaded and this evidence switch is set to one. The model will not manufacture that outcome from proxy curves.

## Scene 14. Hardware and capital costs: Products
On screen: Hardware FOB cost in US dollars; landed cost includes freight and duty at the month's exchange rate. Sheet Products, range A17:G46.

Hardware is entered as the dollar FOB cost per unit. The model adds freight and duty, converts at the exchange rate of the month and applies the scenario hardware cost lever. For Tier 2, a cost of 150 dollars becomes a landed cost of 23,400 at the opening rate. Installation, warranty and the acquisition cost are set per tier. Do not enter a local price already converted at today's rate. That would count depreciation twice.

## Scene 15. Operating costs: Inputs
On screen: Payment fees, servicing per active account, staff and general and administrative costs. Sheet Inputs, range A23:D28.

Operating costs follow their drivers. Payment fees are two per cent of cash collected. Customer service and collections cost 150 per active account per month. Staff and general costs are fixed monthly amounts, indexed to inflation. Size the central costs for the volume plan. A book of seventy thousand active accounts needs a collections team, a call centre and a data function.

## Scene 16. Financing: Inputs
On screen: Initial equity, a dollar term loan and a local currency receivables facility, with an automatic equity top up. Sheet Inputs, range A48:D57.

Four sources fund the plan: initial equity, a dollar term loan revalued every month, a local currency receivables facility, and an automatic equity top up whenever cash would fall below the minimum. The facility is drawn only to hold the minimum cash balance, up to the lower of its limit and the borrowing base. The cumulative top up is your funding requirement. It is equity you must raise, not free money.

## Scene 17. Financing: Credit_Assumptions
On screen: Default at 180 DPD, staging thresholds, borrowing base eligibility, recovery cost and the proxy DPD distribution. Sheet Credit_Assumptions, range A4:E24.

Credit Assumptions holds the definitions. Default at 180 days past due. Stage 2 from thirty days and Stage 3 from ninety days for the indicative expected credit loss. Borrowing base eligibility up to thirty days past due. A recovery cost of fifteen per cent of resale proceeds. The binding constraint on the facility is usually the borrowing base, not the limit, and it shrinks when credit quality deteriorates.

## Scene 18. Financial statements: Annual
On screen: Read the revenue mix, credit losses charged at origination, and EBITDA year by year. Sheet Annual, range A5:I28.

The Annual sheet sums the monthly statements by year. Check the revenue mix between hardware, financing income and other revenue. Expected credit losses are charged when each contract is originated, so a growing book carries the full lifetime loss of its newest cohorts. In the default Base case, EBITDA turns positive in month 21.

## Scene 19. Financial statements: Annual
On screen: Profit arrives before cash. The balance check must read zero; the cash flow shows the true funding gap. Sheet Annual, range A30:I62.

Now the balance sheet and cash flow. The balance check must read zero in every period. Operating cash flow stays negative while the receivables book grows. In the default case it stays positive only from month 51, thirty months after EBITDA. A PAYGo company can report a profit and still run out of cash. The cash flow statement and the funding requirement are the figures to trust.

## Scene 20. Scenarios: Sensitivity
On screen: Fifteen dated cases computed at default inputs, and a live row for the active case. Currency and pricing move value more than volume. Sheet Sensitivity, range A5:I24.

Switch the selector between Base, Downside and Severe and read the investment summary each time. The Sensitivity sheet holds a static table of fifteen cases, dated and computed at default inputs, and below it a live row that follows the active case. The Base investor IRR is 46.4 per cent. In the Downside the IRR is minus 22.9 per cent, and the Severe case is a total loss. Look at the currency rows. Twenty per cent depreciation a year takes the Base IRR to minus sixteen per cent, and freezing prices on new contracts cuts it to 7.9 per cent. Remember to reset the selector to Base before you save.

## Scene 21. Lender case: Credit_Portfolio
On screen: Gross receivables by DPD bucket, the collection ratio, indicative ECL and the borrowing base with its headroom. Sheet Credit_Portfolio, range A4:L31.

Credit Portfolio consolidates the five tiers month by month: gross receivables by DPD bucket, the collection ratio, PD and LGD proxies, the indicative stage based ECL, and the borrowing base with its headroom against the facility. The buckets reconcile exactly to gross receivables. This is the view a lender reads first.

## Scene 22. Lender case: Covenants
On screen: Each covenant is tested monthly. Headroom matters as much as compliance. Sheet Covenants, range A4:L26.

Covenants tests each threshold every month and flags breaches. In the default Base case the lowest trailing three month collection rate is 72.9 per cent against a minimum of seventy, and no month breaches. Look at the headroom, not only at the pass or fail flag. The annual DSCR sits on the KPIs sheet. It is below its minimum of 1.20 times in Years 1 to 4, so the readiness gate on covenants is not met. DSCR is a poor test for a growing book, so replace it with portfolio covenants in the facility rather than ignore it.

## Scene 23. Lender case: Credit_Input
On screen: Paste the company's own history, then switch the credit data mode to Actual. Shown here: the fictional SolaraPay case. Sheet Credit_Input, range A6:L25.

Now load the company's own data. Credit Input takes one block per tier and up to sixty months: month end balances and DPD buckets, and monthly flows such as originations, collections and write offs. The screen shows the SolaraPay case workbook, whose history is synthetic teaching data. The buckets must add up to gross receivables. Then set the credit data mode to Actual. Reporting switches to the company's history, while projections stay on the curves.

## Scene 24. Lender case: Vintage_Dashboard
On screen: Compare observed cohorts with the proxy curves, then recalibrate the hazards and collection rates on Products. Sheet Vintage_Dashboard, range A1:I20.

Vintage Dashboard sets the observed cohorts against the plan curves. In the SolaraPay case, every tier with history repays below plan at month 12. When the curves diverge, recalibrate the default hazard and collection rates on the Products sheet. Lenders lend against data, and twelve or more months of clean cohort history is the fastest route to better terms.

## Scene 25. Investment memo: Valuation
On screen: DCF on normalised free cash flow, exit value, and investor returns in US dollars. Sheet Valuation, range A22:D40.

Valuation holds three views. The DCF of free cash flow gives an enterprise value of about 15.6 million dollars, with a terminal value larger than the whole value, which is normal for a growing PAYGo book. The exit value at six times EBITDA gives an equity value of about 80.6 million dollars at the end of Year 5. The investor's stake of one third then returns an IRR of 46.4 per cent and 6.7 times the money, in dollars. Present the DCF and the exit value side by side and explain the gap.

## Scene 26. Investment memo: Unit_Economics
On screen: Per tier: expected loss, contribution, LTV to CAC, cash payback and unit IRR. Sheet Unit_Economics, range A4:G24.

Unit Economics answers whether each sale creates value. For Tier 2 at default inputs, the expected loss is about 35.6 per cent of scheduled instalments, LTV to CAC is 4.8 times, and the cash payback is fifteen months. Read the ratio with the payback and the unit IRR. A strong ratio on a product with no repayment history is a hypothesis, not a result.

## Scene 27. Investment memo: Calibration
On screen: Diagnostics use verified references only. Suspended or conflicting references are shown, never used as targets. Sheet Calibration, range A5:F12.

Calibration turns benchmarks into questions, and it compares the model only with references whose source is verified. At this edition, every reference on the sheet is suspended or absent. The M-KOPA group figures conflict between sources, so that comparison is withdrawn until the group's consolidated accounts are read. The ESMAP sector collection rate is pending its primary document, and it is context for the model's operational collection rate, not a PERFORM repayment rate. The sheet asks you to justify the cost and credit assumptions on the company's own data. It never changes an input on its own.

## Scene 28. Investment memo: Investment_Readiness
On screen: Twenty three gates, thirteen critical. The decision rule reads evidence only: STOP, CONDITIONAL GO or GO. Sheet Investment_Readiness, range A4:G36.

Finally, Investment Readiness. Twenty three gates, automatic where the model can test them and manual where they need outside evidence, such as legal review or the auditor's view of the ECL approach. A manual gate counts only when the sheet records where the evidence is held and who signed it off. Thirteen gates are critical, and the decision rule uses the evidence and nothing else. It reads STOP when a test fails, GO only when all twenty three gates are met, and CONDITIONAL GO when every critical gate is met. Otherwise it reads STOP, because the evidence is incomplete. At default inputs two gates are met and the decision is STOP on a failed test. Gate ten now covers the annual DSCR as well as the monthly covenants, and the DSCR sits below its minimum in Years 1 to 4. A STOP on incomplete evidence is not a verdict on the business, but a STOP on a failed test is a finding against the plan as modelled. A GO is not an investment recommendation. Every gate not yet met should become a condition precedent, a covenant or an accepted risk in the investment memo.

## Scene 29. Investment memo: Investment_Summary
On screen: The one page summary for the investment committee, live for the active scenario. Sheet Investment_Summary, range A4:G35.

The Investment Summary brings it together on one page for the active scenario: the operating trajectory, the funding requirement, valuation and returns, the lender view and unit economics by tier. Build the memo from this page and the sheets behind it, using Template T01, and check every figure you quote against its source sheet.

## Scene 30. Investment memo: Dashboard
On screen: Thirty nine labelled metrics by year, rounded for reading, each with its unit and its source sheet. Sheet Dashboard, range A5:H50.

Behind the summary sits the Dashboard: a table of thirty nine labelled metrics by year, rounded for reading, each with its unit and its source sheet. Single values, such as returns, peaks, timing and readiness, sit under Year 1. Three readings teach the most. First, revenue is not cash. Cash conversion, operating cash flow over EBITDA, reads not applicable in Years 1 and 2, while EBITDA is negative. It is then minus 1.32 times in Year 3, minus 0.08 times in Year 4 and 0.25 times in Year 5, because the growing receivables book absorbs the cash. Second, the operational collection rate falls from 84.5 per cent in Year 1 to 73.3 per cent in Year 5. It is labelled not a PERFORM KPI, and the PERFORM repayment line below it reads not provided, because only company results can fill it. Third, the net FX transaction effect on costs and RBF, before price pass through, is a cost that grows from about twenty five million local currency units in Year 1 to about nine hundred and twenty eight million in Year 5. The last lines repeat the readiness result: two of twenty three gates met, and a decision of STOP, on a failed test.

## Scene 31. Twelve steps, one discipline
On screen: Load the company's data before you trust the projections

That completes the twelve steps. Three habits matter most. Never use an output while the master check reads error. Load the company's own history before you trust any projection. And read the Downside as carefully as the Base. The user manual, the case study, the templates and the decision tools take each step further. Thank you for watching.
