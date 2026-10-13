# Development progress

Updated 12 October 2026.

| Step (brief section 21) | State | Evidence |
|---|---|---|
| 1. Architecture and plan | Done | docs/architecture.md, docs/adr/0001-stack-and-deviations.md, docs/roadmap-and-backlog.md, docs/risk-register.md |
| 2. Repository structure, schema, foundation | Done | backend/, frontend/, Alembic migration 0001 with row level security |
| 3. Authentication and project management | Done | Registration, login, MFA, roles, CSRF header, projects, milestones; API tests |
| 4. Financial engine with deterministic tests | Done; reviewed once (AI review, 21 findings, fixed or documented) | 78 backend tests incl. mutation tests; docs/financial-engine-spec.md; docs/reviews/ |
| 5. Dashboard and financial input interface | Done | frontend /app, /app/projects/[id] (Inputs, Results); screenshots |
| 6. Technology comparison and geospatial view | Done (screening level; no bundled geodata) | /app/optimizer, /app/explore |
| 7. Excel export and one page teaser | Done (Excel holds values, not formulas) | API tests and the e2e test download the teaser |
| 8. Tests and real results | Done | Backend: 78 passed. Frontend: tsc, lint and build pass; Playwright e2e 1 passed |
| 9. Gaps and next milestone | Done | docs/known-limitations.md (26 items), docs/roadmap-and-backlog.md |

## Not done (and not claimed)

* No production deployment. The Docker images have not been built here (no Docker daemon).
* No human expert review of the engine.
* No Excel test of the export.
* Phases 2 to 4 modules: portfolio score, marketplace, payments, delivery, verify, academy, copilot.

## Milestone 2 (13 October 2026)

| Item | State | Evidence |
|---|---|---|
| Engine: working capital, sculpting, DSRA draw | Done | tests/engine (test_working_capital..., test_sculpted..., test_dsra_is_drawn...) |
| Live formula Excel export | Done | tests/engine/test_formula_xlsx.py: 4 cases recalculated in LibreOffice, 37 rows and metrics equal to the engine |
| Public reference data | Done | docs/public-data-manifest.md; tests/api/test_public_data.py |
| PostGIS context and screening | Done | tests/api/test_spatial.py |
| Security hardening | Done | tests/api/test_security.py |
| Score, gates, portfolios (API and interface) | Done | tests/api/test_portfolio.py; e2e/portfolio.spec.ts |
| Three page summary | Done | API workflow test (3 pages) |
| Test results | 120 backend tests passed; frontend tsc and lint clean; Playwright 2 passed (screenshots spec skipped by default) | rerun by the lead on 13 October 2026 |

Not done: test in Microsoft Excel; the detailed memorandum and the other investment documents; raster layers; marketplace, payments, delivery, verify, academy, copilot.
