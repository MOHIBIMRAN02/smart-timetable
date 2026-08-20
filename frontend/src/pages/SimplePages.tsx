import ModulePage from "./ModulePage";

export const ClassesPage = () => <ModulePage title="Classes" subtitle="Manage school classes and sections." />;
export const SubjectsPage = () => <ModulePage title="Subjects" subtitle="Manage subjects and departments." />;
export const SubjectDetailPage = () => <ModulePage title="Subject Details" subtitle="Subject profile and timetable entries." />;
export const PeriodsPage = () => <ModulePage title="Periods" subtitle="Configure period timings from database." />;
export const SettingsPage = () => <ModulePage title="Settings" subtitle="School configuration and defaults." />;

export const TimetableClassPage = () => <ModulePage title="Class Timetable" subtitle="Class weekly schedule view." />;
export const TimetableTeacherPage = () => <ModulePage title="Teacher Timetable" subtitle="Teacher weekly schedule view." />;
export const TeacherDetailPage = () => <ModulePage title="Teacher Details" subtitle="Teacher profile and schedule." />;
export const ClassDetailPage = () => <ModulePage title="Class Details" subtitle="Class profile and timetable." />;
export const AbsenceDetailPage = () => <ModulePage title="Absence Details" subtitle="Affected periods and substitutions." />;
export const SubstitutionDetailPage = () => <ModulePage title="Substitution Details" subtitle="Substitution assignment details." />;
export const ReportsDailyPage = () => <ModulePage title="Daily Report" subtitle="Printable daily schedule." />;
export const ReportsSubstitutionPage = () => <ModulePage title="Substitution Report" subtitle="Substitution analytics." />;
