# Book 7 v0.4: pre-publication QA summary

| Workstream | Scope | Result | Report |
|---|---|---|---|
| Proofread and source audit, front matter and Chapters 1 to 6 | 53 citation claims | 30 full text, 21 page, 2 search summary only (Hydro Finance Handbook), 7 corrected; 37 edits | docs/AUDIT_R1.md |
| Chapters 7 to 12 | 26 claims | 9 full text, 8 page, 0 summary only, 1 unsupported corrected; 28 edits | docs/AUDIT_R2.md |
| Chapters 13 to 18 and Annexes A to M | 26 claims | 12 full text, 11 page, 3 summary only (none carrying a claim alone), 3 unsupported corrected; 25 edits | docs/AUDIT_R3.md |
| Technical due-diligence reference, Annexes N to R | 214 claims, 64 calculations | 196 full text, 11 page, 5 summary only, 6 corrected; 19 edits | docs/AUDIT_R4.md |
| Case-study data | 102 facts, 15 benchmark cases | 88 confirmed on the page, 1 summary only, 11 corrected, 2 no public figure | docs/CASE_DATA_AUDIT.md |
| Independent model test | Excel compatibility, second engine, identities, behaviour, book cross-check | 11 findings (1 critical packaging, 1 high, 3 medium, 6 low); critical, high and medium fixed; second engine agrees on all 11,166 cells; 48 of 48 book numbers match | docs/MODEL7_TEST_REPORT.md |

## Fixed after the model test
- Excel quoting of digit-leading sheet names restored after every LibreOffice recalculation (tools/model/excel_quote_fix.py); a strict Excel-grammar parser now loads the shipped workbook.
- Developer IRR: three starting values; real rates now reported in the six stress runs that showed -100%.
- Selector validations (1 to 3 for case and generation case, 1 to 4 for lender case) with error messages on.
- Cover gate requires debt to exist; average DSCR no longer divides by zero.

## Open before version 1.0
1. Open the workbook in Microsoft Excel and confirm it opens without repair and recalculates to the same results.
2. Hydro Finance Handbook (LIT:S2): obtain the document or drop it from Table P.1.
3. Trademark check for "Hydro Readiness Framework".
4. ISBN and the KDP cover (spine width from the final page count and paper).
5. Low model points: zero-flow behaviour, design flow not linked to capacity and cost, gate label "base case", zero-tariff behaviour.
6. Practitioner and engineer review of the text and Annexes N to R.
