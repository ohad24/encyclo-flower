from fastapi.testclient import TestClient
import json
from main import app
import pytest


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


@pytest.fixture
def get_users_url(base_url):
    # * Arrange
    return base_url + "users/"


class TestCreateUser:
    @pytest.fixture(autouse=True)
    def prepare_test_data(self, get_users_url):
        # * Arrange
        self._users_url = get_users_url
        self._login_json = json.dumps(
            {
                "username": pytest.test_username,
                "f_name": "Bob",
                "l_name": "Salad",
                "password": "test12",
                "email": f"{pytest.test_username}@1.com",
                "sex": "female",
                "phone": "+123456789",
                "settlement": "Haifa"
            }
        )

    def test_create_user(self):
        # * Act
        response = client.post(
            self._users_url,
            data=self._login_json,
        )
        # * Assert
        assert response.status_code == 200

    def test_create_user_duplicate(self):
        # * Act
        response = client.post(
            self._users_url,
            data=self._login_json,
        )
        # * Assert
        assert response.status_code == 400


class TestLogin:
    @pytest.fixture(autouse=True)
    def prepare_test_data(self, base_url):
        # * Arrange
        self._token_url = base_url + "token"
        self._login_headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def test_login(self, auth_data):
        # * Act
        response = client.post(
            self._token_url,
            data={"username": pytest.test_username, "password": "test12"},
            headers=self._login_headers,
        )
        # * Assert
        assert response.status_code == 200

        # * update fixture auth_data
        auth_data["Authorization"] = f"Bearer {response.json()['access_token']}"

    def test_login_failed(self):
        # * Act
        response = client.post(
            self._token_url,
            data={"username": pytest.test_username + "1", "password": "test12"},
            headers=self._login_headers,
        )
        # * Assert
        assert response.status_code == 401

        # * Act
        response = client.post(
            self._token_url,
            data={"username": pytest.test_username, "password": "test122"},
            headers=self._login_headers,
        )
        # * Assert
        assert response.status_code == 401


class TestUserAccess:
    @pytest.fixture(autouse=True)
    def prepare_test_data(self, get_users_url):
        # * Arrange
        self._users_url = get_users_url
        self._users_url_me = get_users_url + "me"

    def test_get_current_user(self, auth_headers):
        # * Act
        response = client.get(self._users_url_me, headers=auth_headers)
        # * Assert
        assert response.status_code == 200
        assert response.json()["username"] == pytest.test_username

    @pytest.fixture
    def set_db_inactive_active_user(self, db, request):
        # * Arrange
        db.users.update_one(
            {"username": pytest.test_username}, {"$set": {"is_active": False}}
        )

        def set_db_user_active():
            db.users.update_one(
                {"username": pytest.test_username}, {"$set": {"is_active": True}}
            )

        # * Post Assert
        request.addfinalizer(set_db_user_active)

    @pytest.mark.usefixtures("set_db_inactive_active_user")
    def test_auth_inactive_user(self, auth_headers):
        # * Act
        response = client.get(self._users_url_me, headers=auth_headers)
        # * Assert
        assert response.status_code == 400

    @pytest.fixture
    def set_db_user_superuser(self, db, request):
        # * Arrange
        db.users.update_one(
            {"username": pytest.test_username}, {"$set": {"is_superuser": True}}
        )

        def set_db_user_superuser_false():
            db.users.update_one(
                {"username": pytest.test_username}, {"$set": {"is_superuser": False}}
            )

        # * Post Assert
        request.addfinalizer(set_db_user_superuser_false)

    @pytest.mark.usefixtures("set_db_user_superuser")
    def test_superuser_access(self, auth_headers):
        # * Act
        response = client.get(self._users_url, headers=auth_headers)
        # * Assert
        assert response.status_code == 200

    def test_superuser_no_access(self, auth_headers):
        # * Act
        response = client.get(self._users_url, headers=auth_headers)
        # * Assert
        assert response.status_code == 403
        assert response.json()["detail"] == "The user does not have enough privileges"


class TestBrokenToken:
    @pytest.fixture(autouse=True)
    def prepare_test_data(self, get_users_url):
        # * Arrange
        self._users_url_me = get_users_url + "me"

    def test_access_invalid_token(self, db, auth_headers):
        # * Arrange + Act
        request = client.get(
            self._users_url_me,
            headers=auth_headers | {"Authorization": "Bearer 123"},
        )
        # * Assert
        assert request.status_code == 401

    @pytest.fixture
    def set_db_update_username(self, db, request):
        # * Arrange
        db.users.update_one(
            {"username": pytest.test_username},
            {"$set": {"username": pytest.test_username + "a"}},
        )

        def set_db_restore_username():
            db.users.update_one(
                {"username": pytest.test_username + "a"},
                {"$set": {"username": pytest.test_username}},
            )

        # * Post Assert
        request.addfinalizer(set_db_restore_username)

    # * test removed user
    @pytest.mark.usefixtures("set_db_update_username")
    def test_access_removed_user(self, auth_headers):
        # * Arrange
        request = client.get(
            self._users_url_me,
            headers=auth_headers,
        )
        # * Assert
        assert request.status_code == 401
