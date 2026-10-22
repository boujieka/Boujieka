"""Controlled vocabularies. Stored as plain strings (portable, migration-friendly)."""

from enum import StrEnum


class DataNature(StrEnum):
    """The six kinds of information AP²I must keep apart (Master prompt §3)."""

    OFFICIALLY_REPORTED = "officially_reported"  # published by the source, not independently checked
    VERIFIED = "verified"  # checked by an AP²I reviewer against the source document
    CALCULATED = "calculated"  # derived by AP²I with a documented formula
    ESTIMATED = "estimated"  # an estimate, always labelled with its method
    AI_GENERATED = "ai_generated"  # produced by an AI model; never a fact
    MISSING = "missing"  # explicitly not available — never replaced by zero
    SYNTHETIC = "synthetic"  # test/dev fixtures only; refused in production


class VerificationStatus(StrEnum):
    UNVERIFIED = "unverified"
    NEEDS_REVIEW = "needs_review"
    VERIFIED = "verified"
    REJECTED = "rejected"


class ProjectStatus(StrEnum):
    PIPELINE = "pipeline"
    APPROVED = "approved"
    ACTIVE = "active"
    COMPLETED = "completed"
    CLOSED = "closed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    DROPPED = "dropped"
    UNKNOWN = "unknown"


class OperationalStatus(StrEnum):
    OPERATIONAL = "operational"
    PARTIALLY_OPERATIONAL = "partially_operational"
    NOT_OPERATIONAL = "not_operational"
    UNKNOWN = "unknown"


class ConnectorStatus(StrEnum):
    """A connector is OPERATIONAL only after real records were retrieved, parsed, validated, stored."""

    OPERATIONAL = "operational"
    PARTIAL = "partial"
    NOT_TESTED = "not_tested"
    BLOCKED = "blocked"  # source unreachable or credentials missing
    NOT_IMPLEMENTED = "not_implemented"
    MANUAL = "manual"  # documented official-data import workflow


class AlertLevel(StrEnum):
    INFORMATION = "information"
    WATCH = "watch"
    HIGH_ATTENTION = "high_attention"
    CRITICAL_ATTENTION = "critical_attention"


class ReviewStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    CONFIRMED = "confirmed"
    DISMISSED = "dismissed"
    RESOLVED = "resolved"


class ApprovalStatus(StrEnum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"


class ActionStatus(StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"


class FlowType(StrEnum):
    """Never confuse these (Master prompt §13, §16)."""

    COMMITMENT = "commitment"
    DISBURSEMENT = "disbursement"
    EXPENDITURE = "expenditure"
    BUDGET_APPROPRIATION = "budget_appropriation"
    CONTRACT_PAYMENT = "contract_payment"


class FundingType(StrEnum):
    GOVERNMENT = "government_funded"
    EXTERNAL = "externally_funded"
    CO_FINANCED = "co_financed"
    PPP = "public_private_partnership"
    SOE = "state_owned_enterprise"
    UNKNOWN = "unknown"


class Role(StrEnum):
    PUBLIC_VISITOR = "public_visitor"
    REGISTERED_USER = "registered_user"
    PROFESSIONAL_SUBSCRIBER = "professional_subscriber"
    GOVERNMENT_ANALYST = "government_analyst"
    GOVERNMENT_ADMINISTRATOR = "government_administrator"
    DFI_ANALYST = "dfi_analyst"
    INSTITUTIONAL_ADMINISTRATOR = "institutional_administrator"
    DATA_CONTRIBUTOR = "data_contributor"
    DATA_REVIEWER = "data_reviewer"
    SUPER_ADMIN = "ap2i_super_admin"


class MatchStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
