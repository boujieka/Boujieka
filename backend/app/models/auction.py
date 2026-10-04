from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import (
    Base,
    Money,
    ProvenanceMixin,
    Rate,
    TimestampMixin,
    provenance_constraints,
    str_enum,
)
from app.models.enums import AuctionStatus, AuctionType
from app.models.security import Security


class Auction(ProvenanceMixin, TimestampMixin, Base):
    """An auction/issuance event. All amount and yield fields are as published (FACT).

    Derived figures (bid-to-cover etc.) are NOT stored here; they are computed by
    app.analytics and labelled CALCULATION in the API.
    """

    __tablename__ = "auction"
    __table_args__ = (
        *provenance_constraints(),
        # Idempotency. UMOA-Titres sometimes holds two distinct auctions of the same security on
        # the same day (e.g. a regular issue and a "rachat-émission" issue), told apart only by
        # the printed adjudication number ("ADJ-SN0000003971-BAT1A-1-2025" vs "…-BAT1A-2025").
        # A row with a reference is unique on (security, date, type, reference); NULLs are
        # distinct in a unique constraint on both PostgreSQL and SQLite, so rows without a
        # reference (synthetic data, reports that print none) keep the old rule — one per
        # (security, date, type) — through the partial unique index below.
        UniqueConstraint("security_id", "auction_date", "auction_type", "auction_reference",
                         name="uq_auction_natural_key"),
        Index("uq_auction_natural_key_unreferenced", "security_id", "auction_date", "auction_type",
              unique=True, postgresql_where=text("auction_reference IS NULL"),
              sqlite_where=text("auction_reference IS NULL")),
        CheckConstraint(
            "amount_offered IS NULL OR amount_offered >= 0", name="amount_offered_non_negative"
        ),
        CheckConstraint(
            "amount_submitted IS NULL OR amount_submitted >= 0",
            name="amount_submitted_non_negative",
        ),
        CheckConstraint(
            "amount_allocated IS NULL OR amount_allocated >= 0",
            name="amount_allocated_non_negative",
        ),
    )

    auction_id: Mapped[int] = mapped_column(primary_key=True)
    security_id: Mapped[int] = mapped_column(ForeignKey("security.security_id"), index=True)
    announcement_date: Mapped[date | None]
    auction_date: Mapped[date] = mapped_column(index=True)
    settlement_date: Mapped[date | None]
    auction_type: Mapped[AuctionType] = mapped_column(str_enum(AuctionType))
    # The adjudication number printed by the source ("ADJ-…" for an issue, "RA-…" for a buyback),
    # as published. NULL when the source prints none (and for synthetic rows).
    auction_reference: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[AuctionStatus] = mapped_column(str_enum(AuctionStatus), index=True)
    amount_offered: Mapped[Decimal | None] = mapped_column(Money)
    amount_submitted: Mapped[Decimal | None] = mapped_column(Money)
    amount_allocated: Mapped[Decimal | None] = mapped_column(Money)
    minimum_bid: Mapped[Decimal | None] = mapped_column(Rate)
    maximum_bid: Mapped[Decimal | None] = mapped_column(Rate)
    cutoff_yield: Mapped[Decimal | None] = mapped_column(Rate)
    weighted_average_yield: Mapped[Decimal | None] = mapped_column(Rate)
    average_price: Mapped[Decimal | None] = mapped_column(Rate)  # per 100 face
    # As published, if the source publishes its own ratio. Our computed ratio is separate.
    reported_bid_to_cover: Mapped[Decimal | None] = mapped_column(Rate)
    number_of_bidders: Mapped[int | None]
    number_of_successful_bidders: Mapped[int | None]
    # How the source quotes yields (e.g. simple interest ACT/360). Needed before comparing.
    yield_convention: Mapped[str | None] = mapped_column(String(64))

    security: Mapped[Security] = relationship(back_populates="auctions")
