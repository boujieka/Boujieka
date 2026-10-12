# Deployment

**Status:** the Docker files have **not** been built or run yet. The development environment had a Docker client but no daemon. `docker compose config` validates. Build and run them once in a Docker-enabled environment before relying on them.

## Single host with Docker Compose

```bash
cd apps/access360
export POSTGRES_PASSWORD='<strong value>' APP_DB_PASSWORD='<strong value>' A360_JWT_SECRET="$(openssl rand -base64 48)"
docker compose up -d --build        # db → migrate (alembic upgrade head) → api :8000 → web :3000
docker compose run --rm api python -m app.seed demo           # optional demo workspace (prints a password once)
A360_ADMIN_EMAIL=you@example.com A360_ADMIN_PASSWORD='<strong value>' docker compose run --rm -e A360_ADMIN_EMAIL -e A360_ADMIN_PASSWORD api python -m app.seed superadmin
```

Put a TLS-terminating reverse proxy (for example Caddy or nginx) in front of `web`. Keep `A360_COOKIE_SECURE=true`.

## Environment variables (backend)

| Variable | Purpose | Default |
|---|---|---|
| A360_ENV | development, test or production. Production refuses to start without a JWT secret | development |
| A360_DATABASE_URL | App role connection (non-owner, so RLS applies) | local dev URL |
| A360_DATABASE_OWNER_URL | Owner connection, used only by migrations | local dev URL |
| A360_APP_DB_ROLE | Name of the app role granted DML in migrations | access360_app |
| A360_JWT_SECRET | Session signing key. **Required in production** | random per process in development |
| A360_JWT_MINUTES | Session length | 60 |
| A360_COOKIE_SECURE | Secure cookies (HTTPS) | false |
| A360_CORS_ORIGINS | Comma-separated origins (only needed if the browser calls the API directly) | http://localhost:3000 |
| A360_STORAGE_DIR | Folder for generated documents | storage |
| A360_MAX_UPLOAD_MB | Dataset upload limit | 20 |
| A360_LOGIN_RATE_PER_MINUTE | Login attempts per IP and email per minute | 10 |

## Production checklist (not yet done)

* Managed PostgreSQL with backups and point-in-time recovery; restore tested.
* Encryption at rest on the database and the storage volume. MFA secrets are not yet encrypted in the application (limitation L13).
* Secrets in a secret manager, not in `.env` files.
* Object storage for documents (limitation L19).
* Error monitoring: the API logs JSON lines with a request ID. Connect a monitoring service after choosing one.
* No production deployment has been made. None will be made without explicit approval.
