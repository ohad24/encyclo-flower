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
        assert response.json() == {"total": 0, "plants": []}

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
        assert len(response.json()["plants"]) == 10

        for page in range(math.floor(response.json()["total"] / 10)):
            response = client.get(
                "/api/v1/plants/simple_search",
                headers=pytest.headers,
                params=params | {"page": page},
            )
            assert response.status_code == 200
            assert response.json()["total"] == 23
            assert (
                len(response.json()["plants"]) == 10
                if page < 2
                else response.json()["total"] % 10
            )
