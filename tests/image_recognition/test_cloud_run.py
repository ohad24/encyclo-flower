import pytest
import google.auth.transport.requests
import google.oauth2.id_token
import os
import requests
from pathlib import Path


"""
# * Based on https://github.com/GoogleCloudPlatform/python-docs-samples/blob/HEAD/auth/service-to-service/auth.py
This script run on GH Actions and test the Cloud Run service after build.
You can run this locally with
pytest tests/image_recognition/test_cloud_run.py --url=$( gcloud run services describe detect-tmp --region us-central1 --format=json | jq .status.url --raw-output) --google-cred-file-location=src/api/google_cred.json
"""


@pytest.fixture(scope="session")
def get_param(request):
    config_param = {}
    config_param["url"] = request.config.getoption("--url")
    config_param["google_cred_file_location"] = request.config.getoption(
        "--google-cred-file-location"
    )
    return config_param


@pytest.fixture(scope="session")
def base_url(get_param):
    return get_param.get("url")


@pytest.fixture(scope="session")
def service_url(base_url):
    return f"{base_url}/detect/"


@pytest.fixture(scope="session", autouse=True)
def set_credentials_file_location(get_param):
    google_cred_file_location = get_param.get("google_cred_file_location")
    if google_cred_file_location:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_cred_file_location


@pytest.fixture(scope="session")
def check_credentials_file():
    google_credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if google_credentials_file and Path(google_credentials_file).is_file():
        return True
    return False


@pytest.fixture(scope="session")
def id_token(base_url, check_credentials_file):
    if not check_credentials_file:
        pytest.fail("Google credentials file not found")

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, base_url)

    return id_token


@pytest.fixture
def files():
    return {"file": open("./tests/assets/images/58NY77V207Q7H06.jpg", "rb")}


def test_unauthorized(id_token, files, service_url):
    headers = {"Authorization": f"Bearer {id_token}1"}  # * Invalid token
    response = requests.post(service_url, headers=headers, files=files)
    assert response.status_code == 401


def test_authorized(id_token, files, service_url):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.post(service_url, headers=headers, files=files)
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"class_name": "Erodium gruinum", "score": 0.13281},
        {"class_name": "Ipomoea indica", "score": 0.05469},
        {"class_name": "Solanum laciniatum", "score": 0.04688},
        {"class_name": "Nicandra physalodes", "score": 0.04297},
        {"class_name": "Hibiscus trionum", "score": 0.02344},
    ]
