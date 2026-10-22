"""Migration tests: Alembic schema and the legacy MVP v0.1 data migration (synthetic MVP database)."""

import sqlite3

from sqlalchemy import select

import app.models as m
from app.migration.mvp import migrate

MVP_DDL = """
CREATE TABLE countries (code VARCHAR(3) PRIMARY KEY, name VARCHAR(120) NOT NULL);
CREATE TABLE projects (id VARCHAR(36) PRIMARY KEY, country_code VARCHAR(3) NOT NULL, name VARCHAR(350) NOT NULL, sector VARCHAR(100) NOT NULL,
  agency VARCHAR(200), status VARCHAR(80), start_year INTEGER, end_year INTEGER, initial_cost NUMERIC(20,2), revised_cost NUMERIC(20,2),
  currency VARCHAR(3), physical_progress NUMERIC(5,2), operational_status VARCHAR(100), source_url TEXT, source_date VARCHAR(20), notes TEXT);
CREATE TABLE financings (id VARCHAR(36) PRIMARY KEY, project_id VARCHAR(36) NOT NULL, funder VARCHAR(200) NOT NULL, instrument VARCHAR(100),
  committed NUMERIC(20,2), currency VARCHAR(3), source_url TEXT);
CREATE TABLE disbursements (id VARCHAR(36) PRIMARY KEY, financing_id VARCHAR(36) NOT NULL, year INTEGER NOT NULL, amount NUMERIC(20,2) NOT NULL, source_url TEXT);
CREATE TABLE amendments (id VARCHAR(36) PRIMARY KEY, project_id VARCHAR(36) NOT NULL, date VARCHAR(20), amount NUMERIC(20,2), currency VARCHAR(3), reason TEXT, source_url TEXT);
CREATE TABLE actions (id VARCHAR(36) PRIMARY KEY, project_id VARCHAR(36) NOT NULL, problem TEXT, recommendation TEXT, owner VARCHAR(200), due_date VARCHAR(20), status VARCHAR(30));
"""


def _mvp_db(path):
    c = sqlite3.connect(path)
    c.executescript(MVP_DDL)
    c.execute("INSERT INTO countries VALUES ('CMR','Cameroun')")
    c.execute("INSERT INTO projects VALUES ('p1','CMR','SYNTHETIC Route Ebolowa-Akom II','Transport routier','MINTP','En cours',2016,2021,"
              "100000000000,130000000000,'XAF',62.5,NULL,'https://example.test/route.pdf','2023-12-31','synthetic')")
    c.execute("INSERT INTO projects VALUES ('p2','CMR','SYNTHETIC Centre de santé','Santé','MINSANTE','Achevé',2015,2018,NULL,NULL,'XAF',100,"
              "'Non opérationnel',NULL,NULL,NULL)")
    c.execute("INSERT INTO financings VALUES ('f1','p1','Banque africaine de développement','Prêt',90000000000,'XAF','https://example.test/route.pdf')")
    c.execute("INSERT INTO financings VALUES ('f2','p1','Fonds SYNTHETIC inconnu','Don',5000000000,'XAF',NULL)")
    c.execute("INSERT INTO disbursements VALUES ('d1','f1',2019,20000000000,NULL)")
    c.execute("INSERT INTO disbursements VALUES ('d2','f1',2020,15000000000,NULL)")
    c.execute("INSERT INTO amendments VALUES ('a1','p1','2020-05-01',30000000000,'XAF','Avenant n°1 (synthetic)',NULL)")
    c.execute("INSERT INTO actions VALUES ('x1','p1','Retard','Réunion de suivi','MINTP','2024-06-30','En cours')")
    c.commit()
    c.close()


def test_mvp_migration_preserves_everything(db, tmp_path):
    path = tmp_path / "mvp.db"
    _mvp_db(path)
    report = migrate(f"sqlite:///{path}", db)
    assert report["read"] == {"countries": 1, "projects": 2, "financings": 2, "disbursements": 2, "amendments": 1, "actions": 1}
    assert report["created"]["projects"] == 2 and report["created"]["agreements"] == 2 and report["created"]["disbursements"] == 2
    p1 = db.scalar(select(m.Project).where(m.Project.title == "SYNTHETIC Route Ebolowa-Akom II"))
    assert p1.ap2i_id.startswith("AP2I-CMR-TRANSPORT-") and p1.status == "active" and p1.revised_estimated_cost == 130000000000
    partners = {a.partner.code for a in p1.agreements}
    assert "AFDB" in partners and any(c.startswith("LEGACY:") for c in partners)
    flows = db.scalars(select(m.Disbursement)).all()
    assert {f.period_year for f in flows} == {2019, 2020} and all(f.value_date is None for f in flows)  # no invented day
    p2 = db.scalar(select(m.Project).where(m.Project.title == "SYNTHETIC Centre de santé"))
    assert p2.operational_status == "not_operational" and p2.verification_status == "needs_review"
    assert db.scalar(select(m.SourceObservation).where(m.SourceObservation.field == "legacy_amendment")).value_numeric == 30000000000
    action = db.scalar(select(m.RecoveryAction))
    assert action.implementation_status == "in_progress" and action.origin == "user"
    assert db.scalar(select(m.SourceRecord).where(m.SourceRecord.source_identifier == "mvp:projects:p1")).payload["name"]
    # Idempotent
    again = migrate(f"sqlite:///{path}", db)
    assert again["created"]["projects"] == 0 and again["created"]["skipped_existing"] == 2
    # year-only disbursements still appear in the annual portfolio
    from app.finance.portfolio import compute_portfolio

    pf = compute_portfolio(db, "CMR", 2019, 2020)
    assert pf["years"][0]["disbursements"]["by_currency"] == {"XAF": "20000000000.0000"}


def test_alembic_migrations_match_models():
    """Upgrade an empty database with Alembic, then check autogenerate finds no difference."""
    import os

    import pytest
    from alembic import command
    from alembic.autogenerate import compare_metadata
    from alembic.config import Config
    from alembic.runtime.migration import MigrationContext
    from sqlalchemy import create_engine, text

    url = os.environ.get("AP2I_MIGRATION_TEST_DATABASE_URL", "postgresql+psycopg://ap2i:ap2i@localhost:5432/ap2i_migr")
    if "migr" not in url:
        pytest.skip("needs a throwaway migration database")
    e = create_engine(url)
    try:
        with e.begin() as c:
            c.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover - environment without the database
        pytest.skip(f"migration database unavailable: {exc}")
    cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    cfg.set_main_option("script_location", os.path.join(os.path.dirname(__file__), "..", "alembic"))
    old = os.environ.get("AP2I_DATABASE_URL")
    os.environ["AP2I_DATABASE_URL"] = url
    from app.config import get_settings

    get_settings.cache_clear()
    try:
        command.downgrade(cfg, "base")
        command.upgrade(cfg, "head")
        with e.connect() as conn:
            ctx = MigrationContext.configure(conn, opts={"include_object": lambda o, n, t, r, c: n not in {
                "spatial_ref_sys", "geog", "ix_project_locations_geog"}})
            diff = compare_metadata(ctx, m.Base.metadata)
        assert diff == []
        command.downgrade(cfg, "base")
    finally:
        os.environ["AP2I_DATABASE_URL"] = old
        get_settings.cache_clear()
