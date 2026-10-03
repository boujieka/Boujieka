# Source verification report (audit stage)

Status: prepared 3 October 2026; updated the same day after step 1 of the change plan (client extraction of the ESMAP MTR 2024 received; register rebuilt as `04_SOURCE_REGISTER_v1.0.xlsx`, which now prevails over the tables below for individual statuses). Page numbers are PDF page numbers of the files provided unless stated otherwise. Where a page could not be verified, the entry says PAGE TO VERIFY.

Grades: A primary official, regulatory or audited source; B authoritative institutional source; C reputable secondary source; D unverified or informal.

Status values: VERIFIED; VERIFIED — HISTORICAL; PENDING PRIMARY DOCUMENT; UNVERIFIED; CONFLICTING SOURCES; NOT USED.

## 1. Documents received and their standing

| Ref | Document | Publisher | Date | Grade | Standing |
|---|---|---|---|---|---|
| E2 | PAYGo PERFORM KPIs: Industry Standards for End-User Asset Financing, Technical Guide (42 pages) | GOGLA (PAYGo PERFORM initiative; update led by GOGLA and PAYGoWise) | June 2026 | B | Current industry standard for the KPIs it defines |
| E2-G | PAYGo PERFORM KPIs, At a Glance (12 pages) | GOGLA | June 2026 | B | Summary of E2; E2 prevails on detail |
| E2a | PAYGo PERFORM Technical Guide (85 pages) | CGAP, GOGLA, IFC Lighting Global | July 2021 | B | Historical reference. Two identical copies were uploaded (same checksum). |
| E2b | PAYGo Accounting Brief (67 pages), authored by MFR | PAYGo PERFORM initiative | October 2021 | B | Practitioner guidance on IFRS 15 and IFRS 9 for PAYGo; not an accounting standard and not an auditor's view |
| E2c | Guidance for Company Analysis, v3 Beta (63 pages) | GOGLA (PAYGo PERFORM) | July 2025 | B | Beta status must be stated when cited |
| E2d | Guidance for PAYGo RBF Funds: Strengthening how we measure and incentivise sustained energy access (27 pages) | PAYGo PERFORM initiative | April 2026 | B | Reference for RBF design and outcome metrics |
| E4 | M-KOPA UK LIMITED, Annual Report and Accounts, year ended 31 December 2024 (34 pages, scanned) | Companies House filing | Filed 25 September 2025 | A | Primary, but for a UK subsidiary only (see 08_MKOPA_SOURCE_RECONCILIATION.md) |

Not received and not reachable from this environment (network policy refuses the hosts):

| Ref | Document | Needed for |
|---|---|---|
| E1 | ESMAP / World Bank, Off-Grid Solar Market Trends Report 2024 | 62% collection rate (2023) and the "about half written off or more than 30 days late" statement |
| E7 | The Gazette, BBOXX LTD (07177839), notice of appointment of administrators | Administration date |
| E3 | ESMAP, Beyond Connections: Energy Access Redefined (2015) | Multi Tier Framework thresholds (model SR20) |
| E8 | GOGLA investment data for 2024 | About USD 299m, down about 30% (book Ch. 11, 14) |
| E5, E6, E9, E10 | Sun King, Citi, d.light, ZOLA, SEforALL primary announcements | Securitisation, purchasing capacity, funding round, UEF |
| E4-G | M-Kopa Holdings Limited consolidated accounts FY2024 | Group revenue, if it is to be used |

## 2. Claim-by-claim position

| Ref | Claim | Book | Model | Current status in v0.1 / v0.7 | Verified position now | Evidence |
|---|---|---|---|---|---|---|
| E1 | Sector PAYGo collection rate about 62% in 2023 | Ch 1, 7, 15 | SR19, Calibration | Secondary reporting, grade B in register | PENDING PRIMARY DOCUMENT. The client's extraction (3 Oct 2026) gives 62% as the average for 2021 to 2023, with quartiles of 75% to 80% and below 50%: the book's 'in 2023' is revised. Definition and page still unknown. Never a model assumption; in v0.8 Calibration the reference is suspended until verified. | Client extraction; report not held |
| E1 | About half of PAYGo customers written off or more than 30 days late | Ch 1, 7, 15 | none | Secondary | CONFLICTING SOURCES. The client's extraction reports that about half of companies had a write-off ratio plus RAR30 between 30% and 50% in 2023 (18% in 2021): a statement about companies, not customers. The book's wording is withdrawn. | Client extraction |
| E2 | PERFORM KPI set | Ch 7, Annex A | Glossary, KPIs, Vintage_Dashboard, SR21 | Framework attributed to CGAP, GOGLA and Lighting Global; collection rate, receivables at risk and write offs presented as its standard metrics | VERIFIED against E2: the 2026 standard defines five KPIs: RR Paid vs Plan (PvP), RR Paid vs Financed (PvFin), RR PvP @90 Days, RR PvP @2x, and Ownership Rate @2x (E2 PDF page 8, summary guide). | E2 pages 8 to 18 |
| E2 | Collection rate is not a PERFORM substitute | none | none | Not stated | VERIFIED: "Do not use substitute metrics or proxies such as Collection Rate, days locked / enabled, or self-defined variants on Repayment Rate calculation" (E2 PDF page 10, rule 3A). The only accepted alternative basis is cumulative arrears (rule 3B). | E2 page 10 |
| E2 | Core RR rules | Ch 7 gives a simpler definition | Vintage_Engine | Not aligned | VERIFIED: RR excludes deposits and prepayments, includes arrears payments and write offs, and is cumulative since contract start after any free use period; instalments normalised to daily equivalents; payments recognised pro rata when applied to due instalments (E2 PDF pages 9 and 10; E2-G PDF page 5) | E2, E2-G |
| E2 | Ownership Rate @2x | Ch 7 (twice the tenor) | Vintage_Dashboard, RBF_Engine | Aligned on the horizon | VERIFIED on horizon (2x contract term); calculation details E2 PDF pages 16 to 18 still to be compared with the workbook formulas | E2 page 8 |
| E2a | Collection Rate, Receivables at Risk, Write-Off Ratio as PERFORM portfolio quality KPIs | Ch 7 | KPIs, Covenants | Presented as current | VERIFIED — HISTORICAL: defined in the 2021 guide (E2a portfolio quality section, PDF pages 14 to 33). They are not among the 2026 KPIs. They may be kept as operational or lender metrics with their own definitions printed. | E2a |
| E2b | Revenue recognition and ECL practice for PAYGo | Ch 8 | Glossary, FS | Not cited | To be cited for context only (IFRS 15 discussion PDF pages 6 to 21; IFRS 9 PDF pages 37 to 54). Not a basis for any compliance statement. | E2b |
| E3 | MTF tier thresholds (T4 at least 800 W / 3.4 kWh a day; T5 at least 2 kW / 8.2 kWh a day) | Ch 2.6 | SR20, Products tier labels | Grade D, not checked | UNVERIFIED (PENDING PRIMARY DOCUMENT) | None |
| E4 | M-KOPA FY2024 revenue USD 416m or USD 253.5m; net profit USD 9.2m; FY2023 loss USD 24.7m or 20.6m | Ch 15 | SR01 to SR04, Calibration | CONFLICT recorded, grade C | CONFLICTING SOURCES. The primary filing provided is M-KOPA UK LIMITED (revenue GBP 1,712,776 from carbon credit sales). It supports neither figure. | E4 PDF pages 3, 10, 18 |
| E5 | Sun King securitisations about USD 130m (May 2023) and USD 156m (July 2025); cumulative loans about USD 1.3bn to almost 10 million customers | Ch 3, 11, 12, 15 | SR05 to SR08 | Company and secondary reporting | PENDING PRIMARY DOCUMENT | None in project |
| E6 | d.light five securitisation facilities, about USD 718m purchasing capacity since 2020; 2024 facility USD 176m | Ch 3, 11, 12, 15 | SR10, SR11 | Secondary | PENDING PRIMARY DOCUMENT. The book already distinguishes purchasing capacity from debt raised. | None |
| E7 | BBOXX LTD entered administration on 19 May 2025; latest filed accounts FY2022 | Ch 1, 14 | SR14, SR15 | Register grade A, status "original not reviewed" | PENDING PRIMARY DOCUMENT. Grade A cannot stand while the notice is unread; the appointment date must come from the formal notice, not from a petition, hearing or publication date. | None |
| E8 | Off-grid solar investment about USD 299m in 2024, down about 30% | Ch 11, 14 | none | Secondary | PENDING PRIMARY DOCUMENT | None |
| E9 | ZOLA Electric USD 90m round, September 2021 | (register only) | SR18 | Secondary | PENDING PRIMARY DOCUMENT; currently context only | None |
| E10 | SEforALL Universal Energy Facility pays per verified connection | Ch 13 | none | Secondary, amounts not quoted | PENDING PRIMARY DOCUMENT | None |
| SR09, SR13, SR16, SR17 | Sun King MSME bond; d.light revenue estimate; Pawame figures | none | Register | Excluded or estimate | NOT USED (already excluded) | Register |

## 3. Findings on the register itself

1. The model register uses a five-grade scale (A to E). The brief requires A to D. Grade E ("contextual") will map to D or to NOT USED.
2. SR14 and SR15 (BBOXX) are graded A while their status text says the original has not been reviewed. The new register resolves this by separating the two judgements: the grade describes the source cited (the Gazette and the companies register are A), and the status (PENDING PRIMARY DOCUMENT) records that this project has not read them. Only the status governs use in the model.
3. SR19 (ESMAP) is graded B while marked "secondary reporting; original not yet reviewed". Under the same separation it keeps grade B and carries the status PENDING PRIMARY DOCUMENT.
4. SR21 (PERFORM) points to the 2021 framework page and lists collection rate and receivables at risk as framework KPIs. It must be split into E2 (2026, current) and E2a (2021, historical).
5. The register has no page, section or evidence-type fields. These will be added in 04_SOURCE_REGISTER_v1.0.xlsx.

## 4. What is needed to close the open items

* Upload of E1, E7 and E3, or access to www.esmap.org, documents1.worldbank.org, www.thegazette.co.uk and find-and-update.company-information.service.gov.uk.
* The consolidated FY2024 accounts of M-Kopa Holdings Limited, if the group figure is to be used at all.
* Primary announcements for E5, E6, E8, E9 and E10, or a decision to keep them as context with the secondary caveat.
