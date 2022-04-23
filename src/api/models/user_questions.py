from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime
from models.helpers import question_id_generator
from models.generic import ImagePreview, CommunityImageInDB, CommunityImageMetadata
from models.user import BaseUserOut
from models.custom_types import AnswerFilterLiteral


class QuestionImageMetadata(CommunityImageMetadata):
    pass


class QuestionImageInDB(CommunityImageInDB, QuestionImageMetadata):
    pass


class ObservationImageOut(QuestionImageMetadata):
    image_id: str
    file_name: str


class QuestionImageInDB_w_qid(BaseModel):
    question_id: str
    image: QuestionImageInDB


class Question(BaseModel):
    question_text: str = Field(min_length=5, max_length=1000)


class Answer(BaseModel):
    """User Input"""

    science_name: str


class AnswerPlantData(Answer):
    """Addition data for answer (plant)"""

    heb_name: str
    plant_id: str


class AnswerInDB(AnswerPlantData):
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


class QuestionOut(QuestionInDB):
    user_data: BaseUserOut


class QuestionPreviewBase(BaseModel):
    question_id: str
    question_text: str
    answer: Optional[AnswerInDB]
    image: Optional[ImagePreview]
    created_dt: datetime


class QuestionPreview(QuestionPreviewBase):
    user_id: str
    username: str


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
