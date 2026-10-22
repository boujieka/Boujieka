from sqlalchemy import func, select

import app.models as m
from app.reference.countries import COUNTRIES


def test_54_countries_with_required_fields(db):
    assert db.scalar(select(func.count(m.Country.id))) == 54
    assert len({c.iso2 for c in COUNTRIES}) == len({c.iso3 for c in COUNTRIES}) == len({c.numeric for c in COUNTRIES}) == 54
    for c in db.scalars(select(m.Country)):
        assert len(c.iso2) == 2 and len(c.iso3) == 3 and len(c.currency) == 3
        assert c.name_en and c.name_fr and c.region and c.subregion and c.official_languages


def test_cameroon_is_the_only_active_country_by_configuration(db):
    active = db.scalars(select(m.Country.iso3).where(m.Country.is_active.is_(True))).all()
    assert active == ["CMR"]
    cmr = db.scalar(select(m.Country).where(m.Country.iso3 == "CMR"))
    assert cmr.currency == "XAF" and set(cmr.official_languages) == {"fr", "en"}
    regions = db.scalars(select(m.AdminRegion).where(m.AdminRegion.country_id == cmr.id)).all()
    assert len(regions) == 10


def test_second_country_activated_by_configuration_only(db, monkeypatch):
    from app.config import get_settings
    from app.reference.seed import sync_active_countries

    monkeypatch.setattr(get_settings(), "active_countries", ["CMR", "SEN"])
    assert sync_active_countries(db) == ["CMR", "SEN"]
    assert db.scalar(select(m.Country).where(m.Country.iso3 == "SEN")).is_active
    conn = db.scalar(select(m.SourceConnector).where(m.SourceConnector.key == "worldbank_projects"))
    assert conn.config["countries"] == ["CMR", "SEN"]


def test_donor_registry_and_connectors_seeded(db):
    codes = set(db.scalars(select(m.FinancingPartner.code)))
    assert {"WB", "AFDB", "AFD", "IATI", "EIB", "ISDB", "KFW", "JICA", "GEF", "GCF", "BADEA", "SFD", "KFAED", "ADFD", "IFAD",
            "UNDP", "UNICEF", "FAO", "UNIDO"} <= codes
    conns = {c.key: c for c in db.scalars(select(m.SourceConnector))}
    assert conns["worldbank_projects"].enabled and conns["afdb_iati"].enabled and conns["afd_iati"].enabled
    assert conns["kfw"].status == "not_implemented" and not conns["kfw"].enabled
    assert conns["afdb_portal"].status == "blocked"
    # Nothing is "operational" before a real successful sync.
    assert all(c.status != "operational" for c in conns.values())


def test_no_project_data_is_seeded(db):
    assert db.scalar(select(func.count(m.Project.id))) == 0
