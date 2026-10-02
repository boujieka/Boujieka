# About the Decision Tools

The Volume 2 Decision Tools are six compact calculators, each built to answer one question that comes up again and again in PAYGo finance. They sit between the book and the full model. The book explains the reasoning; the AEF SHS PAYGo model integrates everything over five years; the tools give a fast, transparent answer to a single question, in a form that can be shown on a screen in a credit committee and checked by hand.

| No. | Tool | Question it answers | Book |
|---|---|---|---|
| D1 | Price plan and APR calculator | Is this price plan affordable, and what rate does it imply? | Chapters 2, 3, 4 |
| D2 | Unit economics calculator | Does each sale create value, and when does it pay back? | Chapters 1, 6, 9 |
| D3 | Repayment curve and cohort calibration | Which credit assumptions does the company's own history support? | Chapters 6, 16 |
| D4 | Receivables financing calculator | How much equity and debt does a sales plan consume? | Chapters 10, 11 |
| D5 | Investment screening scorecard | Is this company worth a full diligence? | Chapters 15, 16 |
| D6 | Investor returns calculator | What does this entry price imply in US dollars? | Chapters 15, 16 |

## Conventions

The tools follow the colour code of the model: blue figures on a cream background are inputs, black figures are formulas. Every sheet opens with a guide, prints with the sheet name and "Page x of y" in the footer, and avoids array formulas, so that the results are the same in any spreadsheet program. The default inputs are not arbitrary: each tool opens on a worked example from the book or from the fictional SolaraPay case, so that a user can check the tool against a published figure before trusting it with company data.

# The tools one by one

## D1 Price plan and APR calculator

Five price plans side by side. From the cash price, deposit, daily rate and tenor, the tool computes the instalment, the total contract value, the PAYGo premium, the implied monthly rate, the nominal APR, the effective annual rate and the flat rate, and sets the instalment against average and lean month household income. A solver block returns the daily rate that meets the payment burden threshold, the daily rate for a target APR, the tenor that would bring the instalment within the threshold at the same monthly rate (or "Not reachable" when no tenor can), and the reduction in amount financed that would do so. Plan A is the illustrative Tier 2 plan of Chapters 1 and 2 (monthly rate 3.28%, nominal APR 39.3%, effective rate 47.3%); Plans B to E are the model's default Tiers 1 to 4.

## D2 Unit economics calculator

The expected cash flow of one sale, month by month for sixty months: collections from the survival curve, deposit, recoveries after the repossession lag, servicing, payment fees, RBF and the day one outlay. The results sheet gives the expected loss rate, lifetime contribution, LTV to CAC, cash payback month, peak funding per unit, unit IRR and unit NPV, and a closed form check that must read zero difference. A sensitivity grid shows contribution across default hazard and collection rate multipliers. The tier dashboard compares the five default tiers in closed form, with LTV to CAC and the months of collections needed to recover the day one outlay. The default inputs reproduce the Tier 2 sale of Chapter 1: collections of LCY 33,832, payback in month 14 and lifetime cash of LCY 11,832.

## D3 Repayment curve and cohort calibration

The curve sheet draws survival and cumulative repayment by account age from a hazard, a collection rate and a tenor. The calibration sheet searches a grid of 151 hazards and 18 collection rates for the pair that best fits observed cumulative repayment at M3, M6, M12 and M18, reports the fit error at each checkpoint, and warns when the best fit sits at the edge of the grid. Loaded with the average observed Tier 2 cohorts of the SolaraPay case, it returns a monthly hazard of 3.45% and a collection rate of 87%, within half a point of each observation; the case itself used 3.38% and 87%, obtained by raising the plan hazard by 30%. The portfolio effect sheet shows how the same customers produce a portfolio collection rate of 64.4%, 68.3% and 71.6% at zero, 5% and 10% monthly growth, the figures of Chapter 6.

## D4 Receivables financing calculator

A sixty month funding path for a sales plan. Each month's cohort is followed through its life in a cohort matrix; collections, deposits, the day one outlay and central costs give the cumulative cash position; the facility advances against the carrying amount of paying accounts from the month it becomes available, up to its limit; equity fills the rest. With the default Tier 2 product, the volumes of Chapter 10, a 70% advance rate, a facility available from month 7 and the model's central costs, the plan needs at most LCY 1,797m of funding, of which the facility carries up to LCY 1,054m and equity up to LCY 851m (about USD 6.6m), with peak equity in month 40. Setting central costs to zero shows the book alone: the facility then carries almost all of it, because the outlay net of deposit is below 70% of the amount financed. The currency sheet computes the depreciation at which dollar debt costs as much as a local currency facility.

## D5 Investment screening scorecard

Twelve criteria rated green, amber or red against editable thresholds, with weights: history, reconciliation, cohort gap to plan, PAR30, collection rate, unit contribution, LTV to CAC, payment burden, hard currency funding, runway, licence position and credit independence. Three are kill criteria. A blank criterion is reported as not assessed, never scored. The verdict reads Decline when a kill criterion fails, Incomplete while criteria are missing, and otherwise Proceed to diligence, Proceed with conditions or Decline according to the weighted score. With the SolaraPay values the case reports, the screen reads "Incomplete: 4 criteria not assessed; provisional score 64%". The thresholds are the author's suggested defaults and should be replaced by the fund's own policy.

## D6 Investor returns calculator

From the ticket, the pre money valuation, the exit year and the exit case in local currency, the tool computes the stake, exit equity in local currency and in dollars after depreciation, investor proceeds, the multiple and the IRR, including follow on equity calls funded pro rata. It solves for the highest pre money valuation that meets a target IRR and tabulates the IRR across exit multiples and depreciation rates. The default inputs reproduce the SolaraPay calibrated Base: a 3.57x multiple and a 29.0% IRR in dollars.

# Verification

Every formula in the six tools was evaluated outside Excel with no errors, and the key outputs were recomputed independently and compared.

| Tool | Check | Result |
|---|---|---|
| D1 | Monthly rate, nominal APR, effective rate and lean month burden for all five plans | Identical to independent computation |
| D2 | Collections, contribution, payback month, unit IRR and unit NPV for the Chapter 1 sale | Identical; payback month 14 |
| D3 | Best fit hazard and collection rate on the SolaraPay Tier 2 cohorts; portfolio effect | Grid search identical (3.45%, 87%); 64.4%, 68.3%, 71.6% |
| D4 | Peak funding need, peak facility and peak equity from a separate month by month simulation | Identical |
| D5 | Ratings and verdict on the case values | As described above |
| D6 | Multiple and IRR for the SolaraPay case | 3.57x and 29.0% |

A full test in Microsoft Excel, including charts and printing, is part of the v1.0 release cycle and has not yet been done.

## Limits of the tools

The tools simplify on purpose. They use a constant monthly hazard, monthly averages without seasonality, a single product in D2 and D4, and no tax or interest in D4. The scorecard thresholds are judgement, not sector standards. For an investment decision, the integrated model, the company's own data and professional advice remain necessary. Nothing in these tools is investment, legal, tax or accounting advice.
