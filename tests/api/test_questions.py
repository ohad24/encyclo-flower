from test_main import client
import pytest
from pathlib import Path


@pytest.fixture(scope="module")
def question_url(base_url):
    # * Arrange
    return base_url + "community/questions/"


def create_user_question(question_url, auth_headers, question_data):
    response = client.post(question_url, headers=auth_headers, json=question_data)
    return response


class TestQuestion:
    def test_create_question(self, question_url, auth_headers):
        # * Arrange
        question_data = {
            "question_text": "What is the meaning of life?",
            "images": [
                {
                    "orig_file_name": "58NY77V207Q7H06.jpg",
                    "description": "test image",
                    "notes": "test notes",
                    "what_in_image": "פרי",
                    "location": {"lat": 0, "lon": 0, "alt": 0},
                },
                {
                    "orig_file_name": "I3YOFNKFFRVZOPN.jpg",
                    "description": "test image1",
                    "notes": "test notes1",
                    "what_in_image": "הצמח במלואו",
                },
            ],
        }
        # * Act
        # response = client.post(question_url, headers=auth_headers, json=question_data)
        response = create_user_question(question_url, auth_headers, question_data)
        # * Assert
        assert response.status_code == 200, response.text
        assert response.json()["question_id"][:2] == "q-"
        pytest.question_id = response.json()["question_id"]
        pytest.question_images_ids = response.json()["images_ids"]

    def test_add_new_image_metadata(self, auth_headers, question_url):
        """
        This test is for adding new image metadata to an existing question
        don't upload the image bytes, just add the metadata
        """
        # * Arrange
        new_image_metadata = [
            {
                "orig_file_name": "new_image.jpg",
                "description": "new image",
                "notes": "new notes",
                "what_in_image": "פרי",
                "location": {"lat": 0, "lon": 0, "alt": 0},
            }
        ]
        # * Act
        response = client.post(
            question_url + f"{pytest.question_id}/images_metadata",
            headers=auth_headers,
            json=new_image_metadata,
        )
        # * Assert
        assert response.status_code == 200, response.text

    def test_add_images(self, auth_headers, question_url):
        # * Arrange
        files = [
            (
                "images",
                (
                    "58NY77V207Q7H06.jpg",
                    Path("tests/assets/images/58NY77V207Q7H06.jpg").read_bytes(),
                ),
            ),
            (
                "images",
                (
                    "I3YOFNKFFRVZOPN.jpg",
                    Path("tests/assets/images/I3YOFNKFFRVZOPN.jpg").read_bytes(),
                ),
            ),
        ]
        auth_headers.pop("Content-Type", None)

        images_name_metadata = []
        for name in pytest.question_images_ids:
            images_name_metadata.append(
                (
                    "images_ids",
                    (name),
                )
            )

        # * Act
        response = client.post(
            question_url + f"{pytest.question_id}/images",
            headers=auth_headers,
            files=files,
            data=images_name_metadata,
        )
        # * Assert
        assert response.status_code == 200, response.text

    def test_add_comment(self, auth_headers, question_url):
        # * Arrange
        comment_data = {
            "comment_text": "This is a comment",
        }
        # * Act
        response = client.post(
            question_url + f"{pytest.question_id}/comments",
            headers=auth_headers,
            json=comment_data,
        )
        # * Assert
        assert response.status_code == 200

    def test_get_question(self, auth_headers, question_url):
        # * Act
        response = client.get(
            question_url + f"{pytest.question_id}", headers=auth_headers
        )
        # * Assert
        assert response.status_code == 200
        assert response.json()["question_id"] == pytest.question_id

    def test_get_all_questions(self, auth_headers, question_url):
        # * Act
        response = client.get(
            question_url, headers=auth_headers, params={"limit": 9, "skip": 0}
        )
        # * Assert
        assert response.status_code == 200
        assert 9 >= len(response.json()) >= 1

    def test_rotate_image(self, auth_headers, question_url):
        # * Arrange
        data = {
            "angle": "R",
        }
        # * Act
        response = client.post(
            question_url
            + f"{pytest.question_id}/images/{pytest.question_images_ids[0]}/rotate",
            headers=auth_headers,
            json=data,
        )
        # * Assert
        assert response.status_code == 200, response.text

    def test_delete_image(self, auth_headers, question_url):
        # * Act
        response = client.delete(
            question_url
            + f"{pytest.question_id}/images/{pytest.question_images_ids[0]}",
            headers=auth_headers,
        )
        # * Assert
        assert response.status_code == 200, response.text

    @pytest.mark.usefixtures("change_user_id")
    @pytest.mark.usefixtures("editor_user")
    def test_delete_image_as_editor(self, auth_headers, question_url):
        # * Act
        response = client.delete(
            question_url
            + f"{pytest.question_id}/images/{pytest.question_images_ids[1]}",
            headers=auth_headers,
        )
        # * Assert
        assert response.status_code == 200, response.text

    @pytest.mark.usefixtures("editor_user")
    def test_set_answer(self, auth_headers, question_url):
        # * Arrange
        answer_data = {"plant_id": "sfdm76"}
        # * Act
        response = client.post(
            question_url + f"{pytest.question_id}/answer",
            headers=auth_headers,
            json=answer_data,
        )
        # * Assert
        assert response.status_code == 200, response.text
