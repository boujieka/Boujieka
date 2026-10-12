# ADR 0001: technology stack and deviations from the proposed stack

Status: accepted for the MVP, 12 October 2026.

## Context

The development brief proposes:
* frontend: Next.js and TypeScript, Tailwind, shadcn/ui, Recharts, MapLibre;
* backend: FastAPI, PostgreSQL with PostGIS, SQLAlchemy and Alembic;
* infrastructure: Redis, object storage, managed authentication, Docker, CI/CD.

The repository previously held only the book and Excel model generators (Python). There was no web application code to reuse. The generator conventions in `docs/modelling-conventions.md` were carried over to the engine:
* quarterly or monthly time base;
* interest on opening balances;
* an explicit equity top-up instead of circularity;
* checks that must read OK.

## Decisions

| Area | Decision | Deviation | Reason |
|---|---|---|---|
| Frontend | Next.js (App Router), TypeScript, Tailwind, Recharts, MapLibre GL | shadcn/ui components may be hand-written in the same style if the shadcn registry is unreachable | The sandbox network blocks most hosts |
| Backend | FastAPI, SQLAlchemy 2, Alembic, Pydantic 2 | None | |
| Database | PostgreSQL 16 | **PostGIS not enabled yet.** Geometry is stored as GeoJSON (JSONB) with project latitude and longitude | PostGIS is not installed in the development environment. The MVP needs display and upload, not spatial queries. PostGIS is planned for Phase 2 (site screening queries), with a migration converting the GeoJSON columns |
| Authentication | Established libraries (bcrypt, PyJWT, PyOTP) in-house, behind one dependency module | Not a managed identity provider | No paid service may be created without approval. The `deps.py` boundary allows a switch to a managed provider (OIDC) later |
| Background jobs and cache | Not used yet | **No Redis in the MVP** | A full set of 19 runs (base plus 18 sensitivity cases) took about 0.1 s in testing, so synchronous calls are enough. Redis-backed rate limiting and job queues come with multi-instance deployment |
| Object storage | Local directory behind a single storage function | Not S3 or another object store yet | No paid cloud resource. The storage key scheme (`org_id/uuid.ext`) maps one to one onto an object store |
| Energy system modelling | No PyPSA | The engine takes deliverable energy from the design study | Hourly dispatch belongs to the engineering study. PyPSA integration is justified only for an hourly sizing module (roadmap) |
| Analytics libraries | NumPy only in the engine | GeoPandas, Rasterio and SciPy not used yet | Needed only when raster and vector screening arrives (Phase 2) |
| Excel export | Values export of a run | Not a live-formula workbook | A formula workbook generator (as for MODEL 2 in this repository) is a larger task and is on the roadmap |
| AI | Not implemented | Provider-agnostic Copilot with retrieval and citations is planned for Phase 4 | The financial engine had to be correct and tested first, as the brief requires |
| Payments | Not implemented | Plan field only | Requires a confirmed incorporation jurisdiction and merchant eligibility |

## Consequences

* The MVP runs on one PostgreSQL instance and one API process, without paid services.
* Moving to PostGIS, Redis, object storage and a managed identity provider is planned work behind existing boundaries, not a rewrite.
