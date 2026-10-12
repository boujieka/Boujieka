from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from ..models import AuditLog


def audit(s: Session, action: str, entity: str, entity_id=None, *, org_id: uuid.UUID | None = None,
          user_id: uuid.UUID | None = None, **detail) -> None:
    s.add(AuditLog(org_id=org_id, user_id=user_id, action=action, entity=entity,
                   entity_id=str(entity_id) if entity_id is not None else None, detail=detail))
