import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("participants" in v for v in data.values())


def test_signup_and_unregister():
    activity = list(client.get("/activities").json().keys())[0]
    email = "pytestuser@mergington.edu"

    # Signup
    resp_signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup.status_code == 200
    assert f"Signed up {email}" in resp_signup.json()["message"]

    # Unregister
    resp_unreg = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg.status_code == 200
    assert f"Removed {email}" in resp_unreg.json()["message"]

    # Unregister again should fail
    resp_unreg2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg2.status_code == 404
    assert "Participant not found" in resp_unreg2.json()["detail"]
