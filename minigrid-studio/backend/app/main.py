from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, engine, exports, orgs, projects, scenarios
from .config import get_settings
from .engine import ENGINE_VERSION

settings = get_settings()
app = FastAPI(
    docs_url="/docs" if settings.expose_docs else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.expose_docs else None,
    title="Mini-Grid Financial Model Studio API",
    version=ENGINE_VERSION,
    description="Deterministic project-finance engine for mini-grid portfolios. Results are not a certification "
                "by AfDB, the World Bank or CrossBoundary, nor legal or investment advice.",
)
if settings.cors_origins:
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=False,
                       allow_methods=["GET", "POST", "PUT", "PATCH"], allow_headers=["Authorization", "Content-Type"])


@app.middleware("http")
async def security_headers(request, call_next):
    # request-size guard (Content-Length based; also enforce a limit at the reverse proxy)
    length = request.headers.get("content-length")
    limit = (settings.max_upload_mb * 1024 + 512) * 1024 if request.url.path.endswith(("/import-xlsm", "/export-crossboundary")) \
        else settings.max_json_body_kb * 1024
    if length and length.isdigit() and int(length) > limit:
        from fastapi.responses import JSONResponse
        return JSONResponse({"detail": "request body too large"}, status_code=413)
    resp = await call_next(request)
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    resp.headers.setdefault("Cache-Control", "no-store")
    resp.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    resp.headers.setdefault("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
    return resp


for r in (auth.router, orgs.router, projects.router, scenarios.router, exports.router, engine.router):
    app.include_router(r, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "engine_version": ENGINE_VERSION}
