import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { Plus, AlertCircle } from "lucide-react";
import * as api from "../utils/api";
import { formatDate, getStatusColor } from "../utils/helpers";

const absenceSchema = z.object({
  teacher_id: z.number({ coerce: true }),
  date: z.string().date(),
  reason: z.string().optional(),
  notes: z.string().optional(),
});

type AbsenceFormData = z.infer<typeof absenceSchema>;

export default function AbsencesPage() {
  const queryClient = useQueryClient();
  const [isOpen, setIsOpen] = useState(false);
  const [selectedAbsence, setSelectedAbsence] = useState<any | null>(null);

  const { data: absences = [] } = useQuery({
    queryKey: ["absences"],
    queryFn: api.getAbsences,
  });

  const { data: teachers = [] } = useQuery({
    queryKey: ["teachers"],
    queryFn: api.getTeachers,
  });

  const form = useForm<AbsenceFormData>({
    resolver: zodResolver(absenceSchema),
  });

  const markAbsentMutation = useMutation({
    mutationFn: api.markAbsent,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["absences"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      queryClient.invalidateQueries({ queryKey: ["substitutions"] });
      toast.success(`Teacher marked absent. ${data.affected_periods?.length || 0} affected periods.`);
      setIsOpen(false);
      setSelectedAbsence(data);
      form.reset();
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail?.message || "Failed to mark absence");
    },
  });

  const onSubmit = (data: AbsenceFormData) => {
    markAbsentMutation.mutate(data);
  };

  const teacherMap = Object.fromEntries(teachers.map((t) => [t.id, t]));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="page-title">Teacher Absences</h1>
          <p className="text-slate-600 mt-1">Manage teacher absences and affected periods</p>
        </div>
        <button className="btn-primary flex items-center gap-2" onClick={() => setIsOpen(true)}>
          <Plus size={16} /> Mark Absent
        </button>
      </div>

      {/* Mark Absent Modal */}
      {isOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="card w-full max-w-md">
            <h2 className="font-semibold text-lg mb-4">Mark Teacher Absent</h2>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="text-sm font-medium">Teacher *</label>
                <select className="input" {...form.register("teacher_id")}>
                  <option value="">Select teacher</option>
                  {teachers.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.name}
                    </option>
                  ))}
                </select>
                {form.formState.errors.teacher_id && <p className="text-red-600 text-xs mt-1">{form.formState.errors.teacher_id.message}</p>}
              </div>

              <div>
                <label className="text-sm font-medium">Date *</label>
                <input type="date" className="input" {...form.register("date")} />
                {form.formState.errors.date && <p className="text-red-600 text-xs mt-1">{form.formState.errors.date.message}</p>}
              </div>

              <div>
                <label className="text-sm font-medium">Reason</label>
                <input className="input" placeholder="e.g., Medical leave" {...form.register("reason")} />
              </div>

              <div>
                <label className="text-sm font-medium">Notes</label>
                <textarea className="input" placeholder="Additional notes" {...form.register("notes")} rows={3} />
              </div>

              <div className="flex gap-2 pt-4">
                <button
                  type="button"
                  className="flex-1 px-4 py-2 rounded-md border border-slate-300 text-slate-900"
                  onClick={() => setIsOpen(false)}
                >
                  Cancel
                </button>
                <button type="submit" disabled={markAbsentMutation.isPending} className="flex-1 btn-primary">
                  {markAbsentMutation.isPending ? "Processing..." : "Mark Absent"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Affected Periods Alert */}
      {selectedAbsence && (
        <div className="card bg-blue-50 border border-blue-200">
          <div className="flex gap-3">
            <AlertCircle size={20} className="text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-900">Affected Periods</h3>
              <p className="text-sm text-blue-800 mt-1">
                {teacherMap[selectedAbsence.absence.teacher_id]?.name} has {selectedAbsence.affected_periods?.length || 0} classes on{" "}
                {formatDate(selectedAbsence.absence.date)}. Pending substitutions have been created.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Absence History */}
      <div className="card">
        <h3 className="font-semibold text-lg mb-4">Absence History</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200">
                <th className="text-left py-3 px-4">Teacher</th>
                <th className="text-left py-3 px-4">Date</th>
                <th className="text-left py-3 px-4">Reason</th>
                <th className="text-left py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {absences.length === 0 ? (
                <tr>
                  <td colSpan={4} className="text-center py-4 text-slate-500">
                    No absences recorded
                  </td>
                </tr>
              ) : (
                absences.map((absence) => (
                  <tr key={absence.id} className="border-b border-slate-100 hover:bg-slate-50">
                    <td className="py-3 px-4 font-medium">{teacherMap[absence.teacher_id]?.name}</td>
                    <td className="py-3 px-4">{formatDate(absence.date)}</td>
                    <td className="py-3 px-4">{absence.reason || "-"}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(absence.status)}`}>
                        {absence.status.toUpperCase()}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
