from __future__ import annotations

from datetime import date, datetime, time

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, String, Text, Time, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.enums import AbsenceStatus, DayOfWeek, EntityStatus, PeriodDayType, SubstitutionStatus, UserRole


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Teacher(Base, TimestampMixin):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    employee_code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(120), unique=True)
    phone: Mapped[str | None] = mapped_column(String(40))
    designation: Mapped[str | None] = mapped_column(String(120))
    department: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[EntityStatus] = mapped_column(Enum(EntityStatus), default=EntityStatus.active)


class ClassRoom(Base, TimestampMixin):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    section: Mapped[str | None] = mapped_column(String(40))
    program: Mapped[str | None] = mapped_column(String(100))
    class_code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    status: Mapped[EntityStatus] = mapped_column(Enum(EntityStatus), default=EntityStatus.active)


class Subject(Base, TimestampMixin):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    short_name: Mapped[str | None] = mapped_column(String(30))
    department: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[EntityStatus] = mapped_column(Enum(EntityStatus), default=EntityStatus.active)


class Period(Base):
    __tablename__ = "periods"
    __table_args__ = (
        UniqueConstraint("period_number", "applicable_day_type", name="uq_period_number_day_type"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    period_number: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    applicable_day_type: Mapped[PeriodDayType] = mapped_column(Enum(PeriodDayType), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Timetable(Base, TimestampMixin):
    __tablename__ = "timetable"
    __table_args__ = (
        UniqueConstraint("day", "period_id", "class_id", name="uq_class_day_period"),
        # teacher conflict detection is handled in the service layer, not enforced at DB level
        # so that seed data with the same teacher across multiple classes can be stored
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day: Mapped[DayOfWeek] = mapped_column(Enum(DayOfWeek), nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey("periods.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id"), nullable=True)
    room: Mapped[str | None] = mapped_column(String(80))
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    teacher: Mapped[Teacher | None] = relationship()
    class_room: Mapped[ClassRoom] = relationship()
    subject: Mapped[Subject] = relationship()
    period: Mapped[Period] = relationship()


class TeacherAbsence(Base):
    __tablename__ = "teacher_absences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[AbsenceStatus] = mapped_column(Enum(AbsenceStatus), default=AbsenceStatus.absent)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    teacher: Mapped[Teacher] = relationship()


class Substitution(Base, TimestampMixin):
    __tablename__ = "substitutions"
    __table_args__ = (
        UniqueConstraint("date", "period_id", "substitute_teacher_id", name="uq_substitute_double_booking"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    absence_id: Mapped[int] = mapped_column(ForeignKey("teacher_absences.id"), nullable=False)
    timetable_id: Mapped[int] = mapped_column(ForeignKey("timetable.id"), nullable=False)
    original_teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    substitute_teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id"))
    date: Mapped[date] = mapped_column(Date, nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey("periods.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    status: Mapped[SubstitutionStatus] = mapped_column(Enum(SubstitutionStatus), default=SubstitutionStatus.pending)
    notes: Mapped[str | None] = mapped_column(Text)

    absence: Mapped[TeacherAbsence] = relationship()
    timetable: Mapped[Timetable] = relationship()


class TeacherAvailability(Base):
    __tablename__ = "teacher_availability"
    __table_args__ = (
        UniqueConstraint("teacher_id", "day", "period_id", name="uq_teacher_availability_slot"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    day: Mapped[DayOfWeek] = mapped_column(Enum(DayOfWeek), nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey("periods.id"), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[str] = mapped_column(String(120), nullable=False)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    entity: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    school_name: Mapped[str] = mapped_column(String(255), default="Smart Timetable School")
    school_logo: Mapped[str | None] = mapped_column(String(255))
    academic_session: Mapped[str | None] = mapped_column(String(60))
    working_days: Mapped[str] = mapped_column(String(120), default="monday,tuesday,wednesday,thursday,friday")
    default_dashboard_view: Mapped[str] = mapped_column(String(60), default="today")
