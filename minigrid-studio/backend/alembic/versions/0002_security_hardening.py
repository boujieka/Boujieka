"""Security hardening: invitations, submitter, stronger database guarantees.

Revision ID: 0002
Revises: 0001
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = '0002'
down_revision: Union[str, Sequence[str], None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'invitations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('org_id', sa.String(length=36), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('role', postgresql.ENUM('admin', 'analyst', 'reviewer', 'investor', name='role', create_type=False),
                  nullable=False),
        sa.Column('token_hash', sa.String(length=64), nullable=False),
        sa.Column('invited_by', sa.String(length=36), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('accepted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('revoked', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['invited_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token_hash'),
    )
    op.create_index(op.f('ix_invitations_org_id'), 'invitations', ['org_id'], unique=False)
    op.create_index(op.f('ix_invitations_email'), 'invitations', ['email'], unique=False)
    op.add_column('scenario_versions', sa.Column('submitted_by', sa.String(length=36), nullable=True))
    op.create_foreign_key('fk_scenario_versions_submitted_by', 'scenario_versions', 'users',
                          ['submitted_by'], ['id'])
    # Stronger guarantees. The application should also connect with a role that has
    # no TRUNCATE/DDL rights (see docs/architecture.md); triggers are a second line.
    op.execute("""
        CREATE TRIGGER audit_events_no_truncate BEFORE TRUNCATE ON audit_events
            FOR EACH STATEMENT EXECUTE FUNCTION audit_events_append_only();
        CREATE OR REPLACE FUNCTION scenario_versions_frozen() RETURNS trigger AS $$
        BEGIN
            IF TG_OP = 'DELETE' THEN
                RAISE EXCEPTION 'scenario versions cannot be deleted';
            END IF;
            IF NEW.assumptions IS DISTINCT FROM OLD.assumptions OR NEW.options IS DISTINCT FROM OLD.options
               OR NEW.solver_method IS DISTINCT FROM OLD.solver_method
               OR NEW.content_hash IS DISTINCT FROM OLD.content_hash
               OR NEW.project_id IS DISTINCT FROM OLD.project_id OR NEW.scenario IS DISTINCT FROM OLD.scenario
               OR NEW.version IS DISTINCT FROM OLD.version OR NEW.parent_id IS DISTINCT FROM OLD.parent_id
               OR NEW.changes IS DISTINCT FROM OLD.changes OR NEW.provenance IS DISTINCT FROM OLD.provenance
               OR NEW.created_by IS DISTINCT FROM OLD.created_by THEN
                RAISE EXCEPTION 'scenario version content is immutable; create a new version';
            END IF;
            IF NEW.status IS DISTINCT FROM OLD.status AND NOT (
                   (OLD.status IN ('draft', 'rejected') AND NEW.status = 'submitted')
                OR (OLD.status = 'submitted' AND NEW.status IN ('approved', 'rejected'))) THEN
                RAISE EXCEPTION 'invalid status transition % -> %', OLD.status, NEW.status;
            END IF;
            RETURN NEW;
        END $$ LANGUAGE plpgsql;
        DROP TRIGGER scenario_versions_no_rewrite ON scenario_versions;
        CREATE TRIGGER scenario_versions_no_rewrite BEFORE UPDATE OR DELETE ON scenario_versions
            FOR EACH ROW EXECUTE FUNCTION scenario_versions_frozen();
        CREATE FUNCTION calculation_runs_immutable() RETURNS trigger AS $$
        BEGIN RAISE EXCEPTION 'calculation runs are immutable'; END $$ LANGUAGE plpgsql;
        CREATE TRIGGER calculation_runs_no_change BEFORE UPDATE OR DELETE ON calculation_runs
            FOR EACH ROW EXECUTE FUNCTION calculation_runs_immutable();
    """)


def downgrade() -> None:
    op.execute("""
        DROP TRIGGER IF EXISTS calculation_runs_no_change ON calculation_runs;
        DROP FUNCTION IF EXISTS calculation_runs_immutable();
        DROP TRIGGER IF EXISTS audit_events_no_truncate ON audit_events;
        DROP TRIGGER scenario_versions_no_rewrite ON scenario_versions;
        CREATE OR REPLACE FUNCTION scenario_versions_frozen() RETURNS trigger AS $$
        BEGIN
            IF NEW.assumptions IS DISTINCT FROM OLD.assumptions OR NEW.options IS DISTINCT FROM OLD.options
               OR NEW.solver_method IS DISTINCT FROM OLD.solver_method
               OR NEW.content_hash IS DISTINCT FROM OLD.content_hash THEN
                RAISE EXCEPTION 'scenario version content is immutable; create a new version';
            END IF;
            RETURN NEW;
        END $$ LANGUAGE plpgsql;
        CREATE TRIGGER scenario_versions_no_rewrite BEFORE UPDATE ON scenario_versions
            FOR EACH ROW EXECUTE FUNCTION scenario_versions_frozen();
    """)
    op.drop_constraint('fk_scenario_versions_submitted_by', 'scenario_versions', type_='foreignkey')
    op.drop_column('scenario_versions', 'submitted_by')
    op.drop_index(op.f('ix_invitations_email'), table_name='invitations')
    op.drop_index(op.f('ix_invitations_org_id'), table_name='invitations')
    op.drop_table('invitations')
