# Module 9. Unit economics

Duration: about 8 minutes. Book: Chapter 9. Model sheets: Unit_Economics, Consumer_Risk, Products, Curves, Vintage_Dashboard, Investment_Summary. Templates and tools: D2 Unit economics calculator, D3 Repayment curve and cohort calibration, T01 Investment memo.

## Learning objectives
1. Build the expected lifetime cash flow of one PAYGo unit from its inflow and outflow lines.
2. Compute and interpret cash payback, unit IRR, unit NPV and LTV to CAC, and explain why LTV to CAC on its own misleads.
3. Read the SolaraPay unit table tier by tier and connect unit economics to overheads, growth and the cost of funding.

## Scene 1. A unit is not a sale
On screen: Title "A unit is a customer relationship". Three words: tenor, cash, probability.

This module supports one decision: whether each sale creates value once the cost of acquiring, equipping, financing and servicing the customer is set against the cash that customer will actually pay. If a single unit loses money, no amount of volume will rescue the company.

In a cash retailer, a unit is a sale, booked and collected on the same day. In a PAYGo, or pay as you go, company, a unit is a customer relationship that lasts the full tenor and sometimes longer. The income statement books the hardware margin on the day of sale. The cash arrives instalment by instalment, from a population that thins out each month as accounts lock out.

So unit economics is a cash exercise. The useful unit is the expected lifetime cash flow of one customer at origination. A unit is a probability weighted customer, not the median good payer, and the weights come from the cohort curves.

## Scene 2. The lines of the unit
On screen: Unit_Economics sheet. Inflows: customer cash, recoveries, RBF. Outflows: hardware, installation, warranty, CAC, servicing.

The Unit_Economics sheet of the AEF SHS PAYGo model, SHS standing for solar home system, sets out the unit for each tier. Inflows are the deposit plus expected instalments collected, net recoveries from repossessed and resold systems, and any RBF, or results based financing, payment attached to the unit. Outflows are hardware landed cost, installation, a warranty provision, CAC, the customer acquisition cost of commission plus marketing, and servicing.

Two disciplines apply. Every line is per unit sold, not per surviving account, so servicing is scaled to expected active months, which are fewer than the tenor. And expected loss and recoveries must come from the same curve. Take one from a sober source and the other from an optimistic one, and you build a unit that never existed.

## Scene 3. An illustrative unit
On screen: Illustrative unit build: deposit 3,000, instalments 24 times 1,500, expected loss 30 per cent, contribution 8,800 local currency units.

Take an illustrative mid tier system with a television, in a fictional local currency. The deposit is three thousand local currency units, followed by 24 monthly instalments of one thousand five hundred. The expected loss rate is 30 per cent of contractual instalments.

Contractual instalments total thirty six thousand. Thirty per cent of that is lost, so expected collections are twenty five thousand two hundred. Add the deposit, recoveries of one thousand two hundred and an RBF payment of one thousand, and expected inflows are thirty thousand four hundred.

Against that, hardware costs fourteen thousand, installation one thousand, warranty seven hundred, acquisition three thousand five hundred and servicing two thousand four hundred. Outflows total twenty one thousand six hundred. Lifetime contribution is eight thousand eight hundred local currency units, about 23 per cent of contract value. It is also the most flattering number in the analysis, because it is undiscounted.

## Scene 4. Timing the cash
On screen: Cumulative cash by half year: minus 16,200 at month 0, minus 1,900 at month 12, payback about month 14. Unit IRR about 48.8 per cent. NPV at 25 per cent about 3,280.

At month 0 the company receives the deposit and pays for hardware, installation, warranty and acquisition. Net cash is a loss of sixteen thousand two hundred. Collections then decline as the survival curve falls, and recoveries arrive in the second year.

Three measures follow. Cash payback is where cumulative cash turns positive. At month 12 the unit is still one thousand nine hundred short, and payback comes at roughly month 14. For a 24 month product that is acceptable but not generous.

Unit IRR, the internal rate of return, is about 48.8 per cent a year. Unit NPV, the net present value at a 25 per cent hurdle, is about three thousand two hundred and eighty. That is a little over a third of the undiscounted contribution, and the gap is the first reason to treat contribution with care.

## Scene 5. LTV to CAC and its pitfalls
On screen: LTV to CAC: 12,300 divided by 3,500 equals 3.5 times. Three weaknesses: undiscounted, before overheads, loss sensitive.

Lifetime value to customer acquisition cost, LTV to CAC, is the most quoted unit metric in pitch decks and the least reliable in credit papers. Here lifetime value is contribution plus CAC, twelve thousand three hundred, and the ratio is 3.5 times. Definitions vary, so ask which numerator and denominator were used.

The ratio has three weaknesses. It is undiscounted, so a 48 month unit and a 12 month unit can look alike. It is struck before overheads, so a ratio of 3 times can sit alongside a loss making company. And it is highly sensitive to the loss assumption.

Raise the expected loss from 30 to 40 per cent. Contribution drops to five thousand two hundred, a fall of 41 per cent, and the ratio falls to 2.5 times. Payback slips to about month 17, the unit IRR to about 28 per cent, and the NPV to about four hundred and eighty. A ten point error in the loss rate takes the unit from comfortably value creating to marginal.

## Scene 6. The SolaraPay unit table
On screen: Unit_Economics, SolaraPay calibrated, Tiers 1 to 5: expected loss, contribution, LTV to CAC, payback, unit IRR. Consumer_Risk burden flags on Tiers 2, 3 and 4.

SolaraPay is the book's fictional company, in the fictional Republic of Kivara, with 24 months of synthetic history. Tiers 1 to 3 are recalibrated to that history. Tiers 4 and 5 are new and keep default assumptions. Every tier has positive contribution. That is a minimum condition and no more.

Tier 2 is the weakest where it matters: the highest expected loss at 41.8 per cent, the lowest unit IRR at 37 per cent, and a 17 month payback on a 24 month tenor. Its payment burden, the instalment as a share of illustrative household income, is 13.0 per cent against a 10 per cent threshold on Consumer_Risk. Part of the loss is an affordability problem. Tier 2 is also 40 per cent of the planned mix, so its redesign should be a condition of investment.

Tier 1 has the lowest LTV to CAC, 2.4 times, and a contribution of one thousand and ninety two shillings, yet a 66 per cent IRR and a nine month payback. It returns a small investment quickly but creates little value, so judge it as an upgrade funnel.

Tiers 4 and 5 look best on paper, at 11.0 and 14.9 times. They are the least proven. Their hazards are untested, and their recoveries assume repossession rates of 60 and 70 per cent against an observed loss given default proxy of about 99 per cent. Doubling their hazards cuts the investor IRR from 29.0 to 14.8 per cent. Hence the pilot cap.

## Scene 7. From the unit to the company
On screen: Three bridges: overheads, growth, cost of funding. Blended funding cost 18.7 per cent.

Three bridges connect the unit to the company. The first is overheads. In the illustration, central costs of six hundred million local currency units a year need about 68,200 units just to cover them. Under the 40 per cent loss case, that rises to about 115,400.

The second is growth. Each unit needs sixteen thousand two hundred at origination and pays back only around month 14, so doubling sales doubles the investment before earlier units repay.

The third is funding. With 70 per cent of each receivable funded at 16 per cent and 30 per cent by equity expecting 25 per cent, the blended cost is 18.7 per cent. The unit at about 49 per cent clears it easily. At about 28 per cent, little is left for overheads.

At SolaraPay every tier contributes, yet the calibrated Base margin on earnings before interest, tax, depreciation and amortisation is minus 35.2 per cent in Year 1 and turns positive only in Year 3. The units are profitable. The company becomes so only once the book can absorb its overheads and its financing.

## Scene 8. Recap and exercise
On screen: Recap: cash not sales, read metrics together, Tier 2 redesign, Tiers 4 and 5 pilot. Exercise: D2 Unit economics calculator.

A PAYGo unit is a probability weighted customer, measured in cash over its whole life. Read contribution, payback, unit IRR, unit NPV and payment burden together, and never accept LTV to CAC alone. At SolaraPay, Tier 2 needs redesign, and Tiers 4 and 5 stay a pilot until twelve months of cohort data sit within 10 per cent of plan.

Open the D2 unit economics calculator on its default Tier 2 sale and note contribution, payback month and unit IRR. Raise the default hazard until the expected loss rate is ten points higher, and record the same figures. Then write two sentences for a memo on whether the unit still clears a blended funding cost of 18.7 per cent.
