from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Teacher, User
from app.schemas.common import APIMessage
from app.schemas.entities import TeacherCreate, TeacherOut, TeacherUpdate
from app.services.audit_service import log_action
from app.services.crud_service import CRUDService
from app.utils.deps import get_current_user, require_roles
from app.utils.enums import UserRole
from app.utils.exceptions import AppError

router = APIRouter(prefix="/api/teachers", tags=["Teachers"])
service = CRUDService(Teacher, "Teacher")


@router.get("", response_model=list[TeacherOut], summary="List teachers")
def list_teachers(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.list(db, select(Teacher).order_by(Teacher.name.asc()))


@router.get("/{teacher_id}", response_model=TeacherOut, summary="Get teacher")
def get_teacher(teacher_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.get(db, teacher_id)


@router.post("", response_model=TeacherOut, summary="Create teacher")
def create_teacher(
    payload: TeacherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    try:
        teacher = service.create(db, payload.model_dump())
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate employee code or email", "DUPLICATE_TEACHER", 409) from exc

    log_action(db, user=current_user.username, action="Created", entity="Teacher", entity_id=str(teacher.id))
    return teacher


@router.put("/{teacher_id}", response_model=TeacherOut, summary="Update teacher")
def update_teacher(
    teacher_id: int,
    payload: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    data = payload.model_dump(exclude_unset=True)
    if not data:
        return service.get(db, teacher_id)

    try:
        teacher = service.update(db, teacher_id, data)
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate employee code or email", "DUPLICATE_TEACHER", 409) from exc

    log_action(db, user=current_user.username, action="Updated", entity="Teacher", entity_id=str(teacher.id))
    return teacher


@router.delete("/{teacher_id}", response_model=APIMessage, summary="Delete teacher")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
):
    service.delete(db, teacher_id)
    log_action(db, user=current_user.username, action="Deleted", entity="Teacher", entity_id=str(teacher_id))
    return APIMessage(message="Teacher deleted successfully")
