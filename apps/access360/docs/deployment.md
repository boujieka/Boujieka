# Deployment

**Status:** the Docker files have **not** been built or run yet. The development environment had a Docker client but no daemon. `docker compose config` validates. Build and run them once in a Docker-enabled environment before relying on them.

## Single host with Docker Compose

```bash
cd apps/access360
export POSTGRES_PASSWORD='<strong value>' APP_DB_PASSWORD='<strong value>' A360_JWT_SECRET="$(openssl rand -base64 48)"
export A360_DATA_KEY="$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"
docker compose up -d --build        # db → migrate (alembic upgrade head) → api :8000 → web :3000
docker compose run --rm api python -m app.seed demo           # optional demo workspace (prints a password once)
A360_ADMIN_EMAIL=you@example.com A360_ADMIN_PASSWORD='<strong value>' docker compose run --rm -e A360_ADMIN_EMAIL -e A360_ADMIN_PASSWORD api python -m app.seed superadmin
```

Put a TLS-terminating reverse proxy (for example Caddy or nginx) in front of `web`. Keep `A360_COOKIE_SECURE=true`.

## Environment variables (backend)

| Variable | Purpose | Default |
|---|---|---|
| A360_ENV | development, test or production. Production refuses to start unless A360_DATABASE_URL, A360_JWT_SECRET and A360_DATA_KEY are set (one error listing every missing variable) | development |
| A360_DATABASE_URL | App role connection (non-owner, so RLS applies). **Required in production** | local dev URL |
| A360_DATABASE_OWNER_URL | Owner connection, used only by migrations | local dev URL |
| A360_APP_DB_ROLE | Name of the app role granted DML in migrations | access360_app |
| A360_JWT_SECRET | Session signing key. **Required in production** | random per process in development |
| A360_JWT_MINUTES | Session length | 60 |
| A360_COOKIE_SECURE | Secure cookies (HTTPS) | false |
| A360_CORS_ORIGINS | Comma-separated origins (only needed if the browser calls the API directly) | http://localhost:3000 |
| A360_TRUSTED_PROXY_HOPS | Number of proxies in front of the API that append to `X-Forwarded-For`. The client address used for per-IP rate limits is the N-th entry from the right. 0 uses the TCP peer address | 0 |
| A360_STORAGE_DIR | Folder for generated documents | storage |
| A360_MAX_UPLOAD_MB | Dataset upload limit | 20 |
| A360_LOGIN_RATE_PER_MINUTE | Login attempts per IP and email per minute | 10 |
| A360_REGISTER_RATE_PER_MINUTE | Registrations per IP per minute | 5 |
| A360_MFA_RATE_PER_MINUTE | MFA setup verification attempts per user per minute | 10 |
| A360_PASSWORD_RATE_PER_MINUTE | Password forgot (per IP and per email), reset (per IP) and change (per user) requests per minute | 5 |
| A360_REDIS_URL | Redis for shared rate limits and "log out everywhere" (for example `redis://redis:6379/0`). **Recommended in production**, required with more than one API instance | unset (in memory, per process) |
| A360_PUBLIC_BASE_URL | Public URL of the web app, used in the password reset link | http://localhost:3000 |
| A360_RESET_TOKEN_MINUTES | Validity of a password reset link | 30 |
| A360_EMAIL_BACKEND | `console` (logs the e-mail, including the reset link: development only), `smtp`, or `memory` (tests) | console; smtp in production |
| A360_SMTP_HOST / A360_SMTP_PORT | SMTP server for the `smtp` backend. **Required in production** for password reset | unset / 587 |
| A360_SMTP_USER / A360_SMTP_PASSWORD | SMTP credentials (secret) | unset |
| A360_SMTP_FROM | Sender address, on a domain the operator controls. **Required with smtp** | unset |
| A360_SMTP_STARTTLS / A360_SMTP_SSL | STARTTLS on the plain port, or implicit TLS (port 465) | true / false |
| A360_DATA_KEY | Fernet key for field encryption (`python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`). Encrypts MFA secrets at rest (limitation L13, resolved). **Required in production**. Keep it in the secret manager; losing it makes stored MFA secrets unreadable | unset |
| A360_DATA_KEYS_OLD | Comma-separated previous data keys still accepted for decryption during a rotation | unset |

## Frontend on Netlify, backend elsewhere

Netlify hosts only the Next.js frontend (`frontend/netlify.toml`). The browser calls same-origin `/api/*`; the Next.js rewrite in `frontend/next.config.ts` forwards it server side to `BACKEND_URL`. The session cookie is set without a `Domain` attribute and with `SameSite=Lax`, so it stays first party on the Netlify domain. The FastAPI API and the database must run elsewhere. **None of this has been deployed or tested on Netlify or on any container host yet.**

### Netlify environment variables

| Variable | Scopes | Notes |
|---|---|---|
| BACKEND_URL | Builds and Functions | Public HTTPS base URL of the API, without a trailing slash and without `/api` (for example `https://api.example.org`). `next.config.ts` reads it when the rewrites are built, so **trigger a new deploy after changing it**; changing the variable alone does not update the running site |
| NEXT_PUBLIC_MAP_STYLE_URL | Builds | Optional map style URL. `NEXT_PUBLIC_*` values are inlined at build time, so a change also needs a redeploy |

Use the frontend's own README for anything else the build needs. Check Netlify's current documentation for how scopes and redeploys behave; the notes above follow from how this code reads the variables, not from a check of Netlify's documentation.

### Backend container

Build `backend/Dockerfile`. The image starts `uvicorn` on `$PORT` (default 8000) and needs only environment variables:

| Variable | Value behind Netlify |
|---|---|
| A360_ENV | `production` |
| A360_DATABASE_URL | `postgresql+psycopg://access360_app:<password>@<host>:5432/<db>` (the non-owner app role; add `?sslmode=require` if the provider requires TLS) |
| A360_DATABASE_OWNER_URL | Owner role URL. Only the migration step needs it; do not give it to the running API |
| A360_JWT_SECRET | `openssl rand -base64 48` |
| A360_DATA_KEY | Fernet key, see the table above |
| A360_COOKIE_SECURE | `true` (the API logs a warning in production when it is false) |
| A360_PUBLIC_BASE_URL | The Netlify site URL (used in password reset links) |
| A360_TRUSTED_PROXY_HOPS | See "Client address" below |
| A360_SMTP_HOST, A360_SMTP_PORT, A360_SMTP_USER, A360_SMTP_PASSWORD, A360_SMTP_FROM | Needed for password reset e-mail |
| A360_REDIS_URL | Optional. Without it rate limits and "log out everywhere" are in memory per process, which is acceptable only with exactly one API instance. Redis is imported only when this is set |
| A360_STORAGE_DIR | Generated documents are written to local disk (limitation L19). Point it at a persistent volume if the host offers one; otherwise documents are lost when the container is replaced |

`A360_CORS_ORIGINS` is not needed: the browser never calls the API directly. The API has no host allow-list. The CSRF check (`X-Requested-With: access360` on cookie-authenticated writes) passes through the rewrite because request headers are forwarded.

If a required variable is missing, the API exits at start-up with `ACCESS360 API refuses to start: ...` naming each missing variable (exit code 3 from uvicorn).

**Migrations** are a separate step and are not run by the API container. Run once per release, before the new API version takes traffic, from the same image (as a release or pre-deploy command, or a one-off job):

```bash
alembic upgrade head        # environment: A360_DATABASE_OWNER_URL (and A360_APP_DB_ROLE if the app role is not access360_app)
```

### Database requirements

* PostgreSQL 16 with the **PostGIS** extension available. Migration 0004 runs `CREATE EXTENSION IF NOT EXISTS postgis`, so the owner role must be allowed to create it (or an administrator creates it first). Tested here with PostgreSQL 16 and PostGIS 3.4.
* **Two roles.** The owner role owns the tables and runs migrations. The app role (`access360_app` by default) must **not** own the tables, so that row level security applies to it; migrations grant it the table rights it needs. Create the app role before the first migration, for example:

  ```sql
  CREATE ROLE access360_app LOGIN PASSWORD '<strong value>';
  GRANT CONNECT ON DATABASE <db> TO access360_app;
  ```

  Some managed services do not let you create roles with SQL; use the provider's console or API in that case. The app role must not be a superuser and must not have `BYPASSRLS`, or tenant isolation in the database is lost.

### Client address for rate limits (A360_TRUSTED_PROXY_HOPS)

Per-IP limits (login, registration, password reset) use the TCP peer address by default. Behind Netlify and a container host's load balancer, that address belongs to a proxy, so every user shares one bucket: one person can exhaust the registration limit (5 per minute) for everyone. Set `A360_TRUSTED_PROXY_HOPS` to the number of proxies that append to `X-Forwarded-For` before the request reaches the API; the API then uses the N-th entry from the right and ignores entries further left, which a client can forge. A likely value is 2 (Netlify, then the host's load balancer), but this depends on both providers and **has not been verified**: after deploying, inspect the `X-Forwarded-For` header the API receives and count the entries added after the real client address. If the backend URL is reachable directly (it must be, for Netlify to call it), a caller who bypasses Netlify can put arbitrary addresses in the header and so rotate per-IP buckets. The login limit is keyed on address and e-mail together, so such a caller is then not limited per account; only the password-forgot request also has a per-e-mail limit. Keep the default 0 unless the proxy chain is confirmed, and consider restricting direct access to the API if the host allows it.

### Where the backend can run

Any host that runs a Docker image over HTTPS together with a PostgreSQL service that offers PostGIS, for example:

* a platform-as-a-service that deploys a Dockerfile or a container image;
* a serverless container service from a cloud provider;
* a managed Kubernetes cluster;
* a virtual machine with Docker Compose (this repository's `docker-compose.yml`), with a TLS reverse proxy in front.

For the database: a managed PostgreSQL service whose supported extensions include PostGIS and that allows a second, non-owner login role; or PostgreSQL with PostGIS run by you (for example the `postgis/postgis:16-3.4` image) with backups you operate. Check each provider's documentation for PostGIS support, role management and TLS, and check the provider's current pricing. Nothing here has been tried on a specific provider, and no account or resource has been created.

## Production checklist (not yet done)

* Managed PostgreSQL with backups and point-in-time recovery; restore tested.
* Encryption at rest on the database and the storage volume. MFA secrets are not yet encrypted in the application (limitation L13).
* Set `A360_REDIS_URL` (rate limits and "log out everywhere" shared across instances) and the SMTP variables (password reset e-mail). If SMTP is missing, reset requests still answer 202 but the e-mail fails (logged without the link).
* Changing `A360_JWT_SECRET` ends every session and invalidates every pending password reset link.
* Secrets in a secret manager, not in `.env` files.
* Object storage for documents (limitation L19).
* Error monitoring: the API logs JSON lines with a request ID. Connect a monitoring service after choosing one.
* No production deployment has been made. None will be made without explicit approval.
