# BVMAC ingestion: Bulletin officiel de la cote (CEMAC bonds)

The BVMAC (Bourse des Valeurs Mobilières de l'Afrique Centrale) publishes a daily official price
list, the *Bulletin officiel de la cote* (BOC). It is the only free, text-based source for the
listed bonds of the CEMAC states (Cameroon, Gabon, Chad, Congo, …), of the regional development
bank BDEAC, and of some private issuers. This pipeline reads its bond tables, checks them strictly
and promotes the verified results: bond reference data to `security`, and **actual trades only**
to `market_observation`.

The owner holds BVMAC's written authorisation to publish these data **free of charge (no
resale)**. Every stored row keeps its source (`source_id`, `source_document_id`, `source_url`,
SHA-256 of the PDF, locator of each value) and the attribution text.

Rules followed throughout:
* no value is invented, estimated or filled in — a value is stored only if it is printed in the
  BOC; anything not printed is NULL with a `field_status` reason (`not_disclosed`);
* new data enters UNVERIFIED (staging table `bvmac_quote`) and is promoted only by the strict
  automatic checks below; any doubt holds the row for a person (`hold_reasons`);
* no LLM, no OCR.

## Source

| | |
|---|---|
| Listing | https://www.bvm-ac.org/bulletin-officiel-de-la-cote-boc/ — ~1,350 PDF links, Aug 2019 → today, one per trading session, labelled "BOC Séance de cotation du *d mois yyyy*" |
| Documents | text PDFs (Word-generated, ~27 pages): `wp-content/uploads/YYYY/MM/BOC-YYYYMMDD.pdf` (current), older `BOC-BVMAC-DD-MM-YY(YY).pdf`, a few variants (`-1`, `_compressed`, `BOC-automatise-…`) |
| Source row | `source.name = "BVMAC — Bulletin officiel de la cote"`, institution BVMAC, category `stock_exchange`, regional (no country), created by the fetcher if absent |
| Politeness | one request at a time, ≥ 1.2 s apart, `User-Agent: CartoucheIngest/1.0 (https://cartouche-africa.netlify.app)`; HTTPS_PROXY / SSL_CERT_FILE honoured, TLS never disabled |
| Malformed links | two listing links start with `https://https://…` (2020): skipped and reported, never repaired |

## Pipeline

```
listing ─▶ select by session date (--since/--until/--limit; date from the link label)
   └─ PDF ─▶ SourceDocument (SHA-256 unique, bytes + -layout text in the document store)
        └─ bvmac_extract (parser "bvmac_boc/1", pdftotext -layout)
             └─ bvmac_quote (staging, UNVERIFIED, one row per bond line, value + raw + locator)
                  └─ bvmac_check: re-download + re-hash, -layout AND -raw readings, strict checks
                       ├─ pass ─▶ VERIFIED; security (once per ISIN); market_observation if traded
                       └─ fail ─▶ stays UNVERIFIED with hold_reasons (human review)
```

```
cd backend
python -m app.ingest.bvmac --since 2024-01-01          # fetch + stage
python -m app.ingest.bvmac_check                       # strict checks + promotion
python -m app.ingest.bvmac_check --dry-run --report r.json
python -m app.ingest.bvmac --reextract                 # after a parser change (no network)
python -m app.seed.verified export                     # write the verified dataset (git)
```

Idempotent: a known URL is not downloaded again (`--refresh` forces it), identical bytes are
stored once, staging rows are unique per (document, ISIN) and re-extraction rewrites only rows
still UNVERIFIED; observations are unique per (security, date, kind, source).

## What the parser reads (`app/ingest/bvmac_extract.py`, version `bvmac_boc/1`)

Only the **bond** tables; equities, funds and commentary are ignored.

1. **Quote table** ("MARCHE DES OBLIGATIONS", sub-tables OBLIGATIONS DES ETATS / REGIONALES /
   PRIVEES). Per bond line: issuer, bond name, ISIN, mnemo and 17 columns:

   | field | printed column | unit |
   |---|---|---|
   | previous_price_date | Cours précédent — Date | date |
   | previous_price_pct | Cours précédent — Cours en % | % of nominal |
   | previous_price_fcfa | Cours précédent — Cours en FCFA | FCFA per bond |
   | nominal | Nominal (j+3) | FCFA (current, amortised nominal) |
   | accrued_coupon | Coupon couru (j+3) | FCFA per bond |
   | volume_demanded / volume_offered / volume_traded | Volume demandé / offert / transigé | number of bonds |
   | value_traded | Valeur transigée | FCFA (includes accrued coupon) |
   | trades | Nbr de trans | count |
   | status | Statut | e.g. `NC` (non coté = no trade), `PEq` |
   | open_price_pct / close_price_pct | Cours du jour — Ouver. / Clôt. | % of nominal |
   | upper_limit_pct / lower_limit_pct | Seuil Haut / Seuil Bas | % of nominal |
   | variation_pct | Variation | % |
   | next_reference_price_fcfa | Cours de référence de la séance suivante | FCFA per bond |

   Also the section "Total" lines and the front-page summary line
   "OBLIGATIONS <volume> <value> <trades> <lines>".
2. **Characteristics table** ("MARCHE DES OBLIGATIONS : N LIGNES OBLIGATAIRES"): coupon (Taux
   facial), first listing date, amount raised, number of securities, current nominal, price,
   maturity in years, amortisation (CONSTANT / IN FINE), periodicity (AN / SEM / TRIM),
   previous / next payment dates, outstanding (Encours), printed "Rend net/brut", turnover.

### How numbers are read
French format (thousands separated by spaces, decimal comma) with columns also separated by
spaces, so a line like `500 500 500 5 003 835 1` has several readings. The parser enumerates
every reading allowed by the number grammar and the column order, keeps those satisfying the
order-book identities (whole numbers of bonds and trades, traded ≤ demanded, traded ≤ offered,
1 ≤ trades ≤ traded, nothing traded ⇔ value 0 and 0 trades), and **accepts a field only if all
remaining readings agree**. In `-layout` text a gap of two or more spaces is a hard column
boundary. In `-raw` text (single spaces, line breaks that can fall inside a token such as
`GA000002031⏎3` or `EGA1⏎0`), each line break is tried both as a separator and as a join, a
record must end at a line end, and — only when two readings remain — the readings satisfying the
printed value identity are kept (the layout reading never uses this rule; the checker compares
the two).

Every value carries its raw printed text and a locator `p<page>:L<line> t<i>-<j>` (page, line and
token range in the `pdftotext -layout` text); the staging row keeps the printed line itself.

### Layouts
* `bvmac_boc/1`: the layout with a "Code ISIN" column and "Seuil Haut / Seuil Bas" columns,
  used since late 2023 (verified on every BOC from 2024-01-02 to 2026-10-01).
* **Not parsed** (`unsupported_layout`): the 2019–2022 layout, whose bond table has no ISIN
  column (bond code such as `ECMR.05-18/23` and an internal number) — bonds cannot be tied to
  an ISIN from the document itself, so no `bvmac_boc/0` parser was written. The mid-2023 layout
  (ISIN column but "Ouver./Clôt./Plus haut/Plus bas" instead of the price limits) is also
  refused because its header differs; it was not needed for the 2024 → today range.

## Strict checks (`app/ingest/bvmac_check.py`)

Per document: re-download from the official URL and compare the SHA-256 with the stored copy;
extract the text twice with its own `pdftotext -layout` and `pdftotext -raw` calls. Per bond
line, every check must pass:

* both readings complete, and equal to the staged value for every column (and mnemo); the
  layout issuer + name printed just before the ISIN in the raw text;
* session date identical in the PDF header (both readings), the listing label and the staged
  row; same BOC number. The header is read on the front page and on every page carrying a bond
  table, which must all agree (some BOCs repeat the previous session's header on later fund /
  company pages — e.g. 2026-01-02 — which is only a warning); printed variants "DU 2/08/2024"
  and "DU 1er/10/2025" are accepted;
* ISIN check digit (ISO 6166 / Luhn) and CEMAC prefix (CM, GA, TD, CG, GQ, CF); "ETAT DU <pays>"
  matches the ISIN country; the line is in a known section;
* prices (previous, open, close) in (0, 200] % of nominal; previous price FCFA = previous % ×
  nominal / 100 and next reference price = close % × nominal / 100, to the printed cent;
* order book: traded ≤ demanded and offered, 1 ≤ trades ≤ traded; status NC ⇔ nothing traded;
* if traded: value traded = traded × (close % × nominal / 100 + accrued coupon) within
  rounding (traded × 0.005 + 1 FCFA); printed variation = close / previous − 1 (± 0.006 %);
  the section "Total" line and the front-page "OBLIGATIONS" line print exactly the sums of the
  traded volumes, values and trades (both readings for the front page);
* characteristics table: the ISIN printed once, same mnemo, coupon / periodicity /
  amortisation read identically by both readings, coupon equal to the coupon in the bond name,
  periodicity AN / SEM / TRIM;
* no other document for the same session prints different trade figures; an already promoted
  security has the same coupon; an existing observation for that day has the same price and
  value.

Rows failing any check stay UNVERIFIED with `hold_reasons` and the full `checks` list.

## What is stored

**`security`** (once per ISIN, from the first passing line): ISIN, bond name as printed, mnemo
(`local_code`), issuer, country, `instrument_type = regional_bond` (bond listed on the regional
exchange), currency XAF, coupon (Taux facial), coupon frequency (AN → annual, SEM →
semi-annual, TRIM → quarterly), amortisation as printed, `listing_status`, FACT / VERIFIED,
provenance. Issuer and country:

| section printed | issuer | `issuer_type` | country |
|---|---|---|---|
| OBLIGATIONS DES ETATS ("ETAT DU CAMEROUN" …) | existing "Government of <country>" | sovereign | the state named, which must equal the ISIN prefix |
| OBLIGATIONS REGIONALES (BDEAC) | "BDEAC" as printed | supranational | ISIN prefix (CG: BDEAC bonds are registered in Congo) |
| OBLIGATIONS PRIVEES (ALIOS FINANCE, ACEP CAMEROUN, SNPC …) | name as printed | corporate (new enum value) | ISIN prefix |

Left NULL with `field_status = not_disclosed`: maturity date, issue date, face value, tenor,
minimum denomination — the BOC prints the years in the name ("2022-2029"), a maturity in years
and a first *listing* date, but no maturity or issue date; the nominal printed is the current
amortised nominal, not the face value.

**`market_observation`** (`kind = secondary_market`) — **only for sessions where the bond
traded** (volume traded > 0, status ≠ NC):
* `price` = printed closing price "Clôt." in **% of nominal**;
* `volume` = printed "Valeur transigée" in **FCFA** (includes the accrued coupon; the number of
  bonds and of trades are in the provenance note and in the staging row);
* `yield` NULL and `spread_bps` NULL (`not_disclosed`): the quote table prints no yield. The
  "Rend net/brut" column of the characteristics table is a static figure close to the coupon,
  not a market yield; it is kept in staging only;
* `date` = session date of the BOC; provenance note quotes the printed line and the locators.

**Not stored as facts:** the previous / reference prices of bonds that did not trade ("NC"):
they are stale reference prices (most bonds show "NC" at 100,00 for months); they stay in the
staging row only. Order-book volumes (demanded / offered), price limits, outstanding amounts,
turnover and the other characteristics are also kept in staging only.

**Verified export** (`app/seed/verified.py`): the export now also writes VERIFIED
`market_observation` rows (natural key ISIN + date + kind + source name), and the issuers and
sources they need (`issuers`, `sources` keys), so the daily job (which starts from an empty
database) re-creates them. Older files without these keys load as before.

## Results of the first run (2024-01-01 → 2026-10-04)

Run on 2026-10-04 (separate local database), all BOCs listed with a session date from
2024-01-02 to 2026-10-01:

| | |
|---|---|
| Documents | 686 BOCs downloaded and stored (SHA-256), all in layout `bvmac_boc/1`; 0 fetch errors, 0 unsupported, 0 scanned; re-download at check time: 686 / 686 identical hashes |
| Bond lines staged | 16,998 (one per bond per session); 94 of them with a trade |
| Parser | 16,991 lines read completely; 7 partial (2024-08-07: regional table printed without its last column; 2025-05-15: one order book with several readings) |
| Verified | 16,647 lines (92 traded lines) |
| Held for review | 351 lines, of which 2 traded (see below) |
| Bonds (ISINs) | 37, all promoted to `security`: sovereign 24 (Gabon 17, Cameroon 5, Congo 1, Chad 1), supranational 6 (BDEAC, ISIN CG), corporate 7 (Cameroon 6: ALIOS FINANCE, ACEP CAMEROUN …; Congo 1: SNPC) |
| Observations | 92 `secondary_market` rows on 27 bonds, 2024-01-03 → 2026-10-01 (36 in 2024, 33 in 2025, 23 in 2026): Cameroon 38 (sovereign 28, corporate 10), Congo 24 (BDEAC 21, sovereign 3), Gabon 27, Chad 3. 11 of them came from a line whose order-book numbers were separated by single spaces and were told apart by the value identity (and then confirmed by the printed totals) |

Held lines, by first reason (a line can have several):

| reason | lines | what it is |
|---|---|---|
| previous / next reference price ≠ price % × nominal | 185 | around partial redemptions the printed nominal (j+3) already reflects the amortisation while the FCFA prices do not (or the reverse); also matured bonds printed with nominal 0 |
| characteristics table not readable by both readings | 114 | wrapped bond names push the numbers to another line (e.g. April 2026) or the table is missing a row |
| session header missing on the bond pages | 32 | 2024-02-19 and 2024-05-16: the bond pages carry no "BULLETIN OFFICIEL DE LA COTE N° … DU …" header |
| coupon printed ≠ coupon in the name | 11 | BOC errors, e.g. 2026-04-13/14 ACEP "Taux facial 6" for "ACEP 7%", ALIOS 6.5% printed 7 (2026-01-14/15) |
| line not read completely / readings disagree | 7 | see "Parser" above |
| ISIN printed twice in the characteristics table | 4 | 2026-04-13/14: the AFC04 line carries ACEP's ISIN |

The 2 held trades: 2024-12-17 EGA07 (the sovereign "Total" line prints 806 712 000 / 1 but no
volume, so the totals check cannot pass) and 2025-10-01 ECMR6 (characteristics table unreadable
that day). Both remain in `bvmac_quote` for a person.

Audit by eye (10 random promoted observations against the PDF text, `pdftotext -layout` of the
stored file): all 10 match — closing price, value traded, and the session date in the page
header (e.g. 2024-08-13 EOCG: printed "100,00 95,00 … -5,00%", stored price 95, value
1 951 368 = 300 × (95 % × 6 666,667 + 171,23)).

## Limitations

* **Stale prices**: most bonds do not trade for weeks; the BOC keeps printing the last
  reference price with status NC. Those prices are never promoted. Observations are sparse
  (a few trades per month across the whole market).
* **Value includes accrued coupon**: `volume` is the cash amount printed (dirty), not nominal.
* **Days with several trades at different prices**: only the closing price is stored; such a
  day passes only if the value identity holds with the closing price, otherwise it is held.
* **Amortisation dates**: around a partial redemption the nominal printed (j+3) and the
  previous price in FCFA disagree; those lines are held (not traded lines lose nothing; a
  traded line on such a day would need a person).
* **Errors in the BOC itself** are held, not corrected (e.g. 2026-04-13/14: an ISIN printed on
  the wrong line of the characteristics table; coupon differing from the name).
* **Layout drift**: wrapped bond names that push the numbers to another line, or a new column
  set, make the line unreadable → held / `unsupported_layout`. Nothing is guessed.
* **2019 → 2023 history** is not ingested (no ISIN column before late 2023).
* **Corrected editions** for the same session would be compared; if they disagree, the line is
  held (none were found for 2024 → 2026).
