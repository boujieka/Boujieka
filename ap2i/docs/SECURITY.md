# AP²I — Security

Status: baseline controls implemented and tested. **Not yet production-ready**: no external penetration test,
no managed secrets store, no TLS termination configured in this repository, no backup automation tested
against a real host. See "Open items".

## Implemented controls
| Area | Control | Where / test |
|---|---|---|
| Passwords | Argon2id (argon2-cffi); min length 12, 3 character classes, common-password and email-name checks | `security/core.py`, `test_auth.py` |
| Sessions | JWT HS256, 60-min expiry, `token_version` revocation (logout, password reset, MFA change, role change) | `test_auth.py::test_password_reset`, `::test_mfa_flow` |
| MFA | TOTP (RFC 6238) with a 5-minute signed challenge; MFA-enabled accounts cannot use non-MFA tokens | `test_auth.py::test_mfa_flow` |
| Email verification / reset | One-time tokens, stored as SHA-256 only, expiry (48 h / 1 h), single use; no account enumeration | `test_auth.py` |
| Brute force | Per-IP auth rate limit; account lockout after 5 failures for 15 min | `test_auth.py::test_lockout_after_failed_logins` |
| Authorization | RBAC: 10 roles → permissions; plan features gate commercial functions | `test_authz_tenant.py` |
| Tenant isolation | `tenant_filter()` on every query of tenant-scoped tables; 404 (not 403) for other tenants' records; public aggregates exclude private rows | `test_authz_tenant.py::test_tenant_isolation`, `test_workflows.py::test_rescue_api_flow` |
| API keys | Enterprise only; random 256-bit keys, stored hashed, revocable | `test_authz_tenant.py::test_enterprise_api_key` |
| Rate limiting | Global per key/IP limit (429 + Retry-After). In-process: use Redis or a gateway for multi-instance | `main.py` |
| Input validation | Pydantic schemas, enum/regex constraints, bounded pagination, numeric parsing that never guesses | all routers |
| SQL injection | SQLAlchemy parameterised queries only; no string-built SQL with user input | code review |
| XSS / clickjacking | API returns JSON; CSP `default-src 'none'`, `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy: no-referrer`; frontend sets its own CSP | `test_api.py::test_security_headers` |
| CSRF | API uses bearer tokens (no cookies). The Next.js session cookie is httpOnly + SameSite=Strict and mutating proxy calls check `Origin` | frontend proxy |
| Uploads | Size limit (20 MB), extension allowlist (.csv/.xlsx), magic-byte check for XLSX, NUL-byte check for CSV, parsed as data only, never executed or served back | `test_workflows.py::test_upload_workflow_validates_and_imports` |
| Prompt injection | Imported text scanned for instruction patterns (flag at import); untrusted text fenced/escaped in prompts; system guard; numeric grounding check discards unsupported narratives | `test_pipeline.py::test_prompt_injection_text_is_flagged_not_obeyed`, `test_workflows.py::test_llm_narrative_grounding` |
| AI data leakage | The model receives only facts the caller is authorised to see (tenant filter applied before retrieval); no secrets in prompts; provider disabled by default | `assistant/service.py` |
| Secrets | Environment variables only; production refuses the default `AP2I_SECRET_KEY`; settings API refuses secret-like keys | `main.py`, `api/admin.py` |
| Audit | Logins, failures, MFA, password events, exports, reports, reviews, merges, admin changes, assistant use → `audit_logs` with truncated IP | `test_auth.py::test_audit_log_written` |
| Transport | HSTS header in production; TLS must be terminated by the reverse proxy / load balancer | deployment |
| Containers | Non-root users, no secrets baked into images | Dockerfiles |
| Dependencies | CI runs `pip-audit` and `npm audit --audit-level=high` | `.github/workflows/ap2i-ci.yml` |

## Backups and recovery (procedure)
* Database: `pg_dump -Fc` nightly to encrypted object storage, 30-day retention; weekly restore test into a
  scratch database followed by `pytest` smoke tests and `python -m app.cli connector-report`.
* Document store (`var/documents`, reports): object-storage versioning.
* Source data can be re-fetched from the official sources; manual uploads must be backed up (their only copy).
* Recovery: restore the dump, `alembic upgrade head`, restart api/worker/beat, run `python -m app.cli post-sync`.

## Open items before production
1. External penetration test and dependency audit triage (CI job is configured, not yet run on GitHub).
2. Reverse proxy with TLS, request size limits and a shared (Redis) rate limiter.
3. Secrets manager integration and key rotation procedure for `AP2I_SECRET_KEY` (rotation invalidates tokens).
4. SMTP provider configuration and SPF/DKIM; email is logged to console by default.
5. Automated, tested backups on the target host.
6. Malware scanning for uploaded files if PDF/DOCX upload is enabled (currently only CSV/XLSX are accepted).
