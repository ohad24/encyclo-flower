from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from models.helpers import observation_id_generator


class Observation(BaseModel):
    observation_text: str


class ObservationInDB(Observation):
    observation_id: str = Field(default_factory=observation_id_generator)
    images: List = []  # TODO: add image class
    comments: List = []  # TODO: add comment class
    user_id: str
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    deleted: bool = False


class ObservationInResponse(BaseModel):
    """
    response for added new observation.
    """

    observation_id: str
