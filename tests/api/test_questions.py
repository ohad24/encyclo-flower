from test_main import client
import pytest
from pathlib import Path
from conftest import google_credential_not_found
from images_data import upload_file_multi_params
import logging


@pytest.fixture(scope="module")
def question_url(base_url):
    # * Arrange
    return base_url + "community/questions/"


class QuestionTester:

    # TODO: need to implement more method (add image, add comment, etc)

    def __init__(self, auth_headers, auth_headers_with_no_content_type, question_url):
        self.auth_headers = auth_headers
        self.file_auth_headers = auth_headers_with_no_content_type
        self.question_url = question_url
        self.question_id = None

    def get_question(self, question_id):
        response = client.get(
            self.question_url + question_id, headers=self.auth_headers
        )
        return response

    def create(self, number_of_questions=1):
        question_data = {"question_text": "What is the meaning of life?"}
        responses = []
        for i in range(number_of_questions):
            # logging.info(self.question_url)
            response = client.post(
                self.question_url, json=question_data, headers=self.auth_headers
            )
            responses.append(response)
        return responses[0] if len(responses) == 1 else responses

    def set_image_metadata(self, image_id, image_metadata):
        response = client.put(
            self.question_url + self.question_id + "/image/" + image_id,
            json=image_metadata,
            headers=self.auth_headers,
        )
        assert response.status_code == 204
        return response

    def upload_image(self, files, metadata):
        response = client.post(
            self.question_url + self.question_id + "/image",
            files=files,
            headers=self.file_auth_headers,
        )
        if response.status_code == 200:
            self.set_image_metadata(response.json()["image_id"], metadata)
        return response

    def rotate_image(self, question_id, image_id, direction):
        response = client.post(
            self.question_url + question_id + "/images/" + image_id + "/rotate",
            json={"angle": direction},
            headers=self.auth_headers,
        )
        return response

    def delete_image(self, image_id):
        response = client.delete(
            self.question_url + self.question_id + "/images/" + image_id,
            headers=self.auth_headers,
        )
        return response

    def set_answer(self, question_id, answer_data):
        response = client.put(
            self.question_url + question_id + "/answer",
            headers=self.auth_headers,
            params=answer_data,
        )
        return response

    def remove_answer(self, question_id):
        response = client.delete(
            self.question_url + question_id + "/answer",
            headers=self.auth_headers,
        )
        return response

    def delete_question(self, question_id):
        response = client.delete(
            self.question_url + question_id,
            headers=self.auth_headers,
        )
        return response

    def add_comment(self, comment_text):
        response = client.post(
            self.question_url + self.question_id + "/comments",
            json={"comment_text": comment_text},
            headers=self.auth_headers,
        )
        return response

    def get_comments(self, question_id, limit=9, skip=0):
        response = client.get(
            self.question_url + question_id + "/comments",
            params={"limit": limit, "skip": skip},
            headers=self.auth_headers,
        )
        return response

    def submit_question(self, question_id):
        response = client.put(
            self.question_url + question_id + "/submit",
            headers=self.auth_headers,
        )
        return response

    def edit_question(self, question_id, question_data):
        response = client.put(
            self.question_url + question_id,
            json=question_data,
            headers=self.auth_headers,
        )
        return response


@pytest.fixture(scope="class")
def user_question(auth_headers, auth_headers_with_no_content_type, question_url):
    return QuestionTester(auth_headers, auth_headers_with_no_content_type, question_url)


class TestQuestion:
    def test_create_question(self, user_question):
        # * Act
        response = user_question.create(number_of_questions=1)
        # * Assert
        assert response.status_code == 200, response.text
        assert response.json()["question_id"][:2] == "q-"
        user_question.question_id = response.json()["question_id"]

    @google_credential_not_found
    @pytest.mark.parametrize(
        "file_data",
        upload_file_multi_params,
        ids=[x["test_name"] for x in upload_file_multi_params],
    )
    def test_upload_image(self, user_question, file_data):
        # * Arrange
        # * read file as bytes and set it in file_data
        file_name = file_data["file_name"]
        files = {
            "image": tuple(
                [
                    file_name,
                    Path(f"tests/assets/images/{file_name}").read_bytes(),
                ]
            )
        }
        # * Act
        response = user_question.upload_image(
            files=files, metadata=file_data["metadata"]
        )
        # * Assert
        assert response.status_code == 200, response.text

    def test_add_comment(self, user_question):
        # * Arrange
        comment_text = "Here is some new comment"
        # * Act
        response = user_question.add_comment(comment_text)
        # * Assert
        assert response.status_code == 201, response.text

    def test_get_comments(self, user_question):
        # * Act
        response = user_question.get_comments(user_question.question_id)
        # * Assert
        assert response.status_code == 200, response.text
        assert response.json()[0]["comment_text"] == "Here is some new comment"
        # TODO: add more comments (over 50) and check order

    def test_get_question(self, user_question):
        # * Act
        response = user_question.get_question(user_question.question_id)
        # * Assert
        assert response.status_code == 200

    @pytest.mark.skip(reason="change_user_id fixture is broken")
    @pytest.mark.usefixtures("change_user_id")
    def test_submit_question__not_owner(self, user_question):
        # * Act
        response = user_question.submit_question(user_question.question_id)
        # * Assert
        assert response.status_code == 403, response.text

    def test_submit_question(self, user_question):
        # * Act
        response = user_question.submit_question(user_question.question_id)
        # * Assert
        assert response.status_code == 204, response.text

    @pytest.mark.usefixtures("editor_user")
    def test_set_answer(self, user_question):
        # * Arrange
        answer_data = {"science_name": "Aegilops sharonensis"}
        # * Act
        response = user_question.set_answer(user_question.question_id, answer_data)
        # * Assert
        assert response.status_code == 204, response.text

    def test_set_answer__regular_user(self, user_question):
        # * Arrange
        answer_data = {"science_name": "Aegilops sharonensis"}
        # * Act
        response = user_question.set_answer(user_question.question_id, answer_data)
        # * Assert
        assert response.status_code == 403, response.text

    @pytest.mark.usefixtures("editor_user")
    def test_set_answer__wrong_plant(self, user_question):
        # * Arrange
        answer_data = {"science_name": "aaa"}
        # * Act
        response = user_question.set_answer(user_question.question_id, answer_data)
        # * Assert
        assert response.status_code == 404, response.text
        assert response.json()["detail"] == "Plant not found."

    def test_get_all_questions(self, auth_headers, question_url, user_question):
        # TODO: move to separate test class or refactor
        # * Arrange
        # * Create 8 questions (additional to first one)
        responses = user_question.create(number_of_questions=8)
        # * Submit questions (all 8)
        [user_question.submit_question(x.json().get("question_id")) for x in responses]
        # * Act
        response = client.get(
            question_url, headers=auth_headers, params={"limit": 9, "skip": 0}
        )
        # * Assert
        assert response.status_code == 200
        assert 9 == len(response.json())

        # # * Arrange
        # answer_data = {"plant_id": "sfdm76"}
        # # * set answer to first five questions
        # response = user_question.set_answer(
        #     responses[0].json().get("question_id"), answer_data
        # )
        # assert response.status_code == 200
        # * Act
        response = client.get(
            question_url,
            headers=auth_headers,
            params={"limit": 9, "skip": 0, "answer_filter": "answered"},
        )
        # * Assert
        assert response.status_code == 200
        assert 1 <= len(response.json())

        # * Arrange
        # # * create two more questions
        # responses = user_question.create(number_of_questions=2)
        # # * Submit questions (all 10)
        # [user_question.submit_question(x.json().get("question_id")) for x in responses]
        # * Act
        response = client.get(
            question_url,
            headers=auth_headers,
            params={"limit": 9, "skip": 0, "answer_filter": "not_answered"},
        )
        # * Assert
        assert response.status_code == 200
        assert 8 <= len(response.json())

    @google_credential_not_found
    def test_rotate_image(self, user_question):
        # * Arrange
        observation = user_question.get_question(user_question.question_id)
        image_id = observation.json()["images"][0]["image_id"]
        # * Act
        response = user_question.rotate_image(user_question.question_id, image_id, "R")
        # * Assert
        assert response.status_code == 204, response.text

    @google_credential_not_found
    def test_delete_image(self, user_question):
        # * Arrange
        question = user_question.get_question(user_question.question_id)
        # * Act
        response = user_question.delete_image(question.json()["images"][0]["image_id"])
        # * Assert
        assert response.status_code == 204, response.text

    def test_delete_image__wrong_image_id(self, user_question):
        # * Act
        response = user_question.delete_image("wrong_image_id")
        # * Assert
        assert response.status_code == 404, response.text
        assert response.json()["detail"] == "Image not found"

    def test_edit_question(self, user_question):
        # * Arrange
        question_data = {"question_text": "Here is some new question"}
        # * Act
        response = user_question.edit_question(user_question.question_id, question_data)
        # * Assert
        assert response.status_code == 204, response.text

        # * Act
        # * get question
        question = user_question.get_question(user_question.question_id)
        # * Assert
        assert question.json()["question_text"] == question_data["question_text"]

    @pytest.mark.usefixtures("editor_user")
    def test_remove_answer(self, user_question):
        # * Act
        response = user_question.remove_answer(user_question.question_id)
        # * Assert
        assert response.status_code == 204, response.text

    def test_remove_answer__regular_user(self, user_question):
        # * Act
        response = user_question.remove_answer(user_question.question_id)
        # * Assert
        assert response.status_code == 403, response.text

    @google_credential_not_found
    # @pytest.mark.usefixtures("change_user_id")  # TODO: fix later
    @pytest.mark.usefixtures("editor_user")
    def test_delete_image_as_editor(self, user_question):
        # * Arrange
        question = user_question.get_question(user_question.question_id)
        # * Act
        response = user_question.delete_image(question.json()["images"][0]["image_id"])
        # * Assert
        assert response.status_code == 204, response.text

    @google_credential_not_found
    @pytest.mark.usefixtures("editor_user")
    def test_delete_question(self, user_question):
        # * Act
        response = user_question.delete_question(user_question.question_id)
        # * Assert
        assert response.status_code == 204, response.text

        # * try to get deleted observation
        response = user_question.get_question(user_question.question_id)
        assert response.status_code == 404, response.text
