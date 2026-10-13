"""Spatial queries on PostGIS: project context and radius screening.

Results come only from datasets the tenant can see (platform reference data and its own uploads, through row level
security). Every result carries the dataset's source and licence. Natural Earth populated places are a cartographic
selection, not a settlement inventory, and the response says so.
"""
from __future__ import annotations

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import text

from ..deps import OrgCtx, org_ctx
from ..models import Project

router = APIRouter(prefix="/api/orgs/{org_id}", tags=["spatial"])

PLACES_NOTE = ("Natural Earth populated places are selected for 1:10m cartography; they are not a complete settlement "
               "inventory and their populations are estimates as published.")


class ScreeningIn(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    radius_km: float = Field(25, gt=0, le=200)
    dataset_ids: list[uuid.UUID] | None = None
    max_features: int = Field(50, ge=0, le=500)


def _src(row) -> dict:
    return {"dataset_id": str(row.dataset_id), "title": row.title, "source_institution": row.source_institution,
            "licence": row.licence, "quality": row.quality, "scope": "platform" if row.org_id is None else "organisation"}


def _context(ctx: OrgCtx, lat: float, lon: float, radius_km: float) -> dict:
    s = ctx.session
    pt = "ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)"
    prm = {"lat": lat, "lon": lon, "r": radius_km * 1000.0}
    admin = {}
    for level, key in (("admin0", "name_long"), ("admin1", "adm1_code")):
        row = s.execute(text(f"""
            SELECT f.properties, d.id AS dataset_id, d.title, d.source_institution, d.licence, d.quality, d.org_id
            FROM dataset_features f JOIN datasets d ON d.id = f.dataset_id
            WHERE d.org_id IS NULL AND d.layer_type = 'boundaries' AND f.properties ? :key AND ST_Intersects(f.geom, {pt})
            LIMIT 1"""), {**prm, "key": key}).first()
        admin[level] = None if row is None else {"properties": row.properties, "source": _src(row)}
    places = s.execute(text(f"""
        SELECT f.properties, ST_Distance(f.geom::geography, {pt}::geography) AS dist_m,
               d.id AS dataset_id, d.title, d.source_institution, d.licence, d.quality, d.org_id
        FROM dataset_features f JOIN datasets d ON d.id = f.dataset_id
        WHERE d.org_id IS NULL AND d.layer_type = 'settlements' AND f.properties ? 'ne_id'
          AND ST_DWithin(f.geom::geography, {pt}::geography, :r)
        ORDER BY dist_m LIMIT 10"""), prm).all()
    layers = s.execute(text(f"""
        SELECT d.id AS dataset_id, d.title, d.source_institution, d.licence, d.quality, d.org_id, d.layer_type,
               count(*) AS n, min(ST_Distance(f.geom::geography, {pt}::geography)) AS nearest_m
        FROM dataset_features f JOIN datasets d ON d.id = f.dataset_id
        WHERE d.org_id IS NOT NULL AND ST_DWithin(f.geom::geography, {pt}::geography, :r)
        GROUP BY d.id, d.title, d.source_institution, d.licence, d.quality, d.org_id, d.layer_type"""), prm).all()
    return {
        "point": {"latitude": lat, "longitude": lon}, "radius_km": radius_km,
        "country": admin["admin0"], "admin1": admin["admin1"],
        "nearest_places": [{"name": r.properties.get("name"), "admin1": r.properties.get("adm1name"),
                            "population_max_estimate": r.properties.get("pop_max"), "distance_km": round(r.dist_m / 1000.0, 2),
                            "source": _src(r)} for r in places],
        "places_note": PLACES_NOTE,
        "organisation_layers": [{"layer_type": r.layer_type, "features_within_radius": r.n,
                                 "nearest_km": round(r.nearest_m / 1000.0, 2), "source": _src(r)} for r in layers],
        "unavailable": [x for x, v in (("country", admin["admin0"]), ("admin1", admin["admin1"])) if v is None],
    }


@router.get("/projects/{pid}/context")
def project_context(pid: uuid.UUID, radius_km: float = Query(25, gt=0, le=200), ctx: OrgCtx = Depends(org_ctx())):
    p = ctx.session.get(Project, pid)
    if p is None or p.org_id != ctx.org.id:
        raise HTTPException(404, "Project not found")
    if p.latitude is None or p.longitude is None:
        return {"point": None, "message": "Data unavailable: the project has no location"}
    return _context(ctx, p.latitude, p.longitude, radius_km)


@router.post("/screening")
def screening(body: ScreeningIn, ctx: OrgCtx = Depends(org_ctx())):
    """Features of visible datasets within a radius of a point, with counts and nearest distance per dataset."""
    pt = "ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)"
    prm = {"lat": body.latitude, "lon": body.longitude, "r": body.radius_km * 1000.0, "lim": body.max_features}
    flt = ""
    if body.dataset_ids:
        flt = "AND d.id = ANY(:ids)"
        prm["ids"] = [str(x) for x in body.dataset_ids]
    s = ctx.session
    summary = s.execute(text(f"""
        SELECT d.id AS dataset_id, d.title, d.source_institution, d.licence, d.quality, d.org_id, d.layer_type,
               count(*) AS n, min(ST_Distance(f.geom::geography, {pt}::geography)) AS nearest_m
        FROM dataset_features f JOIN datasets d ON d.id = f.dataset_id
        WHERE ST_DWithin(f.geom::geography, {pt}::geography, :r) {flt}
        GROUP BY d.id, d.title, d.source_institution, d.licence, d.quality, d.org_id, d.layer_type
        ORDER BY nearest_m"""), prm).all()
    feats = s.execute(text(f"""
        SELECT ST_AsGeoJSON(f.geom)::text AS g, f.properties, d.id AS dataset_id,
               ST_Distance(f.geom::geography, {pt}::geography) AS dist_m
        FROM dataset_features f JOIN datasets d ON d.id = f.dataset_id
        WHERE ST_DWithin(f.geom::geography, {pt}::geography, :r) {flt} AND GeometryType(f.geom) IN ('POINT', 'MULTIPOINT')
        ORDER BY dist_m LIMIT :lim"""), prm).all()
    return {
        "point": {"latitude": body.latitude, "longitude": body.longitude}, "radius_km": body.radius_km,
        "datasets": [{"layer_type": r.layer_type, "features_within_radius": r.n, "nearest_km": round(r.nearest_m / 1000.0, 2),
                      "source": _src(r)} for r in summary],
        "point_features": {"type": "FeatureCollection", "features": [
            {"type": "Feature", "geometry": json.loads(r.g),
             "properties": {**(r.properties or {}), "_dataset_id": str(r.dataset_id), "_distance_km": round(r.dist_m / 1000.0, 3)}}
            for r in feats]},
        "places_note": PLACES_NOTE,
    }
