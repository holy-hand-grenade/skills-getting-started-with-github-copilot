import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

INITIAL = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(INITIAL))
    yield
    activities.clear()
    activities.update(copy.deepcopy(INITIAL))


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities(client):
    # Arrange
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    assert "Chess Club" in resp.json()


def test_signup_and_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "tester@example.com"
    # Act
    r1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert r1.status_code == 200
    assert r2.status_code == 400


def test_remove_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    r = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert r.status_code == 200
    assert email not in activities[activity]["participants"]
