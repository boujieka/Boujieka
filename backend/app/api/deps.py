from datetime import date
from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Source

SessionDep = Annotated[Session, Depends(get_session)]


def as_of_date(
    as_of: Annotated[
        date | None, Query(description="Reference date for 'upcoming'/'recent'. Defaults to today.")
    ] = None,
) -> date:
    return as_of or date.today()


AsOfDep = Annotated[date, Depends(as_of_date)]


def source_map(session: SessionDep) -> dict[int, Source]:
    """Sources are a small table; load once per request for provenance lookups."""
    return {s.source_id: s for s in session.scalars(select(Source))}


SourcesDep = Annotated[dict[int, Source], Depends(source_map)]
