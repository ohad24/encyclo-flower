from pydantic import BaseModel, Field, AnyUrl, validator
from typing import Dict, List, Optional, Literal
from db import get_db
from bson.son import SON
from models.base import DBBaseModel
from datetime import datetime
from enum import Enum

db = get_db()

pipeline_colors_name = [
    {"$unwind": "$colors"},
    {"$group": {"_id": "$colors"}},
    {"$sort": SON([("_id", -1)])},
]


COLORS = Literal[
    tuple(x["_id"] for x in list(db.plants.aggregate(pipeline_colors_name)))
]


class LocationCommonEnum(str, Enum):
    a = "נפוץ"
    b = "מצוי"
    c = "נדיר"
    d = "נדיר מאוד"
    e = "שכיחות לא ידועה"


class LocationKMLtranslate(str, Enum):
    """
    key is the value in KML file
    value is the value in db
    """

    GalileeBeach = "חוף הגליל"
    CarmelBeach = "חוף הכרמל"
    Sharon = "שרון"
    SouthernBeach = "מישור החוף הדרומי"
    UpperGalilee = "גליל עליון"
    LowerGalilee = "גליל תחתון"
    Carmel = "כרמל"
    MenasheHills = "רמות מנשה"
    IzraelValley = "עמק יזרעאל"
    Shomron = "הרי שומרון"
    JudeaLowLands = "שפלת יהודה"
    JudeaMountains = "הרי יהודה"
    NorthernNegev = "צפון הנגב"
    WesternNegev = "מערב הנגב"
    CentralNegev = "מרכז והר הנגב"
    SouthernNegev = "דרום הנגב"
    Hula = "עמק החולה"
    KinarotValley = "בקעת כינרות"
    BetSheanValley = "עמק בית שאן"
    Gilboa = "גלבוע"
    ShomronDesert = "מדבר שומרון"
    JudeaDesert = "מדבר יהודה"
    JordanValley = "בקעת הירדן"
    DeadSeaValley = "בקעת ים המלח"
    Arava = "ערבה"
    Hermon = "חרמון"
    Golan = "גולן"


class Taxonomy(BaseModel):
    clade1: str
    clade2: str
    clade3: Optional[str]
    clade4: Optional[str]
    family: str
    subfamily: Optional[str]
    genus: str


class PlantImage(BaseModel):
    author_name: Optional[str]
    licenses: Optional[List[str]]
    what_inside: Optional[List[str]]
    image_date: Optional[datetime]
    location: Optional[List[str]]
    general_description: Optional[str]
    specific_description: Optional[str]
    source_url: Optional[AnyUrl]
    source_url_page: Optional[AnyUrl]
    level: Optional[str]
    file_name: str

    @validator("level")
    def set_level(cls, level):
        return level or "e"


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
    images: List[PlantImage]


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
    science_name: str
    colors: List
    image: Optional[PlantImage] = None
    commoness: Optional[str]

    def __init__(__pydantic_self__, **data: Dict) -> None:
        super().__init__(**data)
        plant = Plant(**data)
        if plant.images:
            # * sort images in plant by level - show pre selected image first
            # * sort reverse plant images by level (level = a,b,c.d)
            plant.images.sort(key=lambda x: x.level)
            # * get the first image
            __pydantic_self__.image = plant.images[0].file_name

        commoness = set(plant.locations.values())

        # * get most commoness by LocationCommonEnum
        commoness = sorted(commoness, key=lambda x: LocationCommonEnum(x).value)
        # * set default value (latest one)
        commoness = commoness[0] if commoness else "שכיחות לא ידועה"
        __pydantic_self__.commoness = commoness


class SearchOutList(BaseModel):
    total: int = 0
    total_pages: int = 1
    current_page: int = 1
    plants: List[Optional[SearchOut]] = []

    @validator("plants")
    def sort_plants_image(cls, v):
        """
        sort plants by image and commoness
        """

        # * sort plants by image first
        plants = sorted(v, key=lambda x: x.image if x.image else "", reverse=True)

        # * sort plants_with_images and plants_without_images by commoness by LocationCommonEnum
        plants.sort(key=lambda x: LocationCommonEnum(x.commoness).value)

        # * remove key 'commoness' from each plant (after sorting) - canceled because UI group by commoness
        # TODO: remove this after UI group by commoness
        # for plant in plants:
        #     del plant.commoness

        return plants
