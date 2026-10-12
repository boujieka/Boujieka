"""Alembic environment: migrations run as the owner role (A360_DATABASE_OWNER_URL), never as the app role."""
from alembic import context
from sqlalchemy import create_engine

from app.config import get_settings
from app.db import Base
from app import models  # noqa: F401  (registers tables)

target_metadata = Base.metadata


def run() -> None:
    url = context.config.attributes.get("url") or get_settings().database_owner_url
    eng = create_engine(url)
    with eng.connect() as conn:
        context.configure(connection=conn, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run()
