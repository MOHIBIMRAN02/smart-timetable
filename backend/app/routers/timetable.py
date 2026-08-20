from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Timetable, User
from app.schemas.common import APIMessage
from app.schemas.entities import TimetableCreate, TimetableOut, TimetableUpdate
from app.services.audit_service import log_action
from app.services.crud_service import CRUDService
from app.services.conflict_service import has_class_timetable_conflict, has_teacher_timetable_conflict
from app.utils.deps import get_current_user, require_roles
from app.utils.enums import DayOfWeek, UserRole
from app.utils.exceptions import AppError

router = APIRouter(prefix="/api/timetable", tags=["Timetable"])
service = CRUDService(Timetable, "Timetable entry")


@router.get("", response_model=list[TimetableOut], summary="List timetable entries")
def list_timetable(
    day: DayOfWeek | None = Query(default=None),
    class_id: int | None = Query(default=None),
    teacher_id: int | None = Query(default=None),
    subject_id: int | None = Query(default=None),
    period_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stmt = select(Timetable)
    if day:
        stmt = stmt.where(Timetable.day == day)
    if class_id:
        stmt = stmt.where(Timetable.class_id == class_id)
    if teacher_id:
        stmt = stmt.where(Timetable.teacher_id == teacher_id)
    if subject_id:
        stmt = stmt.where(Timetable.subject_id == subject_id)
    if period_id:
        stmt = stmt.where(Timetable.period_id == period_id)
    return service.list(db, stmt.order_by(Timetable.day.asc(), Timetable.period_id.asc()))


@router.get("/{entry_id}", response_model=TimetableOut, summary="Get timetable entry")
def get_timetable_entry(entry_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.get(db, entry_id)


@router.post("", response_model=TimetableOut, summary="Create timetable entry")
def create_timetable_entry(
    payload: TimetableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    if has_teacher_timetable_conflict(db, day=payload.day, period_id=payload.period_id, teacher_id=payload.teacher_id):
        raise AppError("Teacher is already assigned during this period.", "TEACHER_CONFLICT", 409)
    if has_class_timetable_conflict(db, day=payload.day, period_id=payload.period_id, class_id=payload.class_id):
        raise AppError("Class already has timetable in this period.", "CLASS_CONFLICT", 409)

    try:
        entity = service.create(db, payload.model_dump())
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate timetable assignment", "TIMETABLE_DUPLICATE", 409) from exc

    log_action(db, user=current_user.username, action="Created", entity="Timetable", entity_id=str(entity.id))
    return entity


@router.put("/{entry_id}", response_model=TimetableOut, summary="Update timetable entry")
def update_timetable_entry(
    entry_id: int,
    payload: TimetableUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    current = service.get(db, entry_id)
    data = payload.model_dump(exclude_unset=True)

    check_day = data.get("day", current.day)
    check_period = data.get("period_id", current.period_id)
    check_teacher = data.get("teacher_id", current.teacher_id)
    check_class = data.get("class_id", current.class_id)

    # Only check teacher conflict if teacher/period/day actually changed
    teacher_changed = (
        check_teacher != current.teacher_id
        or check_period != current.period_id
        or check_day != current.day
    )
    if check_teacher and teacher_changed:
        if has_teacher_timetable_conflict(
            db,
            day=check_day,
            period_id=check_period,
            teacher_id=check_teacher,
            exclude_timetable_id=entry_id,
        ):
            raise AppError("Teacher is already assigned during this period.", "TEACHER_CONFLICT", 409)

    # Only check class conflict if class/period/day actually changed
    class_changed = (
        check_class != current.class_id
        or check_period != current.period_id
        or check_day != current.day
    )
    if class_changed:
        if has_class_timetable_conflict(
            db,
            day=check_day,
            period_id=check_period,
            class_id=check_class,
            exclude_timetable_id=entry_id,
        ):
            raise AppError("Class already has timetable in this period.", "CLASS_CONFLICT", 409)

    try:
        entity = service.update(db, entry_id, data)
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate timetable assignment", "TIMETABLE_DUPLICATE", 409) from exc

    log_action(db, user=current_user.username, action="Updated", entity="Timetable", entity_id=str(entity.id))
    return entity


@router.delete("/{entry_id}", response_model=APIMessage, summary="Delete timetable entry")
def delete_timetable_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
):
    service.delete(db, entry_id)
    log_action(db, user=current_user.username, action="Deleted", entity="Timetable", entity_id=str(entry_id))
    return APIMessage(message="Timetable entry deleted successfully")
