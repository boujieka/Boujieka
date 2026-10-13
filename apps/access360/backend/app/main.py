"""ACCESS360 AFRICA API."""
from __future__ import annotations

import logging
import time
import uuid

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import ENGINE_VERSION, get_settings
from .crypto import cipher
from .routers import auth, geo, orgs, portfolio, projects, spatial

log = logging.getLogger("access360")
logging.basicConfig(level=logging.INFO, format='{"t":"%(asctime)s","level":"%(levelname)s","msg":%(message)s}')

@asynccontextmanager
async def lifespan(_app):
    st = get_settings()
    problems = st.startup_problems()
    if problems:
        raise RuntimeError("ACCESS360 API refuses to start: " + "; ".join(problems))
    if st.env == "production" and not st.cookie_secure:
        log.warning('"A360_COOKIE_SECURE is false in production: the session cookie will also be sent over plain HTTP"')
    cipher()  # refuses to start in production without A360_DATA_KEY
    get_settings().secret()  # refuses to start in production without A360_JWT_SECRET
    yield


app = FastAPI(title="ACCESS360 AFRICA API", version=ENGINE_VERSION, lifespan=lifespan,
              description="Electrification investment, finance and delivery intelligence. Financial outputs come from the "
                          "deterministic ACCESS FINANCE engine; nothing in this API is investment advice.")
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in get_settings().cors_origins.split(",") if o.strip()],
                   allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE"],
                   allow_headers=["content-type", "x-requested-with", "authorization"])


@app.middleware("http")
async def headers_and_log(request: Request, call_next):
    rid = str(uuid.uuid4())
    t0 = time.perf_counter()
    resp = await call_next(request)
    resp.headers["X-Request-ID"] = rid
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["X-Frame-Options"] = "DENY"
    log.info('{"rid":"%s","method":"%s","path":"%s","status":%d,"ms":%.1f}', rid, request.method, request.url.path,
             resp.status_code, (time.perf_counter() - t0) * 1000)
    return resp


@app.get("/api/health")
def health():
    return {"status": "ok", "engine_version": ENGINE_VERSION}


for r in (auth.router, orgs.router, projects.router, geo.router, portfolio.router, spatial.router):
    app.include_router(r)
