"""LIVE tests against the real official sources (network). Run with: pytest -m live

They verify that each Tier-1 connector retrieves, parses, validates and persists REAL Cameroon records
(the condition for marking a connector operational), and cross-check the country reference codes.
"""

import pytest
from sqlalchemy import func, select

import app.models as m
from app.connectors.base import SyncParams
from app.ingestion.pipeline import run_sync

pytestmark = pytest.mark.live


@pytest.mark.parametrize("key", ["worldbank_projects", "worldbank_iati", "afdb_iati", "afd_iati"])
def test_tier1_connector_retrieves_and_persists_real_records(db, key):
    run = run_sync(db, key, trigger="test", force=True, params=SyncParams(countries=["CMR"], limit=15))
    assert run.status in ("success", "partial"), run.log
    assert run.records_retrieved >= 1 and run.records_imported >= 1
    conn = db.scalar(select(m.SourceConnector).where(m.SourceConnector.key == key))
    assert conn.status in ("operational", "partial")
    n = db.scalar(select(func.count(m.SourceRecord.id)).where(m.SourceRecord.connector_id == conn.id))
    assert n >= 1
    p = db.scalar(select(m.Project).limit(1))
    assert p.country.iso3 == "CMR" and p.ap2i_id.startswith("AP2I-CMR-")


def test_exchange_rates_real_sources(db):
    from app.connectors.fx import refresh_rates

    out = refresh_rates(db, ["CMR"], 2015, 2024)
    assert out["XAF"] >= 5 and out["EUR"] >= 5 and out["XDR"] >= 5


def test_country_codes_match_world_bank_api():
    import httpx

    from app.reference.countries import COUNTRIES

    r = httpx.get("https://api.worldbank.org/v2/country", params={"format": "json", "per_page": 400}, timeout=60)
    wb = {c["id"]: c["iso2Code"] for c in r.json()[1]}
    mismatches = [(c.iso3, c.iso2, wb.get(c.iso3)) for c in COUNTRIES if wb.get(c.iso3) != c.iso2]
    assert mismatches == []


def test_numeric_codes_match_natural_earth():
    import httpx

    from app.reference.countries import COUNTRIES

    topo = httpx.get("https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json", timeout=60).json()
    ids = {g.get("id") for g in topo["objects"]["countries"]["geometries"]}
    missing = [c.iso3 for c in COUNTRIES if c.numeric not in ids]
    # Small island states are absent from the 110m dataset; they are listed, not hidden.
    assert set(missing) <= {"CPV", "COM", "MUS", "SYC", "STP"}, missing
