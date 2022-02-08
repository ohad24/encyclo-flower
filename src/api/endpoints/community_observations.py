from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    Response,
    Query,
)
from models.user_observations import Observation, ObservationInDB, ObservationInResponse
from models.user import User
from core.security import get_current_active_user, get_current_privilege_user
import db
from pymongo.mongo_client import MongoClient

router = APIRouter(prefix="/observations", tags=["observations"])

# TODO: edit observation
# TODO: delete observation
# TODO: add image to observation
# TODO: delete image from observation
# TODO: rotate image
# TODO: add comment to observation
# TODO: format file


# TODO: get all observations
@router.get("/")
async def get_all_observations():
    return "Hello World"


# TODO: create new observation
@router.post("/", response_model=ObservationInResponse)
async def add_observation(
    observation: Observation,
    user: User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    observationInDB = ObservationInDB(**observation.dict(), user_id=user.user_id)
    db.observations.insert_one(observationInDB.dict())
    return ObservationInResponse(observation_id=observationInDB.observation_id)
