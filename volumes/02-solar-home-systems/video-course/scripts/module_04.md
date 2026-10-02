# Module 4. Product and price plan design

Duration: about 9 minutes. Book: Chapter 4. Model sheets: Products, Consumer_Risk, Unit_Economics, Sensitivity, Scenarios, Vintage_Dashboard. Templates and tools: D1 Price plan and APR calculator, D2 Unit economics calculator, D3 Repayment curve and cohort calibration.

## Learning objectives
1. Derive the instalment, contract value, premium and amount financed from the four price plan inputs, and explain how the cash price moves revenue and APR.
2. Compute the expected collected share of a plan from the hazard, the collection rate and the tenor, and use it to compare tenors.
3. Assess product mix, upgrades and warranty, and decide how to treat untested tiers.

## Scene 1. The design decision
On screen: Title. "Which price plan maximises value without destroying repayment?"

This module supports one decision: which price plan maximises value without destroying repayment.

A price plan has five components. The cash price, the deposit, the daily rate, the tenor, and the PAYGo, or pay as you go, premium that results. Each moves revenue, exposure, affordability and default risk at once.

The plan that maximises contract value is rarely the one that maximises cash collected.

## Scene 2. The components
On screen: Products sheet. Four inputs: cash price, deposit, daily rate, tenor. Derived: instalment, contract value, premium, amount financed, implied APR.

The Products sheet takes four inputs for each tier: cash price, deposit, daily rate and tenor. The instalment, contract value and premium are derived from them.

The cash price matters more than it looks. Hardware revenue equals the cash price and is booked at sale. The premium is spread over the tenor as financing income. So a high cash price with a low premium brings revenue forward, without changing what the customer pays. It also lowers the implied annual percentage rate, or APR. Check that the cash price is one at which the company really sells for cash.

A common design error is to set the daily rate from a target contract value, and only then ask whether the customer can pay.

## Scene 3. Tenor and deposit
On screen: Longer tenor: lower instalment, more exposure, more months at risk. Higher deposit: screening, lower conversion. Deposit doubled: amount financed down 11.1%.

Two trade offs dominate design.

A longer tenor lowers the instalment, and so the payment burden. It also raises exposure and funding per unit. With a monthly hazard, every extra month is another month in which the account can stop.

A higher deposit screens customers and lowers exposure. In the illustrative Tier 2 plan, doubling the deposit from four thousand to eight thousand local currency units cuts the amount financed by 11.1 per cent. It also lifts the deposit from 22.2 to 44.4 per cent of average monthly income, and from 33.3 to 66.7 per cent of a lean month. Conversion will fall, and only tested cohorts show whether better repayment compensates.

A higher premium lifts contract value, but also the burden and the APR. If the hazard rises with it, part of the extra premium is never collected.

## Scene 4. How collection falls with tenor
On screen: Survival 0.974 to the power of age. Month 6: 0.854. Month 12: 0.729. Month 18: 0.622. Month 24: 0.531. Expected collected share: 18 months 69.2%, 24 months 64.4%.

With a monthly hazard of 2.6 per cent, the share of Tier 2 accounts still paying is 0.974 raised to the power of the account's age in months.

At month six, about 85 per cent are still paying. At month twelve, about 73 per cent. At month twenty four, about 53 per cent.

The expected share of scheduled instalments collected is the collection rate on paying accounts, times the average survival over the tenor. With a collection rate of 88 per cent, an eighteen month plan collects an expected 69.2 per cent of its instalments. A twenty four month plan collects 64.4 per cent.

So moving from eighteen to twenty four months costs 4.8 percentage points of expected collection. The last six months of the longer plan carry 25 per cent of the scheduled instalments, but only 19.4 per cent of the expected collections. The company is lending into months in which many customers have already stopped paying.

## Scene 5. No easy way out through tenor
On screen: Same expected cash. 18 months: instalment 2,718, burden 15.1%. 30 months: instalment 1,879, burden 10.4%.

The same arithmetic shows what a shorter tenor costs in affordability. The Tier 2 plan expects to collect thirty three thousand eight hundred and thirty two over twenty four months. To collect the same over eighteen months, the instalment must rise to about two thousand seven hundred and eighteen. On average income of eighteen thousand, the burden rises from 12.2 to 15.1 per cent.

That is unlikely to leave the hazard unchanged. Suppose, for illustration, that it rises to 3.38 per cent, the level SolaraPay's Tier 2 was recalibrated to. The eighteen month plan then collects about thirty one thousand five hundred and fifty two. That is less than the twenty four month plan.

Lengthening the tenor fails the other way. Over thirty months at the default hazard, the expected collected share is 60.0 per cent. The instalment needed is about one thousand eight hundred and seventy nine, a burden of 10.4 per cent. Still above the threshold, and with six more months of exposure.

Tenor alone cannot reconcile this product with this customer. The workbook holds the hazard constant across tenors, so you must decide whether a change in tenor or burden changes the hazard, and run that judgement through Products and Scenarios.

## Scene 6. Upgrades, add ons and warranty
On screen: Repeat customers: lowest risk. Watch rolled balances. Warranty: a fault becomes a credit loss. Battery life against tenor.

A customer who completes a plan is the lowest risk prospect the company will ever have. But an upgrade that rolls an unpaid balance into a new, larger contract can extend the tenor and hide arrears. Ask for upgrade cohorts to be reported separately.

Warranty is part of the price plan. A customer whose system fails stops paying, so a slow warranty turns a hardware fault into a credit loss. For Tiers 4 and 5, check that battery life and warranty cover the thirty six or forty eight month tenor, and that supplier warranties match the warranty given to customers.

## Scene 7. Product mix and untested tiers
On screen: Tier 4 and 5 mix 20% and 10%: IRR 46.4% to 66.6%. SolaraPay Tier 4 and 5 hazard doubled: IRR 29.0% to 14.8%, multiple 3.6 to 2.0 times, 38 breach months.

Higher tiers look better per unit. In the workbook they carry lower hazards, larger contracts and higher advance rates, 75 per cent for Tiers 4 and 5 against 50 per cent for Tier 1. Raising the Tier 4 and 5 mix to 20 and 10 per cent lifts the default investor internal rate of return, or IRR, from 46.4 to 66.6 per cent, with no covenant breach.

The difficulty is that those assumptions are, for most companies, untested. Shifting the mix towards them is the largest credit bet in the plan, made on the least evidence.

SolaraPay is launching Tier 4 at three hundred and ninety thousand shillings and Tier 5 at eight hundred and forty five thousand. Calibrated unit economics give them the best ratios of lifetime value to acquisition cost in the range, 11.0 and 14.9 times. But they have no history. Doubling their hazard cuts the investor IRR in the calibrated case from 29.0 to 14.8 per cent. The multiple falls from 3.6 to 2.0 times, with 38 months in covenant breach. The case caps both tiers as a pilot, released only after twelve months of cohort data within 10 per cent of plan.

## Scene 8. What SolaraPay's Tier 2 shows
On screen: SolaraPay Tier 2. Expected loss 41.8%. Unit IRR 37%. Payback 17 months. 40% of mix. Burden 13.0%. Calibrated collected share 58.2%.

Tier 2 is SolaraPay's weakest product on the measures a lender cares about most. Its expected loss is 41.8 per cent, the highest in the range. Its unit IRR is 37 per cent, the lowest. It pays back in seventeen months on a twenty four month plan. Its lifetime contribution of seven thousand five hundred and twenty four shillings is 19.3 per cent of its cash price. And it is the largest line in the plan, at 40 per cent of the mix.

Its burden is 13.0 per cent, above the threshold. Calibration raised its hazard from 2.60 to 3.38 per cent and cut its collection rate from 88 to 87 per cent. On those parameters, the expected collected share over twenty four months falls from 64.4 to 58.2 per cent.

The response is redesign, not withdrawal. Bring the instalment within the threshold, through a smaller product, a lower premium, a higher deposit for some segments or a different target customer. Then test the redesign on new cohorts before scaling it. New prices also need indexing to the exchange rate. In the default sensitivities, freezing prices on new contracts cuts the Base investor IRR from 46.4 to 7.9 per cent.

## Scene 9. Recap and exercise
On screen: Exercise. Tier 1 defaults: hazard 3.5%, collection 88%, tenor 12 months. Expected collected share. Compare with Unit_Economics and D2.

To recap. The four price plan inputs move revenue, exposure, affordability and risk together. Expected collection falls with tenor, and neither a shorter nor a longer tenor alone fixes an unaffordable plan. Untested tiers deserve a pilot cap and a doubled hazard stress.

Your exercise applies the tenor mechanics to Tier 1. Use the default monthly hazard of 3.5 per cent and the collection rate of 88 per cent. Compute the expected collected share over a twelve month tenor, then over eighteen months. Check your answers in the D3 repayment curve tool or the D2 unit economics calculator. Then decide, in one paragraph, whether a longer Tier 1 tenor would be worth its extra exposure.
