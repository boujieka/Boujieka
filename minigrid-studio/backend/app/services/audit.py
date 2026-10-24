from sqlalchemy.orm import Session

from ..models import AuditEvent


def record(db: Session, *, org_id: str | None, user_id: str | None, action: str, entity_type: str,
           entity_id: str = "", payload: dict | None = None) -> None:
    db.add(AuditEvent(org_id=org_id, user_id=user_id, action=action, entity_type=entity_type,
                      entity_id=entity_id, payload=payload or {}))
