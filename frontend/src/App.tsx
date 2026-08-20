import { Navigate, Route, Routes } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";
import AbsencesPage from "./pages/AbsencesPage";
import DashboardPage from "./pages/DashboardPage";
import ReportsPage from "./pages/ReportsPage";
import {
  AbsenceDetailPage,
  ClassDetailPage,
  ClassesPage,
  PeriodsPage,
  ReportsDailyPage,
  ReportsSubstitutionPage,
  SettingsPage,
  SubjectDetailPage,
  SubjectsPage,
  SubstitutionDetailPage,
  TeacherDetailPage,
  TimetableClassPage,
  TimetableTeacherPage,
} from "./pages/SimplePages";
import SubstitutionsPage from "./pages/SubstitutionsPage";
import TeachersPage from "./pages/TeachersPage";
import TimetablePage from "./pages/TimetablePage";

function AppShell() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/timetable" element={<TimetablePage />} />
        <Route path="/timetable/class/:id" element={<TimetableClassPage />} />
        <Route path="/timetable/teacher/:id" element={<TimetableTeacherPage />} />
        <Route path="/teachers" element={<TeachersPage />} />
        <Route path="/teachers/:id" element={<TeacherDetailPage />} />
        <Route path="/classes" element={<ClassesPage />} />
        <Route path="/classes/:id" element={<ClassDetailPage />} />
        <Route path="/subjects" element={<SubjectsPage />} />
        <Route path="/subjects/:id" element={<SubjectDetailPage />} />
        <Route path="/periods" element={<PeriodsPage />} />
        <Route path="/absences" element={<AbsencesPage />} />
        <Route path="/absences/:id" element={<AbsenceDetailPage />} />
        <Route path="/substitutions" element={<SubstitutionsPage />} />
        <Route path="/substitutions/:id" element={<SubstitutionDetailPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/reports/daily" element={<ReportsDailyPage />} />
        <Route path="/reports/teacher" element={<ReportsPage />} />
        <Route path="/reports/class" element={<ReportsPage />} />
        <Route path="/reports/substitutions" element={<ReportsSubstitutionPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </MainLayout>
  );
}

export default function App() {
  return <AppShell />;
}
