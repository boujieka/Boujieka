# Module 12. Securitisation and off balance sheet structures

Duration: about 8 minutes. Book: Chapter 12. Model sheets: Inputs, Products, Credit_Assumptions, Credit_Portfolio, Sensitivity, Credit_Input, Vintage_Input, Investment_Readiness. Templates and tools: T06 Loan tape and data request, T07 Borrowing base and term sheet, T02 Due diligence checklist.

## Learning objectives
1. Explain how a true sale to an SPV, tranching, overcollateralisation, excess spread and triggers protect noteholders, and why the servicer matters so much in PAYGo.
2. Compute credit enhancement and excess spread for an illustrative pool, and show how a small rise in losses removes the cushion.
3. Apply the readiness criteria, the cost logic and the accounting test to decide whether a securitisation is worth pursuing.

## Scene 1. What a securitisation changes
On screen: Diagram: originator sells receivables to an SPV in a true sale. SPV issues notes. Collections pay the notes.

This module supports a decision that is usually taken too early: when a securitisation is feasible, and whether it is worth the effort.

A receivables facility is a secured loan to the company. A securitisation separates the receivables from the company. The originator sells a pool of receivables to a special purpose vehicle, or SPV, in a true sale. The SPV funds the purchase by issuing notes, and collections on the pool pay those notes in order of priority.

Two legal properties carry the structure. A true sale takes the receivables out of the originator's estate, so its creditors cannot claim them in an insolvency. Bankruptcy remoteness means the SPV has no other business and limited permitted activities. Together they let investors analyse the pool rather than the company.

In PAYGo, or pay as you go, solar, that separation is never complete. Someone must run the payment platform, issue unlock codes, collect through mobile money and repossess devices. If the originator fails, the receivables still belong to the SPV, but someone has to keep collecting them.

## Scene 2. Tranching and credit enhancement
On screen: Illustrative pool of 5,000 million local currency units: senior 3,000 at 14 per cent, mezzanine 750 at 20 per cent, first loss 1,250 retained. Senior subordination 40 per cent.

The SPV issues notes in layers. Senior notes are paid first and absorb losses last. Mezzanine notes sit below them. A first loss tranche, usually kept by the originator, absorbs losses first.

Take an illustrative pool of five billion local currency units. Senior notes are three billion, or 60 per cent. Mezzanine notes are seven hundred and fifty million, or 15 per cent. The retained first loss is one billion two hundred and fifty million, or 25 per cent. The senior notes are protected by the 40 per cent of the pool that ranks below them. Where notes issued are less than the pool, the difference is overcollateralisation, which works the same way.

A first loss of that size fits PAYGo. In the calibrated SolaraPay case, lifetime expected losses run from about 27 to 42 per cent by tier. A senior tranche needs protection against a multiple of expected loss, not just the expected figure.

## Scene 3. Excess spread
On screen: One year snapshot: gross yield 2,250, losses 1,000, servicing 400, senior interest 420, mezzanine interest 150, other costs 50. Excess spread 230, or 4.6 per cent.

The second line of defence is excess spread: pool income less losses, fees and note interest. This one year snapshot is stylised.

A gross yield of 45 per cent on five billion brings in two billion two hundred and fifty million. Credit losses at 20 per cent take one billion. Servicing at 8 per cent takes four hundred million. Senior interest is four hundred and twenty million, mezzanine interest one hundred and fifty million, and trustee and other costs fifty million. Excess spread is two hundred and thirty million, or 4.6 per cent of the pool.

That cushion is thin. If losses rise from 20 to 25 per cent, they take a further two hundred and fifty million, and excess spread becomes a loss of twenty million. A five point rise in losses, well within the gap between a management plan and a calibrated case, wipes out the cushion and starts eating into the first loss. PAYGo pools yield a lot because they lose a lot, and the margin between the two is what a structurer protects.

## Scene 4. Triggers, servicer and data tape
On screen: Triggers: collection rate, PAR30, cumulative defaults, excess spread, servicer events. Backup servicer: cold or warm. T06 loan tape.

Triggers change the flow of cash when performance slips. The most important is early amortisation: the SPV stops buying new receivables, stops releasing excess spread and applies all collections to the senior notes. Typical metrics are the trailing collection rate, PAR30, the share of the pool more than 30 days past due, cumulative defaults by vintage, and servicer events. Levels must come from the company's own history. A collection trigger at a level the book has already breached, as SolaraPay's history shows for a 70 per cent covenant, would amortise the deal on day one.

The servicer is the originator, because only it runs the platform and the agents. A backup servicer is appointed at closing. A cold backup holds the contract and would need months. A warm backup receives regular data and could take over in weeks. The test is simple: a backup that cannot keep devices unlocked for paying customers cannot protect collections.

Investors analyse the pool through a loan level data tape. It must cover vintages that have reached full tenor, reconcile monthly to the audited accounts, and use stable definitions for the operational metrics, with repayment and ownership rates computed under the PAYGo PERFORM 2026 standard.

## Scene 5. Local currency issuance and the legal questions
On screen: Reported transactions, with caveats: Sun King, Kenya, 2023 and 2025. d.light, five facilities since 2020. Legal checklist: true sale, assignment, SPV tax, data, licences.

The main attraction is local currency funding at scale, which removes the translation risk of dollar debt. Local pension funds, insurers and banks may buy, if their rules allow.

The reported transactions give a sense of scale, from company and secondary reporting. Sun King is reported to have completed local currency securitisations in Kenya of about one hundred and thirty million dollars in May 2023, and about one hundred and fifty six million dollars, or twenty point one billion Kenyan shillings, in July 2025, arranged with Citi. d.light is reported to have five securitisation facilities since 2020 with about seven hundred and eighteen million dollars of purchasing capacity, which is capacity, not debt raised. These are large originators with long histories. They show the structure can work, not the terms a smaller company could expect.

Feasibility is first a legal question, to be confirmed with local counsel. Ask whether the law recognises a true sale of future instalments, whether receivables can be assigned without each customer's consent, whether the SPV is tax neutral, whether data and mobile money rules allow the transfer, and whether a lending licence is needed.

## Scene 6. Cost, size and the accounting
On screen: Fixed costs of one million dollars over a three year life: 20 million dollar deal keeps 0.33 points of a 2 point saving, 100 million dollar deal keeps 1.67 points. Off balance sheet: usually not.

Securitisations carry large fixed costs, from lawyers and arrangers to the tape review and months of management time. Suppose fixed costs are one million dollars and the notes have a three year average life. On a twenty million dollar deal that is about 1.67 per cent a year. On a hundred million dollar deal it is about 0.33 per cent. If the structure saves two points a year, the small deal keeps a third of a point, and the large one keeps 1.67 points. Size decides.

On accounting, under IFRS 9, the international standard for financial instruments, an originator derecognises receivables only if it transfers substantially all the risks and rewards, or gives up control. An originator that keeps the first loss usually keeps most of the risk. The receivables stay on its balance sheet and the notes become a financing liability. Assume off balance sheet treatment is wrong until the auditors confirm otherwise.

## Scene 7. What the model shows
On screen: Inputs: structure 1 warehouse line, structure 2 securitisation on balance sheet. Investor IRR: default 46.4 to 46.5 per cent. SolaraPay 29.0 to 29.1 per cent.

The companion workbook offers two facility structures on the Inputs sheet. Structure 1 is a warehouse line. Structure 2 is a securitisation or term asset backed issue, modelled on balance sheet, with its own rate, a haircut to advance rates and an upfront fee. True sale through an SPV is not modelled in version 0.8.

On that basis the option barely moves returns. For the default fictional company, the investor IRR, the internal rate of return, goes from 46.4 to 46.5 per cent. For SolaraPay, it goes from 29.0 to 29.1 per cent, with the multiple unchanged at 3.6 times and no breach months in either case. A structure cannot fix a pool. At most it prices a good one more efficiently, and SolaraPay's effort is better spent on collections and data.

## Scene 8. Recap and exercise
On screen: Readiness: full tenor vintages, reconciled tape, stable definitions, legal opinion, backup servicer, sufficient size, tested triggers, auditor view. Exercise: T06 Loan tape.

A securitisation moves receivables into an SPV and protects noteholders through subordination, excess spread and triggers, but in PAYGo it still depends on the originator as servicer. Excess spread is thin, fixed costs set a minimum size, and the receivables will probably stay on the balance sheet. In the model the structure changes returns by a tenth of a point, so readiness matters more than structure.

Open the T06 loan tape template and load a sample of your own company's accounts, or of a company you are assessing. Run the validation sheet until every check count reads zero. Then list which of the eight readiness criteria in Chapter 12 your data can already support, and which would block an arranger mandate today.
