"""Controlled vocabularies.

Stored as VARCHAR (non-native enums) so adding a value never needs a Postgres
ALTER TYPE migration and the schema stays portable.
"""

from enum import StrEnum


class DataNature(StrEnum):
    """What kind of claim a value is. The platform never mixes these."""

    FACT = "FACT"  # As published by the cited source.
    CALCULATION = "CALCULATION"  # Derived deterministically from FACT values.
    ESTIMATE = "ESTIMATE"  # Modelled or assumed; must be labelled as such.
    AI_INTERPRETATION = "AI_INTERPRETATION"  # LLM-written narrative; never a data source.
    SYNTHETIC = "SYNTHETIC"  # Generated for development/demo. NOT real market data.


class VerificationStatus(StrEnum):
    VERIFIED = "verified"  # Checked against the official source document.
    UNVERIFIED = "unverified"  # Captured but not yet checked.
    CONFLICTING = "conflicting"  # Sources disagree; needs review.
    REJECTED = "rejected"  # Failed validation; kept for audit only.
    SYNTHETIC = "synthetic"  # Not real data.


class FieldStatus(StrEnum):
    """Why a field is empty. A null with no status means "Not available"."""

    NOT_DISCLOSED = "not_disclosed"  # Source exists but does not publish this field.
    NOT_AVAILABLE = "not_available"  # We have no source for this field.
    PENDING = "pending"  # Expected later (e.g. result before the auction is held).


class MonetaryZone(StrEnum):
    CEMAC = "CEMAC"
    WAEMU = "WAEMU"
    NONE = "NONE"  # Country has its own currency / central bank.


class InstrumentType(StrEnum):
    TREASURY_BILL = "treasury_bill"
    TREASURY_BOND = "treasury_bond"
    EUROBOND = "eurobond"
    INFRASTRUCTURE_BOND = "infrastructure_bond"
    SUKUK = "sukuk"
    REGIONAL_BOND = "regional_bond"  # e.g. public offering on a regional exchange
    OTHER = "other"


class AuctionType(StrEnum):
    PRIMARY_AUCTION = "primary_auction"
    REOPENING = "reopening"
    TAP = "tap"
    SYNDICATION = "syndication"
    PUBLIC_OFFERING = "public_offering"
    BUYBACK = "buyback"
    SWITCH = "switch"


class AuctionStatus(StrEnum):
    ANNOUNCED = "announced"
    COMPLETED = "completed"  # Results published.
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class SourceCategory(StrEnum):
    """Ordered by priority: lower rank = more authoritative."""

    CENTRAL_BANK = "central_bank"
    MINISTRY_OF_FINANCE = "ministry_of_finance"
    DEBT_MANAGEMENT_OFFICE = "debt_management_office"
    STOCK_EXCHANGE = "stock_exchange"
    AUCTION_PLATFORM = "auction_platform"
    REGIONAL_INSTITUTION = "regional_institution"
    GOVERNMENT_PUBLICATION = "government_publication"
    INVESTOR_RELATIONS = "investor_relations"
    MARKET_DATA_PROVIDER = "market_data_provider"
    FINANCIAL_NEWS = "financial_news"
    SYNTHETIC = "synthetic"


SOURCE_PRIORITY: dict[SourceCategory, int] = {c: i + 1 for i, c in enumerate(SourceCategory)}


class SourceStatus(StrEnum):
    ACTIVE = "active"
    PENDING_CONFIGURATION = "pending_configuration"  # URL/crawler not yet confirmed by an operator.
    DISABLED = "disabled"
    FAILING = "failing"


class IssuerType(StrEnum):
    SOVEREIGN = "sovereign"
    SUB_SOVEREIGN = "sub_sovereign"
    SUPRANATIONAL = "supranational"
    STATE_OWNED_ENTERPRISE = "state_owned_enterprise"


class CouponFrequency(StrEnum):
    ZERO = "zero"  # Discount instrument
    ANNUAL = "annual"
    SEMI_ANNUAL = "semi_annual"
    QUARTERLY = "quarterly"


class ObservationKind(StrEnum):
    AUCTION = "auction"
    SECONDARY_MARKET = "secondary_market"
    INDICATIVE = "indicative"
