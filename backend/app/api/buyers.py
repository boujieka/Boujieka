"""Buyer access: who can buy government securities and how (procedural, quoted, not advice)."""

from decimal import Decimal

from fastapi import APIRouter
from sqlalchemy import select

from app.api.deps import SessionDep
from app.models import Country, SubscriptionRoute
from app.schemas import AccreditedDealers, DealerOut, DealerSourceOut, SubscriptionRouteOut
from app.seed.dealers import DEALER_SOURCES, DEALERS, VERIFIED_ON

router = APIRouter(tags=["buyers"])


@router.get("/subscription-routes", response_model=list[SubscriptionRouteOut])
def subscription_routes(session: SessionDep, country: str | None = None) -> list[SubscriptionRouteOut]:
    stmt = select(SubscriptionRoute, Country).join(Country, Country.country_id == SubscriptionRoute.country_id)
    if country:
        stmt = stmt.where(Country.iso3 == country.upper())
    rows = session.execute(stmt.order_by(Country.name, SubscriptionRoute.instrument_type)).all()
    return [
        SubscriptionRouteOut(
            country_iso3=c.iso3,
            country_name=c.name,
            monetary_zone=c.monetary_zone,
            instrument_type=r.instrument_type,
            investor_type=r.investor_type,
            eligibility=r.eligibility,
            primary_dealer=r.primary_dealer,
            account_requirement=r.account_requirement,
            submission_method=r.submission_method,
            settlement_method=r.settlement_method,
            fees=r.fees,
            taxes=r.taxes,
            instrument_notes=r.instrument_notes,
            official_source_url=r.official_source_url,
            last_verified=r.last_verified,
            quotes=r.quotes or [],
        )
        for r, c in rows
    ]


@router.get("/accredited-dealers", response_model=AccreditedDealers)
def accredited_dealers(country: str | None = None) -> AccreditedDealers:
    """Institutions accredited to bid at auctions, from official lists (static, versioned data)."""
    iso = country.upper() if country else None
    sources = [s for s in DEALER_SOURCES if iso is None or iso in s["countries"]]
    ids = {s["id"] for s in sources}
    return AccreditedDealers(
        sources=[DealerSourceOut(**s, verified_on=VERIFIED_ON) for s in sources],
        dealers=[
            DealerOut(source_id=src, country_iso3=c, name=n, kind=k,
                      market_share_pct=Decimal(share) if share is not None else None, rank=rank)
            for src, c, n, k, share, rank in DEALERS
            if src in ids and (iso is None or c == iso)
        ],
    )
