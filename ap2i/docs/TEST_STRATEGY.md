# AP²I — Test strategy

## Layers
| Layer | What | How to run |
|---|---|---|
| Unit + integration (backend) | Parsers, pipeline, resolution, finance, portfolio, alerts, rescue, auth, RBAC, tenant isolation, API endpoints, reports, assistant, uploads, scheduling, migrations | `cd backend && pytest` (PostgreSQL test database, no network) |
| Live source tests | Real retrieval + persistence for each Tier-1 connector, real exchange rates, ISO code cross-checks | `cd backend && pytest -m live` (network) |
| Migration tests | Alembic upgrade on an empty DB; autogenerate diff must be empty; downgrade; legacy MVP migration on a synthetic MVP database | part of `pytest` (`AP2I_MIGRATION_TEST_DATABASE_URL`) |
| Frontend | Type check, lint, unit tests (i18n completeness, formatting), production build | `cd frontend && npm run typecheck && npm run lint && npm test && npm run build` |
| End-to-end smoke | Production build + Playwright against the running API; screenshots | see frontend README |
| Container | Image build; container start; migrations; seed; Celery worker real sync; beat dispatch | DEPLOYMENT.md §Verification |

## Fixtures
`backend/tests/fixtures/` contains **explicitly synthetic** World Bank JSON and IATI XML (titles start with
"SYNTHETIC", identifiers `P9xxxxx` / `TEST-…`). They reproduce the real formats, including the edge cases that
matter: Additional Financing parent links, AFD parent/child hierarchy, WB API ↔ WB IATI equivalence,
multi-country activities, a dropped project with `totalamt=0`, a description containing a prompt-injection
string. Network calls are served by `httpx.MockTransport`. The test database is truncated between tests.

## Mapping to Master-prompt §33
| Requirement | Tests |
|---|---|
| Authentication | `test_auth.py` (register, verify, login, lockout, MFA, reset, revocation, internal domains) |
| Authorization | `test_authz_tenant.py::test_role_based_authorization`, feature gating |
| Country filtering / activation | `test_reference.py`, `test_api.py::test_countries_and_map_show_coverage_separately` |
| Project creation / updates | `test_pipeline.py` (creation, new versions, idempotency), uploads |
| Financial calculations | `test_finance.py` |
| Annual portfolio calculations | `test_finance.py::test_annual_portfolio_counts_projects_once_and_dates_flows`, snapshots |
| Source ingestion | `test_connectors.py`, `test_pipeline.py`, `test_live_sources.py` |
| Duplicate detection / project matching | `test_resolution.py`, `test_api.py::test_admin_review_merge_and_reverse` |
| Data validation | `test_pipeline.py`, uploads |
| AI response grounding | `test_workflows.py::test_llm_narrative_grounding`, `::test_assistant_answers_from_database_only` |
| Project Rescue rules | `test_alerts_rescue.py`, `test_workflows.py::test_rescue_api_flow` |
| Tenant isolation | `test_authz_tenant.py::test_tenant_isolation`, private plans |
| Report generation | `test_workflows.py::test_reports_all_types_and_formats` (9 types × 3 formats) |
| API endpoints | `test_api.py` |

## Results (2026-10-22, this environment)
* `pytest`: 67 passed (backend, PostgreSQL 16 + PostGIS 3).
* `pytest -m live`: 7 passed (World Bank, World Bank IATI, AfDB IATI, AFD IATI, rates, ISO codes, Natural Earth codes).
* Frontend: see the frontend section of the final report / `frontend/README.md`.
