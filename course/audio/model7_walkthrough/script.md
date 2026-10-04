# MODEL 7 audio walkthrough: script

Narration for the audio guide "How to use MODEL 7, step by step". Each section below is one chapter of the audio file. Figures are those of the default Kasiri case in MODEL 7 v1.0 release candidate 1, written as they are spoken.

## 01. Introduction

Welcome to the audio guide to MODEL 7, the Hydropower Development and Finance Model. It accompanies Book 7, Hydropower Development and Finance, From River to Financial Close.

In the next fifteen minutes, we will walk through the model one step at a time, on its reference case: Kasiri River Hydro, a fictional sixty megawatt run-of-river plant in the fictional Republic of Navaria. By the end, you will know where to start, how to check that the model is sound, how to read its results, how to stress them, and how to replace the case with your own project.

Please open the workbook now, and keep it next to you as you listen. Pause the recording whenever you want to try a step yourself.

## 02. The cover sheet

The workbook opens on the cover sheet. At the top, you see the title and the framework the model applies: the Hydro Readiness Framework, with eight questions, twenty-three gates and one financial close decision.

Below it, a block called Live status gives six answers that update with every change you make. For the default case, they read as follows. The financial close decision is STOP, because a critical gate is not met. Six of twenty-three gates are met. The nine-gate development screen reads not bankable. The fiscal screen reads low additional fiscal pressure. The model integrity checks read all OK. And the book consistency check reads all pass.

At the foot of the cover, the Start here links take you straight to the main sheets. We will use them in this order.

## 03. Read me and the colour code

Click the link to the Read me sheet. It explains what the model does and how it is organised. Three points matter before you touch anything.

First, the colour code. Blue font is an input you may change. Black font is a formula; never type over it. Green font is a link from another sheet. And a shaded green cell is a key output.

Second, the timeline. The model is annual, with forty periods, and every amount is in millions of US dollars, nominal, unless the label says real twenty twenty-six.

Third, the two levels of gates. A nine-gate screen helps you decide whether to keep developing. The twenty-three gates, on sheet thirty A, test whether the evidence file supports financial close. Keep that distinction in mind; we will come back to it.

## 04. The control panel

Now open sheet zero one, the control panel. This is the only sheet you need to run scenarios.

Section A sets the case. The model case is one for base, two for low and three for high. The generation case for cash flows is one for P fifty, two for P seventy-five, and three for P ninety. The lender sizing case has four options; the default, four, sizes the debt on the ten-year P ninety.

Section B sets the transaction. Structure two is a private independent power producer. Debt mode one means the debt is sized inside the model; mode two locks it at given amounts. The budget backstop, set to one, means the government covers any shortfall in the utility's payments to the project.

Section C holds nine stress toggles, from drought to transmission delay. Each is zero or one, and they can be combined. Section D holds five sensitivity flexes, in percent, for cost, generation, tariff, operating cost and interest rate.

Leave every value at its default for now. Section E, at the bottom, shows the main results for whatever you have selected.

## 05. Check before you read

Before reading any result, check that the model is sound. Open sheet thirty-three, Checks. It runs fourteen integrity tests: sources equal uses, debt is fully repaid, the energy chain is consistent, and so on. The last line must read all OK.

Then open sheet thirty-five, Book check. It compares the live model with the twenty-six Kasiri figures printed in Book 7. With the default inputs, every line reads pass. If you change an input, some lines will read check; that is expected, because the printed figures belong to the default case.

The rule is simple: do not rely on any output until the integrity checks read all OK.

## 06. Read the dashboard

Open sheet thirty-two, the dashboard. Row four gives three verdicts side by side: the nine-gate screen, the twenty-three gate close readiness, and the fiscal screen.

The project block shows the plant: sixty megawatts, about two hundred and ninety-two gigawatt hours a year at P fifty, a capacity factor of about fifty-six percent, and a plant cost of about one hundred and fifty-seven million dollars in twenty twenty-six terms.

The financial block shows how the plant is financed. Senior debt is about one hundred and forty-five million dollars. The minimum debt service cover ratio is one point five three. The private equity return is thirteen point eight percent, against a target of fifteen. And there is a financing gap of about four million dollars. In other words, the project is sound, but slightly short of the tariff its sponsors need.

The developer block shows the economics of getting there. The development budget is about nine million dollars over six years, with about a fifteen percent chance of reaching financial close from reconnaissance. On the success path, the developer earns about sixteen percent. But weighted by the chance of failure, its net present value is about minus one million dollars. The project is attractive once it succeeds, and not worth starting on these assumptions. Book 7, Chapter fourteen, explains why.

The utility and public finance blocks show the other side of the deal: the buyer can pay about six times the bill, but the government and the utility together lose about twenty-eight million dollars in present value, because the tariff is above what the utility collects from its customers.

## 07. Why the decision is STOP

Open sheet thirty A, Close readiness. Each of the twenty-three gates has a status. Some are tested automatically by the model; the others are evidence statuses that you enter, met, partial, not met or no evidence. A gate counts as met only on evidence. A blank status counts as no evidence.

The decision follows a fixed ladder. Any critical gate not met gives STOP. Critical gates only partly met give not ready. All critical gates met gives conditional go. And all twenty-three met gives go.

For Kasiri, seven critical gates are not met: the flow record and its independent review, the bankable feasibility sign-off, the environmental and social assessment to lender standards, land rights, six months of payment security, a fully committed financing plan, and an equity return at target.

At the foot of the sheet, the gates are grouped under the eight questions of the framework, and each question names the party that must accept it: developer, lender or government. Sheet thirty-four, the framework map, shows for each gate where the model tests it and which chapters of the book discuss it. STOP is not a verdict on the project. It is a work programme.

## 08. The developer's view

Open sheet zero one A, Development. Section A lists the six development stages, each with a duration, a budget and a probability of success. These probabilities are your judgement; no public data calibrate them for African hydro.

Section D gives the developer's returns: the risk-weighted net present value, the break-even development premium and the success-path value. Section D two values the whole development position at the start of each stage. Use it to price a co-developer's entry: at the start of permitting, Kasiri's position is worth about one point three million dollars.

Try one change. Raise the probability of the feasibility stage, and watch the risk-weighted value. Then set it back.

## 09. Stress the river

Go back to the control panel and set the drought toggle to one. The model applies three years at fifty-five percent of normal flow. The debt is still sized on the same lender case, so the amount does not change. But open the dashboard: the minimum debt service cover ratio falls below one, to about zero point seven. The reserve account is drawn, and it is not enough.

This is the most important stress for an energy-only tariff. A lender would ask for a larger reserve, a cash sweep in wet years, or less debt. Set the drought toggle back to zero.

## 10. Stress the buyer

Now set the offtaker stress to one. The utility's collections fall, transfers are cut and the retail tariff is frozen. Within ten years, the utility can no longer pay the project's bill. With the budget backstop on, the project is paid in full, and the cost moves to the government: the consolidated fiscal value falls to about minus one hundred and twenty-five million dollars.

Then set the backstop to zero. The twelve-month payment guarantee is used up, the rest becomes arrears, and the project defaults: the minimum cover ratio turns negative. This is the central lesson of the book: a project can be bankable because the risk has moved to the state. Reset both values to their defaults.

## 11. Compare structures and contracts

On the control panel, set the structure to one, then three, four and five, and read sheet seventeen A, Structures, together with the dashboard. Structure one is public, three a public-private partnership with concessional debt, four a hybrid with public civil works, and five blended finance. Watch how the equity return and the fiscal value move together: a grant that is not matched by a lower tariff transfers public money to private shareholders. Set the structure back to two.

On sheet zero five A, Contracting, the construction contract structure can be one, a single turnkey contract, two, split packages, or three, multiple contracts. Compare the cost and the share of overruns the owner keeps.

## 12. Use it on your own project

To apply the model to a real project, replace the blue inputs in this order. First, sheet zero two, the project inputs, and sheet zero three, the hydrology: monthly flows, head, design flow, the length and quality of the flow record. Second, sheet zero five, the plant cost. Third, sheet zero one A, the development stages, budgets and probabilities. Fourth, the commercial terms: sheet fourteen for the power purchase agreement, and sheets eleven and twelve for the buyer. Fifth, the financing terms on the debt and structures sheets. Finally, the evidence statuses of the twenty-three gates on sheet thirty A.

After every block of changes, check sheet thirty-three before reading any result. Expect sheet thirty-five to show check lines: it only applies to the Kasiri case. And keep a record of every assumption and its source, because the gates will ask for it.

## 13. Closing

That is the whole route: the cover, the checks, the dashboard, the close decision, the developer's view, the stresses and your own project. The User and Methodology Manual, MANUAL 7, gives every formula and every sheet in detail, and Book 7 explains the reasoning behind each step.

Remember that MODEL 7 is a decision-support tool, not investment advice, and that every default input is illustrative. Thank you for listening.
