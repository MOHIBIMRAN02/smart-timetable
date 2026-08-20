from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import AuditLog


def log_action(
    db: Session,
    *,
    user: str,
    action: str,
    entity: str,
    entity_id: str,
    description: str | None = None,
) -> None:
    entry = AuditLog(
        user=user,
        action=action,
        entity=entity,
        entity_id=entity_id,
        description=description,
    )
    db.add(entry)
    db.commit()
