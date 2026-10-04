# Audit R3: chapters 13 to 18, Annexes A to M, technical reference introduction

Files: book7/src/ch13.md, ch14.md, ch15.md, ch16.md, ch17.md, ch18.md, ch99_annexes.md, ch99b_technical_intro.md. Numbers checked against build/book7_resolved.md and model/build_model.py; Annex K checked against docs/RED_TEAM_REVIEW_raw.md and book/src/05_redteam.md.

Note: another reviewer's commit (6a2fa74, "review R2 edits") swept up most of my working-tree edits and research/audit_sources_R3.md. The edits are as listed below; only the last ch13 edit (MIGA) is still uncommitted.

## Summary counts

- Citation instances in the assigned files after edits: 30. Case-study citations not re-verified (per brief): 4 (A2:S6, A2:S53, A1:S40, A2:S22). Audited: 26.
- CONFIRMED-FULLTEXT: 12
- CONFIRMED-PAGE: 11 (four upgraded from search summary this session: PF-04, CL-04, DE:S30, DE:S39)
- SUMMARY-ONLY: 3 (PF-01, PF-06, FR-01; none carries a claim on its own)
- NOT SUPPORTED before edits: 3 claims, all corrected (Bugoye sponsor sale cited to DE:S30; Kariba North output; MIGA expropriation cover). Sources removed: DE:S11 (Wikipedia snippet), CL-05 (Bloomberg page did not load).
- New audit sources: 3 ([R3:S1] to [R3:S3]).
- Edits: 25.

## Audit table

| Claim (short) | File:line | Source ID | Exact evidence | Status | Action |
|---|---|---|---|---|---|
| Uganda small plants financed by FMO, EAIF, Proparco | ch13:11 | DE:S39 | FMO: "underwritten USD 39 million senior debt ... Nyamagasani"; Proparco "to share 40% of the risk" | CONFIRMED-PAGE | None |
| same (EAIF, FMO) | ch13:11 | DE:S53 | "EAIF is lending $27 million and ... FMO has contributed the same amount" | CONFIRMED-PAGE | None |
| Nachtigal 21-year local-currency tranche, IBRD-guaranteed | ch13:17 | PF-11 | DB extract (F): "local-currency 21 yrs ... IBRD loan guarantee US$200m"; WB blog: tranche "covered by an up to 21-year IBRD ... guarantee" | CONFIRMED-FULLTEXT | None |
| GET FiT premium USD 0.014/kWh, 20 yrs paid in 5, half at COD | ch13:32 | DE:S9 | ERA brief: Hydro premium 0.014, period 20; "50% of the FiT premium will be disbursed upon Commercial Operation Date ... limited to a 5-year period" | CONFIRMED-FULLTEXT | None |
| MIGA PRI covers and non-honouring cover | ch13:38 | PF-03 | MIGA: "a government's failure to make a payment when due under an unconditional and irrevocable financial payment obligation"; lists Breach of Contract, Currency Inconvertibility and Transfer Restriction, War and Civil Disturbances. Expropriation not on the pages read | CONFIRMED-PAGE after edit | Removed "expropriation"; reworded to page text |
| WB/AfDB partial risk and loan guarantees | ch13:40 | PF-01 | URL now redirects to miga.org | SUMMARY-ONLY | Supported by R3:S3 |
| same | ch13:40 | PF-02 | "credit guarantees (also called loan guarantees) cover the public sector borrower's debt"; "payment guarantees to cover defaults on non-loan related government payment obligations" | CONFIRMED-PAGE | None |
| same (AfDB PRG) | ch13:40 | PF-06 | Press page loops on redirect | SUMMARY-ONLY | Kept as precedent only |
| Guarantees backed by government indemnity | ch13:40 | R3:S3 | "A partial risk guarantee protects private lenders against debt service defaults ... caused by a government's failure to meet specific obligations"; "All World Bank guarantees require a sovereign indemnity of the bank" | CONFIRMED-PAGE | Added |
| ATIDI RLSF: up to 12 months revenue, up to ~100 MW | ch13:42 | PF-04 | "cover up to twelve months' worth of revenue"; "installed capacity of up to 100 MW; exceptional cases can be considered" | CONFIRMED-PAGE | None (DB still marks S) |
| Bugoye refinanced 2017 by EAIF and FMO | ch13:50; ch14:115 | DE:S30 | "FMO and ... EAIF ... will each provide USD 14.6 million to (i) refinance the existing senior debt"; effective 13 July 2017; "indirectly wholly owned by Africa Energy Renewable Fund" | CONFIRMED-PAGE | Kept |
| "after its original sponsors had sold" / sponsors exited 2015 | ch13:50; ch14:115 | DE:S30, DE:S11 | S30 says nothing on the sale; S11 is a Wikipedia snippet | NOT SUPPORTED as cited | Re-cited to R3:S1; wording limited to Norfund's exit |
| Norfund exited Bugoye in 2015 | ch13:50; ch14:115 | R3:S1 | "In 2015 Norfund exited from five equity investments: ... the hydropower plant Bugoye in Uganda" | CONFIRMED-FULLTEXT | Added |
| No public data on development premiums | ch14:91 | DE:BENCH | "Development premium / developer fee at FC ... PUBLIC DATA NOT FOUND" | CONFIRMED-FULLTEXT | None |
| SSA T&D losses 15% (23% excl. SA); collection 58 to ~100% | ch15:11 | UT-02 | DB extract (F): "Weighted avg T&D losses SSA 15% (23% excl. South Africa) ... lowest 58-60%"; "~100%" | CONFIRMED-FULLTEXT | None |
| QFD about 1.5% of GDP | ch15:11 | UT-02 | "QFD avg 1.5% GDP" | CONFIRMED-FULLTEXT | None |
| DSF as standard tool | ch15:41 | FR-09 | DB (F): LIC DSF guidance note | CONFIRMED-FULLTEXT | None |
| PFRAM as standard tool | ch15:41 | FR-01 | DB (S) | SUMMARY-ONLY | Descriptive, non-central; kept |
| Kariba allocation cut ~47% for 2024 | ch16:57 | CL-04 | TEI: ZRA "reduced the amount of water allocated for power generation at the Kariba Dam by 47 per cent"; 30 to 16 BCM | CONFIRMED-PAGE | "In 2024" changed to "For 2024" |
| Kariba North output 1,080 MW to ~166 MW | ch16:57 | CL-05 | Page fetch returns the BNN homepage; nothing on Kariba | NOT SUPPORTED as framed | Re-cited to R3:S2: 98 MW in June 2024, down from 166 MW a month earlier |
| Kariba North 98 MW / 166 MW | ch16:57 | R3:S2 | "dropped by 90.9% from 1,080MW to 98MW"; "Barely a month ago, it was producing 166MW" | CONFIRMED-PAGE | Added |
| Kikagati close 2019, 16-year loan | ch17:177 | DE:S53 | "Financial close ... 15 August 2019"; "Both loans have 16-year terms" | CONFIRMED-PAGE | None |
| Technical annexes draw on IFC guide, ESHA, AG/IHA, WB/ESMAP full texts | ch99b:5 | DE:S1, LIT:S6, LIT:S7, HY-06 | Local full texts ifc.txt, esha.txt, ag.txt, esmap.txt present and cited throughout tech/annex_*.md | CONFIRMED-FULLTEXT (4) | None |
| Nachtigal lenders; Lumora-side guarantees; Bui arrears; Ruzizi III | ch13:11; ch15:37; ch16:57; ch17:177 | A2:S6, A2:S53, A1:S40, A2:S22 | Not re-verified (case-study audit) | n/a | Wording only |

Model and internal checks (no external source):
- Annex A: every sheet named exists in SHEETS. KPI locations checked in model_map.json (p50/p90/cf in 03_HYDROLOGY; uses, gearing, IRRs, LLCR, LCOE, min DSCR, gap in 17_PROJECT_FINANCE; CFADS and DSCR rows in 20_CASH_FLOW; dev measures in 01A_DEVELOPMENT; ut_ratio10 in 12_UTILITY; fiscal NPVs in 25_FISCAL_IMPACT; cl_peak in 24_CONTINGENT_LIABILITIES; fc_decision in 30A_CLOSE_READINESS).
- Annex K: 30 findings (3/10/10/7) and IDs C-01 to L-07 match the raw review; statuses agree with book/src/05_redteam.md. 33_CHECKS has 14 checks, as stated.
- Ch17 decision rule matches the fc_decision formula. Gate counts in Table 17.2 match the text (four critical open under Q1/Q2, seven in all).
- Ch16: 16 risks and 8 parties in 29_RISK_ALLOCATION; 12-month guarantee cap (ppag_months); IPP tenor 16 years (str_nm); hybrid grant 35% (str_grant); IPP gearing cap 70% (str_maxdebt).
- Ch18: 5.2 + 3.8 = 9.0 (Ch6 budget); co-developer share 2.06 / 3.34 = 62%.
- Lumora (ch15.6): checked against book/build/manuscript_resolved.md: peak CL 2.7% of GDP; screen moderate, high under overruns, offtaker stress and currency step; offtaker central fiscal NPV 49 to −1,177; 400 MW (inst_mw in the red-team notes).

## Edits made (old to new, short)

ch13
1. 13.2: "local-currency debt adds currency risk ...; the mismatch sits with the utility instead, and Chapter 15 measures it" to "would add currency risk ... Kasiri's mismatch sits with the utility, which earns in local currency and pays the PPA in dollars; the currency stress in Chapter 16 measures it" (Ch15 does not measure FX).
2. 13.3: "compares five structures" plus a four-row table: added "The table shows the four with private equity; the fifth, fully public, has none."
3. 13.4 MIGA: dropped "expropriation" and aligned the wording with the MIGA page.
4. 13.4 guarantees: added [R3:S3] for the indemnity.
5. 13.5 Bugoye: "refinanced in 2017 by EAIF and FMO, after its original sponsors had sold [DE:S30]" to "by then owned by AREF, refinanced its senior debt in 2017 with EAIF and FMO [DE:S30]; Norfund ... had exited in 2015 [R3:S1]".

ch14
6. Table row "All four development levers together" to "Rate, premium, odds and grant together (tariff unchanged)". The dev_all run in tools/run_snapshots.py sets rate, premium, odds and grant but not the tariff, so the old label and text implied the tariff was included.
7. "Only all the levers together" to "Only the four development levers together, with the tariff unchanged".
8. 14.5 Bugoye: removed the "search summaries we could not confirm" hedge and DE:S11; now cites R3:S1 and DE:S30.

ch15
9. "about 6.0x times the PPA bill" to "the ratio ... is about 6.0x".
10. Lumora: "at commercial operation ... of the order of 3 percent of GDP", "high under cost overrun or offtaker stress" to "peak ... about 2.7 percent of GDP", "high under cost overruns, the offtaker stress or the currency step".

ch16
11. 16.1: added "The table shows the main ones for Kasiri" (16 risks mapped; 7 shown).
12. 16.3: "needs either a larger reserve, a cash sweep ..., or completion of a drought test before close" to "needs a larger reserve, a cash sweep in wet years or a smaller loan, and should see the drought test before close" (matches 18.4).
13. 16.3: moved the "African experience gives both stresses a real shape" paragraph after the buyer paragraph, because it referred to the buyer stress before that stress was introduced.
14. 16.3 Kariba: CL-05 claim replaced: "output of the 1,080 MW Kariba North Bank station was reported at 98 MW in June 2024, down from 166 MW a month earlier [R3:S2]".

ch18
15. 18.4: "debt sized on the ten-year P90 and the 70 percent gearing limit binding by a small margin" to "debt set by the 70 percent gearing limit, which binds just before cover on the ten-year P90". Ch12 gives 145 (gearing) against 148 (cover), and the table shows 68% on total uses, so "binding by a small margin" read as a contradiction.

ch99_annexes
16. Intro: "Annexes A to I are checklists and templates" to "Annex A defines the key results; Annexes B to I are checklists and templates".
17. Annex A CFADS: the definition now follows the model (taxes and project-funded transmission in operation; no separate maintenance capex term).
18. Annex A LLCR: added "life of the longest tranche, at the weighted interest rate" (fix M-01; matches the kpi_llcr label).
19. Annex K: "a cycle detector confirms" to "a dependency check on the workbook found no circular references" (see open issue 1).
20. Annex K H-10: "Fixed" to "Partly fixed: ... no currency pass-through (see M-06)".
21. Annex K "What the model does not do": added the bullet on the permanent currency step. The table said M-06 was "stated as a limitation", but the limitation was not in the list.
22. Glossary Gearing: "Debt as a share of total funding" to "Senior debt as a share of total uses" (matches Annex A).
23. Glossary P50/P90: now defines P50 as the central estimate and separates the one-year and ten-year P90 (was "exceeded with 50 ... percent probability", which conflicted with Annex A "mean").

ch99b_technical_intro
24. "ends with decision tests linked to the gates of the Hydro Readiness Framework" to "ends with decision tests. The table shows which questions ... and which chapters each annex informs." The annexes' decision tests do not reference gates.
25. Annex R row: "Q2, Q7 | 7, 15" to "Q2, Q5, Q7 | 2, 7, 15, 16". R.14 tests DSCR under a 10% flow cut (Q5), and its climate content draws on Ch2 and Ch16.

Style scan of all eight files: no em or en dashes, no spaced hyphens, no listed banned words, British spelling.

## Open issues for the author

1. Circularity. The only cycle check is a scratch script (scratchpad/cyc.py), which is not in the repository. Commit it or keep Annex K's softer wording. The model's own 00_README line still says "Circularity: None. IDC, fees and DSRA are equity-funded", which contradicts the H-06 fix (IDC and fees debt-funded). Fix this in model/build_model.py, line about 1966.
2. Two "risk-weighted" values. The developer's risk-weighted NPV at reconnaissance is −0.95 (Ch14, Table 18.3). The Ch6 table gives the position value at reconnaissance as −1.20. Both are correct but are different measures, and readers will compare them. Name them distinctly, or add one sentence in Ch14.1 explaining the difference.
3. Annex L preamble. tools/book7/prepare7.py generates it, and it does not explain the R1 to R4 audit-source prefixes. Add one clause.
4. Source database. PF-04 and CL-04 can be upgraded from S to P (pages read today). CL-05 should be marked as unverifiable (the URL resolves to the BNN homepage). PF-01's URL now redirects to miga.org.
5. MIGA expropriation cover is real, but it is not on the pages cited. If the author wants it back, cite a MIGA product page that lists it.
6. The Bugoye exit by TrønderEnergi (the majority sponsor) is still unconfirmed. The text now names only Norfund.
7. Ch16.3 says "Three results stand out", and the African-evidence paragraph now sits between the second and third results. This is acceptable, but the author may prefer it after the third.
