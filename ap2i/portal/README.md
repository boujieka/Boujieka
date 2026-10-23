# AP²I public portal (ap2i-africa.netlify.app)

Interactive, read-only portal over a **public snapshot** of the AP²I database. Static site (Vite + React + ECharts +
MapLibre), deployed on Netlify. The full application (FastAPI + PostgreSQL + Next.js, with accounts, private
organisation data and official Project Rescue plans) is unchanged and remains the reference.

## Why a snapshot

Netlify does not run the Python backend or PostgreSQL. Until the backend is hosted elsewhere, the portal reads JSON
files exported from the real database. Every figure therefore comes from database records, but it is only as recent as
the last export (date shown in the sidebar and on every export).

## Data: what is exported and how it is checked

`python -m app.cli export-public-snapshot <portal>/public [ISO3 …]` (backend, `app/publish/snapshot.py`):

* API-shaped files (countries, Africa overview, alerts, data quality, country dashboard/portfolio, one file per
  project with its agreements, transactions, documents and sources) are produced by calling the real API **without
  credentials**: tenant-private projects, plan-gated field provenance and the Project Rescue diagnosis are never exported.
* Flat tables (`projects.json`, `agreements.json`, `flows.json`) use the backend finance functions
  (`agreement_position`, `FX.convert`): USD equivalents at the annual average rate of the transaction year; a missing
  rate or date gives `null`, never another year's rate.
* **Reconciliation (export fails if it does not hold):** per-year commitment / disbursement / expenditure totals
  (by currency and USD) recomputed from `flows.json` equal `compute_portfolio()`; total commitments (USD eq.) equal
  `/africa/overview`. The portal's own aggregations are checked against the same files (`src/lib/reconcile.test.ts`).

Run of 2026-10-22: 483 projects, 648 agreements, 4,769 dated transactions, 238 alerts (Cameroon); both checks OK.

## Modules

Africa Explorer (choropleth, 54 countries, grey = no data), Country intelligence (10 charts: annual commitments,
annual disbursements, sectors, institutions, instruments, status, attention, commitments vs disbursements, completions,
data completeness), Projects (table / cards / map with clustering, search, sort, pagination, comparison, CSV / Excel),
project profile, Finance (stacked bars, Sankey, treemap drill-down sector → institution → project → agreement →
transactions, costs, additional financing, undisbursed, cumulative execution), Performance (status, delays, financial
execution, operational status, risk matrix, alerts with evidence), Project Rescue (risk overview, timeline, gaps,
bottlenecks, rule-based checklist, **local draft** action plan with owners / deadlines / status, CSV export),
Data explorer (pivot of any two dimensions × measure, missing ≠ zero), Method & sources.

Global filters (country, years, sector, institution, status, instrument, region, alerts, minimum commitment,
completeness, search) live in the URL hash: views are shareable; saved views are stored in the browser.
Years = approval year for project lists, transaction year for annual series. FR / EN.

## Commands

```bash
npm ci
npm run build          # typecheck + production build (dist/)
npm test               # unit tests incl. reconciliation on public/data
npm run e2e            # Playwright (playwright-core) end-to-end tests on the built site
E2E_BASE=https://ap2i-africa.netlify.app/ npm run e2e   # same tests against production
```

Chromium path: `CHROMIUM_PATH` (default `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`).

## Refresh and deploy

1. Backend: run the syncs / `post-sync`, then
   `python -m app.cli export-public-snapshot ../portal/public` (fails if the reconciliation fails).
2. `npm run build && npm test && npm run e2e`.
3. Deploy the **content of `dist/`** (it contains `public/data`, which is git-ignored) to the Netlify site `ap2i-africa`
   (site id `a6395298-e654-4e1a-9b8f-21911b9fd49c`), e.g. `netlify deploy --prod --dir dist`. No build runs on Netlify;
   no secret is needed by the site. Security headers and caching are in `public/_headers`.
4. Verify production: `E2E_BASE=https://ap2i-africa.netlify.app/ npm run e2e` and `curl -sI …/data/meta.json`.

**If a deploy is wrong:** a failed Netlify deploy never goes live (the previous one stays). For a bad published
deploy, fix forward: rebuild from the previous good commit (or previous snapshot) and deploy it again.

## Commercial pages and before going live

`src/lib/site.ts` holds the publisher identity (`SITE.publisher`) and `contactFormEnabled`. While the publisher is not
set, the legal pages show a visible "to be completed" notice and the demo-request form (Netlify Forms, `#/contact`) is
disabled: fill in the legal entity, country and contact address, have the terms / privacy texts validated, then enable
the form. Plans (`#/plans`) mirror `backend/app/reference/catalog.py` (prices on request).

## Moving to live data later

When the FastAPI backend is hosted (any container host with PostgreSQL), either deploy the Next.js application on
Netlify with `AP2I_API_URL` pointing to it, or keep this portal and regenerate the snapshot on a schedule. CORS
(`AP2I_CORS_ORIGINS`) must then include the portal origin; secrets stay in the backend environment only.

## Limitations

* Read-only snapshot: no accounts, no saved views across devices, no official Project Rescue plans (drafts stay in the
  browser and are labelled as unofficial). No AI-generated content.
* Filtering runs in the browser over the exported tables (small: ≈2 MB gzip-compressed for the core tables);
  per-project files load on demand.
* Coverage: connected donor sources for Cameroon only; no national budget data; physical progress, contracts,
  amendments and operational status are mostly not published by the sources (shown as not available).
