from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ClassRoom, Substitution, Teacher, TeacherAbsence, Timetable
from app.utils.enums import SubstitutionStatus


def teacher_weekly_schedule(db: Session, teacher_id: int):
    return list(db.scalars(select(Timetable).where(Timetable.teacher_id == teacher_id)).all())


def class_weekly_schedule(db: Session, class_id: int):
    return list(db.scalars(select(Timetable).where(Timetable.class_id == class_id)).all())


def daily_substitution_sheet(db: Session, target_date: date):
    return list(
        db.scalars(
            select(Substitution).where(
                Substitution.date == target_date,
                Substitution.status == SubstitutionStatus.assigned,
            )
        ).all()
    )


def teacher_workload(db: Session):
    stmt = (
        select(Teacher.name, func.count(Timetable.id).label("periods"))
        .join(Timetable, Timetable.teacher_id == Teacher.id)
        .group_by(Teacher.id)
        .order_by(func.count(Timetable.id).desc())
    )
    return [{"teacher": row[0], "weekly_periods": row[1]} for row in db.execute(stmt).all()]


def dashboard_summary(db: Session, target_date: date):
    return {
        "total_teachers": db.scalar(select(func.count(Teacher.id))) or 0,
        "total_classes": db.scalar(select(func.count(ClassRoom.id))) or 0,
        "total_subjects": db.scalar(select(func.count(Timetable.subject_id.distinct()))) or 0,
        "absent_teachers": db.scalar(select(func.count(TeacherAbsence.id)).where(TeacherAbsence.date == target_date)) or 0,
        "pending_substitutions": db.scalar(
            select(func.count(Substitution.id)).where(
                Substitution.date == target_date,
                Substitution.status == SubstitutionStatus.pending,
            )
        )
        or 0,
        "assigned_substitutions": db.scalar(
            select(func.count(Substitution.id)).where(
                Substitution.date == target_date,
                Substitution.status == SubstitutionStatus.assigned,
            )
        )
        or 0,
    }
