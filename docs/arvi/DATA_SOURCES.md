# ARVI pilot: data sources, licence and method

## Source

**UN Comtrade** (UN Statistics Division), public preview API
`https://comtradeapi.un.org/public/v1/preview/C/A/HS`. Annual data in the HS classification,
values in current USD (`primaryValue`), quantities as net weight (`netWgt`, kg).

- Exports (`flowCode=X`) declared by each pilot country, by partner.
- Mirror: imports (`flowCode=M`) declared by every other reporter, with the pilot country as partner.
- Kept: totals over customs procedure (`C00`), mode of transport (`0`) and second partner (`0`);
  individual partners only (no "World" total, no country groups).
- The preview takes one year per call and returns at most 500 records; queries hitting the cap
  are split by HS code. Calls are spaced and retried with backoff.

## Traceability

Every API response is archived byte-for-byte as `backend/var/arvi/raw/<sha256>.json.gz` and listed
in `backend/var/arvi/manifest.json` (URL, SHA-256, fetch time, record count). Each flow keeps the
SHA-256 of the response it came from, and each published cell lists them.
`backend/app/arvi/data/manifest.json` is the committed copy of the manifest (no trade values), so
a release can be re-fetched and compared.

## Licence: why raw data is not in git and no CSV is offered

UN Comtrade data are copyrighted by the United Nations. The terms published through WITS state
they are for internal use and may not be re-disseminated without written permission of UNSD. A
2014 UNSD policy waived the re-dissemination fee for free, non-profit visualisation and analysis
applications; whether it still applies has **not** been confirmed.

Consequences for ARVI:

1. Raw responses stay in `backend/var/` (git-ignored); the repository holds code and the manifest.
2. The public site shows indicators and per-partner values in a free visualisation, with
   attribution; it offers no bulk download.
3. **Before any paid offer (ARVI Professional / Institutional) or bulk export, written permission
   must be requested from UNSD (comtrade@un.org).**

## Method (version 0.1-pilot)

| Indicator | Definition | Nature |
|---|---|---|
| ARVI-1 | X = exports declared by the country; M = imports declared by partners. Per cell (partner, HS code, year): gap = M − X, relative gap = (M − X) / max(M, X). Positive and negative gaps of matched cells are summed separately; one-sided flows ("exporter only", "partner only") are reported apart and never counted as gaps. | CALCULATION |
| ARVI-2 | Unit value (USD/t) on cells where both sides declare value and weight, per HS code; ratio mirror / export. | CALCULATION |
| ARVI-3 | Share of value at each processing stage, from each side's declarations. Value shares, not metal content (grades not collected). | CALCULATION |
| ARVI-4/5/6 | Not published: need sourced fiscal, cost, grade and price parameters. | — |

**Confidence** (0–100, value-weighted for a country-resource-year): mirror availability (15),
quantity coherence (15), unit-value coherence (10), exporter reporting regularity (10), partner
reporting regularity (10), no hub/landlocked transit (10), persistence of the gap's sign (10).
The blueprint's two other components (share of gap explained, independent corroboration) are not
computed yet; the score is rescaled from 80 points. Levels: high ≥ 70, medium 40–69, low < 40
**[HYPOTHÈSE]**. A relative gap between 0 and +10 % is flagged as compatible with CIF/FOB costs
**[HYPOTHÈSE]**; no CIF/FOB adjustment is applied to the figures.

## Pilot scope

| Country | Resources |
|---|---|
| DR Congo | copper (2603, 7401, 7402, 7403), cobalt (2605, 282200, 8105) |
| Zambia | copper, cobalt |
| Guinea | bauxite (2606), alumina (281820), aluminium (7601) |
| Gabon | manganese (2602, 720211, 720219, 720230), timber (4403, 4407, 4408, 4412) |
| South Africa | manganese |
| Cameroon, Congo | timber |

Years 2019–2023. Hub partners [HYPOTHÈSE]: CHE, ARE, NLD, BEL, SGP, HKG. Landlocked: ZMB.

## Known limits

- A missing mirror can mean the partner does not report to Comtrade at all that year, not that
  the flow did not happen.
- Importers record the country of origin, exporters the country of last known destination:
  transit and trading hubs move value between partners.
- Net weights may be estimated by Comtrade; estimated weights lower the confidence score.
- Values are not adjusted for inflation or for CIF/FOB.

## Reproduce

```bash
cd backend
python -m app.arvi.run all        # fetch (a few minutes, rate-limited) + compute
cd .. && python site/arvi/build.py  # site/arvi/dist/, deploy to Netlify project "arvi-africa"
```
