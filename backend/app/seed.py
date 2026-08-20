from __future__ import annotations

from datetime import date, timedelta, time

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import (
    ClassRoom,
    Period,
    Setting,
    Subject,
    Substitution,
    Teacher,
    TeacherAbsence,
    TeacherAvailability,
    Timetable,
    User,
)
from app.utils.enums import AbsenceStatus, DayOfWeek, EntityStatus, PeriodDayType, SubstitutionStatus, UserRole
from app.utils.security import hash_password


# Seed assumptions from timetable image:
# - The image is a single-sheet class timetable with day markers (1-5) for Mon-Fri.
# - Where multiple teachers are listed for one slot, primary/alternate teachers are used
#   and auto-distributed across weekdays to prevent teacher double-booking.
# - Period 4 appears to be break; it is not stored as class teaching assignment.


def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seed_users(db):
    users = [
        User(name="System Admin", username="admin", password_hash=hash_password("admin123"), role=UserRole.admin, is_active=True),
        User(name="Scheduler Staff", username="scheduler", password_hash=hash_password("scheduler123"), role=UserRole.scheduler, is_active=True),
    ]
    db.add_all(users)


def seed_teachers(db):
    teachers = [
        Teacher(name="Ms. Arshia", employee_code="T001", department="Science", designation="Teacher", status=EntityStatus.active),
        Teacher(name="Sir Javed", employee_code="T002", department="Science", designation="Teacher", status=EntityStatus.active),
        Teacher(name="Ms. Maheen", employee_code="T003", department="Arts", designation="Teacher", status=EntityStatus.active),
        Teacher(name="Sir Suhaib", employee_code="T004", department="Islamic Studies", designation="Teacher", status=EntityStatus.active),
        Teacher(name="Ms. Rashida", employee_code="T005", department="Languages", designation="Teacher", status=EntityStatus.active),
        Teacher(name="Ms. Tayyaba", employee_code="T006", department="Science", designation="Teacher", status=EntityStatus.active),
        Teacher(name="Ms. Nousheen", employee_code="T007", department="Languages", designation="Teacher", status=EntityStatus.active),
        Teacher(name="Sir Kashif", employee_code="T008", department="Computer", designation="Teacher", status=EntityStatus.active),
        Teacher(name="Ms. Numaira", employee_code="T009", department="Science", designation="Teacher", status=EntityStatus.active),
        Teacher(name="Ms. Noor", employee_code="T010", department="Science", designation="Teacher", status=EntityStatus.active),
    ]
    db.add_all(teachers)


def seed_classes(db):
    classes = [
        ClassRoom(name="B1", section="B", program="Engg+Med", class_code="B1", status=EntityStatus.active),
        ClassRoom(name="B2", section="B", program="ICS-MPC", class_code="B2", status=EntityStatus.active),
        ClassRoom(name="B3", section="B", program="FA.IT", class_code="B3", status=EntityStatus.active),
        ClassRoom(name="A1", section="A", program="Engg+Med", class_code="A1", status=EntityStatus.active),
        ClassRoom(name="A2", section="A", program="ICS-MPC", class_code="A2", status=EntityStatus.active),
        ClassRoom(name="A3", section="A", program="FA.IT", class_code="A3", status=EntityStatus.active),
        ClassRoom(name="IX", section="IX", program="General", class_code="IX", status=EntityStatus.active),
    ]
    db.add_all(classes)


def seed_subjects(db):
    subjects = [
        Subject(name="Assembly / Awareness", short_name="Assembly", department="General", status=EntityStatus.active),
        Subject(name="Physics", short_name="Physics", department="Science", status=EntityStatus.active),
        Subject(name="Chemistry", short_name="Chemistry", department="Science", status=EntityStatus.active),
        Subject(name="Computer", short_name="Computer", department="Computer", status=EntityStatus.active),
        Subject(name="Mathematics", short_name="Mathematics", department="Science", status=EntityStatus.active),
        Subject(name="English", short_name="English", department="Languages", status=EntityStatus.active),
        Subject(name="Urdu", short_name="Urdu", department="Languages", status=EntityStatus.active),
        Subject(name="Biology", short_name="Biology", department="Science", status=EntityStatus.active),
        Subject(name="Sociology", short_name="Sociology", department="Arts", status=EntityStatus.active),
        Subject(name="Education", short_name="Education", department="Arts", status=EntityStatus.active),
        Subject(name="T.Q / Isl", short_name="T.Q / Isl", department="Islamic Studies", status=EntityStatus.active),
        Subject(name="Pak Study", short_name="Pak Study", department="Arts", status=EntityStatus.active),
        Subject(name="Physics / Stats", short_name="Physics / Stats", department="Science", status=EntityStatus.active),
        Subject(name="Biology / Computer", short_name="Bio / Comp", department="Science", status=EntityStatus.active),
        Subject(name="Urdu / English", short_name="Urdu / Eng", department="Languages", status=EntityStatus.active),
        Subject(name="Break", short_name="Break", department="General", status=EntityStatus.active),
    ]
    db.add_all(subjects)


def seed_periods(db):
    # Times taken directly from the handwritten reference table image
    # P0 = Assembly, P4 = Break, P1-P3 and P5-P8 = teaching periods
    mon_thu = [
        (0, time(8,  0), time(8,  20)),   # Assembly
        (1, time(8,  20), time(9,  0)),    # Period 1
        (2, time(9,  0), time(9,  40)),    # Period 2
        (3, time(9,  40), time(10, 20)),   # Period 3
        (4, time(10, 20), time(11, 0)),    # Break
        (5, time(11, 0), time(11, 40)),    # Period 5
        (6, time(11, 40), time(12, 20)),   # Period 6
        (7, time(12, 20), time(13, 0)),    # Period 7
        (8, time(13, 0), time(13, 40)),    # Period 8
    ]
    friday = [
        (0, time(8,  0), time(8,  10)),   # Assembly
        (1, time(8,  10), time(8,  45)),   # Period 1
        (2, time(8,  45), time(9,  20)),   # Period 2
        (3, time(9,  20), time(9,  55)),   # Period 3
        (4, time(9,  55), time(10, 25)),   # Break
        (5, time(10, 25), time(10, 55)),   # Period 5
        (6, time(10, 55), time(11, 25)),   # Period 6
        (7, time(11, 25), time(12, 0)),    # Period 7
        (8, time(12, 0), time(12, 30)),    # Period 8 (estimated)
    ]
    for number, start, end in mon_thu:
        db.add(Period(period_number=number, start_time=start, end_time=end,
                      applicable_day_type=PeriodDayType.mon_thu, is_active=True))
    for number, start, end in friday:
        db.add(Period(period_number=number, start_time=start, end_time=end,
                      applicable_day_type=PeriodDayType.friday, is_active=True))


def seed_settings(db):
    db.add(
        Setting(
            school_name="Smart Timetable School",
            academic_session="2026-2027",
            working_days="monday,tuesday,wednesday,thursday,friday",
            default_dashboard_view="today",
        )
    )


def seed_timetable(db):
    teachers = {t.name: t for t in db.scalars(select(Teacher)).all()}
    classes = {c.class_code: c for c in db.scalars(select(ClassRoom)).all()}
    subjects = {s.name: s for s in db.scalars(select(Subject)).all()}

    mon_thu_periods = {
        p.period_number: p
        for p in db.scalars(select(Period).where(Period.applicable_day_type == PeriodDayType.mon_thu)).all()
    }
    friday_periods = {
        p.period_number: p
        for p in db.scalars(select(Period).where(Period.applicable_day_type == PeriodDayType.friday)).all()
    }

    # ---------------------------------------------------------------
    # Reference table — Mon-Thu (same schedule all 4 days)
    # period 0 = Assembly (no teacher)
    # period 4 = Break    (None,None = skip entirely)
    # periods 1-3, 5-8   = teaching slots
    # ---------------------------------------------------------------
    mon_thu_data = {
        # B1 — Engg+Med
        "B1": {
            0: ("Assembly / Awareness", None),
            1: ("Physics",             "Ms. Arshia"),
            2: ("Chemistry",           "Sir Javed"),
            3: ("Pak Study",           "Ms. Maheen"),
            4: (None, None),                          # Break
            5: ("Urdu",                "Ms. Rashida"),
            6: ("Biology",             "Ms. Tayyaba"),
            7: ("English",             "Ms. Nousheen"),
            8: ("T.Q / Isl",           "Sir Suhaib"),
        },
        # B2 — ICS-MPC
        "B2": {
            0: ("Assembly / Awareness", None),
            1: ("Mathematics",          "Ms. Noor"),
            2: ("Computer",             "Sir Kashif"),
            3: ("Physics / Stats",      "Ms. Arshia"),
            4: (None, None),
            5: ("T.Q / Isl",            "Sir Suhaib"),
            6: ("English",              "Ms. Nousheen"),
            7: ("Urdu",                 "Ms. Rashida"),
            8: ("Pak Study",            "Ms. Maheen"),
        },
        # B3 — FA.IT
        "B3": {
            0: ("Assembly / Awareness", None),
            1: ("Sociology",            "Ms. Maheen"),
            2: ("Computer",             "Sir Kashif"),
            3: ("Pak Study",            "Ms. Maheen"),
            4: (None, None),
            5: ("Urdu",                 "Ms. Rashida"),
            6: ("Education",            "Ms. Maheen"),
            7: ("English",              "Ms. Nousheen"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
        # A1 — Engg+Med
        "A1": {
            0: ("Assembly / Awareness", None),
            1: ("Biology",              "Ms. Tayyaba"),
            2: ("Urdu",                 "Ms. Rashida"),
            3: ("Chemistry",            "Sir Javed"),
            4: (None, None),
            5: ("English",              "Ms. Nousheen"),
            6: ("T.Q / Isl",            "Sir Suhaib"),
            7: ("Physics",              "Ms. Arshia"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
        # A2 — ICS-MPC
        "A2": {
            0: ("Assembly / Awareness", None),
            1: ("English",              "Ms. Nousheen"),
            2: ("Urdu",                 "Ms. Rashida"),
            3: ("Computer",             "Sir Kashif"),
            4: (None, None),
            5: ("Mathematics",          "Ms. Noor"),
            6: ("T.Q / Isl",            "Sir Suhaib"),
            7: ("Physics / Stats",      "Ms. Arshia"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
        # A3 — FA.IT
        "A3": {
            0: ("Assembly / Awareness", None),
            1: ("Urdu",                 "Ms. Rashida"),
            2: ("Sociology",            "Ms. Maheen"),
            3: ("Computer",             "Sir Kashif"),
            4: (None, None),
            5: ("English",              "Ms. Nousheen"),
            6: ("T.Q / Isl",            "Sir Suhaib"),
            7: ("Education",            "Ms. Maheen"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
        # IX — 9th Grade
        "IX": {
            0: ("Assembly / Awareness", None),
            1: ("Chemistry",            "Ms. Numaira"),
            2: ("English",              "Ms. Nousheen"),
            3: ("T.Q / Isl",            "Sir Suhaib"),
            4: (None, None),
            5: ("Physics",              "Ms. Arshia"),
            6: ("Mathematics",          "Ms. Noor"),
            7: ("T.Q / Isl",            "Sir Suhaib"),
            8: ("Urdu",                 "Ms. Rashida"),
        },
    }

    # ---------------------------------------------------------------
    # Friday — shorter periods
    # ---------------------------------------------------------------
    friday_data = {
        "B1": {
            0: ("Assembly / Awareness", None),
            1: ("English",              "Ms. Nousheen"),
            2: ("Biology",              "Ms. Tayyaba"),
            3: ("Urdu",                 "Ms. Rashida"),
            4: (None, None),
            5: ("Pak Study",            "Ms. Maheen"),
            6: ("Chemistry",            "Sir Javed"),
            7: ("Physics",              "Ms. Arshia"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
        "B2": {
            0: ("Assembly / Awareness", None),
            1: ("Urdu",                 "Ms. Rashida"),
            2: ("English",              "Ms. Nousheen"),
            3: ("T.Q / Isl",            "Sir Suhaib"),
            4: (None, None),
            5: ("Mathematics",          "Ms. Noor"),
            6: ("Computer",             "Sir Kashif"),
            7: ("Physics / Stats",      "Ms. Arshia"),
            8: ("Pak Study",            "Ms. Maheen"),
        },
        "B3": {
            0: ("Assembly / Awareness", None),
            1: ("English",              "Ms. Nousheen"),
            2: ("Education",            "Ms. Maheen"),
            3: ("Urdu",                 "Ms. Rashida"),
            4: (None, None),
            5: ("Sociology",            "Ms. Maheen"),
            6: ("Pak Study",            "Ms. Maheen"),
            7: ("Computer",             "Sir Kashif"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
        "A1": {
            0: ("Assembly / Awareness", None),
            1: ("Physics",              "Ms. Arshia"),
            2: ("T.Q / Isl",            "Sir Suhaib"),
            3: ("English",              "Ms. Nousheen"),
            4: (None, None),
            5: ("Biology",              "Ms. Tayyaba"),
            6: ("Urdu",                 "Ms. Rashida"),
            7: ("Chemistry",            "Sir Javed"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
        "A2": {
            0: ("Assembly / Awareness", None),
            1: ("Physics / Stats",      "Ms. Arshia"),
            2: ("Mathematics",          "Ms. Noor"),
            3: ("English",              "Ms. Nousheen"),
            4: (None, None),
            5: ("Computer",             "Sir Kashif"),
            6: ("T.Q / Isl",            "Sir Suhaib"),
            7: ("Urdu",                 "Ms. Rashida"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
        "A3": {
            0: ("Assembly / Awareness", None),
            1: ("Education",            "Ms. Maheen"),
            2: ("Urdu",                 "Ms. Rashida"),
            3: ("English",              "Ms. Nousheen"),
            4: (None, None),
            5: ("T.Q / Isl",            "Sir Suhaib"),
            6: ("Sociology",            "Ms. Maheen"),
            7: ("Computer",             "Sir Kashif"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
        "IX": {
            0: ("Assembly / Awareness", None),
            1: ("T.Q / Isl",            "Sir Suhaib"),
            2: ("Mathematics",          "Ms. Noor"),
            3: ("Chemistry",            "Ms. Numaira"),
            4: (None, None),
            5: ("English",              "Ms. Nousheen"),
            6: ("Physics",              "Ms. Arshia"),
            7: ("Urdu",                 "Ms. Rashida"),
            8: ("T.Q / Isl",            "Sir Suhaib"),
        },
    }

    def add_entries(day, timetable_data, period_lookup):
        for class_code, period_map in timetable_data.items():
            for period_number, (subject_name, teacher_name) in period_map.items():
                if subject_name is None:
                    continue  # Skip Break

                class_obj = classes.get(class_code)
                subject_obj = subjects.get(subject_name)
                period_obj = period_lookup.get(period_number)
                teacher_obj = teachers.get(teacher_name) if teacher_name else None

                if not all([class_obj, subject_obj, period_obj]):
                    print(f"  SKIP: {day} {class_code} P{period_number} "
                          f"(class={class_obj is not None} subj={subject_obj is not None} "
                          f"period={period_obj is not None}) — {subject_name}")
                    continue
                if teacher_name and not teacher_obj:
                    print(f"  SKIP: teacher '{teacher_name}' not found — {class_code} P{period_number}")
                    continue

                db.add(Timetable(
                    day=day,
                    period_id=period_obj.id,
                    class_id=class_obj.id,
                    subject_id=subject_obj.id,
                    teacher_id=teacher_obj.id if teacher_obj else None,
                    room=None,
                    notes="Seeded from reference schedule",
                    is_active=True,
                ))

    for day in [DayOfWeek.monday, DayOfWeek.tuesday, DayOfWeek.wednesday, DayOfWeek.thursday]:
        add_entries(day, mon_thu_data, mon_thu_periods)
    add_entries(DayOfWeek.friday, friday_data, friday_periods)


def seed_availability(db):
    teachers = {t.name: t for t in db.scalars(select(Teacher)).all()}
    periods = {
        p.period_number: p
        for p in db.scalars(select(Period).where(Period.applicable_day_type == PeriodDayType.mon_thu)).all()
    }

    entries = [
        ("Ms. Noor", DayOfWeek.monday, 2, False, "On lab duty"),
        ("Sir Kashif", DayOfWeek.monday, 7, False, "Computer lab setup"),
        ("Ms. Maheen", DayOfWeek.monday, 1, True, "Available for substitute"),
        ("Sir Suhaib", DayOfWeek.monday, 5, True, "Available for substitute"),
    ]

    for teacher_name, day, period_number, is_available, notes in entries:
        db.add(
            TeacherAvailability(
                teacher_id=teachers[teacher_name].id,
                day=day,
                period_id=periods[period_number].id,
                is_available=is_available,
                notes=notes,
            )
        )


def seed_demo_absence_and_pending_substitutions(db):
    teachers = {t.name: t for t in db.scalars(select(Teacher)).all()}

    # find next Monday for demo workflow
    target_date = date.today()
    while target_date.weekday() != 0:
        target_date += timedelta(days=1)

    absence = TeacherAbsence(
        teacher_id=teachers["Ms. Arshia"].id,
        date=target_date,
        reason="Medical leave",
        status=AbsenceStatus.absent,
        notes="Demo scenario for substitution engine",
    )
    db.add(absence)
    db.flush()

    monday_rows = list(
        db.scalars(
            select(Timetable).where(
                Timetable.day == DayOfWeek.monday,
                Timetable.teacher_id == teachers["Ms. Arshia"].id,
                Timetable.is_active.is_(True),
            )
        ).all()
    )

    for row in monday_rows:
        db.add(
            Substitution(
                absence_id=absence.id,
                timetable_id=row.id,
                original_teacher_id=row.teacher_id,
                substitute_teacher_id=None,
                date=target_date,
                period_id=row.period_id,
                class_id=row.class_id,
                subject_id=row.subject_id,
                status=SubstitutionStatus.pending,
                notes="Auto-created from absence",
            )
        )


def main() -> None:
    reset_database()
    with SessionLocal() as db:
        seed_users(db)
        seed_teachers(db)
        seed_classes(db)
        seed_subjects(db)
        seed_periods(db)
        seed_settings(db)
        db.commit()

        seed_timetable(db)
        seed_availability(db)
        db.commit()

        seed_demo_absence_and_pending_substitutions(db)
        db.commit()

    print("Database seeded successfully")
    print("Admin login: admin / admin123")
    print("Scheduler login: scheduler / scheduler123")


if __name__ == "__main__":
    main()
