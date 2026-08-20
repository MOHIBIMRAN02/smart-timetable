import { Menu } from "lucide-react";
import { useState } from "react";

import Sidebar from "../components/Sidebar";

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-100 flex">
      <Sidebar />
      <div className="flex-1">
        <header className="bg-white border-b border-slate-200 px-4 py-3 flex items-center justify-between">
          <button className="md:hidden" onClick={() => setOpen((value) => !value)}>
            <Menu />
          </button>
          <div>
            <p className="text-sm text-slate-500">Welcome</p>
            <h2 className="font-semibold">Smart Timetable System</h2>
          </div>
          <div></div>
        </header>

        {open && (
          <div className="md:hidden bg-slate-950 text-white px-4 py-4 space-y-2">
            <p className="text-sm text-slate-400">Menu available on desktop sidebar.</p>
          </div>
        )}

        <main className="p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
