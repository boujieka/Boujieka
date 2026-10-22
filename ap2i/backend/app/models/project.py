"""Master project registry (Master prompt §14) and its history."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, Money, Pct, Timestamped, utcnow


class IdSequence(Base):
    """Per-country counters used to mint stable AP²I identifiers (AP2I-CMR-ENERGY-000001)."""

    __tablename__ = "id_sequences"

    key: Mapped[str] = mapped_column(String(40), primary_key=True)
    value: Mapped[int] = mapped_column(Integer, default=0)


class Project(Base, Timestamped):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint(
            "physical_progress_pct IS NULL OR (physical_progress_pct >= 0 AND physical_progress_pct <= 100)",
            name="physical_progress_range",
        ),
        CheckConstraint(
            "is_synthetic = false OR data_nature = 'synthetic'", name="synthetic_is_labelled"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    ap2i_id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)
    # Tenant isolation: NULL = public record; otherwise private to that organization.
    tenant_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), index=True)

    title: Mapped[str] = mapped_column(Text)
    title_language: Mapped[str | None] = mapped_column(String(5))
    description: Mapped[str | None] = mapped_column(Text)
    objectives: Mapped[str | None] = mapped_column(Text)
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"), index=True)
    subsector_id: Mapped[int | None] = mapped_column(ForeignKey("subsectors.id"))
    region_id: Mapped[int | None] = mapped_column(ForeignKey("regions.id"))
    funding_type: Mapped[str] = mapped_column(String(40), default="unknown")

    executing_agency: Mapped[str | None] = mapped_column(Text)
    supervising_ministry: Mapped[str | None] = mapped_column(Text)
    implementing_agency: Mapped[str | None] = mapped_column(Text)
    project_owner: Mapped[str | None] = mapped_column(Text)

    original_estimated_cost: Mapped[Decimal | None] = mapped_column(Money)
    revised_estimated_cost: Mapped[Decimal | None] = mapped_column(Money)
    cost_currency: Mapped[str | None] = mapped_column(String(3))

    original_approval_date: Mapped[date | None] = mapped_column(Date, index=True)
    implementation_start_date: Mapped[date | None] = mapped_column(Date)
    original_completion_date: Mapped[date | None] = mapped_column(Date)
    revised_completion_date: Mapped[date | None] = mapped_column(Date)
    actual_completion_date: Mapped[date | None] = mapped_column(Date)
    commissioning_date: Mapped[date | None] = mapped_column(Date)

    status: Mapped[str] = mapped_column(String(20), default="unknown", index=True)
    status_source: Mapped[str | None] = mapped_column(String(200))
    physical_progress_pct: Mapped[Decimal | None] = mapped_column(Pct)
    physical_progress_date: Mapped[date | None] = mapped_column(Date)
    operational_status: Mapped[str] = mapped_column(String(30), default="unknown")
    expected_beneficiaries: Mapped[str | None] = mapped_column(Text)
    actual_beneficiaries: Mapped[str | None] = mapped_column(Text)
    development_results: Mapped[str | None] = mapped_column(Text)

    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")
    verification_status: Mapped[str] = mapped_column(String(20), default="unverified", index=True)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=False)
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_source_update_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Set when this record was merged into another master project (reversible, see ProjectMerge).
    merged_into_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), index=True)

    country = relationship("Country")
    sector = relationship("Sector")
    region = relationship("AdminRegion")
    aliases: Mapped[list["ProjectAlias"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    locations: Mapped[list["ProjectLocation"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    agreements = relationship("FinancingAgreement", back_populates="project")


class ProjectAlias(Base):
    __tablename__ = "project_aliases"
    __table_args__ = (UniqueConstraint("project_id", "alias"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    alias: Mapped[str] = mapped_column(Text)
    language: Mapped[str | None] = mapped_column(String(5))
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))

    project: Mapped[Project] = relationship(back_populates="aliases")


class ProjectLocation(Base):
    """Latitude/longitude as NUMERIC; on PostgreSQL a PostGIS geography column is derived (migration 0001)."""

    __tablename__ = "project_locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    region_id: Mapped[int | None] = mapped_column(ForeignKey("regions.id"))
    place_name: Mapped[str | None] = mapped_column(Text)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    precision: Mapped[str | None] = mapped_column(String(40))
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))

    project: Mapped[Project] = relationship(back_populates="locations")


class ProjectStatusHistory(Base):
    __tablename__ = "project_status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(20))
    previous_status: Mapped[str | None] = mapped_column(String(20))
    effective_date: Mapped[date | None] = mapped_column(Date)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    note: Mapped[str | None] = mapped_column(Text)


class ProjectMilestone(Base):
    __tablename__ = "project_milestones"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(Text)
    planned_date: Mapped[date | None] = mapped_column(Date)
    revised_date: Mapped[date | None] = mapped_column(Date)
    actual_date: Mapped[date | None] = mapped_column(Date)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))


class ImplementationProgress(Base):
    __tablename__ = "implementation_progress"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    report_date: Mapped[date] = mapped_column(Date)
    physical_progress_pct: Mapped[Decimal | None] = mapped_column(Pct)
    financial_progress_pct: Mapped[Decimal | None] = mapped_column(Pct)
    narrative: Mapped[str | None] = mapped_column(Text)
    rating: Mapped[str | None] = mapped_column(Text)
    document_id: Mapped[int | None] = mapped_column(ForeignKey("documents.id"))
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")
    verification_status: Mapped[str] = mapped_column(String(20), default="unverified")


class OperationalStatusObservation(Base):
    __tablename__ = "operational_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(30))
    observed_date: Mapped[date] = mapped_column(Date)
    evidence: Mapped[str | None] = mapped_column(Text)
    document_id: Mapped[int | None] = mapped_column(ForeignKey("documents.id"))
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    verification_status: Mapped[str] = mapped_column(String(20), default="unverified")


class ResultsIndicator(Base):
    __tablename__ = "results_indicators"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    sector_indicator_id: Mapped[int | None] = mapped_column(ForeignKey("sector_indicators.id"))
    name: Mapped[str] = mapped_column(Text)
    unit: Mapped[str | None] = mapped_column(String(60))
    measure: Mapped[str | None] = mapped_column(String(20))  # unit | percentage | nominal | qualitative
    baseline_value: Mapped[Decimal | None] = mapped_column(Money)
    baseline_date: Mapped[date | None] = mapped_column(Date)
    target_value: Mapped[Decimal | None] = mapped_column(Money)
    target_date: Mapped[date | None] = mapped_column(Date)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))


class ResultsObservation(Base):
    __tablename__ = "results_observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    indicator_id: Mapped[int] = mapped_column(ForeignKey("results_indicators.id", ondelete="CASCADE"), index=True)
    value: Mapped[Decimal | None] = mapped_column(Money)
    value_text: Mapped[str | None] = mapped_column(Text)
    period_start: Mapped[date | None] = mapped_column(Date)
    period_end: Mapped[date | None] = mapped_column(Date)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")


class Document(Base, Timestamped):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    tenant_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    title: Mapped[str] = mapped_column(Text)
    doc_type: Mapped[str | None] = mapped_column(String(80))
    url: Mapped[str | None] = mapped_column(Text)
    language: Mapped[str | None] = mapped_column(String(5))
    published_date: Mapped[date | None] = mapped_column(Date)
    storage_key: Mapped[str | None] = mapped_column(Text)
    sha256: Mapped[str | None] = mapped_column(String(64), index=True)
    mime_type: Mapped[str | None] = mapped_column(String(100))
    size_bytes: Mapped[int | None] = mapped_column(Integer)
    extracted_text: Mapped[str | None] = mapped_column(Text)
    injection_flags: Mapped[list] = mapped_column(JSON, default=list)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))


class ProjectRisk(Base, Timestamped):
    __tablename__ = "project_risks"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    category: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(Text)
    rating: Mapped[str | None] = mapped_column(String(30))
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")


class ProjectMerge(Base):
    """History of merges; `reversed_at` set when an authorised reviewer undoes one."""

    __tablename__ = "project_merges"

    id: Mapped[int] = mapped_column(primary_key=True)
    survivor_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    merged_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    match_candidate_id: Mapped[int | None] = mapped_column(ForeignKey("match_candidates.id"))
    merged_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    merged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    reason: Mapped[str | None] = mapped_column(Text)
    moved: Mapped[dict] = mapped_column(JSON, default=dict)  # ids moved, so the merge can be reversed
    reversed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reversed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))


class ProjectIdentifier(Base):
    """Source identifiers that designate a master project (deterministic matching index).

    scheme examples: "wb" (P181491), "iati" (46002-P-CM-A00-001), "budget" (national code).
    """

    __tablename__ = "project_identifiers"
    __table_args__ = (UniqueConstraint("scheme", "identifier"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    scheme: Mapped[str] = mapped_column(String(30))
    identifier: Mapped[str] = mapped_column(String(200), index=True)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
