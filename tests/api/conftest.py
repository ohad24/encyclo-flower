import pytest
import string
import random
import sys
import os
import logging

os.environ["MONGO_DB_NAME"] = "test"
sys.path.append("./src/api/")

from db import get_db
from core.gstorage import bucket


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


@pytest.fixture(scope="session", autouse=True)
def teardown(request):
    def do_teardown():
        logging.info("Finalizing tests. Teardown")
        logging.info("Check if tests failed")
        test_failed = False
        for item in request.node.items:
            if item.session.exitstatus != 0:
                test_failed = True
                break
        if not test_failed:
            logging.info("No tests failed. Deleting test data")
            # * clear db collections
            db = get_db()
            db.users.delete_many({})
            db.questions.delete_many({})
            db.observations.delete_many({})
            db.comments.delete_many({})
            db.images_detections.delete_many({})

            # * clear google cloud storage
            bucket.delete_blobs(list(bucket.list_blobs(prefix="questions/")))
            bucket.delete_blobs(list(bucket.list_blobs(prefix="observations/")))
            bucket.delete_blobs(list(bucket.list_blobs(prefix="image_api_files/")))
        else:
            logging.info("Tests failed. Not deleting test data")

    request.addfinalizer(do_teardown)
