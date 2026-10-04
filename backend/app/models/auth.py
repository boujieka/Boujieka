from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, str_enum, utcnow
from app.models.enums import Role

# BIGINT in Postgres; SQLite only auto-increments a plain INTEGER primary key.
BigId = BigInteger().with_variant(Integer, "sqlite")


class ApiKey(Base):
    """An API credential. Only the SHA-256 hash is stored; the plaintext is shown once at creation."""

    __tablename__ = "api_key"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    key_hash: Mapped[str] = mapped_column(String(64), unique=True)
    role: Mapped[Role] = mapped_column(str_enum(Role, length=16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AuditLog(Base):
    """One row per request to a protected endpoint and per auth failure (401/403/429).

    `path` never includes the query string and no credential is ever stored.
    `client_ip` is truncated to its network (/24 for IPv4, /48 for IPv6): enough to
    investigate abuse, without keeping a precise personal identifier. A plain hash
    would not help: the IPv4 space is small enough to reverse an unsalted hash.
    """

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(BigId, primary_key=True)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    api_key_id: Mapped[int | None] = mapped_column(
        ForeignKey("api_key.id", ondelete="SET NULL"), index=True
    )
    role: Mapped[Role] = mapped_column(str_enum(Role, length=16))
    method: Mapped[str] = mapped_column(String(10))
    path: Mapped[str] = mapped_column(String(512))
    status_code: Mapped[int]
    client_ip: Mapped[str | None] = mapped_column(String(64))
    request_id: Mapped[str] = mapped_column(String(64))
