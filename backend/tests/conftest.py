"""Test fixtures.

Runs against in-memory SQLite by default. Set ABI_TEST_DATABASE_URL to a
throwaway PostgreSQL database to run the same suite against Postgres
(all tables in that database are dropped and recreated).
"""

import os
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import get_session
from app.main import create_app
from app.models import Base
from app.models.enums import Role
from app.security.keys import create_key
from app.seed.load import load_reference, load_synthetic

REFERENCE_DATE = date(2026, 10, 3)


@pytest.fixture(scope="session")
def engine():
    url = os.environ.get("ABI_TEST_DATABASE_URL")
    if url:
        eng = create_engine(url)
    else:
        eng = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()


@pytest.fixture(scope="session")
def seeded(engine):
    with Session(engine) as s:
        countries = load_reference(s)
        load_synthetic(s, countries, REFERENCE_DATE)
        s.commit()
    return engine


@pytest.fixture
def db(seeded):
    """A session whose changes are rolled back after each test."""
    conn = seeded.connect()
    tx = conn.begin()
    session = Session(bind=conn, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    tx.rollback()
    conn.close()


@pytest.fixture(scope="session")
def client(seeded):
    factory = sessionmaker(bind=seeded, expire_on_commit=False)

    def override():
        with factory() as s:
            yield s

    app = create_app()
    app.dependency_overrides[get_session] = override
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def api_keys(seeded) -> dict[Role, str]:
    """Plaintext keys for each key role, committed so the client can see them."""
    with Session(seeded) as s:
        keys = {role: create_key(s, f"test-{role.value}", role)[1] for role in (Role.ANALYST, Role.ADMIN)}
        s.commit()
    return keys


@pytest.fixture(scope="session")
def analyst_headers(api_keys) -> dict[str, str]:
    return {"X-API-Key": api_keys[Role.ANALYST]}


@pytest.fixture(scope="session")
def admin_headers(api_keys) -> dict[str, str]:
    return {"X-API-Key": api_keys[Role.ADMIN]}
