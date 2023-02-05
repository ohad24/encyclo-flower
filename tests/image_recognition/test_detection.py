# from fastapi import FastAPI
import sys

sys.path.append("./src/services/image_recognition/")
from plant_recognition import app
from fastapi.testclient import TestClient
from conftest import ASSERT_DETECT_DATA

# app = FastAPI()


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404


def test_detection():
    response = client.post(
        "/detect/",
        files={"file": open("./tests/assets/images/58NY77V207Q7H06.jpg", "rb")},
    )
    assert response.status_code == 200
    assert response.json() == ASSERT_DETECT_DATA
