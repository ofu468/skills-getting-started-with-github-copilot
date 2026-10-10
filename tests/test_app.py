from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    baseline = deepcopy(activities)
    activities.clear()
    activities.update(deepcopy(baseline))

    with TestClient(app) as test_client:
        yield test_client

    activities.clear()
    activities.update(baseline)


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    payload = client.get("/activities").json()
    assert email in payload[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_unknown_activity_returns_not_found(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404


def test_signup_without_email_returns_validation_error(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


def test_unregister_participant_removes_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert signup_response.status_code == 200
    assert response.status_code == 200
    payload = client.get("/activities").json()
    assert email not in payload[activity_name]["participants"]


def test_unregister_unknown_email_returns_error(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
