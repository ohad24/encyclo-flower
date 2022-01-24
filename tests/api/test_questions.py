from test_main import client
import pytest
import json
from db import get_db
import os
from pathlib import Path


@pytest.fixture(scope="module")
def question_url(base_url):
    # * Arrange
    return base_url + "community/questions"


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
        response = client.post(question_url, headers=auth_headers, json=question_data)
        # * Assert
        assert response.status_code == 200
        assert response.json()["question_id"][:2] == "q-"
        pytest.question_id = response.json()["question_id"]

    def test_add_image(self, auth_headers, question_url):
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
        # * Act
        response = client.post(
            question_url + f"/{pytest.question_id}/images",
            headers=auth_headers,
            files=files,
        )
        # * Assert
        assert response.status_code == 200