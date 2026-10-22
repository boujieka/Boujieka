# AP²I — Africa Public Project Intelligence

**Every Project. Every Dollar. Every Impact.**

Independent, source-verified public-investment intelligence for Africa. First deployment: **Cameroon**.
Architecture: all **54** African UN member states, activated by configuration.

> AP²I shows only what official sources publish, with provenance. Coverage is limited to the connected sources
> and is **not** the complete national public-investment portfolio. Alerts are signals for verification, not
> findings of wrongdoing.

## What works today (verified 2026-10-22)
* **Real data**: 7 operational connectors — World Bank Projects API, World Bank IATI, AfDB IATI, AFD IATI,
  EIB IATI, EU INTPA IATI, IFAD IATI — 820 real source records for Cameroon → 483 master projects, with
  verbatim source records, field-level provenance and deterministic matching (no double counting).
* Annual portfolios 2011–2026 (counts, commitments, disbursements per currency + USD at year-specific
  World Bank / IMF annual rates), reproducible snapshots.
* 12 documented early-warning rules, Project Rescue (evidence-based plans with approval workflow), grounded
  Intelligence Assistant, reports (9 types × PDF/Excel/CSV), data-quality dashboard.
* Users, Argon2, JWT, TOTP MFA, 10 roles, tenant isolation, audit log, plans/feature gating.
* Celery worker + beat scheduling; Docker images; 67 automated tests + 7 live-source tests passing.

See [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md) for what is not done.

## Layout
```
ap2i/
  backend/        FastAPI · SQLAlchemy 2 · Alembic · PostgreSQL/PostGIS · Celery
    app/connectors/   World Bank, IATI family (AfDB, AFD, EIB, EU, IFAD, UN agencies…), uploads, FX
    app/ingestion/    pipeline (provenance, validation) and entity resolution
    app/finance/      FX, indicators, annual portfolios
    app/performance/  alerts, data quality
    app/rescue/       Project Rescue
    app/assistant/    Intelligence Assistant + prompt-injection safeguards
    app/reports/      PDF / Excel / CSV
    app/security/     auth, RBAC, tenant isolation, rate limiting, audit
    app/migration/    legacy MVP v0.1 → v2
    tests/            pytest (synthetic fixtures) + live tests (-m live)
  frontend/       Next.js · TypeScript · Tailwind · ECharts/Recharts · MapLibre GL (FR/EN)
  docs/           requirements, architecture, schema, sources, governance, security, tests, roadmap, guides
  data_templates/ official-data import templates
  legacy_mvp/     the AP²I MVP v0.1 files as supplied (reference for the migration)
  brand/          logo
```

## Quick start
```bash
cp .env.example .env   # set POSTGRES_PASSWORD and AP2I_SECRET_KEY
docker compose up --build -d
docker compose exec api python -m app.cli create-admin you@your-org.org
docker compose exec api python -m app.cli rates
docker compose exec api python -m app.cli sync worldbank_projects worldbank_iati afdb_iati afd_iati
```
Details: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). API reference: `/docs` (OpenAPI; exported to
[docs/openapi.json](docs/openapi.json)).

## Documentation
[Product requirements](docs/PRODUCT_REQUIREMENTS.md) · [Architecture](docs/ARCHITECTURE.md) ·
[Database schema](docs/DATABASE_SCHEMA.md) · [Data sources](docs/DATA_SOURCES.md) ·
[Connector status](docs/CONNECTOR_STATUS.md) · [Data governance](docs/DATA_GOVERNANCE.md) ·
[Security](docs/SECURITY.md) · [Test strategy](docs/TEST_STRATEGY.md) ·
[Roadmap](docs/IMPLEMENTATION_ROADMAP.md) · [Migration report](docs/MIGRATION_REPORT.md) ·
[Known limitations](docs/KNOWN_LIMITATIONS.md) · [Deployment](docs/DEPLOYMENT.md) ·
[Administrator guide](docs/ADMIN_GUIDE.md) · [Import templates](data_templates/README.md)

## Tests
```bash
cd backend && pytest            # PostgreSQL test DB (AP2I_TEST_DATABASE_URL), no network
cd backend && pytest -m live    # real sources
cd frontend && npm run typecheck && npm run lint && npm test && npm run build
```
