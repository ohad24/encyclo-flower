from fastapi import params
from fastapi.params import Header
from test_main import client
import pytest
from db import get_db
import math


class TestSimpleSearch:
    def test_no_params(self):
        response = client.get("/api/v1/plants/simple_search", headers=pytest.headers)
        assert response.status_code == 400
        assert response.json() == {"detail": "must supply at least one parameter"}

    def test_no_results(self):
        response = client.get(
            "/api/v1/plants/simple_search",
            headers=pytest.headers,
            params={"name_text": "not_a_real_name"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "total": 0,
            "plants": [],
            "pages": 1,
            "current_page": 1,
        }

    def test_simple_search(self):
        response = client.get(
            "/api/v1/plants/simple_search",
            headers=pytest.headers,
            params={"name_text": "Aegilops sharonensis"},
        )
        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert response.json()["plants"][0]["science_name"] == "Aegilops sharonensis"

    def test_simple_search_with_multi_params(self):
        params = {"color_name": "אדום", "location_name": "עמקים", "season_num": "4"}
        response = client.get(
            "/api/v1/plants/simple_search", headers=pytest.headers, params=params
        )
        assert response.status_code == 200
        assert response.json()["total"] == 23
        assert len(response.json()["plants"]) == 23

    def test_simple_search_with_multi_page(self):
        params = {"name_text": "מצוי", "season_num": "3"}
        response = client.get(
            "/api/v1/plants/simple_search", headers=pytest.headers, params=params
        )
        assert response.status_code == 200
        assert response.json()["total"] == 98

        for page in range(response.json()["pages"]):
            response = client.get(
                "/api/v1/plants/simple_search",
                headers=pytest.headers,
                params=params | {"page": page + 1},
            )
            assert response.status_code == 200
            assert response.json()["total"] == 98
            assert (
                len(response.json()["plants"]) == 30
                if response.json()["current_page"] < response.json()["pages"]
                else response.json()["total"] % 30
            )

    def test_simple_search_page_out_of_range(self):
        params = {"name_text": "מצוי", "season_num": "3"}
        response = client.get(
            "/api/v1/plants/simple_search", headers=pytest.headers, params=params
        )
        assert response.status_code == 200
        assert response.json()["total"] == 98

        response = client.get(
            "/api/v1/plants/simple_search",
            headers=pytest.headers,
            params=params | {"page": response.json()["pages"] + 1},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "page number out of range"}
