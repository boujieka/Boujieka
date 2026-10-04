# Cartouche · African Bond Intelligence

**Africa's Sovereign Debt Opportunity Engine** — a source-first intelligence platform for African
sovereign Treasury bills, bonds and Eurobonds.

> Information and analytics only. Not investment advice, not a recommendation, and no guarantee of
> returns or of access to any market.

## Status

**Phases 1 and 4 complete** (database, provenance, read API, dashboard; Opportunity Engine + Opportunity Radar).
**Phase 1b security baseline in place**: API keys (hashed), roles, rate limiting, audit log, security
headers — see [`docs/SECURITY.md`](docs/SECURITY.md).
See [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) and
[`docs/PHASE_1_REPORT.md`](docs/PHASE_1_REPORT.md), [`docs/PHASE_4_REPORT.md`](docs/PHASE_4_REPORT.md).

⚠️ **All market data currently in the system is SYNTHETIC** — generated for development, labelled
as such in the database, the API and the UI, and not real. No official source is being crawled yet.

## Public showcase site

**https://cartouche-africa.netlify.app**: a static snapshot of the platform (all 54 countries,
heat grid, signals with passports, refinancing walls, source registry). Market data on it is
synthetic and labelled as such. To rebuild and redeploy:

```bash
python site/build.py --as-of 2026-10-03   # needs a seeded database; writes site/dist/
# then deploy site/dist/ to the Netlify project "cartouche-africa"
```

The site is available in French (reference), English, Portuguese and Spanish (`site/i18n/*.json`;
the build fails if a language misses a key). A global country menu filters every section. It also
has an investor area (official access procedures, accredited dealers, step-by-step guide), a
subscription simulator (CALCULATION), a diversification test bench and a glossary.

Brand (logo, colours from ancient Egyptian pigments, type): see [`brand/BRAND.md`](brand/BRAND.md).

## Coverage

All **54 African UN member states** have a reference profile: ISO codes, currency, monetary
zone (CEMAC, WAEMU, CMA or national), central bank and a registered central-bank source.
These profiles are unverified. **Synthetic** market data covers all 54 countries (hand-set
anchor yields for the 6 pilot countries; hash-derived, deliberately unrelated to real markets
for the other 48). Whether each country runs regular domestic auctions has not been verified.

## Daily update (every 24 h)
A scheduled job rolls the data forward, re-runs the Opportunity Engine, **watches the official
source pages for real** (reachability, changes, newly published documents), and redeploys the
site. See [`docs/DAILY_WATCH.md`](docs/DAILY_WATCH.md).

## Principles

- **Source first.** Every market-data record carries source, URL, document, publication date,
  extraction date, verification status and confidence.
- **Never invent.** Empty fields are reported as *Not disclosed* (source doesn't publish it),
  *Not available* (we have no source) or *Pending* (result not yet published) — never guessed.
- **Never mix kinds of value.** API payloads separate `official` (FACT / SYNTHETIC),
  `calculated` (CALCULATION, with definitions) and `provenance`. ESTIMATE and AI_INTERPRETATION
  are reserved labels for later phases.
- **Synthetic is enforced.** A database CHECK constraint refuses any row with `is_synthetic=true`
  unless it is also labelled `data_nature=SYNTHETIC` and `verification_status=synthetic`.
- **Neutral language.** Nothing is ranked "best" or recommended.

## Layout

```
backend/    FastAPI · SQLAlchemy 2 · Alembic · PostgreSQL
  app/models/       Country, Issuer, Security, Auction, Source, SourceDocument,
                    MarketObservation, Opportunity, SubscriptionRoute
  app/analytics/    Decimal-only financial calculations (CALCULATION)
  app/api/          Read-only REST API under /api/v1
  app/seed/         Unverified reference data + labelled synthetic generator
  tests/            pytest (runs on SQLite, or Postgres via ABI_TEST_DATABASE_URL)
frontend/   Next.js 15 · TypeScript · Tailwind v4 · shadcn-style components · Recharts
docs/       Plan and phase reports
```

## Running locally

Requirements: Python 3.11+, Node 22+, PostgreSQL 16.

```bash
# Backend
cd backend
pip install -e ".[dev]"
export ABI_DATABASE_URL=postgresql+psycopg://abi:abi@localhost:5432/abi
alembic upgrade head
python -m app.seed.load --synthetic      # idempotent; also runs the Opportunity Engine
python -m app.engine.run --as-of 2026-10-03   # re-run signal detection
python -m app.security.keys create --name me --role admin   # prints the key ONCE
uvicorn app.main:app --port 8000 --no-server-header   # API docs at http://localhost:8000/docs

# Frontend
cd frontend
npm install
ABI_API_URL=http://localhost:8000/api/v1 ABI_API_KEY=<analyst or admin key> npm run dev   # http://localhost:3000
# ABI_API_KEY is optional (only /admin pages need it) and server-side only: never NEXT_PUBLIC_.
```

Or `docker compose up --build` (see `docker-compose.yml`; local credentials only).

## Tests

```bash
cd backend && pytest                                    # SQLite
ABI_TEST_DATABASE_URL=postgresql+psycopg://abi:abi@localhost:5432/abi_test pytest   # Postgres
cd frontend && npm test && npm run typecheck && npm run lint && npm run build
```

## API (v1)

Market endpoints are **public** (no key) and read-only. Protected endpoints need an API key in the
`X-API-Key` header: no key → `401`, unknown or revoked key → `401` (on any endpoint), wrong role →
`403`. Requests are rate-limited per key or per client IP (`429` + `Retry-After`); protected calls and
every refusal are written to the audit log. Details, key management and limits:
[`docs/SECURITY.md`](docs/SECURITY.md).

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/health` | Liveness + disclaimer |
| `GET /api/v1/dashboard/summary` | Home KPIs |
| `GET /api/v1/auctions` | Calendar; filters: `country`, `currency`, `instrument_type`, `status`, `date_from`, `date_to`, `min_tenor_days`, `max_tenor_days`, `include_synthetic` |
| `GET /api/v1/auctions/{id}` | Result + historical comparison vs. peers |
| `GET /api/v1/securities`, `/securities/{id}` | Instruments and their auction history |
| `GET /api/v1/countries`, `/countries/{iso3}` | Country reference + sources |
| `GET /api/v1/countries/{iso3}/yield-curve` | Latest auction yield per tenor (no fitting) |
| `GET /api/v1/sources` | Source registry, ordered by authority |
| `GET /api/v1/opportunities` | Opportunity Radar signals with passports; investor-criteria matching |
| `GET /api/v1/market/heat-grid` | Country × tenor grid: latest yield + demand vs own history |
| `GET /api/v1/countries/{iso3}/maturity-wall` | Tracked maturities per month, next 12 months |
| `GET /api/v1/accredited-dealers` | Institutions accredited to bid at auctions, from official lists (UMOA-Titres, BEAC, DMO Nigeria, Bank of Ghana, National Treasury South Africa, Morocco top 3); shares and ranks only where the authority publishes them; filter: `country` |
| `GET /api/v1/subscription-routes` | How buyers access each market (who, intermediary, account, minimums), with verbatim official quotes; filter: `country`. Covers CEMAC, WAEMU and Kenya (15 countries) |
| `GET /api/v1/data-quality` | **analyst/admin.** Stale/pending sources, missing fields, duplicates, synthetic counts |
| `GET /api/v1/admin/audit-log?limit=` | **admin.** Latest audit rows (key id, role, method, path, status, truncated IP, request id) |
