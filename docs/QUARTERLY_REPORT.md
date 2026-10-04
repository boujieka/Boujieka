# Quarterly report (synthèse trimestrielle)

`site/report.py` writes a summary report for every calendar quarter that has ended, using only the
verified real auctions in `backend/app/seed/data/verified_market_data.json`. Every figure is a
CALCULATION on FACT rows from UMOA-Titres. Nothing is estimated, filled in or synthetic.

```
python site/report.py --as-of 2026-10-04 --pdf        # standalone
python site/build.py  --as-of 2026-10-04 --pdf        # with the site (the daily job passes --pdf)
```

## Editions

| Edition | Where | Content | Deployed |
|---|---|---|---|
| Preview (free) | `site/dist/rapports/<AAAA-Tn>/apercu-{fr,en}.html` (+ `.pdf`) | Cover with flags, regional summary (key figures, 8-quarter charts, yields by residual maturity), country table, description of the full edition, method, legal notice, emblem credits | Yes. Linked from the site's « Rapports » section |
| Complete (free, with an account) | `site/reports/<AAAA-Tn>/cartouche-<AAAA-Tn>-complet-{fr,en}.html` (+ `.pdf`); with `--pdf` the PDF is also published in `site/dist/rapports/<AAAA-Tn>/` | Everything above, plus one page per country (flag and coat of arms, key figures vs previous quarter and previous year, 8-quarter charts, yields by maturity, 5 largest operations linked to the official PDF), plus the list of source documents | PDF only, behind the free account (`site/edge/gate.js`); the HTML stays in the git-ignored `site/reports/` |

## Definitions

- **Issuance:** every auction type except buybacks and switches. Buybacks are reported separately.
- **Amount allotted / bid:** sums over the quarter's issuance auctions.
- **Bid / allotted:** sum bid ÷ sum allotted, over auctions where both amounts are published. This is not the official cover ratio (bid ÷ offered), because the amount offered per security is often not published.
- **Weighted average yield:** the published weighted average yields, weighted by amount allotted. Because it mixes maturities, the report also breaks it down by residual maturity on the auction date (≤1, 1–3, 3–5, 5–7, >7 years).
- **Coverage:** totals are lower bounds. Auctions still awaiting verification, or whose results report could not be read, are not counted.

## Flags and coats of arms

`python site/emblems.py` fetches them from Wikimedia Commons into `brand/emblems/`. It writes a
manifest (`emblems.json`) with the following for each file:

- Commons page and author;
- licence as stated by Commons;
- SHA-1 as published by Commons, and SHA-256 of the downloaded bytes.

The script rejects any file whose SHA-1 differs from the published one, and any SVG with scripts or external references. The file names are chosen by hand to be each country's current version. Burkina Faso adopted new arms in 2025; the file used is `Coat of arms of Burkina Faso (2025-present).svg`. Recheck the names when a country changes its emblem.

Licences as stated by Commons on the fetch date:

- **Flags:** public domain.
- **Coats of arms:** mostly CC BY-SA 3.0. Mali is public domain; Togo is CC BY-SA 4.0. Commons tags most of them "insignia". That tag means use may be restricted by law independently of copyright.
- **Credits:** every report prints author, licence and source page for each emblem, as CC BY-SA requires. The images are reproduced unmodified.

**Before selling the complete edition, get legal advice.** State emblems are protected in many countries, for example by national laws on state symbols and by Article 6ter of the Paris Convention for trademarks. A paid publication must not suggest it is official. Each report carries the notice "Publication indépendante… n'émane d'aucun État, ni de la BCEAO, ni d'UMOA-Titres". To publish without the coats of arms, remove the `arms` entries from `brand/emblems/emblems.json`. The pages then render with flags only.

## Authorisation scope: free publication only

The owner holds written authorisations from UMOA-Titres, BEAC, BVMAC and other institutions. These authorisations cover **free publication only**, not resale (`backend/app/ingest/data/authorisations.json`). As a result:

- the complete edition is published free of charge;
- no purchase button is shown, and `site/build.py` ignores `CARTOUCHE_REPORT_PURCHASE_URL` while `commercial_use` is false;
- selling the report would need a new, explicit commercial authorisation from each source institution.

The legal points about the coats of arms above still apply to a free publication.
