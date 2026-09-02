# tests/test_api.py
"""
Automated Integration Tests for FastAPI API Endpoints.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from api.main import app
from db.storage import init_database_sync


@pytest.fixture(autouse=True)
def setup_db():
    init_database_sync()


@pytest.mark.asyncio
async def test_auth_and_session_lifecycle():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Register
        reg_res = await client.post("/api/v1/auth/register", json={
            "username": "tester_agent",
            "password": "secret_password_123",
            "email": "tester@example.com"
        })
        assert reg_res.status_code in [200, 400]
        
        # 2. Login
        login_res = await client.post("/api/v1/auth/login", json={
            "username": "tester_agent",
            "password": "secret_password_123"
        })
        assert login_res.status_code == 200
        token_data = login_res.json()
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Get /me
        me_res = await client.get("/api/v1/auth/me", headers=headers)
        assert me_res.status_code == 200
        assert me_res.json()["username"] == "tester_agent"

        # 4. Session Start
        sess_res = await client.post("/api/v1/session/start", headers=headers)
        assert sess_res.status_code == 200
        assert "current_node" in sess_res.json()

        # 5. Onboarding Submit
        onb_res = await client.post("/api/v1/onboarding/submit", headers=headers, json={
            "name": "Alex Tester",
            "prior_experience": "intermediate",
            "prefers_examples": True,
            "prefers_steps": True,
            "prefers_detailed": True,
            "preferred_quiz_style": "mixed",
            "session_time_budget": 30
        })
        assert onb_res.status_code == 200
        assert onb_res.json()["profile"]["onboarding_done"] is True

        # 6. Fetch Lesson
        lesson_res = await client.get("/api/v1/lesson/current", headers=headers)
        assert lesson_res.status_code == 200
        assert "lesson_markdown" in lesson_res.json()

        # 7. Fetch Progress Tree
        tree_res = await client.get("/api/v1/progress/tree", headers=headers)
        assert tree_res.status_code == 200
        assert tree_res.json()["total_nodes"] == 36

        # 8. Fetch Quiz & Request 3 Hints (ensure all 3 hints are unique)
        quiz_res = await client.get("/api/v1/quiz/current?node_id=node_04", headers=headers)
        assert quiz_res.status_code == 200
        quiz_data = quiz_res.json()
        assert "passing_threshold" in quiz_data
        assert quiz_data["passing_threshold"] > 0

        hints = []
        # Request Hint for Q1 (MCQ), Q2 (Writing), Q3 (Diagnosis)
        for q_idx, i in zip([1, 2, 3], range(1, 4)):
            hint_res = await client.post("/api/v1/quiz/hint", headers=headers, json={"node_id": "node_04", "question_idx": q_idx})
            assert hint_res.status_code == 200
            h_data = hint_res.json()
            assert "hint" in h_data
            assert h_data["hints_used"] == i
            hints.append(h_data["hint"].strip())

        # Assert all 3 hints are unique and non-empty
        assert len(hints) == 3
        assert len(set(hints)) == 3, f"Duplicate hints detected across questions: {hints}"


