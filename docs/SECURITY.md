# Security baseline (Phase 1b)

What protects the API today, how to operate it, and what is still required before a public,
multi-instance deployment. Code: `backend/app/security/`, tests: `backend/tests/test_security.py`.

## Threat model (brief)

| Asset | Threat | Control |
|---|---|---|
| Internal views (data quality, audit log, future write/admin routes) | Anonymous or under-privileged access | API keys + roles, `require_role(...)` on each protected route |
| API keys | Leak from the database, logs or responses | Only SHA-256 hashes stored; keys never logged, echoed or listed; constant-time check |
| API availability | Scraping / brute force / runaway clients | Per-key and per-IP sliding-window rate limit, `429` + `Retry-After` |
| Accountability | Unnoticed misuse | Audit log of every protected call and every `401`/`403`/`429` |
| Browser users of the frontend | Clickjacking, MIME sniffing, referrer leaks, cross-origin reads | Security headers; CORS allow-list (no wildcard) |
| Secrets | Committed to the repo | Environment variables only (`ABI_*`); nothing secret in code or compose files |

Out of scope for now: end-user accounts / SSO (identity-provider decision pending), TLS (terminated
by the hosting platform or a reverse proxy), DDoS protection (CDN/WAF level).

The public market endpoints remain open on purpose: they serve the public showcase and contain
only labelled synthetic or public reference data. `site/build.py` (run by the daily job) calls them
in-process through FastAPI's `TestClient`, without a key, and is not affected by this phase.

## Roles

| Role | How | Can access |
|---|---|---|
| `public` | No `X-API-Key` header | All read-only market endpoints (`/health`, `/dashboard/summary`, `/auctions`, `/countries`, `/opportunities`, …) |
| `analyst` | Key with role `analyst` | Public endpoints + `/api/v1/data-quality` |
| `admin` | Key with role `admin` | Everything, including `/api/v1/admin/audit-log` |

Responses: no key on a protected route → `401` (`WWW-Authenticate: X-API-Key`); a key that is
unknown or revoked → `401` **on any route** (a bad credential is never silently downgraded to public);
valid key with an insufficient role → `403`.

Protecting a new route:

```python
from fastapi import Depends
from app.models.enums import Role
from app.security.auth import require_role

@router.post("/things", dependencies=[Depends(require_role(Role.ADMIN))])
def create_thing(...): ...
```

`require_role` also marks the request for the audit log. Roles are an explicit allow-list (no
implicit hierarchy): `require_role(Role.ANALYST, Role.ADMIN)`.

## API keys

Keys look like `cart_<43 url-safe chars>` (256 bits from `secrets`). The prefix makes leaked keys
easy to find with secret scanners. Only `sha256(key)` is stored in `api_key.key_hash`; a fast hash is
fine because the input is random, not a password. Lookup is by hash, then `hmac.compare_digest`.

```bash
cd backend
python -m app.security.keys create --name "ops laptop" --role admin   # prints the key ONCE
python -m app.security.keys create --name "frontend" --role analyst
python -m app.security.keys list            # id, role, created, last used, revoked, name — never keys or hashes
python -m app.security.keys revoke --id 3   # immediate: next request with that key gets 401
```

The CLI uses `ABI_DATABASE_URL`. Copy the printed key straight into a secret manager; it cannot be
recovered. `last_used_at` is updated at most once a minute per key (a hint, not an audit trail).

Clients send the key in the `X-API-Key` header. Never put keys in URLs: query strings end up in
proxy and browser logs (the audit log stores the path only, never the query string).

**Frontend.** `frontend/src/lib/api.ts` calls the API from the Next.js server only. If `ABI_API_KEY` is
set in the server environment it is sent as `X-API-Key`; use an `analyst` key so the
`/admin/data-quality` page works. Never name it `NEXT_PUBLIC_*` (that would ship it to browsers).
Without a key the page shows a clear "not authorized" message instead of failing.

## Rate limiting

In-memory sliding window per client, 60-second window:

| Setting (env) | Default | Meaning |
|---|---|---|
| `ABI_RATE_LIMIT_ENABLED` | `true` | Master switch |
| `ABI_RATE_LIMIT_PER_MINUTE` | `120` | Requests/minute per client IP, without a key |
| `ABI_RATE_LIMIT_PER_MINUTE_KEY` | `600` | Requests/minute per API key (counted by key id, whatever the IP) |
| `ABI_RATE_LIMIT_EXEMPT_HOSTS` | `["testclient"]` | Peer hosts never throttled |

Over the limit → `429` with `Retry-After` (seconds) and an audit row. Requests with an invalid key
are refused (`401`) before the limiter and audited.

**Why `testclient` is exempt.** Starlette's `TestClient` reports the peer host `testclient`. The test
suite and `site/build.py` (≈70 calls in a burst, in the daily job) use it in-process. The value is
the socket peer, set by the ASGI server, so a remote client cannot claim it. To exercise the limiter
in a test, build an app with `create_app(Settings(rate_limit_exempt_hosts=[], ...))` (see
`TestRateLimit`).

**Limitations.** State is per process: with N workers or instances the effective limit is N times
higher, and counters reset on restart. Behind a reverse proxy, run uvicorn with
`--proxy-headers --forwarded-allow-ips=<proxy ip>`, otherwise every client shares the proxy's IP
bucket. Never trust `X-Forwarded-For` from arbitrary peers.

## Audit log

Table `audit_log`: `id, at, api_key_id, role, method, path, status_code, client_ip, request_id`.
Written for every request to a route guarded by `require_role` (success or failure) and for every
`401`, `403` and `429`. Public reads are not audited (high volume, no privilege involved).

- `path` excludes the query string; no header, key or body is stored.
- `client_ip` is truncated to the network (`/24` IPv4, `/48` IPv6): enough to spot abusive networks
  and correlate incidents, without keeping a precise personal identifier. Hashing was rejected: the
  IPv4 space is small enough to reverse an unsalted hash, and a salted one adds a secret to manage.
- `request_id` is the client's `X-Request-ID` if well-formed (`[A-Za-z0-9._-]{1,64}`), else a
  random id; it is echoed in the response header for correlation.
- Writes are best effort: a database error is logged (without secrets) and never fails the request.

Admins read it with `GET /api/v1/admin/audit-log?limit=100` (1–1000, newest first). Retention and
export to a SIEM are not implemented yet.

## Headers and CORS

Every response, including refusals, carries `X-Content-Type-Options: nosniff`,
`X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`,
`Content-Security-Policy: default-src 'none'; frame-ancestors 'none'` (skipped on `/docs` and `/redoc`
so Swagger UI still loads), `Cross-Origin-Resource-Policy: same-site` and `X-Request-ID`. The uvicorn
`Server` banner is removed with `--no-server-header` (Dockerfile and compose).

CORS: origins from `ABI_CORS_ORIGINS` (JSON list, default `["http://localhost:3000"]`); a `"*"` entry
is rejected at startup. Methods: `GET`; headers: `X-API-Key`, `X-Request-ID`, `Content-Type`.
The frontend calls the API server-side, so production normally needs no browser origin at all.

## Secrets

All configuration comes from `ABI_*` environment variables (`app/config.py`), loaded from the
process environment or an untracked `.env`. The credentials in `docker-compose.yml` are for local
development only. Never commit keys, never print them in CI logs, and never pass them as `NEXT_PUBLIC_*`.

## Before production

- **TLS termination** at the platform or reverse proxy; HSTS there.
- **Redis-backed rate limiter** (Redis is already in the compose stack) so limits hold across workers
  and instances; per-route limits for expensive endpoints.
- **Key rotation**: issue a new key, deploy it, revoke the old one (`revoke --id`); add expiry dates
  and a periodic review of `last_used_at` for unused keys.
- Audit-log retention policy, export/alerting on bursts of `401`/`429`.
- Identity provider for human users (SSO) if per-person access is needed; keys stay for services.
- Secret manager for `ABI_DATABASE_URL` and `ABI_API_KEY` instead of plain environment files.
