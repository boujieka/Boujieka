# Added-value challenge: *Bankable Hydro* and the case for Book 7

Status: review memorandum, 4 October 2026. Written from two seats at once: a senior hydropower developer who has taken African hydro IPPs to financial close, and a commissioning editor of professional finance books. The brief was to be hostile but fair.

Scope and evidence rules:
* "The current book" is `book/Bankable_Hydro_Book.pdf` (68 pages, A5-ish trim) and its sources `book/src/01_front.md` to `05_redteam.md`. Figures from it are quoted from the PDF text.
* "The format" is the PAYGo book on branch `origin/ccr-d5d6abff-p7fc0j` (`output/20_BOOK2_INTERIOR_7x10_draft.pdf`, 178 pages, 7x10), with that branch's `README.md` and `output/13_PRODUCT_SUITE_PLAN.md`.
* External facts are used only where they already sit in this repository. Each one cites its location: `research/source_database.md` (source ID and verification flag F/P/S as defined there), `research/competitive_intelligence.md` (source tags [S1] to [S40]), or `research/case_studies/*.md`. If a fact is not in the repository, this memo does not state it. Statements marked **(Reviewer judgement)** are opinion.

---

## A. A blunt assessment of the current book

### A1. What the book is

*Bankable Hydro* is a 68-page policy monograph. It runs 19 chapters, about 2.5 pages each, plus three annexes. A 35-sheet model drives it, applied to a fictional 400 MW PPP (Lumora Falls, Republic of Navaria). Its thesis is good and clearly argued: a project can be bankable on its own terms while the arrangements that make it bankable leave the state carrying unpriced risk (Ch. 17, "Reading the table"). The book follows one chain from river flow, through the utility's ability to pay, to the sovereign's contingent liabilities. It is honest about its sources: "public data not found", "seen only in a summary", and a red-team chapter that sets out the model's own defects.

The writing is controlled and the tone is adult. The thesis, though, is aimed at the Ministry of Finance. The people who pay for professional hydro books and models are mostly elsewhere.

### A2. Who would buy it

| Segment | Would they buy? | Why |
|---|---|---|
| Ministry of Finance, PPP and debt-management units | Some would read it; few would pay | The fiscal half (Ch. 13 and 14) sits next to PFRAM 2.0 and LIC-DSF, which are free, authoritative and already in use in these units (`competitive_intelligence.md` A4, items 24 to 26; [S28] to [S32]). The book's added value for them is the hydro and utility front end, and that front end takes up about 15 pages. |
| DFI and MIGA project teams, guarantee officers | Possibly, as a reference | The shortfall-routing logic (Ch. 8) and the "guarantees are sovereign exposure" argument (Ch. 13) are useful framing. They will notice that their own appraisal work goes deeper on the offtaker than one simplified cash model. |
| Developers and sponsors | **No** | The book treats the project as a given object that already exists at the point of structuring. It contains no development process, no development budget, no developer returns before financial close, no EPC strategy and no financial-close mechanics. Development cost is one capex line (`model/build_model.py`, line 501: "Development costs & owner's costs"). A developer finishes the book knowing why the Treasury should worry. He learns nothing about how to get his project to close. |
| Commercial and DFI lenders, credit analysts | Unlikely | Chapter 11 is three pages long. It admits that covenant levels are unsourced beyond one appraisal document (Nachtigal, `source_database.md` PF-11, F). The base case shows a minimum DSCR of 1.64x and an **average of 3.32x** (Table 11.1). Any credit officer reads that as debt capped by gearing, not sized on cover, so the structure is not realistic for a hydro IPP. The book explains it in one sentence and moves on. |
| Transaction advisers | Partly | They would value the integrated scenario table (Table 17.1). They would want the contract set, the CP list and the model mechanics they actually build: monthly construction, draw sequencing, sculpting with DSRA and MMRA, and refinancing. |
| Graduate students and academics | Yes, if priced low | It is a readable, well-sourced introduction to fiscal risk in hydro PPPs. The market is small and price-sensitive. |

**(Reviewer judgement)** The current buyer is the policy reader, and that reader is served free by the IMF, the World Bank and the ALSF. The paying professional market is developers, lenders, advisers and DFI investment staff, and that market is barely addressed. The competitive scan points the same way. The products with visible prices are project-finance courses (US$499 to US$3,200 and £2,700 to £4,495) and hydro Excel templates (US$45 to 499, partly snippet-only). Every product with a fiscal lens is free (`competitive_intelligence.md` D, [S12], [S14], [S17], [S20], [S22], [S28] to [S35]).

### A3. What is genuinely new (and worth keeping)

1. **The integrated chain in one set of inputs:** hydrology, generation, transmission readiness, utility cash, PPA bill, shortfall routing, guarantee calls, consolidated fiscal NPV, and a screen. The competitive scan found no reviewed product that links hydrology-driven project cash flow to the offtaker's capacity to pay and then to the sovereign envelope (`competitive_intelligence.md` C, note 4; E1). The scan rests on public descriptions, not hands-on testing (its methodology item 4), so this is a defensible differentiator, not a proven first.
2. **The maximum sustainable PPA payment and the routing rule:** backstop, then capped guarantee, then arrears to the project (equations 8.2 to 8.5). The rule makes visible a point that lenders and Treasuries both miss: without the backstop, the "robust" project defaults (Ch. 8; Table 17.1, offtaker stress with no backstop).
3. **A consolidated fiscal NPV that includes the state utility,** with the honest admission that a Treasury-only perimeter made a transmission delay look fiscally beneficial (Ch. 6 and Ch. 18).
4. **Locked-package stress testing.** Stresses are run with the financing frozen at base-case terms, which is how a signed deal behaves (Ch. 1 and 11).
5. **Hydrology caveats that most PF texts skip:** the Jensen bias from using mean flows, and one-year P90 versus multi-year persistence (Ch. 3). The book raises them but does not model them.
6. **Two results a developer can actually use.** First, the pure IPP structure does not reach its target at the negotiated tariff: equity IRR 10.4% against a 16% target, with a USD 87m financing gap (Table 12.2). Second, a grant with no tariff adjustment produces a windfall: the hybrid structure's equity IRR is 30.3% (Table 12.2). Both are developer-relevant results, and the book draws only the policy conclusion from them.

### A4. What is thin

| Area | Current treatment | Why it is thin |
|---|---|---|
| Length and depth | 68 pages, 19 chapters | Chapter 9 (regulation), Chapter 10 (PPA) and Chapter 15 (risk allocation) run about 1.5 pages each. The PAYGo book gives a comparable topic 8 to 10 pages, with worked numbers and committee points. |
| PPA | 1.5 pages: two-part tariff, volume clauses, currency, termination | The book omits wet and dry season pricing, availability definitions, the mechanics of a hydrology-risk allocation, deemed-energy triggers and caps, change in law, indexation baskets, the tariff true-up at financial close, and the termination formula by event type. Its own case library holds a seasonal-tariff precedent it does not use (Upper Trishuli-1, wet- and dry-season run-of-river tariff, `international_benchmarks.md` §6). |
| Debt | Sculpting formula, closed-form IDC, one covenant source | Missing: semi-annual debt service, DSRA sizing logic, MMRA, the cash waterfall and lock-up, completion tests, sponsor support before completion, intercreditor arrangements in a DFI club, A/B loans, refinancing or mini-perm, and hedging. HY-06 proposes refinancing within 7 to 10 years of operation (`source_database.md` HY-06, F). The book does not model it. |
| Construction | Reference class (Ansar) plus a 4%-per-year delay cost | Missing: contract strategy, the geology risk split, the LD regime, bonds, the owner's engineer, the funded contingency rule (the repo holds the Nachtigal 20% funded contingency with 50:50 sharing of unused contingency, `source_database.md` benchmarks, PF-11), and a monthly draw schedule. The model's capex profile is a sine S-curve with the note "Replace with EPC payment schedule when available" (`build_model.py`, line 487). |
| Operations | One paragraph on O&M cost (Ch. 5) | Missing: the O&M contract model, availability guarantees, major overhauls, insurance, and the World Bank O&M handbook with its African cases (`source_database.md` HY-07, F; `competitive_intelligence.md` item 10). |
| Risk allocation | A six-row table (Table 15.1) | A sixteen-by-eight matrix exists in the model but does not appear in the book. |
| Rules for financial close | Eleven numbered rules (Ch. 19) | These are policy maxims, not a close process. The chapter has no CP list, no funds flow, no long-stop dates, no EPC price-validity issue and no legal opinions. |
| The red-team chapter | A full chapter of model defects | It is honest and unusual, but in a professional book it reads as "the tool was broken last month". The workbook "passed every one of its own integrity checks while several of these defects were present" (Ch. 18). That sentence will be quoted against the product. The material belongs in a validation annex. |
| Format | Plain monograph | Unlike the PAYGo book, it has no decision statement per chapter, no place in a chain, no committee points, no "working with the model" section, no templates, no Go/Conditional/Stop gates with an evidence rule, and no case walk-through chapter. |

### A5. What a developer or lender would find missing

1. **Development process.** Site identification, reconnaissance, pre-feasibility, feasibility, bankable feasibility, permitting and PPA negotiation, financing, close. None of it is described, and nothing says what is decided at each stage or what it costs. The only timeline data point in the repo is "large hydro typically 8 to 10 years from initiation to COD" (HY-06, F) and an 8.6-year mean build time (HY-08, F). The book uses the second as a construction statistic only.
2. **Development budget.** Studies (hydrology, topography, geotechnical investigations, sediment), ESIA and RAP, legal, PPA and concession negotiation, grid studies, financial advisory, lender due diligence costs reimbursed at close, and development team overhead. None of it is presented by stage or workstream, and none of it is treated as at-risk capital.
3. **Developer returns.** The book has no risk-weighted development NPV, no development premium, no developer fee, no success fee, no reimbursement of development costs at financial close, no value step-ups at milestones, and no sell-down. The repo records Nachtigal's equity changing from EDF 40/IFC 30/Cameroon 30 at close to EDF 40/IFC 20/Cameroon 15/Africa50 15/STOA 10 later (`africa_part2.md` §1 J, partly search-result only). That is exactly the sell-down story a developer wants explained, and the book does not use it.
4. **EPC and contracting.** Single-point turnkey EPC versus a multi-lot split (civil, electro-mechanical, hydro-mechanical). Who takes ground risk. LD rates and caps, performance tests, bonds, price validity and its interaction with the close date. The Chinese EPC-plus-Exim route the case library documents (Isimba, Karuma, `africa_part2.md` §7 and §8). The procurement failures it records (Gibe III, Bujagali I, Batoka; Ch. 9).
5. **Permitting sequence.** Which consents gate which others. Water rights before the PPA, ESIA before lender commitment, RAP before construction, dam safety review (`source_database.md` HY-15), and transboundary notification. The book gives a sixteen-item readiness matrix with no sequence and no critical path.
6. **Financial-close mechanics.** The CP list, the lenders' technical, legal, insurance and E&S advisers, the model audit, direct agreements, security perfection, the funds flow at close, the first drawdown conditions, hedging execution, and the long-stop date.
7. **Operations.** Availability, the O&M contract, major maintenance reserve, insurance renewal, the hydrology true-up after COD, refinancing, and reporting covenants.

### A6. Where it duplicates free institutional material

| Current book content | Free material that already covers it (repo location) | Overlap |
|---|---|---|
| Ch. 13 and 14: direct vs contingent liabilities, expected loss, project fiscal screen | PFRAM 2.0 model, guidance note and user manual (`source_database.md` FR-01 to FR-03; `competitive_intelligence.md` item 24, [S28] and [S29]); World Bank FCCL guidance (item 26, [S32]); Polackova (FR-14) | High. The book's screen is a simplified PFRAM front end and should say so. |
| Ch. 14: DSA thresholds and CL stress | LIC-DSF guidance note and supplement (FR-09, FR-10; item 25, [S30]) | High. The book restates the thresholds. |
| Ch. 8: utility viability data, QFD | Kojima and Trimble, Trimble et al., UPBEAT (UT-01, UT-02, UT-05; items 27 and 28) | Medium. The data are theirs; the MSP mechanism is the book's own. |
| Ch. 10, 11, 15: PPA structure, financing, credit enhancement, guarantee instruments | CLDP/ALSF *Understanding Power Purchase Agreements* and *Understanding Power Project Financing* (PF-07 to PF-10; items 7 and 8) | Medium to high on concepts. The free handbooks are Africa-specific and longer on PPAs than the book. |
| Ch. 3 to 5: hydrology, cost, O&M at overview level; lifecycle | IFC *Hydroelectric Power: A Guide for Developers and Investors* (2015) (item 9, [S10]); World Bank O&M handbook (HY-07) | Medium. The IFC guide is exactly the developer lifecycle the book lacks. Its finance chapter is general (item 9), and that is where a new book should go deeper. |
| Ch. 4: reference-class overruns | Ansar et al. (HY-08, F), Flyvbjerg (HY-11) | Low (properly cited). Widely quoted, so it is no differentiator. |
| Ch. 9: E&S readiness | Hydropower Sustainability Standard and HESG (HY-03; items 29 and 30) | Low to medium. |

**(Reviewer judgement)** About a third of the book's pages restate free institutional frameworks at a lower depth than the originals. The two-thirds that are original (the integration, the MSP routing, the consolidated perimeter, locked stresses) are valuable, but they fit in two strong chapters of a broader book. They do not justify a standalone paid volume for a professional audience.

---

## B. Recommendation: reposition as Book 7

### B1. The repositioned book

**Book 7. *Hydropower Development and Finance: Business Models, Project Development and Financial Structuring for Hydropower in Africa*.** Africa Energy Finance, Business & Financial Models. 7x10 interior, PAYGo book format, about 230 to 250 pages.

Primary readers, in priority order: developers and sponsors (including utility-backed and DFI co-developers), lenders and DFI investment officers, transaction advisers, and Ministry of Finance and PPP unit staff (who get one full chapter written for them and a template annex). The existing *Bankable Hydro* material is not dropped. It is compressed into Chapter 15 and threaded through Chapters 4, 8 and 13.

**Collection entry** (to add to the collection table used in "About this book"):

| Book | Subject | Central question | Status |
|---|---|---|---|
| Book 7 | Hydropower | Can this hydropower project be developed to financial close and financed on terms that the developer, the lenders and the state can each accept? | Proposed |

### B2. Central question

> **Can this hydropower project be developed to financial close, and financed on terms that reward the developer for the risk it took, satisfy the lenders, and leave the state with obligations it can carry?**

The three-party clause is deliberate. It keeps the current book's best idea, that a deal the Ministry of Finance cannot sign does not close, while moving the centre of gravity to the developer and the lender.

### B3. Core thesis (one sentence)

> **A hydro project is three investments in one asset: a development option bought with at-risk equity, a construction contract that is a bet on geology, and a thirty-year annuity on a river and a utility's creditworthiness. Each is priced by a different investor at a different cost of capital, and most failures come from funding one with capital meant for another.**

This plays the role of "a PAYGo company is three businesses in one". It explains why development equity needs a premium, why EPC structure and contingency drive bankability, and why the long-term holder, the lender and the state care about hydrology and offtaker credit. It also gives Chapter 1 the same shape as the PAYGo Chapter 1: where each of the three shows in the numbers, and where cash and value diverge.

| Area | Development option | Construction contract | Operating annuity |
|---|---|---|---|
| Period | Site to financial close (often 5 years or more; HY-06 cites 8 to 10 years initiation to COD for large hydro) | Close to COD | COD to end of concession |
| Main risks | Permits, PPA, land, hydrology evidence, failure to close | Geology, contractor performance, delay, interface with the line | Hydrology, offtaker payment, FX, O&M, regulation |
| Who funds it | Developer equity, co-developers, project development facilities | Equity (often first), senior debt, contingency, standby equity | Senior debt service, distributions, refinancing |
| How value shows | Step-ups at milestones; development premium at close | Completion; LDs; IDC; contingency release | DSCR, distributions, refinancing gain |
| Typical failure | Spending past a gate the project should have failed | Overrun beyond contingency; contractor default | Offtaker arrears; drought run; FX step |

### B4. The analytical chain

"A hydro project can be read in a fixed order. A weakness found early, in the flow record or the permitting sequence, travels down the chain and arrives larger at the debt sizing and the close."

| Link | Question | What it passes on | Chapters |
|---|---|---|---|
| River and site | Is there a resource worth developing here? | Catchment, head, access, competing uses | 2, 3 |
| Hydrology evidence | How good is the flow record, and how uncertain is energy? | Flow series, data-adequacy score, P50/P90 (one-year and multi-year) | 2 |
| Configuration | What should be built? | Design flow, MW, storage, energy by season, capex envelope | 3 |
| Offtake route | Who buys, through which procurement route, at what tariff structure? | PPA route, tariff form, indexation, currency | 4 |
| Development plan | What must be done, in what order, at what cost and probability? | Stage plan, development budget, stage-gate probabilities | 5, 6 |
| Consents and E&S | Which permits gate which others, and how long do they take? | Consent sequence, critical path, E&S conditions | 7 |
| Contract set | Is the chain of contracts bankable and consistent? | Concession, PPA, grid connection, water use and direct agreements; termination amounts | 8 |
| EPC and construction | Who takes geology and delay, and at what price? | Contract structure, LDs, contingency, monthly spend | 9, 10 |
| Operations | Who runs it, and what will it cost to keep it available? | O&M model, availability, MMRA, insurance | 11 |
| Debt | How much senior debt, at what tenor, on which case? | Debt quantum, DSCR/LLCR, DSRA/MMRA, covenants | 12 |
| Lender group and enhancements | Which lenders, and which guarantees and insurances? | DFI club, MIGA/PRG/liquidity cover, local-currency tranches | 13 |
| Developer returns | Is it investable for the developer, and at what price can it sell down? | rNPV, development premium, equity IRR at close and at sell-down | 14 |
| Public obligations | What does the state commit, and can it carry it? | MSP, support package, contingent liabilities, fiscal screen | 15 |
| Stress | What breaks first, and who holds it? | Break-even flow, maximum overrun, distance to default | 16 |
| Financial close | Go, conditional go or stop, on what evidence? | CP status, readiness gates, decision and conditions | 17, 18 |

### B5. Questions that are not the same question

"Hydro projects are described as 'feasible' or 'bankable' as if those words meant one thing. The book separates eight questions, because a project can pass one and fail the next, and each is answered by a different document or test."

| Question | Answered by | Typical trap |
|---|---|---|
| Is the site technically viable? | Feasibility study and geotechnical investigation (Ch. 2, 3, 9) | A feasibility study built on a short or synthetic flow record presented as a long one |
| Is the project developable? | Consent sequence, land and water rights, PPA route (Ch. 5, 7) | Spending on bankable feasibility before the PPA route and water rights are secure |
| Is it economic for the power system? | Least-cost plan, LCOE against alternatives, value by season (Ch. 3, 4) | Quoting plant LCOE when the system pays plant plus line (current book, eq. 5.1) |
| Is it investable for the developer? | Risk-weighted development NPV, development premium, sell-down value (Ch. 6, 14) | Reading the equity IRR at close as the developer's return while ignoring at-risk development spend and the probability of failure |
| Is it bankable? | Lender case, DSCR/LLCR, security package, lender DD reports (Ch. 12, 13) | A project protected by capacity charges and backstops, so that lenders "see nothing" (current book, Ch. 8) |
| Is it buildable on budget? | EPC structure, contingency, reference class, draw schedule (Ch. 9, 10) | A "fixed-price" EPC with ground conditions excluded |
| Is it affordable for the offtaker and the state? | MSP, support package, contingent-liability measures, fiscal screen (Ch. 15) | A bankable project whose arrangements move the risk onto the Treasury (current book thesis) |
| Is it ready to close? | CP tracker and evidence-based readiness gates (Ch. 17) | Treating a signed term sheet as a closed deal |

### B6. Chapter plan (18 chapters)

Every chapter follows the PAYGo template. It opens with "This chapter supports one decision...", then "Place in the analytical chain:", then numbered sections (n.1, n.2...). Each chapter includes a "What the [case] shows" section and ends with "Points for the investment and credit committees" (five or six numbered points) and "Working with the model" (sheet names). Sheet names below are the proposed Model 7 names (section C). Sheets marked † reuse an existing *Bankable Hydro* sheet with modification.

**Part I. The business and the resource**

| # | Title | Decision it supports | Main contents | Model sheets | Pages |
|---|---|---|---|---|---|
| 1 | The hydro project: three investments in one asset | Which capital should fund which phase, and which numbers each party should read first | 1.1 Option, contract, annuity. 1.2 How value and cash are created and where they diverge (worked example: one MW from site to year 10). 1.3 Who develops hydro in Africa: private developers, utility-led, DFI co-development (IFC co-development role, `source_database.md` HY-12, F), state-led with Chinese EPC (Isimba, Karuma). 1.4 Scale and private participation (HY-06: private share 74% for plants <10 MW vs 8% for >2,500 MW, F). 1.5 How hydro projects fail: at development, at construction, in operation (Ch. 1 of current book, refocused). 1.6 How the book and model are organised; the case. | START, DASHBOARD, CASE | 10 |
| 2 | River, flow record and hydrology risk | Is the hydrological evidence good enough to spend feasibility money, and later good enough to size debt? | 2.1 Four kinds of capacity (from current Ch. 3). 2.2 The flow record: gauges, gaps, rating curves, extension by correlation. 2.3 Data adequacy as a credit variable. 2.4 Flow duration curves and the Jensen bias. 2.5 P50, P90 one-year and multi-year; persistence and dry runs. 2.6 Climate and sediment (CL-01, CL-03, CL-06). 2.7 Kariba as the persistence warning (CL-04/05, news, flagged). 2.8 What the case shows. | HYD_DATA (new), HYDROLOGY†, GENERATION† | 14 |
| 3 | Configuration, energy and the value of a seasonal kWh | What to build: design flow, installed capacity, pondage or storage | 3.1 Sizing design flow against the FDC. 3.2 Run-of-river, pondage, storage. 3.3 Capacity factor benchmarks (HY-01: large hydro in Africa 33/48/81%; small 50/55/66%). 3.4 Firm dry-season energy versus annual energy. 3.5 Capex envelope by configuration (HY-01, PF-11 ranges). 3.6 Plant LCOE and system LCOE (current eq. 5.1). 3.7 The case's sizing choice. | CONFIG_OPT (new), CAPEX†, OPEX† | 10 |
| 4 | The route to a PPA: procurement, tariff design and the buyer | Which offtake route to pursue, and which tariff structure to propose | 4.1 Routes: unsolicited or direct negotiation, competitive tender, standardised tariff, bilateral or mining offtake. 4.2 Procurement transparency as a lender filter (Gibe III, Bujagali I, Batoka from current Ch. 9; the Nyagak III tender, `africa_part2.md` §10). 4.3 Tariff forms: energy-only, two-part, wet and dry season (Upper Trishuli-1). 4.4 Indexation and currency. 4.5 Can the buyer pay? MSP in brief, with full treatment in Ch. 15. 4.6 Tariff solved for target return. | PPA_TARIFF†, OFFTAKER† | 12 |

**Part II. Developing the project**

| # | Title | Decision it supports | Main contents | Model sheets | Pages |
|---|---|---|---|---|---|
| 5 | The development process and its stage gates | Go or stop at the end of each development stage | 5.1 Five stages, from reconnaissance to close. 5.2 What each stage must prove. 5.3 Timelines and their evidence (HY-06, HY-08; no invented durations; case values labelled illustrative). 5.4 Stage-gate probabilities as a model input, not a statistic. 5.5 Critical path and probability-weighted COD. 5.6 Killing a project early: the cheapest decision a developer makes. | DEV_PLAN (new) | 12 |
| 6 | The development budget and how it is funded | How much to spend, in what order, and with whose money | 6.1 Budget by stage and workstream. 6.2 At-risk versus recoverable spend. 6.3 Expected development spend under stage probabilities. 6.4 Funding sources: developer equity, co-developers, project development facilities (DevCo/PIDG funding advisory work on Nyagak III, `africa_part2.md` §10 K). 6.5 Joint development agreements: contribution, dilution, step-in. 6.6 Development fee, success fee and reimbursement at close. 6.7 The case's budget. | DEV_BUDGET (new), DEV_VALUE (new) | 12 |
| 7 | Consents, land and E&S: the permitting sequence | Which consents to pursue first, and which are on the critical path to close | 7.1 Map of consents: water rights, generation licence, concession, ESIA, land, dam safety (HY-15), grid, tax, FX approvals. 7.2 Dependencies and sequencing. 7.3 Lender E&S standards (IFC PS, HSS, HY-03) and the ESAP. 7.4 Resettlement and the RAP schedule. 7.5 Transboundary notification (GERD, Ch. 9 of current book). 7.6 A consent tracker. | PERMITS (new), REGULATION† | 10 |
| 8 | The contract set: concession, PPA, grid connection and direct agreements | Is the contract chain bankable, consistent and complete? | 8.1 The contract map and interfaces. 8.2 PPA terms that matter for hydro: availability, hydrology allocation, deemed energy triggers and caps, seasonal pricing, indexation, change in law, payment security. 8.3 Concession or implementation agreement. 8.4 Grid connection and transmission interface (readiness gap from current Ch. 6). 8.5 Termination events and amounts. 8.6 Direct agreements and step-in. 8.7 Contract consistency checklist. | CONTRACTS (new), TRANSMISSION† | 12 |

**Part III. Building and running it**

| # | Title | Decision it supports | Main contents | Model sheets | Pages |
|---|---|---|---|---|---|
| 9 | EPC and construction contracting | Which contract structure, and who takes ground and delay risk at what price | 9.1 Single-point EPC vs multi-lot (civil / E&M / hydro-mechanical). 9.2 Ground risk: geotechnical baseline, provisional sums, remeasurement. 9.3 LDs, caps, performance tests, bonds and retention. 9.4 Owner's engineer and lenders' technical adviser. 9.5 EPC plus export credit packages (Isimba, Karuma). 9.6 Price validity and the close date. 9.7 Contractor failure: Isimba defects, Nachtigal remediation (`africa_part2.md` §1 G, §7). | EPC (new) | 14 |
| 10 | Construction budget, contingency and the draw schedule | How large the contingency should be, and how construction is funded month by month | 10.1 Total uses (current Ch. 4 scope discipline). 10.2 Contingency by lot. 10.3 The reference class and its limits for mid-size run-of-river (HY-08 is large dams). 10.4 Monthly draw schedule: equity first or pro rata. 10.5 IDC and fees. 10.6 Standby equity and cost-overrun facilities. 10.7 Delay: cost twice (current Ch. 4). | CONSTRUCTION_M (new), SOURCES_USES† | 10 |
| 11 | Operations: availability, O&M, major maintenance and insurance | Which O&M model, and how to reserve for major maintenance | 11.1 Owner-operated, O&M contractor, OEM long-term service. 11.2 Availability definitions and guarantees. 11.3 O&M cost benchmarks (HY-01: 1 to 3% of installed cost). 11.4 Major overhauls and the MMRA. 11.5 Insurance. 11.6 World Bank O&M framework (HY-07). 11.7 Post-COD hydrology true-up and reporting. | OM_MMRA (new), OPEX† | 8 |

**Part IV. Financing it**

| # | Title | Decision it supports | Main contents | Model sheets | Pages |
|---|---|---|---|---|---|
| 12 | Sizing hydro debt: the lender case | How much senior debt, at what tenor, on which generation case | 12.1 Tenor and the tariff (PF-13: rarely >15 to 18 years; Nachtigal 18 and 21 years, PF-11). 12.2 Sculpting on P90 (current eq. 11.1 and 11.2). 12.3 One-year versus multi-year P90 and dry-run tests. 12.4 Closed-form IDC (current eq. 11.3, presented as a technique, not an innovation). 12.5 DSRA, MMRA and the cash waterfall. 12.6 Covenants, lock-up, completion test (sourced only to PF-11, labelled). 12.7 Refinancing and mini-perm (HY-06). 12.8 Why the current Lumora base shows an average DSCR of 3.32x, and what a sized-on-cover structure looks like. | DEBT†, CASHFLOW†, TAX† | 14 |
| 13 | The lender group: DFIs, ECAs, blended finance and credit enhancement | Which lenders, and which guarantees and insurances, at what cost to whom | 13.1 DFI clubs, A/B loans, intercreditor (Nachtigal: 11 DFIs plus local banks, `africa_part2.md` §1 H and I). 13.2 Local-currency tranches (Nachtigal). 13.3 Concessional and blended finance; grants and the windfall rule (current Ch. 12). 13.4 MIGA, IBRD/IDA and AfDB guarantees (PF-01 to PF-03, PF-06). 13.5 Liquidity facilities (ATIDI RLSF: up to 12 months of revenue, projects up to 100 MW, PF-04). 13.6 Every enhancement has a counter-indemnity (Bujagali, Nachtigal; current Ch. 13). | DFI_ENH (new), STRUCTURES† | 12 |
| 14 | Developer returns, valuation and sell-down | Is the project investable for the developer, and at what price and stage should it bring in partners or sell? | 14.1 The developer's cash flows from first spend to exit. 14.2 Risk-weighted development NPV. 14.3 Development premium and value step-ups by milestone. 14.4 Equity IRR at close and the hurdle. 14.5 Sell-down at close, at COD, after refinancing (Nachtigal shareholding changes, flagged as partly search-result). 14.6 Promotes, carried interest and development fees: what lenders and governments accept. 14.7 Why the pure IPP in the current Lumora runs reaches 10.4% against a 16% target, and what a developer does about it. | EQUITY_RETURNS†, SELLDOWN (new), DEV_VALUE | 12 |
| 15 | The public side: affordability, support and contingent liabilities | What support to ask the state for, and whether the state can carry it, because a package the Ministry of Finance cannot sign does not close | 15.1 Maximum sustainable PPA payment and the payment gap (current Ch. 8). 15.2 Where a shortfall goes: backstop, capped guarantee, arrears. 15.3 Direct support and contingent liabilities, three measures kept apart (current Ch. 13). 15.4 Consolidated perimeter including the utility. 15.5 A project screen designed as a front end to PFRAM and LIC-DSF, not a substitute (FR-01, FR-09). 15.6 The Lumora 400 MW contrast: why fiscal exposure dominates at scale (current Table 12.1, 17.1). 15.7 The one-page MoF note. | OFFTAKER†, GOVT_SUPPORT†, CONTINGENT†, FISCAL_SCREEN† | 14 |

**Part V. Deciding**

| # | Title | Decision it supports | Main contents | Model sheets | Pages |
|---|---|---|---|---|---|
| 16 | Risk allocation and stress testing | What breaks first, when, and who holds it | 16.1 The allocation matrix (full 16x8 from the model). 16.2 Designing hydro stresses: dry run, overrun, delay, transmission, offtaker, FX, rates. 16.3 Locked-package testing. 16.4 Reverse stress: break-even flow factor, maximum overrun before default, months of arrears to DSRA exhaustion. 16.5 Reading developer, lender and state results side by side. 16.6 The case stress table. | SCENARIOS†, REVERSE_STRESS (new), RISK_MATRIX† | 10 |
| 17 | Financial close: conditions precedent, readiness gates and the close | Go, conditional go or stop for financial close, and on what evidence | 17.1 What "financial close" legally means: signing, CP satisfaction, first drawdown. 17.2 The CP list by workstream. 17.3 Lender due diligence reports. 17.4 Funds flow at close. 17.5 Readiness gates (B8) and the evidence rule. 17.6 The investment memo and the credit paper. 17.7 CPs, covenants and conditions subsequent as levers. 17.8 Why projects stall between signing and close (Bujagali I ECA withdrawal, Nyagak III lender withdrawal, current Ch. 9; `africa_part2.md` §10). | CP_TRACKER (new), FC_READINESS (new) | 14 |
| 18 | Case walk-through: the case from site to close | Applying the full decision sequence to one project | 18.1 The ask. 18.2 Loading the flow record. 18.3 What the data show (data adequacy). 18.4 Re-sizing. 18.5 Development budget and rNPV. 18.6 The EPC bids. 18.7 Debt sizing on the lender case. 18.8 The lender group and enhancements. 18.9 The public side. 18.10 Stress tests. 18.11 Readiness gates and the decision. 18.12 Sell-down valuation. 18.13 Reflections on method. | All; CASE | 16 |

Chapter total: about 220 pages. With front matter (about 16 pages: About this book, Preface, Introduction) and annexes (about 35 pages), the book comes to roughly 260 pages at 7x10. If the editor wants nearer 220, cut Chapters 3 and 11 to 6 pages each, merge Chapter 7 into Chapter 5, and move Annex J to the model manual. This keeps 17 chapters.

**Front matter (PAYGo template):**
* About this book: the collection table, the central question, and the product set (book, Model 7, Manual 7, Case 7, video course).
* Preface:
  * how the book works with the model;
  * conventions, including P-values, real versus nominal, and USD/kW scope labels (plant, funding base, total uses, system; current Ch. 4);
  * sources and evidence, with the PAYGo A to D grade plus verification status. Map the repo's F/P/S flags onto it: F to "verified", P to "pending primary page", S to "unverified/snippet";
  * status of this edition;
  * disclaimer.
* Introduction: "How to read a hydro project", with the B4 chain table and the B5 "questions that are not the same question" table.

### B7. The fictional case: recommendation

**Recommendation: move the primary case to a fictional 60 MW run-of-river IPP in Navaria. Keep Lumora Falls (400 MW PPP) as a secondary contrast case, used in Chapters 1, 15 and 16 only.**

Working name: *Kasiri River Hydro*. The developer is *Tamarind Hydro Ltd*, a fictional mid-size regional developer, with a fictional DFI co-development partner. The offtaker is the same fictional Navaria utility, so the existing utility cash model (sheets 11 and 12) is reused.

Why move to a smaller private IPP:
1. **The developer has to be the protagonist.** At 400 MW in a PPP with state equity, a VGF grant and a state-built line, the developer is one of many. Private participation is concentrated at the smaller end (HY-06: 74% private share below 10 MW against 8% above 2,500 MW, F). A 40 to 80 MW plant is credibly developed by a private sponsor with DFI support.
2. **Hydrology risk becomes the developer's problem again.** About 71% of Lumora's revenue comes from capacity payments, so a three-year drought "barely touched the equity return" (current Ch. 3 and 10). That makes the hydrology chapter irrelevant to the investor. A run-of-river IPP with an energy-heavy or seasonal tariff puts the flow record at the centre of the credit, which is the reality developers and lenders face.
3. **The instruments fit.** The ATIDI RLSF covers projects up to 100 MW (PF-04). The case can use a real-world-style liquidity instrument without assuming a sovereign guarantee by default.
4. **The development budget becomes a real decision.** At this scale, development spend is material to a developer's balance sheet and small relative to a state's. The rNPV and the development premium become the developer's central questions.
5. **The fiscal question compresses naturally.** Fiscal exposure from a 60 MW plant will usually be small relative to GDP. Kept as the contrast case, Lumora's 400 MW exposure shows when the public-finance chapter becomes decisive. This is the honest way to keep the current book's best material without letting it dominate.
6. **It avoids the mega-dam debate.** The current book spends effort on neutrality about large dams (Preface). A run-of-river IPP still raises E&S issues but shifts the reader's attention to structuring.

Cautions:
* **Reference class mismatch.** Ansar et al. studied 245 large dams (HY-08). Applying a 27% median and a 96% mean overrun to a 60 MW run-of-river plant needs an explicit caveat: present them as sensitivity anchors, not calibrated priors.
* **Thin case library at this size.** The repo has no 40 to 80 MW private African hydro IPP case. The nearest are Rusumo (80 MW, public), Nyagak III (6.6 MW PPP), Isimba (183 MW), Upper Trishuli-1 (216 MW, Nepal; the closest structural analogue per `international_benchmarks.md` §6), Bujagali (250 MW) and Nachtigal (420 MW). Research is needed before publication. Do not fill the gap with invented "typical" numbers.
* **Capex.** The repo's African benchmarks are USD 2,330 to 3,290/kW for >10 MW and about USD 3,800 to 4,200/kW for ≤10 MW (`source_database.md` benchmark table). Any Kasiri capex must be labelled a model assumption chosen inside that envelope, not a benchmark.

**The case's "ask" (mirroring SolaraPay).** Tamarind has completed feasibility. It seeks two things: a co-development partner to fund the remaining development budget (bankable feasibility, ESIA/RAP, PPA negotiation, lender DD) in exchange for an equity stake, and a DFI-led lender group for senior debt with a liquidity facility. The management case looks attractive. Once the synthetic flow record is loaded, the data-adequacy adjustment widens the P90, the EPC bids come in with ground risk carved out, and the case becomes conditional. That journey, from management case to evidence-based case, is the method of the book, as it is for SolaraPay. All numbers come from Model 7 and are labelled illustrative.

### B8. Readiness gates for financial close

These follow the PAYGo rule. Automatic gates are computed by the model. Manual gates count only when marked Met with the evidence location, the signatory and the date recorded. The decision rule:
* **STOP** when a test fails.
* **STOP (incomplete evidence)** when a critical gate is open.
* **CONDITIONAL GO** when every critical gate is met, with the open gates as conditions.
* **GO** when all gates are met.

The wording is "readiness" and "evidence completeness", never "rating" or "bankable grade". A GO says the file is ready for a credit committee to decide; it is not a recommendation (as in PAYGo §15.6). Thresholds are author's screening defaults, editable, and labelled.

| # | Gate | Type | Critical | Evidence / test |
|---|---|---|---|---|
| 1 | Flow record adequacy | Auto | Yes | Data-adequacy score ≥ threshold (years, gaps, on-site vs correlated, R² of extension) |
| 2 | Independent energy yield | Manual | Yes | Lenders' technical adviser report on P50 and P90 (one-year and multi-year) |
| 3 | Geotechnical investigation sufficient for the EPC price basis | Manual | Yes | Investigation report; geotechnical baseline report agreed with EPC contractor |
| 4 | ESIA approved and lender-compliant; ESAP agreed | Manual | Yes | Approval letter; lender E&S adviser sign-off against IFC PS / HSS |
| 5 | Land and resettlement on schedule | Manual | Yes | RAP implementation status vs construction access dates |
| 6 | Water use rights and generation licence granted | Manual | Yes | Permits held; tenor ≥ debt tenor plus tail |
| 7 | Concession/IA and PPA signed and consistent | Manual | Yes | Contract consistency checklist (Annex E) complete; termination amounts ≥ debt outstanding |
| 8 | Payment security in place | Auto + manual | Yes | Months of billing covered (LC, escrow, liquidity facility) ≥ threshold |
| 9 | Grid connection and transmission readiness | Auto + manual | Yes | Connection agreement signed; line financed; timing gap ≤ threshold or deemed-energy allocation agreed |
| 10 | EPC signed: price basis, LDs, security, validity beyond close date | Manual | Yes | EPC term sheet checklist (Annex D); price validity date > expected close date |
| 11 | Contingency adequate | Auto | No | Contingency ≥ the model's risk-based requirement by lot |
| 12 | O&M arrangement and insurance placed | Manual | No | O&M contract/LTSA; insurance adviser report |
| 13 | Lender case passes | Auto | Yes (STOP test) | Minimum DSCR on lender case ≥ covenant; LLCR ≥ threshold |
| 14 | Dry-run test passes | Auto | Yes (STOP test) | Minimum DSCR ≥ 1.0x under multi-year drought with DSRA |
| 15 | Equity committed | Manual | Yes | Equity commitment letters / LCs; standby equity or overrun facility |
| 16 | FX, hedging and convertibility | Manual | No | Hedging strategy; central bank approvals; currency of tariff vs debt |
| 17 | Credit enhancement and political risk cover approved, with counter-indemnities recorded | Manual | No | Board approvals; indemnity agreements logged in the support register |
| 18 | Public support approved and fiscal screen signed | Auto + manual | Yes | Fiscal screen result not "high", or high with written MoF acceptance |
| 19 | Developer return at close ≥ hurdle, with development costs reimbursed as agreed | Auto | No (sponsor gate) | Equity IRR at close vs hurdle; reimbursement within lenders' cap |
| 20 | Legal opinions, direct agreements, security perfected | Manual | Yes | Lenders' counsel CP sign-off |
| 21 | Tax, regulatory and FX approvals | Manual | No | Tax stabilisation / incentives; exchange control approvals |
| 22 | Model integrity and audit | Auto + manual | Yes | Checks = OK; model auditor's report |

That gives 22 gates, 15 of them critical. The PAYGo book uses 23 gates with 13 critical. The count and the critical set are the author's design choice and should be documented as such, as the PAYGo suite plan does for P5 (decision D5).

### B9. Annexes and templates

| Annex | Content | Product link |
|---|---|---|
| A | Hydro project KPI and term dictionary (capacity concepts, P-values, availability, DSCR/LLCR/PLCR, MSP, readiness gap, rNPV, development premium) | Quick reference |
| B | Development budget template by stage and workstream, with stage probabilities | H2 calculator |
| C | Consents and permitting tracker | FC toolkit |
| D | EPC term sheet checklist (price basis, ground risk, LDs, caps, bonds, tests, validity) | FC toolkit |
| E | Hydro PPA and concession term sheet checklist (hydrology allocation, deemed energy, seasonal tariff, indexation, termination by event) | FC toolkit |
| F | Lender CP checklist and financial-close tracker | FC toolkit |
| G | Lender due-diligence data request (hydrology, technical, E&S, legal, insurance, model) | Lender DD toolkit |
| H | Investment memo template in two versions (developer IC; lender credit paper), twelve sections, recommendation and conditions first, readiness beside the recommendation | IC pack |
| I | Government support disclosure note (one page, PFRAM-compatible fields) | Public-side screen |
| J | Case library summary (current Annex A, reorganised by size and structure) | Case library |
| K | Model validation summary (replaces current Ch. 18; findings and fixes as a validation log) | Manual |
| L | Sources and verification status | — |
| M | Glossary | — |

### B10. Companion products ladder

This follows `13_PRODUCT_SUITE_PLAN.md`: one source, generators, inherited release gates, few products. Prices are assumptions to test. The only market evidence is the benchmark band in `competitive_intelligence.md` D (templates US$45 to 499; PF courses US$499 to 3,200; fiscal tools free).

| Level | Product | Built from | Effort |
|---|---|---|---|
| Book | Book 7 (Kindle, paperback) | This plan | L (rewrite) |
| Level 1: calculators | H1 Hydrology and energy-yield calculator (FDC, P-values one-year and multi-year, data-adequacy score) | HYD_DATA, HYDROLOGY | S to M |
| | H2 Development budget and rNPV calculator (stages, probabilities, development premium, partner entry price) | DEV_BUDGET, DEV_VALUE | M (new logic) |
| | H3 Tariff and LCOE calculator (energy-only, two-part, seasonal; plant vs system LCOE) | PPA_TARIFF, existing sheet 15 | S |
| | H4 Debt sizing calculator (sculpting, closed-form IDC, DSRA) | DEBT | S |
| Level 2: toolkits | T1 Financial close readiness toolkit (22 gates, CP tracker, consent tracker, EPC/PPA checklists) | FC_READINESS, CP_TRACKER, Annexes C to F | M |
| | T2 Lender due-diligence toolkit (data request, red flags, credit paper outline) | Annexes G, H | S to M |
| | T3 Public-side screen (MSP, routing, contingent liabilities, one-page MoF note; positioned as a PFRAM front end) | Existing sheets 11, 12, 22 to 26 | S (repackaging of current work) |
| Level 3: models | MODEL 7 Hydro IPP Development and Finance Model | Section C | L |
| | Lumora 400 MW PPP fiscal model (the current Bankable Hydro model, released as the public-sector edition) | Existing workbook | S once gates pass |
| Training | Video course (about 18 modules, mirroring PAYGo); quick reference guide | Book and model | M |

The existing *Bankable Hydro* text should not be sold as a second hydro book next to Book 7, because the two would cannibalise each other. Two options:
* Option (a): fold it into Chapter 15 and Annex I, and release the current model as the public-sector edition (T3 plus the Lumora model).
* Option (b): republish it as a short free policy paper that markets Book 7 to Ministry of Finance and DFI readers.

**(Reviewer judgement)** Option (b) costs little and builds credibility with exactly the institutions whose free tools the paper complements.

---

## C. Model additions (Model 7)

Architecture: monthly periodicity from first development spend to COD plus six months, then semi-annual through the debt life, then annual to the end of the concession. Today's model is annual throughout (current Ch. 18, "What we did not change"). Existing sheets that are reused are marked †. All formulas are written so that a reviewer can rebuild them, and none uses iteration. Notation: *s* = development stage, *m* = month, *t* = period, *k* = operating year.

### C1. Hydrology data adequacy (HYD_DATA, new)

* Inputs:
  * years of on-site record *N_site*, years of reference-gauge record *N_ref*;
  * share of missing months *g*;
  * correlation of monthly flows between site and reference gauge *R²*;
  * number of rating-curve gaugings;
  * years since last gauging;
  * lag-1 autocorrelation of annual energy *ρ*.
* Effective record length: *N_eff = N_site·(1−g) + N_ref·R²·λ*, with *λ* ≤ 1 a user discount for transferred records.
* Data uncertainty on mean energy: *σ_data = CV / √N_eff*, combined with a user model uncertainty *σ_model* (power curve, losses).
* Data-adequacy score: a weighted checklist mapped to Ready / Conditional / Gap / Critical, feeding Gate 1. This is the only weighted score in the model. It is shown component by component and the gate still takes the weakest test.
* Output: an energy uncertainty band that feeds C2.

### C2. Multi-year P-values and dry runs (HYDROLOGY†, GENERATION†)

* Effective independent years over horizon *n*: *n′ = n·(1−ρ)/(1+ρ)*.
* *n*-year P90 of mean energy: *P90_n = P50 × (1 − 1.2816 × √(CV²/n′ + σ_data² + σ_model²))*. The one-year P90 is the special case *n′ = 1* (current eq. 3.4, extended).
* Energy from a monthly series, not from mean flows. Compute *E_m = f(Q_m)* for each month of the (synthetic) record, then average, which removes the Jensen bias the current book describes but does not model.
* Dry-run generator: the worst consecutive *k*-year window in the record, or a user flow factor for *k* years. Output: minimum rolling *k*-year DSCR.

### C3. Configuration optimiser (CONFIG_OPT, new)

* For a grid of design flows *Q_d,i*: annual energy from the FDC, *E_i = Σ_m min(max(Q_m − Q_e,0), Q_d,i)·ρgHη·h_m*, capex *K_i = a + b·MW_i^c* (user cost curve), and LCOE_i and equity IRR_i at a fixed tariff.
* Output: the MW that maximises NPV or minimises LCOE. Uses a formula grid, no macro.

### C4. Development plan and stage-gate probabilities (DEV_PLAN, new)

* Stages *s* = 1 to 5, each with start month, duration *d_s*, probability of passing *p_s* (user input, labelled judgement) and dependencies.
* Probability of reaching stage *s*: *P_s = Π_{j<s} p_j*. Probability of financial close: *P_FC = Π_s p_s*.
* Probability-weighted COD: *E[COD] = Σ* over delay scenarios; critical path from the dependency table (MAX of predecessor finish dates).

### C5. Development budget by stage (DEV_BUDGET, new)

* Cost matrix *C_{s,w}* by stage and workstream *w* (hydrology, topography, geotech, ESIA/RAP, legal, PPA/concession, grid studies, financial advisory, team overhead, lender DD).
* Monthly spend from the stage schedule. Cumulative spend *CumDev_m*.
* Expected development spend: *E[Dev] = Σ_s P_s·Σ_w C_{s,w}*.
* Recoverable share *r_w* per workstream, reimbursed at close and subject to a lenders' cap *Cap_reimb* (a share of total uses, user input). Reimbursement at close: *Reimb = min(Σ_w r_w·Cost_w, Cap_reimb·Uses)*.
* Development fee: *DevFee = f·Capex*, with *f* a user input, labelled. It enters uses at close and must pass the lender cap.

### C6. Risk-weighted developer NPV and development premium (DEV_VALUE, new)

* Equity value at close to a buyer at required return *r_b*: *V_FC = NPV_{r_b}(equity distributions) − equity still to inject*.
* Developer rNPV at today (*t* = 0) with development discount rate *r_d*: *rNPV_0 = −Σ_m P_{s(m)}·Dev_m/(1+r_d)^{m/12} + P_FC·(V_FC + Reimb + DevFee)/(1+r_d)^{t_FC}*.
* Development premium at close: *DP = V_FC − Equity_injected_PV*, and per MW *DP/MW*. Development multiple: *(V_FC + Reimb + DevFee)/CumDev_FC*.
* Break-even probability of close: *P_FC* such that *rNPV_0 = 0* (closed form, since rNPV is linear in *P_FC* given fixed stage costs; solve analytically).
* Value step-up at milestone *s*: *V_s = (P_FC/P_s)·(V_FC + Reimb + DevFee)/(1+r_d)^{t_FC−t_s} − Σ_{j≥s} expected remaining costs*. This prices partner entry at each stage: partner share for contribution *X* at stage *s* = *X/(V_s + X)*.

### C7. Permits and contracts trackers (PERMITS, CONTRACTS, new)

* Each row holds: consent or contract, issuing body, prerequisite rows, status (not started / applied / granted / conditions), expiry, evidence location, signatory, date.
* Derived: earliest grant date = MAX(prerequisite grant dates) + processing time. A flag shows if expiry < debt maturity + tail.
* Contract consistency checks, for example: PPA term ≥ debt tenor + tail; PPA termination amount ≥ senior debt outstanding at each date; concession end ≥ PPA end; grid connection date ≤ COD; EPC long-stop ≤ PPA long-stop. Each is a TRUE/FALSE cell feeding Gate 7.

### C8. EPC contract structure (EPC, new)

* Lots *l* (civil, E&M, hydro-mechanical, owner's costs, transmission spur). Each has contract value *B_l*, price basis (fixed / remeasured / provisional sum) and contractor-retained risk share *θ_l* (1 for a true fixed price, lower where ground risk is excluded).
* Overrun scenario *o_l* (from the reference-class or user distribution). Owner-borne overrun: *OwnerOver_l = (1−θ_l)·o_l·B_l*.
* Delay LDs: *LD_delay = min(rate_l × days_late, cap_l × B_l)*. Performance LDs: *LD_perf = min(rate_perf × MW shortfall, cap_perf × B_l)*. Net owner delay cost = delay cost (C10) − LD_delay.
* Risk-based contingency requirement by lot at the user percentile: *Cont_l = B_l·(1−θ_l)·q_α(o_l)*. Gate 11 tests Σ funded contingency ≥ Σ *Cont_l*. The Nachtigal 20% funded contingency (PF-11) is shown as a single-case benchmark, not a norm.
* Multi-lot interface allowance: user percentage on the sum of lots, active only under the multi-lot option.

### C9. Monthly construction draw schedule (CONSTRUCTION_M, new; replaces the sine S-curve)

* Spend *S_m* from EPC milestone payments (percentage of *B_l* per milestone month) plus owner's costs.
* Funding order switch:
  * equity-first: *EqDraw_m = min(S_m + IDC_m + fees_m, EqCommit − CumEq_{m−1})*, *DebtDraw_m = S_m + IDC_m + fees_m − EqDraw_m*;
  * pro rata: *DebtDraw_m = g·(S_m + IDC_m + fees_m)*.
* *IDC_m = i/12·DebtBal_{m−1}*, plus commitment fee *cf/12·(Commit − DebtBal_{m−1})*. The model computes it on the prior balance, which avoids circularity without iteration. The current closed-form factor (eq. 11.3) is retained for the screening version.
* Overrun funding cascade: contingency, then standby equity, then cost-overrun facility, then gap. The gap is the financing gap reported by scenario.
* Checks: Σ sources = Σ uses at COD; debt drawn ≤ commitment; equity drawn ≤ commitment.

### C10. Delay and completion

* COD delay *δ* months adds *S* rescheduled, IDC and fees on the extended period, lost revenue *Σ Rev* for the delay months, and LD income from C8.
* Completion test: an availability or energy test over *x* consecutive days, as user inputs. Sponsor completion support releases when the test is passed.

### C11. O&M and MMRA (OM_MMRA, new; OPEX†)

* Major overhaul schedule (component, year, cost). MMRA target at *t* = PV of the next *h* years of overhaul spend, and funding *MMRA_fund_t = max(0, target_t − balance_{t−1})*, paid from CFADS before distributions.
* Availability: *Avail = 1 − planned − forced outage*, with a contract guarantee and a bonus/LD band.

### C12. Debt with DSRA, MMRA, waterfall and refinancing (DEBT†, CASHFLOW†)

* Semi-annual sculpting: *DS_t = CFADS^L_t / DSCR\**. Debt capacity = PV at all-in rate. Debt = min(capacity, gearing × uses).
* *DSRA target_t = DS_{t+1}* for the next 6 or 12 months, funded at close or from cash; drawn first in shortfalls (the current model's red-team fix, retained).
* Waterfall: opex, then taxes, then senior DS, then DSRA top-up, then MMRA, then lock-up test (DSCR ≥ lock-up), then distributions.
* Refinancing at year *R*: new tenor and margin. The refinancing gain *ΔNPV_equity* is computed with a user gain-share *γ* to the offtaker or tariff. Output: equity IRR with and without refinancing.
* Report the average DSCR alongside the minimum, with a flag if average/minimum exceeds a user ratio. That flags gearing-capped structures like the current Lumora base (1.64x minimum, 3.32x average).

### C13. Lender group and enhancements (DFI_ENH, new; STRUCTURES†)

* Tranches by lender type (A loan, B loan, ECA, local currency, concessional): amount, tenor, grace, margin, fees, currency.
* Enhancements:
  * guarantee or PRI premium (bp × covered amount);
  * cover limits;
  * liquidity facility months *L* (current eq. 8.4 cap, retained);
  * counter-indemnity flag that auto-posts the exposure to CONTINGENT.
* All-in cost of debt by tranche, and blended.

### C14. Developer returns and sell-down (EQUITY_RETURNS†, SELLDOWN, new)

* Developer cash flow vector: *−Dev_m* (at risk), *−Eq_m* (share), *+Reimb*, *+DevFee*, *+sale proceeds*, *+retained distributions*, *+promote*.
* Sale at milestone *τ* ∈ {FC, COD, post-refinancing} of share *σ*. Price = *σ·NPV_{r_b(τ)}(remaining distributions)*, where *r_b(τ)* falls with de-risking (user inputs by milestone, labelled).
* Promote: the developer receives *π* of distributions above a hurdle IRR *h* to co-investors (a standard tiered waterfall).
* Outputs: development IRR, equity IRR at close, multiple, peak equity, payback, rNPV (C6), and sale value by milestone.

### C15. Reverse stress (REVERSE_STRESS, new)

* Break-even flow factor: *φ*, such that min DSCR = 1.0, solved in closed form, because CFADS is linear in energy for an energy-only tariff: *φ* = (DS + opex + tax adjustment − fixed revenue) / variable revenue in the binding year. A data-table cross-check is included.
* Maximum overrun before the financing gap exceeds standby funding: *o* such that the gap = standby equity + overrun facility.
* Months of offtaker non-payment before DSRA plus liquidity facility are exhausted: *(DSRA + L × monthly bill) / (monthly bill − other cash)*.

### C16. CP tracker and financial-close readiness (CP_TRACKER, FC_READINESS, new)

* Each CP row holds: workstream, description, owner, status (open / in progress / satisfied / waived), evidence location, signatory, date, critical flag and long-stop.
* Derived:
  * % satisfied (count, and critical-only);
  * days to long-stop = long-stop − TODAY;
  * EPC price validity check (validity date − expected close date) feeding Gate 10;
  * hedging execution window.
* FC_READINESS: 22 gates (B8), each with type, critical flag, test cell or evidence fields. A manual gate counts only if Met plus evidence plus signatory. The decision follows the rule in B8 and is printed with its reason (failed test vs incomplete evidence).

### C17. Funds flow at close (SOURCES_USES†)

* Uses at close: development reimbursement, development fee, upfront and arrangement fees, DSRA initial funding (if funded at close), hedging costs, advisers' success fees, first EPC advance.
* Sources: equity at close, first debt draw. Check: sources = uses on the close date.

### C18. Public side (OFFTAKER†, GOVT_SUPPORT†, CONTINGENT†, FISCAL_SCREEN†)

Retain the current MSP (eq. 8.2), gap (8.3), routing (8.4 and 8.5), the three exposure measures (13.1), the consolidated perimeter and the four-test screen. Add:
* an export block shaped to PFRAM's input structure: annual government payments, guarantee exposures and termination amounts by scenario (field names to be checked against FR-03 before release);
* a "60 MW vs 400 MW" switch to show the scale effect in Chapter 15.

### C19. Checks (CHECKS†)

Carry over the existing 33_CHECKS logic and add:
* monthly sources = uses;
* DSRA/MMRA balance roll-forwards;
* development spend reconciles to DEV_BUDGET;
* stage probabilities in [0,1];
* sell-down shares sum to 100%;
* CP and gate counts reconcile;
* fault injection on each check (as the suite plan requires).

---

## D. Claims of novelty that would not survive a review, and how to avoid them

| # | Claim (current book or likely in Book 7) | Why a reviewer would reject it | How to avoid it |
|---|---|---|---|
| 1 | "Quantities that, as far as our review found, are not computed together elsewhere" (MSP, payment gap, readiness gap; current Ch. 1) | The review rests on public product descriptions, not hands-on testing (`competitive_intelligence.md`, methodology 4). DFI and guarantee appraisals assess offtaker finances as a matter of course, and the current book itself points to the IMF SOE health-check and stress-test tools (FR-11, FR-12). | Say "this book packages in one model..." and state the review date and method. Never "first" or "unique". Cite the tools the method draws on. |
| 2 | "A single analytical engine from river flow to fiscal exposure" as a unique contribution | The same evidence limit applies. PFRAM, LIC-DSF and project models together can do this, only not in one file. | Present integration as a convenience and a consistency check ("one set of assumptions"), not as a discovery. |
| 3 | "Risk is moved, not removed" / "risk is conserved" | This is the basic risk-allocation principle of project finance texts (Yescombe, Gatti; `competitive_intelligence.md` items 1 and 2). | Use it as framing with a citation, not as an insight. |
| 4 | The closed-form IDC that avoids circularity (eq. 11.3) | Modellers break the IDC circularity routinely (the current book says so: macro or iteration). Closed forms and prior-period interest are known techniques. | Call it "the method used in the model", with no novelty language. In Model 7, prefer prior-period monthly interest (C9). |
| 5 | "The Hydropower Bankability Framework" with nine gates as a named framework | It reads like a standard. The real arbiters are lenders' CP lists and credit committees. Stage-gate methods are generic. | Rename it "readiness gates". Use the PAYGo wording: evidence completeness, not rating. Document the gate set as an author design choice (PAYGo suite plan D5). |
| 6 | The consolidated fiscal perimeter including the utility as a book finding | The IMF Fiscal Transparency Code and DSF guidance already require SOE and contingent-liability coverage (FR-08, FR-09 with its SOE shock). | Present it as applying an existing principle at project level, and show the numerical effect. |
| 7 | "Grants without a tariff adjustment are a windfall" | This is a standard VGF and PPP design principle (PPP Reference Guide, FR-06). | Keep it as a worked illustration of a known rule. |
| 8 | "Gross public exposure barely changes across structures" | It is an identity, as the red-team review noted and the book now concedes. | Never present it as a finding. Present the composition and the timing of exposure as the result. |
| 9 | The Jensen bias and one-year P90 caveats as contributions | Both are standard hydrology and energy-yield practice. | Present them as reminders and model them properly (C2), and the model then adds value without the claim. |
| 10 | Book 7: "development premium", "risk-weighted NPV", "stage-gate probabilities" as new methods | These are standard in renewables M&A and other stage-gated industries. The repo holds no evidence base for hydro stage probabilities, development cost shares, success fees or premiums. | Call them standard tools applied to hydro. Label every probability and fee an illustrative input. Publish no "x% of hydro projects reach close" or "development costs are y% of capex" without a source added to the register. |
| 11 | "Ready for financial close" as a verdict | Only the lenders' CP satisfaction decides that. The model's gates are a proxy. | Use "readiness for a close decision". Print the PAYGo disclaimer that GO is evidence completeness, not a recommendation. |
| 12 | Typical covenant levels, contingency norms or tenors stated as market norms | The repo holds one appraisal (Nachtigal, PF-11) for DSCR and contingency, and one article for tenors (PF-13). The source database itself lists covenant levels as a known gap. | Label each "single-case benchmark" or "model input". Show the source count beside the number. |
| 13 | Applying the Ansar reference class (27% median / 96% mean) to a 60 MW run-of-river plant as if calibrated | The sample is 245 large dams (HY-08). | Use it as a sensitivity anchor with an explicit caveat. Add a mid-size evidence base before publication or say none was found. |
| 14 | "The first book on African hydro finance" or "the only hydro-specific finance book" | Chris Head's *Financing of Private Hydropower Projects* exists (item 6, date unverified). So do the IFC 2015 guide (item 9), the CLDP/ALSF handbooks (items 7 and 8) and ESMAP 2024 on private participation in large hydro (HY-06). | Position against them explicitly in the Preface with a short comparison table (what each covers, what Book 7 adds: development economics, EPC-to-debt linkage, the close process, and the model). |
| 15 | The red-team chapter framed as proof of rigour | Reviewers will read "passed every integrity check while defects were present" as a warning about the product. | Move it to a validation annex (K) written as a validation log with the independent recalculation, Excel test and fault injection required by the suite plan's release gates. |
| 16 | Figures seen only in summaries or snippets used in the argument (UT-01's "two viable sectors", FR-13's type split, UETCL deemed energy at 9%, Nachtigal shareholding changes) | These carry flags S or "search-result only" in the repo. | Apply the PAYGo rule: only verified claims feed a calculation or a diagnostic. Others appear with their caveat, and Annex L lists their status. |

**General rule for the Preface (Reviewer judgement):** replace "What the book adds: four contributions" with "What this book does differently". That section should make three claims that are true and checkable: (1) it follows a hydro project from first development spend to financial close and into operation, from the developer's, the lender's and the state's seats, in one decision sequence; (2) every number in the case comes from a model the reader holds; (3) every external figure carries a grade and a verification status. Those three survive review. Claims of being "first" or of finding a "new quantity" will not.
