# AP²I — Product requirements (v2.0)

**AP²I — Africa Public Project Intelligence.** *Every Project. Every Dollar. Every Impact.*
Independent African public-investment intelligence SaaS. Initial market: Cameroon. Architecture: all 54
African UN member states. Historical coverage target: 2011–2026.

## Problem
Public investment information in Africa is scattered across donor databases, national budget documents and
reports, published in different currencies, formats and languages, with no shared identifiers. Decision makers
cannot see where money goes, how projects perform, or which ones need rescue, with traceable evidence.

## Users
Governments (analysts, administrators), development finance institutions, bilateral donors, multilateral
banks, infrastructure investors, consulting firms, researchers, civil society, journalists, citizens.

## Pillars and capabilities
1. **Investment Intelligence** — master project registry; automated donor ingestion with provenance; entity
   resolution; financing agreements, commitments, disbursements; annual portfolios 2011–2026; Africa map;
   country, sector, donor and financing dashboards; Data Explorer; exports.
2. **Performance Intelligence** — transparent indicators (disbursement rate, elapsed time, slippage, cost
   revision, financing gap, contract amendments, physical–financial gap) with formula, inputs and gaps;
   configurable early-warning rules (4 levels); data-quality framework; sector indicator catalogue.
3. **Project Rescue** — evidence-based diagnosis, corrective action plans, approval workflow (approve / reject /
   modify), assignment, progress tracking, recovery dashboard and reports.
Cross-cutting: Intelligence Assistant (grounded, cited answers), reports (PDF/Excel/CSV), bilingual FR/EN UI,
RBAC + tenant isolation, subscriptions (Public, Professional, Institutional, Enterprise), administration.

## Non-negotiable data principles
See [DATA_GOVERNANCE.md](DATA_GOVERNANCE.md): never invent; never replace missing with zero; separate
reported / verified / calculated / estimated / AI / missing; preserve original currency, source, dates and
verification status; no synthetic data in production; coverage is never presented as complete.

## Plans (prices are configuration; currently "on request")
| Plan | Features |
|---|---|
| Public | basic search, country summaries, public dashboards, project pages |
| Professional | + advanced analytics, field-level provenance, custom filters, full exports, saved searches |
| Institutional | + private portfolios, Project Rescue, team collaboration, advanced reports, institutional imports |
| Enterprise | + API keys, custom integrations, dedicated workspace |
Online payment is disabled until a provider is implemented and compliance-reviewed (subscription requests are
recorded and fulfilled by an administrator).

## MVP acceptance criteria (Master prompt §34) — status at 2026-10-22
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Application starts | Met | API in Docker + local; frontend (see report) |
| 2 | Register and log in | Met | `test_auth.py` |
| 3 | Cameroon active country | Met | `AP2I_ACTIVE_COUNTRIES=["CMR"]`, `test_reference.py` |
| 4 | 54 countries in reference DB | Met | `test_reference.py`, live ISO cross-check |
| 5 | ≥1 official connector retrieves real Cameroon records | Met | 7 connectors operational (DATA_SOURCES.md) |
| 6 | Records stored with provenance | Met | `source_records`, `source_observations`, tests |
| 7 | Projects in the registry | Met | 483 master projects from 820 real source records |
| 8 | Project details | Met | `GET /projects/{ref}` + UI |
| 9 | Financing linked to projects | Met | agreements/commitments/flows |
| 10 | Annual portfolios from real records | Met | `/countries/CMR/portfolio`, snapshots |
| 11 | Dashboards use database queries | Met | all dashboard endpoints |
| 12 | Data gaps identified | Met | data-quality dashboard, `missing_inputs` |
| 13 | Alerts from documented rules | Met | 12 rules, `test_alerts_rescue.py` |
| 14 | Evidence-based Project Rescue | Met | `test_alerts_rescue.py`, API flow test |
| 15 | Export project information | Met | CSV export, reports |
| 16 | Admins review imported records | Met | review queue, matches, merges |
| 17 | Scheduled synchronization works | Met | dispatch test + Celery beat/worker in Docker (DEPLOYMENT.md) |
| 18 | Failed sync jobs logged | Met | `test_pipeline.py::test_failed_sync_is_logged` |
| 19 | Automated tests pass | Met | 67 + 7 live |
| 20 | Deployable with Docker | Partly | API/worker/beat images built and run; full `docker compose up` not run end-to-end here (Docker Hub rate limit, see DEPLOYMENT.md) |
| 21 | No synthetic financial data in production dashboards | Met | no seed data; DB CHECK; synthetic only in test fixtures |
| 22 | Every displayed financial observation traceable | Met | source record ids on every flow/agreement |
| 23 | Duplicate financing not counted twice | Met | `is_counted`, parent links, tests |
| 24 | Second country by configuration | Met | `test_second_country_activated_by_configuration_only`; connectors take the country as a parameter |
