# Phase 1 report — database, core models, basic dashboard

## Files created

**Backend** (`backend/`)
- `pyproject.toml`, `Dockerfile`, `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako`,
  `alembic/versions/0001_phase_1_core_schema.py`
- `app/config.py`, `app/db.py`, `app/main.py`, `app/schemas.py`
- `app/models/`: `enums.py`, `base.py` (provenance mixin + constraints), `country.py`
  (Country, Issuer), `security.py`, `auction.py`, `source.py` (Source, SourceDocument),
  `market.py` (MarketObservation, Opportunity, SubscriptionRoute: tables only)
- `app/analytics/calculations.py`
- `app/api/`: `deps.py`, `serializers.py`, `auctions.py`, `countries.py`, `securities.py`, `overview.py`
- `app/seed/`: `reference.py`, `synthetic.py`, `load.py`
- `tests/`: `conftest.py`, `test_calculations.py`, `test_synthetic_and_models.py`, `test_api.py`

**Frontend** (`frontend/`, scaffolded with create-next-app 15, then replaced)
- `src/lib/`: `api.ts` (server-only client), `types.ts`, `format.ts`, `format.test.ts`, `utils.ts`
- `src/components/`: `ui/{card,badge,table}.tsx`, `provenance.tsx`, `auction-table.tsx`,
  `source-table.tsx`, `charts.tsx`, `kpi.tsx`, `nav.tsx`
- `src/app/`: `layout.tsx`, `page.tsx` (Home), `auctions/page.tsx` (Calendar),
  `auctions/[id]/page.tsx` (Auction result), `countries/page.tsx`, `countries/[iso3]/page.tsx`,
  `securities/[id]/page.tsx`, `admin/data-quality/page.tsx`, `globals.css`, `icon.svg`
- `Dockerfile`

**Root:** `docker-compose.yml`, `.env.example`, `.gitignore`, `docs/IMPLEMENTATION_PLAN.md`, this file.

## Files modified
- `README.md` (was a one-line placeholder)

## Architecture
- Every market-data table carries provenance. A CHECK constraint makes it impossible to store
  synthetic data unless it is labelled SYNTHETIC.
- Empty fields carry a reason (`not_disclosed` / `not_available` / `pending`). The API fills in
  `not_available` for any unexplained null.
- The API returns `official`, `calculated` and `provenance` as separate blocks. Calculated
  values state their formula (e.g. bid-to-cover = submitted / offered; some issuers define it
  against the allocated amount instead, so the definition is always shown).
- Rates are stored in percent, money as `NUMERIC(20,4)`, and computed as Decimal only.
  Day-count basis is a required argument and is never defaulted.
- Source registry ordered by authority (central bank → … → news). Source URLs are **null**
  until an operator confirms them; no URL was guessed.

## Tests performed
| Check | Result |
|---|---|
| Backend pytest on SQLite | 264 passed |
| Same suite on PostgreSQL 16 | 264 passed |
| `alembic upgrade` → `check` (no drift) → `downgrade base` → `upgrade` | clean |
| Seed loader run twice | 448 auctions, then 0 (idempotent) |
| Frontend vitest | 7 passed |
| `tsc --noEmit`, `eslint`, `next build` | clean |
| All pages served from the production build against the live API on Postgres; 404s for unknown country/auction | OK |
| Playwright screenshots, light, dark and 390px mobile; console errors; horizontal overflow | none |

**Independent validation of the financial calculations:** expected values come from hand-worked
textbook cases (e.g. a 90-day bill at a 5% discount rate on ACT/360 is priced at exactly 98.75; its
money-market yield is 5.06329114%) and from a separate exact-rational (`fractions.Fraction`)
implementation across 50 rate/tenor/basis combinations. Round trips hold to 1e-25. A test also
checks the synthetic bill prices against their yields using the independent formula.

## Known limitations
1. **No real market data.** All 448 auctions and 398 securities are synthetic. Yield levels are
   arbitrary anchors, not estimates of real markets.
2. **Country reference data is unverified.** It was compiled from general knowledge, not from a
   retrieved document. In particular, the debt-management entity names and the market-structure
   descriptions need checking. Gabon, Côte d'Ivoire and Senegal have the debt office left empty
   on purpose rather than guessed.
3. **No authentication, roles, rate limiting or audit log yet.** The API is read-only and has only
   basic security headers. Do not deploy beyond localhost before Phase 1b.
4. Yield conventions are not normalised. The yield curve mixes bills and bonds and says so
   (Phase 3). Reopened bonds are plotted at their original tenor, not their residual tenor.
5. The synthetic generator's output depends on its reference date. Re-seeding with a different
   date adds a second synthetic set instead of replacing the first.
6. `docker-compose.yml` and the Dockerfiles were **not** run in this environment. Only the native
   setup was tested.
7. The "Alerts" KPI currently counts cancelled and postponed auctions only. The "New
   opportunities" KPI shows *Not available* until Phase 4. The investor-eligibility filter
   waits on Phase 6 data.
8. Tables scroll horizontally inside their card on phones. The page itself does not overflow.

## Next recommended step
**Phase 1b + Phase 2 groundwork.** First, an operator confirms the official URL for each
registered source (start with BEAC, UMOA-Titres and Central Bank of Kenya). Then build:
(a) the auth / RBAC / audit-log / rate-limit baseline, and (b) a single end-to-end ingestion
path for one source. That path should fetch the document, store it by SHA-256, extract text,
write to a staging table, send it to human verification, and promote it to `auction` with full
provenance. Prove it on one market before adding the rest.
