import { LayoutDashboard, CalendarDays, Users, School, BookOpen, Clock3, UserX, RefreshCcw, BarChart3, Settings } from "lucide-react";
import { NavLink } from "react-router-dom";

const items = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/timetable", label: "Timetable", icon: CalendarDays },
  { to: "/teachers", label: "Teachers", icon: Users },
  { to: "/classes", label: "Classes", icon: School },
  { to: "/subjects", label: "Subjects", icon: BookOpen },
  { to: "/periods", label: "Periods", icon: Clock3 },
  { to: "/absences", label: "Absences", icon: UserX },
  { to: "/substitutions", label: "Substitutions", icon: RefreshCcw },
  { to: "/reports", label: "Reports", icon: BarChart3 },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="w-72 bg-slate-950 text-white p-5 hidden md:block">
      <h1 className="text-xl font-semibold tracking-wide">Smart Timetable</h1>
      <p className="text-slate-400 text-sm mt-1">Admin Control Panel</p>
      <nav className="mt-8 space-y-2">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-lg transition ${isActive ? "bg-brand-500" : "hover:bg-slate-800"}`
              }
            >
              <Icon size={16} />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}
