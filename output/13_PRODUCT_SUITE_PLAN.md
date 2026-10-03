# 13 Product suite plan: Africa Energy Finance, PAYGo Finance Toolkit (Book 2)

Status: DRAFT 0.1, 3 October 2026. This is a planning document. It sets out what can be sold, what already exists, what has to be built and what must be proven first. It authorises no release.

Evidence labels:
* **Inventory:** checked in this repository.
* **Assumption:** a planning figure without market evidence, such as a price, a buyer group or a size of effort.
* **Decision:** a choice that belongs to the author.

Effort is sized S, M or L, relative to the work already done on Book 2 (Assumption):
* **S:** repackaging or small extensions to an existing product.
* **M:** a new workbook built from existing engines, with its own checks, manual and validation.
* **L:** new logic not present in any current product, with full validation.

---

## 1. Principles

1. **One source, many products.** Every Excel product is produced by a generator in `tools/`, as the model, calculators and templates are today. A correction is made once and rebuilt everywhere. Hand-edited copies are not sold.
2. **Release gates are inherited.** No product leaves pre-release before:
   * it has been tested in Microsoft Excel (or Word);
   * its numbers have been checked by an independent recalculation;
   * its text has passed the house text scan;
   * its manual exists.

   Nothing carries a 1.0 label before these gates (brief section 33).
3. **Evidence before verdict.** Products that rate a company use the readiness logic: evidence first, a decision on the completeness of the evidence, never an investment recommendation, a rating or "investment grade".
4. **Few products, kept current.** One model change in step 4 required updates to:
   * the manual and the case study;
   * three guides;
   * fourteen calculators and templates;
   * fifteen video modules.

   The number of products is the main driver of maintenance cost. Add a product only when a buyer group needs it.
5. **The book stays self-sufficient.** Products extend the book; the book never requires buying them (brief section 31).

## 2. Inventory: what already exists (Inventory)

| Asset | Content | State |
|---|---|---|
| Book 2, PAYGo Solar Finance | 117 pages, 16 chapters, 8 annexes, 15 figures | v0.2 pre-publication |
| MODEL 2 | 47 sheets, 100,857 formulas, 38 checks; credit, vintage, PERFORM_2026, RBF, FX, financing, valuation, readiness, benchmark engines | v0.8 development build |
| MANUAL 2 | User manual for MODEL 2 | For model v0.8-dev |
| CASE 2, SolaraPay | Worked case with synthetic 24 month history | For model v0.8-dev |
| D1 Price plan and APR calculator | Five plans; instalment, contract value, implied monthly rate, nominal APR, effective rate, burden against average and lean month income; solver for daily rate, target APR and tenor | 0.9 pre-release |
| D2 Unit economics calculator | 60 month cash flow of one sale; expected loss, lifetime contribution, LTV/CAC, payback, peak funding per unit, unit IRR and NPV; sensitivity grid; tier dashboard | 0.9 pre-release |
| D3 Repayment curve and cohort calibration | Curves from hazard, collection rate and tenor; grid calibration to observed cohorts; portfolio growth effect | 0.9 pre-release |
| D4 Receivables financing calculator | 60 month funding path with cohort matrix, facility against paying accounts, equity gap, currency sheet | 0.9 pre-release |
| D5 Investment screening scorecard | 12 criteria, 3 kill criteria, weights; verdict Decline, Incomplete, Proceed to diligence or Proceed with conditions | 0.9 pre-release |
| D6 Investor returns calculator | Stake, exit in LCY and USD, follow-on calls, multiple and IRR; maximum pre-money for a target IRR; IRR grid | 0.9 pre-release |
| T01 Investment committee memorandum | 12 sections, provenance table, readiness decision beside the recommendation | 0.9 pre-release |
| T02 Investor due diligence checklist | 50 items, 8 workstreams, evidence and red flag per item, summary | 0.9 pre-release |
| T03 Customer credit policy | 10 sections with parameter tables | 0.9 pre-release |
| T04 Agent economics and fully loaded CAC | Narrow and fully loaded CAC, agent ranking, new territory ramp | 0.9 pre-release |
| T05 Lender KPI report | PERFORM_2026 company-reported KPIs; operational and lender metrics with definitions | 0.9 pre-release |
| T06 Loan tape specification and data request | 27 fields, 9 account level checks, 13 standard requests | 0.9 pre-release |
| T07 Borrowing base certificate and term sheet checklist | Eligibility, advance rates by tier, concentration limit, headroom; 12 terms | 0.9 pre-release |
| T08 PAYGo business model canvas | Canvas plus credit engine, funding stack, impact, key metrics | 0.9 pre-release |
| Quick reference guide | 15 pages | Aligned with v0.8 |
| Video course | 18 modules; Module 17 model walkthrough | Being refreshed |

Not present in any product (Inventory, checked in the model generator):
* securitisation tranching, waterfall or triggers (the model treats securitisation on balance sheet with a rate, an advance haircut and a fee);
* consumer, supplier or connection subsidy designs (the model's RBF designs are sales-based, repayment-linked, ownership-linked and hybrid);
* web software of any kind.

## 3. Catalogue: proposed products, basis and gaps

| # | Product | Level | Main buyers (Assumption) | Built from | Gap to close | Effort | Recommendation |
|---|---|---|---|---|---|---|---|
| P1 | PAYGo Unit Economics Calculator | 1 | Founders, analysts, students | D2 (and D1 for pricing) | Gross margin at sale; break-even collection rate; maximum affordable CAC; one page summary; buyer manual | S | Phase 1 |
| P2 | PAYGo Pricing and Affordability Simulator | 1 | Founders, product managers, programme designers | D1 plus D2 engine | Grid of deposit by tenor showing burden, expected loss and unit IRR together, without macros (formula grid) | S to M | Phase 2 |
| P3 | PAYGo Investor Returns Calculator | 1 | Angel and fund analysts | D6 | Packaging, manual | S | Phase 1 |
| P4 | PAYGo Due Diligence Toolkit | 2 | Investors, DFIs, lenders | T02, T06, T01, D5 | One workbook: the 16 tabs proposed, with workstreams from T02, the tape and request from T06, red flags, a readiness summary and the memo outline from T01 | S to M | Phase 1 (pack), Phase 2 (single workbook) |
| P5 | PAYGo Investment Readiness Toolkit | 2 | Investors, DFIs, fund managers, companies preparing to raise | MODEL 2 readiness sheet; D5 scorecard | Standalone input sheets for the 23 gates without the full model; data quality assessment; gap list; financing implications; committee pack export | M | Phase 2: most distinctive product |
| P6 | PAYGo Credit Risk and Portfolio Model | 3 | PAYGo lenders, credit teams, PAYGo CFOs | MODEL 2 credit, cohort and vintage engines; Credit_Input and Vintage_Input; D3 | Extraction into a lean workbook; loss waterfall; portfolio ageing; credit stress; own checks and validation | M | Phase 3 |
| P7 | PAYGo Receivables Facility Model | 3 | Banks, debt funds | D4, T07, MODEL 2 Financing and borrowing base | Monthly borrowing base with concentration limits, reserve account, interest, amortisation, covenant tests and headroom; lender reporting outputs | M | Phase 3 |
| P8 | PAYGo Company Financial and Investment Model | 3 | CFOs, CEOs, investors | MODEL 2 as is | Excel test, external model review, buyer licence | S once gates pass | Phase 2 (after the gates) |
| P9 | PAYGo KPI Dashboard | 2 | Operators, lenders | T05 | Monthly history and charts; Power BI out of scope for now | S to M | Phase 3 |
| P10 | PAYGo Credit Policy Template | 1 | PAYGo companies | T03 | Packaging | S | Phase 1 (in the pack) |
| P11 | PAYGo RBF Simulator (four outcome designs) | 3 | Programme managers, DFIs | MODEL 2 RBF_Engine and claim cycle | Standalone programme view: cost per verified outcome, timing, company cash gap, investor IRR effect | M | Phase 4 |
| P12 | Subsidy design comparison (consumer, supplier, connection, results-based) | 3 | Governments, DFIs | Not present | New logic and evidence base | L | Later, only on a client request |
| P13 | PAYGo Securitisation Model (tranches, waterfall, triggers) | 3 | Structured finance investors | Not present (only on-balance-sheet treatment) | New model, legal and structuring input, full validation | L | Later, only with a co-author or client with transaction experience |
| P14 | Data Quality and Calibration Engine | 2 | Investors | MODEL 2 Calibration, Source_Register, Benchmark sheets; D3 | Assumption, source, evidence, actual, variance and calibration status table for any company file | M | Phase 4, or as a module of P5 |
| P15 | Investment Committee Pack and memo generator | 2 | Investment teams | T01; MODEL 2 Investment_Summary and Dashboard | Automatic filling of the memo from model outputs. A document generator is software, not a template | M to L | Phase 4: start as a linked template, not a generator |
| P16 | Training course | 2 | Professionals | Video course | Platform, assessment, certificate wording (no accreditation claim) | M | Phase 3 |
| P17 | Web application | 3 | Investors, DFIs | Not present | Software, hosting, security, data protection, support | L | Not before the Excel products sell |

Two corrections to earlier ideas:
* **P6 scope.** P6 is a PAYGo credit model built on lockout, account-age hazard and repossession. It should not be sold as a general consumer credit or microfinance model.
* **P12 and P13 status.** They are not extractions. They are new products.

## 4. Ladder and bundles (prices are Assumptions to test)

| Level | Products | Indicative price (USD) |
|---|---|---|
| Book | Book 2 (Kindle, paperback) | 13 to 30 |
| Level 1: calculators | P1, P2, P3, P10 | 9 to 29 each |
| Level 2: toolkits | P4, P5, P9, P14 | 49 to 149 each |
| Level 3: models | P6, P7, P8, P11 | 149 to 499 each |

| Bundle | Content | Indicative price (USD) |
|---|---|---|
| Starter pack | P1, P3, P10, D1, T04, T08 | 39 to 79 |
| Investor toolkit | P4, P5, P3, T01 | 149 to 299 |
| Operator toolkit | P1, P2, P9, T03, T04, T06 | 149 to 299 |
| Master suite | Book, MODEL 2, MANUAL 2, CASE 2, investor and operator toolkits, P6, P7, video course | 399 to 799 |

* **Institutional licence:** a per-organisation price (Decision) for funds and DFIs, with use by a named team, no redistribution and no warranty.
* **No market data.** No price above rests on market evidence. Section 9 lists how to test them.

## 5. Sequencing and exit criteria

| Phase | Content | Exit criteria |
|---|---|---|
| 0. Gates | Excel test of MODEL 2, D1 to D6, T01 to T08; Word test of the .docx templates; licence text; privacy policy; landing page | Test log recorded; every product opens, recalculates and prints in Excel or Word without repair prompts |
| 1. Starter and DD pack | P1 (with the two additions), P3, P10 and the DD pack (T02, T06, T01, D5) | Generator rebuilds; independent recalculation of the additions; buyer manual; five external testers |
| 2. Distinctive products | P5 Readiness Toolkit; P8 full model released; P4 as a single workbook; P2 | P5 decision paths tested as in the model (failed test, incomplete, conditional, all gates); external review of P8 |
| 3. Professional models | P6 Credit Risk; P7 Receivables Facility; P9 KPI Dashboard; P16 training | Each model has its own checks, fault injection, a manual and a worked example reconciled to the book |
| 4. Institutional | P11 RBF Simulator; P14 Calibration; P15 memo linking | Driven by client demand |
| Later | P12, P13, P17 | Only with a client, a partner or evidence of demand |

## 6. Specifications for the five priority products

### P1 PAYGo Unit Economics Calculator (from D2)

**Inputs** (already in D2): cash price, hardware cost, deposit, daily rate, tenor, CAC, installation, servicing, mobile money fees, default hazard, collection rate, repossession and recovery, RBF, discount rate.

**Missing inputs:** an FX path for USD hardware and an optional cost of capital line.

**Outputs:**
* Already in D2: lifetime contribution, expected loss rate, cash payback month, peak funding per unit, unit NPV, unit IRR, LTV/CAC.
* To add: gross margin at sale, break-even collection rate (the rate at which lifetime contribution is zero) and maximum affordable CAC (the CAC at which LTV/CAC equals a target).

**Validation:**
* The closed form check that already exists.
* The two new outputs solved twice: once with a formula, once by an independent recalculation.

**Effort:** S.

### P4 PAYGo Due Diligence Toolkit (from T02, T06, T01, D5)

**Tabs:**
* Company;
* commercial, customer, credit, portfolio, financial, regulatory, technology, ESG and consumer protection, RBF, funding, FX;
* data quality, from the T06 tape checks;
* red flags, from T02;
* readiness summary, from the P5 logic once available, D5 before;
* IC memo outline, from T01.

**Rule:** no workstream is scored on missing evidence; open items stay visible.

**Effort:** S as a pack of existing files, M as one workbook.

### P5 PAYGo Investment Readiness Toolkit (from MODEL 2)

**Inputs:**
* company profile;
* years of operation;
* units sold and active customers;
* PERFORM 2026 results if computed by the company;
* cohort coverage;
* receivables and DPD buckets;
* statements available, and whether audited;
* debt and equity, FX exposure;
* licences;
* consumer protection evidence;
* RBF contracts;
* data quality (from the T06 checks);
* governance.

For every gate: the evidence, where it is held, who signed it off and the date.

**Outputs:**
* evidence completeness by area;
* the 23 gates;
* the decision on evidence (GO, CONDITIONAL GO, STOP with reason);
* key gaps;
* financing implications, written as text rules (for example: no cohort data means a receivables facility is premature);
* recommended diligence actions;
* a one page committee summary.

**Validation:**
* The four decision paths tested as in the model.
* A manual gate marked Met without evidence must not count.
* Gate definitions and the 13 critical gates documented as a design choice of the author.

**Wording:**
* "Readiness" and "evidence completeness".
* Never "rating", "score of investability" or "investment grade".

**Effort:** M.

### P6 PAYGo Credit Risk and Portfolio Model (from MODEL 2)

**Chain:** Inputs > credit engine > cohort engine > vintage dashboard > portfolio risk > stress.

**Outputs:**
* default rate;
* operational collection rate, labelled as not a PERFORM KPI;
* cohort repayment curves;
* PAR and DPD;
* LGD proxy and expected loss;
* vintage comparison and portfolio ageing;
* credit stress;
* a loss waterfall.

**Statement:** the accounting statement is carried over verbatim.

**Validation:**
* Checks carried over from MODEL 2: rows 18 to 22, 25, 29, 30 and 34 to 37.
* Fault injection on each.
* A worked example that reproduces the book's Chapter 6 and 7 figures.

**Effort:** M.

### P7 PAYGo Receivables Facility Model (from D4, T07, MODEL 2)

**Chain:** eligible receivables > advance rate by tier > concentration limits > reserve > borrowing base > drawings and repayments > interest and fees > amortisation > covenant tests > headroom.

**Outputs:**
* monthly borrowing base certificate;
* covenant dashboard;
* headroom;
* months in breach;
* lender report pack, linked to T05.

**Validation:**
* Reproduce the Chapter 11 worked borrowing base (base 1,611; headroom 111; 32 after the DPD shift).
* Facility roll forward check.
* Limit checks.

**Effort:** M.

## 7. Production architecture

* **Generators.** One generator per product, sharing the formatting and QA library already used (house style, text scan, footer, document properties). The product version is set in one place.
* **QA per release:**
  * LibreOffice recalculation without errors;
  * independent recalculation of key outputs;
  * fault injection on each check;
  * Excel or Word test log;
  * text scan;
  * changelog entry.
* **Versioning.** Product versions follow the model: 0.9 pre-release, 1.0 only after the gates. A product states the MODEL 2 version its engines come from.
* **Licence and support:**
  * licence per product and per organisation;
  * an errata page;
  * a support channel with a stated response time (Decision).
* **Delivery:** off Amazon, via the Africa Energy Finance site. Amazon carries the book only (12 Amazon pack).

## 8. Replication across the collection

The pattern (book, model, manual, case, calculators, toolkits) can be repeated for Books 1 and 3 to 6. Two cautions:
* No material for those books exists in this repository beyond their titles and central questions. Every product listed for them in the proposal is new work (effort L) and needs its own sources.
* Build each collection book's product line only after its book and model pass their own gates. Do not open five product lines in parallel.

## 9. Evidence to collect before pricing and building beyond Phase 1

| Question | Method | Decides |
|---|---|---|
| Who pays, and how much, for P5 and P4 | 10 interviews (funds, DFIs, banks, PAYGo CFOs); 2 paid pilots | Phase 2 scope and price |
| Is P7 or P6 more wanted by lenders | 5 lender interviews | Phase 3 order |
| Which platform suits paid Excel files (own site, Gumroad or similar) | Compare fees, tax handling, licence delivery | Phase 1 delivery |
| Institutional licence terms | Legal review | All Level 3 products |

## 10. Risks

| Risk | Mitigation |
|---|---|
| Selling a tool before its Excel test | Gate 0 for every product |
| Liability when a tool rates a real company | Evidence-only wording; licence disclaimer; no recommendation language |
| Maintenance load across many products | Generators; few products; one source of engines |
| Products drifting from the book | Each manual names the book chapter and the model version it follows; changelog per product |
| Overpromising scope (general credit model, securitisation, web) | Scope statements in each product page; P12, P13 and P17 deferred |
| Unverified external figures inside products | Same source register and statuses; only VERIFIED claims used as references |

## 11. Decisions for the author

| # | Decision |
|---|---|
| D1 | Approve Phase 0 and Phase 1 scope |
| D2 | Product names: "PAYGo Finance Toolkit" under Africa Energy Finance, or another name |
| D3 | Delivery platform and licence model |
| D4 | Prices to test |
| D5 | Whether P5 counts the 13 critical gates as proposed, or takes another set |
| D6 | Whether to seek a partner for P13 (securitisation) |
