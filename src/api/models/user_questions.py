from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional
from enum import Enum
from datetime import datetime
from models.helpers import question_id_generator, gen_uuid, gen_image_file_name


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
    description: str | None = None
    notes: str | None = None
    what_in_image: WhatInImage
    location: Optional[ImageLocation]
    photo_taken_dt: Optional[datetime]


class QuestionImageInDB(QuestionImage):
    image_id: str = Field(default_factory=gen_uuid)
    file_name: str | None = None
    uploaded: bool = False
    self_link: HttpUrl | None = None
    media_link: HttpUrl | None = None
    public_url: HttpUrl | None = None

    @validator("file_name", pre=True, always=True)
    def set_file_name(cls, v, values):
        if not v:
            return gen_image_file_name(values["orig_file_name"])
        return v


class QuestionImageInDB_w_qid(BaseModel):
    question_id: str
    image: QuestionImageInDB


class Comment(BaseModel):
    comment_text: str


class CommentInDB(Comment):
    comment_id: str = Field(default_factory=gen_uuid)
    comment_dt: datetime = Field(default_factory=datetime.utcnow)
    user_id: str


class Question(BaseModel):
    question_text: str = Field(min_length=5, max_length=1000)
    images: List[QuestionImage] = Field(description="Images metadata")


class Answer(BaseModel):
    plant_id: str


class AnswerInDB(Answer):
    answer_dt: datetime = Field(default_factory=datetime.utcnow)
    user_id: str


class QuestionInDB(Question):
    question_id: str = Field(default_factory=question_id_generator)
    user_id: str
    answer: Optional[AnswerInDB] = None
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    comments: List[Optional[CommentInDB]] = []
    images: List[QuestionImageInDB]
    deleted: bool = False


class ImagesInResponse(BaseModel):
    """
    response for added new images to question.
    """

    images_ids: List[str]


class QuestionInResponse(ImagesInResponse):
    """
    This is the response of the question creation
    """

    question_id: str
