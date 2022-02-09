import db
from pymongo.mongo_client import MongoClient
from fastapi import HTTPException, Depends
from models.user import User
from models.user_observations import (
    Observation,
    ObservationInDB,
    # QuestionImageInDB_w_qid,
)
from core.security import get_current_active_user, check_privilege_user


async def validate_observation_by_id(
    observation_id: str, db: MongoClient = Depends(db.get_db)
) -> ObservationInDB:
    observation = db.observations.find_one(
        {"observation_id": observation_id, "deleted": False}
    )
    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found")
    return ObservationInDB(**observation)


async def get_observation_id(
    observation: ObservationInDB = Depends(validate_observation_by_id),
) -> str:
    return observation.observation_id


async def get_current_observation(
    observation: ObservationInDB = Depends(validate_observation_by_id),
) -> ObservationInDB:
    return observation


async def validate_user_is_observation_owner(
    observation: ObservationInDB = Depends(get_current_observation),
    user: User = Depends(get_current_active_user),
) -> ObservationInDB:
    if user.user_id != observation.user_id:
        raise HTTPException(
            status_code=403, detail="User is not owner of this observation"
        )
    return observation


async def get_current_observation_w_valid_owner(
    observation: ObservationInDB = Depends(validate_user_is_observation_owner),
) -> ObservationInDB:
    return observation


# async def get_current_question_w_valid_editor(
#     question: QuestionInDB = Depends(get_current_question),
#     user: user_model.User = Depends(get_current_active_user),
# ) -> QuestionInDB:
#     """
#     valid editor is the question owner or an admin/editor
#     """
#     if not user.user_id == question.user_id and not check_privilege_user(user):
#         raise HTTPException(
#             status_code=403, detail="User is not owner or editor of this question"
#         )
#     return question


# async def validate_image_by_id(
#     image_id: str,
#     question: QuestionInDB = Depends(get_current_question_w_valid_editor),
# ) -> QuestionImageInDB_w_qid:
#     image_data = list(filter(lambda image: image.image_id == image_id, question.images))
#     if not image_data:
#         raise HTTPException(status_code=404, detail="Image not found")
#     return QuestionImageInDB_w_qid(
#         question_id=question.question_id, image=image_data[0]
#     )


# async def get_image_data_qid_w_valid_editor(
#     image_data: QuestionImageInDB_w_qid = Depends(validate_image_by_id),
# ) -> QuestionImageInDB_w_qid:
#     return image_data


# async def get_image_data_w_valid_editor(
#     image_data: QuestionImageInDB = Depends(validate_image_by_id),
# ) -> QuestionImageInDB:
#     return image_data.image
