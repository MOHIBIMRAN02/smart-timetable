export interface User {
  id: number;
  name: string;
  username: string;
  role: "admin" | "scheduler";
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Teacher {
  id: number;
  name: string;
  employee_code: string;
  email?: string;
  phone?: string;
  designation?: string;
  department?: string;
  status: "active" | "inactive";
  created_at: string;
  updated_at: string;
}

export interface ClassRoom {
  id: number;
  name: string;
  section?: string;
  program?: string;
  class_code: string;
  status: "active" | "inactive";
  created_at: string;
  updated_at: string;
}

export interface Subject {
  id: number;
  name: string;
  short_name?: string;
  department?: string;
  status: "active" | "inactive";
  created_at: string;
  updated_at: string;
}

export interface Period {
  id: number;
  period_number: number;
  start_time: string;
  end_time: string;
  applicable_day_type: "mon_thu" | "friday";
  is_active: boolean;
}

export interface Timetable {
  id: number;
  day: "monday" | "tuesday" | "wednesday" | "thursday" | "friday";
  period_id: number;
  class_id: number;
  subject_id: number;
  teacher_id: number;
  room?: string;
  notes?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface TeacherAbsence {
  id: number;
  teacher_id: number;
  date: string;
  reason?: string;
  status: "absent" | "cancelled";
  notes?: string;
  created_at: string;
}

export interface Substitution {
  id: number;
  absence_id: number;
  timetable_id: number;
  original_teacher_id: number;
  substitute_teacher_id?: number;
  date: string;
  period_id: number;
  class_id: number;
  subject_id: number;
  status: "pending" | "assigned" | "cancelled";
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface TeacherAvailability {
  id: number;
  teacher_id: number;
  day: "monday" | "tuesday" | "wednesday" | "thursday" | "friday";
  period_id: number;
  is_available: boolean;
  notes?: string;
}

export interface AffectedPeriod {
  timetable_id: number;
  day: "monday" | "tuesday" | "wednesday" | "thursday" | "friday";
  period_id: number;
  class_id: number;
  subject_id: number;
  teacher_id: number;
}

export interface RecommendationReason {
  teacher_id: number;
  teacher_name: string;
  score: number;
  reasons: string[];
}

export interface Setting {
  id: number;
  school_name: string;
  school_logo?: string;
  academic_session?: string;
  working_days: string;
  default_dashboard_view: string;
}

export interface AuditLog {
  id: number;
  user: string;
  action: string;
  entity: string;
  entity_id: string;
  description?: string;
  timestamp: string;
}
