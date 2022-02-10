from test_main import client
import pytest
from pathlib import Path


@pytest.fixture(scope="module")
def observation_url(base_url):
    # * Arrange
    return base_url + "community/observations/"


class ObservationTester:

    # TODO: need to implement more method (add image, add comment, etc)

    def __init__(
        self, auth_headers, auth_headers_with_no_content_type, observation_url
    ):
        self.auth_headers = auth_headers
        self.file_auth_headers = auth_headers_with_no_content_type
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

    def upload_image(self, files, metadata):
        response = client.post(
            self.observation_url + self.observation_id + "/image",
            files=files,
            data=metadata,
            headers=self.file_auth_headers,
        )
        return response


@pytest.fixture(scope="class")
def user_observation(auth_headers, auth_headers_with_no_content_type, observation_url):
    return ObservationTester(
        auth_headers, auth_headers_with_no_content_type, observation_url
    )


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

    upload_file_multi_params = [
        {
            "metadata": {},
            "files": [
                (
                    "image",
                    [
                        "IMG_with_exif.jpg",
                    ],
                )
            ],
            "test_name": "Minimum metadata + with gps data",
        },
        {
            "metadata": {
                "description": "test image",
                "what_in_image": "פרי",
                "plant_id": "sfdm76",
            },
            "files": [
                (
                    "image",
                    [
                        "IMG_with_exif.jpg",
                    ],
                )
            ],
            "test_name": "Maximum metadata + with gps data",
        },
        {
            "metadata": {},
            "files": [
                (
                    "image",
                    [
                        "58NY77V207Q7H06.jpg",
                    ],
                )
            ],
            "test_name": "Minimum metadata + with no gps data",
        },
        {
            "metadata": {
                "description": "test image",
                "what_in_image": "פרי",
                "plant_id": "sfdm76",
            },
            "files": [
                (
                    "image",
                    [
                        "58NY77V207Q7H06.jpg",
                    ],
                )
            ],
            "test_name": "Maximum metadata + with no gps data",
        },
    ]

    @pytest.mark.parametrize(
        "file_data",
        upload_file_multi_params,
        ids=[x["test_name"] for x in upload_file_multi_params],
    )
    def test_observation_upload_image(self, user_observation, file_data):
        # * Arrange
        # * read file as bytes and set it in file_data
        file_data["files"][0][1].append(
            Path(f"tests/assets/images/{file_data['files'][0][1][0]}").read_bytes()
        )
        # * Act
        response = user_observation.upload_image(
            files=file_data["files"], metadata=file_data["metadata"]
        )
        # * Assert
        assert response.status_code == 201, response.text
        # TODO: parametrize with more images and different data
