# Phase 4 report — Opportunity Engine & Opportunity Radar

Built ahead of Phases 2–3 at the owner's request. Runs on the stored auction data, which is
currently **synthetic**; every signal it produces is flagged `synthetic_data`.

## What it does
`/radar`: pick a country (grid row or chip) and see all active signals, with investor criteria.

**Three design features:**
1. **Signal passport.** Every signal shows (1) the published facts it used, linked to the
   auction and source; (2) the calculation, with its formula and inputs; (3) the rule and
   threshold that fired; (4) what would invalidate it; (5) caveats. The passport is stored with
   the signal (`opportunity.evidence`), so it is auditable later.
2. **Pan-African heat grid.** Countries × tenor buckets, showing the latest auction yield and a
   demand z-score of bid-to-cover against **that series' own history**. A self-relative measure
   stays comparable across markets even where yield conventions differ. Raw yields are shown but
   explicitly not for cross-country comparison. The colour scale is diverging blue ↔ gray ↔ red,
   always printed alongside ▲▼ and the value (never colour alone).
3. **Refinancing wall.** Allocated amounts of tracked securities maturing in each of the next
   12 months, per country. Useful to investors (supply ahead) and to treasuries (rollover
   concentration).

## Rules (`app/engine/opportunities.py`, thresholds in `RULES`)
| Signal | Fires when |
|---|---|
| Upcoming / newly announced auction | Auction within 14 days ("newly" if announced ≤ 7 days ago). Yield shown = previous published result, labelled as such |
| Significant yield movement | \|WA yield change vs previous same-tenor auction\| ≥ 25 bp, in the last 30 days |
| High / low demand | \|z\| ≥ 1.5 for bid-to-cover vs ≥ 6 (max 12) previous same-tenor auctions |
| Higher historical yield | Percentile rank ≥ 90 against ≥ 8 same-tenor auctions in 365 days |
| Yield curve inversion | Shorter tenor ≥ 15 bp above the next longer tenor (latest auctions, 120 days) |
| Refinancing concentration | A month holds ≥ 15% of next-12-month tracked maturities and ≥ 2× the monthly average |
| Cancelled / postponed | Status published as such |

Idempotent: upsert by `dedup_key`. Signals no longer detected are set `is_active=false`, not deleted.
Run with `python -m app.engine.run --as-of YYYY-MM-DD` (also runs after `app.seed.load --synthetic`).

## API
`GET /opportunities` (filters: country, type; criteria: min_yield, min/max_tenor_days, currency,
matching_only; sort: date | strength) · `GET /market/heat-grid` · `GET /countries/{iso3}/maturity-wall`.
Migration `0002` extends `opportunity` (country, label, strength, evidence, as_of, is_active).

## Tests
295 backend tests pass on SQLite and on PostgreSQL 16; 7 frontend tests pass; typecheck, lint and
build are clean; Playwright shows no console errors or page overflow (desktop, dark, 390px).
New tests:
- mean, stdev and z-score against Python's `statistics` module
- each rule on a hand-built market with hand-computed expectations (z, +50 bp, percentile 100)
- threshold changes switch signals off
- idempotency and deactivation
- every passport fact equals the stored database value
- neutral language: no "best", "buy", "sell", "guarantee" or "recommend"

## Known limitations
- Signals are only as good as the data; today all data is synthetic.
- Thresholds are reasonable defaults, not calibrated on real markets. Calibrate them in Phase 3
  once real history exists.
- "Signal intensity" (multiple of threshold) is not comparable across signal types. It is an
  ordering aid, not a score of attractiveness.
- The refinancing wall covers only auctioned securities in the database (no Eurobonds or loans).
- The yield-criteria filter uses the signal's yield. For upcoming auctions that is the
  previous auction's published yield, labelled "Ref. yield (previous auction)".
- No alerts or emails yet (Phase 5). The UI is English only (French localisation pending).
