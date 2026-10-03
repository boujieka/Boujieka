from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, or_, select

from app.api.deps import AsOfDep, SessionDep, SourcesDep
from app.api.serializers import country_out
from app.models import Auction, Country, Security, Source
from app.models.enums import AuctionStatus, MonetaryZone
from app.schemas import CountryDetail, CountryOut, SourceOut, YieldCurve, YieldCurvePoint

router = APIRouter(prefix="/countries", tags=["countries"])

# Regional sources apply to every member of the zone.
ZONE_INSTITUTIONS = {
    MonetaryZone.CEMAC: ("BEAC", "BVMAC"),
    MonetaryZone.WAEMU: ("BCEAO", "UMOA-Titres", "BRVM"),
}


def _get_country(session, iso3: str) -> Country:
    country = session.scalar(select(Country).where(Country.iso3 == iso3.upper()))
    if country is None:
        raise HTTPException(404, "Country not found")
    return country


@router.get("", response_model=list[CountryOut])
def list_countries(session: SessionDep, sources: SourcesDep) -> list[CountryOut]:
    rows = session.scalars(select(Country).where(Country.is_monitored).order_by(Country.name))
    return [country_out(c, sources) for c in rows]


@router.get("/{iso3}", response_model=CountryDetail)
def get_country(iso3: str, session: SessionDep, sources: SourcesDep, as_of: AsOfDep) -> CountryDetail:
    country = _get_country(session, iso3)
    by_country = (
        select(func.count())
        .select_from(Auction)
        .join(Auction.security)
        .where(Security.country_id == country.country_id)
    )
    upcoming = session.scalar(
        by_country.where(Auction.status == AuctionStatus.ANNOUNCED, Auction.auction_date >= as_of)
    )
    completed = session.scalar(by_country.where(Auction.status == AuctionStatus.COMPLETED))
    securities = session.scalar(
        select(func.count()).select_from(Security).where(Security.country_id == country.country_id)
    )
    regional = ZONE_INSTITUTIONS.get(country.monetary_zone, ())
    country_sources = session.scalars(
        select(Source)
        .where(
            or_(
                Source.country_id == country.country_id,
                Source.country_id.is_(None) & Source.institution.in_(regional),
            )
        )
    ).all()
    return CountryDetail(
        **country_out(country, sources).model_dump(),
        upcoming_auction_count=upcoming or 0,
        completed_auction_count=completed or 0,
        security_count=securities or 0,
        sources=[
            SourceOut.model_validate(s)
            for s in sorted(country_sources, key=lambda s: (s.priority, s.name))
        ],
    )


@router.get("/{iso3}/yield-curve", response_model=YieldCurve)
def yield_curve(
    iso3: str,
    session: SessionDep,
    as_of: AsOfDep,
    lookback_days: Annotated[int, Query(ge=7, le=730)] = 120,
) -> YieldCurve:
    """Primary-auction curve: latest weighted-average yield per original tenor.

    These are observed auction yields (FACT, or SYNTHETIC), not a fitted curve.
    """
    country = _get_country(session, iso3)
    rows = session.execute(
        select(Auction, Security)
        .join(Auction.security)
        .where(
            Security.country_id == country.country_id,
            Auction.status == AuctionStatus.COMPLETED,
            Auction.weighted_average_yield.is_not(None),
            Security.tenor_days.is_not(None),
            Auction.auction_date <= as_of,
            Auction.auction_date > as_of - timedelta(days=lookback_days),
        )
        .order_by(Auction.auction_date.desc())
    ).all()
    latest: dict[int, YieldCurvePoint] = {}
    for auction, security in rows:
        if security.tenor_days not in latest:
            latest[security.tenor_days] = YieldCurvePoint(
                tenor_days=security.tenor_days,
                instrument_type=security.instrument_type,
                weighted_average_yield=auction.weighted_average_yield,
                auction_id=auction.auction_id,
                auction_date=auction.auction_date,
                yield_convention=auction.yield_convention,
                is_synthetic=auction.is_synthetic,
            )
    return YieldCurve(
        country_iso3=country.iso3,
        as_of=as_of,
        lookback_days=lookback_days,
        method="Latest completed-auction weighted-average yield per original tenor (no fitting).",
        caveat=(
            "Points may come from different dates and yield conventions; bills and bonds are "
            "often quoted differently. Reopened bonds are plotted at original, not residual, tenor."
        ),
        points=sorted(latest.values(), key=lambda p: p.tenor_days),
    )
