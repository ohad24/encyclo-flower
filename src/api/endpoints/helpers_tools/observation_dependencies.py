from db import get_db
from pymongo.database import Database
from fastapi import HTTPException, Depends
from models.user import UserInDB
from models.user_observations import (
    ObservationOut,
    ObservationImageInDB_w_oid,
    ObservationImageInDB,
)
from models.exceptions import (
    ExceptionObservationImageNotFound,
    ExceptionObservationNotFound,
)
from core.security import get_current_active_user, check_privilege_user
from endpoints.helpers_tools.db import prepare_aggregate_pipeline_w_users


async def validate_observation_by_id(
    observation_id: str, db: Database = Depends(get_db)
) -> ObservationOut:
    query_filter = dict(observation_id=observation_id, deleted=False)
    pipeline = prepare_aggregate_pipeline_w_users(query_filter, 0, 1)
    observation = next(db.observations.aggregate(pipeline), None)
    if not observation:
        raise HTTPException(
            status_code=404, detail=ExceptionObservationNotFound().detail
        )
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
    user: UserInDB = Depends(get_current_active_user),
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
    user: UserInDB = Depends(get_current_active_user),
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
    # TODO: merge with questions
    # TODO: remove ObservationImageInDB_w_oid (like in questions)
    # TODO: merge all community image dependencies
    image_data = next(
        (image for image in observation.images if image.image_id == image_id), None
    )
    if not image_data:
        raise HTTPException(
            status_code=404, detail=ExceptionObservationImageNotFound().detail
        )
    return ObservationImageInDB_w_oid(
        observation_id=observation.observation_id, image=image_data
    )


async def get_image_data_oid_w_valid_editor(
    image_data: ObservationImageInDB_w_oid = Depends(validate_image_by_id),
) -> ObservationImageInDB_w_oid:
    return image_data


async def get_image_data_w_valid_editor(
    image_data: ObservationImageInDB = Depends(validate_image_by_id),
) -> ObservationImageInDB:
    return image_data.image
