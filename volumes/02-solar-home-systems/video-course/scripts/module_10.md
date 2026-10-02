# Module 10. Working capital, inventory and FX

Duration: about 8 minutes. Book: Chapter 10. Model sheets: Inputs, Scenarios, Products, FS, Annual, Credit_Portfolio, Investment_Summary, Sensitivity. Templates and tools: D4 Receivables financing calculator, T07 Borrowing base and term sheet, T01 Investment memo.

## Learning objectives
1. Explain why the receivables book, not fixed assets, is the main investment of a PAYGo company, and estimate how it grows with sales.
2. Quantify the three effects of a local currency depreciation and the role of FX pass through and price indexation.
3. Trace how the model builds the funding requirement from cash before facility, the borrowing base and the equity top up, and read the SolaraPay currency stress cases.

## Scene 1. The book is the investment
On screen: Title "The receivables book is the main investment". Income statement versus cash flow statement, side by side.

This module supports the decision that most often goes wrong in PAYGo, or pay as you go, solar: how much cash a growth plan will consume before it returns any, and in which currency.

A PAYGo company has few fixed assets. Its main investment is the receivables book. The cash price less the deposit is, in substance, a loan to the customer.

The income statement hides this, because hardware revenue is booked on the day of sale. The cash flow statement shows the opposite: more sales mean a larger increase in receivables, and operating cash flow falls as growth accelerates. A board that reads only the first will approve a plan the balance sheet cannot carry.

## Scene 2. An illustrative receivables build
On screen: Table, Years 1 to 5: units sold 10,000 to 50,000, year end receivables 180 to 1,200 million local currency units, increase in receivables peaking at 360 million in Year 4.

Take an illustrative product with a cash price of twenty seven thousand local currency units, a deposit of three thousand and a 24 month tenor. Each unit adds twenty four thousand of principal to the book, repaid in equal monthly amounts.

Sales rise from 10,000 units in Year 1 to 50,000 in Year 4, then stay flat. The increase in receivables grows every year while sales grow, reaching three hundred and sixty million local currency units in Year 4. In Year 5, when sales stop growing, the increase drops to ninety million and principal collected almost matches new lending. The company turns towards cash generation with unchanged unit economics.

As a rule of thumb, a fast growing 24 month book sits at roughly one year of origination. Longer tenors push the multiple higher, which is why a shift towards Tiers 4 and 5 raises the funding requirement before it raises cash generation.

## Scene 3. Who funds the book, and inventory
On screen: Effective advance: 75 per cent times 80 per cent equals 60 per cent. Inventory: three months cover, sixty days supplier credit.

Suppose a lender advances 75 per cent against eligible receivables, and 80 per cent of the book is eligible. The effective advance is 60 per cent. On a book of one billion one hundred and ten million local currency units, the facility funds at most six hundred and sixty six million. The other four hundred and forty four million must come from equity and retained cash. Equity scales with the book, not with the sales line, and rises again when credit slips and eligibility shrinks.

Inventory is smaller, but risky. At 50,000 units a year and a landed cost of fourteen thousand, purchases run at seven hundred million a year. Three months of cover ties up one hundred and seventy five million. Sixty days of supplier credit funds about one hundred and fifteen million. Inventory is bought ahead of sales and in hard currency, and supplier credit is the first funding to vanish in a stress. Ask to see the plan with supplier credit at zero.

## Scene 4. Two currencies, one balance sheet
On screen: Exchange rate moves from 130 to 156 per dollar. Three effects: hardware cost, book value in dollars, dollar debt.

Hardware and often term debt are in US dollars. Collections are in local currency, fixed for the whole tenor. When the dollar rises by 20 per cent, from 130 to 156, three things happen at once.

New hardware costs more. A unit landed at one hundred dollars rises from thirteen thousand to fifteen thousand six hundred local currency units.

The existing book loses value in dollars. One billion one hundred and ten million local currency units is worth about eight and a half million dollars at 130, and about seven point one million at 156. Signed contracts cannot be repriced.

Dollar debt gets dearer. A three million dollar term loan grows from three hundred and ninety million to four hundred and sixty eight million local currency units, a translation loss of seventy eight million through the income statement.

## Scene 5. FX pass through
On screen: FX pass through 50 per cent: price 27,000 to 29,700, margin 14,000 to 14,100 local currency units, but 108 to 90 dollars.

FX, or foreign exchange, pass through is the share of the currency move recovered by raising prices on new contracts. The model default is 50 per cent. With a 20 per cent rise in the dollar, the cash price of new contracts rises by 10 per cent, to twenty nine thousand seven hundred. The local currency margin per unit is roughly preserved, at about fourteen thousand. In dollars, it falls from about one hundred and eight to about ninety, a decline of about 16 per cent. And nothing has been done for the book already sold.

Higher pass through has a cost. Each price increase raises the instalment and the payment burden, and a tier already above the affordability threshold will feel it in arrears. Pass through is a pricing decision and a credit decision at once.

## Scene 6. What the sensitivities say
On screen: Sensitivity sheet, investor IRR and breach months: Base 46.4 per cent and 0; depreciation 20 per cent a year, minus 16.0 per cent and 41; no price increase 7.9 per cent and 35; hardware cost up 15 per cent, 29.5 per cent and 38; volume down 20 per cent, 37.8 per cent and 0.

The Sensitivity sheet runs one at a time tests from the default Base case, where the investor IRR, the internal rate of return, is 46.4 per cent with no covenant breaches. Cutting volume by a fifth costs about nine points of IRR and no breaches. Local currency depreciation of 20 per cent a year takes the IRR to minus 16.0 per cent, with the company in breach for 41 of 60 months. Freezing prices on new contracts takes it to 7.9 per cent. A 15 per cent rise in hardware cost gives 29.5 per cent and 38 breach months.

The ranking is the point. In this sector, currency and pricing are larger value drivers than volume. A Downside case that cuts volume but leaves the exchange rate on its Base path is testing the wrong thing.

## Scene 7. Cash before facility and the funding requirement
On screen: Formula in words: drawn balance is the lower of limit, borrowing base and the balance needed to hold minimum cash. Example: borrowing base 820, shortfall 40 million, equity top up.

The model builds the funding requirement in a fixed order. It first computes cash before facility, which is opening cash plus the month's operating, investing and term debt flows. It then draws the facility to hold cash at the minimum balance, within the lower of the limit and the borrowing base. Any shortfall is met by an automatic equity top up, and the cumulative top up is the funding requirement.

Say the facility starts the month at eight hundred million, minimum cash is one hundred million and cash before facility is forty million. The company wants to draw to eight hundred and sixty million. If the borrowing base has shrunk to eight hundred and twenty, cash closes at sixty million, and the forty million gap is an equity top up.

The facility limit is rarely the binding constraint. The borrowing base is, and it shrinks just when collections weaken. At default inputs, peak equity is ten million dollars in Base and forty six point six million in Severe.

## Scene 8. SolaraPay: currency decides
On screen: SolaraPay stress table: Calibrated Base, Downside, Downside with full FX indexation, Severe. IRR, multiple, breach months.

SolaraPay, the book's fictional company in the fictional Republic of Kivara, plans in shillings at 135 per dollar, with dollar hardware, a three million dollar term loan at 10 per cent and a proposed four point five billion shilling facility at 16 per cent. Its nine million dollars of initial equity is enough in the calibrated Base.

The calibrated Downside combines higher default hazard, lower collections, lower volume, dearer hardware and depreciation of 12 per cent a year. The investor loses everything. Change one input, so that new contract prices are fully indexed to the exchange rate, and the IRR recovers to 23.6 per cent with a multiple of 2.9 times.

Two cautions apply. Indexation rescues equity value, not covenants, with 38 breach months against 40. And it assumes customers accept higher prices without repaying worse. That is why the recommendation pairs indexation with an affordability redesign that keeps the instalment within 10 per cent of income.

## Scene 9. Recap and exercise
On screen: Recap: book grows with sales, three currency effects, borrowing base binds. Exercise: D4 Receivables financing calculator.

The receivables book absorbs cash in proportion to growth, and equity funds what the borrowing base will not. A weaker local currency raises hardware cost, shrinks the book in dollars and inflates dollar debt at once. Currency and pricing move returns more than volume, and for SolaraPay price indexation is the strongest Downside mitigant.

Open the D4 receivables financing calculator on its default Tier 2 plan and note peak funding, the facility's share and peak equity. Then, on its currency sheet, enter a 10 per cent dollar rate and a 16 per cent local rate, and read the depreciation at which the two cost the same. Compare it with the 12 per cent a year in the Downside, and write one line on which currency should fund the book.
