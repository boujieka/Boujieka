"""ACCESS MAP datasets and the ACCESS OPTIMIZER endpoint.

Uploaded files are untrusted: they are parsed as data (JSON or CSV), size limited, validated against a small
GeoJSON subset and never executed or rendered as HTML."""
from __future__ import annotations

import csv
import io
import json
import uuid
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy import select, text
from sqlalchemy.orm import Session, defer

from ..config import get_settings
from ..db import get_session
from ..deps import Ctx, OrgCtx, current_user, org_ctx
from ..engine.demo import DEMO_LABEL, demo_inputs
from ..engine.inputs import ProjectInputs
from ..engine.optimizer import OptionCosts, Settlement, Weights, compare, demo_settlement
from ..models import CountryProfile, Dataset, ReferenceSource
from ..reference import AFRICA as REF_AFRICA, AFRICA_ISO
from ..services.audit import audit
from ..services.runs import clean

router = APIRouter(tags=["map and optimizer"])

LayerType = Literal["boundaries", "settlements", "grid", "substations", "health", "schools", "markets", "anchors", "minigrids", "constraints", "other"]
Quality = Literal["verified_source", "secondary", "user_assumption", "synthetic_demo"]
GEOM_TYPES = {"Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"}
MAX_FEATURES = 50_000

# The 54 UN member states in Africa (ISO 3166-1 alpha-3); defined with the bundled reference data.
AFRICA = REF_AFRICA


class DatasetMeta(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    layer_type: LayerType
    source_institution: str = Field(min_length=1, max_length=300)
    publication_date: str = Field(min_length=4, max_length=30)
    geographic_coverage: str = Field(min_length=1, max_length=300)
    resolution: str = Field(min_length=1, max_length=100)
    licence: str = Field(min_length=1, max_length=200)
    retrieval_date: date
    quality: Quality
    limitations: str = Field(min_length=1, max_length=5000)


class DatasetIn(DatasetMeta):
    geojson: dict


def _validate_fc(fc: dict) -> int:
    if fc.get("type") != "FeatureCollection" or not isinstance(fc.get("features"), list):
        raise HTTPException(422, "GeoJSON must be a FeatureCollection")
    feats = fc["features"]
    if len(feats) > MAX_FEATURES:
        raise HTTPException(413, f"At most {MAX_FEATURES} features per dataset")
    for i, f in enumerate(feats):
        g = (f or {}).get("geometry") or {}
        if f.get("type") != "Feature" or g.get("type") not in GEOM_TYPES or not isinstance(g.get("coordinates"), list):
            raise HTTPException(422, f"Feature {i} is not a supported GeoJSON feature")
        props = f.get("properties") or {}
        if not isinstance(props, dict):
            raise HTTPException(422, f"Feature {i} has invalid properties")
    return len(feats)


def dataset_out(d: Dataset, with_geo: bool = False) -> dict:
    out = {k: getattr(d, k) for k in ("title", "layer_type", "source_institution", "publication_date", "geographic_coverage",
                                      "resolution", "licence", "quality", "limitations", "feature_count", "is_demo")}
    out.update(id=str(d.id), retrieval_date=d.retrieval_date.isoformat(), scope="platform" if d.org_id is None else "organisation",
               source_key=d.source_key, source_url=d.source_url, source_version=d.source_version, attribution=d.attribution)
    if with_geo:
        out["geojson"] = d.geojson
    return out


@router.get("/api/countries")
def countries(s: Session = Depends(get_session)):
    """The 54 countries. `has_profile` is true when the bundled public reference data has been ingested for the
    country; `bbox` ([west, south, east, north]) comes from the Natural Earth admin 0 boundary, or is null."""
    profiles = {p.iso3: p.bbox for p in s.execute(select(CountryProfile.iso3, CountryProfile.bbox)).all()}
    return [{"iso3": a, "name": n, "has_profile": a in profiles, "bbox": profiles.get(a)} for a, n in AFRICA]


def _iso(iso3: str) -> str:
    code = iso3.upper()
    if code not in AFRICA_ISO:
        raise HTTPException(404, "Country not found")
    return code


def _source_summary(r: ReferenceSource) -> dict:
    rec = r.record
    return {"key": r.key, "kind": r.kind, "title": r.title, "source_institution": r.source_institution,
            "source_title": rec.get("source_title"), "version": rec.get("version"), "publication_date": rec.get("publication_date"),
            "retrieval_date": r.retrieval_date.isoformat(), "licence": r.licence, "attribution": r.attribution, "quality": r.quality,
            "limitations": rec.get("limitations"), "urls": [x.get("pinned_url") or x["url"] for x in rec.get("raw", [])]}


@router.get("/api/countries/{iso3}/profile")
def country_profile(iso3: str, ctx: Ctx = Depends(current_user)):
    """Indicators of the bundled public reference data, each with its year, unit, source, licence and attribution.
    A value that the source does not publish for the country is null (shown as "Data unavailable")."""
    p = ctx.session.get(CountryProfile, _iso(iso3))
    if p is None:
        raise HTTPException(404, "Data unavailable: no public reference data loaded for this country")
    keys = {i["source_key"] for i in p.indicators} | {"ne_admin0_africa", "ne_admin1_africa", "ne_populated_places_africa"}
    srcs = ctx.session.execute(select(ReferenceSource).where(ReferenceSource.key.in_(keys)).order_by(ReferenceSource.key)).scalars().all()
    return {"iso3": p.iso3, "name": p.name, "bbox": p.bbox, "indicators": p.indicators, "admin1_count": p.admin1_count,
            "places_count": p.places_count, "sources": [_source_summary(r) for r in srcs]}


def _platform_features(s: Session, source_key: str, iso3: str) -> dict:
    """Features of one country from a platform dataset, filtered in PostgreSQL (jsonpath) so the full layer is not
    loaded. Platform rows (org_id NULL) are readable by the app role without a tenant context (RLS policy)."""
    d = s.execute(select(Dataset).options(defer(Dataset.geojson))
                  .where(Dataset.source_key == source_key, Dataset.org_id.is_(None))).scalar_one_or_none()
    if d is None:
        raise HTTPException(404, "Data unavailable: the platform dataset is not loaded")
    feats = s.execute(text("SELECT jsonb_path_query_array(geojson -> 'features', '$[*] ? (@.properties.iso3 == $c)', "
                           "jsonb_build_object('c', CAST(:c AS text))) FROM datasets WHERE id = :id"),
                      {"c": iso3, "id": d.id}).scalar_one()
    return {"type": "FeatureCollection", "features": feats or [], "dataset": dataset_out(d)}


@router.get("/api/countries/{iso3}/boundary")
def country_boundary(iso3: str, ctx: Ctx = Depends(current_user)):
    return _platform_features(ctx.session, "ne_admin0_africa", _iso(iso3))


@router.get("/api/countries/{iso3}/admin1")
def country_admin1(iso3: str, ctx: Ctx = Depends(current_user)):
    return _platform_features(ctx.session, "ne_admin1_africa", _iso(iso3))


@router.get("/api/countries/{iso3}/places")
def country_places(iso3: str, ctx: Ctx = Depends(current_user)):
    return _platform_features(ctx.session, "ne_populated_places_africa", _iso(iso3))


@router.get("/api/orgs/{org_id}/datasets")
def list_datasets(ctx: OrgCtx = Depends(org_ctx())):
    """Tenant datasets and platform datasets (org_id NULL, visible to every tenant through RLS)."""
    rows = ctx.session.execute(select(Dataset).options(defer(Dataset.geojson)).order_by(Dataset.created_at.desc())).scalars().all()
    return [dataset_out(d) for d in rows]


@router.get("/api/orgs/{org_id}/datasets/{did}")
def get_dataset(did: uuid.UUID, ctx: OrgCtx = Depends(org_ctx())):
    d = ctx.session.get(Dataset, did)
    if d is None or (d.org_id not in (None, ctx.org.id)):
        raise HTTPException(404, "Dataset not found")
    return dataset_out(d, with_geo=True)


@router.post("/api/orgs/{org_id}/datasets", status_code=201)
def add_dataset(body: DatasetIn, ctx: OrgCtx = Depends(org_ctx("analyst"))):
    raw = json.dumps(body.geojson)
    if len(raw) > get_settings().max_upload_mb * 1_000_000:
        raise HTTPException(413, "Dataset too large")
    n = _validate_fc(body.geojson)
    d = Dataset(org_id=ctx.org.id, feature_count=n, is_demo=ctx.org.is_demo, **body.model_dump())
    ctx.session.add(d)
    ctx.session.flush()
    audit(ctx.session, "upload_dataset", "dataset", d.id, org_id=ctx.org.id, user_id=ctx.user.id, features=n)
    return dataset_out(d)


@router.post("/api/orgs/{org_id}/datasets/csv", status_code=201)
async def add_dataset_csv(meta: str = Form(...), file: UploadFile = File(...), ctx: OrgCtx = Depends(org_ctx("analyst"))):
    """CSV with latitude and longitude columns (names: lat/latitude and lon/lng/longitude); other columns become
    properties."""
    m = DatasetMeta.model_validate_json(meta)
    data = await file.read(get_settings().max_upload_mb * 1_000_000 + 1)
    if len(data) > get_settings().max_upload_mb * 1_000_000:
        raise HTTPException(413, "File too large")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        raise HTTPException(422, "CSV must be UTF-8") from e
    rd = csv.DictReader(io.StringIO(text))
    cols = {c.lower().strip(): c for c in (rd.fieldnames or [])}
    lat = next((cols[c] for c in ("lat", "latitude") if c in cols), None)
    lon = next((cols[c] for c in ("lon", "lng", "longitude") if c in cols), None)
    if not lat or not lon:
        raise HTTPException(422, "CSV needs latitude and longitude columns")
    feats = []
    for i, row in enumerate(rd):
        try:
            y, x = float(row[lat]), float(row[lon])
        except (TypeError, ValueError) as e:
            raise HTTPException(422, f"Row {i + 2}: latitude or longitude not numeric") from e
        if not (-90 <= y <= 90 and -180 <= x <= 180):
            raise HTTPException(422, f"Row {i + 2}: coordinates out of range")
        props = {k: v for k, v in row.items() if k not in (lat, lon)}
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [x, y]}, "properties": props})
        if len(feats) > MAX_FEATURES:
            raise HTTPException(413, f"At most {MAX_FEATURES} rows")
    fc = {"type": "FeatureCollection", "features": feats}
    d = Dataset(org_id=ctx.org.id, feature_count=len(feats), geojson=fc, is_demo=ctx.org.is_demo, **m.model_dump())
    ctx.session.add(d)
    ctx.session.flush()
    audit(ctx.session, "upload_dataset", "dataset", d.id, org_id=ctx.org.id, user_id=ctx.user.id, features=len(feats))
    return dataset_out(d)


class CompareIn(BaseModel):
    settlement: Settlement
    costs: OptionCosts
    weights: Weights = Weights()


@router.post("/api/optimizer/compare")
def optimizer_compare(body: CompareIn, ctx: Ctx = Depends(current_user)):
    return clean(compare(body.settlement, body.costs, body.weights))


@router.get("/api/optimizer/demo")
def optimizer_demo(ctx: Ctx = Depends(current_user)):
    s, c = demo_settlement()
    return {"label": "SYNTHETIC DEMO DATA: illustrative settlement and placeholder costs",
            "settlement": s.model_dump(), "costs": c.model_dump(), "weights": Weights().model_dump()}


@router.get("/api/engine/demo-inputs")
def engine_demo_inputs(ctx: Ctx = Depends(current_user)):
    return {"label": DEMO_LABEL, "inputs": demo_inputs().model_dump(mode="json")}


@router.get("/api/engine/input-schema")
def engine_input_schema(ctx: Ctx = Depends(current_user)):
    return ProjectInputs.model_json_schema()
