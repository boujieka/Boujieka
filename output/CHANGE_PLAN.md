# Change plan: Book v0.1 to v0.2, Model v0.7 to v0.8

Prepared 3 October 2026 from `01_PROJECT_AUDIT.md`. Nothing in this plan has been executed. Each change will be recorded in `11_CHANGELOG_v0.2_v0.8.md` with OLD, NEW, REASON, SOURCE, IMPACT ON MODEL and IMPACT ON BOOK.

Principles: the v0.7 workbook is the source of truth; the model is changed through its generator (`tools/build_shs_model.py`) so that every build is reproducible; no sheet is deleted or renamed before its dependencies are mapped (done in `05_MODEL_ARCHITECTURE.md`); no assumption is changed to improve results; every changed number is reconciled between book and model.

## A. Model v0.8

| ID | Change | Reason | Effect on outputs | Book impact |
|---|---|---|---|---|
| M1 | IRR with a second guess and an explicit "no IRR" message where flows have no sign change | Downside IRR returns n/a in LibreOffice | None at Base; Downside shows (22.9%) in the workbook | None (book already quotes 22.9%) |
| M2 | Add explicit checks: monthly cash reconciliation; receivables roll forward; debt roll forward; equity roll forward; cohort totals to Ops; vintage engine to Vintage_Input; RBF claims to receipts; FCFF to FS; no impossible negative balances | Brief section 20; audit section 6 | None if identities hold; any failure will be reported, not hidden | Update the check count (24 today) everywhere it is quoted |
| M3 | PERFORM 2026 block: RR PvP, RR PvFin, RR PvP @90 Days, RR PvP @2x, Ownership Rate @2x, computed in Actual mode from Vintage_Input where the data allow, with a visible "not available from proxy data" state otherwise; collection rate kept and relabelled "operational collection rate (not a PERFORM KPI)" | E2 PDF page 10, rule 3A | New outputs; existing figures unchanged | Ch 7 restructured (B4) |
| M4 | Provenance labels on every input (MODEL ASSUMPTION, COMPANY DATA, EXTERNAL EVIDENCE, CALIBRATED ASSUMPTION, UNVERIFIED) | Brief section 13 | None | Conventions section explains the labels |
| M5 | Source_Register rebuilt on the A to D scale with the full field list; SR01 to SR04 to CONFLICTING SOURCES; M-KOPA UK filing added as A, VERIFIED, NOT USED; SR14, SR15 regraded; SR19 UNVERIFIED; PERFORM split into 2026 (current) and 2021 (historical) | 07 and 08 reports | Calibration loses its M-KOPA reference | Ch 15 benchmark passage revised; "6.1 times" diagnostic removed |
| M6 | Calibration and Market_Benchmark: suspend references with status other than VERIFIED; show the status beside each reference | Rule: assumptions are not evidence | Diagnostic flags change; projections unchanged | Ch 15, 16 text where diagnostics are quoted |
| M7 | Start sheet (what to input, what the model calculates, what it means, what an investor should look at) and a rebuilt Dashboard with the metric set in brief section 23, each metric labelled and rounded to avoid false precision | Brief sections 22, 23 | None | Manual updated |
| M8 | Investment_Readiness: evidence column per gate (what evidence, where held, who signed), a separate GO / CONDITIONAL GO / STOP summary driven only by the evidence, and the note reworded so that the model never implies an "investment grade" outcome | Brief section 17 | Gate counts unchanged (3 of 23 default, 5 of 23 case) | Ch 15, 16 |
| M9 | Accounting statement on Cover, Glossary and the credit sheets: "This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS." | Brief section 10 | None | Ch 8 |
| M10 | FX exposure table: currency of revenue, collections, receivables, hardware, opex, debt, equity; hedge assumption (none by default); translation and transaction effects shown separately | Brief section 26 | None (presentation of existing calculations) | Ch 10 |
| M11 | RBF engine: separate rows for eligibility, claim, verification, disbursement and the working capital gap; check that RBF never enters customer collections | Brief section 28; E2d | None expected; to be confirmed | Ch 13 |
| M12 | Scenario architecture: label Actual (history), Management Case, Calibrated Case, Base, Downside, Severe; keep history untouched by forecast levers | Brief section 25 | None at default | Ch 6, 16 |
| M13 | Sensitivity: keep the static table with a stamped date and the statement that it was recomputed in the workbook, or replace it with an in-workbook case table if this can be done without macros or circularity | Audit finding 2 | None | Ch 14 |
| M14 | Case workbook: add a history summary (collection rate by history year, with the window stated) so that 77.4% and 69.3% become workbook cells; harmonise the two windows or disclose them | Audit finding 4 | Possible small change to the first-year figure if the window is harmonised | Ch 1, 7, 11, 16 and case study if the figure changes |
| M15 | Contents in tab order with all sheets; version label v0.8; file name `02_PAYGO_SOLAR_FINANCE_MODEL_v0.8.xlsx` | Audit finding 7; brief section 34 | None | Ch 1.7 |
| M16 | Benchmarks: add period, definition, page, status and a comparability warning when definitions or periods differ | Brief section 24 | None | Ch 7.4, 15 |

Not planned without your decision: adding the sheets named in the master context that do not exist in v0.7 (PERFORM_2026, Sources_Standards, Investment_Grade, Disclaimer). M3, M5, M8 and M9 deliver their content; creating them as separate sheets is a presentation choice.

## B. Book v0.2

| ID | Change | Reason |
|---|---|---|
| B1 | Retitle as BOOK 2, PAYGo SOLAR FINANCE: Business Models, Credit Risk and Financial Structuring for Solar Home Systems; series page with Books 1 to 3; publisher family Africa Energy Finance / Business & Financial Models | Fixed brand architecture |
| B2 | New opening framework: the analytical chain (customer to investment committee) and the six distinctions (commercial viability, accounting profitability, cash generation, portfolio quality, funding capacity, investment readiness), referenced from each chapter | Brief sections 4, 5 |
| B3 | Chapter 1: "utility-like service provider" throughout, including the chapter title; implications for cash flow, credit, retention, collections, working capital and funding | Brief section 12 |
| B4 | Chapter 7 restructured on PERFORM 2026: the five KPIs and their rules; collection rate, PAR, receivables at risk and write offs presented as operational and lender metrics, with the 2021 guide cited as historical | E2, E2a |
| B5 | Chapter 8 and Annex: accounting statement; model treatment separated from accounting policy; "conservative" framed as an analytical observation | Brief section 10 |
| B6 | Affordability: keep Chapter 2.3's policy wording; label later uses of 10% as the model's policy threshold; add the list of drivers | Brief section 11 |
| B7 | Sources: new section on source methodology (primary source, institutional evidence, company filing, model assumption, calibrated assumption, illustrative case); Annex G rebuilt from the new register; M-KOPA, ESMAP and BBOXX passages rewritten to their verified status | Brief sections 7 to 15, 30 |
| B8 | Ten to fifteen explanatory figures (list in the brief, section 16), each tied to a model output or a stated illustration | Brief section 16 |
| B9 | Chapter 1.7: "secondary calculation check" instead of "independent shadow calculation"; add the LibreOffice recalculation and the Excel test status | Audit finding 5 |
| B10 | A short valuation section (or chapter) so that the chain's valuation step has a home; FX and funding sections strengthened per brief sections 26 and 27 | Brief sections 26, 27, 29 |
| B11 | Every figure reconciled to the v0.8 model through the cross-reference workbook; wording fixes (for example "its real plan" for the fictional case); the illustrative plan renamed so that it is not confused with the model's Tier 2 | Audit findings 10, 11 |

## C. Manual, case study and satellites

* Manual renamed MANUAL 2, PAYGo Solar Finance Model User & Methodology Manual, v0.1 (pending your confirmation of the numbering); check count corrected; new sheets documented.
* Case study aligned with v0.8 outputs; history summary cells cited.
* Templates, decision tools, quick reference and video: relabelled below 1.0; the Module 17 statement on 25 checks corrected; rebrand after the core is stable.

## D. Sequence and checkpoints

1. Source register and reconciliations (M5, M6, B7): uses only documents in hand; flags the rest.
2. Model controls and fixes (M1, M2, M14), then rerun LibreOffice and engine comparisons.
3. PERFORM 2026 block (M3) and Chapter 7 (B4).
4. Front end and readiness (M4, M7, M8, M9, M10, M11, M12, M13, M15, M16).
5. Book revision (B1 to B11) with figures, then the cross-reference rebuilt on final page numbers.
6. Reports 04, 06, 10, 11 and FINAL_QA_REPORT.

A short report follows each step: inspected, changed, unresolved, evidence.
