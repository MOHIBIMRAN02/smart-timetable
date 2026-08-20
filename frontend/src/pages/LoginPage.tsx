import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { api } from "../services/api";

const loginSchema = z.object({
  username: z.string().min(3),
  password: z.string().min(6),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const navigate = useNavigate();
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (payload: LoginForm) => {
    try {
      const response = await api.post("/api/auth/login", payload);
      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("role", response.data.role);
      localStorage.setItem("name", response.data.name);
      toast.success("Logged in successfully");
      navigate("/dashboard");
    } catch {
      toast.error("Invalid credentials");
    }
  };

  return (
    <div className="min-h-screen grid place-items-center p-4">
      <form className="card w-full max-w-md space-y-4" onSubmit={handleSubmit(onSubmit)}>
        <h1 className="text-2xl font-semibold">Smart Timetable Login</h1>
        <p className="text-slate-600">Use admin/admin123 or scheduler/scheduler123</p>

        <div>
          <label className="text-sm">Username</label>
          <input className="input" {...register("username")} />
          {errors.username && <p className="text-red-600 text-sm">{errors.username.message}</p>}
        </div>

        <div>
          <label className="text-sm">Password</label>
          <input type="password" className="input" {...register("password")} />
          {errors.password && <p className="text-red-600 text-sm">{errors.password.message}</p>}
        </div>

        <button disabled={isSubmitting} className="btn-primary w-full" type="submit">
          {isSubmitting ? "Signing in..." : "Login"}
        </button>
      </form>
    </div>
  );
}
