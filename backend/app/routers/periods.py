from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Period, User
from app.schemas.common import APIMessage
from app.schemas.entities import PeriodCreate, PeriodOut, PeriodUpdate
from app.services.audit_service import log_action
from app.services.crud_service import CRUDService
from app.utils.deps import get_current_user, require_roles
from app.utils.enums import UserRole
from app.utils.exceptions import AppError

router = APIRouter(prefix="/api/periods", tags=["Periods"])
service = CRUDService(Period, "Period")


@router.get("", response_model=list[PeriodOut], summary="List periods")
def list_periods(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.list(db, select(Period).order_by(Period.period_number.asc()))


@router.get("/{period_id}", response_model=PeriodOut, summary="Get period")
def get_period(period_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return service.get(db, period_id)


@router.post("", response_model=PeriodOut, summary="Create period")
def create_period(
    payload: PeriodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    try:
        entity = service.create(db, payload.model_dump())
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate period number for this day type", "DUPLICATE_PERIOD", 409) from exc

    log_action(db, user=current_user.username, action="Created", entity="Period", entity_id=str(entity.id))
    return entity


@router.put("/{period_id}", response_model=PeriodOut, summary="Update period")
def update_period(
    period_id: int,
    payload: PeriodUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.scheduler)),
):
    data = payload.model_dump(exclude_unset=True)
    try:
        entity = service.update(db, period_id, data)
    except IntegrityError as exc:
        db.rollback()
        raise AppError("Duplicate period number for this day type", "DUPLICATE_PERIOD", 409) from exc

    log_action(db, user=current_user.username, action="Updated", entity="Period", entity_id=str(entity.id))
    return entity


@router.delete("/{period_id}", response_model=APIMessage, summary="Delete period")
def delete_period(
    period_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
):
    service.delete(db, period_id)
    log_action(db, user=current_user.username, action="Deleted", entity="Period", entity_id=str(period_id))
    return APIMessage(message="Period deleted successfully")
