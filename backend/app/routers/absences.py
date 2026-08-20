from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TeacherAbsence, User
from app.schemas.entities import AbsenceCreate, AbsenceOut
from app.services.absence_service import create_absence_with_pending_substitutions
from app.services.audit_service import log_action
from app.utils.deps import get_current_user, require_roles
from app.utils.enums import UserRole

router = APIRouter(prefix="/api/absences", tags=["Absences"])


@router.get("", response_model=list[AbsenceOut], summary="List absences")
def list_absences(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list(db.scalars(select(TeacherAbsence).order_by(TeacherAbsence.date.desc())).all())


@router.post("", summary="Mark teacher absent and detect affected periods")
def mark_absent(
    payload: AbsenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    absence, affected = create_absence_with_pending_substitutions(
        db,
        teacher_id=payload.teacher_id,
        target_date=payload.date,
        reason=payload.reason,
        notes=payload.notes,
    )
    log_action(
        db,
        user=current_user.username,
        action="Marked teacher absent",
        entity="TeacherAbsence",
        entity_id=str(absence.id),
        description=f"Teacher {absence.teacher_id} absent on {absence.date}",
    )
    return {
        "success": True,
        "absence": AbsenceOut.model_validate(absence).model_dump(),
        "affected_periods": [item.model_dump() for item in affected],
    }
