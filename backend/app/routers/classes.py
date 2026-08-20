from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ClassRoom, User
from app.schemas.common import APIMessage
from app.schemas.entities import ClassCreate, ClassOut, ClassUpdate
from app.services.audit_service import log_action
from app.services.crud_service import CRUDService
from app.utils.deps import get_current_user, require_roles
from app.utils.enums import UserRole
from app.utils.exceptions import AppError

router = APIRouter(prefix="/api/classes", tags=["Classes"])
service = CRUDService(ClassRoom, "Class")


@router.get("", response_model=list[ClassOut], summary="List classes")
def list_classes(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.list(db, select(ClassRoom).order_by(ClassRoom.name.asc()))


@router.get("/{class_id}", response_model=ClassOut, summary="Get class")
def get_class(class_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.get(db, class_id)


@router.post("", response_model=ClassOut, summary="Create class")
def create_class(
    payload: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    try:
        entity = service.create(db, payload.model_dump())
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate class code", "DUPLICATE_CLASS_CODE", 409) from exc

    log_action(db, user=current_user.username, action="Created", entity="Class", entity_id=str(entity.id))
    return entity


@router.put("/{class_id}", response_model=ClassOut, summary="Update class")
def update_class(
    class_id: int,
    payload: ClassUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    data = payload.model_dump(exclude_unset=True)
    try:
        entity = service.update(db, class_id, data)
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate class code", "DUPLICATE_CLASS_CODE", 409) from exc

    log_action(db, user=current_user.username, action="Updated", entity="Class", entity_id=str(entity.id))
    return entity


@router.delete("/{class_id}", response_model=APIMessage, summary="Delete class")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
):
    service.delete(db, class_id)
    log_action(db, user=current_user.username, action="Deleted", entity="Class", entity_id=str(class_id))
    return APIMessage(message="Class deleted successfully")
