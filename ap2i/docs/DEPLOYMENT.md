# AP²I — Deployment

## 1. Docker Compose (single host)
```bash
cd ap2i
cp .env.example .env          # set POSTGRES_PASSWORD and AP2I_SECRET_KEY (>= 32 random chars)
docker compose up --build -d  # db (PostGIS), redis, api, worker, beat, web
docker compose exec api python -m app.cli create-admin you@your-org.org   # prompts for a password
docker compose exec api python -m app.cli rates                           # historical exchange rates
docker compose exec api python -m app.cli sync worldbank_projects worldbank_iati afdb_iati afd_iati
```
* API: http://localhost:8000 (OpenAPI at /docs) · Web: http://localhost:3000
* The `api` service runs `alembic upgrade head`, the reference seed and `activate-countries` at start.
* `beat` triggers `dispatch_due_syncs` every 5 minutes; enabled connectors run on their cron schedule
  (defaults: World Bank 02:00 UTC daily, IATI-based 02:30 UTC daily). Change schedules in Admin → Connectors.
* Put a TLS reverse proxy (nginx, Traefik, a cloud load balancer) in front of `web` and `api`; set
  `AP2I_CORS_ORIGINS` and `AP2I_PUBLIC_APP_URL` to the public URLs.

### Building behind a TLS-intercepting proxy or a registry rate limit
```bash
docker build --build-arg PYTHON_IMAGE=mirror.gcr.io/library/python:3.12-slim \
  --secret id=extra_ca,src=/path/to/ca-bundle.crt -f backend/Dockerfile -t ap2i-api .
```

## 2. Activating a second country (configuration only)
1. Set `AP2I_ACTIVE_COUNTRIES=["CMR","SEN"]` and restart `api`, `worker`, `beat`.
2. `docker compose exec api python -m app.cli activate-countries` (mirrors the setting into the DB and into
   connectors that follow active countries).
3. `docker compose exec api python -m app.cli rates` (adds the new currency's rates).
4. Run the connectors (`sync ...`) — the same code paths; no country-specific code.

## 3. Without Docker (development)
```bash
# PostgreSQL 16 + PostGIS, Redis
cd ap2i/backend && pip install -e ".[dev]"
export AP2I_DATABASE_URL=postgresql+psycopg://ap2i:ap2i@localhost:5432/ap2i
alembic upgrade head && python -m app.cli seed
uvicorn app.main:app --reload            # API
celery -A app.tasks.celery_app worker -l info
celery -A app.tasks.celery_app beat -l info
cd ../frontend && npm ci && AP2I_API_URL=http://127.0.0.1:8000/api/v1 npm run dev
```

## 4. Verification performed in the build environment (2026-10-22)
| Step | Result |
|---|---|
| `docker build` backend image (via `mirror.gcr.io`, Docker Hub returned HTTP 429) | Built |
| PostGIS 16-3.4 + Redis 7 containers | Started |
| API container: `alembic upgrade head`, seed, uvicorn, `/api/v1/health` (production mode, HSTS header present) | OK |
| Celery worker container: admin-triggered background sync of `worldbank_projects` | 159 real records retrieved and imported |
| Celery beat container: `dispatch_due_syncs` sent at the 5-minute tick; worker ran scheduled syncs (`trigger=scheduled`) | worldbank_iati 46/46, afd_iati 306/306; worldbank_projects re-run 159 retrieved, 0 imported (unchanged, incremental) |
| Full `docker compose up` (including the web image) | Not run end-to-end here (image pulls rate-limited) |

## 5. Operations
* Logs: `sync_runs` (per run: counts, errors, log), `audit_logs`, container logs.
* Failed runs create an admin notification and set `last_failure_at`/`last_error` on the connector.
* Health: `GET /api/v1/health` (public), `GET /api/v1/admin/system` (DB, Redis, PostGIS, running/failed runs).
* Backups and recovery: see [SECURITY.md](SECURITY.md#backups-and-recovery-procedure).
