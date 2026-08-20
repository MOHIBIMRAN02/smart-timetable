from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    scheduler = "scheduler"


class EntityStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class DayOfWeek(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"


class PeriodDayType(str, Enum):
    mon_thu = "mon_thu"
    friday = "friday"


class AbsenceStatus(str, Enum):
    absent = "absent"
    cancelled = "cancelled"


class SubstitutionStatus(str, Enum):
    pending = "pending"
    assigned = "assigned"
    cancelled = "cancelled"
