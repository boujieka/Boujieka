# ACCESS360 AFRICA: technical architecture (MVP, Phase 1)

## 1. Overview

```
Browser (Next.js app, EN/FR)
   │  same-origin /api/* (Next.js rewrite)
   ▼
FastAPI (backend/app)
   ├── routers: auth · orgs (members, dashboard, admin) · projects (inputs, runs, sensitivity,
   │            minimum subsidy, milestones, exports) · geo (countries, datasets, optimizer, engine helpers)
   ├── deps: session cookie / bearer token → user → membership + role → tenant context
   ├── services: runs (engine execution, JSON-safe results) · exports (XLSX, teaser PDF) · audit
   └── engine (pure Python, no I/O): inputs · model · checks · sensitivity · optimizer · finance
   ▼
PostgreSQL 16 (row-level security on tenant tables) · local file storage for generated documents
```

**Why the engine is separate.**
* The financial engine has no knowledge of HTTP or the database.
* It can be tested, versioned and audited on its own.
* AI explanations (Phase 4) will read engine outputs. They will never compute them.

## 2. Multi-tenancy and security

| Layer | Control |
|---|---|
| Authentication | Email and password (bcrypt, cost 12; policy: 12 or more characters, mixed case, a digit). Signed session token (HS256, 60 minutes, `typ=session`) in an httpOnly, SameSite=Lax cookie. Bearer token accepted for API clients |
| Password lifecycle | `POST /api/auth/password/forgot` always answers 202 with the same body; the link is e-mailed (console backend in development, SMTP in production) and never returned. The reset token is signed with a purpose-derived key, lasts 30 minutes and is bound to a keyed fingerprint of the current password hash, so it stops working once used. `password/reset` and `password/change` apply the password policy |
| Session revocation | Each session carries a version derived from the password hash: a password change or reset ends all earlier sessions (the changing session gets a new cookie). `POST /api/auth/logout-all` sets a per-user cut-off in Redis (in memory without Redis) that rejects every session issued before it. No new tables |
| CSRF | Cookie-authenticated state-changing requests must carry `X-Requested-With: access360` |
| MFA | TOTP (RFC 6238). Privileged actions (adding members, platform administration) require an MFA-verified session. Secrets are not yet encrypted in the application: `app/crypto.py` (Fernet, key rotation) is ready but waits for a column migration (L13) |
| Authorisation (API) | Every org-scoped route checks membership and minimum role (viewer < analyst < admin < owner). A non-member gets 404, so the API does not reveal that the organisation exists |
| Authorisation (database) | The app connects as `access360_app`, which is not the table owner. Tenant tables have `ENABLE` and `FORCE ROW LEVEL SECURITY`, with policies on `org_id = current_setting('app.current_org')`. The context is set per transaction. With no context, queries return no rows |
| Accreditation | Registering as an accredited organisation sets status `pending`. Only a platform administrator with an MFA session can verify or reject it |
| Audit | `audit_logs` is append-only for the app role (UPDATE and DELETE revoked). It records registration, login, project changes, input changes, model runs, documents and accreditation |
| Uploads | Parsed as data (JSON or CSV), size limited, validated against a GeoJSON subset, never rendered as HTML |
| Headers | `X-Content-Type-Options`, `X-Frame-Options: DENY`, `Referrer-Policy`, and a request ID on every response |
| Rate limit | Sliding window on login (IP and email), registration (IP), MFA verification (user), password forgot (IP and email), reset (IP) and change (user). Shared through Redis when `A360_REDIS_URL` is set (atomic Lua script, Redis clock); in memory otherwise and as the fallback if Redis fails |

Tables **without** RLS (`users`, `organizations`, `memberships`) are only reached through API code paths that filter on the current user.

## 3. Data model

| Table | Tenant | Purpose |
|---|---|---|
| organizations | n/a | Workspace: kind, accreditation status, plan, demo flag |
| users | n/a | Account, password hash, MFA, superadmin flag |
| memberships | n/a | User ↔ organisation with role |
| projects | yes (RLS) | Site or site batch, stage, location, GeoJSON, current inputs (JSON), inputs version, demo flag |
| model_runs | yes (RLS) | Immutable record of one engine run: inputs snapshot and SHA-256, engine version, status, checks, warnings, metrics, annual and quarterly results |
| milestones | yes (RLS) | Basic project management |
| generated_documents | yes (RLS) | Every export, with the run, engine version, inputs hash and file hash |
| datasets | yes (RLS; `org_id` NULL = platform dataset, read-only) | Map layers with mandatory metadata |
| audit_logs | yes (RLS insert/read) | Audit trail |

Migrations: Alembic (`backend/migrations`). Migrations run as the owner role. The app role has only DML grants.

## 4. Module status

| Module | MVP state |
|---|---|
| ACCESS FINANCE | Engine, runs, checks, status, sensitivities, tornado, minimum subsidy, XLSX export (values), one-page teaser |
| ACCESS OPTIMIZER | Screening comparison of options A to G, feasibility gates, weighted score, Pareto flag, least-cost and recommended option with explanation |
| ACCESS MAP | Country list, project markers, dataset registry with mandatory metadata, GeoJSON and CSV upload. No third-party data bundled (licensing and network) |
| Project management | Projects, stages, milestones, dashboard alerts |
| MARKETPLACE, DELIVERY, VERIFY, ACADEMY, Copilot, billing | Planned (see roadmap). Data model fields reserved: `marketplace_visible`, `plan` |

## 5. Dependencies between modules

```
inputs ──► model ──► checks ──► (status)
   │          └──► sensitivity (reruns model) ──► minimum subsidy
optimizer (independent of model; future link: chosen option prefills project inputs)
runs service ──► model + checks ──► model_runs table ──► exports, dashboard
```
