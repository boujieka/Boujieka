"""Phase 1b: API keys and audit log

Revision ID: 0005
Revises: 0004
Create Date: 2026-10-04 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0005'
down_revision: Union[str, Sequence[str], None] = '0004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Non-native enum (VARCHAR + CHECK), as everywhere else in the schema.
ROLE = sa.Enum('public', 'analyst', 'admin', name='role', native_enum=False, length=16)


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'api_key',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('key_hash', sa.String(length=64), nullable=False),
        sa.Column('role', ROLE, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_api_key')),
        sa.UniqueConstraint('key_hash', name=op.f('uq_api_key_key_hash')),
    )
    op.create_table(
        'audit_log',
        sa.Column('id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
        sa.Column('at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('api_key_id', sa.Integer(), nullable=True),
        sa.Column('role', ROLE, nullable=False),
        sa.Column('method', sa.String(length=10), nullable=False),
        sa.Column('path', sa.String(length=512), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=False),
        sa.Column('client_ip', sa.String(length=64), nullable=True),
        sa.Column('request_id', sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ['api_key_id'], ['api_key.id'],
            name=op.f('fk_audit_log_api_key_id_api_key'), ondelete='SET NULL',
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_audit_log')),
    )
    op.create_index(op.f('ix_audit_log_api_key_id'), 'audit_log', ['api_key_id'], unique=False)
    op.create_index(op.f('ix_audit_log_at'), 'audit_log', ['at'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_audit_log_at'), table_name='audit_log')
    op.drop_index(op.f('ix_audit_log_api_key_id'), table_name='audit_log')
    op.drop_table('audit_log')
    op.drop_table('api_key')
