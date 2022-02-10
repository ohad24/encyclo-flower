import pytest
import string
import random
import sys
import os

os.environ["MONGO_DB_NAME"] = "test"
sys.path.append("./src/api/")

from db import get_db


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


test_username = id_generator()


def pytest_configure():
    pytest.test_username = test_username
    pytest.question_id = None
    pytest.question_images_ids = None


@pytest.fixture(scope="session")
def base_url():
    return "/api/v1/"


@pytest.fixture
def db():
    return get_db()


@pytest.fixture(scope="session")
def auth_data():
    return {"Authorization": None}


@pytest.fixture(scope="session")
def auth_headers(auth_data):
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        **auth_data,
    }


@pytest.fixture(scope="session")
def auth_headers_with_no_content_type(auth_headers):
    auth_headers.pop("Content-Type", None)
    return auth_headers


@pytest.fixture
def editor_user(request, db):
    db = get_db()
    db.users.update_one(
        {"username": pytest.test_username}, {"$set": {"is_editor": True}}
    )
    request.addfinalizer(
        lambda: db.users.update_one(
            {"username": pytest.test_username}, {"$set": {"is_editor": False}}
        )
    )


@pytest.fixture
def change_user_id(request, db):
    """temporary change user id"""
    db = get_db()
    orig_user_id = db.users.find_one({"username": pytest.test_username})["user_id"]
    db.users.update_one(
        {"username": pytest.test_username}, {"$set": {"user_id": id_generator()}}
    )
    request.addfinalizer(
        lambda: db.users.update_one(
            {"username": pytest.test_username}, {"$set": {"user_id": orig_user_id}}
        )
    )


# from core.config import get_settings, Settings

# settings = get_settings()

# def get_settings_override():
#     return Settings(MONGO_DB_NAME="test")

# app.dependency_overrides[get_settings] = get_settings_override

# def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     return "".join(random.choice(chars) for _ in range(size))
