from pydantic import BaseModel, Field, validator
from enum import Enum
from PIL import Image
from fastapi import HTTPException
from models.helpers import gen_uuid, gen_image_file_name
from models.custom_types import (
    LocationHebLiteral,
    ImageContentCategoryLiteral,
    HebMonthLiteral,
)
from models.user import BaseUserOut
from datetime import datetime
from typing import Literal


class GPSTranslateOut(BaseModel):
    location: LocationHebLiteral = Field(description="Location name, in DB")

    @validator("location", pre=True, always=True)
    def set_location(cls, v):
        if not v:
            raise HTTPException(
                status_code=404,
                detail="location not found",
            )
        return v


class AngleEnum(Enum):
    L = Image.Transpose.ROTATE_90
    R = Image.Transpose.ROTATE_270


class RotateDirection(BaseModel):
    angle: Literal["L", "R"] = Field(
        example="R", description="Rotation direction, R or L"
    )


class Coordinates(BaseModel):
    lat: float = Field(example=33.106251, description="latitude")
    lon: float = Field(example=35.719422, description="longitude")
    alt: float | None = Field(default=None, description="altitude")


class ImageLocation(BaseModel):
    coordinates: Coordinates | None = None
    location_name: LocationHebLiteral | None = None


class Comment(BaseModel):
    comment_text: str


class CommentInDB(Comment):
    comment_id: str = Field(default_factory=gen_uuid)
    create_dt: datetime = Field(default_factory=datetime.utcnow)
    type: Literal["observation", "question"]
    object_id: str
    user_id: str


class CommentOut(Comment):
    comment_id: str
    create_dt: datetime
    user_data: BaseUserOut


class ImagePreview(BaseModel):
    # TODO: link to thumbnail
    file_name: str
    created_dt: datetime
    content_category: ImageContentCategoryLiteral | None = None


class LocationKMLtranslate(Enum):
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


class CommunityImageMetadata(BaseModel):
    """Images uploaded by community members in observations and questions"""

    description: str | None = None
    content_category: ImageContentCategoryLiteral | None = None
    location_name: LocationHebLiteral | None = None
    month_taken: HebMonthLiteral | None = Field(
        None, description="Hebrew month"
    )


class CommunityImageInDB(BaseModel):
    """Images uploaded by community members in observations and questions"""

    image_id: str = Field(default_factory=gen_uuid)
    coordinates: Coordinates = Coordinates(lat=0, lon=0, alt=0)
    orig_file_name: str = Field(default="image1.jpg")
    file_name: str | None = None
    created_dt: datetime = Field(default_factory=datetime.utcnow)

    @validator("file_name", pre=True, always=True)
    def set_file_name(cls, v, values):
        if not v:
            return gen_image_file_name(values["orig_file_name"])
        return v
