# 10 Publication QA checklist: Book 2, MODEL 2, MANUAL 2, CASE 2 and companion products

Status: 3 October 2026, at Book v0.2 and Model v0.8 (development build).

The release path is the one agreed with the author:

| Version | Purpose |
|---|---|
| v0.3 | Peer review |
| v0.4 | Technical review and Amazon master |
| v1.0 | Publication |

Nothing may carry a 1.0 label until every item marked **Gate** is Done.

Status values:
* **Done:** checked and evidenced.
* **Open:** not yet done.
* **n/a:** not applicable.

Owner:
* **A:** author.
* **R:** external reviewer.
* **P:** production (rebuild and checks in this repository).

## 1. Critical rules of the brief

| # | Rule | Status | Evidence |
|---|---|---|---|
| 1 | No invented data | Done (with sample review open) | The 30 key claims are verified in the workbooks; every figure of the book (3,391) is classified, and the 8 not found in any workbook are text arithmetic checked in place (section 4); weak matches await a sample review (X3) |
| 2 | No fabricated citations | Done | Annex G and 04 register list only documents held or reported; unread documents are PENDING |
| 3 | No fabricated page numbers | Done | Pages given only for documents held (PERFORM guides, M-KOPA UK filing); "PAGE TO VERIFY" in the benchmark database |
| 4 | No silent replacement of source definitions | Done | Changelog steps 1 to 4 record every definition change |
| 5 | Collection rate never presented as the PERFORM Repayment Rate | Done | Book Ch 1, 7, 11 to 13, 15, 16; model labels; manual, case, templates, video (changelog P.1 to P.5) |
| 6 | No model assumption treated as evidence | Done | Provenance label on every input; Calibration uses VERIFIED references only |
| 7 | SolaraPay never presented as a benchmark | Done | Case labelled fictional and synthetic throughout |
| 8 | Book numbering unchanged | Done | Book 2 in the six-book collection |
| 9, 10 | No functionality deleted; no redesign before dependencies understood | Done | 05 architecture (v0.7 audit and v0.8 addendum); no sheet deleted |
| 11 | No claim of validation without automated checks | Done | 06 validation report; Excel test stated as pending everywhere |
| 12 | No IFRS compliance claim | Done | Accounting statement in book Ch 8, model, manual, case, templates |
| 13, 14 | No optimisation of returns; honest results | Done | Readiness 2 of 23 and 4 of 23 after gate 10 took in the DSCR (an unattractive result kept); decision STOP shown beside the analyst's Conditional Go |
| 15 | Conflicts shown and investigated | Done | 08 M-KOPA reconciliation; register status CONFLICTING SOURCES |

## 2. Book 2 (01_BOOK_PAYGO_SOLAR_FINANCE_v0.2.pdf, 117 pages)

| # | Item | Gate | Status | Owner | Evidence or next step |
|---|---|---|---|---|---|
| B1 | Text scan: no em or en dashes, spaced hyphens, tool or AI traces | Gate | Done | P | Publishing tool reports "text scan clean" |
| B2 | No "investment grade", no "bankable" series | Gate | Done | P | Search of the assembled text: 0 hits ("bankable" once as a quoted word in the introduction) |
| B3 | Paginated contents, running headers, bookmarks | | Done | P | Two-pass build |
| B4 | Figures (15) read from the recalculated workbooks | | Done | P | Figure builder asserts key values (Figure 3: month 14, LCY 11,832) |
| B5 | Primary documents read and cited by page: E1 ESMAP MTR 2024, E3 MTF, E7 BBOXX Gazette notice, E4-G M-Kopa Holdings group accounts, E5, E6, E8 to E10 | Gate | Open | A | Upload the documents or confirm "context only" wording; 40 of 64 register claims are PENDING PRIMARY DOCUMENT |
| B6 | Practitioner review (PAYGo, lender, investor, modeller) | Gate | Open | R | v0.3 |
| B7 | Professional copyedit (British English, house rules) | Gate | Open | R | v0.4 |
| B8 | "Status of this edition" and "pre-publication" wording replaced for the commercial edition | Gate | Open | P | At v1.0 only |
| B9 | Print edition: trim size, greyscale figures, KDP interior and cover | Gate | Open | A, P | 12 Amazon pack, sections 3 and 13 |
| B10 | Rights to quoted text (PERFORM guides: short quotations only) | Gate | Open | A | Legal check before v1.0 |

## 3. MODEL 2 (02_PAYGO_SOLAR_FINANCE_MODEL_v0.8-dev.xlsx)

| # | Item | Gate | Status | Owner | Evidence or next step |
|---|---|---|---|---|---|
| M1 | LibreOffice recalculation without error values; master check OK | Gate | Done | P | 06, section 3 |
| M2 | Independent engine agrees with LibreOffice; secondary calculation agrees | Gate | Done | P | 06, section 3 (one floating residue documented) |
| M3 | Fault injection on the tests | | Done | P | 06, section 5 |
| M4 | Static Sensitivity reproduced in the workbook (default and case) | | Done | P | 06, section 3 |
| M5 | No "investment grade", no "bankability", no dashes in workbook text | | Done | P | Workbook text scan |
| M6 | Internal hyperlinks valid; no external links | | Done | P | 75 hyperlinks checked; no external link parts |
| M7 | Front sheets render legibly (Start, Dashboard, Investment_Readiness, FX_Exposure) | | Done (LibreOffice) | P | Rendered and two alignment issues fixed; Excel rendering open (M8) |
| M8 | Test in Microsoft Excel: opens, recalculates, master check OK, IRR values, charts, validation lists, no repair prompt | Gate | Open | A | Needs Excel; record a test log (readiness gate 17) |
| M9 | Independent engine on the case workbook in the v0.8 cycle | | Open | P | 06, section 6 |
| M10 | External model review | Gate | Open | R | v0.4 |
| M11 | Release file name 02_PAYGO_SOLAR_FINANCE_MODEL_v0.8.xlsx | Gate | Open | P | After M8 |

## 4. Book and model cross reference (09_BOOK_MODEL_CROSS_REFERENCE.xlsx)

| # | Item | Status | Evidence |
|---|---|---|---|
| X1 | Rebuilt on the v0.8 value stores and the final book text | Done | 3,391 figures classified; key claims updated for v0.8 (47 sheets, 100,857 formulas, 38 tests) |
| X2 | Figures marked NOT FOUND (8) | Done | All text arithmetic, checked in place: Ch 1.4 unit example (18,728; 16,560; 11,832), Ch 1.7 "about 100,900" formulas (100,857), Ch 7.7 borrowing base 574 (700 + 120 = 820; × 70%), Ch 8.4 discount factor 0.9129 (1 ÷ 1.2^0.5), Ch 10.3 margins 14,000 and 14,100 |
| X3 | Weak matches (round numbers) | Open | Sample review by the reviewer at v0.3 |

## 5. Companion products

| # | Product | Gate | Status | Evidence or next step |
|---|---|---|---|---|
| C1 | MANUAL 2 (03 copy; 23 pages) aligned with v0.8 | Gate | Done | Changelog P.1; text scan clean |
| C2 | CASE 2 SolaraPay (15 pages) aligned with Ch 16 | Gate | Done | Changelog P.2 |
| C3 | Quick reference (15), decision tools guide (6), templates guide (7) | | Done | Changelog P.3 |
| C4 | Calculators D1 to D6 and templates T01 to T08 rebuilt, recalculated in LibreOffice | | Done | Changelog P.3 |
| C5 | Calculators and templates tested in Excel and Word | Gate | Open | Needs Excel and Word |
| C6 | Video course: scripts corrected, changed narration re-voiced, Module 17 re-rendered (17:33) | | Done | Changelog P.4 |
| C7 | Full viewing of the Module 17 video by a person | | Open | Agent check was by transcription and sampled frames |
| C8 | Companion model access (licence, privacy policy, landing page, domain) | Gate | Open | 12 Amazon pack, section 7 |

## 6. Reports required by the brief (section 34)

| File | Status |
|---|---|
| 01 Book v0.2 PDF | Done |
| 02 Model v0.8 | Done as v0.8-dev; release name after the Excel test |
| 03 Manual PDF | Done as MANUAL 2 for model v0.8-dev |
| 04 Source register v1.0 (register format version, not a product release) | Done |
| 05 Model architecture | Done (v0.7 audit and v0.8 addendum) |
| 06 Model validation report | Done |
| 07 Source verification report | Done |
| 08 M-KOPA source reconciliation | Done |
| 09 Book and model cross reference | Done (rebuilt) |
| 10 This checklist | Done |
| 11 Changelog | Done |
| FINAL_QA_REPORT | Done |
