from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Setting, User
from app.services.audit_service import log_action
from app.utils.deps import get_current_user, require_roles
from app.utils.enums import UserRole

router = APIRouter(prefix="/api/settings", tags=["Settings"])


class SettingPayload(BaseModel):
    school_name: str = Field(min_length=2, max_length=255)
    school_logo: str | None = None
    academic_session: str | None = Field(default=None, max_length=60)
    working_days: str = Field(min_length=3, max_length=120)
    default_dashboard_view: str = Field(min_length=3, max_length=60)


@router.get("", summary="Get settings")
def get_settings(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    setting = db.query(Setting).first()
    if not setting:
        setting = Setting()
        db.add(setting)
        db.commit()
        db.refresh(setting)
    return {"success": True, "item": setting}


@router.put("", summary="Update settings")
def update_settings(
    payload: SettingPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
):
    setting = db.query(Setting).first()
    if not setting:
        setting = Setting(**payload.model_dump())
        db.add(setting)
    else:
        for key, value in payload.model_dump().items():
            setattr(setting, key, value)
    db.commit()
    db.refresh(setting)

    log_action(db, user=current_user.username, action="Updated", entity="Setting", entity_id=str(setting.id))
    return {"success": True, "item": setting}
