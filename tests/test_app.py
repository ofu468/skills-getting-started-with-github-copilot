from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    payload = client.get("/activities").json()
    assert email not in payload[activity_name]["participants"]


def test_unregister_unknown_email_returns_error():
    activity_name = "Chess Club"
    email = "missing.student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 400
