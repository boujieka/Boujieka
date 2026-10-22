"""Financing, flows, contracts, budget and exchange rates (Master prompt §13, §16, §17)."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, Money, Rate, Timestamped, utcnow


class FinancingAgreement(Base, Timestamped):
    """One financing from one partner to one master project. A project may have many."""

    __tablename__ = "financing_agreements"
    __table_args__ = (UniqueConstraint("partner_id", "source_identifier"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    partner_id: Mapped[int | None] = mapped_column(ForeignKey("financing_partners.id"), index=True)
    instrument_id: Mapped[int | None] = mapped_column(ForeignKey("financing_instruments.id"))
    tenant_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    source_identifier: Mapped[str] = mapped_column(String(120))  # e.g. P181491, 46002-P-CM-..., FR-3-CCM127602
    name: Mapped[str | None] = mapped_column(Text)
    instrument_label: Mapped[str | None] = mapped_column(String(200))  # original source wording
    approval_date: Mapped[date | None] = mapped_column(Date, index=True)
    signature_date: Mapped[date | None] = mapped_column(Date)
    effectiveness_date: Mapped[date | None] = mapped_column(Date)
    closing_date_original: Mapped[date | None] = mapped_column(Date)
    closing_date_current: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="unknown")
    currency: Mapped[str | None] = mapped_column(String(3))
    # Amount as published at approval/signature, in the original currency. NULL = not published.
    amount_original: Mapped[Decimal | None] = mapped_column(Money)
    amount_label: Mapped[str | None] = mapped_column(String(200))  # which source field the amount is
    # Cumulative figures as published by the source at a point in time (not annual flows).
    reported_current_commitment: Mapped[Decimal | None] = mapped_column(Money)
    reported_cumulative_disbursed: Mapped[Decimal | None] = mapped_column(Money)
    reported_undisbursed: Mapped[Decimal | None] = mapped_column(Money)
    reported_cumulative_as_of: Mapped[date | None] = mapped_column(Date)
    reported_cumulative_label: Mapped[str | None] = mapped_column(String(300))
    parent_source_identifier: Mapped[str | None] = mapped_column(String(120))  # e.g. WB parentprojid
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")
    verification_status: Mapped[str] = mapped_column(String(20), default="unverified")

    project = relationship("Project", back_populates="agreements")
    partner = relationship("FinancingPartner")
    instrument = relationship("FinancingInstrument")
    commitments: Mapped[list["FinancingCommitment"]] = relationship(back_populates="agreement")
    disbursements: Mapped[list["Disbursement"]] = relationship(back_populates="agreement")


class FinancingCommitment(Base):
    """Commitment events: original, additional, cancellation (negative), revision."""

    __tablename__ = "financing_commitments"
    __table_args__ = (UniqueConstraint("agreement_id", "transaction_key"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    agreement_id: Mapped[int] = mapped_column(ForeignKey("financing_agreements.id", ondelete="CASCADE"), index=True)
    commitment_type: Mapped[str] = mapped_column(String(20))  # original | additional | cancellation | revision
    amount: Mapped[Decimal] = mapped_column(Money)
    currency: Mapped[str] = mapped_column(String(3))
    value_date: Mapped[date | None] = mapped_column(Date, index=True)
    transaction_key: Mapped[str] = mapped_column(String(200))  # idempotency key from the source
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")
    # Anti double-counting: when two sources report the same commitment, only one is counted.
    is_counted: Mapped[bool] = mapped_column(Boolean, default=True)
    counting_note: Mapped[str | None] = mapped_column(Text)

    agreement: Mapped[FinancingAgreement] = relationship(back_populates="commitments")


class Disbursement(Base):
    __tablename__ = "disbursements"
    __table_args__ = (UniqueConstraint("agreement_id", "transaction_key"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    agreement_id: Mapped[int] = mapped_column(ForeignKey("financing_agreements.id", ondelete="CASCADE"), index=True)
    flow_type: Mapped[str] = mapped_column(String(20), default="disbursement")  # disbursement | expenditure
    amount: Mapped[Decimal] = mapped_column(Money)
    currency: Mapped[str] = mapped_column(String(3))
    value_date: Mapped[date | None] = mapped_column(Date, index=True)
    # Year-only flows (e.g. annual figures in a report): the year is kept, no day is invented.
    period_year: Mapped[int | None] = mapped_column(Integer, index=True)
    transaction_key: Mapped[str] = mapped_column(String(200))
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")
    is_counted: Mapped[bool] = mapped_column(Boolean, default=True)
    counting_note: Mapped[str | None] = mapped_column(Text)

    agreement: Mapped[FinancingAgreement] = relationship(back_populates="disbursements")


class CounterpartFinancing(Base):
    """Government counterpart and private financing declared for a project."""

    __tablename__ = "counterpart_financing"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    financier_type: Mapped[str] = mapped_column(String(30))  # government | private | soe | beneficiaries
    financier_name: Mapped[str | None] = mapped_column(Text)
    amount: Mapped[Decimal | None] = mapped_column(Money)
    currency: Mapped[str | None] = mapped_column(String(3))
    as_of: Mapped[date | None] = mapped_column(Date)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")


class Contract(Base, Timestamped):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    reference: Mapped[str | None] = mapped_column(String(120))
    title: Mapped[str] = mapped_column(Text)
    contractor: Mapped[str | None] = mapped_column(Text)
    procurement_method: Mapped[str | None] = mapped_column(String(80))
    signature_date: Mapped[date | None] = mapped_column(Date)
    original_amount: Mapped[Decimal | None] = mapped_column(Money)
    currency: Mapped[str | None] = mapped_column(String(3))
    original_end_date: Mapped[date | None] = mapped_column(Date)
    paid_to_date: Mapped[Decimal | None] = mapped_column(Money)
    paid_as_of: Mapped[date | None] = mapped_column(Date)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")

    amendments: Mapped[list["ContractAmendment"]] = relationship(back_populates="contract")


class ContractAmendment(Base):
    __tablename__ = "contract_amendments"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id", ondelete="CASCADE"), index=True)
    amendment_date: Mapped[date | None] = mapped_column(Date)
    amount_change: Mapped[Decimal | None] = mapped_column(Money)
    currency: Mapped[str | None] = mapped_column(String(3))
    new_end_date: Mapped[date | None] = mapped_column(Date)
    reason: Mapped[str | None] = mapped_column(Text)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))

    contract: Mapped[Contract] = relationship(back_populates="amendments")


class BudgetAllocation(Base):
    """National public investment budget lines (Master prompt §13).

    Appropriations are NOT commitments and NOT disbursements: they live in their own table.
    """

    __tablename__ = "budget_allocations"
    __table_args__ = (
        UniqueConstraint("country_id", "budget_year", "budget_line_code", "source_record_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), index=True)
    budget_year: Mapped[int] = mapped_column(Integer, index=True)
    budget_line_code: Mapped[str] = mapped_column(String(80))
    project_identifier: Mapped[str | None] = mapped_column(String(120))
    project_label: Mapped[str | None] = mapped_column(Text)
    administrative_classification: Mapped[str | None] = mapped_column(Text)
    program_classification: Mapped[str | None] = mapped_column(Text)
    funding_source: Mapped[str | None] = mapped_column(Text)  # e.g. "Ressources internes", "Emprunts extérieurs"
    funding_type: Mapped[str] = mapped_column(String(40), default="unknown")
    currency: Mapped[str] = mapped_column(String(3))
    approved_appropriation: Mapped[Decimal | None] = mapped_column(Money)
    revised_appropriation: Mapped[Decimal | None] = mapped_column(Money)
    commitment: Mapped[Decimal | None] = mapped_column(Money)
    payment: Mapped[Decimal | None] = mapped_column(Money)
    source_record_id: Mapped[int | None] = mapped_column(ForeignKey("source_records.id"))
    data_nature: Mapped[str] = mapped_column(String(30), default="officially_reported")


class ExchangeRate(Base):
    """Historical rates with their source. Never today's rate for a historical comparison."""

    __tablename__ = "exchange_rates"
    __table_args__ = (UniqueConstraint("base_currency", "quote_currency", "period", "period_type", "source"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    base_currency: Mapped[str] = mapped_column(String(3))  # 1 unit of base ...
    quote_currency: Mapped[str] = mapped_column(String(3))  # ... = rate units of quote
    rate: Mapped[Decimal] = mapped_column(Rate)
    period: Mapped[str] = mapped_column(String(10))  # "2024" (annual) or "2024-06-30" (daily)
    period_type: Mapped[str] = mapped_column(String(10), default="annual_avg")
    source: Mapped[str] = mapped_column(String(120))
    source_url: Mapped[str | None] = mapped_column(Text)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AnnualFinancialSnapshot(Base):
    """Reproducible annual portfolio snapshot. New snapshots supersede; old ones are kept."""

    __tablename__ = "annual_financial_snapshots"
    __table_args__ = (CheckConstraint("year >= 1950 AND year <= 2100", name="year_range"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    methodology_version: Mapped[str] = mapped_column(String(20))
    input_fingerprint: Mapped[str] = mapped_column(String(64))  # hash of the inputs used
    payload: Mapped[dict] = mapped_column(JSON)
    is_current: Mapped[bool] = mapped_column(default=True)
    note: Mapped[str | None] = mapped_column(Text)
