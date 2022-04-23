from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from models.helpers import observation_id_generator
from models.generic import ImagePreview, CommunityImageInDB, CommunityImageMetadata
from models.user import BaseUserOut


class Observation(BaseModel):
    observation_text: str = Field(min_length=5, max_length=2000)


class ObservationInResponse(BaseModel):
    """
    response for added new observation.
    """

    observation_id: str


class ObservationImageMeta(CommunityImageMetadata):
    plant_id: Optional[None | str] = Field(
        None,
        example=None,
        description="Plant ID",
        nullable=True,
    )


class ObservationImageInDB(CommunityImageInDB, ObservationImageMeta):
    pass


class ObservationImageOut(ObservationImageMeta):
    image_id: str
    file_name: str


class ObservationImageInDB_w_oid(BaseModel):
    observation_id: str
    image: ObservationImageMeta


class ObservationInDB(Observation):
    observation_id: str = Field(default_factory=observation_id_generator)
    images: List[ObservationImageInDB] = []
    user_id: str
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    submitted: bool = False
    deleted: bool = False


class ObservationOut(ObservationInDB):
    user_data: BaseUserOut


class ObservationPreviewBase(BaseModel):
    observation_id: str
    observation_text: str
    image: ImagePreview | None
    created_dt: datetime


class ObservationsPreview(ObservationPreviewBase):
    user_id: str
    username: str
