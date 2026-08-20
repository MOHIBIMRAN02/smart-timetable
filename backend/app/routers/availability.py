from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TeacherAvailability, User
from app.schemas.common import APIMessage
from app.schemas.entities import TeacherAvailabilityCreate, TeacherAvailabilityOut, TeacherAvailabilityUpdate
from app.services.audit_service import log_action
from app.services.crud_service import CRUDService
from app.utils.deps import get_current_user, require_roles
from app.utils.enums import UserRole
from app.utils.exceptions import AppError

router = APIRouter(prefix="/api/availability", tags=["Teacher Availability"])
service = CRUDService(TeacherAvailability, "Teacher availability")


@router.get("", response_model=list[TeacherAvailabilityOut], summary="List teacher availability")
def list_availability(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.list(db, select(TeacherAvailability).order_by(TeacherAvailability.teacher_id.asc()))


@router.post("", response_model=TeacherAvailabilityOut, summary="Create availability slot")
def create_availability(
    payload: TeacherAvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    try:
        entity = service.create(db, payload.model_dump())
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate teacher availability slot", "DUPLICATE_AVAILABILITY", 409) from exc
    log_action(db, user=current_user.username, action="Created", entity="TeacherAvailability", entity_id=str(entity.id))
    return entity


@router.put("/{availability_id}", response_model=TeacherAvailabilityOut, summary="Update availability slot")
def update_availability(
    availability_id: int,
    payload: TeacherAvailabilityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    entity = service.update(db, availability_id, payload.model_dump(exclude_unset=True))
    log_action(db, user=current_user.username, action="Updated", entity="TeacherAvailability", entity_id=str(entity.id))
    return entity


@router.delete("/{availability_id}", response_model=APIMessage, summary="Delete availability slot")
def delete_availability(
    availability_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
):
    service.delete(db, availability_id)
    log_action(db, user=current_user.username, action="Deleted", entity="TeacherAvailability", entity_id=str(availability_id))
    return APIMessage(message="Availability deleted successfully")
