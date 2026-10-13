"""Portfolios, project gates and score context, wider MFA secret column (encrypted at rest).

Revision ID: 0003
Revises: 0002
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.config import get_settings

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

CURRENT_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.alter_column("users", "mfa_secret", type_=sa.String(255), existing_nullable=True)
    op.add_column("projects", sa.Column("gates", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")))
    op.add_column("projects", sa.Column("score_context", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")))
    op.create_table(
        "portfolios",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("org_id", sa.UUID(), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_by", sa.UUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "portfolio_projects",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("org_id", sa.UUID(), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("portfolio_id", sa.UUID(), sa.ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("project_id", sa.UUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.UniqueConstraint("portfolio_id", "project_id"),
    )
    role = get_settings().app_db_role
    for t in ("portfolios", "portfolio_projects"):
        op.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {t} TO {role}")
        op.execute(f"ALTER TABLE {t} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {t} FORCE ROW LEVEL SECURITY")
        op.execute(f"CREATE POLICY tenant_isolation ON {t} USING (org_id = {CURRENT_ORG}) WITH CHECK (org_id = {CURRENT_ORG})")


def downgrade() -> None:
    op.drop_table("portfolio_projects")
    op.drop_table("portfolios")
    op.drop_column("projects", "score_context")
    op.drop_column("projects", "gates")
    op.alter_column("users", "mfa_secret", type_=sa.String(64), existing_nullable=True)
