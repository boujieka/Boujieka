# Module 6. Repayment behaviour: cohorts, curves and defaults

Duration: about 9 minutes. Book: Chapter 6. Model sheets: Products, Curves, Cohort_T1 to Cohort_T5, Credit_Assumptions, Credit_Input, Vintage_Input, Vintage_Dashboard, Credit_Portfolio, Checks. Templates and tools: D3 Repayment curve and cohort calibration, T06 Loan tape and data request.

## Learning objectives
1. Compute survival and cumulative repayment from a monthly default hazard and a collection rate, and read a cohort against plan.
2. Use DPD buckets, roll rates and cures, and explain why portfolio ratios improve in a growing book without any change in credit quality.
3. Calibrate hazards and collection rates to observed cohorts, and keep history and projection apart with Proxy and Actual modes.

## Scene 1. The assumption behind every number
On screen: Title "How will customers actually pay?" with the chain: repayment, receivables, borrowing base, covenants, valuation.

Revenue, receivables, the borrowing base, covenant headroom and valuation all flow from a small set of repayment assumptions. When those assumptions are wrong, the error rarely shows in the first year, because new sales hide it.

Cohorts, survival curves, arrears buckets and roll rates are how a credit officer finds the error before the lender's covenant test does.

## Scene 2. Cohorts and vintages
On screen: A cohort grid: months of sale down the side, account age across the top.

A cohort, or vintage, is the group of accounts sold in the same month for the same product. Customers behave according to how long they have had the product, not according to the calendar. So each cohort is measured against account age, in months since sale.

The workbook is built the same way. The Curves sheet defines how one unit of each tier behaves at each age. The cohort sheets, Cohort_T1 to Cohort_T5, apply those curves to every monthly cohort. The Ops sheet adds them up by calendar month. Portfolio figures are always sums of cohort behaviour, never assumptions in their own right.

## Scene 3. The survival model
On screen: Curves sheet. Tier 2 survival: 72.9 per cent at month 12, 53.1 per cent at month 24.

The repayment engine rests on one assumption. Each month, a fixed share of the accounts still paying stops paying for good. That share is the monthly default hazard.

Survival to a given age is one less the hazard, raised to the power of the age in months. The instalment collected at that age is the instalment times the collection rate on paying accounts times survival. The collection rate captures payers who skip days. The hazard captures customers who leave altogether.

Take the default Tier 2 product, an SHS, or solar home system, with a TV, sold over 24 months, with a hazard of 2.6 per cent and a collection rate of 88 per cent. At month twelve, 72.9 per cent of accounts survive. At month twenty four, 53.1 per cent. The expected payment in the last month is 46.8 per cent of the instalment due.

Tenor and hazard interact. Tier 1, with a hazard of 3.5 per cent over 12 months, ends its tenor with 65.2 per cent still paying. Tier 3, with 1.9 per cent over 30 months, ends with 56.2 per cent. A lower hazard over a longer tenor can leave a similar share of non payers. Tenor extension is a credit decision, not only an affordability one.

Real hazards are usually higher in the first months and lower later. A constant hazard calibrated at month twelve will understate early losses and overstate late ones, which matters for the timing of covenant tests.

## Scene 4. Cumulative repayment curves
On screen: Chart of Tier 2 cumulative repayment: 83.5, 80.3, 74.5, 69.2 and 64.4 per cent at months 3, 6, 12, 18 and 24.

The most useful single picture of a cohort is its cumulative repayment curve. It is cumulative collections divided by cumulative instalments due, at each account age. Deposits are excluded from both sides, because every customer pays a deposit and it would flatter the ratio.

For default Tier 2, the curve reads 83.5 per cent at month three, 74.5 per cent at month twelve and 64.4 per cent at month twenty four. It falls throughout, because each month adds a full instalment due and a collection from a shrinking pool of payers.

The curve lets you compare each cohort with plan from its first month. A cohort five points below plan at month twelve will not close that gap by month twenty four unless something changes in collections. On a constant hazard, the gap widens.

## Scene 5. Arrears buckets, roll rates and cures
On screen: Buckets: current, 1 to 30, 31 to 60, 61 to 90, 91 to 180, over 180 DPD. Roll rate path: 10, 40, 60, 75 per cent.

Day to day credit management works with arrears, measured in DPD, or days past due. The workbook uses six buckets, from current to over 180 days.

DPD needs a definition first. Some platforms count days since the device last had credit. Others measure the shortfall against the payment schedule. The schedule based measure reconciles to the receivable, so it is closer to how a lender thinks. Whichever is used, state it and keep it.

Roll rates measure the share of a bucket that moves to the next one a month later. In an illustration, 10 per cent of current accounts move to 1 to 30 days, 40 per cent of those roll on, then 60 per cent, then 75 per cent. Multiply the four and 1.8 per cent of a current pool reaches 91 days past due three months later.

A cure is an account that returns to current. PAYGo, or pay as you go, has more cures than most consumer lending, because the lights go off. But roll rates fall steeply past 60 or 90 days. An account dark for three months has usually found an alternative. The workbook's proxy engine assumes no cures in the cash forecast, and uses a cure rate of 30 per cent only in the indicative expected credit loss.

## Scene 6. Lockout and the default definition
On screen: Default definition: 180 DPD in the workbook. Same definition for default flag, write off, repossession and lender data.

The lockout loses its force once the customer stops valuing the service, for example when the battery degrades or the grid arrives. Then the account moves quickly through the buckets and stays there.

The workbook defines default at 180 days past due. Ninety days is another common choice. A longer definition delays recognition and lifts reported cures. A shorter one may count as defaulted customers who would have paid. The same definition should drive the default flag, the write off, the repossession trigger and the lender's data.

## Scene 7. Seasoning and the denominator effect
On screen: Same customers, three growth rates: 64.4, 68.3 and 71.6 per cent portfolio collection rate.

A new cohort's losses arrive over the next 12 to 30 months. A portfolio ratio is therefore a weighted average of cohorts at different ages, and growth sets the weights.

Take the Tier 2 curve and a company selling the same volume every month for two years. Its portfolio collection rate is 64.4 per cent. If sales instead grow 5 per cent a month, the same customers produce 68.3 per cent. At 10 per cent growth, 71.6 per cent. Nothing about credit has changed. Only the denominator has.

When growth slows, the ratios deteriorate even if behaviour is stable. In the workbook's Base case the collection rate falls from 84.5 per cent in Year 1 to 73.3 per cent in Year 5, with no change in hazards. Read cohort curves, and use lagged portfolio ratios, to see through it.

## Scene 8. Calibrating against observed cohorts
On screen: SolaraPay month 12 repayment, observed against plan: Tier 1 64.6 against 70.3, Tier 2 69.4 against 74.5, Tier 3 76.3 against 79.6. Vintage_Dashboard.

The default curves are proxies for a fictional market. Once a company has twelve months of cohort history, they should be replaced.

The SolaraPay case, a fictional company with 24 months of synthetic history, shows the method. At month twelve every tier sat below plan, by 5.7, 5.1 and 3.3 points for Tiers 1 to 3. Recalibration set each hazard at 1.3 times its plan value. Tier 2 moved from 2.6 to 3.38 per cent, and its collection rate from 88 to 87 per cent. The refitted Tier 2 curve gives 70.1 per cent at month twelve, against 69.4 observed. Over the full tenor the effect is larger. Survival at month twenty four falls to 43.8 per cent, against 53.1 on the default curve.

Two cautions apply. One checkpoint can be matched by many pairs of hazard and collection rate, so use months six and eighteen to choose. And Tiers 4 and 5 had no history and kept proxy values, which is ignorance, not comfort.

In the workbook, set Credit_Assumptions to Actual mode, load history into Credit_Input and Vintage_Input, and compare on Vintage_Dashboard. History is reported as history, and projections stay on the calibrated curves.

## Scene 9. Recap and exercise
On screen: Decision tool D3: curve sheet, calibration sheet, portfolio effect sheet.

Every portfolio figure is a sum of cohort behaviour, so start from cohorts measured by account age. Survival and cumulative repayment follow from a hazard and a collection rate. Growth flatters portfolio ratios, and cohort curves remove that flattery. Calibrate to observed history before trusting any plan.

Your exercise: open decision tool D3 and enter the SolaraPay Tier 2 observation of 69.4 per cent at month twelve, with the matching points at months three, six and eighteen if your data hold them. Compare the best fit with the case's 3.38 per cent hazard and 87 per cent collection rate. Then use the portfolio effect sheet to reproduce the 64.4, 68.3 and 71.6 per cent figures at zero, 5 and 10 per cent monthly growth.
