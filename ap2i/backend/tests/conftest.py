"""Test configuration. Runs on PostgreSQL (AP2I_TEST_DATABASE_URL, default local ap2i_test).

The database is THROWAWAY: all tables are dropped and recreated for the session and truncated
between tests. Never point AP2I_TEST_DATABASE_URL at a real database.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

TEST_DB = os.environ.get("AP2I_TEST_DATABASE_URL", "postgresql+psycopg://ap2i:ap2i@localhost:5432/ap2i_test")
os.environ["AP2I_DATABASE_URL"] = TEST_DB
os.environ["AP2I_ENVIRONMENT"] = "test"
os.environ["AP2I_DOCUMENT_STORE_DIR"] = tempfile.mkdtemp(prefix="ap2i-test-")
os.environ["AP2I_RATE_LIMIT_PER_MINUTE"] = "100000"
os.environ["AP2I_AUTH_RATE_LIMIT_PER_MINUTE"] = "100000"
os.environ["AP2I_LLM_PROVIDER"] = "none"

import httpx  # noqa: E402
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine, select, text  # noqa: E402

import app.models as m  # noqa: E402
from app.db import SessionLocal, set_engine  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def engine():
    assert "test" in TEST_DB, "Refusing to run tests against a database whose name does not contain 'test'"
    e = create_engine(TEST_DB)
    m.Base.metadata.drop_all(e)
    m.Base.metadata.create_all(e)
    set_engine(e)
    return e


@pytest.fixture()
def db(engine):
    from app.reference.seed import seed_reference
    from app.security.deps import limiter

    names = ", ".join(f'"{t.name}"' for t in reversed(m.Base.metadata.sorted_tables))
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE {names} RESTART IDENTITY CASCADE"))
    limiter.reset()
    s = SessionLocal()
    seed_reference(s)
    yield s
    s.close()


@pytest.fixture()
def client(db):
    from app.main import app

    return TestClient(app)


def mock_client(routes: dict[str, tuple[int, bytes, str]]) -> httpx.Client:
    """httpx client whose responses are served from fixtures, keyed by URL prefix."""

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        for prefix, (status, body, ctype) in routes.items():
            if url.startswith(prefix):
                return httpx.Response(status, content=body, headers={"content-type": ctype})
        return httpx.Response(404, content=b"not mocked")

    return httpx.Client(transport=httpx.MockTransport(handler))


def wb_connector(config=None):
    from app.connectors.worldbank import WorldBankProjectsConnector

    body = (FIXTURES / "wb_projects_synthetic.json").read_bytes()
    c = WorldBankProjectsConnector(config, client=mock_client({"https://search.worldbank.org": (200, body, "application/json")}))
    c.min_interval_seconds = 0
    return c


def iati_connector(cls=None, config=None):
    from app.connectors.iati import IATIConnector

    cls = cls or IATIConnector
    body = (FIXTURES / "iati_synthetic.xml").read_bytes()
    c = cls(config, client=mock_client({"https://datastore.codeforiati.org": (200, body, "application/xml")}))
    c.min_interval_seconds = 0
    return c


def make_user(db, email: str, roles: list[str], org_id: int | None = None, plan: str | None = None, password="Str0ng!Passw0rd#"):
    from datetime import datetime, timezone

    from app.security.core import hash_password

    u = m.User(email=email, password_hash=hash_password(password), full_name=email.split("@")[0], organization_id=org_id,
               email_verified_at=datetime.now(timezone.utc))
    db.add(u)
    db.flush()
    for code in roles:
        role = db.scalar(select(m.RoleDef).where(m.RoleDef.code == code))
        db.add(m.UserRole(user_id=u.id, role_id=role.id, organization_id=org_id))
    if plan:
        p = db.scalar(select(m.Plan).where(m.Plan.code == plan))
        db.add(m.Subscription(plan_id=p.id, user_id=u.id, organization_id=org_id, status="active"))
    db.commit()
    return u


def token_for(client, email: str, password="Str0ng!Passw0rd#") -> dict:
    r = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture()
def loaded(db):
    """Database with the synthetic World Bank + IATI fixtures ingested through the real pipeline."""
    from app.ingestion.pipeline import run_sync

    run_sync(db, "worldbank_projects", connector=wb_connector(), force=True)
    run_sync(db, "iati_generic", connector=iati_connector(), force=True)
    return db
