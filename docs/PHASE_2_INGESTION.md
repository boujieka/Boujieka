# Phase 2: verified ingestion, first source (UMOA-Titres)

Scope: one regional source end to end. UMOA-Titres organises the BAT (bills) and OAT (bonds)
auctions of the eight WAEMU states and publishes an official result report for each one.
This phase fetches those reports, extracts their figures, and holds them in a review queue.
Nothing reaches the public API or the Opportunity Engine until a person has checked it
against the document.

Rule followed throughout: **no value is inferred.** The parser reads text. A field it cannot
read stays empty, with a status. No LLM is involved at any step.

## Pipeline

```
umoatitres.org/fr/emissions/          listing "Annonces et résultats" → one row per security
   └─ /fr/emission/<operation>/       operation page → documents under headings
        └─ "Compte rendu" PDF         official result report (compte rendu d'adjudication)
             │ fetch: SHA-256, stored once (source_document + document store)
             │ extract: pdftotext -layout → parser → one row per security (tranche)
             ▼
        auction_extraction            staging, FACT + UNVERIFIED, value + locator + confidence
             │ human review: python -m app.ingest.review approve|reject
             ▼
        security / auction            VERIFIED FACT, provenance → document, reviewer, date
```

| Step | Code | Notes |
|---|---|---|
| Fetch | `app/ingest/umoa.py` | Listing table "Émissions réalisées", each operation page, the PDF under the "Compte rendu" heading. A 0.5 s pause between requests. Uses HTTPS_PROXY and SSL_CERT_FILE; TLS verification is never disabled. |
| Store | `save_document()` | `SourceDocument` with url, title, `document_type=auction_result`, `retrieved_at`, `content_sha256` (unique), `mime_type`, `storage_path`. `publication_date` is set from the report's "Dakar le …" line when present. Bytes and extracted text go to `ABI_DOCUMENT_STORE_DIR` (default `var/documents/`, git-ignored), named by hash. |
| Extract | `app/ingest/pdf.py`, `app/ingest/umoa_extract.py` | `pdftotext -layout` (poppler; installed in the Docker image). `pypdf` is the fallback if installed. Scanned PDFs (no text layer) are marked `needs_ocr`; OCR is not run automatically. |
| Stage | `AuctionExtraction` (`auction_extraction`) | One row per (document, ISIN). Re-extraction updates rows still UNVERIFIED and never touches reviewed rows. |
| Review | `app/ingest/review.py`, `app/ingest/queue.py` | CLI; every decision is written to the row (`reviewed_by`, `reviewed_at`, `review_reason`) and to the append-only `extraction_review_event`. |
| Read API | `GET /api/v1/ingest/queue` | Admin-oriented. **TODO: protect with `require_role("analyst")`** (auth is landing separately). |

### Idempotency
* An operation's PDF URL already stored is not downloaded again (`--refresh` forces it).
* The same bytes are never stored twice (`content_sha256` is unique), even under another URL.
  This happens on the site: one "Annonce" link points to a Compte rendu file.
* Staging rows are unique per (document, tranche). Approval refuses a second auction for
  the same security, date and type, so a duplicate document cannot create a duplicate fact.

### Why a staging table
Every public read path (auctions, securities, yield curves, heat grid, maturity walls,
dashboard, Opportunity Engine) reads `auction` and `security` directly. With unreviewed rows
in a separate table, an unverified value cannot leak into a public answer through a query
that forgot a filter. As a second guard, the engine's `load_market` now only loads auctions
whose status is `verified` or `synthetic`.

## The result report (two layouts, 2014 → today)

* **Single security**: "Label : value" pairs, sometimes two per line.
* **Simultaneous issue** ("ES", about 2023 onwards): a header block with one column per
  ISIN (name, auction number, tenor, maturity, nominal, coupon), global totals, then a results
  table headed "OAT - 2 ans … BAT - 364 jours". Columns are matched to the ISIN columns in
  order and checked against instrument and tenor. If they disagree the parser reorders them
  when the match is unique; otherwise it flags the row.
* **2026 template variants**: header values printed on the line *below* their label
  (overlaid onto the label line, keeping the label's locator); amount cells separated by a
  single space (cut on the "… dont ONC :x" pattern); accrued coupon printed as a bare ratio
  (×100, noted).
* **Several reports in one PDF** (e.g. "EC" exchange operations: an issue report then one or
  more "COMPTE RENDU DE RACHAT" reports): each section is parsed on its own. Buyback
  tranches get the key `<ISIN>/buyback` and `operation_kind=buyback`, and are promoted as
  `auction_type=buyback`. Each tranche keeps its own section's totals.
* In the results table, an empty cell (as opposed to a printed "-") is `not_available` with
  an error, so a mis-split row can never pass as "not disclosed".

### Fields extracted

Per security (tranche): `isin`, `security_name`, `auction_number`, `instrument` (BAT/OAT),
`tenor` and `tenor_days`, `maturity_date`, `face_value`, `coupon_rate` (OAT),
`accrued_coupon_rate`, `auction_date`, `settlement_date` (date de valeur),
`number_of_participants`, `number_of_bids`, `amount_submitted`, `amount_allocated`,
`amount_rejected`, `absorption_rate`, `marginal_rate` and `weighted_average_rate` (BAT), or
`marginal_price` and `weighted_average_price` (OAT, in % of nominal or FCFA per unit), and
`weighted_average_yield` (rendement moyen pondéré). For a single-security operation,
`amount_offered` is filled too.

Per operation (`operation`): issuer, `country_iso3`, `security_type`, `total_amount_offered`,
`total_onc_offered`, `total_amount_submitted/allocated/rejected`, `coverage_bids_pct`,
`coverage_accepted_pct`, `absorption_rate`, `publication_date`, layout, tranche count.

Each value is stored as `{value, raw, locator, confidence, unit?, note?}`. For example:

```json
"weighted_average_yield": {"value": "8.49", "raw": "8,49%",
  "locator": "p1:L61 'rendement moyen pondere' col 1/5", "confidence": 0.9, "unit": "percent"}
```

* **Normalisation** is unit conversion only: French number format, "millions de FCFA" to
  FCFA, a ratio printed without "%" multiplied by 100. Each conversion is noted on the field.
  `tenor_days` for "N ans" is N × 365, the platform's bucket convention (noted).
* **Confidence** is deterministic: 0.95 for a single labelled value; 0.90 for a column
  assigned by count; 0.80 for a column assigned by position or a value from a multi-line
  block; 0.75 for a converted ratio. It is capped at 0.6 when a column mapping or a
  consistency check is doubtful. The row's `confidence_score` is the minimum over key fields.
* **Empty fields.** If the label is present but blank, "-" or "ND", or absent from this
  report format (for example, no weighted yield in 2016 reports), the field is
  `not_disclosed`. If the label is present but its value cannot be read, the field is
  `not_available`, an error is recorded, and the row is `partial`. A row is `complete` when
  every expected field is either read or visibly not disclosed.
* **Consistency checks** (CALCULATION, shown to the reviewer, never used to change a value):
  tranche sums against published totals, submitted = allocated + rejected (tolerance from
  printed precision), ISIN prefix against issuer, auction ≤ settlement < maturity. A
  security with nothing allotted is flagged, because its printed "0,00 %" is not a yield.

### Promotion on approval (`app/ingest/queue.py`)

| auction column | from |
|---|---|
| `amount_offered` | single-security operation: amount offered. Multi-security: NULL, `not_disclosed` (UMOA-Titres publishes one global amount; it stays in the staging row) |
| `amount_submitted` / `amount_allocated` | "Montant global des soumissions" / "Soumissions retenues" for the tranche |
| `cutoff_yield` | BAT: "Taux marginal". OAT: NULL, `not_disclosed` (a marginal *price* is published) |
| `weighted_average_yield` | "Rendement moyen pondéré" |
| `average_price` | OAT: "Prix moyen pondéré" per 100 of nominal (converted from FCFA per unit when printed that way, with a note) |
| `reported_bid_to_cover` | single-security operation: "Taux de couverture … par les soumissions" / 100. Multi: NULL, `not_disclosed` |
| `number_of_bidders` | "Nombre de participants" |
| `auction_type` | `buyback` when the auction number starts with "RA-", else `primary_auction` |
| `minimum_bid`, `maximum_bid`, `number_of_successful_bidders` | not published → `not_disclosed` |

If nothing was allotted, the yield, cutoff and price columns stay NULL, with a note. The
security is found or created by ISIN, and approval stops on any conflict (different
country, instrument or maturity). Real rows always have `is_synthetic=false`, so the
existing CHECK constraint holds. `issue_date` and `coupon_frequency` are `not_disclosed`:
the result report doesn't state them (the tender notice does).

## Verification workflow

```bash
export ABI_DATABASE_URL=postgresql+psycopg://…        # never the shared DB for trials
python -m app.ingest.umoa --since 2026-07-01           # fetch + extract (or --limit N)
python -m app.ingest.review list                       # UNVERIFIED queue
python -m app.ingest.review show 42                    # every value, raw text, page/line, checks, PDF URL + local copy
python -m app.ingest.review approve 42 --reviewer "A. Diallo" --note "checked p1"
python -m app.ingest.review reject 43 --reason "column shift on OAT 5 ans" --reviewer "A. Diallo"
```

The reviewer opens the PDF, compares each value with the `raw` text at its `locator`, and
reads the warnings and failed checks. Rejected rows stay for audit. Approved rows become
`verification_status=verified`, `data_nature=FACT` in `auction`/`security`, with provenance
(source, document id, URL, publication date, extraction date, confidence, reviewer and date in
`provenance_notes`). From then on, public endpoints serve them like any fact, and
`include_synthetic=false` returns only them.

## Live dry run (2026-10-04, throwaway database `abi_ingest`, since dropped)

`python -m app.ingest.umoa --since 2026-01-01`, run against the live site:

| | |
|---|---|
| Operations listed on the official page (all years, 2014 onwards) | 1,847 |
| Operations selected (operation date ≥ 2026-01-01) | 158 |
| Result reports ("Compte rendu") found / downloaded / stored | 158 / 158 / 158 (0 fetch errors) |
| Staged tranche extractions | 605 (includes buyback sections of exchange operations) |
| Documents parsed **complete** | 152 |
| Documents **partial** | 6. Each has one security that got no bids, where the report leaves the absorption cell blank instead of printing "-". Flagged `not_available` on purpose; a reviewer decides. |
| Documents failed / needing OCR | 0 / 0 |
| Rows with a failed consistency check (confidence 0.6) | 4. All from one exchange operation (CI, 2026-02-05) whose buyback total spans three buyback reports. This is a quirk of the source, not a parse error. |

The first live pass found three template variants that the fixtures did not cover. All
three are now handled and covered by real fixtures: values printed under their labels,
amount cells separated by one space or by none (the sum checks caught this one), and
issue-plus-buyback PDFs. Documents were re-parsed offline with
`python -m app.ingest.umoa --reextract`.

Spot checks: extraction compared by hand with the PDF text.

| Document | Security | Extracted | In the PDF |
|---|---|---|---|
| Compte-Rendu-ES-25.09.2026.pdf (Senegal) | SN0000005372, OAT 5 ans | maturity 2031-09-28, coupon 6.45, 14 participants / 25 bids, submitted = allotted 44 885 270 000, marginal price 92.0700, WA price 92.8072, yield 8.26 | 28/09/2031 · 6,45% · 14 / 25 · 44 885,27 M · 92,0700% · 92,8072% · 8,26% ✔ |
| Compte-Rendu-BF-ES-23.09.2026.pdf (Burkina) | BF0000005116, BAT 364 jours | maturity 2027-09-22, 3 participants, submitted 15 515 000 000, allotted 5 510 000 000, marginal 3.7500, WA rate 3.5685, yield 3.70 | 22/09/2027 · 3 · 15 515,00 M · 5 510,00 M · 3,7500% · 3,5685% · 3,70% ✔ |
| COmpte-Rendu-TG-ES-26.06.2026.pdf (Togo) | TG0000003524, OAT 5 ans | maturity 2031-06-15, coupon 6.35, 10 participants, submitted 40 700 630 000, allotted 33 000 000 000, marginal price 96.0100, WA price 96.4218, yield 7.23 | 15/06/2031 · 6,35% · 10 · 40 700,63 M (cell glued to the previous one) · 33 000,00 M · 96,0100% · 96,4218% · 7,23% ✔ |

On the same database, `review approve` and `review reject` were exercised once each.
Approval produced a VERIFIED FACT `auction` row with its field statuses. Both decisions
were recorded in `extraction_review_event`.

## Limits and known gaps

* **One document type.** Only the "Compte rendu" is extracted. The "Annonce" (same results
  in exact FCFA) and the operation page's HTML result block could cross-check the
  extraction automatically. Tender notices (announced auctions, coupon frequency, issue
  date) are not parsed yet.
* **Layout dependence.** The parser reads `pdftotext -layout` columns. A column shift in
  a new template is caught by the instrument and tenor cross-check and the sum checks, and
  surfaces as `partial` or low confidence, not as silent errors.
* **Reopenings** are recorded as `primary_auction`: the report doesn't say whether an ISIN
  is new or reopened.
* **Yield conventions.** BAT "taux" and "rendement" are stored as published. Converting
  between conventions is Phase 3.
* **Synthetic and real in one database.** After approval, real WAEMU auctions sit next to
  synthetic ones, and the engine's series key (country, instrument, tenor) does not split
  on `is_synthetic`. For a real-data deployment, load no synthetic data, or split the series
  first.
* **Scheduling.** Runs are manual. Phase 5 adds the daily trigger. The daily watch already
  flags new documents on the same pages.
* **No auth yet** on `/api/v1/ingest/queue` (TODO `require_role("analyst")`).

## Next sources

| Source | What | Expected work |
|---|---|---|
| **BEAC** (CEMAC: CMR, CAF, TCD, COG, GNQ, GAB) | BTA/OTA auction results on the BEAC securities market pages (PDF notices and results) | New listing parser and result-report parser. Same staging, review and promotion (instrument map BTA→bill, OTA→bond). |
| **CBK** (Kenya) | Weekly T-bill and monthly T-bond auction results (PDF press releases) | Watch already tracks the pages. Results are per tenor, with accepted and rejected amounts and average rates. Expect anti-bot interstitials (see DAILY_WATCH.md). |

Each new source needs a parser module plus fixtures of real documents with hand-checked
values. The queue, the review CLI, promotion and the API are source-agnostic, apart from the
instrument map and the field mapping in `queue.py`.
