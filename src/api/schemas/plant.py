from pydantic import BaseModel
from typing import Dict, List, Optional, Literal
import db
from bson.son import SON

class Plant(BaseModel):
    science_name: str
    heb_name: str
    fam_name_eng: str
    fam_name_heb: str
    petal_num_name: Optional[str]
    leaf_shape_name: str
    leaf_edge_name: Optional[str]
    stem_shape_name: Optional[str]
    life_form_name: str
    description: Optional[str]
    protected: bool
    red: bool
    invasive: bool
    arr_syn_name_eng: Optional[List[str]]
    arr_syn_name_heb: Optional[List[str]]
    arr_location_name: Optional[List[str]]
    images_data: Optional[List[Dict]]
    images_count: int
    arr_habitat_name: Optional[List[str]]
    src_site_name: str
    src_site_url: str
    season_num: List[int]
    arr_color_name: List[str]


# pipeline_arr_color_name = [
#             {"$unwind": "$arr_color_name"},
#             {"$group": {"_id": "$arr_color_name"}},
#             {"$sort": SON([("_id", -1)])}
#         ]
# db = db.get_db()

# COLORS = tuple(x['_id'] for x in list(db.plants.aggregate(pipeline_arr_color_name)))
# print(COLORS)

# class PlantsColors(BaseModel):
#     colors: Literal[COLORS]


class SimplePlantsSearchIn(BaseModel):
    name_text: Optional[str]
    color_name: Optional[str]
    location_name: Optional[str]
    season_num: Optional[int]
    page: int = 0


class PlantSearchOut(BaseModel):
    heb_name: str
    science_name: Optional[str]  # ! for debug
    season_num: Optional[List]  # ! for debug
    arr_location_name: Optional[List]  # ! for debug
    arr_color_name: Optional[List]
    fam_name_heb: str
    image: Optional[dict]


class PlantsSearchOutList(BaseModel):
    total: int
    plants: List[Optional[PlantSearchOut]]
