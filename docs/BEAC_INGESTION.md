# BEAC (CEMAC) auction results: ingestion

Scope: the government-securities auctions of the six CEMAC states — Cameroon (CMR), Central
African Republic (CAF), Chad (TCD), Congo (COG), Equatorial Guinea (GNQ), Gabon (GAB); currency
XAF — as published by the Banque des États de l'Afrique Centrale (BEAC).

Use: the owner holds BEAC's written authorisation for **free publication** (no resale). Every
staged and promoted row carries the source URL, the SHA-256 of the official PDF and the
attribution line `app.ingest.beac.ATTRIBUTION`.

Rule followed throughout: **no value is inferred.** A value is stored only if two independent
OCR readings of the printed page agree and every coherence check passes; otherwise the field is
NULL with a `field_status` reason, and an ambiguous row is held in the review queue.

## Source

| | |
|---|---|
| Listing | https://www.beac.int/m-des-titres-publics/annonces-et-communiques/ — one static table `#documents_contenu_cpt` (Titre du document, Taille, Pays, Année), newest first, no pagination |
| Content (2026-10-04) | 992 PDFs: 295 result notices, 446 announcements, 237 weekly reports/dashboards, 14 other (calendars, financial-inclusion indicators, yield curve, buyback notices) |
| Format | Every notice is a **scanned image**. Some carry a text layer written by the scanner's OCR; it is unreliable ("6,007o", "ls 000") and is never read |
| Naming | File names and upload folders are inconsistent (many 2024–2026 files are in `/2016/11/`); the "Pays" column is misspelt and sometimes wrong. Neither is used as data: the country comes from the printed issue code, checked against the printed text |

Documents stored (results + announcements, 2019 → Sep 2026), by the listing's "Année":

| kind | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|
| result notices | 32 | 82 | 64 | 21 | 8 | 21 | 34 | 33 | 295 |
| announcements | 47 | 122 | 99 | 39 | 21 | 48 | 38 | 26 | 440 |

(738 downloads, 735 distinct files by SHA-256; weekly reports were classified but not downloaded.)

## Pipeline

```
beac.int listing ── classify title ─► result | announcement | weekly_report | other
   │ download (UA "CartoucheIngest/1.0 (...)", >= 1 s between requests) → SourceDocument + SHA-256
   ▼
beac_ocr: pdftoppm + tesseract, two passes (A, B), words with boxes, cached <sha>.ocr.json
   ▼
beac_extract "beac_resultat/1": label-anchored parse of each pass → one staging row per security
   (AuctionExtraction, FACT, UNVERIFIED; value set only where passes A and B agree)
   ▼
beac_check: strict checks (a)–(f) → app.ingest.queue.approve(reviewer=…) → security / auction
```

| Step | Code | Command |
|---|---|---|
| Listing, download | `backend/app/ingest/beac.py` | `python -m app.ingest.beac --kind result+announcement [--since --until --limit] [--no-extract]` |
| OCR | `backend/app/ingest/beac_ocr.py` | run by the extractor (cached) |
| Parse, stage | `backend/app/ingest/beac_extract.py` | `python -m app.ingest.beac --reextract --kind result+announcement` (no network) |
| Check, promote | `backend/app/ingest/beac_check.py` | `python -m app.ingest.beac_check [--approve] [--report out.json]` |
| Visual audit | `beac_check.audit_crops` | `python -m app.ingest.beac_check --audit <staging ids> --audit-dir var/beac_audit` |
| Export | `app.seed.verified` | `python -m app.seed.verified export` |

The source row "BEAC — marché des titres publics" (institution BEAC, central bank, regional:
`country_id` NULL) is registered by `app.seed.load` (so that the versioned export can be
re-loaded into a fresh database) and configured (URL, status active) by `app.ingest.beac`.

Idempotency: a URL already stored is not downloaded again; identical bytes are stored once;
re-extraction updates only UNVERIFIED rows (and removes unreviewed rows an earlier parser version
produced for the same document); reviewed rows are never touched.

## OCR method

Each page is rasterised and read twice, with configurations chosen so that their errors are as
independent as possible:

| pass | raster | tesseract | binarisation |
|---|---|---|---|
| A | 300 dpi greyscale | `--psm 4` (single column, variable sizes) | global Otsu (`thresholding_method=0`) |
| B | 400 dpi greyscale | `--psm 3` (automatic page segmentation) | Sauvola, adaptive/local (`thresholding_method=2`) |

Both: tesseract 5.3.4, LSTM (`--oem 1`), `fra+eng`. Each pass keeps its text and every word with
its box and confidence (JSON cache next to the PDF, keyed by the configuration signature). A
`--psm 6` pass was tried and rejected: it cannot read the bordered tables of the RCA notices.
Pages read: results 1–3, announcements page 1 (dealer lists follow).

Layout: words are grouped into printed lines by geometry; values are the numeric runs at the right
end of lines in the value column; each run goes to the vertically nearest label line, never to two
labels (two-line labels and skewed scans place values between lines).

## What is read (parser `beac_resultat/1`)

Per "Code Emission" block (one staging row per security; bilingual notices are merged by code,
and a field read differently in the two language copies is unreadable):

| printed (fr / en) | stored |
|---|---|
| Code Emission / Issuance Code: `CG1200002133 BTA-26 18-MARS-2027`, `CM2J00000279 OTA-03 ANS 6,25% 16-SEPT-2029` | ISIN, BTA/OTA, tenor (weeks / years), coupon (OTA), maturity |
| Séance du … / … session | auction date |
| Nombre de SVT du réseau / soumissionnaires (souscripteurs) | network size (staging only) / `number_of_bidders` |
| Montant annoncé / total des soumissions / total servi (millions FCFA) | `amount_offered` / `amount_submitted` / `amount_allocated` |
| Taux/Prix minimum, maximum proposé | `minimum_bid`, `maximum_bid` (BTA; OTA prices stay in staging) |
| Taux/Prix limite | `cutoff_yield` (BTA) / marginal price (OTA, staging) |
| Taux (d'intérêt)/Prix moyen pondéré | `weighted_average_yield` (BTA) / `average_price` (OTA, per 100) |
| Taux de rendement | staging only (`printed_yield_rate`) |
| Taux de couverture … (par les soumissions) | `reported_bid_to_cover` = printed % / 100 |

**Amounts** are printed in millions of FCFA and stored in FCFA as the printed decimal × 10^6,
exactly (Decimal arithmetic, no rounding: "27 550,19" → 27 550 190 000; "10 041,230" →
10 041 230 000.000). A number whose separators are ambiguous ("3.400": thousands or decimals?) is
not interpreted (NULL, `ambiguous_number`). Rates and prices are stored in percent as printed.
Each BEAC block prints its own announced amount and coverage, so the staging row is a
single-security operation for `approve()` (`tranche_count = 1`).

**Settlement date** (parser for announcements): "Code Emission", "Date limite de souscription"
(else the date of the opening sentence "… procèdera le lundi 25 août 2025 …") and "Date de
règlement", read with the same two-pass rule; dates printed after several codes apply to each.

Instrument mapping: `approve()` knows the UMOA codes BAT/OAT; BEAC's BTA (bills) and OTA (bonds)
are staged under `instrument` = BAT/OAT (same instrument types) with the printed code kept in
`fields.instrument_printed`.

## Strict checks (`beac_check`)

A row is approved only if **all** hold (details in the module docstring):

* **(a) double OCR** — every stored field identical in both passes (and in both language copies);
  digit confidence ≥ 50 in both passes; required fields present. Optional fields (SVT counts,
  printed yield, RCA "retained bids" ratio) unreadable in a pass stay NULL; two different readings
  hold the row. Chad prints no limit/average: when neither pass finds those labels they are NULL,
  `not_disclosed`.
* **(b) issue code** — CEMAC prefix, ISIN check digit valid (BEAC codes are genuine ISINs: 224 of
  the 226 distinct codes read identically by both passes are Luhn-valid; the 2 others are held),
  country named in the notice by both passes.
* **(c) arithmetic** — allotted ≤ submitted; amounts ≤ 1 000 billion FCFA (unit plausibility);
  min ≤ average ≤ max and min ≤ limit ≤ max; rates: average ≤ limit; prices: limit ≤ average;
  plausible ranges. Congo and Chad print OTA price bounds named after the implied rate ("prix
  minimum" 95 > "prix maximum" 90): the interval is ordered for the checks only.
* **(d) coverage** — printed coverage = submitted / offered within one unit of its last printed
  decimal; RCA's "par les soumissions retenues" ratio = allotted / submitted likewise.
* **(e) code line and operation** — 3rd code character 1 = BTA / 2 = OTA; BTA 13/26/52 weeks with
  maturity n weeks (±7 days) after the auction, no coupon; OTA coupon in (0, 15] %, maturity within
  auction + n years + 31 days; the title/opening must not describe a syndication, buyback or
  exchange.
* **(f) settlement date** — from an announcement with the same ISIN and auction date, agreed by
  both passes, unique, within 10 days; else NULL `not_available` (never a hold).

Promotion: `app.ingest.queue.approve(reviewer="Controle strict OCR BEAC (double OCR + coherence) -
autorisation de publication gratuite BEAC")`, then `yield_convention` is set to BEAC wording,
BTA minimum/maximum bids are filled (approve() marks them not_disclosed, a UMOA rule) and the
attribution is appended to the provenance notes.

## Results of the run of 2026-10-04 (local database `abi_beac`)

* 295 result notices → 300 staging rows (one per security block); 2 notices yielded no block
  (letter format), 1 buyback result skipped.
* **60 rows approved** (auctions promoted; 60 new securities); 240 held.
* Settlement date found on a matching announcement for 82 staged rows; 20 of the 60 promoted
  auctions carry it, the others have NULL with `not_available`.
* Export: `app/seed/data/verified_market_data.json` now holds 2 239 verified auctions
  (2 179 UMOA-Titres + 60 BEAC), 1 324 securities, 667 documents.

Approved (staged) per country and auction year:

| | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| CMR | 2 (8) | 6 (18) | 6 (16) | 0 (1) | – | – | 4 (9) | 2 (8) |
| TCD | – | 10 (17) | 3 (13) | 1 (5) | 1 (2) | 2 (4) | 0 (2) | 3 (4) |
| GAB | 0 (9) | 3 (22) | 1 (7) | 3 (10) | 2 (4) | 2 (12) | 1 (4) | 0 (8) |
| COG | 0 (2) | 2 (3) | 0 (4) | – | – | – | 0 (7) | 3 (10) |
| CAF | – | 2 (2) | 0 (1) | – | – | – | 0 (5) | 1 (3) |
| GNQ | 0 (2) | 0 (11) | 0 (6) | 0 (2) | – | – | – | – |

(cells: approved (staged); plus 39 staged rows whose code was not read identically by both
passes, hence no country, and 20 with a country but no auction date read identically.)

Held rows by main reason:

| reason | rows |
|---|---|
| a stored field read differently by the two passes, or unreadable | 87 |
| issue code not read identically (e.g. Congo's font: "C6" for "CG") | 39 |
| fails a coherence check (b)–(e) (coverage defined otherwise, avg outside [min, max], syndication, unit…) | 39 |
| no amount offered printed (Equatorial Guinea format) or not found | 27 |
| only the SVT counts / printed yield disagree | 27 |
| low OCR confidence only | 15 |
| duplicate of a promoted auction (French/English copies; all 5 identical to the promoted values) | 5 |
| ambiguous number ("3.400") | 1 |

## Visual audit

Page regions (pass A raster, 300 dpi) of 25 promoted rows — all five countries with promoted
rows, every year 2019–2026 — were rendered with `--audit` and every promoted value compared with
the image, plus auction-date lines and one settlement line on its announcement.

First round (64 promoted): **two mismatches**, both faithful readings of problematic documents:
* Chad, 24 Jan 2024 (TD2A00000727): the notice prints "16 678 630" under "(en millions de FCFA)"
  (and "30 000 000" offered); stored × 10^6 the amounts were 1 000 times too large. The coverage
  ratio is unit-free, so it passed. → added the amount plausibility check (c).
* Centrafrique, 28 Apr 2025: a **syndication** ("Communiqué des résultats de la syndication
  domestique"), promoted as a primary auction. → added the operation check (e) (5 rows).
The promotions were reverted, the checker tightened, the run repeated: 60 approved. Second round:
all 25 audited rows match the images exactly (code, maturity, coupon, SVT counts, three amounts,
min/max/limit/average, coverage, auction date; settlement date checked on one announcement).

## Coverage gaps and limitations

* **Partial listing**: few results for 2022 (21) and 2023 (8); the site is not exhaustive.
  Announcements without a result notice are not auctions we can record.
* **Equatorial Guinea**: notices print no amount offered and use "3.400" separators: none can pass
  (d); Spanish-only notices are not parsed. 0 rows promoted.
* **OCR quality** limits the yield: Congo's Comic-style font (G/6, 5/9 confusions), faint and
  skewed scans, stamps over values. Held rows stay in the queue for a human (`app.ingest.review`).
* Correlated OCR errors (both passes reading the same wrong digit) remain possible; the
  cross-checks (coverage, check digit, maturity/tenor, inequalities) cover amounts offered and
  submitted, the code and the dates, less so the allotted amount (only ≤ submitted, and the RCA
  ratio) and the rates of rows whose values sit inside [min, max].
* Gabon prints the coverage as submitted / allotted in some years; such rows fail (d) and are held.
* Buyback, syndication and exchange results are not promoted; weekly reports and dashboards are
  classified but not parsed.
* The OCR cache must be rebuilt if tesseract or its models change (signature records the
  configuration; the engine version is recorded in new caches).
* `site/` (quarterly report, brief, dataset pages) is written for UMOA-Titres only: its texts say
  "8 États de l'UMOA" and "Citez UMOA-Titres"; with BEAC rows in the export they must be updated
  (attribution per row) before the site is rebuilt and deployed.
