"""Entities whose logic arrives in later phases. Tables exist now so the schema is stable."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import (
    Base,
    Money,
    ProvenanceMixin,
    Rate,
    TimestampMixin,
    provenance_constraints,
    str_enum,
    utcnow,
)
from app.models.enums import InstrumentType, ObservationKind


class MarketObservation(ProvenanceMixin, TimestampMixin, Base):
    __tablename__ = "market_observation"
    __table_args__ = (
        *provenance_constraints(),
        UniqueConstraint("security_id", "date", "kind", "source_id", name="uq_market_observation_natural_key"),
    )

    observation_id: Mapped[int] = mapped_column(primary_key=True)
    security_id: Mapped[int] = mapped_column(ForeignKey("security.security_id"), index=True)
    observation_date: Mapped[date] = mapped_column("date", index=True)
    kind: Mapped[ObservationKind] = mapped_column(str_enum(ObservationKind))
    yield_pct: Mapped[Decimal | None] = mapped_column("yield", Rate)
    price: Mapped[Decimal | None] = mapped_column(Rate)
    spread_bps: Mapped[Decimal | None] = mapped_column(Rate)
    volume: Mapped[Decimal | None] = mapped_column(Money)


class Opportunity(TimestampMixin, Base):
    """Output of the Opportunity Engine (Phase 4). Neutral labels only — never 'best'."""

    __tablename__ = "opportunity"

    opportunity_id: Mapped[int] = mapped_column(primary_key=True)
    security_id: Mapped[int | None] = mapped_column(ForeignKey("security.security_id"), index=True)
    auction_id: Mapped[int | None] = mapped_column(ForeignKey("auction.auction_id"), index=True)
    opportunity_type: Mapped[str] = mapped_column(String(64))
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    auction_date: Mapped[date | None]
    yield_pct: Mapped[Decimal | None] = mapped_column("yield", Rate)
    estimated_net_yield: Mapped[Decimal | None] = mapped_column(Rate)  # ESTIMATE
    maturity: Mapped[date | None]
    currency: Mapped[str | None] = mapped_column(String(3))
    liquidity_indicator: Mapped[str | None] = mapped_column(String(64))
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    data_confidence: Mapped[Decimal | None] = mapped_column(Rate)
    explanation: Mapped[str | None] = mapped_column(Text)
    source_urls: Mapped[list[str]] = mapped_column(JSON, default=list)
    # Deterministic key so re-running detection never duplicates an opportunity.
    dedup_key: Mapped[str] = mapped_column(String(255), unique=True)
    is_synthetic: Mapped[bool] = mapped_column(default=False)


class SubscriptionRoute(TimestampMixin, Base):
    """How an investor category can access an instrument (Phase 6). Procedural, not advice."""

    __tablename__ = "subscription_route"

    route_id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.country_id"), index=True)
    instrument_type: Mapped[InstrumentType] = mapped_column(str_enum(InstrumentType))
    investor_type: Mapped[str] = mapped_column(String(64))
    eligibility: Mapped[str | None] = mapped_column(Text)
    primary_dealer: Mapped[str | None] = mapped_column(Text)
    account_requirement: Mapped[str | None] = mapped_column(Text)
    submission_method: Mapped[str | None] = mapped_column(Text)
    settlement_method: Mapped[str | None] = mapped_column(Text)
    fees: Mapped[str | None] = mapped_column(Text)
    taxes: Mapped[str | None] = mapped_column(Text)
    official_source_id: Mapped[int | None] = mapped_column(ForeignKey("source.source_id"))
    official_source_url: Mapped[str | None] = mapped_column(String(2048))
    last_verified: Mapped[date | None]
