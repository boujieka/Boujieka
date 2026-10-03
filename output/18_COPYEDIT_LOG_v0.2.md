# Copyedit log, Book 2 (PAYGo Solar Finance), version 0.2

**Cover note.** This is an AI line copyedit, not a professional copyedit. It was carried out on the chapter sources (ch00_front.md, ch00b_intro.md, ch01.md to ch16.md, ch99_annexes.md) in British English against the house style. It does not replace a human copyeditor: release gate B7 stays open until a professional copyeditor has reviewed the text. Nothing here is a practitioner review, a legal opinion or a check of the figures.

**Scope and limits.** Wording only. No number, figure reference, table value, source reference (E1, E4, etc.), sheet or cell name, chapter or section number, or Annex G status was changed; a script compared every number and every source and sheet reference in each file before and after the edit, and the only reference-level difference is the wording of the section 2.6 heading ("Multi Tier" to "Multi-Tier"). No claim was added or removed. The text was already in British spelling (-ise, -our, licence/license, programme, instalment) and contained no em or en dashes, spaced hyphens or repeated words, so most changes are consistency and clarity edits.

**Rebuild.** `python tools/build_book2.py` ends "text scan clean"; the published PDF (output/01_BOOK_PAYGO_SOLAR_FINANCE_v0.2.pdf) has 118 pages (117 at the last commit; other working tree changes, such as the figure script, may also contribute).

## Summary of changes by type

| Change type | Count |
|---|---|
| abbreviation defined | 70 |
| terminology | 26 |
| long sentence split | 11 |
| Markdown formatting | 11 |
| glossary entry added (abbreviation) | 5 |
| capitalisation (cross reference) | 4 |
| punctuation (clarity) | 3 |
| serial comma consistency | 3 |
| hyphenation consistency | 3 |
| table header consistency | 3 |
| abbreviation consistency | 2 |
| repetition | 1 |
| grammar | 1 |
| serial comma | 1 |
| capitalisation | 1 |
| grammar (article) | 1 |
| abbreviation expanded | 1 |
| **Total edits (some edits carry two types)** | **139** |

Notes on conventions applied:

* Abbreviations defined on first use in each chapter where the chapter used them undefined: DPD, ECL, RBF, LCY, DSCR, LGD, PD, PAR, APR, CAC, FX, FOB, SPV, DFI, MOIC, LTV/CAC, DCF, MTF. Definitions follow the wording already used elsewhere in the book and in Annex H.
* "Repayment Rate" capitalised wherever the text means the PAYGo PERFORM 2026 KPI (as in the GOGLA guide and the companion materials); left in lower case where it means a generic or programme repayment measure (for example the RBF "repayment rate at verification", "repayment rates by cohort").
* "Operational collection rate" introduced at the definition in section 7.3 and in three table labels, matching the case study, quick reference and model labels. Elsewhere "collection rate" is kept as the short form, and the ESMAP sector "collection rate" is left as reported.
* "Multi-Tier Framework" hyphenated as in the ESMAP name and Annex G (E3). Proper names with hyphens (Off-Grid Solar Market Trends Report, M-KOPA, M-Kopa Holdings Limited) were not changed.
* Cross references normalised to lower case "section 16.9" mid-sentence, as used in Chapters 2 to 6.
* Serial comma: the book does not use it in simple lists; two stray serial commas removed. Serial commas that separate complex items (for example "legality, and health and safety") were kept.
* Sentences over about 45 words: eleven split. The rest over 45 words are colon or semicolon lists (data tape fields, covenant sets, conditions precedent) or sentences carrying a source label (Sun King and d.light in Chapters 3 and 11, ESMAP in Chapter 15); splitting those would separate a figure from its source tag, so they were left for the human copyeditor.
* Eleven double blank lines before figures collapsed to one (no effect on the PDF layout expected).

## Changes the author should check (possible effect on meaning)

Each of these is believed to preserve meaning, but each changes sentence structure or adds wording. Before and after are given in full.

1. **ch00_front.md** (long sentence split)
   * Before: The book has a companion workbook, MODEL 2, the PAYGo Company Financial and Investment Model (version 0.8, in development at the time of this edition; the projections and valuations quoted in the book are identical in the released version 0.7, while the readiness results, the treatment of external references and the integrity checks follow version 0.8), together with a user manual and a worked case study on SolaraPay Ltd, a fictional company in the fictional Republic of Kivara.
   * After: The book has a companion workbook, MODEL 2, the PAYGo Company Financial and Investment Model, together with a user manual and a worked case study on SolaraPay Ltd, a fictional company in the fictional Republic of Kivara. The workbook is at version 0.8, in development at the time of this edition; the projections and valuations quoted in the book are identical in the released version 0.7, while the readiness results, the treatment of external references and the integrity checks follow version 0.8.

2. **ch02.md** (abbreviation defined; terminology)
   * Before: the deposit as a screening device, the implied APR, the Multi Tier Framework and the data
   * After: the deposit as a screening device, the implied annual percentage rate (APR), the Multi-Tier Framework (MTF) and the data

3. **ch02.md** (terminology)
   * Before: labelled by the capacity attribute of ESMAP's Multi Tier Framework.
   * After: labelled by the capacity attribute of ESMAP's Multi-Tier Framework.

4. **ch02.md** (terminology)
   * Before: ## 2.6 The Multi Tier Framework

ESMAP's Multi Tier Framework,
   * After: ## 2.6 The Multi-Tier Framework

ESMAP's Multi-Tier Framework,

5. **ch02.md** (long sentence split)
   * Before: as affordable "at a stretch", and on that basis to find that a Tier 1
   * After: as affordable "at a stretch". On that basis it is reported to find that a Tier 1

6. **ch04.md** (long sentence split; grammar; serial comma)
   * Before: change the plan so that the instalment falls within the affordability threshold for the customers actually being sold to, which may mean a smaller product, a lower premium, a higher deposit for some segments, or a different target customer, and then to test the redesign on new cohorts before scaling it. The case's conditions also require FX indexation
   * After: change the plan so that the instalment falls within the affordability threshold for the customers actually being sold to. That may mean a smaller product, a lower premium, a higher deposit for some segments or a different target customer, and the redesign should then be tested on new cohorts before it is scaled. The case's conditions also require foreign exchange (FX) indexation

7. **ch07.md** (long sentence split)
   * Before: on the *PERFORM_2026* sheet, which aggregates them by adding numerators and denominators, as the standard requires, and shows beside them
   * After: on the *PERFORM_2026* sheet. That sheet aggregates them by adding numerators and denominators, as the standard requires, and shows beside them

8. **ch07.md** (terminology)
   * Before: The collection rate for a period is the cash collected
   * After: The operational collection rate for a period is the cash collected

9. **ch10.md** (long sentence split)
   * Before: the translation of LCY results into USD; a memo row shows
   * After: the translation of LCY results into USD. A memo row shows

10. **ch11.md** (long sentence split; terminology)
   * Before: along with receivables at risk and write offs; the 2026 standard does not include them and forbids presenting a collection rate as the repayment rate (Chapter 7).
   * After: along with receivables at risk and write offs. The 2026 standard does not include them and forbids presenting a collection rate as the Repayment Rate (Chapter 7).

11. **ch11.md** (long sentence split; capitalisation)
   * Before: (0 = none, 1 = operating cash flow, 2 = cash basis excluding growth in PAYGo receivables): use the facility's own definition, and note that basis 0 models a facility without a DSCR test, as Section 16.9 recommends
   * After: (0 = none, 1 = operating cash flow, 2 = cash basis excluding growth in PAYGo receivables). Use the facility's own definition, and note that basis 0 models a facility without a DSCR test, as section 16.9 recommends

12. **ch12.md** (long sentence split)
   * Before: with an SPV purchasing PAYGo receivables; it reports cumulative solar loans
   * After: with an SPV purchasing PAYGo receivables. It reports cumulative solar loans

13. **ch12.md** (long sentence split)
   * Before: covering Kenya, Tanzania and Uganda; the 718m is purchasing capacity, not debt raised.
   * After: covering Kenya, Tanzania and Uganda. The 718m is purchasing capacity, not debt raised.

14. **ch14.md** (long sentence split)
   * Before: and does not recalculate when inputs change; its live row shows
   * After: and does not recalculate when inputs change. Its live row shows

15. **ch16.md** (long sentence split; terminology)
   * Before: Either way it should replace the DSCR test, which the projection fails in Years 1 to 4, with portfolio covenants and monthly reporting of the operational and lender metrics (collection rate, receivables at risk, write offs), each with its definition printed, and of the PAYGo PERFORM 2026 KPIs
   * After: Either way it should replace the DSCR test, which the projection fails in Years 1 to 4, with portfolio covenants. It should also require monthly reporting of the operational and lender metrics (operational collection rate, receivables at risk, write offs), each with its definition printed, and of the PAYGo PERFORM 2026 KPIs

16. **ch16.md** (abbreviation expanded)
   * Before: | ESMAP MTR 2024, reported average
   * After: | ESMAP Off-Grid Solar Market Trends Report 2024, reported average

17. **ch99_annexes.md** (glossary entry added (abbreviation))
   * Before: | Advance rate | Share of eligible receivables a lender will fund |

   * After: | Advance rate | Share of eligible receivables a lender will fund |
| APR | Annual percentage rate |


18. **ch99_annexes.md** (glossary entry added (abbreviation))
   * Before: | Borrowing base | Maximum facility drawing allowed by eligible receivables and advance rates |

   * After: | Borrowing base | Maximum facility drawing allowed by eligible receivables and advance rates |
| CAC | Customer acquisition cost |


19. **ch99_annexes.md** (glossary entry added (abbreviation))
   * Before: | DPD | Days past due |

   * After: | DPD | Days past due |
| DSCR | Debt service coverage ratio |


20. **ch99_annexes.md** (glossary entry added (abbreviation))
   * Before: | First loss | Tranche or equity that absorbs losses before any other investor |

   * After: | First loss | Tranche or equity that absorbs losses before any other investor |
| FX | Foreign exchange |
| LCY | Local currency of the generic model (KVS in the SolaraPay case) |


21. **ch99_annexes.md** (glossary entry added (abbreviation))
   * Before: | LGD | Loss given default |

   * After: | LGD | Loss given default |
| MTF | Multi-Tier Framework (ESMAP) |


Items noted but not changed (for the author):

* ch00b_intro.md, "Six questions": the text quotes "bankable" as a word others use ("described as \"profitable\" or \"bankable\""). House style says never use "bankable"; here it is mentioned, not used, so it was left. The author may prefer to rephrase.
* ch15.md, ESG workstream: "a DFI's ESG team" leaves DFI and ESG undefined in that chapter (DFI is defined in Chapters 3 and 14).
* "LTV/CAC" (Chapters 4, 9) and "LTV to CAC" (Chapters 5, 16, Annex A) are both used; the model label should decide which one to keep.
* "term ABS" (Chapters 11, 12) is not expanded.
* ch16.md, conditions summary: "one addresses affordability, one price, and one creates the data" keeps its serial comma, because removing it makes the clause harder to read.

## Full list of edits

| # | File | Type | Before | After |
|---|---|---|---|---|
| 1 | ch00_front.md | abbreviation defined | the programme managers who design results based financing. | the programme managers who design results based financing (RBF). |
| 2 | ch00b_intro.md | abbreviation defined | \| RBF \| Does subsidy money | \| Results based financing (RBF) \| Does subsidy money |
| 3 | ch01.md | punctuation (clarity) | sells a physical product, a panel, a battery, a controller and a set of appliances, to a household | sells a physical product (a panel, a battery, a controller and a set of appliances) to a household |
| 4 | ch01.md | abbreviation defined | Ownership matters to impact investors and results based financing programmes, | Ownership matters to impact investors and results based financing (RBF) programmes, |
| 5 | ch01.md | abbreviation defined | the observed LGD proxy is about 99% | the observed loss given default (LGD) proxy is about 99% |
| 6 | ch01.md | terminology | is not the repayment rate defined by the PAYGo PERFORM standard | is not the Repayment Rate defined by the PAYGo PERFORM standard |
| 7 | ch01.md | abbreviation defined | fails the lender's annual DSCR test | fails the lender's annual debt service coverage ratio (DSCR) test |
| 8 | ch01.md | repetition | Then use the *Dashboard* and *KPIs* sheets to see the company as management presents it, then go to | Then use the *Dashboard* and *KPIs* sheets to see the company as management presents it, and go to |
| 9 | ch00_front.md | long sentence split | The book has a companion workbook, MODEL 2, the PAYGo Company Financial and Investment Model (version 0.8, in development at the time of this edition; the projections and valuations quoted in the book are identical in the released version 0.7, while the readiness results, the treatment of external references and the integrity checks follow version 0.8), together with a user manual and a worked case study on SolaraPay Ltd, a fictional company in the fictional Republic of Kivara. | The book has a companion workbook, MODEL 2, the PAYGo Company Financial and Investment Model, together with a user manual and a worked case study on SolaraPay Ltd, a fictional company in the fictional Republic of Kivara. The workbook is at version 0.8, in development at the time of this edition; the projections and valuations quoted in the book are identical in the released version 0.7, while the readiness results, the treatment of external references and the integrity checks follow version 0.8. |
| 10 | ch02.md | abbreviation defined; terminology | the deposit as a screening device, the implied APR, the Multi Tier Framework and the data | the deposit as a screening device, the implied annual percentage rate (APR), the Multi-Tier Framework (MTF) and the data |
| 11 | ch02.md | terminology | labelled by the capacity attribute of ESMAP's Multi Tier Framework. | labelled by the capacity attribute of ESMAP's Multi-Tier Framework. |
| 12 | ch02.md | terminology | ## 2.6 The Multi Tier Framework /  / ESMAP's Multi Tier Framework, | ## 2.6 The Multi-Tier Framework /  / ESMAP's Multi-Tier Framework, |
| 13 | ch02.md | long sentence split | as affordable "at a stretch", and on that basis to find that a Tier 1 | as affordable "at a stretch". On that basis it is reported to find that a Tier 1 |
| 14 | ch02.md | abbreviation consistency | The implied annual percentage rate is the figure | The implied APR is the figure |
| 15 | ch03.md | abbreviation defined | is a cost and a timing risk. An APR cap is | is a cost and a timing risk. An annual percentage rate (APR) cap is |
| 16 | ch03.md | abbreviation defined | such as a financing subsidiary or an SPV. | such as a financing subsidiary or a special purpose vehicle (SPV). |
| 17 | ch03.md | abbreviation defined | shows an observed LGD proxy of about 99% | shows an observed loss given default (LGD) proxy of about 99% |
| 18 | ch03.md | abbreviation defined | exclusion from results based financing programmes or DFI funding | exclusion from results based financing (RBF) programmes or development finance institution (DFI) funding |
| 19 | ch03.md | abbreviation defined | as a percentage of FOB cost | as a percentage of free on board (FOB) cost |
| 20 | ch03.md | punctuation (clarity) | would force the company to raise the cash price, which moves margin from financing income to hardware revenue but does not change what the customer pays, or to accept a lower return on the product, or to withdraw it. | would force the company to raise the cash price (which moves margin from financing income to hardware revenue but does not change what the customer pays), to accept a lower return on the product or to withdraw it. |
| 21 | ch03.md | abbreviation defined | holds the recovery cost and the DPD definitions | holds the recovery cost and the days past due (DPD) definitions |
| 22 | ch04.md | abbreviation defined | \| Implied APR \| From the annuity equation in Chapter 2 \| | \| Implied annual percentage rate (APR) \| From the annuity equation in Chapter 2 \| |
| 23 | ch04.md | abbreviation defined | Calibrated unit economics give them the best ratios in the range: LTV/CAC of 11.0x and 14.9x, and unit IRRs of 67% and 54%. But they have no history, and doubling their hazard cuts the investor IRR in the calibrated case from 29.0% to 14.8%, and the MOIC from | Calibrated unit economics give them the best ratios in the range: lifetime value to customer acquisition cost (LTV/CAC) of 11.0x and 14.9x, and unit IRRs of 67% and 54%. But they have no history, and doubling their hazard cuts the investor IRR in the calibrated case from 29.0% to 14.8%, and the multiple on invested capital (MOIC) from |
| 24 | ch04.md | punctuation (clarity) | and selling them a second product, an upgrade to a larger system or an appliance on a short plan, is the cheapest | and selling them a second product (an upgrade to a larger system or an appliance on a short plan) is the cheapest |
| 25 | ch04.md | long sentence split; grammar; serial comma | change the plan so that the instalment falls within the affordability threshold for the customers actually being sold to, which may mean a smaller product, a lower premium, a higher deposit for some segments, or a different target customer, and then to test the redesign on new cohorts before scaling it. The case's conditions also require FX indexation | change the plan so that the instalment falls within the affordability threshold for the customers actually being sold to. That may mean a smaller product, a lower premium, a higher deposit for some segments or a different target customer, and the redesign should then be tested on new cohorts before it is scaled. The case's conditions also require foreign exchange (FX) indexation |
| 26 | ch05.md | abbreviation defined | The workbook defines customer acquisition cost on *Unit_Economics* | The workbook defines customer acquisition cost (CAC) on *Unit_Economics* |
| 27 | ch05.md | abbreviation defined | if the agent's 30+ DPD ratio exceeds | if the agent's 30+ days past due (DPD) ratio exceeds |
| 28 | ch06.md | abbreviation defined | (cohorts, survival curves, DPD buckets and roll rates) | (cohorts, survival curves, days past due (DPD) buckets and roll rates) |
| 29 | ch06.md | abbreviation defined | appear only in the indicative stage based ECL, | appear only in the indicative stage based expected credit loss (ECL), |
| 30 | ch06.md | serial comma consistency | moved, sold the device, or decided the debt | moved, sold the device or decided the debt |
| 31 | ch07.md | terminology | \| Repayment rate, paid versus plan (RR PvP) \| | \| Repayment Rate, paid versus plan (RR PvP) \| |
| 32 | ch07.md | terminology | \| Repayment rate, paid versus financed (RR PvFin) \| | \| Repayment Rate, paid versus financed (RR PvFin) \| |
| 33 | ch07.md | terminology | 1. Repayment rates exclude deposits | 1. Repayment Rates exclude deposits |
| 34 | ch07.md | terminology | must not be used in place of the repayment rate. | must not be used in place of the Repayment Rate. |
| 35 | ch07.md | terminology | First, a repayment rate is a contract level calculation | First, a Repayment Rate is a contract level calculation |
| 36 | ch07.md | terminology; abbreviation defined | so results based financing paid to the company never improves its repayment rate (Chapter 13). | so results based financing (RBF) paid to the company never improves its Repayment Rate (Chapter 13). |
| 37 | ch07.md | long sentence split | on the *PERFORM_2026* sheet, which aggregates them by adding numerators and denominators, as the standard requires, and shows beside them | on the *PERFORM_2026* sheet. That sheet aggregates them by adding numerators and denominators, as the standard requires, and shows beside them |
| 38 | ch07.md | terminology | The collection rate for a period is the cash collected | The operational collection rate for a period is the cash collected |
| 39 | ch07.md | terminology | but under the 2026 standard it may not stand in for the repayment rate. | but under the 2026 standard it may not stand in for the Repayment Rate. |
| 40 | ch07.md | abbreviation defined | A company that writes off at 180 DPD will show | A company that writes off at 180 days past due (DPD) will show |
| 41 | ch07.md | terminology | It is a collection rate, not a PERFORM repayment rate, | It is a collection rate, not a PERFORM Repayment Rate, |
| 42 | ch07.md | terminology | \| Performance \| Collection rate, month and trailing 3 months \| | \| Performance \| Operational collection rate, month and trailing 3 months \| |
| 43 | ch07.md | abbreviation defined | \| Losses \| Indicative ECL and coverage \| | \| Losses \| Indicative expected credit loss (ECL) and coverage \| |
| 44 | ch07.md | hyphenation consistency | holds the company-reported PERFORM KPIs | holds the company reported PERFORM KPIs |
| 45 | ch07.md | abbreviation defined | the collection ratio, PD and LGD proxies, | the collection ratio, probability of default (PD) and loss given default (LGD) proxies, |
| 46 | ch08.md | abbreviation defined | cure, so 30 DPD is not a reliable signal | cure, so 30 days past due (DPD) is not a reliable signal |
| 47 | ch08.md | abbreviation defined | shows an observed LGD proxy of about 99% | shows an observed loss given default (LGD) proxy of about 99% |
| 48 | ch08.md | abbreviation defined | \| RBF \| Other income when received | \| Results based financing (RBF) \| Other income when received |
| 49 | ch08.md | abbreviation defined | so a company with a lower APR will show | so a company with a lower annual percentage rate (APR) will show |
| 50 | ch08.md | abbreviation defined | on the source of PD and LGD estimates | on the source of probability of default (PD) and LGD estimates |
| 51 | ch08.md | abbreviation defined | Its covenants test collection rates, PAR and receivables at risk | Its covenants test collection rates, portfolio at risk (PAR) and receivables at risk |
| 52 | ch08.md | abbreviation consistency | before the IC memo is finalised | before the investment committee memo is finalised |
| 53 | ch09.md | abbreviation defined | RBF is any results based payment the programme attaches | Results based financing (RBF) is any results based payment the programme attaches |
| 54 | ch09.md | abbreviation defined | the hardware landed cost is the FOB cost translated | the hardware landed cost is the free on board (FOB) cost translated |
| 55 | ch09.md | abbreviation defined | The ratio of lifetime value to customer acquisition cost is the most quoted | The ratio of lifetime value to customer acquisition cost (LTV/CAC) is the most quoted |
| 56 | ch09.md | abbreviation defined | when the observed LGD proxy on the existing book | when the observed loss given default (LGD) proxy on the existing book |
| 57 | ch10.md | abbreviation defined | The following example is illustrative. A company sells a single product | The following example is illustrative and uses a fictional local currency (LCY). A company sells a single product |
| 58 | ch10.md | abbreviation defined | books the unrealised FX loss each month | books the unrealised foreign exchange (FX) loss each month |
| 59 | ch10.md | abbreviation defined | \| RBF payments \| USD per unit \| | \| Results based financing (RBF) payments \| USD per unit \| |
| 60 | ch10.md | long sentence split | the translation of LCY results into USD; a memo row shows | the translation of LCY results into USD. A memo row shows |
| 61 | ch11.md | abbreviation defined | Lenders lend against data: cohort curves, DPD history that reconciles | Lenders lend against data: cohort curves, days past due (DPD) history that reconciles |
| 62 | ch11.md | abbreviation defined | can sell receivables to an SPV. | can sell receivables to a special purpose vehicle (SPV). |
| 63 | ch11.md | abbreviation defined | \| Equity, grants, RBF, supplier credit \| | \| Equity, grants, results based financing (RBF), supplier credit \| |
| 64 | ch11.md | abbreviation defined | and an annual DSCR of at least 1.20x. | and an annual debt service coverage ratio (DSCR) of at least 1.20x. |
| 65 | ch11.md | long sentence split; terminology | along with receivables at risk and write offs; the 2026 standard does not include them and forbids presenting a collection rate as the repayment rate (Chapter 7). | along with receivables at risk and write offs. The 2026 standard does not include them and forbids presenting a collection rate as the Repayment Rate (Chapter 7). |
| 66 | ch11.md | terminology | may add the PERFORM 2026 repayment rate as a reporting line | may add the PERFORM 2026 Repayment Rate as a reporting line |
| 67 | ch11.md | abbreviation defined | Receivables at risk and PAR measures capture | Receivables at risk and portfolio at risk (PAR) measures capture |
| 68 | ch11.md | abbreviation defined | depends heavily on the ECL methodology | depends heavily on the expected credit loss (ECL) methodology |
| 69 | ch11.md | terminology | that none presents a collection rate as the PERFORM repayment rate, | that none presents a collection rate as the PERFORM Repayment Rate, |
| 70 | ch11.md | long sentence split; capitalisation | (0 = none, 1 = operating cash flow, 2 = cash basis excluding growth in PAYGo receivables): use the facility's own definition, and note that basis 0 models a facility without a DSCR test, as Section 16.9 recommends | (0 = none, 1 = operating cash flow, 2 = cash basis excluding growth in PAYGo receivables). Use the facility's own definition, and note that basis 0 models a facility without a DSCR test, as section 16.9 recommends |
| 71 | ch12.md | abbreviation defined | the share of the pool beyond a DPD threshold such as PAR30 | the share of the pool beyond a days past due (DPD) threshold such as PAR30 |
| 72 | ch12.md | long sentence split | with an SPV purchasing PAYGo receivables; it reports cumulative solar loans | with an SPV purchasing PAYGo receivables. It reports cumulative solar loans |
| 73 | ch12.md | long sentence split | covering Kenya, Tanzania and Uganda; the 718m is purchasing capacity, not debt raised. | covering Kenya, Tanzania and Uganda. The 718m is purchasing capacity, not debt raised. |
| 74 | ch15.md | capitalisation (cross reference) | 2. Check every red flag in Section 15.4 | 2. Check every red flag in section 15.4 |
| 75 | ch16.md | capitalisation (cross reference) | in Years 1 to 4 (Section 16.6), and 9 of | in Years 1 to 4 (section 16.6), and 9 of |
| 76 | ch16.md | capitalisation (cross reference) | replaced or reset with the lender, as Section 16.9 proposes, | replaced or reset with the lender, as section 16.9 proposes, |
| 77 | ch16.md | capitalisation (cross reference) | without a DSCR test, as Section 16.9 recommends, and is the setting | without a DSCR test, as section 16.9 recommends, and is the setting |
| 78 | ch13.md | abbreviation defined | translated into local currency along the FX path on *Timeline* | translated into local currency along the foreign exchange (FX) path on *Timeline* |
| 79 | ch13.md | terminology | subsidies are excluded from the repayment rate, so RBF cannot improve | subsidies are excluded from the Repayment Rate, so RBF cannot improve |
| 80 | ch13.md | abbreviation defined | It lowers effective CAC and shortens payback | It lowers effective customer acquisition cost (CAC) and shortens payback |
| 81 | ch13.md | terminology | The PAYGo PERFORM 2026 repayment rate is the natural reference | The PAYGo PERFORM 2026 Repayment Rate is the natural reference |
| 82 | ch13.md | abbreviation defined | long before PAR30 moves. It is also a figure a regulator or a journalist will compute, alongside the implied APR. | long before portfolio at risk (PAR30) moves. It is also a figure a regulator or a journalist will compute, alongside the implied annual percentage rate (APR). |
| 83 | ch14.md | abbreviation defined | receivables at risk and DPD move towards their limits | receivables at risk and days past due (DPD) move towards their limits |
| 84 | ch14.md | abbreviation defined | 2. FX: depreciation of the local currency against the USD, which affects hardware cost, USD debt service, USD RBF receipts | 2. Foreign exchange (FX): depreciation of the local currency against the USD, which affects hardware cost, USD debt service, USD results based financing (RBF) receipts |
| 85 | ch14.md | abbreviation defined | which drive revenue, CAC and the growth | which drive revenue, customer acquisition cost (CAC) and the growth |
| 86 | ch14.md | abbreviation defined | The annual DSCR test is reported separately | The annual debt service coverage ratio (DSCR) test is reported separately |
| 87 | ch14.md | abbreviation defined | and the MOIC falls from 6.7x to 0.3x | and the multiple on invested capital (MOIC) falls from 6.7x to 0.3x |
| 88 | ch14.md | hyphenation consistency | put off-grid solar investment | put off grid solar investment |
| 89 | ch14.md | abbreviation defined | across a local bank, a DFI and a securitisation | across a local bank, a development finance institution (DFI) and a securitisation |
| 90 | ch14.md | long sentence split | and does not recalculate when inputs change; its live row shows | and does not recalculate when inputs change. Its live row shows |
| 91 | ch15.md | abbreviation defined | rebuilds the collection rate, PAR30, receivables at risk | rebuilds the collection rate, portfolio at risk (PAR30), receivables at risk |
| 92 | ch15.md | abbreviation defined | with the 30 DPD rebuttable presumption; | with the 30 days past due (DPD) rebuttable presumption; |
| 93 | ch15.md | abbreviation defined | whether a true sale to an SPV would be respected | whether a true sale to a special purpose vehicle (SPV) would be respected |
| 94 | ch15.md | abbreviation defined | relative to income, the implied APR and how it is disclosed | relative to income, the implied annual percentage rate (APR) and how it is disclosed |
| 95 | ch15.md | abbreviation defined | 11. RBF and grant agreements | 11. Results based financing (RBF) and grant agreements |
| 96 | ch15.md | abbreviation defined | warranty terms and FX exposure by currency. | warranty terms and foreign exchange (FX) exposure by currency. |
| 97 | ch15.md | abbreviation defined | A DCF of unlevered free cash flow | A discounted cash flow (DCF) valuation of unlevered free cash flow |
| 98 | ch15.md | abbreviation defined | = USD 14.3m, a MOIC of | = USD 14.3m, a multiple on invested capital (MOIC) of |
| 99 | ch15.md | abbreviation defined | (the monthly covenants and the annual DSCR) | (the monthly covenants and the annual debt service coverage ratio, DSCR) |
| 100 | ch15.md | abbreviation defined | auditor review of the ECL approach and similar items | auditor review of the expected credit loss (ECL) approach and similar items |
| 101 | ch15.md | grammar (article) | credit workstream rebuilt collection rate, PAR30 | credit workstream rebuilt the collection rate, PAR30 |
| 102 | ch16.md | abbreviation defined | with eligibility up to 30 DPD. | with eligibility up to 30 days past due (DPD). |
| 103 | ch16.md | abbreviation defined | and indicative ECL coverage of 36.5% | and indicative expected credit loss (ECL) coverage of 36.5% |
| 104 | ch16.md | abbreviation defined | The observed LGD proxy is about 99% | The observed loss given default (LGD) proxy is about 99% |
| 105 | ch16.md | abbreviation defined | An ownership linked RBF design would pay nothing | An ownership linked results based financing (RBF) design would pay nothing |
| 106 | ch16.md | abbreviation defined | and its 106% implied APR will draw | and its 106% implied annual percentage rate (APR) will draw |
| 107 | ch16.md | terminology | \| Collection rate \| 82.3% \| | \| Operational collection rate \| 82.3% \| |
| 108 | ch16.md | abbreviation defined | The annual DSCR stays below 1.20x | The annual debt service coverage ratio (DSCR) stays below 1.20x |
| 109 | ch16.md | abbreviation defined | that is a MOIC of about 3.6x | that is a multiple on invested capital (MOIC) of about 3.6x |
| 110 | ch16.md | abbreviation defined | The DCF value of USD 6.1m | The discounted cash flow (DCF) value of USD 6.1m |
| 111 | ch16.md | long sentence split; terminology | Either way it should replace the DSCR test, which the projection fails in Years 1 to 4, with portfolio covenants and monthly reporting of the operational and lender metrics (collection rate, receivables at risk, write offs), each with its definition printed, and of the PAYGo PERFORM 2026 KPIs | Either way it should replace the DSCR test, which the projection fails in Years 1 to 4, with portfolio covenants. It should also require monthly reporting of the operational and lender metrics (operational collection rate, receivables at risk, write offs), each with its definition printed, and of the PAYGo PERFORM 2026 KPIs |
| 112 | ch16.md | abbreviation expanded | \| ESMAP MTR 2024, reported average | \| ESMAP Off-Grid Solar Market Trends Report 2024, reported average |
| 113 | ch16.md | terminology | not a PERFORM repayment rate, and it is not yet verified | not a PERFORM Repayment Rate, and it is not yet verified |
| 114 | ch16.md | abbreviation defined | equivalent to 100% FX pass through in the model | equivalent to 100% foreign exchange (FX) pass through in the model |
| 115 | ch99_annexes.md | terminology; hyphenation consistency | may not be used as a substitute for the repayment rate. In the companion model, company-reported results | may not be used as a substitute for the Repayment Rate. In the companion model, company reported results |
| 116 | ch99_annexes.md | terminology | defined in the 2021 PERFORM guide; not a substitute for the repayment rate \| | defined in the 2021 PERFORM guide; not a substitute for the Repayment Rate \| |
| 117 | ch99_annexes.md | terminology | \| Repayment rate (RR) \| PAYGo PERFORM 2026 KPI family | \| Repayment Rate (RR) \| PAYGo PERFORM 2026 KPI family |
| 118 | ch99_annexes.md | terminology | \| Collection rate \| Collections ÷ instalments due in a period, excluding deposits; an operational metric, not a PERFORM KPI \| | \| Collection rate (operational) \| Collections ÷ instalments due in a period, excluding deposits; an operational metric, not a PERFORM KPI \| |
| 119 | ch99_annexes.md | glossary entry added (abbreviation) | \| Advance rate \| Share of eligible receivables a lender will fund \| /  | \| Advance rate \| Share of eligible receivables a lender will fund \| / \| APR \| Annual percentage rate \| /  |
| 120 | ch99_annexes.md | glossary entry added (abbreviation) | \| Borrowing base \| Maximum facility drawing allowed by eligible receivables and advance rates \| /  | \| Borrowing base \| Maximum facility drawing allowed by eligible receivables and advance rates \| / \| CAC \| Customer acquisition cost \| /  |
| 121 | ch99_annexes.md | glossary entry added (abbreviation) | \| DPD \| Days past due \| /  | \| DPD \| Days past due \| / \| DSCR \| Debt service coverage ratio \| /  |
| 122 | ch99_annexes.md | glossary entry added (abbreviation) | \| First loss \| Tranche or equity that absorbs losses before any other investor \| /  | \| First loss \| Tranche or equity that absorbs losses before any other investor \| / \| FX \| Foreign exchange \| / \| LCY \| Local currency of the generic model (KVS in the SolaraPay case) \| /  |
| 123 | ch99_annexes.md | glossary entry added (abbreviation) | \| LGD \| Loss given default \| /  | \| LGD \| Loss given default \| / \| MTF \| Multi-Tier Framework (ESMAP) \| /  |
| 124 | ch00_front.md | serial comma consistency | unverified, conflicting sources, or not used. | unverified, conflicting sources or not used. |
| 125 | ch15.md | serial comma consistency | recoveries, active accounts, and ownership at twice | recoveries, active accounts and ownership at twice |
| 126 | ch14.md | table header consistency | \| Case \| Peak equity USD m \| Y5 EBITDA margin \| Investor IRR \| MOIC \| Monthly covenant breach months \| | \| Case \| Peak equity (USD m) \| Y5 EBITDA margin \| Investor IRR \| MOIC \| Monthly covenant breach months \| |
| 127 | ch14.md | table header consistency | \| Case \| Peak equity USD m \| Y5 EBITDA margin \| Y5 collection rate \| Investor IRR \| MOIC \| Breach months \| | \| Case \| Peak equity (USD m) \| Y5 EBITDA margin \| Y5 collection rate \| Investor IRR \| MOIC \| Breach months \| |
| 128 | ch16.md | table header consistency | \| Case \| Peak equity USD m \| Y5 EBITDA margin \| Y5 collection \| IRR \| MOIC \| Breach months \| | \| Case \| Peak equity (USD m) \| Y5 EBITDA margin \| Y5 collection rate \| Investor IRR \| MOIC \| Breach months \| |
| 129 | ch01.md | Markdown formatting | (double blank line) | (single blank line) |
| 130 | ch01.md | Markdown formatting | (double blank line) | (single blank line) |
| 131 | ch02.md | Markdown formatting | (double blank line) | (single blank line) |
| 132 | ch06.md | Markdown formatting | (double blank line) | (single blank line) |
| 133 | ch06.md | Markdown formatting | (double blank line) | (single blank line) |
| 134 | ch07.md | Markdown formatting | (double blank line) | (single blank line) |
| 135 | ch08.md | Markdown formatting | (double blank line) | (single blank line) |
| 136 | ch11.md | Markdown formatting | (double blank line) | (single blank line) |
| 137 | ch14.md | Markdown formatting | (double blank line) | (single blank line) |
| 138 | ch15.md | Markdown formatting | (double blank line) | (single blank line) |
| 139 | ch15.md | Markdown formatting | (double blank line) | (single blank line) |
