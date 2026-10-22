# AP²I — Migration report: Cameroon MVP v0.1 → v2.0

## 0. What was audited
* **Repository on the working branch**: it contains a *different* product, "Cartouche · African Bond
  Intelligence" (sovereign bond auctions, WAEMU data). It is **not** the AP²I MVP and was left untouched.
  AP²I v2 lives in the self-contained `ap2i/` directory. Nothing from Cartouche was modified or deleted.
* **AP²I MVP v0.1**: the files supplied with the request (copied verbatim to `ap2i/legacy_mvp/`): `app.py`
  (single-file FastAPI + SQLAlchemy), `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `.env.example`
  (as `env.example`), `README.md`, `projects_template.csv`. The MVP's `static/index.html` (served at `/`) was
  **not supplied**; its UI could not be audited or migrated.

## 1. MVP inventory
| Item | MVP v0.1 |
|---|---|
| Endpoints | `GET /`, `GET/POST /api/countries`, `GET/POST /api/projects`, `GET /api/projects/{id}`, `POST /api/projects/{id}/financings`, `POST /api/financings/{id}/disbursements`, `POST /api/projects/{id}/actions`, `GET /api/dashboard`, `GET /api/annual`, `GET /api/projects/{id}/diagnostic`, `GET /api/export.csv`, `POST /api/import.csv` |
| Models | countries, projects, financings, disbursements (year + amount), amendments, actions |
| Auth | single shared admin key header for writes |
| Calculations | counts by sector/status; annual new/active counts from start/end years; no cross-currency sums |
| Project Rescue | 4 rules: missing physical progress; end year passed and not closed; revised cost > 1.2 × initial; completed without operational status |
| CSV import | all-or-nothing, source_url mandatory |
| Tests | none supplied |
| Docker | python:3.12-slim + postgres:16 compose with required secrets |

## 2. Retained (behaviour kept, re-implemented)
* "No invented data": the MVP shipped no data; v2 also ships none (projects only come from connectors/uploads).
* Mandatory source on import (now per row: `source_url` + `reporting_date`) and all-or-nothing validation.
* Never adding amounts across currencies.
* The four diagnostic rules, now part of the early-warning engine: missing progress → `MISSING_PROGRESS_REPORT`
  (generalised), end date passed → `CLOSING_DATE_PASSED`, cost revision > 20 % → `COST_REVISION` (threshold
  configurable, default 1.20), completed without operational status → `OPERATIONAL_STATUS_UNVERIFIED`.
* CSV export of projects; dashboard by sector and status; annual counts (now with documented counting rules).
* Docker with secrets from `.env` and required variables.

## 3. Modified
| MVP | v2 |
|---|---|
| Free-text sector/status/funder | Controlled vocabularies + original wording kept as observations |
| `start_year`/`end_year` | Real dates from sources; legacy years kept as observations, never turned into dates |
| One `source_url` per project | Full provenance: verbatim source records, hashes, observations per field |
| Admin key | Users, Argon2, JWT, MFA, RBAC (10 roles), tenant isolation, audit log |
| Annual counts from years | Methodology v1.0 (approval/active/completed rules, dated transactions, USD at annual rates, snapshots) |
| `actions` | Project Rescue plans/actions with evidence, approval workflow and tracking |
| Project-level `amendments` | Kept as `legacy_amendment` observations (no contract existed to attach them to) |
| `create_all` at import time | Alembic migrations |

## 4. Removed
* `X-Admin-Key` authentication (replaced, not kept in parallel — a shared key cannot provide audit or tenancy).
* `POST /api/countries` (the 54 countries are reference data; activation is configuration).
* Implicit SQLite default in production (SQLite is not supported by v2; PostgreSQL + PostGIS only).

## 5. New
Connectors (World Bank, IATI family incl. AfDB/AFD/EIB/EU/IFAD), entity resolution and merge review, financial
engine with historical FX, annual portfolios with snapshots, 12 alert rules, Project Rescue workflow,
Intelligence Assistant, reports (9 types × PDF/Excel/CSV), data-quality framework, subscriptions/plans, admin
panel API, Celery scheduling, Next.js bilingual frontend with Africa map.

## 6. Data migration
`python -m app.cli migrate-mvp <MVP database URL>` (SQLite or PostgreSQL). Implementation:
`backend/app/migration/mvp.py`; test: `tests/test_migration.py::test_mvp_migration_preserves_everything`.
* Every legacy row is preserved verbatim as a source record of connector `legacy_mvp` (nothing discarded).
* projects → master projects (new AP²I ids, legacy id registered as identifier); unknown sectors/statuses are
  listed in the report's `unmapped` section and kept as observations; rows without `source_url` → `needs_review`.
* financings → agreements (+ commitment events); free-text funders mapped to registry partners when
  recognised, otherwise a `LEGACY:` partner flagged for review.
* disbursements (year only) → flows with `period_year`, no invented day; still counted in annual portfolios.
* amendments → observations (see §3). actions → a recovery plan per project with user-origin actions.
* Idempotent: re-running creates nothing new.
* The report printed by the command lists rows read, created, skipped and unmapped, plus warnings.

## 7. Migration risks
1. **MVP production data was not available** to this build; the migration was tested on a synthetic MVP
   database built with the MVP's exact schema. Run it first on a copy and review `unmapped`.
2. Free-text funder names may map to the wrong partner if ambiguous (e.g. "BID" is read as IsDB): review the
   partner list after migration.
3. Legacy projects may duplicate projects now imported from donor sources: they get match candidates only if
   created after the connector runs — run `generate_candidates` or review manually.
4. The MVP UI (`static/index.html`) was not supplied and is not migrated.
