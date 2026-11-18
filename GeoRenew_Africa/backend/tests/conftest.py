"""Base de test créée par les migrations Alembic (teste aussi les migrations).

Par défaut : SQLite dans un dossier temporaire (aucun service externe).
Pour tester sur PostGIS : GEORENEW_TEST_DATABASE_URL=postgresql+psycopg://...  (base dédiée, vidée).
"""

import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.db import get_db, make_engine
from app.main import app

BACKEND = Path(__file__).resolve().parents[1]


def _alembic(url: str) -> Config:
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "alembic"))
    cfg.attributes["database_url"] = url
    return cfg


@pytest.fixture
def db_url(tmp_path):
    url = os.environ.get("GEORENEW_TEST_DATABASE_URL") or f"sqlite:///{tmp_path / 'test.db'}"
    cfg = _alembic(url)
    if url.startswith("postgresql"):
        command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    yield url


@pytest.fixture
def client(db_url):
    engine = make_engine(db_url)
    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def _db():
        s = Session()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = _db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    engine.dispose()
