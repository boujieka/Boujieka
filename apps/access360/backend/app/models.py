"""ORM models. Tables marked TENANT carry org_id and are protected by row level security (see migrations)."""
from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base

JSONType = JSON().with_variant(JSONB(), "postgresql")


def now() -> datetime:
    return datetime.now(timezone.utc)


def uid() -> uuid.UUID:
    return uuid.uuid4()


class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uid)
    name: Mapped[str] = mapped_column(String(200))
    kind: Mapped[str] = mapped_column(String(30))  # individual | developer | investor | government | accredited
    accreditation_status: Mapped[str] = mapped_column(String(20), default="not_applicable")  # not_applicable | pending | verified | rejected
    plan: Mapped[str] = mapped_column(String(30), default="free_explorer")
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uid)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(100))
    full_name: Mapped[str] = mapped_column(String(200))
    locale: Mapped[str] = mapped_column(String(5), default="en")
    is_superadmin: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_secret: Mapped[str | None] = mapped_column(String(64), nullable=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Membership(Base):
    __tablename__ = "memberships"
    __table_args__ = (UniqueConstraint("user_id", "org_id"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uid)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(20))  # owner | admin | analyst | viewer


class Project(Base):  # TENANT
    __tablename__ = "projects"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uid)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    country: Mapped[str] = mapped_column(String(100))
    technology: Mapped[str] = mapped_column(String(60), default="solar_battery_minigrid")
    stage: Mapped[str] = mapped_column(String(30), default="screening")  # screening | feasibility | development | financing | construction | operation
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    geometry: Mapped[dict | None] = mapped_column(JSONType, nullable=True)  # GeoJSON
    inputs: Mapped[dict | None] = mapped_column(JSONType, nullable=True)  # ProjectInputs
    inputs_version: Mapped[int] = mapped_column(Integer, default=0)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    marketplace_visible: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)


class ModelRun(Base):  # TENANT
    __tablename__ = "model_runs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uid)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    engine_version: Mapped[str] = mapped_column(String(20))
    inputs_version: Mapped[int] = mapped_column(Integer)
    inputs_snapshot: Mapped[dict] = mapped_column(JSONType)
    inputs_sha256: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(30))
    metrics: Mapped[dict] = mapped_column(JSONType)
    checks: Mapped[list] = mapped_column(JSONType)
    warnings: Mapped[list] = mapped_column(JSONType)
    missing_inputs: Mapped[list] = mapped_column(JSONType)
    annual: Mapped[dict] = mapped_column(JSONType)
    sources_uses: Mapped[dict] = mapped_column(JSONType)
    quarterly: Mapped[dict] = mapped_column(JSONType)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Milestone(Base):  # TENANT
    __tablename__ = "milestones"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uid)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(40), default="other")
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open")  # open | in_progress | done | blocked
    owner_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class GeneratedDocument(Base):  # TENANT
    __tablename__ = "generated_documents"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uid)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("model_runs.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(String(30))  # teaser_pdf | model_xlsx
    engine_version: Mapped[str] = mapped_column(String(20))
    inputs_sha256: Mapped[str] = mapped_column(String(64))
    file_sha256: Mapped[str] = mapped_column(String(64))
    storage_key: Mapped[str] = mapped_column(String(300))
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Dataset(Base):  # TENANT (org_id NULL = platform dataset visible to all)
    __tablename__ = "datasets"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uid)
    org_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(300))
    layer_type: Mapped[str] = mapped_column(String(40))  # settlements | grid | health | schools | anchors | constraints | other
    source_institution: Mapped[str] = mapped_column(String(300))
    publication_date: Mapped[str] = mapped_column(String(30))
    geographic_coverage: Mapped[str] = mapped_column(String(300))
    resolution: Mapped[str] = mapped_column(String(100))
    licence: Mapped[str] = mapped_column(String(200))
    retrieval_date: Mapped[date] = mapped_column(Date)
    quality: Mapped[str] = mapped_column(String(30))  # verified_source | secondary | user_assumption | synthetic_demo
    limitations: Mapped[str] = mapped_column(Text)
    feature_count: Mapped[int] = mapped_column(Integer, default=0)
    geojson: Mapped[dict] = mapped_column(JSONType)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    # provenance of platform reference datasets (NULL for tenant uploads); see app/ingest_public.py
    source_key: Mapped[str | None] = mapped_column(String(60), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_version: Mapped[str | None] = mapped_column(String(300), nullable=True)
    attribution: Mapped[str | None] = mapped_column(Text, nullable=True)


class ReferenceSource(Base):  # platform reference data: written by the owner role only, SELECT for the app role
    __tablename__ = "reference_sources"
    key: Mapped[str] = mapped_column(String(60), primary_key=True)
    kind: Mapped[str] = mapped_column(String(20))  # dataset | indicators
    title: Mapped[str] = mapped_column(String(300))
    source_institution: Mapped[str] = mapped_column(String(300))
    licence: Mapped[str] = mapped_column(String(300))
    attribution: Mapped[str] = mapped_column(Text)
    quality: Mapped[str] = mapped_column(String(30))
    retrieval_date: Mapped[date] = mapped_column(Date)
    record: Mapped[dict] = mapped_column(JSONType)  # the full manifest entry (URLs, commits, SHA-256, transformations)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class CountryProfile(Base):  # platform reference data: written by the owner role only, SELECT for the app role
    __tablename__ = "country_profiles"
    iso3: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    bbox: Mapped[list | None] = mapped_column(JSONType, nullable=True)  # [west, south, east, north] of the admin 0 boundary
    indicators: Mapped[list] = mapped_column(JSONType)  # [{key, title, unit, value, year, source, source_key, ...}]
    admin1_count: Mapped[int] = mapped_column(Integer, default=0)
    places_count: Mapped[int] = mapped_column(Integer, default=0)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class AuditLog(Base):  # TENANT (org_id NULL for account level events)
    __tablename__ = "audit_logs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uid)
    org_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    action: Mapped[str] = mapped_column(String(60))
    entity: Mapped[str] = mapped_column(String(60))
    entity_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    detail: Mapped[dict] = mapped_column(JSONType, default=dict)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


TENANT_TABLES = ("projects", "model_runs", "milestones", "generated_documents", "datasets", "audit_logs")
