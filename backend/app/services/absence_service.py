from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Substitution, TeacherAbsence, Timetable
from app.schemas.entities import AffectedPeriod
from app.utils.enums import DayOfWeek, SubstitutionStatus


def _date_to_day(target_date: date) -> DayOfWeek:
    mapping = {
        0: DayOfWeek.monday,
        1: DayOfWeek.tuesday,
        2: DayOfWeek.wednesday,
        3: DayOfWeek.thursday,
        4: DayOfWeek.friday,
    }
    return mapping[target_date.weekday()]


def create_absence_with_pending_substitutions(
    db: Session,
    *,
    teacher_id: int,
    target_date: date,
    reason: str | None,
    notes: str | None,
) -> tuple[TeacherAbsence, list[AffectedPeriod]]:
    day = _date_to_day(target_date)
    absence = TeacherAbsence(teacher_id=teacher_id, date=target_date, reason=reason, notes=notes)
    db.add(absence)
    db.flush()

    affected_timetable = list(
        db.scalars(
            select(Timetable).where(
                Timetable.teacher_id == teacher_id,
                Timetable.day == day,
                Timetable.is_active.is_(True),
            )
        ).all()
    )

    affected_periods: list[AffectedPeriod] = []
    for row in affected_timetable:
        substitution = Substitution(
            absence_id=absence.id,
            timetable_id=row.id,
            original_teacher_id=teacher_id,
            date=target_date,
            period_id=row.period_id,
            class_id=row.class_id,
            subject_id=row.subject_id,
            status=SubstitutionStatus.pending,
        )
        db.add(substitution)

        affected_periods.append(
            AffectedPeriod(
                timetable_id=row.id,
                day=row.day,
                period_id=row.period_id,
                class_id=row.class_id,
                subject_id=row.subject_id,
                teacher_id=row.teacher_id,
            )
        )

    db.commit()
    db.refresh(absence)
    return absence, affected_periods
