import pytest
import string
import random
import sys, os

os.environ["MONGO_DB_NAME"] = "test"
sys.path.append("./src/api/")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))

test_username = id_generator()

def pytest_configure():
    pytest.test_username = test_username
    pytest.access_token = None

    pytest.headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


# from core.config import get_settings, Settings

# settings = get_settings()

# def get_settings_override():
#     return Settings(MONGO_DB_NAME="test")

# app.dependency_overrides[get_settings] = get_settings_override

# def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     return "".join(random.choice(chars) for _ in range(size))
