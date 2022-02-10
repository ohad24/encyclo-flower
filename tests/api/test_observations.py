from test_main import client
import pytest
from pathlib import Path


@pytest.fixture(scope="module")
def observation_url(base_url):
    # * Arrange
    return base_url + "community/observations/"


class ObservationTester:

    # TODO: need to implement more method (add image, add comment, etc)

    def __init__(self, auth_headers, observation_url):
        self.auth_headers = auth_headers
        self.observation_url = observation_url
        self.observation_id = None

    def __create_one_observation(self):
        observation_data = {
            "observation_text": "Here is some new observation",
        }
        response = client.post(
            self.observation_url, json=observation_data, headers=self.auth_headers
        )
        return response

    def create(self, number_of_observations=1):
        responses = [
            self.__create_one_observation() for x in range(number_of_observations)
        ]
        return responses[0] if len(responses) == 1 else responses

    def upload_image(self, image, image_name):
        image_data = {
            "description": "test image",
            "what_in_image": "פרי",
        }
        files = [
            (
                "image",
                (
                    image_name,
                    image,
                ),
            )
        ]
        self.auth_headers.pop("Content-Type", None)
        response = client.post(
            self.observation_url + self.observation_id + "/image",
            files=files,
            data=image_data,
            headers=self.auth_headers,
        )
        return response


@pytest.fixture(scope="class")
def user_observation(auth_headers, observation_url):
    return ObservationTester(auth_headers, observation_url)


class TestObservation:
    def test_create_observation(self, user_observation):
        # * Act
        response = user_observation.create(number_of_observations=1)
        # * Assert
        assert response.status_code == 200, response.text
        assert response.json()["observation_id"][:2] == "o-"

        # * set observation_id for next tests
        # pytest.observation_id = response.json()["observation_id"]
        user_observation.observation_id = response.json()["observation_id"]

    def test_observation_id(self, user_observation):
        assert user_observation.observation_id is not None
        assert user_observation.observation_id[:2] == "o-"  # TODO: remove later

    def test_observation_upload_image(self, user_observation):
        # * Arrange
        image_name = "IMG_with_exif.jpg"
        image = Path(f"tests/assets/images/{image_name}").read_bytes()
        # * Act
        response = user_observation.upload_image(image, image_name)
        # * Assert
        assert response.status_code == 201, response.text
        # TODO: parametrize with more images and different data
