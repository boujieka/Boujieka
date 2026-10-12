"""Database sessions and tenant context.

The application connects with a role that is not the table owner, so PostgreSQL row level security applies to
every tenant table. Each org scoped request sets `app.current_org` inside its transaction (SET LOCAL semantics),
and the policies in the migrations only return rows of that organisation. The API layer checks membership first;
the database policies are the second, independent barrier."""
from __future__ import annotations

import uuid
from collections.abc import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import get_settings


class Base(DeclarativeBase):
    pass


_engine = None
_Session: sessionmaker | None = None


def engine():
    global _engine, _Session
    if _engine is None:
        _engine = create_engine(get_settings().database_url, pool_pre_ping=True, future=True)
        _Session = sessionmaker(bind=_engine, expire_on_commit=False)
    return _engine


def reset_engine() -> None:
    global _engine, _Session
    if _engine is not None:
        _engine.dispose()
    _engine, _Session = None, None


def get_session() -> Iterator[Session]:
    engine()
    assert _Session is not None
    s = _Session()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def set_tenant(s: Session, org_id: uuid.UUID | None) -> None:
    s.execute(text("SELECT set_config('app.current_org', :v, true)"), {"v": str(org_id) if org_id else ""})
