# AP²I — Implementation roadmap and status

Legend: ✅ done and tested · 🟡 partial · ⬜ not started. Status date 2026-10-22.

| Phase | Scope | Status | Notes |
|---|---|---|---|
| 0 Repository audit | Inspect MVP, reuse, migration needs | ✅ | Repo branch holds another product (Cartouche); AP²I built in `ap2i/`. See MIGRATION_REPORT.md |
| 1 Core architecture | DB (57 tables, Alembic, PostGIS), auth (Argon2/JWT/MFA/RBAC), 54-country registry, project registry, admin API, frontend framework | ✅ | |
| 2 Real data ingestion | World Bank, AfDB, IATI, AFD connectors; provenance; validation; entity resolution | ✅ | AfDB/AFD via their IATI publications; direct portals blocked |
| 3 Financial intelligence | Agreements, commitments, disbursements, indicators, historical FX, annual portfolios + snapshots, dashboards | ✅ | Constant prices ⬜ |
| 4 Performance intelligence | Indicators, operational status model, 12 alert rules, thresholds, data quality | 🟡 | Implementation progress / operational status need document imports (no source publishes them) |
| 5 Project Rescue | Diagnosis, evidence-based plans, approvals, tracking, reports | ✅ | |
| 6 AI intelligence | Grounded assistant, injection safeguards, optional LLM narrative | 🟡 | Document extraction + RAG/semantic search ⬜ |
| 7 Commercial platform | Plans, subscriptions, feature gating, institutional workspaces, API keys, reports | 🟡 | Payment provider deliberately inactive |
| 8 Deployment | Docker, compose, CI, monitoring endpoints, backup procedure, security doc | 🟡 | CI not yet run on GitHub; no pen test; backups not automated |

## Next steps (proposed order)
1. Obtain an IATI Datastore key; run Tier-3 IATI connectors after deciding whether humanitarian activities are
   in scope; review the 3 pending co-financing candidates.
2. Cameroon national budget: obtain the Loi de finances / BIP annexes and execution reports; import with the
   budget template; link budget lines to projects.
3. Document pipeline: download World Bank / AfDB / AFD documents (ISR, completion reports), extract progress,
   ratings and operational status with human validation; then RAG over documents for the assistant.
4. Second country (e.g. Senegal or Côte d'Ivoire) by configuration; validate connectors' output.
5. Production hardening: TLS proxy, Redis rate limiter, secrets manager, automated backups, pen test, payment
   provider with compliance review.
