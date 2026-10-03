from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Secrets come from the environment only, never from code."""

    model_config = SettingsConfigDict(env_prefix="ABI_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://abi:abi@localhost:5432/abi"
    cors_origins: list[str] = ["http://localhost:3000"]
    # A source is "stale" when it has not been successfully checked for this many hours.
    source_stale_after_hours: int = 48
    # Records below this confidence are surfaced on the data-quality page.
    low_confidence_threshold: float = 0.7
    environment: str = "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
