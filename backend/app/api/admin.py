"""Admin-only endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select

from app.api.deps import SessionDep
from app.models import AuditLog
from app.models.enums import Role
from app.schemas import AuditLogOut
from app.security.auth import require_role

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_role(Role.ADMIN))])


@router.get("/audit-log", response_model=list[AuditLogOut])
def audit_log(
    session: SessionDep,
    limit: Annotated[int, Query(ge=1, le=1000, description="Most recent rows first.")] = 100,
) -> list[AuditLogOut]:
    rows = session.scalars(select(AuditLog).order_by(AuditLog.id.desc()).limit(limit))
    return [AuditLogOut.model_validate(r) for r in rows]
