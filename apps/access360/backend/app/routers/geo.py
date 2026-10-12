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
from sqlalchemy import select

from ..config import get_settings
from ..deps import Ctx, OrgCtx, current_user, org_ctx
from ..engine.optimizer import OptionCosts, Settlement, Weights, compare, demo_settlement
from ..models import Dataset
from ..services.audit import audit
from ..services.runs import clean

router = APIRouter(tags=["map and optimizer"])

LayerType = Literal["settlements", "grid", "substations", "health", "schools", "markets", "anchors", "minigrids", "constraints", "other"]
Quality = Literal["verified_source", "secondary", "user_assumption", "synthetic_demo"]
GEOM_TYPES = {"Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"}
MAX_FEATURES = 50_000

# The 54 UN member states in Africa (ISO 3166-1 alpha-3), used only for the country selector.
AFRICA = [("DZA", "Algeria"), ("AGO", "Angola"), ("BEN", "Benin"), ("BWA", "Botswana"), ("BFA", "Burkina Faso"),
          ("BDI", "Burundi"), ("CPV", "Cabo Verde"), ("CMR", "Cameroon"), ("CAF", "Central African Republic"), ("TCD", "Chad"),
          ("COM", "Comoros"), ("COG", "Congo"), ("COD", "Democratic Republic of the Congo"), ("CIV", "Côte d'Ivoire"),
          ("DJI", "Djibouti"), ("EGY", "Egypt"), ("GNQ", "Equatorial Guinea"), ("ERI", "Eritrea"), ("SWZ", "Eswatini"),
          ("ETH", "Ethiopia"), ("GAB", "Gabon"), ("GMB", "Gambia"), ("GHA", "Ghana"), ("GIN", "Guinea"), ("GNB", "Guinea-Bissau"),
          ("KEN", "Kenya"), ("LSO", "Lesotho"), ("LBR", "Liberia"), ("LBY", "Libya"), ("MDG", "Madagascar"), ("MWI", "Malawi"),
          ("MLI", "Mali"), ("MRT", "Mauritania"), ("MUS", "Mauritius"), ("MAR", "Morocco"), ("MOZ", "Mozambique"),
          ("NAM", "Namibia"), ("NER", "Niger"), ("NGA", "Nigeria"), ("RWA", "Rwanda"), ("STP", "Sao Tome and Principe"),
          ("SEN", "Senegal"), ("SYC", "Seychelles"), ("SLE", "Sierra Leone"), ("SOM", "Somalia"), ("ZAF", "South Africa"),
          ("SSD", "South Sudan"), ("SDN", "Sudan"), ("TZA", "United Republic of Tanzania"), ("TGO", "Togo"), ("TUN", "Tunisia"),
          ("UGA", "Uganda"), ("ZMB", "Zambia"), ("ZWE", "Zimbabwe")]


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
    out.update(id=str(d.id), retrieval_date=d.retrieval_date.isoformat(), scope="platform" if d.org_id is None else "organisation")
    if with_geo:
        out["geojson"] = d.geojson
    return out


@router.get("/api/countries")
def countries():
    return [{"iso3": a, "name": n} for a, n in AFRICA]


@router.get("/api/orgs/{org_id}/datasets")
def list_datasets(ctx: OrgCtx = Depends(org_ctx())):
    rows = ctx.session.execute(select(Dataset).order_by(Dataset.created_at.desc())).scalars().all()
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
