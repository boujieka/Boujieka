"""Configuration par variables d'environnement (préfixe GEORENEW_). Aucun secret dans le code."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GEORENEW_", env_file=".env", extra="ignore")

    # PostGIS en Docker : postgresql+psycopg://user:pass@db:5432/georenew
    # Option locale sans serveur : SQLite (géométries stockées en WKB, calculs identiques).
    database_url: str = f"sqlite:///{BACKEND_DIR / 'var' / 'georenew.db'}"
    max_upload_mb: int = 50
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    frontend_dist: Path = BACKEND_DIR.parent / "frontend" / "dist"


@lru_cache
def get_settings() -> Settings:
    return Settings()
