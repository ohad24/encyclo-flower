import db
from pymongo.mongo_client import MongoClient
from fastapi import HTTPException, Depends
from models.user import User
from models.user_observations import (
    ObservationOut,
    ObservationImageInDB_w_oid,
    ObservationImageInDB,
)
from models.generic import ExceptionResponse
from core.security import get_current_active_user, check_privilege_user
from endpoints.helpers_tools.db import prepare_aggregate_pipeline_w_users


# TODO: show responses options in the documentation (POC in add image to observation)
# https://fastapi.tiangolo.com/advanced/additional-responses/?h=responses#combine-predefined-responses-and-custom-ones
# * cant use multi status code in fastapi (?)
responses = {
    404: {"description": "Observation not found", "model": ExceptionResponse},
    #   {"description": "Image not found", "model": ExceptionResponse}],
}


async def validate_observation_by_id(
    observation_id: str, db: MongoClient = Depends(db.get_db)
) -> ObservationOut:
    query_filter = dict(observation_id=observation_id, deleted=False)
    pipeline = prepare_aggregate_pipeline_w_users(query_filter, 0, 1)
    observation = next(db.observations.aggregate(pipeline), None)
    if not observation:
        raise HTTPException(status_code=404, detail=responses[404]["description"])
    observation["user_data"] = observation["user_data"][0]
    return ObservationOut(**observation)


async def get_observation_id(
    observation: ObservationOut = Depends(validate_observation_by_id),
) -> str:
    return observation.observation_id


async def get_current_observation(
    observation: ObservationOut = Depends(validate_observation_by_id),
) -> ObservationOut:
    return observation


async def validate_user_is_observation_owner(
    user: User = Depends(get_current_active_user),
    observation: ObservationOut = Depends(get_current_observation),
) -> ObservationOut:
    if user.user_id != observation.user_id:
        raise HTTPException(
            status_code=403, detail="User is not owner of this observation"
        )
    return observation


async def get_current_observation_w_valid_owner(
    observation: ObservationOut = Depends(validate_user_is_observation_owner),
) -> ObservationOut:
    return observation


async def get_current_observation_w_valid_editor(
    user: User = Depends(get_current_active_user),
    observation: ObservationOut = Depends(get_current_observation),
) -> ObservationOut:
    """
    valid editor is the observation owner or an admin/editor
    """
    if not user.user_id == observation.user_id and not check_privilege_user(user):
        raise HTTPException(
            status_code=403, detail="User is not owner or editor of this observation"
        )
    return observation


async def validate_image_by_id(
    image_id: str,
    observation: ObservationOut = Depends(get_current_observation_w_valid_editor),
) -> ObservationImageInDB_w_oid:
    image_data = list(
        filter(lambda image: image.image_id == image_id, observation.images)
    )
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    return ObservationImageInDB_w_oid(
        observation_id=observation.observation_id, image=image_data[0]
    )


async def get_image_data_oid_w_valid_editor(
    image_data: ObservationImageInDB_w_oid = Depends(validate_image_by_id),
) -> ObservationImageInDB_w_oid:
    return image_data


async def get_image_data_w_valid_editor(
    image_data: ObservationImageInDB = Depends(validate_image_by_id),
) -> ObservationImageInDB:
    return image_data.image