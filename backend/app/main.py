from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin, auctions, buyers, countries, ingest, opportunities, overview, securities
from app.config import Settings, get_settings
from app.security.auth import API_KEY_HEADER
from app.security.middleware import REQUEST_ID_HEADER, install_security

DISCLAIMER = (
    "Information and analytics only. Not investment advice, not a recommendation, "
    "and no guarantee of returns or of access to any market."
)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(
        title="African Bond Intelligence API",
        version="0.1.0",
        description=f"Africa's Sovereign Debt Opportunity Engine.\n\n{DISCLAIMER}",
    )
    # Authentication, rate limiting, audit and security headers (docs/SECURITY.md).
    install_security(app, settings)
    # Added last so it is outermost: refusals (401/429) also carry CORS headers.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET"],
        allow_headers=[API_KEY_HEADER, REQUEST_ID_HEADER, "Content-Type"],
        expose_headers=["Retry-After", REQUEST_ID_HEADER],
    )

    api = APIRouter(prefix="/api/v1")

    @api.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok", "disclaimer": DISCLAIMER}

    for module in (overview, opportunities, buyers, countries, securities, auctions, admin):
        api.include_router(module.router)
    # Review queue: analyst/admin only (see app/api/ingest.py).
    api.include_router(ingest.router)
    app.include_router(api)
    return app


app = create_app()
