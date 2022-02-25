from pydantic import BaseModel, Field, validator
from enum import IntEnum
from PIL import Image
from fastapi import HTTPException
from models.helpers import gen_uuid
from models.custom_types import LocationHebLiteral, ImageContentCategoryLiteral
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


class AngleEnum(IntEnum):
    L = Image.ROTATE_90
    R = Image.ROTATE_270


class RotateDirection(BaseModel):
    angle: Literal["L", "R"] = Field(
        example="R", description="Rotation direction, R or L"
    )


class Coordinates(BaseModel):
    lat: float = Field(example=33.106251, description="latitude")
    lon: float = Field(example=35.719422, description="longitude")
    alt: float | None = Field(default=None, description="altitude")


class ImageLocationText(BaseModel):
    location_name: LocationHebLiteral | None = None


class ImageLocation(ImageLocationText):
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
    content_category: ImageContentCategoryLiteral | None
