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
