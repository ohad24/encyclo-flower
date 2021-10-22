from fastapi.testclient import TestClient
import sys, os

os.environ["MONGO_DB_NAME"] = "test"
sys.path.append("./src/api/")

from main import app
import pytest


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


class TestUser:

    login_json = {
        "username": pytest.test_username,
        "full_name": "test",
        "password": "test",
        "email": "1@1.com",
    }

    def test_create_user(self):
        response = client.post(
            "/api/v1/users/",
            json=self.login_json,
        )
        assert response.status_code == 200

    def test_create_user_duplicate(self):
        response = client.post(
            "/api/v1/users/",
            json=self.login_json,
        )
        assert response.status_code == 400

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    

    def test_login(self):
        response = client.post(
            "/api/v1/token",
            data={"username": pytest.test_username, "password": "test"},
            headers=self.headers,
        )
        assert response.status_code == 200
        pytest.access_token = response.json()["access_token"]

    def test_login_failed(self):
        response = client.post(
            "/api/v1/token",
            data={"username": pytest.test_username + "1", "password": "test"},
            headers=self.headers,
        )
        assert response.status_code == 401

        response = client.post(
            "/api/v1/token",
            data={"username": pytest.test_username, "password": "test1"},
            headers=self.headers,
        )
        assert response.status_code == 401

    def test_get_users(self):
        response = client.get(
            "/api/v1/users/",
            headers={
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(pytest.access_token),
            },
        )
        assert response.status_code == 200
