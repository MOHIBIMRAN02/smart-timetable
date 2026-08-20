from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ClassRoom, Subject, Teacher, Timetable, User
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("", summary="Global search by teacher, class, subject or employee code")
def global_search(
    q: str = Query(min_length=1),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    teachers = db.query(Teacher).filter(or_(Teacher.name.ilike(f"%{q}%"), Teacher.employee_code.ilike(f"%{q}%"))).all()
    classes = db.query(ClassRoom).filter(or_(ClassRoom.name.ilike(f"%{q}%"), ClassRoom.class_code.ilike(f"%{q}%"))).all()
    subjects = db.query(Subject).filter(Subject.name.ilike(f"%{q}%")).all()

    teacher_ids = [teacher.id for teacher in teachers]
    schedules = db.query(Timetable).filter(Timetable.teacher_id.in_(teacher_ids)).all() if teacher_ids else []

    return {
        "success": True,
        "query": q,
        "teachers": teachers,
        "classes": classes,
        "subjects": subjects,
        "teacher_schedules": schedules,
    }
