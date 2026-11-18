from logging.config import fileConfig

from alembic import context

from app import models  # noqa: F401  (enregistre les tables)
from app.config import get_settings
from app.db import Base, make_engine

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


POSTGIS_TABLES = {"spatial_ref_sys", "topology", "layer"}


def include_object(obj, name, type_, reflected, compare_to):
    # Tables système de PostGIS : jamais gérées par nos migrations.
    if type_ == "table" and reflected and compare_to is None and name in POSTGIS_TABLES:
        return False
    # Index GiST : créés explicitement par les migrations (PostgreSQL seulement).
    if type_ == "index" and reflected and name and name.endswith("_gist"):
        return False
    return True


def run_migrations_online() -> None:
    url = config.attributes.get("database_url") or get_settings().database_url
    engine = make_engine(url)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=url.startswith("sqlite"),
                          include_object=include_object)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
