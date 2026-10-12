# Roadmap, milestones and backlog

## Milestones

| Phase | Scope | Acceptance before moving on |
|---|---|---|
| 0 Architecture | Repository audit, ADR, schema, engine specification, test strategy | Documents in `docs/` |
| 1 MVP | Authentication, organisations and roles, projects, site selection, map, input forms, technology comparison, financial model, scenarios, dashboard, Excel export, teaser, EN/FR | Backend and engine test suites pass; the end-to-end browser test passes; the known limitations are documented |
| 2 Portfolio intelligence | Portfolios, Electrification Acceleration Score with mandatory gates, portfolio finance, readiness gates, pipeline dashboards, multi-project reports; PostGIS and data ingestion | Score explanation per project; a failed gate always overrides the score; tests |
| 3 Commercial platform | Subscriptions and entitlements, payment provider (after jurisdiction and eligibility checks), organisation administration, marketplace (information and introduction only), secure data rooms, institutional reporting | Legal review of marketplace terms; tenant isolation tests on data rooms |
| 4 Delivery and verification | Implementation monitoring, milestone workflows, meter and operator data integrations, verified access reporting, Copilot, Academy | Verification rules distinguish registered, installed, energised and active connections; no double counting tests |

## Next milestone (proposed): Phase 1 hardening, then Phase 2 start

1. Independent review of the engine specification and test cases by a project finance modeller.
2. Debt sizing on a target DSCR (sculpting) and receivable days (L2, L3).
3. Formula-based Excel export (L16).
4. PostGIS and a boundary dataset ingestion pipeline with licence checks (L11, L12).
5. Encryption of MFA secrets; Redis rate limiting; password reset (L13 to L15).
6. Electrification Acceleration Score (weights configurable and labelled as initial design assumptions; mandatory gates for land rights, permits, technical feasibility, E&S risk, regulatory restrictions and failed model checks).

## Backlog (prioritised)

| ID | Item | Phase |
|---|---|---|
| B1 | DSCR sculpting and a debt sizing solver | 1+ |
| B2 | Working capital: receivable and payable days | 1+ |
| B3 | Formula Excel export | 1+ |
| B4 | Three-page summary and detailed memorandum generators (DOCX and PDF) | 2 |
| B5 | Risk matrix, sensitivity report, bankability assessment, preparation and due diligence checklists | 2 |
| B6 | Portfolio entity and portfolio report | 2 |
| B7 | Acceleration Score | 2 |
| B8 | PostGIS, GeoPandas and Rasterio ingestion; site screening filters; screening report | 2 |
| B9 | Country rule library for grid arrival and tariffs (verified sources only) | 2 |
| B10 | Monte Carlo after independent review | 2+ |
| B11 | Plans and entitlements; payment abstraction | 3 |
| B12 | Marketplace and data rooms | 3 |
| B13 | Delivery: Gantt, budget against actual, disbursements, delay alerts | 4 |
| B14 | Verify: connection taxonomy and verification rules | 4 |
| B15 | Copilot: provider-agnostic LLM layer, retrieval over approved documents, schema-validated outputs, citations, human review | 4 |
| B16 | Academy: catalogue, enrolment, lessons, quizzes, certificates (no external accreditation claims) | 4 |
