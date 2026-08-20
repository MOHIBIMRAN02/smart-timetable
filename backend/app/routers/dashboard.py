from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Substitution, TeacherAbsence, Timetable, User
from app.services.report_service import dashboard_summary
from app.utils.deps import get_current_user
from app.utils.enums import SubstitutionStatus

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("", summary="Dashboard analytics and today's operational schedule")
def get_dashboard(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    today = date.today()
    summary = dashboard_summary(db, today)

    today_absences = list(db.scalars(select(TeacherAbsence).where(TeacherAbsence.date == today)).all())
    today_substitutions = list(db.scalars(select(Substitution).where(Substitution.date == today)).all())

    return {
        "success": True,
        "summary": summary,
        "today_timetable": list(db.scalars(select(Timetable).where(Timetable.is_active.is_(True))).all()),
        "today_absences": today_absences,
        "today_substitutions": today_substitutions,
        "pending_count": len([x for x in today_substitutions if x.status == SubstitutionStatus.pending]),
    }
