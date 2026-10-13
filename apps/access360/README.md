# ACCESS360 AFRICA

Electrification investment, finance and delivery intelligence platform (MVP 0.1.0, development).

ACCESS360 AFRICA is an independent commercial product. No government, development finance institution or development partner owns, sponsors or partners with it.

## What works now (Phase 1 MVP)

* Accounts, organisations, roles and MFA.
* Tenant isolation at the API and in PostgreSQL (row-level security).
* Projects and milestones.
* **ACCESS FINANCE**, a deterministic quarterly mini grid project finance engine:
  * three statements, DSCR, LLCR, IRRs, LCOE, viability gap;
  * subsidies, RBF and grid arrival;
  * 18 sensitivity cases, a tornado chart and a minimum subsidy solver;
  * integrity checks with fault injection tests, and a status that is never "Validated" without a named review.
* **ACCESS OPTIMIZER:** a screening comparison of options A to G, with feasibility gates, weights, a Pareto flag and an explanation.
* **ACCESS MAP:** a dataset registry with mandatory metadata, and GeoJSON and CSV upload.
* Excel export of runs, and the one-page investment teaser (PDF).
* A demo workspace with clearly labelled synthetic data.
* A Next.js frontend in English and French (see `frontend/README.md`).

Planned (Phases 2 to 4): portfolios and the acceleration score, the marketplace and data rooms, subscriptions and payments, delivery, verification, Academy and Copilot. See `docs/roadmap-and-backlog.md` and `docs/known-limitations.md`.

## Quick start (development)

Requirements: Python 3.11, PostgreSQL 16, Node 20 or later.

```bash
# 1. database (once)
createdb -h 127.0.0.1 -p 5433 -U postgres access360
createdb -h 127.0.0.1 -p 5433 -U postgres access360_test
psql -h 127.0.0.1 -p 5433 -U postgres -c "CREATE ROLE access360_app LOGIN PASSWORD 'app';"

# 2. backend
cd apps/access360/backend
python3.11 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export A360_DATABASE_URL=postgresql+psycopg://access360_app:app@127.0.0.1:5433/access360
export A360_DATABASE_OWNER_URL=postgresql+psycopg://postgres@127.0.0.1:5433/access360
export A360_JWT_SECRET=dev-secret-change-me-0123456789
alembic upgrade head
A360_DEMO_PASSWORD='Demo-password-2027' python -m app.seed demo
python -m app.ingest_public                  # bundled public reference data (see docs/public-data-manifest.md)
uvicorn app.main:app --port 8000            # API docs at http://127.0.0.1:8000/docs

# 3. tests
python -m pytest                             # engine tests need nothing; API tests need the access360_test database

# 4. frontend: see frontend/README.md
```

Demo login: `demo@access360.example`, with the password set in `A360_DEMO_PASSWORD`.

## Documentation

| File | Content |
|---|---|
| docs/architecture.md | Components, security, data model |
| docs/adr/0001-stack-and-deviations.md | Stack decisions and deviations |
| docs/financial-engine-spec.md | Every formula of the finance engine |
| docs/geospatial-data-spec.md | Dataset metadata and upload rules |
| docs/openapi.json | API contract (generated) |
| docs/test-strategy.md | What the tests prove |
| docs/deployment.md | Docker Compose and environment variables |
| docs/user-guide.md, docs/admin-guide.md | Guides |
| docs/known-limitations.md, docs/risk-register.md, docs/roadmap-and-backlog.md | Limits, risks, plan |
| PROGRESS.md, CHANGELOG.md | Status and history |

The finance engine follows the method of Book 1 of the Africa Energy Finance collection (`output/22_BOOK1_MINI_GRIDS_STRUCTURE.md`): the site and the portfolio as units of analysis, operating sustainability, the viability gap and the grid arrival question. No figure in that document is used as a benchmark.
