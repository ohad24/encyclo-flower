import pytest

from pydantic import BaseModel
from typing import Dict, List, Optional, Literal


# def pytest_addoption(parser):
#     parser.addoption(
#         "--filename",
#         action="store",
#         default="plants_data.json",
#         help="plants data file name",
#     )


# @pytest.fixture
# def filename(request):
#     return request.config.getoption("--filename")

class Taxonomy(BaseModel):
    genus: Optional[str]
    family: Optional[str]
    subfamily: Optional[str]
    clade1: Optional[str]
    clade2: Optional[str]
    clade3: Optional[str]
    clade4: Optional[str]


class Plant(BaseModel):
    science_name: str
    heb_name: str
    fam_name_eng: Optional[str]
    # fam_name_heb: Optional[str]
    petal_num_name: Optional[str]
    leaf_shape_name: Optional[List[str]]
    leaf_edge_name: Optional[List[str]]
    leaf_arrangement: List[str]
    stem_shape_name: Optional[str]
    life_form_name: List[str]
    description: Optional[str]
    protected: bool
    red: bool
    invasive: bool
    arr_syn_name_eng: List[str]
    arr_syn_name_heb: Optional[List[str]]
    arr_location_name: Optional[Dict]
    images_data: Optional[List[Dict]]
    # images_count: int
    arr_habitat_name: List[str]
    # src_site_name: str
    # src_site_url: str
    season_num: Optional[List[int]]
    arr_color_name: List[str]
    sex_flower: List[str]
    denger: bool
    rare: bool
    taxon: Taxonomy
    spine: List[str]
