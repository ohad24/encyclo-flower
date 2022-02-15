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

    def get_observation(self, observation_id):
        response = client.get(
            self.observation_url + observation_id, headers=self.auth_headers
        )
        return response

    def create(self, number_of_observations=1):
        responses = [
            self.__create_one_observation() for x in range(number_of_observations)
        ]
        return responses[0] if len(responses) == 1 else responses

    def set_image_metadata(self, image_id, image_metadata):
        response = client.put(
            self.observation_url + self.observation_id + "/image/" + image_id,
            json=image_metadata,
            headers=self.auth_headers,
        )
        return response

    def upload_image(self, files, metadata):
        response = client.post(
            self.observation_url + self.observation_id + "/image",
            files=files,
            headers=self.file_auth_headers,
        )
        self.set_image_metadata(response.json()["image_id"], metadata)
        return response

    def delete_image(self, image_id):
        response = client.delete(
            self.observation_url + self.observation_id + "/image/" + image_id,
            headers=self.auth_headers,
        )
        return response

    def add_comment(self, comment_text):
        response = client.post(
            self.observation_url + self.observation_id + "/comment",
            json={"comment_text": comment_text},
            headers=self.auth_headers,
        )
        return response

    def submit_observation(self, observation_id):
        response = client.put(
            self.observation_url + observation_id + "/submit",
            headers=self.auth_headers,
        )
        return response

    def edit_observation(self, observation_id, header_data):
        response = client.put(
            self.observation_url + observation_id,
            json=header_data,
            headers=self.auth_headers,
        )
        return response

    def get_observations(self, limit=9, skip=0):
        response = client.get(
            self.observation_url,
            params={"limit": limit, "skip": skip},
            headers=self.auth_headers,
        )
        return response

    def rotate_image(self, observation_id, image_id, direction):
        response = client.post(
            self.observation_url + observation_id + "/images/" + image_id + "/rotate",
            json={"direction": direction},
            headers=self.auth_headers,
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
    def test_upload_image(self, user_observation, file_data):
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
        assert response.status_code == 200, response.text

    def test_delete_image(self, user_observation):
        # * Arrange
        observation = user_observation.get_observation(user_observation.observation_id)
        # * Act
        response = user_observation.delete_image(
            observation.json()["images"][0]["image_id"]
        )
        # * Assert
        assert response.status_code == 204, response.text

    def test_add_comment(self, user_observation):
        # * Arrange
        comment_text = "Here is some new comment"
        # * Act
        response = user_observation.add_comment(comment_text)
        observation = user_observation.get_observation(user_observation.observation_id)
        # * Assert
        assert response.status_code == 201, response.text
        assert observation.json()["comments"][0]["comment_text"] == comment_text

    def test_submit_observation(self, user_observation):
        # * Act
        response = user_observation.submit_observation(user_observation.observation_id)
        # * Assert
        assert response.status_code == 204, response.text

    def test_get_one_observation(self, user_observation):
        # * Act
        response = user_observation.get_observation(user_observation.observation_id)
        # * Assert
        assert response.status_code == 200, response.text
        assert response.json()["observation_id"] == user_observation.observation_id

    def test_edit_header(self, user_observation):
        # * Arrange
        header_data = {"observation_text": "new description"}
        # * Act
        response = user_observation.edit_observation(
            user_observation.observation_id,
            header_data=header_data,
        )
        # * Assert
        assert response.status_code == 204, response.text

        # * Get updated observation
        observation = user_observation.get_observation(user_observation.observation_id)
        # * Verify data
        assert observation.json()["observation_text"] == header_data["observation_text"]

    def test_get_observations(self, user_observation):
        # * Act
        response = user_observation.get_observations()
        # * Assert
        assert response.status_code == 200, response.text
        assert len(response.json()) > 0

    def test_rotate_image(self, user_observation):
        # * Arrange
        observation = user_observation.get_observation(user_observation.observation_id)
        image_id = observation.json()["images"][0]["image_id"]
        # * Act
        response = user_observation.rotate_image(
            user_observation.observation_id, image_id, "R"
        )
        # * Assert
        assert response.status_code == 204, response.text


# TODO: test get image
