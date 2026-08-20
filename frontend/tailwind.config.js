/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef4ff",
          100: "#d7e5ff",
          500: "#1e5eff",
          700: "#1241b8"
        }
      },
      boxShadow: {
        soft: "0 10px 30px rgba(17, 50, 112, 0.08)"
      }
    },
  },
  plugins: [],
};
