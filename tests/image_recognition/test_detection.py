# from fastapi import FastAPI
import sys

sys.path.append("./src/services/image_recognition/")
from plant_recognition import app
from fastapi.testclient import TestClient

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
    assert response.json() == [
        {"class_name": "Erodium gruinum", "score": 0.13281},
        {"class_name": "Ipomoea indica", "score": 0.05469},
        {"class_name": "Solanum laciniatum", "score": 0.04688},
        {"class_name": "Nicandra physalodes", "score": 0.04297},
        {"class_name": "Hibiscus trionum", "score": 0.02344},
    ]
