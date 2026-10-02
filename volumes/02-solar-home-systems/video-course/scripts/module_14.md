# Module 14. Stress testing

Duration: about 8 minutes. Book: Chapter 14. Model sheets: Inputs, Scenarios, Sensitivity, Covenants, Credit_Portfolio, Valuation, Investment_Summary, Dashboard. Templates and tools: D4 Receivables financing calculator, D6 Investor returns calculator, T05 Lender KPI report.

## Learning objectives
1. Design a Downside that moves credit, currency, volume, hardware cost and funding together.
2. Read the default scenario and sensitivity results, and judge which levers destroy equity and which hurt the lender.
3. Run a reverse stress on a covenant and on exit equity, and a funding drought, and read MOIC, peak equity and breach months together.

## Scene 1. What can kill the company
On screen: Title card. "Base case: what management hopes. Stress test: how far away failure is."

This module asks a blunt question, which is what can kill the company. A base case tells a committee what management hopes will happen. A stress test tells it which plausible combination of events would leave the company unable to pay its lenders, unable to raise its next round, or worth nothing at exit.

The committee does not need to believe the stress will happen. It needs to know how far away it is, and what can be done before the company gets there.

## Scene 2. How PAYGo companies fail
On screen: Chain diagram. Collections fall, borrowing base shrinks, covenants approach limits, facility at risk.

A PAYGo, or pay as you go, company usually runs out of cash while its income statement still looks acceptable. Hardware revenue is booked on the day of sale. The cash arrives over 12 to 48 months.

The book is funded partly by borrowing against eligible receivables. So when credit weakens, three things happen at once. Collections fall. The borrowing base shrinks, because more of the book ages beyond the eligibility cut off. And covenants on collection rate, receivables at risk and days past due, or DPD, move towards their limits. The lender's protection is triggered at the moment the company most needs the facility.

That is why stress testing here is mostly about credit and liquidity, with currency as the main amplifier. Volume, which worries founders most, is usually the least dangerous of the major variables.

## Scene 3. Designing a stress
On screen: Scenarios sheet. Levers for Base, Downside, Severe: hazard 1.00, 1.30, 1.75. Collection 1.00, 0.97, 0.92. Volume 1.00, 0.90, 0.75. Hardware 1.00, 1.05, 1.10. Depreciation 5, 12, 25 per cent a year.

The commonest mistake is to move one variable and call it a Downside. Real stress arrives in combinations. Depreciation raises the local cost of dollar priced hardware and often comes with inflation that squeezes household incomes. Squeezed households pay less reliably, and lenders grow cautious.

So cover five channels: credit, currency, volume, hardware cost and funding. The Scenarios sheet scales the first four. The Downside raises default hazard by 30 per cent, adds seven points of depreciation a year and trims volume by 10 per cent. The Severe case raises hazard by 75 per cent and has the currency losing a fifth of its value each year.

Two things are missing from the levers. The scenarios keep the facility in place, and they keep the default pricing response of a 5 per cent annual price increase and 50 per cent pass through of exchange rate moves. Test both separately.

## Scene 4. The three scenarios at default inputs
On screen: Table. Base: peak equity 10.0 million dollars, EBITDA margin 21.6 per cent, IRR 46.4 per cent, multiple 6.7 times, 0 breach months. Downside: 10.0, 7.3 per cent, minus 22.9 per cent, 0.3 times, 44. Severe: 46.6, minus 18.4 per cent, total loss, 0.0 times, 48.

At default inputs, with an investor putting in four million dollars, the Base gives an investor internal rate of return, or IRR, of 46.4 per cent and a multiple of 6.7 times, with no covenant breaches.

The Downside is the instructive row. Peak equity does not move from ten million dollars. Yet the IRR is minus 22.9 per cent, the multiple is 0.3 times, so the investor loses about 70 per cent of its money. And the company is in breach of at least one covenant for 44 of 60 months. A cash survival test alone would miss both facts.

The Severe case adds a funding crisis. Peak equity rises to forty six point six million dollars, because the workbook tops up equity automatically to fill the gap. No shareholder group would supply thirty six point six million dollars more than Base. Read it as failure or a distressed sale.

## Scene 5. One lever at a time
On screen: Sensitivity sheet. Depreciation 20 per cent: minus 16.0 per cent. No price increase: 7.9 per cent. Hazard 1.5 times: 36.1 per cent, 40 breach months. Volume 20 per cent lower: 37.8 per cent, 0. Tier 4 and 5 mix: 66.6 per cent.

The Sensitivity sheet moves one assumption at a time from Base. Five readings follow.

Currency and pricing destroy equity. Depreciation of 20 per cent a year takes the IRR to minus 16.0 per cent. Removing the 5 per cent annual price increase on new contracts takes it from 46.4 to 7.9 per cent. The price increase is how the company passes on dollar cost inflation.

Credit hurts the lender more than the equity. A 50 per cent higher default hazard leaves the investor at 36.1 per cent, but puts the company in breach for 40 months. Volume is the least dangerous lever. A 20 per cent fall gives 37.8 per cent and no breaches.

Structure barely moves returns. Securitisation adds 0.1 points. And the higher Tier 4 and 5 mix, at 66.6 per cent, is the most dangerous number in the table because it is the most attractive. It assumes larger systems repay at default parameters, without the cohort history to prove it.

## Scene 6. Reverse stress testing
On screen: Two calculations. Collection: 73.3 to 70 per cent, a fall of about 4.5 per cent. Equity: exit at 6.0 times EBITDA, net debt 4.0 billion, threshold EBITDA 0.667 billion.

A forward stress asks what happens under a scenario. A reverse stress asks what scenario causes a given failure. It turns a scenario into a distance.

The default covenant needs a trailing three month collection rate of at least 70 per cent. In Base the annual rate falls from 84.5 per cent in Year 1 to 73.3 per cent in Year 5. A first pass says a uniform fall of about 4.5 per cent brings Year 5 to the limit. Then the workbook corrects you. With collections cut by 5 per cent, the company is in breach for 27 months, longer than the annual rates suggest. Locate the threshold by arithmetic, then confirm it in the workbook.

For equity, take an illustration. Suppose the company exits at 6.0 times EBITDA, its earnings before interest, tax, depreciation and amortisation, with Year 5 EBITDA of one billion local currency units and net debt of four billion. Equity is two billion. It is wiped out when EBITDA falls to about six hundred and sixty seven million, a fall of a third. If net debt also rises to four point five billion, the threshold rises to seven hundred and fifty million, a fall of only a quarter.

## Scene 7. Funding drought
On screen: Inputs sheet, facility limit set to zero on a copy. Eligible receivables 4.0 billion times 70 per cent advance rate equals 2.8 billion, about 21.5 million dollars.

A funding drought tests what happens when the facility is not there. GOGLA is reported to put off grid solar investment at about two hundred and ninety nine million dollars in 2024, down about 30 per cent. That is secondary reporting, still to be checked against the primary document.

To run it, set the facility limit to zero or its start month beyond the horizon, on a copy. Peak equity then measures the cost. As an illustration, eligible receivables of four billion local currency units at a 70 per cent advance rate give a facility of two point eight billion, about twenty one point five million dollars at one hundred and thirty to the dollar.

Failures do happen. BBOXX LTD entered administration on 19 May 2025, and its latest filed accounts were for FY2022, according to the public register, with primary documents not yet reviewed. Filed accounts can be well over a year old by the time a failure is public.

## Scene 8. Reading total loss, and the SolaraPay stresses
On screen: Three figures to read together: multiple, peak equity, breach months. SolaraPay: calibrated Downside total loss, 40 breach months. Full FX indexation: 23.6 per cent.

IRR is a poor statistic in the tails. When exit equity is zero it cannot be computed, and the workbook reports a total loss. So read three figures together. The multiple says how much money comes back. Peak equity says how much had to go in. Breach months say how long the lenders were in control.

In the fictional SolaraPay case, the calibrated Downside is a total loss with 40 breach months, without any call for new cash. Full indexation of new prices to the exchange rate turns it into a 23.6 per cent IRR, though 38 breach months remain. Doubling the hazard on the untested Tiers 4 and 5 roughly halves the IRR, from 29.0 to 14.8 per cent.

## Scene 9. Recap and exercise
On screen: Recap. Move levers together. Pricing and currency destroy equity. Credit hurts the lender. Measure the distance. Exercise: reverse stress on the collection covenant.

A credible Downside moves credit, currency, volume and hardware cost together, and funding is tested on its own. In the default model, pricing and currency move returns more than any credit or volume assumption, while credit hits the lender hardest. Reverse stress turns scenarios into distances, and the multiple, peak equity and breach months must be read side by side.

Your exercise is a reverse stress. On a copy of the workbook, reduce the collection rate multiplier on Scenarios in small steps from 1.00, one change at a time. Record the multiplier at which the Covenants sheet first shows a breach month, and compare it with the first pass estimate of about 0.955. Then set the facility limit to zero and note the peak equity on Investment_Summary.
