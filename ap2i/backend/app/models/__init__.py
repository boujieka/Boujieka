"""All ORM models; importing this package registers every table on Base.metadata."""

from app.models.base import Base
from app.models.reference import (
    AdminRegion,
    Country,
    CountryDataSource,
    FinancingInstrument,
    FinancingPartner,
    Organization,
    Sector,
    SectorIndicator,
    Subsector,
)
from app.models.auth import ApiKey, AuditLog, RoleDef, User, UserRole, UserToken
from app.models.ingest import (
    DataQualityAssessment,
    DataValidation,
    MatchCandidate,
    ProjectSourceLink,
    SourceConnector,
    SourceObservation,
    SourceRecord,
    SyncRun,
)
from app.models.project import (
    Document,
    IdSequence,
    ImplementationProgress,
    OperationalStatusObservation,
    Project,
    ProjectAlias,
    ProjectIdentifier,
    ProjectLocation,
    ProjectMerge,
    ProjectMilestone,
    ProjectRisk,
    ProjectStatusHistory,
    ResultsIndicator,
    ResultsObservation,
)
from app.models.finance import (
    AnnualFinancialSnapshot,
    BudgetAllocation,
    Contract,
    ContractAmendment,
    CounterpartFinancing,
    Disbursement,
    ExchangeRate,
    FinancingAgreement,
    FinancingCommitment,
)
from app.models.ops import (
    AIAssessment,
    AlertThreshold,
    AppSetting,
    Notification,
    Payment,
    Plan,
    ProjectAlert,
    RecoveryAction,
    RecoveryPlan,
    Report,
    SavedSearch,
    Subscription,
)

__all__ = [name for name in dir() if not name.startswith("_")]
