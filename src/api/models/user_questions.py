from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional, Dict
from datetime import datetime
from models.helpers import question_id_generator, gen_uuid, gen_image_file_name
from models.generic import CommentInDB, ImagePreview, Coordinates
from models.user import BaseUserOut
from models.custom_types import (
    ImageContentCategoryLiteral,
    AnswerFilterLiteral,
    HebMonthLiteral,
    LocationHebLiteral,
)


class QuestionImageMetadata(BaseModel):
    description: str | None = None
    content_category: ImageContentCategoryLiteral | None = None
    location_name: LocationHebLiteral | None = None
    month_taken: Optional[HebMonthLiteral | None] = Field(
        None, description="Hebrew month"
    )


class QuestionImageInDB(QuestionImageMetadata):
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


class ObservationImageOut(QuestionImageMetadata):
    image_id: str
    file_name: str


class QuestionImageInDB_w_qid(BaseModel):
    question_id: str
    image: QuestionImageInDB


class Question(BaseModel):
    question_text: str = Field(min_length=5, max_length=1000)
    # images: List[QuestionImage] = Field(description="Images metadata")


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
    images: List[QuestionImageInDB] = []
    submitted: bool = False
    deleted: bool = False
    # user_data: BaseUserOut | None = None


class QuestionPreviewBase(BaseModel):
    question_id: str
    question_text: str
    answer: Optional[AnswerInDB]
    image: Optional[ImagePreview]
    created_dt: datetime


class QuestionsPreview(QuestionPreviewBase):
    # TODO: fix class name to QuestionPreview
    user_id: str
    username: str


class ImagesInResponse(BaseModel):
    """
    response for added new images to question.
    """

    images_ids: List[str]


class QuestionInResponse(BaseModel):
    """
    This is the response of the question creation
    """

    question_id: str


class GetQuestionsFilterPreviewQuery(BaseModel):
    answer_filter_value: AnswerFilterLiteral
    answer_query: Dict = {"$or": []}

    @validator("answer_query", pre=True, always=True)
    def prepare_answer_query(cls, v, values) -> Dict:
        """query for answer filter. in db"""
        if values["answer_filter_value"] in ["answered", "all"]:
            v["$or"].append({"answer": {"$ne": None}})
        if values["answer_filter_value"] in ["not_answered", "all"]:
            v["$or"].append({"answer": {"$eq": None}})
        return v
