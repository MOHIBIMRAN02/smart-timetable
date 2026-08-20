from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Subject, Teacher, Timetable
from app.schemas.entities import RecommendationReason
from app.services.conflict_service import can_assign_substitute
from app.utils.enums import DayOfWeek, EntityStatus


def _date_to_day(target_date: date) -> DayOfWeek:
    mapping = {
        0: DayOfWeek.monday,
        1: DayOfWeek.tuesday,
        2: DayOfWeek.wednesday,
        3: DayOfWeek.thursday,
        4: DayOfWeek.friday,
    }
    return mapping[target_date.weekday()]


def rank_substitute_candidates(db: Session, *, date_value: date, timetable_entry: Timetable, absent_teacher_id: int) -> list[RecommendationReason]:
    day = _date_to_day(date_value)
    target_subject = db.get(Subject, timetable_entry.subject_id)

    active_teachers = list(db.scalars(select(Teacher).where(Teacher.status == EntityStatus.active)).all())
    recommendations: list[RecommendationReason] = []

    for teacher in active_teachers:
        if teacher.id == absent_teacher_id:
            continue

        valid, conflict_message, _ = can_assign_substitute(
            db,
            substitution_date=date_value,
            period_id=timetable_entry.period_id,
            absent_teacher_id=absent_teacher_id,
            candidate_teacher_id=teacher.id,
        )

        if not valid:
            continue

        score = 0
        reasons: list[str] = []

        subject_match_stmt = select(Timetable.id).where(
            Timetable.teacher_id == teacher.id,
            Timetable.subject_id == timetable_entry.subject_id,
            Timetable.is_active.is_(True),
        ).limit(1)
        same_subject = db.execute(subject_match_stmt).scalar_one_or_none() is not None
        if same_subject:
            score += 40
            reasons.append("Teaches same subject (+40)")

        if target_subject and teacher.department and target_subject.department and teacher.department == target_subject.department:
            score += 20
            reasons.append("Same department (+20)")

        score += 30
        reasons.append("Free during affected period (+30)")

        class_match_stmt = select(Timetable.id).where(
            Timetable.teacher_id == teacher.id,
            Timetable.class_id == timetable_entry.class_id,
            Timetable.is_active.is_(True),
        ).limit(1)
        teaches_class = db.execute(class_match_stmt).scalar_one_or_none() is not None
        if teaches_class:
            score += 10
            reasons.append("Already teaches affected class (+10)")

        if conflict_message:
            score -= 100
            reasons.append(f"Conflict: {conflict_message} (-100)")

        if score > 0:
            recommendations.append(
                RecommendationReason(
                    teacher_id=teacher.id,
                    teacher_name=teacher.name,
                    score=score,
                    reasons=reasons,
                )
            )

    recommendations.sort(key=lambda item: item.score, reverse=True)
    return recommendations
