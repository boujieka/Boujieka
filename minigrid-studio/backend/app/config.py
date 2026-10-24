from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All settings come from the environment (prefix MGS_), never from code."""
    model_config = SettingsConfigDict(env_prefix="MGS_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://mgs:mgs@127.0.0.1:55432/mgs"
    token_ttl_hours: int = 12
    allow_signup: bool = False          # self-service organisation creation
    max_upload_mb: int = 10
    cors_origins: list[str] = []
    login_attempts_per_minute: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()
