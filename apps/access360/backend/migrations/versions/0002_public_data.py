"""public reference data: dataset provenance columns, reference_sources and country_profiles

Revision ID: 0002
Revises: 0001
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.config import get_settings

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

JSONB = sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql")


def upgrade() -> None:
    op.add_column("datasets", sa.Column("source_key", sa.String(length=60), nullable=True))
    op.add_column("datasets", sa.Column("source_url", sa.String(length=500), nullable=True))
    op.add_column("datasets", sa.Column("source_version", sa.String(length=300), nullable=True))
    op.add_column("datasets", sa.Column("attribution", sa.Text(), nullable=True))
    # a source key identifies one platform dataset; tenant rows never carry one
    op.create_check_constraint("ck_datasets_source_key_platform_only", "datasets", "source_key IS NULL OR org_id IS NULL")
    op.create_index("ux_datasets_platform_source_key", "datasets", ["source_key"], unique=True,
                    postgresql_where=sa.text("org_id IS NULL AND source_key IS NOT NULL"))

    op.create_table(
        "reference_sources",
        sa.Column("key", sa.String(length=60), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=300), nullable=False),
        sa.Column("source_institution", sa.String(length=300), nullable=False),
        sa.Column("licence", sa.String(length=300), nullable=False),
        sa.Column("attribution", sa.Text(), nullable=False),
        sa.Column("quality", sa.String(length=30), nullable=False),
        sa.Column("retrieval_date", sa.Date(), nullable=False),
        sa.Column("record", JSONB, nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_table(
        "country_profiles",
        sa.Column("iso3", sa.String(length=3), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("bbox", JSONB, nullable=True),
        sa.Column("indicators", JSONB, nullable=False),
        sa.Column("admin1_count", sa.Integer(), nullable=False),
        sa.Column("places_count", sa.Integer(), nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("iso3"),
    )
    # public reference data: no tenant column, so no RLS; the app role may read but never write
    role = get_settings().app_db_role
    for t in ("reference_sources", "country_profiles"):
        op.execute(f"REVOKE ALL ON {t} FROM {role}")
        op.execute(f"GRANT SELECT ON {t} TO {role}")


def downgrade() -> None:
    op.drop_table("country_profiles")
    op.drop_table("reference_sources")
    op.drop_index("ux_datasets_platform_source_key", table_name="datasets")
    op.drop_constraint("ck_datasets_source_key_platform_only", "datasets", type_="check")
    for c in ("attribution", "source_version", "source_url", "source_key"):
        op.drop_column("datasets", c)
