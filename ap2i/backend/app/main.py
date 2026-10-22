"""AP²I API application. OpenAPI documentation at /docs and /openapi.json."""

from __future__ import annotations

import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.api import admin, auth, data, workflows
from app.config import get_settings
from app.security.deps import client_ip, limiter

DISCLAIMER = ("AP²I publishes information from official sources with provenance. Coverage is limited to connected sources. "
              "Alerts are signals for verification, not findings of wrongdoing.")


def create_app() -> FastAPI:
    s = get_settings()
    if s.is_production and (s.secret_key.startswith("dev-only") or len(s.secret_key) < 32):
        raise RuntimeError("AP2I_SECRET_KEY must be set to a strong secret (>= 32 chars) in production")
    app = FastAPI(title="AP²I — Africa Public Project Intelligence", version=__version__,
                  description="Every Project. Every Dollar. Every Impact.\n\n" + DISCLAIMER,
                  docs_url="/docs", openapi_url="/openapi.json")
    app.add_middleware(CORSMiddleware, allow_origins=s.cors_origins, allow_credentials=False,
                       allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"], allow_headers=["Authorization", "Content-Type", "X-API-Key"])

    @app.middleware("http")
    async def security(request: Request, call_next):
        rid = request.headers.get("x-request-id") or uuid.uuid4().hex[:16]
        key = request.headers.get("x-api-key") or request.headers.get("authorization") or client_ip(request)
        retry = limiter.check(f"req:{key[-40:]}", get_settings().rate_limit_per_minute)
        if retry is not None:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429, headers={"Retry-After": str(int(retry) + 1)})
        response = await call_next(request)
        response.headers["X-Request-Id"] = rid
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = response.headers.get("Cache-Control", "no-store")
        if not request.url.path.startswith(("/docs", "/redoc")):
            response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        if s.is_production:
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        return response

    @app.get("/api/v1/health", tags=["system"])
    def health():
        return {"status": "ok", "version": __version__, "disclaimer": DISCLAIMER, "active_countries": get_settings().active_countries}

    for r in (auth.router, data.router, workflows.router, admin.router):
        app.include_router(r, prefix="/api/v1")
    return app


app = create_app()
