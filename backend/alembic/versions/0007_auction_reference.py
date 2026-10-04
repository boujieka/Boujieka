"""auction.auction_reference: the printed adjudication number becomes part of the natural key

Revision ID: 0007
Revises: 0006
Create Date: 2026-10-04

UMOA-Titres sometimes holds two distinct auctions of the same ISIN on the same day (a regular
issue and a "rachat-émission" issue, or two separate BAT auctions), each with its own
adjudication number and its own results. The old key (security_id, auction_date, auction_type)
made the second one impossible to store.

New key:
  * uq_auction_natural_key (security_id, auction_date, auction_type, auction_reference)
    — a plain unique constraint. NULLs are distinct in unique constraints on both PostgreSQL and
    SQLite, so it only constrains rows that carry a reference;
  * uq_auction_natural_key_unreferenced (security_id, auction_date, auction_type)
    WHERE auction_reference IS NULL — a partial unique index (supported by both databases), so
    rows without a reference (synthetic rows, reports that print no number) keep the old rule.

Backfill: every verified, non-synthetic auction takes the adjudication number of the staging row
it was promoted from (auction_extraction.promoted_auction_id -> fields.auction_number.value), as
printed. Nothing is inferred: an auction whose staging row has no number keeps NULL.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0007'
down_revision: Union[str, Sequence[str], None] = '0006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NULL_REF = sa.text("auction_reference IS NULL")


def upgrade() -> None:
    op.add_column('auction', sa.Column('auction_reference', sa.String(length=64), nullable=True))

    bind = op.get_bind()
    auction = sa.table('auction', sa.column('auction_id', sa.Integer), sa.column('auction_reference', sa.String),
                       sa.column('is_synthetic', sa.Boolean), sa.column('verification_status', sa.String))
    extraction = sa.table('auction_extraction', sa.column('promoted_auction_id', sa.Integer),
                          sa.column('fields', sa.JSON))
    rows = bind.execute(
        sa.select(extraction.c.promoted_auction_id, extraction.c.fields)
        .join(auction, auction.c.auction_id == extraction.c.promoted_auction_id)
        .where(auction.c.is_synthetic.is_(False), auction.c.verification_status == 'verified')
    ).all()
    for auction_id, fields in rows:
        value = ((fields or {}).get('auction_number') or {}).get('value')
        if value and str(value).strip():
            bind.execute(auction.update().where(auction.c.auction_id == auction_id)
                         .values(auction_reference=str(value).strip()))

    op.drop_constraint('uq_auction_natural_key', 'auction', type_='unique')
    op.create_unique_constraint('uq_auction_natural_key', 'auction',
                                ['security_id', 'auction_date', 'auction_type', 'auction_reference'])
    op.create_index('uq_auction_natural_key_unreferenced', 'auction',
                    ['security_id', 'auction_date', 'auction_type'], unique=True,
                    postgresql_where=NULL_REF, sqlite_where=NULL_REF)


def downgrade() -> None:
    bind = op.get_bind()
    clash = bind.execute(sa.text(
        "SELECT security_id, auction_date, auction_type, count(*) FROM auction "
        "GROUP BY security_id, auction_date, auction_type HAVING count(*) > 1")).all()
    if clash:
        raise RuntimeError(
            f"cannot downgrade: {len(clash)} security/date/type triples hold more than one auction "
            "(same-day auctions with different adjudication numbers); the old key cannot hold them. "
            f"First ones: {[tuple(map(str, c[:3])) for c in clash[:5]]}")
    op.drop_index('uq_auction_natural_key_unreferenced', table_name='auction',
                  postgresql_where=NULL_REF, sqlite_where=NULL_REF)
    op.drop_constraint('uq_auction_natural_key', 'auction', type_='unique')
    op.create_unique_constraint('uq_auction_natural_key', 'auction',
                                ['security_id', 'auction_date', 'auction_type'])
    op.drop_column('auction', 'auction_reference')
