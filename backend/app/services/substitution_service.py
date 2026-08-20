from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Substitution
from app.services.conflict_service import can_assign_substitute
from app.utils.enums import SubstitutionStatus
from app.utils.exceptions import AppError


def assign_substitute(
    db: Session,
    *,
    absence_id: int,
    timetable_id: int,
    substitute_teacher_id: int,
    notes: str | None,
) -> Substitution:
    substitution = db.execute(
        select(Substitution).where(
            Substitution.absence_id == absence_id,
            Substitution.timetable_id == timetable_id,
        )
    ).scalar_one_or_none()

    if not substitution:
        raise AppError("Substitution record not found", "NOT_FOUND", 404)

    valid, message, code = can_assign_substitute(
        db,
        substitution_date=substitution.date,
        period_id=substitution.period_id,
        absent_teacher_id=substitution.original_teacher_id,
        candidate_teacher_id=substitute_teacher_id,
    )
    if not valid:
        raise AppError(message or "Conflict detected", code or "CONFLICT", 409)

    substitution.substitute_teacher_id = substitute_teacher_id
    substitution.status = SubstitutionStatus.assigned
    substitution.notes = notes
    db.commit()
    db.refresh(substitution)
    return substitution


def cancel_substitution(db: Session, substitution_id: int) -> Substitution:
    substitution = db.get(Substitution, substitution_id)
    if not substitution:
        raise AppError("Substitution not found", "NOT_FOUND", 404)
    substitution.status = SubstitutionStatus.cancelled
    db.commit()
    db.refresh(substitution)
    return substitution
