from pydantic import BaseModel, Field, AnyUrl, validator
from typing import Dict, List, Optional
from datetime import datetime
from models.plant_custom_types import (
    LocationCommonEnum,
    COLORS,
    PETALS,
    LEAF_SHAPES,
    LEAF_EDGES,
    LEAF_ARRANGEMENTS,
    STEM_SHAPES,
    LIFE_FORMS,
    HABITATS,
    SEX_FLOWER,
    SPINE,
)
from models.plant_taxonomy_custom_types import (
    CLADE1,
    CLADE2,
    CLADE3,
    FAMILY,
    SUBFAMILY,
    GENUS,
)
from models.custom_types import LocationHebLiteral
from core.config import get_settings

settings = get_settings()


class Taxonomy(BaseModel):
    clade1: CLADE1
    clade2: CLADE2
    clade3: Optional[CLADE3]
    clade4: Optional[str]
    family: FAMILY
    subfamily: Optional[SUBFAMILY]
    genus: GENUS


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
        """
        Because the level in DB is null by default
        """
        return level or "e"


class PlantLocation(BaseModel):
    # TODO: refactor this class
    location_name: LocationHebLiteral = Field(description="Hebrew name of the location")
    commoness: LocationCommonEnum | None

    @validator("commoness", pre=True, always=True)
    def set_location_common(cls, v):
        if v:
            return LocationCommonEnum(v).value
        return None


class Plant(BaseModel):
    science_name: str
    heb_name: str
    fam_name_eng: Optional[str]
    petals: Optional[PETALS]
    leaf_shapes: List[LEAF_SHAPES]
    leaf_edges: List[LEAF_EDGES]
    leaf_arrangements: List[LEAF_ARRANGEMENTS]
    stem_shapes: Optional[STEM_SHAPES]
    life_forms: List[LIFE_FORMS]
    description: Optional[str]
    protected: bool
    red: bool
    invasive: bool
    synonym_names_eng: List[str]
    synonym_names_heb: List[str]
    locations: List[PlantLocation]
    habitats: List[HABITATS]
    flowering_seasons: Optional[List[int]]
    colors: List[COLORS]
    sex_flower: List[SEX_FLOWER]
    danger: bool
    rare: bool
    taxon: Taxonomy
    spine: List[SPINE]
    images: List[Optional[PlantImage]]


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

        commoness = set([x.commoness.value for x in plant.locations])

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


class PreSearchData(BaseModel):
    documents_count: int
    query: dict
    total_pages: int
    current_page: int
    per_page: int = settings.ITEMS_PER_PAGE
