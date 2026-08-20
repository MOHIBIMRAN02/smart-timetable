from __future__ import annotations

import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from sqlalchemy import func, select
from app.database import Base, SessionLocal, engine, get_db
from app.models import Teacher
from app.routers import absences, auth, audit, availability, classes, dashboard, periods, reports, search, settings, subjects, substitutions, teachers, timetable
from app.seed import (
    seed_availability,
    seed_classes,
    seed_demo_absence_and_pending_substitutions,
    seed_periods,
    seed_settings,
    seed_subjects,
    seed_teachers,
    seed_timetable,
    seed_users,
)


def auto_seed_if_empty():
    with SessionLocal() as db:
        teacher_count = db.scalar(select(func.count(Teacher.id)))
        if not teacher_count:
            try:
                seed_users(db)
                seed_teachers(db)
                seed_classes(db)
                seed_subjects(db)
                seed_periods(db)
                seed_settings(db)
                db.commit()

                seed_timetable(db)
                seed_availability(db)
                db.commit()

                seed_demo_absence_and_pending_substitutions(db)
                db.commit()
                print("[INIT] Database was empty. Auto-seeded initial data successfully.")
            except Exception as exc:
                db.rollback()
                print(f"[INIT] Auto-seed warning: {exc}")


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    auto_seed_if_empty()
    yield


app = FastAPI(
    title="Smart Timetable and Substitute Management API",
    description="School timetable, absences and smart substitute assignment backend",
    version="1.0.0",
    lifespan=lifespan,
)

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

if "*" in allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error_code": "INTERNAL_SERVER_ERROR",
            "detail": str(exc.__class__.__name__),
        },
    )


app.include_router(auth.router)
app.include_router(teachers.router)
app.include_router(classes.router)
app.include_router(subjects.router)
app.include_router(periods.router)
app.include_router(timetable.router)
app.include_router(absences.router)
app.include_router(substitutions.router)
app.include_router(availability.router)
app.include_router(reports.router)
app.include_router(dashboard.router)
app.include_router(search.router)
app.include_router(settings.router)
app.include_router(audit.router)


@app.get("/health", summary="Render health check")
def render_health(db: Session = Depends(get_db)):
    """Used by Render to keep the service alive. Must return 200."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
    return {
        "status": "ok",
        "db": db_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/api/health", summary="Health check")
def health_check():
    return {"success": True, "message": "API is running"}
