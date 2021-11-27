from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal
from db import get_db
from bson.son import SON
from models.base import DBBaseModel

db = get_db()

pipeline_colors_name = [
    {"$unwind": "$colors"},
    {"$group": {"_id": "$colors"}},
    {"$sort": SON([("_id", -1)])},
]


COLORS = Literal[
    tuple(x["_id"] for x in list(db.plants.aggregate(pipeline_colors_name)))
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
    leaf_shapes: List[str]
    leaf_edges: List[str]
    leaf_arrangements: List[str]
    stem_shapes: Optional[str]
    life_forms: List[str]
    description: Optional[str]
    protected: bool
    red: bool
    invasive: bool
    synonym_names_eng: List[str]
    synonym_names_heb: List[str]
    locations: Dict
    images_data: Optional[List[Dict]]
    habitats: List[str]
    flowering_seasons: Optional[List[int]]
    colors: List[COLORS]
    sex_flower: List[str]
    danger: bool
    rare: bool
    taxon: Taxonomy
    spine: List[str]


class SearchIn(BaseModel):
    name_text: Optional[str]
    colors: Optional[List[COLORS]]
    location_names: Optional[List[str]]
    flowering_seasons: Optional[List[int]]
    petals: Optional[List[str]]
    # TODO: leaf attributes
    life_forms: Optional[List[str]]
    habitats: Optional[List[str]]
    stem_shapes: Optional[List[str]]
    spine: Optional[List[str]]
    red: Optional[bool]
    invasive: Optional[bool]
    danger: Optional[bool]
    rare: Optional[bool]
    page: int = Field(ge=1, default=1)


class SearchOut(BaseModel):
    heb_name: str
    science_name: str  # ! for debug
    flowering_seasons: Optional[List[int]]  # ! for debug
    colors: List
    image: Optional[dict]


class SearchOutList(BaseModel):
    total: int = 0
    total_pages: int = 1
    current_page: int = 1
    plants: List[Optional[SearchOut]] = []
