"""Application FastAPI : API /api/v1 et, si construit, le front-end React (frontend/dist)."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.api.v1 import router
from app.config import get_settings
from app.geo.crs import CRSError
from app.geo.importers import ImportError_
from app.geo.validation import GeometryError
from app.services import BusinessError

app = FastAPI(
    title="GeoRenew Africa API",
    version=__version__,
    description="Screening géospatial préliminaire (phase P1). Résultats indicatifs, non bancables.",
)
settings = get_settings()
app.add_middleware(
    CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["*"], allow_headers=["*"]
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "same-origin")
    return response


def _err(code: str, message: str, status: int = 422) -> JSONResponse:
    return JSONResponse({"detail": {"code": code, "message": message}}, status_code=status)


@app.exception_handler(ImportError_)
async def _import_error(_: Request, exc: ImportError_):
    return _err("fichier_refuse", str(exc))


@app.exception_handler(GeometryError)
async def _geom_error(_: Request, exc: GeometryError):
    return _err("geometrie_invalide", str(exc))


@app.exception_handler(CRSError)
async def _crs_error(_: Request, exc: CRSError):
    return _err("scr_invalide", str(exc))


@app.exception_handler(BusinessError)
async def _business_error(_: Request, exc: BusinessError):
    return _err(exc.code, str(exc))


app.include_router(router)

dist = settings.frontend_dist
if dist.is_dir() and (dist / "index.html").is_file():
    app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    async def spa(path: str):
        candidate = (dist / path).resolve()
        if path and candidate.is_file() and dist.resolve() in candidate.parents:
            return FileResponse(candidate)
        return FileResponse(dist / "index.html")
