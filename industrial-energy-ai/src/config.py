"""Application configuration.

All settings come from environment variables (optionally loaded from a local ``.env`` file).
No credential is ever hardcoded. Physical and modelling constants that are *defaults* (and may be
overridden by the user) live in :mod:`src.energy.defaults`, not here.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
REPORT_DIR = DATA_DIR / "reports"

HOURS_PER_YEAR = 8760  # standard non-leap year used by every hourly engine
APP_VERSION = "1.0.0"
APP_NAME = "Industrial Energy AI Africa"


def _load_dotenv(path: Path) -> None:
    """Minimal ``.env`` loader (KEY=VALUE lines); existing environment variables win."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on", "oui"}


@dataclass(frozen=True)
class Settings:
    database_url: str
    language: str
    ai_enabled: bool
    ai_provider: str
    ai_model: str
    openai_api_key: str | None
    log_level: str

    @property
    def openai_configured(self) -> bool:
        return bool(self.openai_api_key)


def get_settings() -> Settings:
    _load_dotenv(PROJECT_ROOT / ".env")
    default_db = f"sqlite:///{(DATA_DIR / 'industrial_energy_ai.db').as_posix()}"
    db_url = os.environ.get("IEA_DATABASE_URL") or default_db
    # Relative SQLite paths are resolved against the project root so the app works from any cwd.
    if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:////"):
        rel = db_url[len("sqlite:///"):]
        if rel and rel != ":memory:" and not Path(rel).is_absolute():
            db_url = f"sqlite:///{(PROJECT_ROOT / rel).as_posix()}"
    language = (os.environ.get("IEA_LANGUAGE") or "fr").lower()
    return Settings(
        database_url=db_url,
        language=language if language in {"fr", "en"} else "fr",
        ai_enabled=_as_bool(os.environ.get("IEA_AI_ENABLED"), False),
        ai_provider=(os.environ.get("IEA_AI_PROVIDER") or "offline").lower(),
        ai_model=os.environ.get("IEA_AI_MODEL") or "gpt-4o-mini",
        openai_api_key=os.environ.get("OPENAI_API_KEY") or None,
        log_level=(os.environ.get("IEA_LOG_LEVEL") or "INFO").upper(),
    )


def configure_logging(level: str | None = None) -> None:
    logging.basicConfig(
        level=getattr(logging, (level or get_settings().log_level), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
