# Module 16. Case walk through: SolaraPay

Duration: about 10 minutes. Book: Chapter 16. Model sheets: Credit_Input, Vintage_Input, Credit_Assumptions, Credit_Portfolio, Vintage_Dashboard, Products, Unit_Economics, Consumer_Risk, Dashboard, KPIs, Covenants, Valuation, Benchmark_Compare, Calibration, Investment_Readiness. Templates and tools: case workbook SolaraPay_Case_Model_v0.8-dev, D3 Repayment curve and cohort calibration, D6 Investor returns calculator, T01 Investment committee memorandum, T06 Loan tape specification and data request, T07 Borrowing base certificate and term sheet checklist.

## Learning objectives
1. Apply the method end to end: load history before touching projections, recalibrate, and read unit economics and affordability.
2. Compare the management plan with the calibrated case under stress, and read valuation and the lender's covenant position.
3. Build a Conditional Go recommendation whose conditions map to the risks and readiness gates found.

## Scene 1. The ask
On screen: Title card. SolaraPay Ltd, Republic of Kivara, fictional. Equity: 4.0 million dollars at 8.0 million pre money, 33.3 per cent. Facility: 4.5 billion shillings at 16 per cent.

This module follows an analyst at an impact fund through one file. SolaraPay Ltd and the Republic of Kivara are fictional, the 24 month history is synthetic, and every figure comes from the case workbook.

SolaraPay sells solar products on PAYGo, or pay as you go, terms. Its currency is the Kivara shilling, at an opening rate of one hundred and thirty five shillings to the dollar. It asks the fund for four million dollars of equity at a pre money valuation of eight million, a stake of 33.3 per cent. It asks a local bank for a receivables facility of four point five billion shillings at 16 per cent. Eligibility runs to 30 days past due.

About 65 per cent of planned volume sits in Tiers 1 and 2. Most of the value sits in Tiers 4 and 5, which the company has never sold. And the facility is about 3.7 times total equity in shillings, so the equity case depends on the facility and its covenants.

## Scene 2. Load the history first
On screen: Credit_Input and Vintage_Input loaded. Credit data mode set to Actual on Credit_Assumptions. Portfolio collection rate 77.4 to 69.3 per cent. Latest month: 66.5 per cent, PAR30 17.0 per cent.

Management built its plan on the workbook's default credit assumptions. The analyst loads the company's data before touching the projections.

Twenty four months of portfolio data for Tiers 1 to 3 go into Credit_Input, and eighteen monthly cohorts per tier into Vintage_Input. The credit data mode is set to Actual. That changes the reports, not the projections. History is never blended silently into the forecast.

The data contradict the plan. The portfolio collection rate fell from 77.4 per cent in the first year to 69.3 per cent in the second. In the latest month the collection ratio is 66.5 per cent, PAR30, the share more than 30 days past due, is 17.0 per cent, and indicative coverage by expected credit loss, or ECL, is 36.5 per cent. At month 12, cohorts repay below plan in every tier. Tier 2, for example, has repaid 69.4 per cent against a plan of 74.5. Recoveries are close to nil, with a loss given default proxy of about 99 per cent. And no cohort is old enough to show ownership.

## Scene 3. Recalibration
On screen: Products sheet. Hazard: Tier 1 3.50 to 4.55 per cent, Tier 2 2.60 to 3.38 per cent, Tier 3 1.90 to 2.47 per cent. Survival to end of contract, Tier 2: 53.1 to 43.8 per cent.

The analyst re-estimates the Tier 1 to 3 curves so that projected cohorts sit on the observed points. Each calibrated monthly default hazard is exactly 1.30 times the plan. That is the workbook's Downside multiplier. On credit hazard, the company's history already sits at management's Downside. Collection rates on paying accounts fall by one or two points.

The effect is large. For Tier 2 over 24 months, the share of accounts still paying at the end falls from 53.1 per cent to 43.8 per cent. Tiers 1 and 3 lose eight to nine points.

Tiers 4 and 5 stay on the default curves, because there is no history. That assumes customers of products never sold will repay better than any tier the company has sold. Real data will fit less neatly than synthetic history, but the principle holds: a plan contradicted by the company's own history cannot serve as a base case.

## Scene 4. Unit economics and affordability
On screen: Unit_Economics table. Expected loss, LTV to CAC, payback, unit IRR by tier. Tier 2: 41.8 per cent, 3.5 times, 17 months, 37 per cent. Consumer_Risk: Tier 2 13.0, Tier 3 13.2, Tier 4 11.3 per cent of income.

With calibrated curves, every tier still creates value per unit. The distribution is the issue.

Tier 2 is the largest product, at 40 per cent of planned units, and the weakest. It loses 41.8 per cent of scheduled instalments, pays back in 17 months, and earns a unit internal rate of return, or IRR, of 37 per cent, the lowest in the range.

Tiers 4 and 5 look strongest, with lifetime value to acquisition cost, or LTV to CAC, of 11.0 and 14.9 times. Those ratios rest entirely on curves with no history. Tier 1 pays back in nine months, but its contribution is only one thousand and ninety two shillings per unit, and its implied annual rate of 106 per cent will draw attention.

Affordability adds a second lens. Three tiers sit above the model's 10 per cent policy threshold for payment burden: Tier 2 at 13.0 per cent of illustrative income, Tier 3 at 13.2 and Tier 4 at 11.3. The incomes are illustrative and need survey data.

## Scene 5. The calibrated projections
On screen: Dashboard. Revenue 1.13 to 8.62 billion shillings. EBITDA margin minus 35.2 to 16.4 per cent. Collection rate 82.3 to 70.3 per cent. Debt to book equity peaks at 2.51 times in Year 3.

In the calibrated Base, revenue grows from one point one three billion shillings in Year 1 to eight point six two billion in Year 5, or from eight point one to fifty one point two million dollars.

The margin on EBITDA, earnings before interest, tax, depreciation and amortisation, moves from minus 35.2 per cent to 16.4 per cent. Net credit losses still take 27.5 per cent of revenue in Year 5. The collection rate falls every year and ends at 70.3 per cent, a fraction above the proposed covenant. Leverage peaks at 2.51 times book equity in Year 3, inside the limit of 3.0 times.

No equity top up is needed. Against the management plan, calibration lowers the investor IRR from 33.1 to 29.0 per cent. The plan survives its own data but loses most of its headroom.

## Scene 6. Stress tests
On screen: Stress table. Calibrated Downside: total loss, 40 breach months. Full FX indexation: 23.6 per cent, 38 months. Tier 4 and 5 hazard doubled: 14.8 per cent. Entry at 6 million pre money: 33.8 per cent.

The calibrated Downside applies the 1.30 hazard multiplier on top of a hazard already 1.30 times the plan. Relative to management, Tier 1 to 3 hazards are 1.69 times the plan, close to the 1.75 of the Severe case. On this data, the Downside may be more likely than its label suggests.

The Downside wipes out the equity without any call for new cash. Peak equity stays at nine million dollars, but at exit net debt exceeds six times a much reduced EBITDA, so exit equity is zero, with 40 breach months.

Pricing power is the strongest mitigant. Indexing new contract prices fully to the exchange rate turns the Downside into a 23.6 per cent IRR and a 14.2 per cent EBITDA margin. It leaves 38 breach months, so it protects the equity more than the lender.

Tier 4 and 5 credit is the largest unproven risk. Doubling their hazard roughly halves the IRR, from 29.0 to 14.8 per cent. Entry at six million pre money lifts the IRR to 33.8 per cent, which helps but does not change the risk.

## Scene 7. Valuation and the lender view
On screen: Valuation sheet. DCF enterprise value 6.1 million dollars at 22 per cent. Exit equity 42.9 million dollars. One third is 14.3 million, a multiple of 3.6 times. Lowest trailing collection rate 70.0 per cent against 70 per cent.

The discounted cash flow, or DCF, gives an enterprise value of six point one million dollars at 22 per cent, below the eight million pre money. A third of exit equity of forty two point nine million dollars gives a multiple of about 3.6 times and an IRR of about 29.0 per cent. The entry price is a position on the exit multiple and on credit quality, and the fund should protect both.

For the bank, the covenants hold in the calibrated Base, but barely. The lowest trailing three month collection rate is 70.0 per cent against a 70 per cent minimum, so there is no headroom. On actual data, with 69.3 per cent over the second year and 66.5 per cent in the latest month, a 70 per cent covenant would very likely be breached at the first test date. The bank can set the covenant at a level the book can meet, such as 65 per cent with a cure period, or defer the facility. The debt service coverage ratio sits below 1.20 times in Years 1 to 4, so portfolio covenants should replace it.

## Scene 8. Benchmarks and the recommendation
On screen: Benchmarks: no verified reference, M-KOPA comparison withdrawn. ECL to financing revenue 1.28 times. Analyst: Conditional Go, seven conditions. Workbook: 5 of 23 gates, STOP on incomplete evidence.

The analyst finds that no external reference can be used as a test. The net margin and credit loss references rested on M-KOPA group figures that conflict between sources, so that comparison is withdrawn until the group's consolidated accounts are read. The ratios speak for themselves. Expected credit loss runs at 1.28 times financing revenue, so the financing income does not cover the losses it is meant to price. The hardware margin is carrying them. The benchmark that matters is SolaraPay's own cohort history.

The analyst recommends a Conditional Go: invest four million dollars subject to seven conditions. Index new prices fully to the exchange rate. Cap Tiers 4 and 5 at their planned 13 per cent of units, released only after twelve months of cohort data within 10 per cent of plan. Agree a collections plan and a 65 per cent trailing collection covenant with a cure period. Cut recovery assumptions to observed levels. Redesign Tier 2 to 4 price plans so the instalment stays within 10 per cent of surveyed income. Protect the valuation, towards six million pre money or with a ratchet. And require monthly data, ownership tracking, an independent ECL review and a full test of the workbook.

The workbook's own rule reads STOP for the same file. The case meets 5 of the 23 readiness gates, and 8 of the 13 critical gates still lack evidence. The two do not contradict each other. The workbook measures whether the evidence file is complete; the recommendation is the analyst's judgement of what the investment needs. The committee should see both, and disbursement waits until the critical gates that the conditions address are evidenced. The memo says so.

## Scene 9. Recap and exercise
On screen: Recap. History before projections. Calibrated Base sits at plan Downside. Pricing protects equity. Tiers 4 and 5 unproven. Exercise: combined stress, recorded in T01.

Load history first, and treat the management plan as one scenario among several. On SolaraPay's own data the Base sits at the plan's Downside on credit hazard, and the collection covenant has no headroom. Pricing power protects the equity, while the untested Tiers 4 and 5 hold both the strongest unit economics on paper and the largest unproven risk. The most important number in a PAYGo file is often the one the company cannot yet produce.

Your exercise uses the case workbook. On a copy, run the calibrated Downside with full price indexation and, at the same time, double the default hazard on Tiers 4 and 5. Record the IRR, the multiple and breach months. Then decide whether the seven conditions still support a Conditional Go, and write your answer in section 6 of the T01 memo.
