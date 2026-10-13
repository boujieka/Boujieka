"""Environment based configuration. Secrets come only from the environment; nothing secret is committed."""
from __future__ import annotations

import secrets
import warnings
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

ENGINE_VERSION = "0.1.0"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="A360_", env_file=".env", extra="ignore")

    env: str = "development"  # development | test | production
    database_url: str = "postgresql+psycopg://access360_app:app@127.0.0.1:5433/access360"
    database_owner_url: str = "postgresql+psycopg://postgres@127.0.0.1:5433/access360"
    app_db_role: str = "access360_app"
    jwt_secret: str = ""
    jwt_minutes: int = 60
    cookie_secure: bool = False
    cors_origins: str = "http://localhost:3000"
    storage_dir: str = "storage"
    max_upload_mb: int = 20
    login_rate_per_minute: int = 10
    register_rate_per_minute: int = 5      # per IP
    mfa_rate_per_minute: int = 10          # per user (MFA setup verification)
    password_rate_per_minute: int = 5      # forgot / reset / change, per IP and per email or user
    redis_url: str = ""                    # when set, rate limits and session revocation are shared through Redis
    # password reset e-mail
    public_base_url: str = "http://localhost:3000"  # used to build the reset link sent by e-mail
    reset_token_minutes: int = 30
    email_backend: str = ""                # console | smtp | memory (tests); default console, smtp in production
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""                    # sender address on a domain the operator controls; required for smtp
    smtp_starttls: bool = True
    smtp_ssl: bool = False
    # application data key (Fernet) for field level encryption; see app/crypto.py and limitation L13
    data_key: str = ""
    data_keys_old: str = ""

    def secret(self) -> str:
        if self.jwt_secret:
            return self.jwt_secret
        if self.env == "production":
            raise RuntimeError("A360_JWT_SECRET must be set in production")
        warnings.warn("A360_JWT_SECRET not set: using a random per-process secret (sessions end on restart)")
        self.jwt_secret = secrets.token_urlsafe(48)
        return self.jwt_secret


    def email_backend_name(self) -> str:
        if self.email_backend:
            return self.email_backend
        return "smtp" if self.env == "production" else "console"


@lru_cache
def get_settings() -> Settings:
    return Settings()
