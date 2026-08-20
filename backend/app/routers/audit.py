from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog, User
from app.schemas.entities import AuditLogOut
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/audit", tags=["Audit"])


@router.get("", response_model=list[AuditLogOut], summary="Audit logs")
def list_audit_logs(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list(db.scalars(select(AuditLog).order_by(AuditLog.timestamp.desc())).all())
