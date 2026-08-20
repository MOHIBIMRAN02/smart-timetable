import { useMemo } from "react";

export function useAuth() {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");
  const name = localStorage.getItem("name");

  return useMemo(
    () => ({
      isAuthenticated: Boolean(token),
      token,
      role,
      name,
      logout: () => {
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        localStorage.removeItem("name");
      },
    }),
    [token, role, name]
  );
}
