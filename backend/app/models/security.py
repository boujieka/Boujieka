from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, String
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
from app.models.country import Country, Issuer
from app.models.enums import CouponFrequency, InstrumentType


class Security(ProvenanceMixin, TimestampMixin, Base):
    __tablename__ = "security"
    __table_args__ = provenance_constraints()

    security_id: Mapped[int] = mapped_column(primary_key=True)
    issuer_id: Mapped[int] = mapped_column(ForeignKey("issuer.issuer_id"), index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.country_id"), index=True)
    instrument_type: Mapped[InstrumentType] = mapped_column(str_enum(InstrumentType), index=True)
    security_name: Mapped[str] = mapped_column(String(255))
    # Unique when present; many local instruments have no published ISIN.
    isin: Mapped[str | None] = mapped_column(String(12), unique=True)
    local_code: Mapped[str | None] = mapped_column(String(64))
    currency: Mapped[str] = mapped_column(String(3), index=True)
    face_value: Mapped[Decimal | None] = mapped_column(Money)
    coupon_rate: Mapped[Decimal | None] = mapped_column(Rate)  # percent
    coupon_frequency: Mapped[CouponFrequency | None] = mapped_column(str_enum(CouponFrequency))
    issue_date: Mapped[date | None]
    maturity_date: Mapped[date | None] = mapped_column(index=True)
    tenor_days: Mapped[int | None]
    amortization: Mapped[str | None] = mapped_column(String(255))
    indexation: Mapped[str | None] = mapped_column(String(255))
    green_social_sustainability_flag: Mapped[str | None] = mapped_column(String(32))
    listing_status: Mapped[str | None] = mapped_column(String(128))
    minimum_denomination: Mapped[Decimal | None] = mapped_column(Money)

    issuer: Mapped[Issuer] = relationship()
    country: Mapped[Country] = relationship()
    auctions: Mapped[list["Auction"]] = relationship(  # noqa: F821
        back_populates="security", order_by="Auction.auction_date"
    )
