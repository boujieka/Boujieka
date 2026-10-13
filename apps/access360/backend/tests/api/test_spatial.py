"""PostGIS queries. Ground truth is computed in the test from the bundled Natural Earth files, not typed in."""
import json
import math
from pathlib import Path

from tests.api.test_api import new_client, org_id, register

PD = Path(__file__).resolve().parents[2] / "app" / "public_data"


def _ingest():
    from app.ingest_public import ingest
    ingest()


def _haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def test_project_context_from_public_layers(db_ready):
    _ingest()
    places = json.loads((PD / "ne_populated_places_africa.geojson").read_text())["features"]
    target = next(f for f in places if f["properties"].get("iso3") == "KEN" and f["properties"].get("name") == "Nairobi")
    lon, lat = target["geometry"]["coordinates"]
    c = new_client()
    u = register(c)
    oid = org_id(u)
    pid = c.post(f"/api/orgs/{oid}/projects", json={"name": "Near Nairobi", "country": "Kenya", "latitude": lat + 0.05,
                                                     "longitude": lon}).json()["id"]
    ctx = c.get(f"/api/orgs/{oid}/projects/{pid}/context?radius_km=30").json()
    assert ctx["country"]["properties"]["iso3"] == "KEN"
    assert ctx["admin1"] is not None and ctx["admin1"]["source"]["licence"]
    nearest = ctx["nearest_places"][0]
    assert nearest["name"] == "Nairobi"
    # PostGIS measures on the WGS84 ellipsoid; a spherical haversine differs by up to about 0.6% (north-south near the
    # equator), so agreement within 1% confirms the units and the geography cast
    assert abs(nearest["distance_km"] - _haversine_km(lat + 0.05, lon, lat, lon)) / nearest["distance_km"] < 0.01
    assert "not a complete settlement inventory" in ctx["places_note"]


def test_screening_sees_own_uploads_but_not_other_tenants(db_ready):
    _ingest()
    a, b = new_client(), new_client()
    ua, ub = register(a), register(b)
    meta = {"title": "Clinics", "layer_type": "health", "source_institution": "Own survey", "publication_date": "2026",
            "geographic_coverage": "Test", "resolution": "Point", "licence": "Internal", "retrieval_date": "2026-10-13",
            "quality": "user_assumption", "limitations": "Test"}
    fc = {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [36.8, -1.3]},
                                                      "properties": {"n": 1}}]}
    assert a.post(f"/api/orgs/{org_id(ua)}/datasets", json={**meta, "geojson": fc}).status_code == 201
    q = {"latitude": -1.3, "longitude": 36.81, "radius_km": 5}
    ra = a.post(f"/api/orgs/{org_id(ua)}/screening", json=q).json()
    rb = b.post(f"/api/orgs/{org_id(ub)}/screening", json=q).json()
    assert any(d["source"]["title"] == "Clinics" for d in ra["datasets"])
    assert not any(d["source"]["title"] == "Clinics" for d in rb["datasets"])  # RLS on the feature table
    clinic = [f for f in ra["point_features"]["features"] if f["properties"].get("n") == 1][0]
    assert 1.0 < clinic["properties"]["_distance_km"] < 1.3
