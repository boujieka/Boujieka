"""ORM → API conversion. The only place where official, calculated and provenance blocks are assembled."""

from app.analytics import calculations as calc
from app.models import Auction, Country, Security, Source
from app.models.enums import CoverageTier, FieldStatus
from app.schemas import (
    AuctionCalculated,
    AuctionOfficial,
    AuctionOut,
    CountryOut,
    Provenance,
    SecurityOut,
    SecuritySummary,
    SourceRef,
)

AUCTION_OFFICIAL_FIELDS = tuple(AuctionOfficial.model_fields)
SECURITY_OPTIONAL_FIELDS = (
    "isin",
    "face_value",
    "coupon_rate",
    "coupon_frequency",
    "issue_date",
    "maturity_date",
    "amortization",
    "indexation",
    "green_social_sustainability_flag",
    "listing_status",
    "minimum_denomination",
)
COUNTRY_OPTIONAL_FIELDS = (
    "central_bank",
    "debt_management_office",
    "primary_market_structure",
    "secondary_market_structure",
    "tax_notes",
    "capital_controls",
    "market_access_notes",
    "last_verified",
)


def resolve_field_status(obj: object, fields: tuple[str, ...]) -> dict[str, str]:
    """Explain every empty field. A null with no recorded reason is 'not_available'."""
    recorded: dict[str, str] = getattr(obj, "field_status", None) or {}
    return {
        f: recorded.get(f, FieldStatus.NOT_AVAILABLE.value)
        for f in fields
        if getattr(obj, f) is None
    }


def provenance(obj, source: Source | None) -> Provenance:
    return Provenance(
        data_nature=obj.data_nature,
        verification_status=obj.verification_status,
        confidence_score=obj.confidence_score,
        is_synthetic=obj.is_synthetic,
        source=SourceRef.model_validate(source) if source else None,
        source_url=obj.source_url,
        source_document_id=obj.source_document_id,
        publication_date=obj.publication_date,
        extracted_at=obj.extracted_at,
        notes=obj.provenance_notes,
    )


def country_out(
    country: Country, sources: dict[int, Source], with_market_data: set[int]
) -> CountryOut:
    return CountryOut(
        **{f: getattr(country, f) for f in CountryOut.model_fields if hasattr(Country, f)
           and f not in ("field_status", "provenance")},
        coverage_tier=CoverageTier.MARKET_DATA
        if country.country_id in with_market_data
        else CoverageTier.REFERENCE_ONLY,
        field_status=resolve_field_status(country, COUNTRY_OPTIONAL_FIELDS),
        provenance=provenance(country, sources.get(country.source_id)),
    )


def security_summary(security: Security) -> SecuritySummary:
    return SecuritySummary(
        security_id=security.security_id,
        security_name=security.security_name,
        instrument_type=security.instrument_type,
        tenor_days=security.tenor_days,
        maturity_date=security.maturity_date,
        currency=security.currency,
        country_iso3=security.country.iso3,
        country_name=security.country.name,
        is_synthetic=security.is_synthetic,
    )


def security_out(security: Security, sources: dict[int, Source]) -> SecurityOut:
    summary = security_summary(security).model_dump()
    extra = {
        f: getattr(security, f)
        for f in SecurityOut.model_fields
        if f not in summary and f not in ("field_status", "provenance")
    }
    return SecurityOut(
        **summary,
        **extra,
        field_status=resolve_field_status(security, SECURITY_OPTIONAL_FIELDS),
        provenance=provenance(security, sources.get(security.source_id)),
    )


def auction_calculated(a: Auction) -> AuctionCalculated:
    return AuctionCalculated(
        bid_to_cover=calc.quantize(calc.bid_to_cover(a.amount_submitted, a.amount_offered)),
        allocation_rate=calc.quantize(calc.allocation_rate(a.amount_allocated, a.amount_offered)),
        acceptance_rate=calc.quantize(calc.acceptance_rate(a.amount_allocated, a.amount_submitted)),
    )


def auction_out(a: Auction, sources: dict[int, Source]) -> AuctionOut:
    return AuctionOut(
        auction_id=a.auction_id,
        status=a.status,
        auction_type=a.auction_type,
        announcement_date=a.announcement_date,
        auction_date=a.auction_date,
        settlement_date=a.settlement_date,
        security=security_summary(a.security),
        official=AuctionOfficial(**{f: getattr(a, f) for f in AUCTION_OFFICIAL_FIELDS}),
        calculated=auction_calculated(a),
        field_status=resolve_field_status(a, AUCTION_OFFICIAL_FIELDS),
        provenance=provenance(a, sources.get(a.source_id)),
    )


def countries_with_market_data(session) -> set[int]:
    """Country ids that have at least one security loaded."""
    from sqlalchemy import select

    return set(session.scalars(select(Security.country_id).distinct()))
