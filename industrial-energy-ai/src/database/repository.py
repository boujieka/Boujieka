"""Data access layer: engine/session handling and CRUD for industrial sites."""

from __future__ import annotations

import hashlib
import logging
import math
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path

from sqlalchemy import create_engine, func, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import UPLOAD_DIR, get_settings
from src.database.models import AppSetting, Base, Dataset, LoadProfileRecord, Project, ResultRecord

log = logging.getLogger(__name__)

PROJECT_FIELDS = (
    "code", "company_name", "sector", "country", "region", "latitude", "longitude", "annual_demand_kwh",
    "peak_demand_kw", "installed_capacity_kw", "existing_technologies", "annual_fuel_l", "operating_hours",
    "annual_energy_cost", "currency", "data_sources", "data_quality", "is_synthetic", "notes", "assumptions",
)


@lru_cache(maxsize=8)
def get_engine(url: str | None = None) -> Engine:
    url = url or get_settings().database_url
    if url.startswith("sqlite:///") and ":memory:" not in url:
        Path(url[len("sqlite:///"):]).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(url, future=True)
    Base.metadata.create_all(engine)
    return engine


@contextmanager
def session_scope(url: str | None = None):
    session = sessionmaker(bind=get_engine(url), expire_on_commit=False)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _clean(data: dict) -> dict:
    out = {k: v for k, v in data.items() if k in PROJECT_FIELDS}
    for k, v in list(out.items()):
        if isinstance(v, float) and math.isnan(v):
            out[k] = None
    return out


def next_code(session: Session, prefix: str = "IEA") -> str:
    n = session.scalar(select(func.count(Project.id))) or 0
    while True:
        n += 1
        code = f"{prefix}-{n:04d}"
        if not session.scalar(select(Project.id).where(Project.code == code)):
            return code


def create_project(session: Session, data: dict) -> Project:
    data = _clean(data)
    if not data.get("company_name"):
        raise ValueError("Company name is required.")
    if not data.get("sector"):
        raise ValueError("Industry sector is required.")
    data.setdefault("code", next_code(session))
    if session.scalar(select(Project.id).where(Project.code == data["code"])):
        raise ValueError(f"Project ID {data['code']} already exists.")
    project = Project(**data)
    session.add(project)
    session.flush()
    log.info("Created project %s", project.code)
    return project


def update_project(session: Session, project_id: int, data: dict) -> Project:
    project = session.get(Project, project_id)
    if project is None:
        raise ValueError("Project not found.")
    for key, value in _clean(data).items():
        if key == "code" and value != project.code and session.scalar(select(Project.id).where(Project.code == value)):
            raise ValueError(f"Project ID {value} already exists.")
        setattr(project, key, value)
    session.flush()
    return project


def duplicate_project(session: Session, project_id: int) -> Project:
    src = session.get(Project, project_id)
    if src is None:
        raise ValueError("Project not found.")
    data = {f: getattr(src, f) for f in PROJECT_FIELDS if f != "code"}
    data["company_name"] = f"{src.company_name} (copy)"
    copy = create_project(session, data)
    for prof in src.profiles:
        session.add(LoadProfileRecord(project_id=copy.id, kind=prof.kind, is_synthetic=prof.is_synthetic, active=prof.active,
                                      source=prof.source, payload=prof.payload, validation=prof.validation))
    session.flush()
    return copy


def archive_project(session: Session, project_id: int, archived: bool = True) -> Project:
    project = session.get(Project, project_id)
    if project is None:
        raise ValueError("Project not found.")
    project.archived = archived
    session.flush()
    return project


def list_projects(session: Session, include_archived: bool = False) -> list[Project]:
    stmt = select(Project).order_by(Project.code)
    if not include_archived:
        stmt = stmt.where(Project.archived.is_(False))
    return list(session.scalars(stmt))


def get_project(session: Session, project_id: int) -> Project | None:
    return session.get(Project, project_id)


def save_profile(session: Session, project_id: int, payload: dict, kind: str = "load", is_synthetic: bool = True,
                 source: str = "", validation: dict | None = None) -> LoadProfileRecord:
    for old in session.scalars(select(LoadProfileRecord).where(LoadProfileRecord.project_id == project_id, LoadProfileRecord.kind == kind)):
        old.active = False
    rec = LoadProfileRecord(project_id=project_id, kind=kind, is_synthetic=is_synthetic, active=True, source=source,
                            payload=payload, validation=validation or {})
    session.add(rec)
    session.flush()
    return rec


def active_profile(session: Session, project_id: int, kind: str = "load") -> LoadProfileRecord | None:
    return session.scalar(select(LoadProfileRecord).where(LoadProfileRecord.project_id == project_id, LoadProfileRecord.kind == kind,
                                                          LoadProfileRecord.active.is_(True)).order_by(LoadProfileRecord.id.desc()))


def clear_profile(session: Session, project_id: int, kind: str = "load") -> None:
    for old in session.scalars(select(LoadProfileRecord).where(LoadProfileRecord.project_id == project_id, LoadProfileRecord.kind == kind)):
        old.active = False


def store_upload(session: Session, project_id: int, filename: str, content: bytes, category: str, validation: dict | None = None) -> Dataset:
    digest = hashlib.sha256(content).hexdigest()
    safe = "".join(c for c in Path(filename).name if c.isalnum() or c in "._-") or "upload.bin"
    folder = UPLOAD_DIR / str(project_id)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{digest[:12]}_{safe}"
    path.write_bytes(content)
    ds = Dataset(project_id=project_id, filename=safe, category=category, sha256=digest, stored_path=str(path), validation=validation or {})
    session.add(ds)
    session.flush()
    return ds


def save_result(session: Session, project_id: int, kind: str, payload: dict, assumptions: dict) -> ResultRecord:
    rec = ResultRecord(project_id=project_id, kind=kind, payload=payload, assumptions_snapshot=assumptions)
    session.add(rec)
    session.flush()
    return rec


def latest_result(session: Session, project_id: int, kind: str) -> ResultRecord | None:
    return session.scalar(select(ResultRecord).where(ResultRecord.project_id == project_id, ResultRecord.kind == kind)
                          .order_by(ResultRecord.id.desc()))


def get_setting(session: Session, key: str, default: dict | None = None) -> dict | None:
    rec = session.get(AppSetting, key)
    return rec.value if rec else default


def set_setting(session: Session, key: str, value: dict) -> None:
    rec = session.get(AppSetting, key)
    if rec:
        rec.value = value
    else:
        session.add(AppSetting(key=key, value=value))
    session.flush()
