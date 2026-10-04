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
A Claude Code Routine ("Veille quotidienne Cartouche") fires daily at **04:48 UTC**: 05:48 in
Douala and Lagos (UTC+1), 04:48 in Abidjan and Dakar (UTC+0), 07:48 in Nairobi. It starts a
fresh session, clones the repo, runs `scripts/daily_run.sh`, deploys, verifies the live
`veille.json` and reports.

**Deployment needs one setting:** add a Netlify personal access token as the environment
variable `NETLIFY_AUTH_TOKEN` in the cloud environment's settings. The routine then runs
`scripts/deploy_site.sh` (official Netlify CLI). Without it, the routine still runs the watch
and reports, but the site keeps the previous version. Tested on 2026-10-03: clone and watch
work in a scheduled session; the Netlify connector is not available there.

## Reading the results
- A **new document** is a lead to review (e.g. a newly posted auction-result PDF), not a
  verified market event. Nothing is extracted from documents yet (Phase 2).
- **Changed** pages include pages with live content (e.g. BRVM price bulletins change
  intraday), so "changed" is a weaker signal than "new document".
- **Interstitial pages** (anti-bot or "You are being redirected" shells) count as failures and
  never replace a page's known state. Otherwise the next real visit would report every old
  document as new; this happened once with a CBK page during setup.
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

## Daily collection and strict automatic approval (since 2026-10-04)

At the owner's instruction (2026-10-04), `scripts/daily_run.sh` runs `app.watch.daily --ingest`
by default (`INGEST=0` disables it):

1. Load reference data and the verified dataset (`backend/app/seed/data/verified_market_data.json`).
2. Collect UMOA-Titres result reports published since (last verified auction date − 45 days).
3. Run the strict checker (`app.ingest.autocheck`) and approve only rows that pass every rule:
   re-download + SHA-256, independent `pdftotext`, column placement against sibling securities,
   unit re-derivation, whole-number tenor, no number fragments, every consistency check passed,
   ISIN prefix = country, plausible rates. Approval goes through `app.ingest.queue.approve`
   (duplicates and ISIN conflicts are refused there). Reviewer recorded on every row:
   "Claude - routine quotidienne, controles automatiques stricts (instruction du proprietaire, 2026-10-04)".
   This is **not a human review**; it is stated on the site banner and in each row's provenance.
4. Export the verified dataset; the routine commits and pushes it when it changed.
   If a push fails, nothing is lost: the next run re-collects the same window and re-applies
   the same deterministic checks.
5. Rows that fail stay unverified and are not published.
