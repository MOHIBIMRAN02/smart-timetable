from __future__ import annotations

from datetime import date

from fastapi.testclient import TestClient

from app.main import app
from app.seed import main as seed_main


client = TestClient(app)


def auth_headers(username: str = "admin", password: str = "admin123"):
    response = client.post("/api/auth/login", json={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def setup_module():
    seed_main()


def test_teacher_crud():
    headers = auth_headers()

    create = client.post(
        "/api/teachers",
        headers=headers,
        json={"name": "Ms. Test", "employee_code": "T999", "department": "Science", "designation": "Teacher"},
    )
    assert create.status_code == 200

    teacher_id = create.json()["id"]

    update = client.put(
        f"/api/teachers/{teacher_id}",
        headers=headers,
        json={"department": "Math"},
    )
    assert update.status_code == 200
    assert update.json()["department"] == "Math"

    delete = client.delete(f"/api/teachers/{teacher_id}", headers=headers)
    assert delete.status_code == 200


def test_timetable_conflict_detection():
    headers = auth_headers()

    rows = client.get("/api/timetable?day=monday", headers=headers).json()
    sample = rows[0]

    conflict = client.post(
        "/api/timetable",
        headers=headers,
        json={
            "day": sample["day"],
            "period_id": sample["period_id"],
            "class_id": sample["class_id"],
            "subject_id": sample["subject_id"],
            "teacher_id": sample["teacher_id"],
            "room": "X",
            "is_active": True,
        },
    )
    assert conflict.status_code == 409


def test_absence_and_substitution_recommendation():
    headers = auth_headers()

    teachers = client.get("/api/teachers", headers=headers).json()
    arshia = next(item for item in teachers if item["name"] == "Ms. Arshia")

    absence = client.post(
        "/api/absences",
        headers=headers,
        json={
            "teacher_id": arshia["id"],
            "date": str(date.today()),
            "reason": "Test absence",
            "notes": "test",
        },
    )
    assert absence.status_code == 200

    substitutions = client.get("/api/substitutions", headers=headers).json()
    pending = next(item for item in substitutions if item["status"] == "pending")

    rec = client.get(f"/api/substitutions/recommend/{pending['id']}", headers=headers)
    assert rec.status_code == 200

    recs = rec.json()["recommendations"]
    if recs:
        assign = client.post(
            "/api/substitutions/assign",
            headers=headers,
            json={
                "absence_id": pending["absence_id"],
                "timetable_id": pending["timetable_id"],
                "substitute_teacher_id": recs[0]["teacher_id"],
            },
        )
        assert assign.status_code == 200
