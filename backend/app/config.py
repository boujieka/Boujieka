from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Secrets come from the environment only, never from code."""

    model_config = SettingsConfigDict(env_prefix="ABI_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://abi:abi@localhost:5432/abi"
    # Explicit origins only; a "*" entry is refused (see docs/SECURITY.md).
    cors_origins: list[str] = ["http://localhost:3000"]
    # In-memory, per-process sliding window (see docs/SECURITY.md for multi-instance limits).
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 120  # Callers without a key, per client IP.
    rate_limit_per_minute_key: int = 600  # Per API key.
    # Never throttled: Starlette's TestClient reports this host, used by tests and site/build.py.
    # It is the socket peer name, so a remote client cannot claim it.
    rate_limit_exempt_hosts: list[str] = ["testclient"]
    # A source is "stale" when it has not been successfully checked for this many hours.
    source_stale_after_hours: int = 48
    # Records below this confidence are surfaced on the data-quality page.
    low_confidence_threshold: float = 0.7
    environment: str = "development"
    # Where fetched official documents are kept (bytes + extracted text), named by SHA-256.
    document_store_dir: str = "var/documents"
    # Name recorded on review decisions when --reviewer is not given.
    reviewer: str | None = None

    @field_validator("cors_origins")
    @classmethod
    def no_wildcard_origin(cls, v: list[str]) -> list[str]:
        if "*" in v:
            raise ValueError("ABI_CORS_ORIGINS must list explicit origins, not '*'")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
