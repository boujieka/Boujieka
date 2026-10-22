from alembic import context
from sqlalchemy import engine_from_config, pool

import app.models  # noqa: F401 — registers all tables
from app.config import get_settings
from app.models.base import Base

config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url.replace("%", "%%"))
target_metadata = Base.metadata

POSTGIS_OBJECTS = {"spatial_ref_sys", "geography_columns", "geometry_columns", "geog", "ix_project_locations_geog"}


def include_object(obj, name, type_, reflected, compare_to):
    """Ignore PostGIS-owned tables and the derived geography column during autogenerate."""
    return name not in POSTGIS_OBJECTS


def run_migrations_offline() -> None:
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True,
                          include_object=include_object)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
