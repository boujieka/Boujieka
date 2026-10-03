from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auctions, buyers, countries, opportunities, overview, securities
from app.config import get_settings

DISCLAIMER = (
    "Information and analytics only. Not investment advice, not a recommendation, "
    "and no guarantee of returns or of access to any market."
)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="African Bond Intelligence API",
        version="0.1.0",
        description=f"Africa's Sovereign Debt Opportunity Engine.\n\n{DISCLAIMER}",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-ABI-Disclaimer"] = "information-only; not-investment-advice"
        return response

    api = APIRouter(prefix="/api/v1")

    @api.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok", "disclaimer": DISCLAIMER}

    for module in (overview, opportunities, buyers, countries, securities, auctions):
        api.include_router(module.router)
    app.include_router(api)
    return app


app = create_app()
