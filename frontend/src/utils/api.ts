import { api } from "../services/api";
import * as types from "../types";

// Teachers
export async function getTeachers() {
  const res = await api.get<types.Teacher[]>("/api/teachers");
  return res.data;
}

export async function getTeacher(id: number) {
  const res = await api.get<types.Teacher>(`/api/teachers/${id}`);
  return res.data;
}

export async function createTeacher(payload: any) {
  const res = await api.post<types.Teacher>("/api/teachers", payload);
  return res.data;
}

export async function updateTeacher(id: number, payload: any) {
  const res = await api.put<types.Teacher>(`/api/teachers/${id}`, payload);
  return res.data;
}

export async function deleteTeacher(id: number) {
  await api.delete(`/api/teachers/${id}`);
}

// Classes
export async function getClasses() {
  const res = await api.get<types.ClassRoom[]>("/api/classes");
  return res.data;
}

export async function getClass(id: number) {
  const res = await api.get<types.ClassRoom>(`/api/classes/${id}`);
  return res.data;
}

export async function createClass(payload: any) {
  const res = await api.post<types.ClassRoom>("/api/classes", payload);
  return res.data;
}

export async function updateClass(id: number, payload: any) {
  const res = await api.put<types.ClassRoom>(`/api/classes/${id}`, payload);
  return res.data;
}

export async function deleteClass(id: number) {
  await api.delete(`/api/classes/${id}`);
}

// Subjects
export async function getSubjects() {
  const res = await api.get<types.Subject[]>("/api/subjects");
  return res.data;
}

export async function getSubject(id: number) {
  const res = await api.get<types.Subject>(`/api/subjects/${id}`);
  return res.data;
}

export async function createSubject(payload: any) {
  const res = await api.post<types.Subject>("/api/subjects", payload);
  return res.data;
}

export async function updateSubject(id: number, payload: any) {
  const res = await api.put<types.Subject>(`/api/subjects/${id}`, payload);
  return res.data;
}

export async function deleteSubject(id: number) {
  await api.delete(`/api/subjects/${id}`);
}

// Periods
export async function getPeriods() {
  const res = await api.get<types.Period[]>("/api/periods");
  return res.data;
}

export async function getPeriod(id: number) {
  const res = await api.get<types.Period>(`/api/periods/${id}`);
  return res.data;
}

export async function createPeriod(payload: any) {
  const res = await api.post<types.Period>("/api/periods", payload);
  return res.data;
}

export async function updatePeriod(id: number, payload: any) {
  const res = await api.put<types.Period>(`/api/periods/${id}`, payload);
  return res.data;
}

export async function deletePeriod(id: number) {
  await api.delete(`/api/periods/${id}`);
}

// Timetable
export async function getTimetable(params?: any) {
  const res = await api.get<types.Timetable[]>("/api/timetable", { params });
  return res.data;
}

export async function getTimetableEntry(id: number) {
  const res = await api.get<types.Timetable>(`/api/timetable/${id}`);
  return res.data;
}

export async function createTimetable(payload: any) {
  const res = await api.post<types.Timetable>("/api/timetable", payload);
  return res.data;
}

export async function updateTimetable(id: number, payload: any) {
  const res = await api.put<types.Timetable>(`/api/timetable/${id}`, payload);
  return res.data;
}

export async function deleteTimetable(id: number) {
  await api.delete(`/api/timetable/${id}`);
}

// Absences
export async function getAbsences() {
  const res = await api.get<types.TeacherAbsence[]>("/api/absences");
  return res.data;
}

export async function markAbsent(payload: any) {
  const res = await api.post("/api/absences", payload);
  return res.data;
}

// Substitutions
export async function getSubstitutions(params?: any) {
  const res = await api.get<types.Substitution[]>("/api/substitutions", { params });
  return res.data;
}

export async function getSubstitution(id: number) {
  const res = await api.get<types.Substitution>(`/api/substitutions/${id}`);
  return res.data;
}

export async function getRecommendations(substitutionId: number) {
  const res = await api.get<{ recommendations: types.RecommendationReason[] }>(`/api/substitutions/recommend/${substitutionId}`);
  return res.data.recommendations;
}

export async function assignSubstitute(payload: any) {
  const res = await api.post<types.Substitution>("/api/substitutions/assign", payload);
  return res.data;
}

export async function cancelSubstitution(id: number) {
  const res = await api.put<types.Substitution>(`/api/substitutions/${id}/cancel`);
  return res.data;
}

// Reports
export async function getTeacherSchedule(teacherId: number) {
  const res = await api.get(`/api/reports/teacher/${teacherId}`);
  return res.data;
}

export async function getClassSchedule(classId: number) {
  const res = await api.get(`/api/reports/class/${classId}`);
  return res.data;
}

export async function getDailyTimetable(day: string) {
  const res = await api.get("/api/reports/daily", { params: { day } });
  return res.data;
}

export async function getAbsenceReport(params?: any) {
  const res = await api.get("/api/reports/absences", { params });
  return res.data;
}

export async function getSubstitutionReport(params?: any) {
  const res = await api.get("/api/reports/substitutions", { params });
  return res.data;
}

export async function getTeacherWorkload() {
  const res = await api.get("/api/reports/workload");
  return res.data;
}

export async function getDailySubstitutionSheet(date: string) {
  const res = await api.get("/api/reports/daily-substitution-sheet", { params: { date } });
  return res.data;
}

// Dashboard
export async function getDashboard() {
  const res = await api.get("/api/dashboard");
  return res.data;
}

// Settings
export async function getSettings() {
  const res = await api.get("/api/settings");
  return res.data;
}

export async function updateSettings(payload: any) {
  const res = await api.put("/api/settings", payload);
  return res.data;
}

// Search
export async function search(q: string) {
  const res = await api.get("/api/search", { params: { q } });
  return res.data;
}

// Availability
export async function getAvailability() {
  const res = await api.get<types.TeacherAvailability[]>("/api/availability");
  return res.data;
}

export async function createAvailability(payload: any) {
  const res = await api.post<types.TeacherAvailability>("/api/availability", payload);
  return res.data;
}

export async function updateAvailability(id: number, payload: any) {
  const res = await api.put<types.TeacherAvailability>(`/api/availability/${id}`, payload);
  return res.data;
}

export async function deleteAvailability(id: number) {
  await api.delete(`/api/availability/${id}`);
}

// Audit
export async function getAuditLogs() {
  const res = await api.get("/api/audit");
  return res.data;
}
