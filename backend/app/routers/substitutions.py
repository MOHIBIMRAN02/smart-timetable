from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Substitution, Timetable, User
from app.schemas.entities import SubstitutionAssignRequest, SubstitutionOut
from app.services.audit_service import log_action
from app.services.recommendation_service import rank_substitute_candidates
from app.services.substitution_service import assign_substitute, cancel_substitution
from app.utils.deps import get_current_user, require_roles
from app.utils.enums import SubstitutionStatus, UserRole
from app.utils.exceptions import AppError

router = APIRouter(prefix="/api/substitutions", tags=["Substitutions"])


@router.get("", response_model=list[SubstitutionOut], summary="List substitutions")
def list_substitutions(
    status: SubstitutionStatus | None = Query(default=None),
    date: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stmt = select(Substitution)
    if status:
        stmt = stmt.where(Substitution.status == status)
    if date:
        stmt = stmt.where(Substitution.date == date)
    return list(db.scalars(stmt.order_by(Substitution.date.desc(), Substitution.period_id.asc())).all())


@router.get("/{substitution_id}", response_model=SubstitutionOut, summary="Get substitution")
def get_substitution(substitution_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    substitution = db.get(Substitution, substitution_id)
    if not substitution:
        raise AppError("Substitution not found", "NOT_FOUND", 404)
    return substitution


@router.get("/recommend/{substitution_id}", summary="Recommend substitutes for a pending substitution")
def recommend_for_substitution(substitution_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    substitution = db.get(Substitution, substitution_id)
    if not substitution:
        raise AppError("Substitution not found", "NOT_FOUND", 404)

    timetable_entry = db.get(Timetable, substitution.timetable_id)
    if not timetable_entry:
        raise AppError("Timetable entry not found", "NOT_FOUND", 404)

    candidates = rank_substitute_candidates(
        db,
        date_value=substitution.date,
        timetable_entry=timetable_entry,
        absent_teacher_id=substitution.original_teacher_id,
    )
    return {
        "success": True,
        "substitution_id": substitution.id,
        "recommendations": [row.model_dump() for row in candidates],
    }


@router.post("/assign", response_model=SubstitutionOut, summary="Assign substitute teacher")
def assign(
    payload: SubstitutionAssignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    substitution = assign_substitute(
        db,
        absence_id=payload.absence_id,
        timetable_id=payload.timetable_id,
        substitute_teacher_id=payload.substitute_teacher_id,
        notes=payload.notes,
    )
    log_action(
        db,
        user=current_user.username,
        action="Assigned substitute",
        entity="Substitution",
        entity_id=str(substitution.id),
        description=f"Substitute teacher {substitution.substitute_teacher_id} assigned",
    )
    return substitution


@router.put("/{substitution_id}/cancel", response_model=SubstitutionOut, summary="Cancel substitution")
def cancel(
    substitution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    substitution = cancel_substitution(db, substitution_id)
    log_action(
        db,
        user=current_user.username,
        action="Cancelled substitution",
        entity="Substitution",
        entity_id=str(substitution.id),
    )
    return substitution
