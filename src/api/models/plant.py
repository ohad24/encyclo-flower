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
    genus: str
    family: str
    subfamily: Optional[str]
    clade1: str
    clade2: str
    clade3: Optional[str]
    clade4: Optional[str]


class Plant(DBBaseModel):
    science_name: str
    heb_name: str
    fam_name_eng: Optional[str]
    petal_num_name: Optional[str]
    leaf_shape_name: List[str]
    leaf_edge_name: List[str]
    leaf_arrangement: List[str]
    stem_shape_name: Optional[str]
    life_form_name: List[str]
    description: Optional[str]
    protected: bool
    red: bool
    invasive: bool
    arr_syn_name_eng: List[str]
    arr_syn_name_heb: List[str]
    arr_location_name: Dict
    images_data: Optional[List[Dict]]
    arr_habitat_name: List[str]
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
    location_names: Optional[List[str]]
    seasons: Optional[List[int]]
    page: int = Field(ge=1, default=1)


class SearchOut(BaseModel):
    heb_name: str
    science_name: str  # ! for debug
    season_num: List  # ! for debug
    arr_location_name: Dict  # ! for debug
    arr_color_name: List
    image: Optional[dict]


class SearchOutList(BaseModel):
    total: int = 0
    total_pages: int = 1
    current_page: int = 1
    plants: List[Optional[SearchOut]] = []
