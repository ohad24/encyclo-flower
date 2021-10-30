from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal
from db import get_db
from bson.son import SON
from models.base import DBBaseModel

db = get_db()

pipeline_arr_color_name = [
    {"$unwind": "$arr_color_name"},
    {"$group": {"_id": "$arr_color_name"}},
    {"$sort": SON([("_id", -1)])},
]


COLORS = Literal[
    tuple(x["_id"] for x in list(db.plants.aggregate(pipeline_arr_color_name)))
]


class Taxonomy(BaseModel):
    genus: Optional[str]
    family: Optional[str]
    subfamily: Optional[str]
    clade1: Optional[str]
    clade2: Optional[str]
    clade3: Optional[str]
    clade4: Optional[str]


class Plant(DBBaseModel):
    science_name: str
    heb_name: str
    fam_name_eng: Optional[str]
    fam_name_heb: Optional[str]
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
    arr_color_name: List[COLORS]
    sex_flower: List[str]
    denger: bool
    rare: bool
    taxon: Taxonomy
    spine: List[str]


class SearchIn(BaseModel):
    name_text: Optional[str]
    colors: Optional[List[COLORS]]
    location_name: Optional[str]
    season_num: Optional[int]
    page: int = Field(ge=1, default=1)


class SearchOut(BaseModel):
    heb_name: str
    science_name: Optional[str]  # ! for debug
    season_num: Optional[List]  # ! for debug
    arr_location_name: Optional[Dict]  # ! for debug
    arr_color_name: Optional[List]
    fam_name_heb: str
    image: Optional[dict]


class SearchOutList(BaseModel):
    total: int = 0
    total_pages: int = 1
    current_page: int = 1
    plants: List[Optional[SearchOut]] = []
