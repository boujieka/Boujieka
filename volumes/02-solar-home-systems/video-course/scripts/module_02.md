# Module 2. Market, customers and affordability

Duration: about 8 minutes. Book: Chapter 2. Model sheets: Consumer_Risk, Products, Scenarios, Checks, Investment_Readiness. Templates and tools: D1 Price plan and APR calculator, T03 Customer credit policy.

## Learning objectives
1. Match each product tier to its customer segment and explain how seasonality changes the affordability test.
2. Compute the payment burden, the deposit share of income and the implied APR of a price plan, under both the nominal and effective conventions.
3. Judge the evidence behind affordability data and link a high burden to the default hazard assumptions in the model.

## Scene 1. Who can pay, and how much
On screen: Title. "Who can pay, and how much?"

This module supports one decision: who can pay, and how much.

Every PAYGo, or pay as you go, price plan bets that a household can meet an instalment every month, for the whole tenor, out of a small and irregular income.

Counting households without grid access answers a different question. The investor must know how many can carry the instalment, and the lender how that changes in a bad harvest.

## Scene 2. Segments by tier
On screen: Table of five tiers. Pico kit, 12 months. SHS with TV, 24 months. SHS with fridge, 30 months. Inverter 1.2 kWp, 36 months. Inverter 3 kWp, 48 months.

The workbook carries five product tiers, and each implies a different customer.

Tier 1 is a pico solar kit on a twelve month plan, often for rural customers new to formal credit. The instalment competes with kerosene and torch batteries.

Tier 2 is a solar home system with a television, over twenty four months. When money is short, television is easier to give up than light.

Tier 3 adds a fridge, over thirty months, and can turn the product into an income source for a kiosk.

Tiers 4 and 5 are solar inverters with lithium storage, over thirty six and forty eight months. They serve urban households and small businesses on a weak grid, with higher incomes. But the amounts financed are an order of magnitude larger, and for most companies their repayment behaviour is unknown.

The default monthly hazard falls as tiers rise, from 3.5 per cent for Tier 1 to 2.6, 1.9, 1.3 and 1.0 per cent for Tiers 2 to 5. These are model defaults for a fictional market, not sector evidence. Replace them with cohort data where you have it.

## Scene 3. Seasonality
On screen: Income through the year. Harvest peak. Lean months. School fees.

Most rural customers earn from farming, casual labour, trading or remittances. Cash is plentiful after harvest and scarce in the months before it, when food runs low and school fees fall due.

This has three consequences. An affordability ratio on average income overstates capacity in the months that matter. A month's collection rate must be compared with the same month in earlier years before it is read as a trend. And cohorts sold in different seasons behave differently. A customer who buys just after harvest pays the deposit easily, then meets the lean season a few months in.

Version 0.8 of the workbook works with monthly averages and does not model seasonality. You must apply it yourself, in the affordability test and in reading monthly figures.

## Scene 4. Payment burden
On screen: Payment burden equals monthly instalment divided by monthly household income. Threshold 10%. Consumer_Risk sheet.

The core measure is the payment burden. It is the monthly instalment divided by monthly household income. The Consumer_Risk sheet computes it for each tier and raises a flag when it exceeds a maximum. The default maximum is 10 per cent.

That threshold is a model policy threshold, not a law, a regulatory standard or an empirical boundary between good and bad credit. A company may justify a different line with repayment evidence. What it should not do is set the threshold after the fact to clear the products it wants to sell.

Take the illustrative Tier 2 plan from Module 1. The instalment is two thousand one hundred and ninety local currency units. Assume average monthly income of eighteen thousand, made of six lean months at twelve thousand and six good months at twenty four thousand.

On average income the burden is 12.2 per cent, so the plan fails. In a good month it is 9.1 per cent and passes. In a lean month it is 18.3 per cent.

To pass on average income, the household must earn at least twenty one thousand nine hundred a month. Or the instalment must fall to about one thousand eight hundred, which means a daily rate of about fifty nine.

SolaraPay shows the same problem in its own plan. On its illustrative incomes, the burden is 13.0 per cent for Tier 2, 13.2 per cent for Tier 3 and 11.3 per cent for Tier 4. All three are above the threshold.

## Scene 5. The deposit as a screen
On screen: Deposit: lowers exposure, screens customers. 22.2% of average income. 33.3% of a lean month.

The deposit reduces the amount financed. More importantly, it screens customers. A household that can assemble a few weeks' income has shown it can save.

A higher deposit lowers conversion, and the customers who remain should repay better. Only a company that has varied its deposit and tracked the cohorts knows where the balance lies.

In our example, the deposit of four thousand is 22.2 per cent of average monthly income, and 33.3 per cent of a lean month. Watch for deposits cut sharply in sales campaigns. Weaker cohorts tend to follow, and portfolio figures hide the effect for several months.

## Scene 6. The implied APR
On screen: Tier 2 example. Monthly rate 3.28%. Nominal APR 39.3%. Effective rate 47.3%. Flat rate 23.0%. D1 calculator.

Customers see a deposit, a daily rate and a number of days, not a loan. The implied annual percentage rate, or APR, is the figure a regulator or a journalist will compute. Management should know it first.

The monthly rate is the one that discounts the instalments back to the amount financed. For the Tier 2 plan, thirty six thousand financed, repaid at two thousand one hundred and ninety a month over twenty four months, it is about 3.28 per cent.

Twelve times that monthly rate gives a nominal APR of 39.3 per cent. Compounding it over a year gives an effective rate of 47.3 per cent. Any disclosure must say which convention it uses, and local counsel must confirm which one the rules require.

The flat rate is the premium divided by the amount financed and by the years. Here it is 23.0 per cent. It understates the cost by about half, because the balance declines as the customer pays.

SolaraPay's implied APRs run from 106 per cent on Tier 1 down to 50, 39, 32 and 25 per cent. The highest rate sits on the smallest product, because fixed costs are spread over a small amount financed. It is also the most exposed to a rate cap.

## Scene 7. The Multi Tier Framework and the data
On screen: Multi Tier Framework attributes. Capacity, duration, reliability, quality, affordability, legality, health and safety. Data: surveys, agents, mobile money, own repayment.

The Multi Tier Framework from ESMAP, set out in Beyond Connections in 2015, defines Tiers 0 to 5 of household electricity access. It uses capacity, duration, reliability, quality, affordability, legality, and health and safety. The workbook uses the tier labels on capacity alone. Treating a capacity label as a full access assessment in impact reporting is a common error.

The illustrative incomes in the workbook are placeholders. A readiness flag on the Checks sheet stays raised until you replace them and record their status.

Surveys, agent data and mobile money histories can fill them, each with its own bias. In the end, the company's own repayment data are the most reliable test. A customer who pays for twelve months has shown the instalment was affordable over a full seasonal cycle.

## Scene 8. From affordability to default risk
On screen: SolaraPay Tier 2. Burden 13.0%. Hazard 2.60% to 3.38%. Month 12 repayment 69.4% against 74.5% plan.

Affordability is a credit risk before it is a social one. The workbook does not link burden to hazard by formula. You make that link through the hazard inputs on Products, and test it on Scenarios.

SolaraPay shows why. Its Tier 2 burden is 13.0 per cent. Calibrated to its history, the Tier 2 monthly hazard rises from 2.60 to 3.38 per cent. Cumulative repayment at month twelve is 69.4 per cent, against a plan of 74.5. The data do not prove that the burden caused the shortfall, but they are consistent with it. An investment committee would not accept a plan that assumed the problem away.

## Scene 9. Recap and exercise
On screen: Exercise. D1 calculator, Plan A. Lean month burden. Daily rate for 10%. Nominal and effective APR.

To recap. Affordability is measured against the instalment, by tier, and on lean month income as well as the average. The 10 per cent threshold is a policy line that must be evidenced. The deposit screens as well as reduces exposure, and the implied APR must be stated on a declared convention.

Your exercise uses the D1 price plan and APR calculator. Open Plan A, the illustrative Tier 2 plan. Change the deposit to eight thousand and the tenor to thirty months. Record the new instalment, the burden on average and on lean month income, and both APR figures. Then use the solver block to find the daily rate that meets the 10 per cent threshold, and note what that rate does to the PAYGo premium.
