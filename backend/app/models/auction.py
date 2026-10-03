from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
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
        # Idempotency: one auction per security, date and type.
        UniqueConstraint("security_id", "auction_date", "auction_type", name="uq_auction_natural_key"),
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
