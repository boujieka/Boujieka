from collections import Counter
from datetime import timedelta
from decimal import Decimal
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.analytics import calculations as calc
from app.api.deps import AsOfDep, SessionDep
from app.api.serializers import security_summary
from app.engine.opportunities import RULES, load_market, maturity_walls
from app.models import Country, Opportunity, Security
from app.models.enums import DataNature
from app.schemas import (
    HeatCell,
    HeatGrid,
    HeatRow,
    MaturityWall,
    OpportunityOut,
    OpportunityPage,
    WallMonth,
)

router = APIRouter(tags=["opportunities"])

DISCLAIMER = (
    "Signals are factual, rule-based observations about published auction data. They are not "
    "recommendations, do not rank investments, and do not account for your tax, fees, FX or risk."
)

# Tenor buckets for the pan-African grid: (label, max original tenor in days).
BUCKETS: list[tuple[str, int]] = [
    ("3M", 100), ("6M", 200), ("12M", 400), ("2-3Y", 1200), ("5Y", 2000), ("7Y+", 10**6),
]


def _bucket(days: int) -> str:
    return next(label for label, limit in BUCKETS if days <= limit)


def _csv(value: str | None) -> list[str] | None:
    return [v.strip().upper() for v in value.split(",") if v.strip()] if value else None


def _criteria_unmet(o: Opportunity, min_yield, min_tenor, max_tenor, currencies) -> list[str]:
    unmet = []
    tenor = o.security.tenor_days if o.security else None
    if min_yield is not None and (o.yield_pct is None or o.yield_pct < min_yield):
        unmet.append("yield below minimum" if o.yield_pct is not None else "no yield for this signal")
    if min_tenor is not None and (tenor is None or tenor < min_tenor):
        unmet.append("tenor below minimum" if tenor is not None else "no tenor for this signal")
    if max_tenor is not None and (tenor is None or tenor > max_tenor):
        unmet.append("tenor above maximum" if tenor is not None else "no tenor for this signal")
    if currencies and (o.currency or "") not in currencies:
        unmet.append("currency not selected")
    return unmet


@router.get("/opportunities", response_model=OpportunityPage)
def list_opportunities(
    session: SessionDep,
    country: Annotated[str | None, Query(description="ISO3 codes, comma-separated")] = None,
    opportunity_type: list[str] | None = Query(None),
    include_inactive: bool = False,
    min_yield: Annotated[Decimal | None, Query(description="Criteria: minimum yield, percent")] = None,
    min_tenor_days: Annotated[int | None, Query(ge=0)] = None,
    max_tenor_days: Annotated[int | None, Query(ge=0)] = None,
    currency: Annotated[str | None, Query(description="Criteria: ISO 4217 codes, comma-separated")] = None,
    matching_only: bool = False,
    sort: Literal["date", "strength"] = "date",
    limit: Annotated[int, Query(ge=1, le=500)] = 200,
) -> OpportunityPage:
    stmt = select(Opportunity, Country).join(Country, Country.country_id == Opportunity.country_id)
    if countries := _csv(country):
        stmt = stmt.where(Country.iso3.in_(countries))
    if opportunity_type:
        stmt = stmt.where(Opportunity.opportunity_type.in_(opportunity_type))
    if not include_inactive:
        stmt = stmt.where(Opportunity.is_active.is_(True))
    rows = session.execute(
        stmt.options(joinedload(Opportunity.security).joinedload(Security.country))
    ).all()

    currencies = _csv(currency)
    has_criteria = any(v is not None for v in (min_yield, min_tenor_days, max_tenor_days)) or bool(currencies)
    items: list[OpportunityOut] = []
    for o, c in rows:
        unmet = _criteria_unmet(o, min_yield, min_tenor_days, max_tenor_days, currencies) if has_criteria else []
        if matching_only and has_criteria and unmet:
            continue
        items.append(OpportunityOut(
            opportunity_id=o.opportunity_id,
            opportunity_type=o.opportunity_type,
            label=o.label,
            country_iso3=c.iso3,
            country_name=c.name,
            currency=o.currency,
            security=security_summary(o.security) if o.security else None,
            auction_id=o.auction_id,
            auction_date=o.auction_date,
            yield_pct=o.yield_pct,
            maturity=o.maturity,
            strength=o.strength,
            explanation=o.explanation,
            evidence=o.evidence or {},
            risk_flags=o.risk_flags or [],
            data_confidence=o.data_confidence,
            is_synthetic=o.is_synthetic,
            as_of=o.as_of,
            is_active=o.is_active,
            matches_criteria=(not unmet) if has_criteria else None,
            criteria_unmet=unmet,
        ))

    if sort == "strength":
        items.sort(key=lambda i: (-(i.strength or Decimal(0)), i.country_iso3, i.opportunity_id))
    else:
        # Soonest auction first; signals without a date (e.g. refinancing) after.
        items.sort(key=lambda i: (i.auction_date is None, i.auction_date or i.as_of, i.country_iso3, i.opportunity_id))

    criteria = {
        k: str(v) for k, v in {
            "min_yield": min_yield, "min_tenor_days": min_tenor_days,
            "max_tenor_days": max_tenor_days, "currency": currency,
        }.items() if v not in (None, "")
    }
    return OpportunityPage(
        items=items[:limit],
        total=len(items),
        by_type=dict(Counter(i.opportunity_type for i in items)),
        by_country=dict(Counter(i.country_iso3 for i in items)),
        criteria=criteria,
        disclaimer=DISCLAIMER,
    )


def _active_counts(session: Session) -> dict[int, int]:
    return dict(session.execute(
        select(Opportunity.country_id, func.count()).where(Opportunity.is_active.is_(True))
        .group_by(Opportunity.country_id)
    ).all())


@router.get("/market/heat-grid", response_model=HeatGrid)
def heat_grid(session: SessionDep, as_of: AsOfDep) -> HeatGrid:
    """Pan-African grid: latest auction per country × tenor bucket, with demand vs own history.

    The demand z-score compares each series only with its own past auctions, so it is
    comparable across markets even where yield conventions differ.
    """
    m = load_market(session, as_of)
    r = RULES["demand"]
    lookback = RULES["curve_inversion"]["curve_lookback_days"]
    cells: dict[int, dict[str, HeatCell]] = {}
    for (country_id, instrument, tenor), series in m.completed.items():
        latest = series[-1]
        if latest.auction_date <= as_of - timedelta(days=lookback):
            continue
        bucket = _bucket(tenor)
        current = cells.setdefault(country_id, {}).get(bucket)
        if current and current.auction_date >= latest.auction_date:
            continue
        peers = [
            x for p in series[:-1][-r["max_peers"]:]
            if (x := calc.bid_to_cover(p.amount_submitted, p.amount_offered)) is not None
        ]
        ratio = calc.bid_to_cover(latest.amount_submitted, latest.amount_offered)
        z = calc.z_score(ratio, peers) if len(peers) >= r["min_peers"] else None
        prev = series[-2] if len(series) > 1 else None
        cells[country_id][bucket] = HeatCell(
            bucket=bucket,
            tenor_days=tenor,
            instrument_type=instrument,
            auction_id=latest.auction_id,
            auction_date=latest.auction_date,
            weighted_average_yield=latest.weighted_average_yield,
            bid_to_cover=calc.quantize(ratio),
            demand_z=calc.quantize(z, 2),
            demand_peer_count=len(peers),
            yield_change_bps=calc.quantize(
                calc.change_bps(latest.weighted_average_yield, prev.weighted_average_yield if prev else None), 2
            ),
            is_synthetic=latest.is_synthetic,
        )
    counts = _active_counts(session)
    countries = session.scalars(select(Country).where(Country.is_monitored).order_by(Country.name)).all()
    return HeatGrid(
        as_of=as_of,
        buckets=[b for b, _ in BUCKETS],
        rows=[
            HeatRow(
                country_iso3=c.iso3,
                country_name=c.name,
                currency=c.currency,
                active_opportunities=counts.get(c.country_id, 0),
                cells=sorted(cells.get(c.country_id, {}).values(), key=lambda x: x.tenor_days),
            )
            for c in countries
            if c.country_id in cells  # countries without recent auction data are not gridded
        ],
        method=(
            f"Latest completed auction per country and tenor bucket within {lookback} days. "
            f"demand_z = (bid-to-cover − mean of up to {r['max_peers']} previous same-tenor auctions) "
            f"/ their sample stdev; shown only with ≥ {r['min_peers']} previous auctions."
        ),
        caveat="Yields are as published and may use different conventions across markets; compare "
        "demand_z across countries, not raw yields.",
    )


@router.get("/countries/{iso3}/maturity-wall", response_model=MaturityWall)
def maturity_wall(iso3: str, session: SessionDep, as_of: AsOfDep) -> MaturityWall:
    country = session.scalar(select(Country).where(Country.iso3 == iso3.upper()))
    if country is None:
        raise HTTPException(404, "Country not found")
    wall = maturity_walls(load_market(session, as_of)).get(country.country_id)
    months = wall["months"] if wall else []
    total = sum((mo["amount"] for mo in months), Decimal(0))
    return MaturityWall(
        country_iso3=country.iso3,
        currency=country.currency,
        as_of=as_of,
        total=total,
        months=[
            WallMonth(
                month=mo["month"],
                amount=mo["amount"],
                securities=mo["securities"],
                share_pct=calc.quantize(mo["amount"] / total * 100, 2) if total else None,
            )
            for mo in months
        ],
        data_nature=DataNature.SYNTHETIC if wall and wall["is_synthetic"] else DataNature.FACT,
        caveat="Allocated amounts of auctioned securities tracked here, by maturity month. Excludes "
        "Eurobonds, loans and private placements; not a full debt-service schedule.",
    )
