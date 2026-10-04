"""Phase 2 staging: extracted values waiting for a human, and the review audit trail.

Why a staging table instead of `auction` rows with verification_status=UNVERIFIED: every public
read path (auctions, securities, yield curves, heat grid, maturity walls, the Opportunity
Engine) reads `auction`/`security` directly. Keeping unreviewed extractions out of those tables
means an unverified value cannot leak into a public answer through a query that forgot a
filter. Approval *promotes* a staging row into `security`/`auction` as a VERIFIED FACT.
"""

from datetime import date, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, ProvenanceMixin, TimestampMixin, provenance_constraints, utcnow
from app.models.source import SourceDocument


class AuctionExtraction(ProvenanceMixin, TimestampMixin, Base):
    """One auction tranche read from one official document. UNVERIFIED until reviewed.

    `fields` maps a field name to {value, raw, locator, confidence, unit?, note?}: the value as
    normalised (unit conversion only), the text it was read from, where in the document
    (page/line/label/column), and the extraction confidence. Empty fields are explained in
    `field_status` (ProvenanceMixin). `confidence_score` is the minimum over key fields.
    """

    __tablename__ = "auction_extraction"
    __table_args__ = (
        *provenance_constraints(),
        # Idempotency: re-extracting a document updates its rows instead of adding new ones.
        UniqueConstraint("source_document_id", "tranche_key", name="uq_auction_extraction_document_tranche"),
    )

    extraction_id: Mapped[int] = mapped_column(primary_key=True)
    tranche_key: Mapped[str] = mapped_column(String(64))  # ISIN, or "col-N" if unreadable
    extractor: Mapped[str] = mapped_column(String(64))  # parser name/version
    parse_status: Mapped[str] = mapped_column(String(16), index=True)  # complete | partial
    # Denormalised for listing and filtering the queue; the authoritative values are in `fields`.
    country_iso3: Mapped[str | None] = mapped_column(String(3), index=True)
    isin: Mapped[str | None] = mapped_column(String(12), index=True)
    instrument: Mapped[str | None] = mapped_column(String(8))
    auction_date: Mapped[date | None] = mapped_column(index=True)
    fields: Mapped[dict] = mapped_column(JSON, default=dict)
    # Document-level facts shared by every tranche (global totals, coverage, publication date).
    operation: Mapped[dict] = mapped_column(JSON, default=dict)
    warnings: Mapped[list[str]] = mapped_column(JSON, default=list)
    # Consistency checks run at extraction (CALCULATION, for the reviewer only).
    checks: Mapped[list[dict]] = mapped_column(JSON, default=list)
    reviewed_by: Mapped[str | None] = mapped_column(String(128))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    review_reason: Mapped[str | None] = mapped_column(Text)
    promoted_auction_id: Mapped[int | None] = mapped_column(ForeignKey("auction.auction_id"))

    document: Mapped[SourceDocument | None] = relationship()


class ExtractionReviewEvent(Base):
    """Append-only audit trail of review decisions (who, when, what, why)."""

    __tablename__ = "extraction_review_event"

    event_id: Mapped[int] = mapped_column(primary_key=True)
    extraction_id: Mapped[int] = mapped_column(ForeignKey("auction_extraction.extraction_id"), index=True)
    action: Mapped[str] = mapped_column(String(16))  # approved | rejected
    reviewer: Mapped[str] = mapped_column(String(128))
    reason: Mapped[str | None] = mapped_column(Text)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
