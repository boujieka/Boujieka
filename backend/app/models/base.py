from datetime import date, datetime, timezone
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import JSON, CheckConstraint, DateTime, Enum, ForeignKey, MetaData, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.models.enums import DataNature, VerificationStatus

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def str_enum(enum_cls: type[StrEnum], length: int = 32) -> Enum:
    """Store enum values (not names) as VARCHAR with a CHECK constraint."""
    return Enum(
        enum_cls,
        native_enum=False,
        length=length,
        values_callable=lambda e: [m.value for m in e],
        validate_strings=True,
    )


# Money amounts: up to 10^16 in local currency units with 4 dp.
Money = Numeric(20, 4)
# Rates and yields are stored in PERCENT (e.g. 11.25 means 11.25%).
Rate = Numeric(10, 6)

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class ProvenanceMixin:
    """Source-first: every market-data record carries where it came from.

    `field_status` records why individual fields are empty, so the API can
    distinguish "Not disclosed" (the source does not publish it) from
    "Not available" (we have no source for it).
    """

    @declared_attr
    def source_id(cls) -> Mapped[int | None]:
        return mapped_column(ForeignKey("source.source_id"), index=True)

    @declared_attr
    def source_document_id(cls) -> Mapped[int | None]:
        return mapped_column(ForeignKey("source_document.document_id"), index=True)

    source_url: Mapped[str | None] = mapped_column(String(2048))
    publication_date: Mapped[date | None]
    extracted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    verification_status: Mapped[VerificationStatus] = mapped_column(
        str_enum(VerificationStatus), default=VerificationStatus.UNVERIFIED
    )
    data_nature: Mapped[DataNature] = mapped_column(str_enum(DataNature), default=DataNature.FACT)
    confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(4, 3))
    is_synthetic: Mapped[bool] = mapped_column(default=False, index=True)
    field_status: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    provenance_notes: Mapped[str | None] = mapped_column(Text)


def provenance_constraints() -> tuple[CheckConstraint, ...]:
    """Table-level guarantees for every ProvenanceMixin table."""
    return (
        CheckConstraint(
            "confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1)",
            name="confidence_range",
        ),
        # Synthetic data must be labelled as synthetic everywhere it is described.
        CheckConstraint(
            "(is_synthetic = false) OR "
            "(data_nature = 'SYNTHETIC' AND verification_status = 'synthetic')",
            name="synthetic_is_labelled",
        ),
    )
