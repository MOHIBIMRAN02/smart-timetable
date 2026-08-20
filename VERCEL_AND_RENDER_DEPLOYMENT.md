# 🌐 Deployment Guide: Vercel (Frontend) + Render (Backend)

This guide walks you through deploying your **Frontend on Vercel** and **Backend on Render**.

---

## 🟢 Step 1: Deploy Backend to Render

1. Log into your **[Render Dashboard](https://dashboard.render.com/)**.
2. Click **New +** -> **Web Service**.
3. Connect your GitHub/GitLab repository.
4. Fill in the deployment details:
   - **Name**: `smart-timetable-backend` (or any name you choose)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`
5. Add **Environment Variables**:
   - `ALLOWED_ORIGINS` = `*` (or your Vercel URL e.g. `https://smart-timetable.vercel.app`)
   - `DATABASE_URL` = `sqlite:///./smart_timetable.db`
6. Click **Create Web Service**.

Once deployed, copy your backend URL (e.g. `https://smart-timetable-backend.onrender.com`).

> 💡 **Note**: The backend automatically populates all default timetable, teacher, class, and subject data on its first startup!

---

## ⚡ Step 2: Deploy Frontend to Vercel

1. Log into your **[Vercel Dashboard](https://vercel.com/dashboard)**.
2. Click **Add New...** -> **Project**.
3. Import your GitHub/GitLab repository.
4. Configure Project Settings:
   - **Root Directory**: Select `frontend` (or leave as `./` — `vercel.json` handles both!)
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist` (or `frontend/dist` if root directory is `./`)
5. Add **Environment Variables**:
   - `VITE_API_BASE_URL` = `https://smart-timetable-backend.onrender.com` *(Use your exact Render backend URL from Step 1)*
6. Click **Deploy**.

Vercel will build and launch your frontend. Once complete, open your Vercel deployment URL—your app is live and fully working!

---

## 📄 File Summary of Created Deployment Files

| File | Purpose |
| :--- | :--- |
| [`frontend/.env.example`](file:///c:/Users/mohib/Desktop/Smart%20Timetable/frontend/.env.example) | Template env var `VITE_API_BASE_URL` for Vercel |
| [`backend/.env.example`](file:///c:/Users/mohib/Desktop/Smart%20Timetable/backend/.env.example) | Template env vars (`ALLOWED_ORIGINS`, `DATABASE_URL`, `SECRET_KEY`) for Render |
| [`vercel.json`](file:///c:/Users/mohib/Desktop/Smart%20Timetable/vercel.json) | Vercel root build & SPA rewrite routing configuration |
| [`frontend/vercel.json`](file:///c:/Users/mohib/Desktop/Smart%20Timetable/frontend/vercel.json) | Vercel subfolder SPA rewrite routing configuration |
| [`Procfile`](file:///c:/Users/mohib/Desktop/Smart%20Timetable/Procfile) | Render web service startup command |
| [`render.yaml`](file:///c:/Users/mohib/Desktop/Smart%20Timetable/render.yaml) | Render Blueprint configuration |
