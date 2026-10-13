"""Bundled public reference data (Natural Earth, Our World in Data, World Bank WDI via a mirror).

Profile values are checked against the source CSV read here with the csv module, independently of
app.reference. When A360_PUBLIC_RAW_DIR points at the raw downloads (layout: owid/owid-energy-data.csv,
wdi/data.csv; see docs/public-data-manifest.md) the raw files are used and their SHA-256 must match the manifest;
otherwise the committed verbatim extracts are used, after checking their SHA-256 against the manifest."""
from __future__ import annotations

import csv
import hashlib
import os
import uuid
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text

from tests.api.test_api import new_client, org_id, register

DATA = Path(__file__).resolve().parents[2] / "app" / "public_data"
CHECK_COUNTRIES = ("KEN", "NGA", "SSD")
META_FIELDS = ("title", "layer_type", "source_institution", "publication_date", "geographic_coverage", "resolution",
               "licence", "retrieval_date", "quality", "limitations", "source_url", "source_version", "attribution")


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def ingested(db_ready):
    from app.ingest_public import ingest
    ingest(os.environ["A360_DATABASE_OWNER_URL"])
    yield


def _source_csv(key: str, derived_name: str, raw_rel: str) -> list[dict]:
    from app.reference import manifest, source
    src = source(key, manifest())
    raw_dir = os.environ.get("A360_PUBLIC_RAW_DIR")
    if raw_dir and (Path(raw_dir) / raw_rel).exists():
        p = Path(raw_dir) / raw_rel
        assert _sha(p) == src["raw"][0]["sha256"], f"raw file {p} differs from the manifest"
    else:
        p = DATA / derived_name
        assert _sha(p) == next(d["sha256"] for d in src["derived"] if d["file"] == derived_name)
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _latest(rows, code_col, code, col, year_col):
    vals = [(int(r[year_col]), r[col]) for r in rows if r[code_col] == code and r[col] != ""]
    if not vals:
        return None, None
    y, v = max(vals)
    return float(v), y


def _snapshot():
    eng = create_engine(os.environ["A360_DATABASE_OWNER_URL"])
    with eng.connect() as c:
        ds = c.execute(text("select id, source_key, feature_count, md5(geojson::text), title, licence from datasets "
                            "where org_id is null order by source_key")).all()
        cp = c.execute(text("select iso3, md5(indicators::text), admin1_count, places_count, ingested_at from country_profiles order by iso3")).all()
        rs = c.execute(text("select key, md5(record::text), ingested_at from reference_sources order by key")).all()
    eng.dispose()
    return ds, cp, rs


def test_ingestion_is_idempotent(ingested):
    from app.ingest_public import ingest
    before = _snapshot()
    assert len(before[0]) == 3 and len(before[1]) == 54 and len(before[2]) == 5
    ingest(os.environ["A360_DATABASE_OWNER_URL"])
    assert _snapshot() == before  # same ids, same content, timestamps untouched when nothing changed


def test_ingestion_refuses_a_tampered_file(ingested, monkeypatch):
    import app.ingest_public as ip
    from app.reference import manifest
    man = manifest()
    man["sources"][0]["derived"][0]["sha256"] = "0" * 64
    monkeypatch.setattr(ip, "manifest", lambda: man)
    with pytest.raises(ip.ChecksumError):
        ip.ingest(os.environ["A360_DATABASE_OWNER_URL"])


def test_profile_values_equal_the_source(ingested):
    owid = _source_csv("owid_energy", "owid_energy_africa.csv", "owid/owid-energy-data.csv")
    wdi = _source_csv("wdi_eg_elc_accs_zs", "wdi_eg_elc_accs_zs_africa.csv", "wdi/data.csv")
    c = new_client()
    register(c)
    for iso in CHECK_COUNTRIES:
        r = c.get(f"/api/countries/{iso}/profile")
        assert r.status_code == 200, r.text
        ind = {i["key"]: i for i in r.json()["indicators"]}
        assert len(ind) == 8
        for key, i in ind.items():
            if key == "access_to_electricity":
                v, y = _latest(wdi, "Country Code", iso, "Value", "Year")
            else:
                v, y = _latest(owid, "iso_code", iso, key, "year")
            assert (i["value"], i["year"]) == (v, y), (iso, key)
            assert i["unit"] and i["source"] and i["licence"] and i["attribution"]
    # a value the source does not publish stays null; it is never filled in
    prof = c.get("/api/countries/SSD/profile").json()
    for i in prof["indicators"]:
        if i["value"] is None:
            assert i["year"] is None


def test_profile_requires_login_and_known_country(ingested):
    c = new_client()
    assert c.get("/api/countries/KEN/profile").status_code == 401
    register(c)
    assert c.get("/api/countries/XXX/profile").status_code == 404
    assert c.get("/api/countries/FRA/admin1").status_code == 404


def test_countries_list_keeps_shape_and_adds_has_profile(ingested):
    c = new_client()
    rows = c.get("/api/countries").json()
    assert len(rows) == 54
    assert all({"iso3", "name", "has_profile"} <= set(r) for r in rows)
    assert all(r["has_profile"] for r in rows)
    ken = next(r for r in rows if r["iso3"] == "KEN")
    w, s, e, n = ken["bbox"]
    assert 33 < w < e < 43 and -5 < s < n < 6  # Kenya's extent


def test_admin1_returns_only_that_country(ingested):
    c = new_client()
    register(c)
    for iso in ("KEN", "SSD", "NGA"):
        fc = c.get(f"/api/countries/{iso}/admin1").json()
        assert fc["type"] == "FeatureCollection" and fc["features"]
        assert {f["properties"]["iso3"] for f in fc["features"]} == {iso}
        assert fc["dataset"]["source_key"] == "ne_admin1_africa"
        prof = c.get(f"/api/countries/{iso}/profile").json()
        assert len(fc["features"]) == prof["admin1_count"]
    b = c.get("/api/countries/KEN/boundary").json()
    assert [f["properties"]["iso3"] for f in b["features"]] == ["KEN"]
    p = c.get("/api/countries/KEN/places").json()
    assert p["features"] and {f["properties"]["iso3"] for f in p["features"]} == {"KEN"}


def test_app_role_cannot_modify_public_data(ingested):
    eng = create_engine(os.environ["A360_DATABASE_URL"])  # app role
    with eng.connect() as conn:
        conn.execute(text("select set_config('app.current_org', :v, true)"), {"v": str(uuid.uuid4())})
        n = conn.execute(text("select count(*) from datasets where org_id is null")).scalar()
        assert n == 3  # readable
        assert conn.execute(text("update datasets set title = 'x' where org_id is null")).rowcount == 0
        assert conn.execute(text("delete from datasets where org_id is null")).rowcount == 0
        conn.rollback()
    with eng.connect() as conn:
        with pytest.raises(Exception):
            conn.execute(text("insert into datasets (id, org_id, title, layer_type, source_institution, publication_date, "
                              "geographic_coverage, resolution, licence, retrieval_date, quality, limitations, feature_count, "
                              "geojson, is_demo, created_at) values (:i, null, 't', 'other', 's', '2026', 'c', 'r', 'l', "
                              "'2026-01-01', 'secondary', 'x', 0, '{}', false, now())"), {"i": str(uuid.uuid4())})
        conn.rollback()
    for stmt in ("update country_profiles set name = 'x'", "delete from country_profiles",
                 "insert into country_profiles (iso3, name, indicators, admin1_count, places_count, ingested_at) values ('XXX', 'x', '[]', 0, 0, now())",
                 "update reference_sources set licence = 'x'", "delete from reference_sources"):
        with eng.connect() as conn:
            with pytest.raises(Exception, match="permission denied"):
                conn.execute(text(stmt))
            conn.rollback()
    with eng.connect() as conn:
        assert conn.execute(text("select count(*) from country_profiles")).scalar() == 54
    eng.dispose()


def test_platform_datasets_visible_to_every_tenant_with_full_metadata(ingested):
    seen = []
    for _ in range(2):
        c = new_client()
        u = register(c)
        rows = [d for d in c.get(f"/api/orgs/{org_id(u)}/datasets").json() if d["scope"] == "platform"]
        assert len(rows) == 3
        for d in rows:
            for k in META_FIELDS:
                assert d[k] not in (None, ""), (d["title"], k)
            assert d["quality"] in ("verified_source", "secondary") and d["is_demo"] is False
            assert d["feature_count"] > 0
        seen.append(sorted(d["id"] for d in rows))
        full = c.get(f"/api/orgs/{org_id(u)}/datasets/{rows[0]['id']}").json()
        assert full["geojson"]["features"]
    assert seen[0] == seen[1]
    # every reference source (including the tabular ones) has its provenance filled in
    eng = create_engine(os.environ["A360_DATABASE_OWNER_URL"])
    with eng.connect() as conn:
        for (rec,) in conn.execute(text("select record from reference_sources")):
            for k in ("source_institution", "source_title", "version", "publication_date", "retrieval_date", "licence",
                      "attribution", "geographic_coverage", "resolution", "quality", "limitations", "raw", "derived", "transformations"):
                assert rec.get(k), (rec["key"], k)
            for r in rec["raw"]:
                assert r["url"].startswith("https://raw.githubusercontent.com/") and len(r["sha256"]) == 64
    eng.dispose()
