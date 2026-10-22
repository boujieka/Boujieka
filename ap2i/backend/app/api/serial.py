"""Serialization helpers. Decimals are returned as strings (exact), dates as ISO strings."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Project


def j(v):
    if isinstance(v, Decimal):
        return str(v)
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    return v


def row(obj, fields: list[str]) -> dict:
    return {f: j(getattr(obj, f)) for f in fields}


PROJECT_SUMMARY = ["id", "ap2i_id", "title", "status", "operational_status", "verification_status", "data_nature",
                   "original_approval_date", "implementation_start_date", "original_completion_date",
                   "actual_completion_date", "executing_agency", "last_source_update_at"]


def project_summary(p: Project) -> dict:
    d = row(p, PROJECT_SUMMARY)
    d["country"] = p.country.iso3 if p.country else None
    d["sector"] = {"code": p.sector.code, "name_en": p.sector.name_en, "name_fr": p.sector.name_fr} if p.sector else None
    d["region"] = {"code": p.region.code, "name_fr": p.region.name_fr, "name_en": p.region.name_en} if p.region else None
    d["partners"] = sorted({a.partner.short_name for a in p.agreements if a.partner})
    d["private"] = p.tenant_id is not None
    return d


def missing(d: dict, fields: list[str]) -> list[str]:
    return [f for f in fields if d.get(f) in (None, "", [])]


def db_noop(_: Session) -> None:  # pragma: no cover
    return None
