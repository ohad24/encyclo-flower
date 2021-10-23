from fastapi.testclient import TestClient
import json
from main import app
import pytest
from db import get_db


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


class TestUser:

    login_json = json.dumps(
        {
            "username": pytest.test_username,
            "full_name": "test",
            "password": "test",
            "email": "1@1.com",
        }
    )

    def test_create_user(self):
        response = client.post(
            "/api/v1/users/",
            data=self.login_json,
        )
        assert response.status_code == 200

    def test_create_user_duplicate(self):
        response = client.post(
            "/api/v1/users/",
            data=self.login_json,
        )
        assert response.status_code == 400

    login_headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def test_login(self):
        response = client.post(
            "/api/v1/token",
            data={"username": pytest.test_username, "password": "test"},
            headers=self.login_headers,
        )
        assert response.status_code == 200
        pytest.access_token = response.json()["access_token"]
        pytest.headers["Authorization"] = f"Bearer {pytest.access_token}"

    def test_login_failed(self):
        response = client.post(
            "/api/v1/token",
            data={"username": pytest.test_username + "1", "password": "test"},
            headers=self.login_headers,
        )
        assert response.status_code == 401

        response = client.post(
            "/api/v1/token",
            data={"username": pytest.test_username, "password": "test1"},
            headers=self.login_headers,
        )
        assert response.status_code == 401

    def test_get_current_user(self):
        response = client.get("/api/v1/users/me/", headers=pytest.headers)
        assert response.status_code == 200
        assert response.json()["username"] == pytest.test_username

    def test_all_users_superuser_access(self):
        db = get_db()
        db.users.update_one(
            {"username": pytest.test_username}, {"$set": {"is_superuser": True}}
        )
        response = client.get("/api/v1/users/", headers=pytest.headers)
        assert response.status_code == 200
        db.users.update_one(
            {"username": pytest.test_username}, {"$set": {"is_superuser": False}}
        )
    
    def test_all_users_superuser_no_access(self):
        response = client.get("/api/v1/users/", headers=pytest.headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "The user does not have enough privileges"

    def test_fault_credentials(self):
        db = get_db()

        # * test for invalid token
        request = client.get(
            "/api/v1/users/",
            headers=self.login_headers
            | {"Authorization": "Bearer {}".format(pytest.access_token + "1")},
        )
        assert request.status_code == 401

        # * test removed user
        db.users.update_one(
            {"username": pytest.test_username},
            {"$set": {"username": pytest.test_username + "a"}},
        )
        request = client.get(
            "/api/v1/users/",
            headers={
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(pytest.access_token),
            },
        )
        assert request.status_code == 401
        db.users.update_one(
            {"username": pytest.test_username + "a"},
            {"$set": {"username": pytest.test_username}},
        )

        # * inactive user
        db.users.update_one(
            {"username": pytest.test_username}, {"$set": {"is_active": False}}
        )

        request = client.get(
            "/api/v1/users/me/",
            headers=pytest.headers
        )
        assert request.status_code == 400

        db.users.update_one(
            {"username": pytest.test_username}, {"$set": {"is_active": True}}
        )
