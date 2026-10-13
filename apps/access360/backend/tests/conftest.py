"""Test configuration. API tests need PostgreSQL (the RLS policies are part of what is tested); they are skipped
when A360_TEST_DATABASE_URL is not reachable. Engine tests need nothing."""
from __future__ import annotations

import os

import pytest

TEST_APP_URL = os.environ.get("A360_TEST_DATABASE_URL", "postgresql+psycopg://access360_app:app@127.0.0.1:5433/access360_test")
TEST_OWNER_URL = os.environ.get("A360_TEST_DATABASE_OWNER_URL", "postgresql+psycopg://postgres@127.0.0.1:5433/access360_test")


def _db_up() -> bool:
    try:
        from sqlalchemy import create_engine, text
        with create_engine(TEST_OWNER_URL).connect() as c:
            c.execute(text("select 1"))
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def db_ready(tmp_path_factory):
    if not _db_up():
        pytest.skip("PostgreSQL test database not reachable")
    os.environ["A360_DATABASE_URL"] = TEST_APP_URL
    os.environ["A360_DATABASE_OWNER_URL"] = TEST_OWNER_URL
    os.environ["A360_ENV"] = "test"
    os.environ["A360_JWT_SECRET"] = "test-secret-not-for-production-0123456789"
    os.environ["A360_STORAGE_DIR"] = str(tmp_path_factory.mktemp("storage"))
    os.environ["A360_LOGIN_RATE_PER_MINUTE"] = "1000"
    os.environ["A360_REGISTER_RATE_PER_MINUTE"] = "1000"
    os.environ["A360_MFA_RATE_PER_MINUTE"] = "1000"
    os.environ["A360_PASSWORD_RATE_PER_MINUTE"] = "1000"
    os.environ["A360_EMAIL_BACKEND"] = "memory"
    os.environ.pop("A360_REDIS_URL", None)
    from sqlalchemy import create_engine, text

    from app.config import get_settings
    from app.db import reset_engine
    get_settings.cache_clear()
    reset_engine()
    with create_engine(TEST_OWNER_URL, isolation_level="AUTOCOMMIT").connect() as c:
        c.execute(text("DROP SCHEMA public CASCADE"))
        c.execute(text("CREATE SCHEMA public"))
        c.execute(text("GRANT USAGE ON SCHEMA public TO access360_app"))
    from alembic import command
    from alembic.config import Config
    cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    cfg.set_main_option("script_location", os.path.join(os.path.dirname(__file__), "..", "migrations"))
    cfg.attributes["url"] = TEST_OWNER_URL
    command.upgrade(cfg, "head")
    yield


@pytest.fixture()
def client(db_ready):
    from fastapi.testclient import TestClient

    from app.main import app
    with TestClient(app) as c:
        c.headers.update({"x-requested-with": "access360"})
        yield c
