from pydantic import BaseModel, FileUrl, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime
from models.helpers import question_id_generator


class WhatInImage(str, Enum):
    a = "הצמח במלואו"
    b = "פרי"
    c = "פרח"
    d = "עלים"
    e = "זרעים"
    f = "הצמח בבית הגידול"
    g = "לא נבחר"


class ImageLocation(BaseModel):
    lat: float
    lon: float
    alt: float
    location_name: str | None


class QuestionImage(BaseModel):
    orig_file_name: str = Field(default="image1.jpg")
    file_name: str | None = None
    description: str | None = None
    notes: str | None = None
    what_in_image: WhatInImage
    location: Optional[ImageLocation]
    photo_taken_dt: Optional[datetime]


class Question(BaseModel):
    question_text: str
    images: List[QuestionImage] = Field(description="Images metadata")


class QuestionInDB(Question):
    question_id: str = Field(default_factory=question_id_generator)
    user_id: str


class QuestionInResponse(BaseModel):
    question_id: str
