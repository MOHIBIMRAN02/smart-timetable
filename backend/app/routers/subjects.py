from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Subject, User
from app.schemas.common import APIMessage
from app.schemas.entities import SubjectCreate, SubjectOut, SubjectUpdate
from app.services.audit_service import log_action
from app.services.crud_service import CRUDService
from app.utils.deps import get_current_user, require_roles
from app.utils.enums import UserRole
from app.utils.exceptions import AppError

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])
service = CRUDService(Subject, "Subject")


@router.get("", response_model=list[SubjectOut], summary="List subjects")
def list_subjects(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.list(db, select(Subject).order_by(Subject.name.asc()))


@router.get("/{subject_id}", response_model=SubjectOut, summary="Get subject")
def get_subject(subject_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.get(db, subject_id)


@router.post("", response_model=SubjectOut, summary="Create subject")
def create_subject(
    payload: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    try:
        entity = service.create(db, payload.model_dump())
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate subject name", "DUPLICATE_SUBJECT", 409) from exc

    log_action(db, user=current_user.username, action="Created", entity="Subject", entity_id=str(entity.id))
    return entity


@router.put("/{subject_id}", response_model=SubjectOut, summary="Update subject")
def update_subject(
    subject_id: int,
    payload: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    data = payload.model_dump(exclude_unset=True)
    try:
        entity = service.update(db, subject_id, data)
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate subject name", "DUPLICATE_SUBJECT", 409) from exc

    log_action(db, user=current_user.username, action="Updated", entity="Subject", entity_id=str(entity.id))
    return entity


@router.delete("/{subject_id}", response_model=APIMessage, summary="Delete subject")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
):
    service.delete(db, subject_id)
    log_action(db, user=current_user.username, action="Deleted", entity="Subject", entity_id=str(subject_id))
    return APIMessage(message="Subject deleted successfully")
