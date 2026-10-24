from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, engine, orgs, projects, scenarios
from .config import get_settings
from .engine import ENGINE_VERSION

app = FastAPI(
    title="Mini-Grid Financial Model Studio API",
    version=ENGINE_VERSION,
    description="Deterministic project-finance engine for mini-grid portfolios. Results are not a certification "
                "by AfDB, the World Bank or CrossBoundary, nor legal or investment advice.",
)
settings = get_settings()
if settings.cors_origins:
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=False,
                       allow_methods=["GET", "POST", "PUT", "PATCH"], allow_headers=["Authorization", "Content-Type"])


@app.middleware("http")
async def security_headers(request, call_next):
    resp = await call_next(request)
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    resp.headers.setdefault("Cache-Control", "no-store")
    return resp


for r in (auth.router, orgs.router, projects.router, scenarios.router, engine.router):
    app.include_router(r, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "engine_version": ENGINE_VERSION}
