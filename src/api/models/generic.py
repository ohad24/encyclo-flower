from pydantic import BaseModel, Field, validator
from enum import IntEnum
from PIL import Image


class GPSTranslateOut(BaseModel):
    location: str


class AngleEnum(IntEnum):
    L = Image.ROTATE_90
    R = Image.ROTATE_270


class RotateDirection(BaseModel):
    angle: str = Field(default="R", description="Rotation direction, R or L")

    @validator("angle")
    def validate_angle(cls, v):
        if v not in list(x.name for x in AngleEnum):
            raise ValueError(f"{v} is not a valid angle")
        return v
