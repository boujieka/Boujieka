# Module 13. RBF, subsidies and affordability

Duration: about 8 minutes. Book: Chapter 13. Model sheets: Inputs (RBF block), RBF_Engine, Vintage_Input, Consumer_Risk, Unit_Economics, Sensitivity, Checks. Templates and tools: D1 Price plan and APR calculator, D2 Unit economics calculator.

## Learning objectives
1. Distinguish the four results a PAYGo subsidy can pay for and the incentive each one creates.
2. Use the four RBF designs in the workbook and read what the default model says about RBF value.
3. Measure an affordability gap and compare the ways of closing it, treating payment burden as a credit variable.

## Scene 1. Two decisions, one question
On screen: Title card. Programme manager and investor, side by side. "How should subsidies be used when the product is credit?"

This module serves two people. The first is a programme manager with public or philanthropic money, who must decide what to pay for, how to verify it, and how to stop the payment rewarding the wrong behaviour. The second is an investor or lender, who must decide how much weight to put on subsidy income when sizing returns and debt capacity.

Both decisions come down to how subsidies should be used in a business whose real product is consumer credit.

A subsidy to a PAYGo, or pay as you go, company does not buy a grid asset. It buys the start of a two to four year relationship with a household on irregular income. The benefit arrives only if the household keeps paying, or finishes paying and owns the device. That gap between what is paid for and what is wanted is the central design problem.

## Scene 2. What is being bought
On screen: Four steps moving away from the sale. Sale, connection, repayment, ownership.

Under results based financing, or RBF, the funder pays a fixed amount per verified result after the event. The company pre finances the activity and carries the execution risk. So everything depends on how the result is defined.

There are four candidates, each further from the sale. A sale is easy to verify, but says nothing about whether the customer will pay. A connection requires the system to be installed and working. SEforALL's Universal Energy Facility is described as paying per verified connection, though that is secondary reporting and its own documents must be read.

Repayment is the first result that carries credit information. Ownership is the closest to the public interest, and the slowest to observe. On a 24 month contract, measured at twice the tenor, the first reading arrives four years after the first sale.

## Scene 3. Four designs in the workbook
On screen: RBF_Engine sheet. Mode 1 sales based, mode 2 repayment linked, mode 3 ownership linked, mode 4 hybrid.

The RBF_Engine sheet of the AEF SHS PAYGo model holds four designs. RBF is set in dollars and recognised below gross profit when the cash arrives.

Take an illustration of twenty five dollars per verified Tier 2 unit, at one hundred and thirty local currency units to the dollar. Under mode 1 the company receives twenty five dollars, or three thousand two hundred and fifty local currency units.

Under mode 2, suppose the target is 80 per cent repaid at verification and the cohort has repaid 68 per cent. The payout factor is 68 divided by 80, which is 85 per cent. The company receives twenty one dollars and twenty five cents. Had the cohort repaid 84 per cent, the factor would be capped at 100 per cent.

Under mode 3, suppose forty dollars per owner at month 48, with 55 per cent owning. That is twenty two dollars per unit sold. Discounted at 20 per cent a year over four years, it is worth only about ten dollars and sixty one cents at the date of sale. A hybrid weighted 50, 30 and 20 per cent pays about twenty three dollars and twenty eight cents, most of it early.

## Scene 4. Sales based RBF can reward bad credit
On screen: Two bars. Company A, 1,000 units, 80 per cent repaid. Company B, 1,300 units, 60 per cent repaid.

A sales based payment subsidises customer acquisition. The trouble is that the cheapest way to raise verified sales is to relax underwriting.

Consider two companies in the same programme. Company A underwrites tightly, sells 1,000 units and its cohort repays 80 per cent by verification. Company B underwrites loosely, sells 1,300 units and repays 60 per cent. Under sales based RBF, A receives twenty five thousand dollars and B receives thirty two thousand five hundred. The programme pays 30 per cent more to the company whose customers fall behind more often.

Under repayment linked RBF with an 80 per cent target, A still receives twenty five thousand dollars. B receives twenty four thousand three hundred and seventy five. The ranking reverses, but only modestly.

## Scene 5. Repayment, ownership and hybrids
On screen: Three short panels. Repayment: definitions. Ownership: timing and evidence. Hybrid: weights total 100 per cent.

Repayment linked RBF lines the programme up with the lender. Both now want cohorts that pay. The data already sit on the lockout platform, but the definitions must be tight. They must say whether deposits count, whether written off accounts stay in the denominator, and whether the rate is measured by cohort at a fixed age or on the portfolio at a calendar date. PAYGo PERFORM is the natural reference, subject to alignment with its current published documents.

Ownership linked RBF has two weaknesses. The company waits years for the cash, and ownership is hard to prove, because an unlock can follow a settlement or a goodwill gesture. The workbook is strict. Mode 3 pays zero until validated ownership data sit in Vintage_Input and the evidence switch is set to 1.

A hybrid pays some cash early and holds some back. The weights are a policy choice. The Checks sheet only confirms they total 100 per cent.

## Scene 6. What the model says RBF is worth
On screen: Sensitivity sheet. Base investor IRR 46.4 per cent. RBF off 44.7 per cent. Repayment linked 46.4 per cent. Zero breach months.

At default inputs, switching RBF off lowers the investor internal rate of return, or IRR, from 46.4 per cent to 44.7 per cent. That is a fall of 1.7 percentage points, with no covenant breach months either way. RBF helps, but it does not decide the case. A case that needs RBF to clear the hurdle is a bet on renewal.

Switching from sales based to repayment linked RBF leaves the IRR unchanged at 46.4 per cent. At Base credit quality the payout factor sits at or near its cap, so the change costs a good performer nothing. The design bites only where credit is weak.

## Scene 7. Paying the supplier or the customer
On screen: Supplier subsidy versus consumer subsidy. Demand side voucher: eligibility, duplication, reconciliation.

RBF paid to the company is a supplier subsidy. A twenty five dollar payment does not guarantee a twenty five dollar lower price, because the company may use it for acquisition or margin.

A consumer subsidy shows up in the price. It lowers the cash price or the instalment, and so lowers the payment burden directly. A demand side voucher routes that subsidy through the household. It keeps suppliers competing and targets more precisely, at an administrative cost. It must also fit the credit contract. A voucher that covers the deposit removes the one signal of willingness to pay. One that covers instalments makes the programme a co lender, and its terms must say what happens on default.

## Scene 8. Measuring an affordability gap
On screen: Consumer_Risk sheet. Income 30,000. Instalment 3,900. Burden 13.0 per cent. Threshold 10 per cent. Gap 900 a month.

The Consumer_Risk sheet compares each tier's instalment with an illustrative household income and flags any tier above a threshold, 10 per cent by default.

Take an illustration. A household earns thirty thousand local currency units a month. A Tier 2 instalment is three thousand nine hundred a month over 24 months, a burden of 13.0 per cent. To reach 10 per cent the instalment must fall to three thousand, a cut of nine hundred a month, or 23.1 per cent.

Extending the tenor lets default hazard act on more months. Raising the deposit excludes the households with least cash. You can also redesign the product, or buy the price down. At 50 per cent a year, nine hundred a month for 24 months has a present value of about thirteen thousand four hundred and ninety local currency units, well below the nominal twenty one thousand six hundred. Compare subsidy cost per completed contract, not per sale. And treat payment burden as a credit variable. It is available at origination, long before PAR30, the share of the book more than 30 days past due, starts to move.

## Scene 9. Recap and exercise
On screen: Recap. Define the result. Model with and without RBF. Ownership needs evidence. Burden predicts loss. Exercise: Downside, mode 1 against mode 2.

A subsidy is only as good as the result it pays for, and sales based payments can reward loose underwriting. Repayment linked RBF costs good performers nothing in the default model and redirects money towards credit discipline. Ownership income needs validated data before it appears in any case. Payment burden is a leading indicator of credit loss and belongs in the credit analysis.

Your exercise uses the workbook. On a copy, switch the scenario on Inputs to Downside, then run it once with RBF mode 1 and once with mode 2. Read the RBF line on RBF_Engine and the investor IRR on Investment_Summary for each. The difference between the two payouts is your measure of how much the Downside weakens credit quality.
