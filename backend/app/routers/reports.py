from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Substitution, TeacherAbsence, Timetable, User
from app.services.report_service import class_weekly_schedule, daily_substitution_sheet, teacher_weekly_schedule, teacher_workload
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/teacher/{teacher_id}", summary="Teacher weekly schedule")
def teacher_schedule(teacher_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = teacher_weekly_schedule(db, teacher_id)
    return {"success": True, "items": rows}


@router.get("/class/{class_id}", summary="Class weekly schedule")
def class_schedule(class_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = class_weekly_schedule(db, class_id)
    return {"success": True, "items": rows}


@router.get("/daily", summary="Daily timetable")
def daily_timetable(day: str = Query(default="monday"), db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(Timetable).filter(Timetable.day == day).all()
    return {"success": True, "items": rows}


@router.get("/absences", summary="Absence report")
def absence_report(
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    teacher_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stmt = db.query(TeacherAbsence)
    if teacher_id:
        stmt = stmt.filter(TeacherAbsence.teacher_id == teacher_id)
    if start:
        stmt = stmt.filter(TeacherAbsence.date >= start)
    if end:
        stmt = stmt.filter(TeacherAbsence.date <= end)
    return {"success": True, "items": stmt.order_by(TeacherAbsence.date.desc()).all()}


@router.get("/substitutions", summary="Substitution report")
def substitution_report(
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    teacher_id: int | None = Query(default=None),
    class_id: int | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stmt = db.query(Substitution)
    if teacher_id:
        stmt = stmt.filter((Substitution.original_teacher_id == teacher_id) | (Substitution.substitute_teacher_id == teacher_id))
    if class_id:
        stmt = stmt.filter(Substitution.class_id == class_id)
    if status:
        stmt = stmt.filter(Substitution.status == status)
    if start:
        stmt = stmt.filter(Substitution.date >= start)
    if end:
        stmt = stmt.filter(Substitution.date <= end)
    return {"success": True, "items": stmt.order_by(Substitution.date.desc()).all()}


@router.get("/workload", summary="Teacher workload")
def workload(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return {"success": True, "items": teacher_workload(db)}


@router.get("/daily-substitution-sheet", summary="Printable daily substitution sheet")
def substitution_sheet(
    date_value: date = Query(alias="date"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    items = daily_substitution_sheet(db, date_value)
    return {
        "success": True,
        "school_title": "SMART TIMETABLE",
        "generated_at": date.today().isoformat(),
        "date": date_value,
        "items": items,
    }
