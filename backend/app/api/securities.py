from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from app.api.deps import SessionDep, SourcesDep
from app.api.serializers import auction_out, security_out
from app.models import Auction, Country, Security
from app.models.enums import InstrumentType
from app.schemas import Page, SecurityDetail, SecurityOut

router = APIRouter(prefix="/securities", tags=["securities"])


@router.get("", response_model=Page[SecurityOut])
def list_securities(
    session: SessionDep,
    sources: SourcesDep,
    country: str | None = None,
    instrument_type: InstrumentType | None = None,
    currency: str | None = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Page[SecurityOut]:
    stmt = select(Security).join(Security.country)
    if country:
        stmt = stmt.where(Country.iso3 == country.upper())
    if instrument_type:
        stmt = stmt.where(Security.instrument_type == instrument_type)
    if currency:
        stmt = stmt.where(Security.currency == currency.upper())
    total = session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = session.scalars(
        stmt.options(joinedload(Security.country))
        .order_by(Security.issue_date.desc(), Security.security_id)
        .limit(limit)
        .offset(offset)
    ).all()
    return Page[SecurityOut](
        items=[security_out(s, sources) for s in rows], total=total, limit=limit, offset=offset
    )


@router.get("/{security_id}", response_model=SecurityDetail)
def get_security(security_id: int, session: SessionDep, sources: SourcesDep) -> SecurityDetail:
    security = session.get(
        Security,
        security_id,
        options=[joinedload(Security.country), selectinload(Security.auctions)],
    )
    if security is None:
        raise HTTPException(404, "Security not found")
    auctions: list[Auction] = sorted(security.auctions, key=lambda a: a.auction_date)
    return SecurityDetail(
        **security_out(security, sources).model_dump(),
        auctions=[auction_out(a, sources) for a in auctions],
    )
