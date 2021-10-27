import pytest
from db import get_db


@pytest.fixture
def db():
    return get_db()
