from test_main import client
import pytest
import json
from common_fixtures import db


@pytest.fixture
def get_plants_names(db):
    return db.plants.find({}, {"science_name": 1, "_id": 0}).sort("science_name", 1)


class TestPlant:
    def test_get_plant(self, get_plants_names):
        for i, plant in enumerate(get_plants_names[:10]):
            url = f"/api/v1/plants/{plant.get('science_name')}"
            # print(i, url)
            response = client.get(url)
            assert response.status_code == 200
            assert response.json()['science_name'] == plant.get('science_name')

    def test_get_plant_not_found(self):
        url = "/api/v1/plants/a"
        response = client.get(url)
        assert response.status_code == 404
        assert response.json()['detail'] == "plant not found"



class TestSimpleSearch:
    def test_no_params(self):
        response = client.post("/api/v1/plants/search", headers=pytest.headers, json={})
        # print(response.json())
        assert response.status_code == 400
        assert response.json() == {"detail": "must supply at least one parameter"}

    def test_no_results(self):
        response = client.post(
            "/api/v1/plants/search",
            headers=pytest.headers,
            data=json.dumps({"name_text": "not_a_real_name"}),
        )
        assert response.status_code == 200
        assert response.json() == {
            "total": 0,
            "plants": [],
            "total_pages": 1,
            "current_page": 1,
        }

    def test_search(self):
        response = client.post(
            "/api/v1/plants/search",
            headers=pytest.headers,
            json={"name_text": "Aegilops sharonensis"},
        )
        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert response.json()["plants"][0]["science_name"] == "Aegilops sharonensis"

    def test_search_with_multi_params(self):
        params = {"colors": ["אדום"], "location_names": ["hula valley"], "seasons": ["4"]}
        response = client.post(
            "/api/v1/plants/search", headers=pytest.headers, json=params
        )
        assert response.status_code == 200
        assert response.json()["total"] == 20
        assert len(response.json()["plants"]) == 20

    def test_search_with_multi_page(self):
        params = {"name_text": "מצוי", "seasons": ["3"]}
        response = client.post(
            "/api/v1/plants/search", headers=pytest.headers, json=params
        )
        assert response.status_code == 200
        assert response.json()["total"] == 105

        for page in range(response.json()["total_pages"]):
            response = client.post(
                "/api/v1/plants/search",
                headers=pytest.headers,
                json=params | {"page": page + 1},
            )
            assert response.status_code == 200
            assert response.json()["total"] == 105
            assert (
                len(response.json()["plants"]) == 30
                if response.json()["current_page"] < response.json()["total_pages"]
                else response.json()["total"] % 30
            )

    def test_search_page_out_of_range(self):
        params = {"name_text": "מצוי", "seasons": ["3"]}
        response = client.post(
            "/api/v1/plants/search", headers=pytest.headers, json=params
        )
        assert response.status_code == 200
        assert response.json()["total"] == 105

        response = client.post(
            "/api/v1/plants/search",
            headers=pytest.headers,
            json=params | {"page": response.json()["total_pages"] + 1},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "page number out of range"}
