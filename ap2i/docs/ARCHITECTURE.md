# AP²I — Architecture

## 1. Principles
* **Modular monolith**: one FastAPI application with clear domain packages; no microservices.
* **Source first**: connectors only fetch and normalize; one shared pipeline persists, keeps provenance,
  validates, resolves entities and logs. Analytics read only from the database.
* **Country by configuration**: `AP2I_ACTIVE_COUNTRIES` (e.g. `["CMR"]`). No country-specific code path;
  the 54 countries share the same tables, connectors (country = parameter) and UI components.
* **No invention**: missing stays `NULL` and is reported; calculations declare formula, inputs and gaps.

## 2. Components

```
                 ┌──────────── Official sources ────────────┐
                 │ World Bank API · IATI (WB, AfDB, AFD, EIB, │
                 │ EU, IFAD…) · WDI / IMF rates · uploads     │
                 └───────────────┬────────────────────────────┘
                                 │ httpx (retry, backoff, rate limit)
┌───────────── backend (Python 3.12, FastAPI, SQLAlchemy 2, Alembic) ─────────────┐
│ connectors/   plugin per source → RawRecord → NormalizedRecord                  │
│ ingestion/    pipeline (store raw + SHA-256, validate, resolve, observe, log)   │
│               resolution (deterministic ids, parent links, candidates, merges)  │
│ finance/      fx (annual historical rates), indicators, annual portfolios       │
│ performance/  early-warning rules, data-quality scoring                         │
│ rescue/       diagnosis, evidence-based action plans, approvals, tracking       │
│ assistant/    query parsing, retrieval, structured answers, optional LLM,       │
│               grounding check, prompt-injection guards                          │
│ reports/      PDF (ReportLab), Excel (openpyxl), CSV                            │
│ security/     Argon2, JWT, TOTP MFA, RBAC, tenant filter, rate limit, audit     │
│ commerce/     plans, subscriptions, payment-provider abstraction (inactive)     │
│ tasks/        Celery worker + beat; cron dispatch; advisory locks               │
│ migration/    legacy MVP v0.1 → v2                                              │
│ api/          REST /api/v1 (OpenAPI at /docs)                                   │
└──────────┬──────────────────────────────┬────────────────────────────────────────┘
           │                              │
   PostgreSQL 16 + PostGIS          Redis (Celery broker)
           │
┌──────────┴──────── frontend (Next.js, React, TypeScript, Tailwind, ECharts/Recharts, MapLibre) ─┐
│ Server components fetch the API server-side; the browser talks only to Next.js route handlers.   │
│ Session = httpOnly SameSite=Strict cookie holding the API token; Origin check on mutations.      │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 3. Ingestion flow
1. `run_sync(connector)` creates a `sync_runs` row.
2. `fetch()` yields raw records → stored in `source_records` with SHA-256, URL, source update date,
   retrieval time. Same hash = unchanged → skipped (incremental). New hash = new version; older versions kept
   (`is_latest=false`).
3. `normalize()` maps to AP²I vocabulary (sector, status, instrument, dates, amounts in original currency).
4. Validation rules → `data_validation` (errors send the record to the review queue).
5. Resolution: identifier index (`project_identifiers`) → same project; official parent link → financing of
   the parent project; else a new master project with a minted `AP2I-{ISO3}-{SECTOR}-{n}` identifier.
6. Fields: the primary source sets them, other sources fill gaps; each value → `source_observations`.
7. Agreements/flows: one agreement per partner + source id; commitments carry `is_counted` so that two sources
   reporting the same commitment are never added (transaction-level IATI data outranks API aggregates).
8. After the run: probabilistic match candidates (never auto-merged), then post-sync jobs: alerts,
   data-quality assessment, annual portfolio snapshots.

## 4. Key design decisions
| Decision | Reason |
|---|---|
| AfDB and AFD via their own IATI publications | Direct portals unreachable / no documented API; IATI is the publishers' official open-data channel. |
| World Bank Projects API as primary WB source, WB IATI as transaction detail | API covers 159 projects (IATI only 46) and publishes cumulative disbursement; IATI adds dated flows. |
| Cumulative disbursement kept separate from flows | Avoids inventing annual splits; annual portfolios use dated transactions only. |
| Annual-average rates of the transaction year | Standard practice for flows; avoids today's rate for history; missing rate → no conversion. |
| `is_counted` on commitments/flows | Explicit, auditable anti-double-counting instead of silent deletion. |
| Snapshots with input fingerprint | Reproducible annual reports; corrections create new snapshots, old ones kept. |
| Rules-first Project Rescue and assistant | Truthful without an LLM; AI only phrases facts and must pass a numeric grounding check. |

## 5. Deployment topology
`docker-compose.yml`: `db` (postgis/postgis:16-3.4), `redis`, `api` (migrations + seed + uvicorn), `worker`
(Celery), `beat` (Celery beat → `dispatch_due_syncs` every 5 min), `web` (Next.js standalone).
See [DEPLOYMENT.md](DEPLOYMENT.md).
