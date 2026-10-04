# Final QA report: Book 2 v0.2, MODEL 2 v0.8 (development build) and companion products

Date: 3 October 2026. This is the brief's final validation (section 36). Ratings:

* **PASS:** no material issue remains.
* **PASS WITH WARNING:** the work is sound, but a named item is open that does not make the current content wrong.
* **FAIL:** a material issue remains for the purpose stated.

The purpose assessed is a pre-publication edition (Book v0.2, Model v0.8). The last line also assesses readiness for commercial release (v1.0), which is a different test.

## Summary

| Category | Rating | Reason in one line |
|---|---|---|
| BOOK QA | PASS WITH WARNING | Text, numbers and labels consistent; primary documents, practitioner review and copyedit still open |
| MODEL QA | PASS WITH WARNING | 38 tests OK, faults detected, static tables reproduced; not yet opened in Microsoft Excel |
| SOURCE QA | PASS WITH WARNING | Every claim carries a grade and a status, and none is overstated; 43 of 71 claims await the primary document |
| ACCOUNTING QA | PASS WITH WARNING | No compliance claim anywhere; the treatment has not been reviewed by an accountant |
| FORMULA QA | PASS WITH WARNING | 0 error values in 100,857 formulas in two engines; Excel behaviour unverified |
| LINK QA | PASS WITH WARNING | Internal hyperlinks valid, no external links; web addresses in the source register not checked (network blocked) |
| VISUAL QA | PASS WITH WARNING | Book, front sheets and video checked; no page by page review of every product, nothing rendered in Excel or Word |
| COMMERCIAL QA (pre-publication) | PASS WITH WARNING | Book 2, MODEL 2, MANUAL 2, CASE 2 and the companion products are consistent and branded; prices, licence and access route not set |
| **Readiness for commercial release (v1.0)** | **FAIL** | Gates open: Excel test, primary documents, peer and model review, copyedit, print edition, companion model licence (10 checklist) |

## BOOK QA: PASS WITH WARNING

**Verified**
* 119 pages; paginated contents; text scan clean (no dashes, no tool or AI traces).
* No "investment grade". "Bankable" appears only once, as a quoted word.
* The series page lists the six-book collection, and Book 2 numbering is unchanged.
* Collection rate is distinguished from the PAYGo PERFORM 2026 Repayment Rate in every chapter. The last older wording (Ch 1, 11 to 13, 15, 16.9) was corrected in this cycle.
* Readiness passages match the workbook: 2 of 23 and 4 of 23, STOP on the failed DSCR test (gate 10), shown beside the analyst's Conditional Go, which is conditional on resetting the DSCR covenant.
* The 30 key claims are verified against the v0.8 workbooks (09). The 8 figures not found in any workbook are text arithmetic, checked in place.

**Open**
* Primary documents behind Annex G claims.
* Practitioner review.
* Copyedit.
* Sample review of the weak matches.

## MODEL QA: PASS WITH WARNING

**Verified (06):**
* Master check OK in the default model and in the case.
* 38 tests. Planted faults: 12 in step 2 and 4 in step 3, plus 6 decision-path tests in step 4. Every planted fault was detected and every decision path gave the expected result.
* Secondary calculation agrees to 2.49e-14.
* 15 sensitivity cases are reproduced inside the workbook: default to 1.1e-13, case to 1.2e-12.
* Readiness decision logic tested on all four paths (failed test, incomplete evidence, CONDITIONAL GO, GO), again by the independent red team (14).

**Open**
* Microsoft Excel test (readiness gate 17).
* Independent engine run on the case workbook in this cycle.
* External model review.

## SOURCE QA: PASS WITH WARNING

**Verified**
* Register of 71 claims: grades A 5, B 53, C 8, D 5. Statuses:

  | Status | Claims |
  |---|---|
  | VERIFIED | 11 |
  | VERIFIED (HISTORICAL) | 5 |
  | PENDING PRIMARY DOCUMENT | 43 |
  | CONFLICTING SOURCES | 4 |
  | NOT USED | 8 |

* Only VERIFIED claims feed Calibration, so every Calibration reference is suspended today.
* The M-KOPA FY2024 conflict is documented (08). The ESMAP figure is shown as a 2021 to 2023 average and is pending. The BBOXX date is pending.
* No page number is invented.

**Open**
* The 43 pending claims: documents to upload, or a decision to keep them as context only.

## ACCOUNTING QA: PASS WITH WARNING

**Verified**
* The statement "This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS." appears in:
  * the book (Ch 8);
  * the workbook (Contents, Cover, Glossary, Start, credit sheets and statements);
  * MANUAL 2, CASE 2 and the T01 memo template.
* ECL, PD and staging are labelled as proxies.

**Open**
* Review of the revenue recognition and ECL treatment by an accountant (readiness gates 15 and 19).

## FORMULA QA: PASS WITH WARNING

**Verified**
* No error values after full recalculation in LibreOffice.
* The independent engine agrees on every formula cell except one: a residue of LCY 0.0000011 in the equity top-up total. It is documented and neutralised in the runway flag.
* No circular references and no macros.

**Open**
* Excel recalculation, including the IRR solver and full calculation on load.

## LINK QA: PASS WITH WARNING

**Verified**
* 75 internal hyperlinks in the workbook all point to existing sheets.
* No external link parts.
* Contents and Start are generated from the tab order.

**Open**
* The web addresses in the source register and the benchmark database were not opened: the network policy of this environment refuses those hosts.

## VISUAL QA: PASS WITH WARNING

**Verified**
* Book pages and figures were reviewed at build.
* Start, Dashboard, Investment_Readiness and FX_Exposure were rendered in LibreOffice. Two alignment issues were found and fixed.
* The Module 17 video was checked by transcription and sampled frames.

**Open**
* Excel and Word rendering of the workbooks, calculators and templates.
* Full viewing of the video.
* Page by page review of MANUAL 2, CASE 2 and the guides.

## COMMERCIAL QA (pre-publication): PASS WITH WARNING

**Verified**
* The product line required by the brief exists and agrees on its numbers and framing:
  * BOOK 2, MODEL 2, MANUAL 2, CASE 2;
  * the quick reference;
  * six calculators;
  * eight templates;
  * the video course.
* No product carries a 1.0 label. Calculators and templates are version 0.9 (pre-release).
* The book is usable without the model.

**Open**
* Companion model licence, privacy policy, access route and prices (12 Amazon pack, a draft).

## Readiness for commercial release (v1.0): FAIL

The following gates are open and listed in 10:
* Excel and Word tests;
* primary documents;
* peer review, external model review and copyedit;
* replacement of the pre-publication wording;
* print edition files;
* rights check;
* companion model licence.

This rating is expected at this stage. It is not a defect of the current edition.
