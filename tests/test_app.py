import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Club" in data
    assert "participants" in data["Basketball Club"]

def test_signup():
    # Signup a new participant
    response = client.post("/activities/Basketball%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Basketball Club"]["participants"]

def test_signup_duplicate():
    # Try to signup again
    response = client.post("/activities/Basketball%20Club/signup?email=test@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Already signed up" in data["detail"]

def test_unregister():
    # Unregister
    response = client.delete("/activities/Basketball%20Club/unregister?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" not in data["Basketball Club"]["participants"]

def test_unregister_not_signed():
    # Try to unregister someone not signed
    response = client.delete("/activities/Basketball%20Club/unregister?email=notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Not signed up" in data["detail"]

def test_activity_not_found():
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 307  # Redirect
    assert "/static/index.html" in response.headers["location"]