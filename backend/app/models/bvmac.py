"""BVMAC staging: one row per bond line of one Bulletin officiel de la cote (BOC).

Like `auction_extraction` for UMOA-Titres, unverified values never sit in a public table. A row is
written UNVERIFIED by app.ingest.bvmac, then app.ingest.bvmac_check re-downloads the document,
reads it twice (pdftotext -layout and -raw) and runs strict checks. Only a row that passes every
check becomes VERIFIED and is promoted: the bond to `security` and — only when the bond actually
traded that day — the closing price to `market_observation` (kind SECONDARY_MARKET). Rows that
fail stay UNVERIFIED with their `hold_reasons`, for a person to look at.

`fields` maps a field name to {value, raw, locator}: the value as normalised, the exact printed
text, and where it is printed ("p<page>:L<line> t<i>-<j>" in the -layout text). Quote-table fields
use the column names of app.ingest.bvmac_extract.QUOTE_FIELDS; characteristics-table fields are
prefixed "char_". The previous / reference prices of a bond that did not trade ("NC") are stale
reference prices: they are kept here only, never promoted.
"""

from datetime import date, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, ProvenanceMixin, TimestampMixin, provenance_constraints
from app.models.source import SourceDocument


class BvmacQuote(ProvenanceMixin, TimestampMixin, Base):
    __tablename__ = "bvmac_quote"
    __table_args__ = (
        *provenance_constraints(),
        UniqueConstraint("source_document_id", "isin", name="uq_bvmac_quote_document_isin"),
    )

    quote_id: Mapped[int] = mapped_column(primary_key=True)
    extractor: Mapped[str] = mapped_column(String(32))
    session_date: Mapped[date | None] = mapped_column(index=True)
    boc_number: Mapped[str | None] = mapped_column(String(16))
    isin: Mapped[str] = mapped_column(String(12), index=True)
    mnemo: Mapped[str | None] = mapped_column(String(16))
    section: Mapped[str | None] = mapped_column(String(16))  # sovereign | regional | private
    issuer_name: Mapped[str | None] = mapped_column(String(255))
    security_name: Mapped[str | None] = mapped_column(String(255))
    country_iso3: Mapped[str | None] = mapped_column(String(3), index=True)
    parse_status: Mapped[str] = mapped_column(String(16), index=True)  # complete | partial
    traded: Mapped[bool | None] = mapped_column(index=True)  # volume traded > 0 (None if unread)
    fields: Mapped[dict] = mapped_column(JSON, default=dict)
    raw_line: Mapped[str | None] = mapped_column(Text)  # the printed quote line (-layout)
    errors: Mapped[list[str]] = mapped_column(JSON, default=list)  # parser errors
    checks: Mapped[list[dict]] = mapped_column(JSON, default=list)  # last check run, one entry per check
    hold_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewed_by: Mapped[str | None] = mapped_column(String(128))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    promoted_security_id: Mapped[int | None] = mapped_column(ForeignKey("security.security_id"))
    promoted_observation_id: Mapped[int | None] = mapped_column(
        ForeignKey("market_observation.observation_id"))
    notes: Mapped[str | None] = mapped_column(Text)

    document: Mapped[SourceDocument | None] = relationship()
