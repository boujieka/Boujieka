from datetime import date
from decimal import Decimal
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app.analytics import calculations as calc
from app.api.deps import SessionDep, SourcesDep
from app.api.serializers import auction_out
from app.models import Auction, Country, Security
from app.models.enums import AuctionStatus, InstrumentType
from app.schemas import AuctionDetail, AuctionOut, HistoricalComparison, Page

router = APIRouter(prefix="/auctions", tags=["auctions"])

PEER_LIMIT = 6


def _csv(value: str | None) -> list[str] | None:
    return [v.strip().upper() for v in value.split(",") if v.strip()] if value else None


@router.get("", response_model=Page[AuctionOut])
def list_auctions(
    session: SessionDep,
    sources: SourcesDep,
    country: Annotated[str | None, Query(description="ISO3 codes, comma-separated")] = None,
    currency: Annotated[str | None, Query(description="ISO 4217 codes, comma-separated")] = None,
    instrument_type: list[InstrumentType] | None = Query(None),
    status: list[AuctionStatus] | None = Query(None),
    date_from: date | None = None,
    date_to: date | None = None,
    min_tenor_days: Annotated[int | None, Query(ge=0)] = None,
    max_tenor_days: Annotated[int | None, Query(ge=0)] = None,
    include_synthetic: bool = True,
    order: Literal["asc", "desc"] = "asc",
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Page[AuctionOut]:
    stmt = select(Auction).join(Auction.security).join(Security.country)
    if countries := _csv(country):
        stmt = stmt.where(Country.iso3.in_(countries))
    if currencies := _csv(currency):
        stmt = stmt.where(Security.currency.in_(currencies))
    if instrument_type:
        stmt = stmt.where(Security.instrument_type.in_(instrument_type))
    if status:
        stmt = stmt.where(Auction.status.in_(status))
    if date_from:
        stmt = stmt.where(Auction.auction_date >= date_from)
    if date_to:
        stmt = stmt.where(Auction.auction_date <= date_to)
    if min_tenor_days is not None:
        stmt = stmt.where(Security.tenor_days >= min_tenor_days)
    if max_tenor_days is not None:
        stmt = stmt.where(Security.tenor_days <= max_tenor_days)
    if not include_synthetic:
        stmt = stmt.where(Auction.is_synthetic.is_(False))

    total = session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    sort = Auction.auction_date.asc() if order == "asc" else Auction.auction_date.desc()
    rows = session.scalars(
        stmt.options(joinedload(Auction.security).joinedload(Security.country))
        .order_by(sort, Country.iso3, Security.tenor_days, Auction.auction_id)
        .limit(limit)
        .offset(offset)
    ).all()
    return Page[AuctionOut](
        items=[auction_out(a, sources) for a in rows], total=total, limit=limit, offset=offset
    )


@router.get("/{auction_id}", response_model=AuctionDetail)
def get_auction(auction_id: int, session: SessionDep, sources: SourcesDep) -> AuctionDetail:
    a = session.get(
        Auction, auction_id, options=[joinedload(Auction.security).joinedload(Security.country)]
    )
    if a is None:
        raise HTTPException(404, "Auction not found")

    peers = session.scalars(
        select(Auction)
        .join(Auction.security)
        .where(
            Security.country_id == a.security.country_id,
            Security.instrument_type == a.security.instrument_type,
            Security.tenor_days == a.security.tenor_days,
            Auction.status == AuctionStatus.COMPLETED,
            Auction.auction_date < a.auction_date,
            Auction.auction_id != a.auction_id,
        )
        .options(joinedload(Auction.security).joinedload(Security.country))
        .order_by(Auction.auction_date.desc())
        .limit(PEER_LIMIT)
    ).all()

    previous = peers[0] if peers else None
    ratios = [
        r
        for p in peers
        if (r := calc.bid_to_cover(p.amount_submitted, p.amount_offered)) is not None
    ]
    caveats = []
    conventions = {p.yield_convention for p in peers} | {a.yield_convention}
    if len(conventions) > 1:
        caveats.append("Peers use different yield conventions; yield changes are not comparable.")
    if a.is_synthetic or any(p.is_synthetic for p in peers):
        caveats.append("Includes SYNTHETIC data — not real market data.")

    comparison = HistoricalComparison(
        peer_definition=(
            f"Up to {PEER_LIMIT} previous completed auctions of the same country, "
            "instrument type and original tenor"
        ),
        previous_auction_id=previous.auction_id if previous else None,
        yield_change_bps=calc.quantize(
            calc.change_bps(
                a.weighted_average_yield, previous.weighted_average_yield if previous else None
            ),
            2,
        ),
        peer_average_bid_to_cover=calc.quantize(sum(ratios, Decimal(0)) / len(ratios))
        if ratios
        else None,
        peer_count=len(peers),
        caveat=" ".join(caveats) or None,
    )
    return AuctionDetail(
        **auction_out(a, sources).model_dump(),
        comparison=comparison,
        peers=[auction_out(p, sources) for p in peers],
    )
