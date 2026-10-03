from datetime import date

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, ProvenanceMixin, TimestampMixin, provenance_constraints, str_enum
from app.models.enums import IssuerType, MonetaryZone


class Country(ProvenanceMixin, TimestampMixin, Base):
    __tablename__ = "country"
    __table_args__ = provenance_constraints()

    country_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    iso2: Mapped[str] = mapped_column(String(2), unique=True)
    iso3: Mapped[str] = mapped_column(String(3), unique=True)
    currency: Mapped[str] = mapped_column(String(3))  # ISO 4217
    monetary_zone: Mapped[MonetaryZone] = mapped_column(str_enum(MonetaryZone))
    central_bank: Mapped[str | None] = mapped_column(String(255))
    debt_management_office: Mapped[str | None] = mapped_column(String(255))
    primary_market_structure: Mapped[str | None] = mapped_column(Text)
    secondary_market_structure: Mapped[str | None] = mapped_column(Text)
    tax_notes: Mapped[str | None] = mapped_column(Text)
    capital_controls: Mapped[str | None] = mapped_column(Text)
    market_access_notes: Mapped[str | None] = mapped_column(Text)
    last_verified: Mapped[date | None]
    is_monitored: Mapped[bool] = mapped_column(default=True)

    issuers: Mapped[list["Issuer"]] = relationship(back_populates="country")


class Issuer(TimestampMixin, Base):
    __tablename__ = "issuer"

    issuer_id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.country_id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    issuer_type: Mapped[IssuerType] = mapped_column(str_enum(IssuerType))
    official_website: Mapped[str | None] = mapped_column(String(2048))
    debt_management_entity: Mapped[str | None] = mapped_column(String(255))
    is_synthetic: Mapped[bool] = mapped_column(default=False)

    country: Mapped[Country] = relationship(back_populates="issuers")
