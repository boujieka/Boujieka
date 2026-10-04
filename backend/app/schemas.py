"""API response models.

Decimal values serialise as JSON strings to preserve exact precision.
Every market-data payload separates:
  official    — values as published by the source (data_nature FACT, or SYNTHETIC)
  calculated  — values we derived (data_nature CALCULATION), with their definitions
  provenance  — where the official values came from
Empty official fields are explained in `field_status` (not_disclosed / not_available / pending).
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from app.models.enums import (
    AuctionStatus,
    AuctionType,
    DataNature,
    InstrumentType,
    CoverageTier,
    MonetaryZone,
    SourceCategory,
    SourceStatus,
    VerificationStatus,
)


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SourceRef(ORM):
    source_id: int
    name: str
    institution: str
    category: SourceCategory
    is_synthetic: bool


class Provenance(BaseModel):
    data_nature: DataNature
    verification_status: VerificationStatus
    confidence_score: Decimal | None
    is_synthetic: bool
    source: SourceRef | None
    source_url: str | None
    source_document_id: int | None
    publication_date: date | None
    extracted_at: datetime | None
    notes: str | None


class CountryOut(BaseModel):
    country_id: int
    name: str
    name_fr: str | None
    region: str | None
    # Computed from data actually held: "market_data" if any security is loaded, else "reference_only".
    coverage_tier: CoverageTier
    iso2: str
    iso3: str
    currency: str
    monetary_zone: MonetaryZone
    central_bank: str | None
    debt_management_office: str | None
    primary_market_structure: str | None
    secondary_market_structure: str | None
    tax_notes: str | None
    capital_controls: str | None
    market_access_notes: str | None
    last_verified: date | None
    field_status: dict[str, str]
    provenance: Provenance


class CountryDetail(CountryOut):
    upcoming_auction_count: int
    completed_auction_count: int
    security_count: int
    sources: list["SourceOut"]


class SecuritySummary(BaseModel):
    security_id: int
    security_name: str
    instrument_type: InstrumentType
    tenor_days: int | None
    maturity_date: date | None
    currency: str
    country_iso3: str
    country_name: str
    is_synthetic: bool


class SecurityOut(SecuritySummary):
    isin: str | None
    local_code: str | None
    face_value: Decimal | None
    coupon_rate: Decimal | None
    coupon_frequency: str | None
    issue_date: date | None
    amortization: str | None
    indexation: str | None
    green_social_sustainability_flag: str | None
    listing_status: str | None
    minimum_denomination: Decimal | None
    field_status: dict[str, str]
    provenance: Provenance


class AuctionOfficial(BaseModel):
    amount_offered: Decimal | None
    amount_submitted: Decimal | None
    amount_allocated: Decimal | None
    minimum_bid: Decimal | None
    maximum_bid: Decimal | None
    cutoff_yield: Decimal | None
    weighted_average_yield: Decimal | None
    average_price: Decimal | None
    reported_bid_to_cover: Decimal | None
    number_of_bidders: int | None
    number_of_successful_bidders: int | None
    yield_convention: str | None


class AuctionCalculated(BaseModel):
    data_nature: DataNature = DataNature.CALCULATION
    bid_to_cover: Decimal | None
    bid_to_cover_definition: str = "amount_submitted / amount_offered"
    allocation_rate: Decimal | None
    allocation_rate_definition: str = "amount_allocated / amount_offered"
    acceptance_rate: Decimal | None
    acceptance_rate_definition: str = "amount_allocated / amount_submitted"


class AuctionOut(BaseModel):
    auction_id: int
    status: AuctionStatus
    auction_type: AuctionType
    announcement_date: date | None
    auction_date: date
    settlement_date: date | None
    security: SecuritySummary
    official: AuctionOfficial
    calculated: AuctionCalculated
    field_status: dict[str, str]
    provenance: Provenance


class HistoricalComparison(BaseModel):
    """Comparison with previous completed auctions of the same country, instrument and tenor."""

    data_nature: DataNature = DataNature.CALCULATION
    peer_definition: str
    previous_auction_id: int | None
    yield_change_bps: Decimal | None
    yield_change_definition: str = "weighted_average_yield minus previous, in basis points"
    peer_average_bid_to_cover: Decimal | None
    peer_count: int
    caveat: str | None


class AuctionDetail(AuctionOut):
    comparison: HistoricalComparison
    peers: list[AuctionOut]


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int


class SecurityDetail(SecurityOut):
    auctions: list[AuctionOut]


class YieldCurvePoint(BaseModel):
    tenor_days: int
    instrument_type: InstrumentType
    weighted_average_yield: Decimal
    auction_id: int
    auction_date: date
    yield_convention: str | None
    is_synthetic: bool


class YieldCurve(BaseModel):
    country_iso3: str
    as_of: date
    lookback_days: int
    method: str
    caveat: str
    points: list[YieldCurvePoint]


class SourceCandidate(BaseModel):
    """A proposed URL. Unconfirmed: never used for crawling until an operator sets base_url."""

    url: str
    purpose: str
    check: str  # http_200 | http_403 | search_only
    evidence: str


class SourceOut(ORM):
    source_id: int
    name: str
    institution: str
    category: SourceCategory
    priority: int
    country_id: int | None
    base_url: str | None
    status: SourceStatus
    last_checked_at: datetime | None
    last_success_at: datetime | None
    last_error: str | None
    notes: str | None
    is_synthetic: bool
    candidates: list[SourceCandidate]


class AmountByCurrency(BaseModel):
    currency: str
    amount: Decimal


class DashboardSummary(BaseModel):
    as_of: date
    countries_monitored: int
    countries_with_market_data: int
    upcoming_auctions_7d: int
    upcoming_auctions_30d: int
    results_last_7d: int
    announced_issuance_by_currency: list[AmountByCurrency]
    cancelled_or_postponed: int
    sources_pending_configuration: int
    synthetic_records_present: bool
    new_opportunities: int  # active Opportunity Engine signals
    alerts: int | None  # None until alerts (Phase 5) exist


class MissingFieldStat(BaseModel):
    field: str
    missing: int
    not_disclosed: int
    pending: int
    total: int


class DataQualityReport(BaseModel):
    as_of: date
    sources_total: int
    sources_pending_configuration: list[SourceOut]
    sources_stale: list[SourceOut]
    sources_failing: list[SourceOut]
    auction_missing_fields: list[MissingFieldStat]
    low_confidence_records: int
    unverified_records: int
    synthetic_auctions: int
    synthetic_securities: int
    duplicate_candidates: int
    duplicate_definition: str


CountryDetail.model_rebuild()


class OpportunityOut(BaseModel):
    opportunity_id: int
    opportunity_type: str
    label: str
    country_iso3: str
    country_name: str
    currency: str | None
    security: SecuritySummary | None
    auction_id: int | None
    auction_date: date | None
    yield_pct: Decimal | None
    maturity: date | None
    strength: Decimal | None
    strength_definition: str = "How far past the rule's threshold the signal is (1.0 = at threshold)"
    explanation: str | None
    evidence: dict
    risk_flags: list[str]
    data_confidence: Decimal | None
    is_synthetic: bool
    as_of: date
    is_active: bool
    # Investor-criteria matching; None when no criteria were supplied.
    matches_criteria: bool | None = None
    criteria_unmet: list[str] = []


class OpportunityPage(BaseModel):
    items: list[OpportunityOut]
    total: int
    by_type: dict[str, int]
    by_country: dict[str, int]
    criteria: dict[str, str]
    disclaimer: str


class HeatCell(BaseModel):
    bucket: str
    tenor_days: int
    instrument_type: InstrumentType
    auction_id: int
    auction_date: date
    weighted_average_yield: Decimal | None
    bid_to_cover: Decimal | None
    demand_z: Decimal | None
    demand_peer_count: int
    yield_change_bps: Decimal | None
    is_synthetic: bool


class HeatRow(BaseModel):
    country_iso3: str
    country_name: str
    currency: str
    active_opportunities: int
    cells: list[HeatCell]


class HeatGrid(BaseModel):
    as_of: date
    buckets: list[str]
    rows: list[HeatRow]
    method: str
    caveat: str


class WallMonth(BaseModel):
    month: str
    amount: Decimal
    securities: int
    share_pct: Decimal | None


class MaturityWall(BaseModel):
    country_iso3: str
    currency: str
    as_of: date
    total: Decimal
    months: list[WallMonth]
    data_nature: DataNature
    caveat: str


class SubscriptionRouteOut(BaseModel):
    """Procedural access route, backed by verbatim quotes from the official page. Not advice."""

    country_iso3: str
    country_name: str
    monetary_zone: MonetaryZone
    instrument_type: InstrumentType
    investor_type: str
    eligibility: str | None
    primary_dealer: str | None
    account_requirement: str | None
    submission_method: str | None
    settlement_method: str | None
    fees: str | None  # None = not stated by the source ("Not available")
    taxes: str | None
    instrument_notes: str | None
    official_source_url: str | None
    last_verified: date | None
    quotes: list[str]
    data_nature: DataNature = DataNature.FACT
    disclaimer: str = "Procedural information from official pages; access is not guaranteed and this is not advice."


class DealerSourceOut(BaseModel):
    """Official document listing accredited auction participants."""

    id: str
    lang: str  # language of title and quote (fr | en); notes are written in French
    institution: str
    title: str
    countries: list[str]
    measure: str  # "list" | "rank" | "share": what the document publishes per institution
    basis: str | None
    page_url: str
    document_url: str | None
    document_date: str
    quote: str
    note: str | None
    verified_on: date
    data_nature: DataNature = DataNature.FACT


class DealerOut(BaseModel):
    source_id: str
    country_iso3: str
    name: str  # exactly as printed in the source
    kind: str  # SVT | primary_dealer | PD_BMS | IVT
    market_share_pct: Decimal | None  # only where the authority publishes it per institution
    rank: int | None


class AccreditedDealers(BaseModel):
    sources: list[DealerSourceOut]
    dealers: list[DealerOut]
    disclaimer: str = (
        "Official lists only. Shares and ranks are reproduced as published, never estimated. "
        "A listing is not a recommendation; dealers' commercial terms are not published by these sources."
    )


class ExtractedField(BaseModel):
    """One value read from an official document, with where it was read and how sure we are."""

    value: str | None
    raw: str
    locator: str
    confidence: float
    unit: str | None = None
    note: str | None = None


class ExtractionDocument(ORM):
    document_id: int
    url: str | None
    title: str
    document_type: str
    publication_date: date | None
    retrieved_at: datetime | None
    content_sha256: str | None
    extraction_status: str


class ExtractionOut(BaseModel):
    """A staged extraction. UNVERIFIED rows are NOT facts yet: they await human review."""

    extraction_id: int
    verification_status: VerificationStatus
    data_nature: DataNature
    notice: str
    parse_status: str
    confidence_score: Decimal | None
    extractor: str
    tranche_key: str
    country_iso3: str | None
    isin: str | None
    instrument: str | None
    auction_date: date | None
    fields: dict[str, ExtractedField]
    field_status: dict[str, str]
    operation: dict
    warnings: list[str]
    checks: list[dict]
    document: ExtractionDocument | None
    extracted_at: datetime | None
    reviewed_by: str | None
    reviewed_at: datetime | None
    review_reason: str | None
    promoted_auction_id: int | None
