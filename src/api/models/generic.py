from pydantic import BaseModel, Field, validator
from enum import IntEnum, Enum
from PIL import Image
from endpoints.helpers_tools.GPS_translate import find_point_location
from models.plant import LocationKMLtranslate
from fastapi import HTTPException
from models.helpers import gen_uuid
from models.custom_types import MonthHebLiteral, LocationHebLiteral
from datetime import datetime
from typing import Literal


class GPSTranslateOut(BaseModel):
    location: str = Field(..., description="Location name, in DB")

    @validator("location", pre=True, always=True)
    def set_location(cls, v):
        if not v:
            raise HTTPException(
                status_code=404,
                detail="location not found",
            )
        return v


class AngleEnum(IntEnum):
    L = Image.ROTATE_90
    R = Image.ROTATE_270


class RotateDirection(BaseModel):
    angle: Literal["L", "R"] = Field(
        default="R", description="Rotation direction, R or L"
    )


class WhatInImage(str, Enum):
    """
    for user to specify what is in the image
    """

    a = "הצמח במלואו"
    b = "פרי"
    c = "פרח"
    d = "עלים"
    e = "זרעים"
    f = "הצמח בבית הגידול"
    g = "לא נבחר"


class Coordinates(BaseModel):
    lat: float = Field(default=33.106251, description="latitude")
    lon: float = Field(default=35.719422, description="longitude")
    alt: float | None = Field(default=None, description="altitude")


class ImageLocationText(BaseModel):
    # TODO: set type to LocationHebLiteral
    location_name: str | None = None


# class ImageLocation(Coordinates):
class ImageLocation(ImageLocationText):
    # TODO: refactor later
    coordinates: Coordinates | None = None

    # @validator("location_name", always=True, pre=True)
    # def validate_location_name(cls, v, values):
    #     print(f"values: {values}")
    #     kml_location = find_point_location(
    #         (values.get("lon"), values.get("lat"))
    #     )
    #     if kml_location:
    #         return LocationKMLtranslate[kml_location].value


class Comment(BaseModel):
    comment_text: str


class CommentInDB(Comment):
    comment_id: str = Field(default_factory=gen_uuid)
    comment_dt: datetime = Field(default_factory=datetime.utcnow)
    user_id: str


class ImagePreview(BaseModel):
    # TODO: link to thumbnail
    file_name: str
    what_in_image: WhatInImage | None
