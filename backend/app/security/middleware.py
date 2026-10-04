"""Security gateway: request id, API-key authentication, rate limiting, audit, headers.

Order for each request:
  1. assign a request id (client-supplied X-Request-ID if well-formed);
  2. authenticate X-API-Key if present: unknown/revoked → 401 on any route;
  3. rate-limit per key id, else per client IP (exempt hosts skipped);
  4. run the route; audit it if it is protected (require_role) or ended 401/403;
  5. add security headers to every response, including refusals.
"""

import logging
import re
import uuid

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from app.config import Settings
from app.security.audit import app_session, write_audit
from app.security.auth import API_KEY_HEADER
from app.security.keys import authenticate
from app.security.principal import PUBLIC, Principal
from app.security.ratelimit import SlidingWindowLimiter, retry_after_header

log = logging.getLogger("abi.security")

REQUEST_ID_HEADER = "X-Request-ID"
_REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
AUDITED_STATUSES = frozenset({401, 403, 429})

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    # JSON API: nothing may be framed, scripted or loaded from these responses.
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
    "Cross-Origin-Resource-Policy": "same-site",
    "X-ABI-Disclaimer": "information-only; not-investment-advice",
}
# The interactive docs page loads Swagger UI assets from a CDN; keep it usable.
_DOCS_PATHS = ("/docs", "/redoc")


def _lookup(app: FastAPI, raw_key: str) -> Principal | None:
    with app_session(app) as session:
        key = authenticate(session, raw_key)
        return Principal(role=key.role, key_id=key.id) if key else None


def install_security(app: FastAPI, settings: Settings) -> None:
    limiter = SlidingWindowLimiter()
    app.state.rate_limiter = limiter
    exempt = frozenset(settings.rate_limit_exempt_hosts)

    @app.middleware("http")
    async def security_gateway(request: Request, call_next) -> Response:
        incoming = request.headers.get(REQUEST_ID_HEADER, "")
        request_id = incoming if _REQUEST_ID_RE.match(incoming) else uuid.uuid4().hex
        host = request.client.host if request.client else None
        principal = PUBLIC

        async def audit(status_code: int) -> None:
            await run_in_threadpool(
                write_audit, app, principal, request.method, request.url.path, status_code, host, request_id
            )

        def finish(response: Response) -> Response:
            for name, value in SECURITY_HEADERS.items():
                if name == "Content-Security-Policy" and request.url.path.startswith(_DOCS_PATHS):
                    continue
                response.headers.setdefault(name, value)
            response.headers[REQUEST_ID_HEADER] = request_id
            return response

        raw_key = request.headers.get(API_KEY_HEADER)
        if raw_key is not None:
            found = await run_in_threadpool(_lookup, app, raw_key)
            if found is None:
                # Never echo the presented key, not even partially.
                log.info("rejected API key request_id=%s path=%s", request_id, request.url.path)
                await audit(401)
                return finish(
                    JSONResponse(
                        {"detail": "Invalid or revoked API key."},
                        status_code=401,
                        headers={"WWW-Authenticate": API_KEY_HEADER},
                    )
                )
            principal = found

        if settings.rate_limit_enabled and host not in exempt:
            if principal.key_id is not None:
                client, limit = f"key:{principal.key_id}", settings.rate_limit_per_minute_key
            else:
                client, limit = f"ip:{host}", settings.rate_limit_per_minute
            wait = limiter.hit(client, limit)
            if wait is not None:
                await audit(429)
                return finish(
                    JSONResponse(
                        {"detail": "Rate limit exceeded. Retry later."},
                        status_code=429,
                        headers={"Retry-After": retry_after_header(wait)},
                    )
                )

        request.state.principal = principal
        response = await call_next(request)
        if getattr(request.state, "audit", False) or response.status_code in AUDITED_STATUSES:
            await audit(response.status_code)
        return finish(response)
