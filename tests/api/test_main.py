from fastapi.testclient import TestClient
import json
from main import app
import pytest
from conftest import google_credential_not_found, get_db
from requests.auth import HTTPBasicAuth
from core.config import get_settings
import time

settings = get_settings()

settings.DETECT_USAGE_RATE_REQUEST_NUM = 3
settings.DETECT_USAGE_RATE_TIME_WINDOW_SECONDS = 10


client = TestClient(app)


def test_read_main():
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200


@pytest.fixture
def get_users_url(base_url):
    # * Arrange
    return base_url + "users/"


@pytest.fixture
def get_helpers_url(base_url):
    # * Arrange
    return base_url + "helpers/"


@pytest.fixture
def detect_image_url(base_url):
    # * Arrange
    return base_url + "detect/image/"


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
                "confirm_password": "test12",
                "email": f"{pytest.test_username}@1.com",
                "sex": "נקבה",
                "phone": "+123456789",
                "settlement": "Haifa",
                "accept_terms_of_service": "true",
            }
        )

    def test_accept_terms_of_service(self):
        # * Arrange
        false_terms_of_service_data = json.loads(self._login_json)
        false_terms_of_service_data["accept_terms_of_service"] = "false"
        # * Act
        response = client.post(
            self._users_url,
            json=false_terms_of_service_data,
        )
        # * Assert
        assert response.status_code == 400
        assert (
            response.json()["detail"] == "Terms of service must be accepted"
        ), response.json()

    def test_password_not_match(self):
        # * Arrange
        login_json = json.loads(self._login_json)
        login_json["confirm_password"] = "test13"
        # * Act
        response = client.post(
            self._users_url,
            json=login_json,
        )
        # * Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "The passwords do not match"

    def test_create_user(self):
        # * Act
        response = client.post(
            self._users_url,
            data=self._login_json,
        )
        # * Assert
        assert response.status_code == 201

    def test_create_user_duplicate(self):
        # * Act
        response = client.post(
            self._users_url,
            data=self._login_json,
        )
        # * Assert
        assert response.status_code == 400
        assert (
            response.json()["detail"]
            == "The user with this username or email already exists in the system."
        )

    def test_email_verification_fails(self):
        # * Act
        response = client.get(self._users_url + "verify-email/aaa")
        # * Assert
        assert response.status_code == 404

    def test_email_verification_success(self):
        # * Arrange
        db = get_db()
        data = next(
            db.email_verification_tokens.find({}).sort("create_dt", -1).limit(1)
        )
        # print(data)
        # * Act
        response = client.get(self._users_url + f"verify-email/{data['token']}")
        # * Assert
        assert response.status_code == 204


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

    def test_get_user__user_not_found(self, auth_headers):
        # * Act
        response = client.get(self._users_url + "aaa")
        # * Assert
        assert response.status_code == 404

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

    @pytest.mark.usefixtures("set_db_user_superuser")
    def test_docs__valid_access(self):
        # * Act
        response = client.get(
            "api/docs", auth=HTTPBasicAuth(pytest.test_username, "test12")
        )
        # * Assert
        assert response.status_code == 200

    @pytest.mark.usefixtures("set_db_user_superuser")
    def test_docs__wrong_password(self):
        # * Act
        response = client.get(
            "api/docs", auth=HTTPBasicAuth(pytest.test_username, "test123")
        )
        # * Assert
        assert response.status_code == 401

    def test_docs__regular_user(self):
        """not superuser"""
        # * Act
        response = client.get(
            "api/docs", auth=HTTPBasicAuth(pytest.test_username, "test12")
        )
        # * Assert
        assert response.status_code == 401

    def test_redoc__no_access(self):
        # * Act
        response = client.get("/redoc")
        # * Assert
        assert response.status_code == 404
        # * Act
        response = client.get("/api/redoc")
        # * Assert
        assert response.status_code == 404


class TestResetPassword:

    email = f"{pytest.test_username}@1.com"

    def test_reset_password_request(self, base_url):
        # * Act
        response = client.post(
            base_url + "reset-password-request",
            json={"email": self.email},
        )
        # * Assert
        assert response.status_code == 204, response.json()

    def test_reset_password_request__wrong_email(self, base_url):
        # * Act
        response = client.post(
            base_url + "reset-password-request",
            json={"email": "1@1.com"},
        )
        # * Assert
        assert response.status_code == 404, response.json()

    @pytest.fixture()
    def reset_password_token(self, db):
        user_data = next(db.users.find({"email": self.email}))
        data = next(
            db.reset_password_tokens.find({"user_id": user_data.get("user_id")})
        )
        return data["token"]

    def test_reset_password(self, reset_password_token, base_url):
        # * Act
        response = client.post(
            base_url + "reset-password",
            json={
                "token": reset_password_token,
                "password": "test12",
                "confirm_password": "test12",
            },
        )
        # * Assert
        assert response.status_code == 204, response.json()

    def test_reset_password__invalid_token(self, reset_password_token, base_url):
        # * Act
        response = client.post(
            base_url + "reset-password",
            json={
                "token": reset_password_token + "a",
                "password": "test12",
                "confirm_password": "test12",
            },
        )
        # * Assert
        assert response.status_code == 404, response.json()

    def test_login_after_reset_password(self, base_url, auth_headers):
        # * arrange
        token_url = base_url + "token"
        login_headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        # * Act
        response = client.post(
            token_url,
            data={"username": pytest.test_username, "password": "test12"},
            headers=login_headers,
        )
        # * Assert
        assert response.status_code == 200

        # * update fixture auth_data
        auth_headers["Authorization"] = f"Bearer {response.json()['access_token']}"


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

    # * test removed/not found user
    @pytest.mark.usefixtures("set_db_update_username")
    def test_access_removed_user(self, auth_headers):
        # * Arrange
        request = client.get(
            self._users_url_me,
            headers=auth_headers,
        )
        # * Assert
        assert request.status_code == 404
        assert request.json()["detail"] == "User not found"


class TestUserUpdateData:

    # * prepare assert data
    @pytest.fixture(autouse=True)
    def prepare_assert_data(self, get_users_url, auth_headers):
        # * Arrange
        self._users_url_me = get_users_url + "me"
        response = client.get(self._users_url_me, headers=auth_headers)
        self.phone = response.json()["phone"]
        self.settlement = response.json()["settlement"]

    def test_update_user(self, auth_headers, get_users_url):
        # * Act
        response = client.put(
            get_users_url + pytest.test_username,
            headers=auth_headers,
            json={"f_name": "new_f_name", "l_name": "new_l_name"},
        )
        # * Assert
        assert response.status_code == 204

        # * Act (get user)
        response = client.get(
            get_users_url + pytest.test_username, headers=auth_headers
        )
        # * Assert f_name is changed
        assert response.json()["f_name"] == "new_f_name"
        # * Assert phone didn't change
        assert response.json()["phone"] == self.phone
        assert response.json()["settlement"] == self.settlement

    def test_update_different_user(self, auth_headers, get_users_url):
        # * Act
        response = client.put(
            get_users_url + pytest.test_username + "1",
            headers=auth_headers,
            json={"f_name": "new_f_name", "l_name": "new_l_name"},
        )
        # * Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "The user is not allowed to edit this user"


class TestHelpers:
    def test_KML_translate(self, get_helpers_url):
        # * Arrange valid data
        lat: float = 33.040111127472926
        lon: float = 35.73356519465218
        # * Act - Valid data
        response = client.get(
            get_helpers_url + "translate_gps", params={"lat": lat, "lon": lon}
        )
        # * Assert
        assert response.status_code == 200
        assert response.json()["location"] == "גולן"

        # * Arrange invalid data
        lat: float = 1
        lon: float = 1
        # * Act - Valid data
        response = client.get(
            get_helpers_url + "translate_gps", params={"lat": lat, "lon": lon}
        )
        # * Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "location not found"


# @pytest.mark.skip(reason="Currently not developed fully")
@google_credential_not_found
class TestDetectImage:
    def test_detect_image(self, auth_headers, detect_image_url):
        # * Arrange
        auth_headers.pop("Content-Type", None)
        files = {"file": open("tests/assets/images/IWU8AAVDDDEEKRC.jpg", "rb")}
        # * Act
        response = client.post(
            detect_image_url,
            headers=auth_headers,
            files=files,
        )
        # * Assert
        assert response.status_code == 200
        assert len(response.json()) == 5
        assert response.json()[0] == {
            "heb_name": "כרכום גייארדו תת-מין חופי",
            "science_name": "Crocus aleppicus",
            "images": [
                {"file_name": "8T7M690R8WKUQCD.jpg", "level": "e"},
                {"file_name": "O5DB6U4CO3KV9P8.jpg", "level": "e"},
            ],
            "score": 0.125,
        }

    def test_detect_rate_limit(self, auth_headers, detect_image_url):
        # * Arrange
        auth_headers.pop("Content-Type", None)
        t = time.time()
        files = {"file": open("tests/assets/images/IWU8AAVDDDEEKRC.jpg", "rb")}
        for _ in range(0, settings.DETECT_USAGE_RATE_REQUEST_NUM - 1):
            # * Act
            response = client.post(
                detect_image_url,
                headers=auth_headers,
                files=files,
            )
            # * Assert
            assert response.status_code == 200
        response = client.post(
            detect_image_url,
            headers=auth_headers,
            files=files,
        )
        # * Assert
        assert response.status_code == 429
        assert response.json()["detail"] == "Too many requests"

        # * Wait for rate limit to reset
        while time.time() - t < settings.DETECT_USAGE_RATE_TIME_WINDOW_SECONDS:
            time.sleep(0.5)

        # * Act
        response = client.post(
            detect_image_url,
            headers=auth_headers,
            files=files,
        )
        # * Assert
        assert response.status_code == 200
