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
| A360_DATA_KEY | Fernet key for field encryption (`python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`). Not used yet: MFA secret encryption waits for a column migration (limitation L13). Keep it in the secret manager | unset |
| A360_DATA_KEYS_OLD | Comma-separated previous data keys still accepted for decryption during a rotation | unset |

## Production checklist (not yet done)

* Managed PostgreSQL with backups and point-in-time recovery; restore tested.
* Encryption at rest on the database and the storage volume. MFA secrets are not yet encrypted in the application (limitation L13).
* Set `A360_REDIS_URL` (rate limits and "log out everywhere" shared across instances) and the SMTP variables (password reset e-mail). If SMTP is missing, reset requests still answer 202 but the e-mail fails (logged without the link).
* Changing `A360_JWT_SECRET` ends every session and invalidates every pending password reset link.
* Secrets in a secret manager, not in `.env` files.
* Object storage for documents (limitation L19).
* Error monitoring: the API logs JSON lines with a request ID. Connect a monitoring service after choosing one.
* No production deployment has been made. None will be made without explicit approval.
