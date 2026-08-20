import { Period, Timetable, Teacher, ClassRoom, Subject } from "../types";

export const DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"];

export const DAY_LABELS: Record<string, string> = {
  monday: "Monday",
  tuesday: "Tuesday",
  wednesday: "Wednesday",
  thursday: "Thursday",
  friday: "Friday",
};

export function formatTime(time: string): string {
  if (!time) return "";
  const [h, m] = time.split(":");
  const hour = parseInt(h);
  const min = m;
  const ampm = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 || 12;
  return `${displayHour}:${min} ${ampm}`;
}

export function formatDate(date: string): string {
  if (!date) return "";
  return new Date(date).toLocaleDateString("en-US", {
    weekday: "short",
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function getDayOfWeek(date: string): string {
  const d = new Date(date);
  const dayIndex = d.getDay();
  const mapping: Record<number, string> = {
    0: "sunday",
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
  };
  return mapping[dayIndex] || "monday";
}

export function buildTimetableMatrix(
  timetable: Timetable[],
  periods: Period[],
  teachers?: Record<number, Teacher>,
  classes?: Record<number, ClassRoom>,
  subjects?: Record<number, Subject>
) {
  const matrix: Record<string, Record<number, any>> = {};

  DAYS.forEach((day) => {
    matrix[day] = {};
    periods.forEach((p) => {
      matrix[day][p.period_number] = null;
    });
  });

  timetable.forEach((entry) => {
    if (matrix[entry.day]) {
      matrix[entry.day][periods.find((p) => p.id === entry.period_id)?.period_number || 0] = {
        ...entry,
        teacher_name: teachers?.[entry.teacher_id]?.name,
        class_name: classes?.[entry.class_id]?.name,
        subject_name: subjects?.[entry.subject_id]?.name,
      };
    }
  });

  return matrix;
}

export function exportToCSV(filename: string, data: any[]) {
  if (!data.length) return;

  const headers = Object.keys(data[0]);
  const csv = [headers.join(","), ...data.map((row) => headers.map((h) => JSON.stringify(row[h])).join(","))].join("\n");

  const blob = new Blob([csv], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
}

export function printHTML(html: string) {
  const printWindow = window.open("", "", "height=600,width=800");
  if (printWindow) {
    printWindow.document.write(html);
    printWindow.document.close();
    printWindow.print();
  }
}

export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    active: "bg-green-100 text-green-800",
    inactive: "bg-slate-100 text-slate-800",
    assigned: "bg-blue-100 text-blue-800",
    pending: "bg-yellow-100 text-yellow-800",
    cancelled: "bg-red-100 text-red-800",
    absent: "bg-red-100 text-red-800",
  };
  return colors[status] || "bg-slate-100 text-slate-800";
}
