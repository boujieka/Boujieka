"""Alerts, Project Rescue, AI assessments, commerce, reports, notifications (§20, §21, §22, §26, §27)."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import JSON, Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, Money, Timestamped, utcnow


class ProjectAlert(Base):
    __tablename__ = "project_alerts"
    __table_args__ = (UniqueConstraint("alert_key"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_key: Mapped[str] = mapped_column(String(64))  # stable hash(rule, project, evidence) for idempotency
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    rule_code: Mapped[str] = mapped_column(String(60), index=True)
    level: Mapped[str] = mapped_column(String(30), index=True)
    triggering_indicator: Mapped[str] = mapped_column(String(120))
    observed_value: Mapped[str | None] = mapped_column(Text)
    threshold: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(Text)
    source_record_ids: Mapped[list] = mapped_column(JSON, default=list)
    as_of: Mapped[date] = mapped_column(Date)
    explanation: Mapped[str] = mapped_column(Text)
    recommended_verification: Mapped[str] = mapped_column(Text)
    review_status: Mapped[str] = mapped_column(String(20), default="open", index=True)
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    review_note: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    @property
    def public_id(self) -> str:
        return f"ALR-{self.id:07d}"


class AlertThreshold(Base):
    """Institution-configurable thresholds (organization_id NULL = AP²I default)."""

    __tablename__ = "alert_thresholds"
    __table_args__ = (UniqueConstraint("organization_id", "rule_code", "parameter"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"))
    rule_code: Mapped[str] = mapped_column(String(60))
    parameter: Mapped[str] = mapped_column(String(60))
    value: Mapped[Decimal] = mapped_column(Money)


class RecoveryPlan(Base, Timestamped):
    __tablename__ = "recovery_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    tenant_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    title: Mapped[str] = mapped_column(Text)
    diagnosis: Mapped[dict] = mapped_column(JSON, default=dict)  # structured, evidence-linked
    status: Mapped[str] = mapped_column(String(20), default="draft")
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    method: Mapped[str] = mapped_column(String(40), default="rules_v1")

    actions: Mapped[list["RecoveryAction"]] = relationship(back_populates="plan", cascade="all, delete-orphan")


class RecoveryAction(Base, Timestamped):
    __tablename__ = "recovery_actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("recovery_plans.id", ondelete="CASCADE"), index=True)
    problem: Mapped[str] = mapped_column(Text)
    evidence: Mapped[list] = mapped_column(JSON, default=list)  # [{alert_id, indicator, value, source}]
    contributing_factors: Mapped[str] = mapped_column(Text)
    recommended_action: Mapped[str] = mapped_column(Text)
    responsible_institution: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(20))
    estimated_timeframe: Mapped[str | None] = mapped_column(String(120))
    indicative_budget: Mapped[Decimal | None] = mapped_column(Money)
    budget_currency: Mapped[str | None] = mapped_column(String(3))
    dependencies: Mapped[str | None] = mapped_column(Text)
    expected_result: Mapped[str | None] = mapped_column(Text)
    monitoring_indicator: Mapped[str | None] = mapped_column(Text)
    origin: Mapped[str] = mapped_column(String(20), default="rule")  # rule | ai | user
    data_nature: Mapped[str] = mapped_column(String(30), default="calculated")
    approval_status: Mapped[str] = mapped_column(String(20), default="proposed")
    implementation_status: Mapped[str] = mapped_column(String(20), default="not_started")
    assigned_to: Mapped[str | None] = mapped_column(Text)
    due_date: Mapped[date | None] = mapped_column(Date)
    progress_note: Mapped[str | None] = mapped_column(Text)
    decided_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    plan: Mapped[RecoveryPlan] = relationship(back_populates="actions")


class AIAssessment(Base):
    __tablename__ = "ai_assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    tenant_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"))
    kind: Mapped[str] = mapped_column(String(40))  # assistant_answer | recovery_recommendation | extraction
    provider: Mapped[str] = mapped_column(String(40))
    model: Mapped[str | None] = mapped_column(String(80))
    question: Mapped[str | None] = mapped_column(Text)
    output: Mapped[dict] = mapped_column(JSON, default=dict)
    citations: Mapped[list] = mapped_column(JSON, default=list)
    grounding_check: Mapped[dict] = mapped_column(JSON, default=dict)
    review_status: Mapped[str] = mapped_column(String(20), default="unreviewed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Plan(Base):
    """Subscription plans; price and features are configuration (§26)."""

    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True)
    name_en: Mapped[str] = mapped_column(String(80))
    name_fr: Mapped[str] = mapped_column(String(80))
    price_amount: Mapped[Decimal | None] = mapped_column(Money)  # NULL = "on request"
    price_currency: Mapped[str | None] = mapped_column(String(3))
    billing_period: Mapped[str | None] = mapped_column(String(20))
    features: Mapped[list] = mapped_column(JSON, default=list)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class Subscription(Base, Timestamped):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active | trial | cancelled | pending_payment
    starts_on: Mapped[date | None] = mapped_column(Date)
    ends_on: Mapped[date | None] = mapped_column(Date)
    seats: Mapped[int | None] = mapped_column(Integer)

    plan: Mapped[Plan] = relationship()


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"), index=True)
    provider: Mapped[str] = mapped_column(String(40))
    provider_reference: Mapped[str | None] = mapped_column(String(200))
    amount: Mapped[Decimal] = mapped_column(Money)
    currency: Mapped[str] = mapped_column(String(3))
    status: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_uid: Mapped[str] = mapped_column(String(40), unique=True)
    report_type: Mapped[str] = mapped_column(String(40))
    title: Mapped[str] = mapped_column(Text)
    fmt: Mapped[str] = mapped_column(String(10))
    params: Mapped[dict] = mapped_column(JSON, default=dict)
    period: Mapped[str | None] = mapped_column(String(40))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    generated_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    tenant_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"))
    sha256: Mapped[str] = mapped_column(String(64))
    size_bytes: Mapped[int] = mapped_column(Integer)
    storage_key: Mapped[str] = mapped_column(Text)


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"))
    kind: Mapped[str] = mapped_column(String(40))  # sync_failed | alert | action_due | review_needed
    title: Mapped[str] = mapped_column(Text)
    body: Mapped[str | None] = mapped_column(Text)
    link: Mapped[str | None] = mapped_column(Text)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    query: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AppSetting(Base):
    """Admin-editable runtime settings (AI config, rescue config, schedules)."""

    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String(80), primary_key=True)
    value: Mapped[dict] = mapped_column(JSON)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
