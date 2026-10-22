"""Runtime configuration. Every value comes from the environment (prefix AP2I_)."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AP2I_", env_file=".env", extra="ignore")

    environment: str = Field("development", description="development | test | production")
    database_url: str = "postgresql+psycopg://ap2i:ap2i@localhost:5432/ap2i"
    redis_url: str = "redis://localhost:6379/0"

    # Security. secret_key MUST be set in production (checked at startup).
    secret_key: str = "dev-only-insecure-secret-change-me"
    access_token_minutes: int = 60
    password_min_length: int = 12
    max_failed_logins: int = 5
    lockout_minutes: int = 15
    cors_origins: list[str] = ["http://localhost:3000"]
    rate_limit_per_minute: int = 120
    auth_rate_limit_per_minute: int = 10
    upload_max_bytes: int = 20_000_000

    # Country activation is configuration, never code.
    active_countries: list[str] = ["CMR"]
    default_country: str = "CMR"
    portfolio_first_year: int = 2011
    portfolio_last_year: int = 2026

    # Ingestion
    http_timeout_seconds: float = 60.0
    http_user_agent: str = "AP2I-ingestion/2.0 (+https://github.com/boujieka/boujieka)"
    iati_datastore_url: str = "https://datastore.codeforiati.org/api/1/access"
    iati_official_api_url: str = "https://api.iatistandard.org/datastore"
    iati_api_key: str | None = None
    worldbank_projects_url: str = "https://search.worldbank.org/api/v2/projects"
    worldbank_indicator_url: str = "https://api.worldbank.org/v2"
    imf_sdmx_url: str = "https://api.imf.org/external/sdmx/2.1"
    document_store_dir: str = "var/documents"

    # Email (console backend logs messages instead of sending them)
    email_backend: str = "console"
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    email_from: str = "no-reply@ap2i.local"
    public_app_url: str = "http://localhost:3000"

    # AI: provider-agnostic. "none" = deterministic, database-only answers.
    llm_provider: str = "none"
    llm_model: str | None = None
    llm_api_key: str | None = None
    llm_base_url: str | None = None

    # Payments are never active without verified credentials.
    payment_provider: str = "none"
    payment_api_key: str | None = None

    # Object storage (S3-compatible). Local directory fallback when unset.
    s3_endpoint_url: str | None = None
    s3_bucket: str | None = None
    s3_access_key: str | None = None
    s3_secret_key: str | None = None

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
