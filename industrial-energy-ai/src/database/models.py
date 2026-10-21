"""SQLAlchemy ORM models (SQLite for the MVP; portable to PostgreSQL - only generic column
types and the JSON type are used)."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)  # human-readable project ID
    company_name: Mapped[str] = mapped_column(String(200))
    sector: Mapped[str] = mapped_column(String(60))
    country: Mapped[str] = mapped_column(String(80), default="Republic of Congo")
    region: Mapped[str] = mapped_column(String(120), default="")
    latitude: Mapped[float] = mapped_column(Float, default=0.0)
    longitude: Mapped[float] = mapped_column(Float, default=0.0)
    annual_demand_kwh: Mapped[float] = mapped_column(Float, default=0.0)
    peak_demand_kw: Mapped[float | None] = mapped_column(Float, nullable=True)
    installed_capacity_kw: Mapped[float] = mapped_column(Float, default=0.0)
    existing_technologies: Mapped[list] = mapped_column(JSON, default=list)
    annual_fuel_l: Mapped[float | None] = mapped_column(Float, nullable=True)
    operating_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    annual_energy_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="XAF")
    data_sources: Mapped[str] = mapped_column(Text, default="")
    data_quality: Mapped[str] = mapped_column(String(1), default="C")  # A..D
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=False)
    archived: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(Text, default="")
    assumptions: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    profiles: Mapped[list["LoadProfileRecord"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    datasets: Mapped[list["Dataset"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    results: Mapped[list["ResultRecord"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class LoadProfileRecord(Base):
    __tablename__ = "load_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    kind: Mapped[str] = mapped_column(String(20), default="load")  # load | solar
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    source: Mapped[str] = mapped_column(Text, default="")
    payload: Mapped[dict] = mapped_column(JSON)  # LoadProfile.to_dict() or solar resource dict
    validation: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    project: Mapped[Project] = relationship(back_populates="profiles")


class Dataset(Base):
    """Uploaded file metadata (the file itself is stored under data/uploads)."""

    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    filename: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(60))
    sha256: Mapped[str] = mapped_column(String(64))
    stored_path: Mapped[str] = mapped_column(Text)
    validation: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    project: Mapped[Project] = relationship(back_populates="datasets")


class ResultRecord(Base):
    """Stored engine outputs (JSON summaries, no hourly arrays) for traceability."""

    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    kind: Mapped[str] = mapped_column(String(40))  # optimisation | finance | sensitivity | baseline
    payload: Mapped[dict] = mapped_column(JSON)
    assumptions_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    project: Mapped[Project] = relationship(back_populates="results")


class AppSetting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(80), primary_key=True)
    value: Mapped[dict] = mapped_column(JSON)
