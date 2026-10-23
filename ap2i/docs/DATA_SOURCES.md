# AP²I — Data sources and connector status

Status date: **2026-10-22**. A connector is **operational** only after it has retrieved, parsed, validated
and persisted real source records in a run whose evidence is stored (`source_connectors.status_evidence`,
`sync_runs`). The live table is always available at `GET /api/v1/admin/connectors` and
`python -m app.cli connector-report`.

## 1. How each source was checked

For every connector: official source identified → access method tried from the AP²I environment →
documentation and terms noted → fields inspected on real Cameroon records → source-specific parser →
sample validation → automated tests (synthetic fixtures, no network) → live test (`pytest -m live`).

## 2. Tier 1 — initial Cameroon MVP

| Connector | Source & access | Verified on real data | Status |
|---|---|---|---|
| `worldbank_projects` | World Bank Projects & Operations search API, public JSON, no key: `https://search.worldbank.org/api/v2/projects?format=json&countrycode_exact=CM` | 159 Cameroon projects retrieved and imported (run 2026-10-22). Fields used: id, name, status, board approval date, current closing date, `totalamt` (IBRD+IDA commitment, US$), `commitment`/`disbursement`/`available` (US$ millions, cumulative, 54 projects), `parentprojid` (17 Additional Financing links), implementing agency, PDO, abstract, major sector, lending instrument, financing plan lines. | **Operational** |
| `worldbank_documents` | World Bank Documents & Reports API (`search.worldbank.org/api/v2/wds?proid=…`), public, no key; plain-text renditions of each report | See §2.1 | See §2.1 |
| `worldbank_iati` | World Bank IATI publication (reporting-org `44000`) via the Code for IATI datastore mirror | 46 activities; dated commitment and disbursement transactions; matched deterministically to the Projects API records (`44000-Pxxxxxx` ↔ `Pxxxxxx`). | **Operational** |
| `afdb_iati` | African Development Bank IATI publication (reporting-org `XM-DAC-46002`) | 105 activities, amounts in XDR (SDR / units of account), bilingual titles, transactions types 2/3/5/6. | **Operational** |
| `afd_iati` | AFD IATI publication (reporting-org `FR-3`) | 306 activities = 128 project-level parents (no transactions) + financing-level children; French titles preserved. | **Operational** |
| `iati_generic` | All IATI publishers for a country (same mirror) | Implemented and covered by tests; disabled by default (6,851 Cameroon activities incl. humanitarian ones — enabling it changes the portfolio scope). | Not tested live |
| `afdb_portal` | AfDB projects portal / MapAfrica (direct) | `projectsportal.afdb.org` unreachable from this environment (proxy CONNECT 502); no documented public API identified. | **Blocked** — AfDB data comes from `afdb_iati`; the portal remains a manual-import source |
| `afd_opendata` | `opendata.afd.fr` (Opendatasoft) | Connection reset from this environment; `afd.fr` returned HTTP 503 (maintenance) on 2026-10-22. | **Blocked** — AFD data comes from `afd_iati` |
| `manual_upload` | Documented official-data import workflow (CSV/XLSX built from official documents) | Covered by tests; row-level validation; every row must cite `source_url` + `reporting_date`. | Manual workflow |

### 2.1 World Bank supervision and completion reports (`worldbank_documents`)
For every World Bank project of the active countries, the connector lists all disclosed documents (catalogued
as project documents with type, date and link) and parses the text rendition of:
* **ISR — Implementation Status and Results Reports** (from 2011, configurable `since_year`): ratings
  (progress towards the development objective, implementation progress, overall risk — previous and current),
  the "Implementation Status and Key Decisions" narrative, original and revised closing dates, the per-loan
  disbursement table (original, revised, cancelled, disbursed, undisbursed, % disbursed) and results indicators
  (baseline, previous, current, end target, with dates).
* **ICR — Implementation Completion and Results Reports** and **ICR Reviews by IEG**: outcome, risk to development
  outcome, Bank and borrower performance ratings (ICR and IEG).

Mapping: one `implementation_progress` row per report (rating, narrative, % disbursed when the report has a single
financing), `results_indicators` / `results_observations`, `documents` (with extracted text and prompt-injection
flags), and the original/revised closing dates of the project. **Physical progress is never set automatically**:
percentages quoted in narratives (e.g. "92% completion") are stored as candidates and must be validated by a Data
Reviewer (Admin → Physical progress to validate).

**Run of 2026-10-22 (Cameroon):** 3,213 documents listed for 161 World Bank identifiers, of which 490 reports
from 2011 onwards were parsed (435 ISRs, 27 ICRs, 28 ICR Reviews) for 49 projects; 0 failures. Ratings recognised
in 430/435 ISRs and 51/55 ICR/ICR Reviews; 5,806 results observations; 48 reports flagged as partially extracted;
5 physical-progress candidates awaiting review. 6 active projects have an unsatisfactory rating in their latest ISR.

Three ISR layouts exist (pre-2015 columnar tables, 2015–2024 blocks, post-2024). Since about 2024, the results
tables' values are absent from the text rendition (only indicator names). For those ISRs the PDF is downloaded
once and the table is read by word position (pymupdf): each number/date is assigned to the nearest of the eight
sub-columns (Baseline value / month-year, Previous value / date, Current value / date, Closing-period value /
month-year); empty cells stay empty; a row whose tokens do not fit their column is dropped; bold section titles,
the running header and the footer are ignored. The parsed table is kept as provenance (`source_observations`,
field `isr_pdf_results`, with the PDF's SHA-256 and URL) so the PDF is not downloaded again. "Month/Year" dates
have no day and are stored as empty dates. An actual value dated after its own report (source typo) is not stored
and is flagged (`result_date_after_report`) when it is more than 60 days after the catalogue date.

**PDF table run of 2026-10-22:** of the 44 ISRs whose text rendition had no table values, 32 had a PDF link
(the other 12 are 2011–2013 reports without a PDF link in the catalogue). 24 PDFs gave 783 indicator rows
(14 projects) and 475 dated results observations; 8 gave none — 6 are 2020-template ISRs whose PDO/intermediate
tables contain comments but no values (their Performance-Based Conditions tables use another layout and are not
read), 1 is a 2011 ISR and 1 a 2023 development-policy document of another template. Verified by hand against the PDF
words: Bénoué valley (P166072, ISR of 2025-03-04, e.g. "Total area irrigated": baseline 1,000, previous and
current 0.00 on 05-Apr-2024, target 14,000) and the Mora–Dabanga–Kousseri road indicator (P178207).

**Correction made in the same run (pre-2015 layout):** the plain-text tables of 2011–2014 ISRs do not keep a fixed
column grid (rows of one table are shifted by up to ~15 characters). The earlier parser cut cells at the header
positions, which moved values to the wrong column on shifted rows (e.g. an end target read as the current value)
and cut units ("Numbe"/"r"). Cells are now taken by header position only when every token is aligned with a header
column; otherwise a row with exactly three tokens is read in order, and any other row is dropped. All results
derived from World Bank reports were recomputed: 6,506 observations, 1,159 indicators.

### 2.2 AfDB completion reports and IDEV review notes (`afdb_documents`)
Source: the document links AfDB publishes in its own IATI activities (1,030 links for Cameroon).
* **evrd.afdb.org** (AfDB Independent Development Evaluation repository) serves PDFs directly: 33 links, of which
  31 PDFs (2 are Excel files, not parsed) — completion reports (PR…) and IDEV review notes of completion reports
  (PN…, "Note de revue de RAP").
* **www.afdb.org, mapafrica.afdb.org, idev.afdb.org** answer with an anti-bot challenge (HTTP 403 "Just a
  moment…"). **AP²I does not circumvent it.** 988 links — including the EER/IPR supervision reports — are therefore
  catalogued but not downloaded. A person can download them from the AfDB website and attach them through
  Admin → Uploads → "Attach an official document (PDF)" (`POST /api/v1/uploads/documents`).

Extracted (officially reported): approval, signature, effectiveness, original and revised closing dates, report
date, cancelled amount (UA), and — in IDEV review notes — the 1–4 ratings (development objective, Bank, borrower,
other stakeholders, outcomes) as given by the completion report and as validated by IDEV. A rating is kept only
when both numbers are present. Not extracted: the financing-sources table (misread too often on the real corpus),
completion reports' own rating tables (templates vary), and anything from EER/IPR (no sample could be retrieved to
build a parser; uploaded EER/IPR are stored as text).

**Run of 2026-10-22:** 31 documents parsed, 0 failures; 16 projects received completion data (64 dates), 12 have
IDEV ratings (12 of 19 review notes; the 7 others use an older template). Verified by hand against the PDF text:
Lom-Pangar (development objective 1/4) and two other ratings.

### IATI access method — important
The **official IATI Datastore API** (`https://api.iatistandard.org/datastore`) requires a free subscription key
(header `Ocp-Apim-Subscription-Key`). None was available in this build (HTTP 401 without key). The connector
supports it (set `AP2I_IATI_API_KEY`) but that path has **not been exercised**. All IATI data was retrieved from
the **Code for IATI datastore** (`https://datastore.codeforiati.org/api/1/access/activity.xml`), a community-run
public mirror of the same publisher files, which returns the activities' original IATI XML (stored verbatim).

## 3. Tier 2 and Tier 3

IATI reporting-organisation references below were **observed** as `reporting-org/@ref` on Cameroon activities
(datastore query, 2026-10-22). References that could not be observed are left empty — not guessed.

| Connector | Donor | Access | Cameroon activities | Status |
|---|---|---|---|---|
| `eib_iati` | European Investment Bank | IATI `XM-DAC-918-3` | 10 | **Operational** (run 2026-10-22: 10 retrieved, 10 imported) |
| `eu_intpa_iati` | EU — DG International Partnerships | IATI `XI-IATI-EC_INTPA` | 182 | **Operational** (182 retrieved, 182 imported) |
| `ifad_iati` | IFAD | IATI `XM-DAC-41108` | 12 | **Operational** (12 retrieved, 12 imported) |
| `undp_iati` | UNDP | IATI `XM-DAC-41114` | 108 | Implemented, not run live, disabled |
| `unicef_iati` | UNICEF | IATI `XM-DAC-41122` | 261 | Implemented, not run live, disabled |
| `fao_iati` | FAO | IATI `XM-DAC-41301` | 113 | Implemented, not run live, disabled |
| `unido_iati` | UNIDO | IATI `XM-DAC-41123` | 27 | Implemented, not run live, disabled |
| `bmz_iati` | German BMZ (DE-1) | IATI `DE-1` | 399 | Implemented, not run live, disabled |
| `isdb` | Islamic Development Bank | none found | — | Not implemented → manual import |
| `kfw` | KfW | not a separate IATI reporter for Cameroon (German flows under DE-1) | — | Not implemented → manual import |
| `jica` | JICA | none found for Cameroon | — | Not implemented → manual import |
| `gef` | GEF | GEF portal not assessed; GEF-funded UNDP activities appear in `undp_iati` | — | Not implemented |
| `gcf` | Green Climate Fund | open data not assessed | — | Not implemented |
| `badea`, `sfd`, `kfaed`, `adfd` | Arab funds | no machine-readable source identified | — | Not implemented → manual import |

Counts are activities reported by the datastore for `recipient-country=CM` on 2026-10-22; they include
humanitarian and technical-assistance activities, not only investment projects.

## 4. Reference and conversion sources

| Purpose | Source | Status |
|---|---|---|
| XAF/USD, any national currency/USD | World Bank WDI `PA.NUS.FCRF` (official exchange rate, LCU per US$, annual average) | Retrieved (2000–2025) |
| EUR/USD | World Bank WDI `PA.NUS.FCRF` for economy `EMU` | Retrieved (2000–2025) |
| US$ per SDR (AfDB amounts in XDR) | IMF Exchange Rates dataset `IMF.STA:ER`, series `USA.XDC_XDR.PA_RT.A` via `api.imf.org` SDMX 2.1 | Retrieved (2000–2025) |
| Country ISO codes | Cross-checked against the World Bank country API (all 54 ISO-2/ISO-3 match) | Live test passes |
| Map boundaries | Natural Earth via `world-atlas@2.0.2` countries-110m (public domain). CPV, STP, SYC, MUS and COM have no polygon at this scale and are shown as markers. | Used by the frontend |

2026 annual averages were not yet published for EUR and XDR at the status date: 2026 USD equivalents are
flagged incomplete instead of using another year's rate.

## 5. Cameroon national public investment data (Master prompt §13)

No machine-readable national source was found. The framework is implemented as a **documented import workflow**
(`POST /api/v1/uploads/budget-lines`, template `data_templates/budget_lines_template.csv`) storing, per line:
budget year, administrative and programme classification, project identifier, approved and revised
appropriation, commitment, payment, funding source and type (government / external / co-financed / PPP / SOE),
with the execution rate computed as `payment / (revised appropriation, else approved)`. Budget appropriations
live in `budget_allocations` and are never mixed with financing commitments or disbursements.
Candidate official sources (MINFI, MINEPAT, ARMP, Chambre des Comptes, INS) are registered per country
(`country_data_sources`); reachability is checked with `python -m app.cli check-country-sources`.
**No Cameroon budget data has been imported**: AP²I does not yet show government-funded investment.

## 5b. Counting rules added after the October 2026 data audit

* **Identical repeats in a source file are counted once.** Some publishers repeat the same transaction in one file with
  only the reference changed (EIB loan XM-DAC-918-3-20150526-85142: 17 identical EUR 50M commitments for a EUR 50M loan;
  AfDB quarterly disbursement totals published two or three times). Rows of one agreement with the same date, amount and
  currency (and flow type for disbursements) are counted once; the repeats stay stored with `is_counted = false` and a
  note, and a `duplicate_transaction` validation is recorded (run of 2026-10-23: 19 commitments and 70 disbursements).
* **EU decision vs contracts.** When a project has both an EU financing decision (`…-ACT-…`) and the contracts that
  implement it, only the contracts are counted (34 decision commitments on 24 projects); the decision's headline amount
  does not come back through the agreement amount.
* Effect on the Cameroon total of commitments (agreement positions, USD eq.): US$ 17.95 bn → US$ 16.39 bn.

## 6. What a source does NOT provide (never inferred)

* World Bank Projects API: no dated disbursement series by transaction type (the per-year `amount` arrays are
  unlabeled and are kept only as raw provenance), no original closing date, no physical progress.
* IATI: physical progress and operational status are not part of the standard; results indicators appear for
  some activities only.
* No source used here publishes operational status of completed infrastructure: AP²I reports it as unknown.
