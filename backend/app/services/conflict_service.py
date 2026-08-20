from __future__ import annotations

from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models import Substitution, Teacher, TeacherAvailability, Timetable
from app.utils.enums import DayOfWeek, EntityStatus, SubstitutionStatus


def _date_to_day(target_date: date) -> DayOfWeek:
    mapping = {
        0: DayOfWeek.monday,
        1: DayOfWeek.tuesday,
        2: DayOfWeek.wednesday,
        3: DayOfWeek.thursday,
        4: DayOfWeek.friday,
    }
    return mapping[target_date.weekday()]


def has_teacher_timetable_conflict(db: Session, *, day: DayOfWeek, period_id: int, teacher_id: int, exclude_timetable_id: int | None = None) -> bool:
    conditions = [Timetable.day == day, Timetable.period_id == period_id, Timetable.teacher_id == teacher_id, Timetable.is_active.is_(True)]
    if exclude_timetable_id is not None:
        conditions.append(Timetable.id != exclude_timetable_id)
    stmt = select(Timetable.id).where(and_(*conditions)).limit(1)
    return db.execute(stmt).scalar_one_or_none() is not None


def has_class_timetable_conflict(db: Session, *, day: DayOfWeek, period_id: int, class_id: int, exclude_timetable_id: int | None = None) -> bool:
    conditions = [Timetable.day == day, Timetable.period_id == period_id, Timetable.class_id == class_id, Timetable.is_active.is_(True)]
    if exclude_timetable_id is not None:
        conditions.append(Timetable.id != exclude_timetable_id)
    stmt = select(Timetable.id).where(and_(*conditions)).limit(1)
    return db.execute(stmt).scalar_one_or_none() is not None


def can_assign_substitute(db: Session, *, substitution_date: date, period_id: int, absent_teacher_id: int, candidate_teacher_id: int) -> tuple[bool, str | None, str | None]:
    if candidate_teacher_id == absent_teacher_id:
        return False, "Original teacher cannot be substitute.", "ORIGINAL_TEACHER_CONFLICT"

    teacher = db.get(Teacher, candidate_teacher_id)
    if not teacher or teacher.status != EntityStatus.active:
        return False, "Inactive or missing teacher cannot be assigned.", "INACTIVE_TEACHER"

    day = _date_to_day(substitution_date)

    timetable_busy = has_teacher_timetable_conflict(db, day=day, period_id=period_id, teacher_id=candidate_teacher_id)
    if timetable_busy:
        return False, "This teacher is already assigned in timetable during the period.", "TEACHER_CONFLICT"

    substitution_stmt = select(Substitution.id).where(
        Substitution.date == substitution_date,
        Substitution.period_id == period_id,
        Substitution.substitute_teacher_id == candidate_teacher_id,
        Substitution.status == SubstitutionStatus.assigned,
    ).limit(1)
    substitution_busy = db.execute(substitution_stmt).scalar_one_or_none() is not None
    if substitution_busy:
        return False, "This teacher is already assigned as a substitute during the period.", "SUBSTITUTE_DOUBLE_BOOKING"

    availability_stmt = select(TeacherAvailability).where(
        TeacherAvailability.teacher_id == candidate_teacher_id,
        TeacherAvailability.day == day,
        TeacherAvailability.period_id == period_id,
    ).limit(1)
    availability = db.execute(availability_stmt).scalar_one_or_none()
    if availability and not availability.is_available:
        return False, "Teacher is marked unavailable for this period.", "AVAILABILITY_CONFLICT"

    return True, None, None
