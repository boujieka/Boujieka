"""Connectors, raw source records, observations, provenance links, matching (Master prompt §7, §15)."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, Money, Timestamped, utcnow


class SourceConnector(Base, Timestamped):
    __tablename__ = "source_connectors"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(60), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    partner_id: Mapped[int | None] = mapped_column(ForeignKey("financing_partners.id"))
    tier: Mapped[int] = mapped_column(Integer, default=1)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="not_tested")
    status_evidence: Mapped[str | None] = mapped_column(Text)
    access_method: Mapped[str] = mapped_column(String(60))
    base_url: Mapped[str | None] = mapped_column(Text)
    documentation_url: Mapped[str | None] = mapped_column(Text)
    usage_terms: Mapped[str | None] = mapped_column(Text)
    update_frequency: Mapped[str | None] = mapped_column(String(80))
    config: Mapped[dict] = mapped_column(JSON, default=dict)  # countries, date range, filters
    schedule_cron: Mapped[str | None] = mapped_column(String(60))
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_failure_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_error: Mapped[str | None] = mapped_column(Text)
    cursor: Mapped[dict] = mapped_column(JSON, default=dict)  # incremental-sync state
    notes: Mapped[str | None] = mapped_column(Text)


class SyncRun(Base):
    """One synchronisation attempt = the import log."""

    __tablename__ = "sync_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    connector_id: Mapped[int] = mapped_column(ForeignKey("source_connectors.id"), index=True)
    trigger: Mapped[str] = mapped_column(String(20), default="manual")  # manual | scheduled | test
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), default="running")  # running | success | partial | failed
    params: Mapped[dict] = mapped_column(JSON, default=dict)
    attempts: Mapped[int] = mapped_column(Integer, default=1)
    records_retrieved: Mapped[int] = mapped_column(Integer, default=0)
    records_new: Mapped[int] = mapped_column(Integer, default=0)
    records_unchanged: Mapped[int] = mapped_column(Integer, default=0)
    records_imported: Mapped[int] = mapped_column(Integer, default=0)
    records_review: Mapped[int] = mapped_column(Integer, default=0)
    records_failed: Mapped[int] = mapped_column(Integer, default=0)
    errors: Mapped[list] = mapped_column(JSON, default=list)
    log: Mapped[str | None] = mapped_column(Text)

    connector: Mapped[SourceConnector] = relationship()


class SourceRecord(Base):
    """The original source record, preserved verbatim with its hash. Never edited in place."""

    __tablename__ = "source_records"
    __table_args__ = (UniqueConstraint("connector_id", "source_identifier", "payload_sha256"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    connector_id: Mapped[int] = mapped_column(ForeignKey("source_connectors.id"), index=True)
    sync_run_id: Mapped[int | None] = mapped_column(ForeignKey("sync_runs.id"))
    source_identifier: Mapped[str] = mapped_column(String(200), index=True)
    record_type: Mapped[str] = mapped_column(String(40))  # project | iati_activity | budget_line | upload_row
    country_iso3: Mapped[str | None] = mapped_column(String(3), index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    payload_format: Mapped[str] = mapped_column(String(10), default="json")
    raw_text: Mapped[str | None] = mapped_column(Text)  # verbatim XML/CSV row when not JSON
    payload_sha256: Mapped[str] = mapped_column(String(64))
    source_url: Mapped[str | None] = mapped_column(Text)
    source_last_updated: Mapped[str | None] = mapped_column(String(40))  # as stated by the source
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    processing_status: Mapped[str] = mapped_column(String(20), default="pending")  # pending|imported|review|failed|skipped
    processing_note: Mapped[str | None] = mapped_column(Text)
    verification_status: Mapped[str] = mapped_column(String(20), default="unverified")
    tenant_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"))

    connector: Mapped[SourceConnector] = relationship()


class SourceObservation(Base):
    """A single field value observed in a source record — the unit of provenance."""

    __tablename__ = "source_observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_record_id: Mapped[int] = mapped_column(ForeignKey("source_records.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), index=True)
    field: Mapped[str] = mapped_column(String(80))
    source_field: Mapped[str | None] = mapped_column(String(200))  # path in the source payload
    value_text: Mapped[str | None] = mapped_column(Text)
    value_numeric: Mapped[Decimal | None] = mapped_column(Money)
    value_date: Mapped[date | None] = mapped_column(Date)
    currency: Mapped[str | None] = mapped_column(String(3))
    reporting_date: Mapped[date | None] = mapped_column(Date)
    extracted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")
    verification_status: Mapped[str] = mapped_column(String(20), default="unverified")
    # Corrections never overwrite: the corrected observation points at the one it supersedes.
    supersedes_id: Mapped[int | None] = mapped_column(ForeignKey("source_observations.id"))
    correction_note: Mapped[str | None] = mapped_column(Text)


class ProjectSourceLink(Base):
    __tablename__ = "project_source_links"
    __table_args__ = (UniqueConstraint("project_id", "source_record_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    source_record_id: Mapped[int] = mapped_column(ForeignKey("source_records.id"), index=True)
    link_type: Mapped[str] = mapped_column(String(30))  # primary | deterministic_match | reviewed_match | manual
    match_rule: Mapped[str | None] = mapped_column(String(120))
    match_score: Mapped[float | None] = mapped_column(Float)
    linked_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    linked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class MatchCandidate(Base):
    """Probabilistic match awaiting human review. Never merged automatically."""

    __tablename__ = "match_candidates"
    __table_args__ = (UniqueConstraint("project_a_id", "project_b_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_a_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    project_b_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    score: Mapped[float] = mapped_column(Float)
    features: Mapped[dict] = mapped_column(JSON, default=dict)
    relation: Mapped[str] = mapped_column(String(30), default="same_project")  # same_project | additional_financing
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    review_note: Mapped[str | None] = mapped_column(Text)


class DataValidation(Base):
    """Validation findings raised during import (table `data_validation`)."""

    __tablename__ = "data_validation"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), index=True)
    rule: Mapped[str] = mapped_column(String(80))
    severity: Mapped[str] = mapped_column(String(10))  # error | warning | info
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    resolved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class DataQualityAssessment(Base):
    __tablename__ = "data_quality_assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    completeness: Mapped[float] = mapped_column(Float)
    timeliness: Mapped[float | None] = mapped_column(Float)
    traceability: Mapped[float] = mapped_column(Float)
    consistency: Mapped[float | None] = mapped_column(Float)
    source_reliability: Mapped[float | None] = mapped_column(Float)
    duplicate_risk: Mapped[float | None] = mapped_column(Float)
    missing_fields: Mapped[list] = mapped_column(JSON, default=list)
    detail: Mapped[dict] = mapped_column(JSON, default=dict)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)

