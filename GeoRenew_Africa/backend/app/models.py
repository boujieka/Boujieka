"""Modèle relationnel P1.

Toutes les géométries sont stockées en EPSG:4326 (affichage, échange). Les mesures sont faites
par le moteur dans un SCR métrique (``app.geo.engine``), jamais sur ces colonnes.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.geomtype import GeomType

TECHNOLOGIES = ("pv", "eolien", "bess", "hybride")
DATASET_CATEGORIES = (
    "limite_site",
    "exclusion",
    "contrainte",
    "cadastre_officiel",
    "releve_qualifie",
    "reseau_electrique",
    "etude_reseau",
    "accord_gestionnaire",
    "autre",
)
DATA_NATURES = ("observee", "modelisee", "hypothese", "inconnue")
RULE_KINDS = ("exclusion_stricte", "contrainte_indicative")
JUSTIFICATION_TYPES = (
    "aucun_buffer",
    "hypothese_utilisateur",
    "texte_reglementaire_cite",
    "norme_technique_citee",
    "etude_terrain",
)
LAND_STATUSES = ("inconnu", "declare_non_verifie", "verifie_sur_piece")
GRID_STATUSES = ("inconnu", "etude_en_cours", "raccordement_confirme")

# Catégories de jeux de données acceptées comme pièces justificatives
LAND_EVIDENCE = ("cadastre_officiel", "releve_qualifie")
GRID_EVIDENCE = ("etude_reseau", "accord_gestionnaire")


def _enum(values: tuple[str, ...], name: str) -> Enum:
    return Enum(*values, name=name, native_enum=False, create_constraint=True, length=40)


def _now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


class Timestamped:
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now, server_default=func.now())


class Organization(Timestamped, Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)


class User(Timestamped, Base):
    """Compte utilisateur. P1 : table prête, authentification NON implémentée (voir docs)."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"))
    email: Mapped[str] = mapped_column(String(320), unique=True)
    display_name: Mapped[str] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(_enum(("lecteur", "analyste", "administrateur"), "user_role"), default="lecteur")


class Project(Timestamped, Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(String(200))
    country_iso3: Mapped[str] = mapped_column(String(3))
    technology: Mapped[str] = mapped_column(_enum(TECHNOLOGIES, "technology"))
    description: Mapped[str] = mapped_column(Text, default="")
    is_fictional: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    sites: Mapped[list[Site]] = relationship(back_populates="project", cascade="all, delete-orphan")
    datasets: Mapped[list[Dataset]] = relationship(back_populates="project", cascade="all, delete-orphan")
    rules: Mapped[list[ConstraintRule]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Dataset(Timestamped, Base):
    """Jeu de données fourni par l'utilisateur, avec sa provenance (CLAUDE.md §3)."""

    __tablename__ = "datasets"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(_enum(DATASET_CATEGORIES, "dataset_category"))
    nature: Mapped[str] = mapped_column(_enum(DATA_NATURES, "data_nature"), default="inconnue")
    source_name: Mapped[str] = mapped_column(String(300), default="")
    source_url: Mapped[str] = mapped_column(String(1000), default="")
    licence: Mapped[str] = mapped_column(String(300), default="")
    producer: Mapped[str] = mapped_column(String(300), default="")
    reference_date: Mapped[dt.date | None] = mapped_column(Date)
    horizontal_accuracy_m: Mapped[float | None] = mapped_column(Float)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(Text, default="")

    project: Mapped[Project] = relationship(back_populates="datasets")
    versions: Mapped[list[DatasetVersion]] = relationship(
        back_populates="dataset", cascade="all, delete-orphan", order_by="DatasetVersion.version_no"
    )

    __table_args__ = (CheckConstraint("horizontal_accuracy_m IS NULL OR horizontal_accuracy_m >= 0", name="ck_dataset_accuracy"),)

    @property
    def latest_version(self) -> DatasetVersion | None:
        return self.versions[-1] if self.versions else None


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"
    id: Mapped[int] = mapped_column(primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"), index=True)
    version_no: Mapped[int] = mapped_column(Integer)
    sha256: Mapped[str] = mapped_column(String(64))
    original_filename: Mapped[str] = mapped_column(String(300))
    file_format: Mapped[str] = mapped_column(String(30))
    source_crs: Mapped[str] = mapped_column(String(300))
    crs_origin: Mapped[str] = mapped_column(String(40))
    feature_count: Mapped[int] = mapped_column(Integer)
    geometry_types: Mapped[list[str]] = mapped_column(JSON, default=list)
    bbox: Mapped[list[float] | None] = mapped_column(JSON)
    warnings: Mapped[list[str]] = mapped_column(JSON, default=list)
    imported_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now, server_default=func.now())

    dataset: Mapped[Dataset] = relationship(back_populates="versions")
    features: Mapped[list[Feature]] = relationship(
        back_populates="version", cascade="all, delete-orphan", order_by="Feature.feature_index"
    )

    __table_args__ = (UniqueConstraint("dataset_id", "version_no", name="uq_dataset_version"),)


class Feature(Base):
    __tablename__ = "features"
    id: Mapped[int] = mapped_column(primary_key=True)
    dataset_version_id: Mapped[int] = mapped_column(ForeignKey("dataset_versions.id", ondelete="CASCADE"), index=True)
    feature_index: Mapped[int] = mapped_column(Integer)
    geom: Mapped[Any] = mapped_column(GeomType())
    properties: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    version: Mapped[DatasetVersion] = relationship(back_populates="features")


class Site(Timestamped, Base):
    __tablename__ = "sites"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    boundary: Mapped[Any] = mapped_column(GeomType())
    # Provenance de la limite : jeu de données importé, ou tracé manuel.
    boundary_dataset_version_id: Mapped[int | None] = mapped_column(
        ForeignKey("dataset_versions.id", ondelete="SET NULL")
    )
    boundary_source: Mapped[str] = mapped_column(String(300), default="")
    boundary_accuracy_m: Mapped[float | None] = mapped_column(Float)
    land_status: Mapped[str] = mapped_column(_enum(LAND_STATUSES, "land_status"), default="inconnu")
    land_evidence_dataset_id: Mapped[int | None] = mapped_column(ForeignKey("datasets.id", ondelete="SET NULL"))
    grid_status: Mapped[str] = mapped_column(_enum(GRID_STATUSES, "grid_status"), default="inconnu")
    grid_evidence_dataset_id: Mapped[int | None] = mapped_column(ForeignKey("datasets.id", ondelete="SET NULL"))
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    project: Mapped[Project] = relationship(back_populates="sites")
    analyses: Mapped[list[AnalysisRun]] = relationship(
        back_populates="site", cascade="all, delete-orphan", order_by="AnalysisRun.id"
    )


class ConstraintRule(Timestamped, Base):
    __tablename__ = "constraint_rules"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(200))
    kind: Mapped[str] = mapped_column(_enum(RULE_KINDS, "rule_kind"))
    buffer_m: Mapped[float] = mapped_column(Float, default=0.0)
    justification_type: Mapped[str] = mapped_column(_enum(JUSTIFICATION_TYPES, "justification_type"))
    justification: Mapped[str] = mapped_column(Text, default="")
    weight: Mapped[float | None] = mapped_column(Float)  # réservé au scoring multicritère (non implémenté en P1)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    project: Mapped[Project] = relationship(back_populates="rules")
    dataset: Mapped[Dataset] = relationship()

    __table_args__ = (CheckConstraint("buffer_m >= 0", name="ck_rule_buffer"),)


class AnalysisRun(Base):
    """Exécution du moteur. Conserve entrées (instantané + empreinte), paramètres et sorties."""

    __tablename__ = "analysis_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now, server_default=func.now())
    status: Mapped[str] = mapped_column(String(20), default="termine")
    input_hash: Mapped[str] = mapped_column(String(64), index=True)
    inputs: Mapped[dict[str, Any]] = mapped_column(JSON)
    results: Mapped[dict[str, Any]] = mapped_column(JSON)
    software_version: Mapped[str] = mapped_column(String(40))
    engine_version: Mapped[str] = mapped_column(String(40))
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    actor: Mapped[str] = mapped_column(String(200), default="")

    site: Mapped[Site] = relationship(back_populates="analyses")
    layers: Mapped[list[Layer]] = relationship(back_populates="run", cascade="all, delete-orphan", order_by="Layer.id")


class Layer(Base):
    """Couche géographique produite par une analyse (EPSG:4326)."""

    __tablename__ = "layers"
    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("analysis_runs.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(40))
    rule_id: Mapped[int | None] = mapped_column(Integer)
    area_m2: Mapped[float] = mapped_column(Float)  # mesurée dans le SCR métrique de l'analyse
    geom: Mapped[Any] = mapped_column(GeomType())

    run: Mapped[AnalysisRun] = relationship(back_populates="layers")


class AuditLog(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now, server_default=func.now())
    actor: Mapped[str] = mapped_column(String(200))
    action: Mapped[str] = mapped_column(String(60))
    entity_type: Mapped[str] = mapped_column(String(60))
    entity_id: Mapped[int | None] = mapped_column(Integer)
    project_id: Mapped[int | None] = mapped_column(Integer, index=True)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
