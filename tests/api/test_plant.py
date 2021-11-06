from test_main import client
import pytest
import json
from common_fixtures import get_db
import os


def get_plants_names():
    limit = int(
        os.getenv("TESTS_GET_PLANTS_NAMES_LIMIT", 0)
    )  # * 0 is equivalent to no limit
    db = get_db()
    science_names = (
        db.plants.find({}, {"science_name": 1, "_id": 0})
        .limit(limit)
        .sort("science_name", 1)
    )
    return [plant["science_name"] for plant in science_names]


@pytest.fixture(scope="module")
def plants_url(base_url):
    # * Arrange
    return base_url + "plants/"


class TestPlant(object):
    @pytest.mark.parametrize("science_name", get_plants_names())
    def test_get_plant(self, science_name, plants_url):
        # * Act
        response = client.get(plants_url + science_name)
        # * Assert
        assert response.status_code == 200
        assert response.json()["science_name"] == science_name

    def test_get_plant_not_found(self, plants_url):
        # * Act
        response = client.get(plants_url + "a")
        # * Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "plant not found"


class TestSearch:
    @pytest.fixture(autouse=True)
    def plants_search_utl(self, plants_url):
        # * Arrange
        self._plants_search_url = plants_url + "search"

    def test_no_params(self):
        # * Act
        response = client.post(self._plants_search_url, headers=pytest.headers, json={})
        # * Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "must supply at least one parameter"}

    def test_no_results(self):
        # * Act
        response = client.post(
            self._plants_search_url,
            headers=pytest.headers,
            data=json.dumps({"name_text": "not_a_real_name"}),
        )
        # * Assert
        assert response.status_code == 200
        assert response.json() == {
            "total": 0,
            "plants": [],
            "total_pages": 1,
            "current_page": 1,
        }

    def test_search(self):
        # * Arrange
        response = client.post(
            self._plants_search_url,
            headers=pytest.headers,
            json={"name_text": "Aegilops sharonensis"},
        )
        # * Assert
        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert response.json()["plants"][0]["science_name"] == "Aegilops sharonensis"

    @pytest.fixture
    def multi_params(self):
        # * Arrange
        return {
            "colors": ["אדום"],
            "location_names": ["hula valley"],
            "seasons": ["4"],
        }

    def test_search_with_multi_params(self, multi_params):
        # * act
        response = client.post(
            self._plants_search_url, headers=pytest.headers, json=multi_params
        )
        # * assert
        assert response.status_code == 200
        assert response.json()["total"] == 20
        assert len(response.json()["plants"]) == 20

    @pytest.fixture(autouse=True)
    def basic_params(self):
        # * Arrange
        self._basic_params = {"name_text": "מצוי", "seasons": ["3"]}

    def test_search_with_multi_page(self):
        # * Act
        response = client.post(
            self._plants_search_url, headers=pytest.headers, json=self._basic_params
        )
        # * Assert
        assert response.status_code == 200
        assert response.json()["total"] == 105

        for page in range(response.json()["total_pages"]):
            # * Act
            response = client.post(
                self._plants_search_url,
                headers=pytest.headers,
                json=self._basic_params | {"page": page + 1},
            )
            # * Assert
            assert response.status_code == 200
            assert response.json()["total"] == 105
            assert (
                len(response.json()["plants"]) == 30
                if response.json()["current_page"] < response.json()["total_pages"]
                else response.json()["total"] % 30
            )

    def test_search_page_out_of_range(self):
        # * Act
        response = client.post(
            self._plants_search_url, headers=pytest.headers, json=self._basic_params
        )
        # * Assert
        assert response.status_code == 200
        assert response.json()["total"] == 105

        # * Act
        response = client.post(
            self._plants_search_url,
            headers=pytest.headers,
            json=self._basic_params | {"page": response.json()["total_pages"] + 1},
        )
        # * Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "page number out of range"}
