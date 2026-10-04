from datetime import date, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, str_enum
from app.models.enums import SOURCE_PRIORITY, SourceCategory, SourceStatus


class Source(TimestampMixin, Base):
    """A publisher we take data from (a website section, a feed, a document series)."""

    __tablename__ = "source"

    source_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    institution: Mapped[str] = mapped_column(String(255))
    category: Mapped[SourceCategory] = mapped_column(str_enum(SourceCategory))
    # Null for regional/multi-country sources (e.g. BEAC covers six CEMAC states).
    country_id: Mapped[int | None] = mapped_column(
        ForeignKey("country.country_id", use_alter=True), index=True
    )
    # Null until an operator has confirmed the official URL. We never guess URLs.
    base_url: Mapped[str | None] = mapped_column(String(2048))
    status: Mapped[SourceStatus] = mapped_column(
        str_enum(SourceStatus), default=SourceStatus.PENDING_CONFIGURATION
    )
    crawl_config: Mapped[dict] = mapped_column(JSON, default=dict)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_error: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    is_synthetic: Mapped[bool] = mapped_column(default=False)

    documents: Mapped[list["SourceDocument"]] = relationship(back_populates="source")

    @property
    def candidates(self) -> list[dict[str, str]]:
        """Proposed URLs awaiting operator confirmation (see app.seed.source_candidates)."""
        return (self.crawl_config or {}).get("candidates", [])

    @property
    def priority(self) -> int:
        """1 = most authoritative (central bank) … higher = less authoritative."""
        return SOURCE_PRIORITY[self.category]


class SourceDocument(TimestampMixin, Base):
    """One retrieved artefact (PDF, HTML page, press release). Deduplicated by content hash."""

    __tablename__ = "source_document"

    document_id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("source.source_id"), index=True)
    url: Mapped[str | None] = mapped_column(String(2048))
    title: Mapped[str] = mapped_column(String(512))
    document_type: Mapped[str] = mapped_column(String(64))  # e.g. auction_notice, auction_result
    publication_date: Mapped[date | None]
    retrieved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Idempotency key for ingestion: the same bytes are never stored twice.
    content_sha256: Mapped[str | None] = mapped_column(String(64), unique=True)
    mime_type: Mapped[str | None] = mapped_column(String(128))
    storage_path: Mapped[str | None] = mapped_column(String(1024))
    extraction_status: Mapped[str] = mapped_column(String(32), default="not_started")
    is_synthetic: Mapped[bool] = mapped_column(default=False)

    source: Mapped[Source] = relationship(back_populates="documents")
