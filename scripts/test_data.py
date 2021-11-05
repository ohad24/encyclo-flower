import pytest
import json
import os
from conftest import Plant

from pydantic import ValidationError


FILE_NAME = "plant_data_1_11_2021.json"


@pytest.fixture
def file_exists(FILE_NAME):
    # FILE_NAME = request.config.getoption("--file-name")
    assert os.path.isfile(FILE_NAME) is True, f"File {FILE_NAME} does not exist"


# @pytest.mark.usefixtures("FILE_NAME")
# @pytest.fixture
def json_file(FILE_NAME):
    with open(FILE_NAME) as f:
        data = json.load(f)
    return sorted(data, key=lambda d: d["science_name"])


@pytest.mark.usefixtures("file_exists")
@pytest.fixture
def data():
    try:
        data = json_file(FILE_NAME)
    except FileNotFoundError:
        data = None
    return data


def test_json_data_type(data):
    assert isinstance(data, list), "json_data is not a list"


class TestJsonData:
    @pytest.mark.parametrize(
        "plant_data", json_file(FILE_NAME), ids=lambda d: d["science_name"]
    )
    def test_plants_type_dict(self, plant_data):
        # request.config.getoption("--file-name")
        # print(f"{plant_data.get('science_name')}", end=" :: ")
        assert isinstance(plant_data, dict), "plants_data is not a dict"

    @pytest.mark.parametrize(
        "plant_data", json_file(FILE_NAME), ids=lambda d: d["science_name"]
    )
    def test_plants_model(cls, plant_data):
        # request.config.getoption("--file-name")
        error = ''
        # try:
        plant = Plant(**plant_data)
        # except ValidationError as e:
        #     # print(e)
        #     error = e
        #     plant = {}
        # assert json.dumps(plant_data) == json.dumps(dict(plant), ensure_ascii=True)
        # assert dict(plant_data).keys() in dict(plant).keys()
        assert all([(key in plant.dict()) for key in plant_data.keys()])
        assert plant is not {}
        # assert isinstance(plant_data.keys(), list), "plants_data is not a list"
