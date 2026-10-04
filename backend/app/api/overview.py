"""Dashboard summary, source registry and data-quality endpoints."""

from datetime import datetime, time, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select

from app.api.serializers import AUCTION_OFFICIAL_FIELDS
from app.api.deps import AsOfDep, SessionDep
from app.config import get_settings
from app.models import Auction, Country, Opportunity, Security, Source
from app.models.enums import AuctionStatus, FieldStatus, Role, SourceStatus, VerificationStatus
from app.schemas import (
    AmountByCurrency,
    DashboardSummary,
    DataQualityReport,
    MissingFieldStat,
    SourceOut,
)
from app.security.auth import require_role

router = APIRouter(tags=["overview"])


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(session: SessionDep, as_of: AsOfDep) -> DashboardSummary:
    def count(*where) -> int:
        return session.scalar(select(func.count()).select_from(Auction).where(*where)) or 0

    upcoming = (Auction.status == AuctionStatus.ANNOUNCED, Auction.auction_date >= as_of)
    issuance = session.execute(
        select(Security.currency, func.sum(Auction.amount_offered))
        .join(Auction.security)
        .where(*upcoming, Auction.auction_date <= as_of + timedelta(days=30))
        .group_by(Security.currency)
        .order_by(Security.currency)
    ).all()
    return DashboardSummary(
        as_of=as_of,
        countries_with_market_data=session.scalar(
            select(func.count(func.distinct(Security.country_id)))
        )
        or 0,
        countries_monitored=session.scalar(
            select(func.count()).select_from(Country).where(Country.is_monitored)
        )
        or 0,
        upcoming_auctions_7d=count(*upcoming, Auction.auction_date <= as_of + timedelta(days=7)),
        upcoming_auctions_30d=count(*upcoming, Auction.auction_date <= as_of + timedelta(days=30)),
        results_last_7d=count(
            Auction.status == AuctionStatus.COMPLETED,
            Auction.auction_date <= as_of,
            Auction.auction_date > as_of - timedelta(days=7),
        ),
        announced_issuance_by_currency=[
            AmountByCurrency(currency=c, amount=amt) for c, amt in issuance if amt is not None
        ],
        cancelled_or_postponed=count(
            Auction.status.in_([AuctionStatus.CANCELLED, AuctionStatus.POSTPONED]),
            Auction.auction_date >= as_of,
        ),
        sources_pending_configuration=session.scalar(
            select(func.count())
            .select_from(Source)
            .where(Source.status == SourceStatus.PENDING_CONFIGURATION)
        )
        or 0,
        synthetic_records_present=session.scalar(
            select(func.count()).select_from(Auction).where(Auction.is_synthetic)
        )
        > 0,
        new_opportunities=session.scalar(
            select(func.count()).select_from(Opportunity).where(Opportunity.is_active.is_(True))
        )
        or 0,
        alerts=None,
    )


@router.get("/sources", response_model=list[SourceOut])
def list_sources(session: SessionDep) -> list[SourceOut]:
    rows = sorted(session.scalars(select(Source)), key=lambda s: (s.priority, s.name))
    return [SourceOut.model_validate(s) for s in rows]


# Internal operations view: analysts and admins only (and audited).
@router.get(
    "/data-quality",
    response_model=DataQualityReport,
    dependencies=[Depends(require_role(Role.ANALYST, Role.ADMIN))],
)
def data_quality(session: SessionDep, as_of: AsOfDep) -> DataQualityReport:
    settings = get_settings()
    sources = session.scalars(select(Source).order_by(Source.name)).all()
    stale_before = datetime.combine(as_of, time.min, tzinfo=timezone.utc) - timedelta(
        hours=settings.source_stale_after_hours
    )

    def is_stale(s: Source) -> bool:
        if s.status != SourceStatus.ACTIVE or s.is_synthetic:
            return False
        last = s.last_success_at
        if last is not None and last.tzinfo is None:  # SQLite drops tz info
            last = last.replace(tzinfo=timezone.utc)
        return last is None or last < stale_before

    # Missing-field stats over completed auctions only: announced auctions have no results yet.
    completed = session.scalars(
        select(Auction).where(Auction.status == AuctionStatus.COMPLETED)
    ).all()
    missing_stats = []
    for field in AUCTION_OFFICIAL_FIELDS:
        empty = [a for a in completed if getattr(a, field) is None]
        reasons = [(a.field_status or {}).get(field) for a in empty]
        missing_stats.append(
            MissingFieldStat(
                field=field,
                missing=len(empty),
                not_disclosed=reasons.count(FieldStatus.NOT_DISCLOSED.value),
                pending=reasons.count(FieldStatus.PENDING.value),
                total=len(completed),
            )
        )

    # Natural key (security, date, type) is enforced by a unique constraint, so exact duplicates
    # cannot exist. Flag likely duplicates captured under different security records instead.
    dup_groups = (
        select(func.count())
        .select_from(Auction)
        .join(Auction.security)
        .group_by(
            Security.country_id,
            Security.instrument_type,
            Security.tenor_days,
            Auction.auction_date,
            Auction.amount_offered,
        )
        .having(func.count() > 1)
    ).subquery()

    def count(model, *where) -> int:
        return session.scalar(select(func.count()).select_from(model).where(*where)) or 0

    return DataQualityReport(
        as_of=as_of,
        sources_total=len(sources),
        sources_pending_configuration=[
            SourceOut.model_validate(s)
            for s in sources
            if s.status == SourceStatus.PENDING_CONFIGURATION
        ],
        sources_stale=[SourceOut.model_validate(s) for s in sources if is_stale(s)],
        sources_failing=[
            SourceOut.model_validate(s) for s in sources if s.status == SourceStatus.FAILING
        ],
        auction_missing_fields=missing_stats,
        low_confidence_records=count(
            Auction,
            Auction.confidence_score.is_not(None),
            Auction.confidence_score < settings.low_confidence_threshold,
        ),
        unverified_records=count(Auction, Auction.verification_status == VerificationStatus.UNVERIFIED)
        + count(Security, Security.verification_status == VerificationStatus.UNVERIFIED)
        + count(Country, Country.verification_status == VerificationStatus.UNVERIFIED),
        synthetic_auctions=count(Auction, Auction.is_synthetic),
        synthetic_securities=count(Security, Security.is_synthetic),
        duplicate_candidates=session.scalar(select(func.count()).select_from(dup_groups)) or 0,
        duplicate_definition=(
            "Groups of auctions sharing country, instrument type, tenor, auction date and "
            "amount offered but recorded against different securities."
        ),
    )
