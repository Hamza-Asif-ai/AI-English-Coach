import pytest
from fastapi.testclient import TestClient

from app import services
from app.main import app

from . import samples

CLIENT_ID = "test-client-12345"


@pytest.fixture()
def client():
    with TestClient(app) as test_client:  # runs lifespan -> creates the database
        yield test_client


@pytest.fixture()
def fake_ai(monkeypatch):
    """Replace the CrewAI call with canned replies."""
    calls = {"count": 0, "replies": None}

    def fake_run_crew(area, prompt):
        calls["count"] += 1
        replies = calls["replies"]
        if replies is not None:
            return replies.pop(0)
        return samples.as_json(samples.BY_AREA[area])

    monkeypatch.setattr(services, "run_crew", fake_run_crew)
    return calls


def test_root_and_health(client):
    assert client.get("/").json()["message"].startswith("AI English Coach")
    body = client.get("/api/health").json()
    assert body == {"status": "healthy", "llm_configured": False}


@pytest.mark.parametrize("area", ["Reading", "Writing", "Vocabulary", "Grammar"])
def test_generate_exercise_every_area(client, fake_ai, area):
    response = client.post(
        "/api/generate-exercise", json={"level": "Intermediate", "area": area}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["area"] == area and body["level"] == "Intermediate"
    assert body["session_id"]
    assert body["exercise"]


def test_generate_rejects_unknown_area_and_level(client):
    assert client.post("/api/generate-exercise", json={"area": "Cooking"}).status_code == 422
    assert client.post("/api/generate-exercise", json={"level": "Expert"}).status_code == 422


def test_missing_api_key_returns_clear_503(client):
    response = client.post("/api/generate-exercise", json={"area": "Grammar"})
    assert response.status_code == 503
    assert "GROQ_API_KEY" in response.json()["detail"]


def test_retries_after_invalid_reply(client, fake_ai):
    fake_ai["replies"] = ["this is not json", samples.as_json(samples.GRAMMAR)]
    response = client.post("/api/generate-exercise", json={"area": "Grammar"})
    assert response.status_code == 200
    assert fake_ai["count"] == 2


def test_gives_502_when_ai_keeps_failing(client, fake_ai):
    fake_ai["replies"] = ["bad", "still bad", "{}"]
    response = client.post("/api/generate-exercise", json={"area": "Reading"})
    assert response.status_code == 502
    assert "try again" in response.json()["detail"].lower()
    assert fake_ai["count"] == 3


def test_ai_exception_is_handled(client, monkeypatch):
    def boom(area, prompt):
        raise ConnectionError("network down")

    monkeypatch.setattr(services, "run_crew", boom)
    response = client.post("/api/generate-exercise", json={"area": "Vocabulary"})
    assert response.status_code == 502


def test_evaluate_writing(client, fake_ai):
    fake_ai["replies"] = [samples.as_json(samples.FEEDBACK)]
    response = client.post(
        "/api/evaluate-writing",
        json={
            "level": "Beginner",
            "topic": "My day",
            "instructions": "Write about your day.",
            "answer": "I go to school every day. I like it.",
        },
    )
    assert response.status_code == 200
    assert response.json()["feedback"]["score"] == 7


def test_evaluate_writing_validates_input(client):
    response = client.post(
        "/api/evaluate-writing", json={"topic": "x", "answer": "short"}
    )
    assert response.status_code == 422


def test_progress_save_and_stats(client):
    empty = client.get("/api/progress", params={"client_id": CLIENT_ID}).json()
    assert empty["total_practices"] == 0
    assert empty["recommendation"]["area"] == "Reading"

    for area, score, total in [("Reading", 4, 5), ("Writing", 7, 10), ("Grammar", 0, 1)]:
        saved = client.post(
            "/api/progress",
            json={
                "client_id": CLIENT_ID,
                "area": area,
                "level": "Beginner",
                "score": score,
                "total": total,
            },
        )
        assert saved.status_code == 200

    stats = client.get("/api/progress", params={"client_id": CLIENT_ID}).json()
    assert stats["total_practices"] == 3
    assert stats["average_score"] == 50  # (80 + 70 + 0) / 3
    assert stats["streak"] == 1
    assert stats["per_area"]["Reading"] == {"count": 1, "average": 80}
    assert stats["recommendation"]["area"] == "Vocabulary"  # first untried area
    assert stats["recent"][0]["area"] == "Grammar"

    other = client.get("/api/progress", params={"client_id": "someone-else-1"}).json()
    assert other["total_practices"] == 0


def test_progress_validation(client):
    base = {"client_id": CLIENT_ID, "area": "Reading", "level": "Beginner", "total": 5}
    assert client.post("/api/progress", json={**base, "score": 6}).status_code == 422
    assert client.post("/api/progress", json={**base, "score": -1}).status_code == 422
    assert client.post("/api/progress", json={**base, "score": 1, "total": 0}).status_code == 422
    bad_id = {**base, "score": 1, "client_id": "bad id!"}
    assert client.post("/api/progress", json=bad_id).status_code == 422
    assert client.get("/api/progress", params={"client_id": "x"}).status_code == 422


def test_recommendation_uses_weakest_area_when_all_tried(client):
    for area, score in [("Reading", 5), ("Writing", 9), ("Vocabulary", 1), ("Grammar", 1)]:
        client.post(
            "/api/progress",
            json={"client_id": CLIENT_ID, "area": area, "level": "Beginner", "score": score, "total": 10},
        )
    stats = client.get("/api/progress", params={"client_id": CLIENT_ID}).json()
    assert stats["recommendation"]["area"] in {"Vocabulary", "Grammar"}


def test_cors_allows_localhost_dev_server(client):
    response = client.options(
        "/api/generate-exercise",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
