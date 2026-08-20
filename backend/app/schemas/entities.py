from __future__ import annotations

from datetime import date, time

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.common import ORMBase, TimestampedSchema
from app.utils.enums import AbsenceStatus, DayOfWeek, EntityStatus, PeriodDayType, SubstitutionStatus, UserRole


class UserOut(TimestampedSchema):
    id: int
    name: str
    username: str
    role: UserRole
    is_active: bool


class TeacherBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    employee_code: str = Field(min_length=2, max_length=40)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=40)
    designation: str | None = Field(default=None, max_length=120)
    department: str | None = Field(default=None, max_length=120)
    status: EntityStatus = EntityStatus.active


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    employee_code: str | None = Field(default=None, min_length=2, max_length=40)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=40)
    designation: str | None = Field(default=None, max_length=120)
    department: str | None = Field(default=None, max_length=120)
    status: EntityStatus | None = None


class TeacherOut(TeacherBase, TimestampedSchema):
    id: int


class ClassBase(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    section: str | None = Field(default=None, max_length=40)
    program: str | None = Field(default=None, max_length=100)
    class_code: str = Field(min_length=1, max_length=40)
    status: EntityStatus = EntityStatus.active


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=60)
    section: str | None = Field(default=None, max_length=40)
    program: str | None = Field(default=None, max_length=100)
    class_code: str | None = Field(default=None, min_length=1, max_length=40)
    status: EntityStatus | None = None


class ClassOut(ClassBase, TimestampedSchema):
    id: int


class SubjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    short_name: str | None = Field(default=None, max_length=30)
    department: str | None = Field(default=None, max_length=100)
    status: EntityStatus = EntityStatus.active


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    short_name: str | None = Field(default=None, max_length=30)
    department: str | None = Field(default=None, max_length=100)
    status: EntityStatus | None = None


class SubjectOut(SubjectBase, TimestampedSchema):
    id: int


class PeriodBase(BaseModel):
    period_number: int = Field(ge=0, le=20)
    start_time: time
    end_time: time
    applicable_day_type: PeriodDayType
    is_active: bool = True

    @field_validator("end_time")
    @classmethod
    def validate_end_after_start(cls, value: time, info):
        start_time = info.data.get("start_time")
        if start_time and value <= start_time:
            raise ValueError("end_time must be later than start_time")
        return value


class PeriodCreate(PeriodBase):
    pass


class PeriodUpdate(BaseModel):
    period_number: int | None = Field(default=None, ge=0, le=20)
    start_time: time | None = None
    end_time: time | None = None
    applicable_day_type: PeriodDayType | None = None
    is_active: bool | None = None


class PeriodOut(PeriodBase):
    id: int


class TimetableBase(BaseModel):
    day: DayOfWeek
    period_id: int
    class_id: int
    subject_id: int
    teacher_id: int | None = None   # None for Assembly periods
    room: str | None = Field(default=None, max_length=80)
    notes: str | None = None
    is_active: bool = True


class TimetableCreate(TimetableBase):
    pass


class TimetableUpdate(BaseModel):
    day: DayOfWeek | None = None
    period_id: int | None = None
    class_id: int | None = None
    subject_id: int | None = None
    teacher_id: int | None = None
    room: str | None = Field(default=None, max_length=80)
    notes: str | None = None
    is_active: bool | None = None


class TimetableOut(TimetableBase, TimestampedSchema):
    id: int


class TeacherAvailabilityBase(BaseModel):
    teacher_id: int
    day: DayOfWeek
    period_id: int
    is_available: bool
    notes: str | None = None


class TeacherAvailabilityCreate(TeacherAvailabilityBase):
    pass


class TeacherAvailabilityUpdate(BaseModel):
    is_available: bool | None = None
    notes: str | None = None


class TeacherAvailabilityOut(TeacherAvailabilityBase):
    id: int


class AbsenceCreate(BaseModel):
    teacher_id: int
    date: date
    reason: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class AbsenceOut(ORMBase):
    id: int
    teacher_id: int
    date: date
    reason: str | None
    status: AbsenceStatus
    notes: str | None


class SubstitutionAssignRequest(BaseModel):
    absence_id: int
    timetable_id: int
    substitute_teacher_id: int
    notes: str | None = None


class SubstitutionOut(ORMBase):
    id: int
    absence_id: int
    timetable_id: int
    original_teacher_id: int
    substitute_teacher_id: int | None
    date: date
    period_id: int
    class_id: int
    subject_id: int
    status: SubstitutionStatus
    notes: str | None


class RecommendationReason(BaseModel):
    teacher_id: int
    teacher_name: str
    score: int
    reasons: list[str]


class AffectedPeriod(BaseModel):
    timetable_id: int
    day: DayOfWeek
    period_id: int
    class_id: int
    subject_id: int
    teacher_id: int


class AuditLogOut(BaseModel):
    id: int
    user: str
    action: str
    entity: str
    entity_id: str
    description: str | None
