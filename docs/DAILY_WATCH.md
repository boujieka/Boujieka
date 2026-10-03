# Daily update ("veille") — runs every 24 h

## What runs
`scripts/daily_run.sh` (fresh container safe), then a Netlify deploy of `site/dist/`.

1. **Market data, rolled forward to today (SYNTHETIC).** All 54 countries. The generator is
   deterministic per auction: past auctions never change, announced auctions get their synthetic
   result once their date passes, and new auctions are announced 21 days ahead.
2. **Opportunity Engine** re-run for today.
3. **Watch of official sources (REAL).** Each proposed or confirmed source URL (31 today) is
   fetched. The run records reachability, whether the visible text changed, and **new document
   links** (PDF, Word, Excel) compared with the previous run.
4. **Site rebuild:** `index.html` gets a "Veille quotidienne" section, and `veille.json` carries
   the report, the 60-day history, the feed of the last 150 new documents, and the comparison
   state.

State between runs lives in the published `https://cartouche-africa.netlify.app/veille.json`,
so no persistent disk is needed. If it cannot be read, the run records a fresh baseline.

## Schedule
A Claude Code Routine fires daily at **04:48 UTC** (05:48 in Douala/Lagos/Abidjan, which is
UTC+1/UTC+0, and 07:48 in Nairobi). It starts a fresh session, checks out the branch, runs the
script, deploys with the Netlify connector, verifies the live `veille.json`, and reports.

## Reading the results
- A **new document** is a lead to review (e.g. a newly posted auction-result PDF), not a
  verified market event. Nothing is extracted from documents yet (Phase 2).
- **Changed** pages include pages with live content (e.g. BRVM price bulletins change
  intraday), so "changed" is a weaker signal than "new document".
- **Known failures** as of 2026-10-03:
  - caa.cm: incomplete TLS certificate chain on the server; verification is not disabled.
  - afdb.org: blocks automated access with HTTP 403.
  - dette.ga: resets the connection.
  - finances.gouv.ci: returns an empty body.

## Run manually
```bash
./scripts/daily_run.sh                       # today, compared with the live veille.json
AS_OF=2026-10-04 PREVIOUS=none ./scripts/daily_run.sh   # specific date, fresh baseline
```
