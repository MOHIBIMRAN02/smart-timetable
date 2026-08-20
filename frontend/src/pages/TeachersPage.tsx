import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { Plus, Edit2, Trash2, Loader } from "lucide-react";
import * as api from "../utils/api";
import { Teacher } from "../types";
import { getStatusColor } from "../utils/helpers";

const teacherSchema = z.object({
  name: z.string().min(2),
  employee_code: z.string().min(2),
  email: z.string().email().optional().or(z.literal("")),
  phone: z.string().optional(),
  designation: z.string().optional(),
  department: z.string().optional(),
  status: z.enum(["active", "inactive"]),
});

type TeacherFormData = z.infer<typeof teacherSchema>;

export default function TeachersPage() {
  const queryClient = useQueryClient();
  const [isOpen, setIsOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);

  const { data: teachers = [], isLoading } = useQuery({
    queryKey: ["teachers"],
    queryFn: api.getTeachers,
  });

  const form = useForm<TeacherFormData>({
    resolver: zodResolver(teacherSchema),
    defaultValues: { status: "active" },
  });

  const createMutation = useMutation({
    mutationFn: api.createTeacher,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["teachers"] });
      toast.success("Teacher created successfully");
      setIsOpen(false);
      form.reset();
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail?.message || "Failed to create teacher");
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => api.updateTeacher(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["teachers"] });
      toast.success("Teacher updated successfully");
      setIsOpen(false);
      setEditingId(null);
      form.reset();
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail?.message || "Failed to update teacher");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: api.deleteTeacher,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["teachers"] });
      toast.success("Teacher deleted successfully");
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail?.message || "Failed to delete teacher");
    },
  });

  const onSubmit = (data: TeacherFormData) => {
    if (editingId) {
      updateMutation.mutate({ id: editingId, data });
    } else {
      createMutation.mutate(data);
    }
  };

  const handleEdit = (teacher: Teacher) => {
    setEditingId(teacher.id);
    form.reset(teacher);
    setIsOpen(true);
  };

  const handleNew = () => {
    setEditingId(null);
    form.reset({ status: "active" });
    setIsOpen(true);
  };

  if (isLoading) {
    return <div className="flex items-center justify-center h-96"><Loader className="animate-spin" /></div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="page-title">Teachers</h1>
          <p className="text-slate-600 mt-1">Manage teachers and staff</p>
        </div>
        <button className="btn-primary flex items-center gap-2" onClick={handleNew}>
          <Plus size={16} /> Add Teacher
        </button>
      </div>

      {/* Modal */}
      {isOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="card w-full max-w-md">
            <h2 className="font-semibold text-lg mb-4">{editingId ? "Edit Teacher" : "Add Teacher"}</h2>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="text-sm font-medium">Name *</label>
                <input className="input" {...form.register("name")} />
                {form.formState.errors.name && <p className="text-red-600 text-xs mt-1">{form.formState.errors.name.message}</p>}
              </div>

              <div>
                <label className="text-sm font-medium">Employee Code *</label>
                <input className="input" {...form.register("employee_code")} />
                {form.formState.errors.employee_code && <p className="text-red-600 text-xs mt-1">{form.formState.errors.employee_code.message}</p>}
              </div>

              <div>
                <label className="text-sm font-medium">Email</label>
                <input type="email" className="input" {...form.register("email")} />
              </div>

              <div>
                <label className="text-sm font-medium">Phone</label>
                <input className="input" {...form.register("phone")} />
              </div>

              <div>
                <label className="text-sm font-medium">Designation</label>
                <input className="input" {...form.register("designation")} />
              </div>

              <div>
                <label className="text-sm font-medium">Department</label>
                <input className="input" {...form.register("department")} />
              </div>

              <div>
                <label className="text-sm font-medium">Status</label>
                <select className="input" {...form.register("status")}>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>

              <div className="flex gap-2 pt-4">
                <button type="button" className="flex-1 px-4 py-2 rounded-md border border-slate-300 text-slate-900" onClick={() => setIsOpen(false)}>
                  Cancel
                </button>
                <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="flex-1 btn-primary">
                  {createMutation.isPending || updateMutation.isPending ? "Saving..." : "Save"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Table */}
      <div className="card overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-200">
              <th className="text-left py-3 px-4">Name</th>
              <th className="text-left py-3 px-4">Code</th>
              <th className="text-left py-3 px-4">Department</th>
              <th className="text-left py-3 px-4">Email</th>
              <th className="text-left py-3 px-4">Status</th>
              <th className="text-left py-3 px-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {teachers.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-4 text-slate-500">
                  No teachers found
                </td>
              </tr>
            ) : (
              teachers.map((teacher) => (
                <tr key={teacher.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="py-3 px-4 font-medium">{teacher.name}</td>
                  <td className="py-3 px-4">{teacher.employee_code}</td>
                  <td className="py-3 px-4">{teacher.department || "-"}</td>
                  <td className="py-3 px-4">{teacher.email || "-"}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(teacher.status)}`}>
                      {teacher.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="py-3 px-4 flex gap-2">
                    <button onClick={() => handleEdit(teacher)} className="text-blue-600 hover:text-blue-800">
                      <Edit2 size={16} />
                    </button>
                    <button onClick={() => deleteMutation.mutate(teacher.id)} className="text-red-600 hover:text-red-800">
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
