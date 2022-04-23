from db import get_db
from pymongo.mongo_client import MongoClient
from fastapi import HTTPException, Depends
from models.user import UserInDB
from models.user_questions import (
    QuestionImageInDB,
    QuestionOut,
    AnswerPlantData,
)
from models.plant import Plant
from core.security import get_current_active_user, check_privilege_user
from endpoints.helpers_tools.db import prepare_aggregate_pipeline_w_users
from endpoints.helpers_tools.plant_dependencies import get_plant_from_science_name
from models.exceptions import (
    ExceptionQuestionNotFound,
    ExceptionQuestionUserIsNotOwner,
    ExceptionQuestionUserIsNotValidEditor,
    ExceptionQuestionImageNotFound,
)


async def validate_question_by_id(
    question_id: str, db: MongoClient = Depends(get_db)
) -> QuestionOut:
    query_filter = dict(question_id=question_id, deleted=False)
    pipeline = prepare_aggregate_pipeline_w_users(query_filter, 0, 1)
    question = next(db.questions.aggregate(pipeline), None)
    if not question:
        raise HTTPException(status_code=404, detail=ExceptionQuestionNotFound().detail)
    return QuestionOut(**question)


async def get_question_id(
    question: QuestionOut = Depends(validate_question_by_id),
) -> str:
    return question.question_id


async def get_current_question(
    question: QuestionOut = Depends(validate_question_by_id),
) -> QuestionOut:
    return question


async def validate_user_is_question_owner(
    question: QuestionOut = Depends(get_current_question),
    user: UserInDB = Depends(get_current_active_user),
) -> QuestionOut:
    if user.user_id != question.user_id:
        raise HTTPException(
            status_code=403, detail=ExceptionQuestionUserIsNotOwner().detail
        )
    return question


async def get_current_question_w_valid_owner(
    question: QuestionOut = Depends(validate_user_is_question_owner),
) -> QuestionOut:
    return question


async def get_current_question_w_valid_editor(
    question: QuestionOut = Depends(get_current_question),
    user: UserInDB = Depends(get_current_active_user),
) -> QuestionOut:
    """
    valid editor is the question owner or an admin/editor
    """
    if not user.user_id == question.user_id and not check_privilege_user(user):
        raise HTTPException(
            status_code=403, detail=ExceptionQuestionUserIsNotValidEditor().detail
        )
    return question


async def validate_image_by_id(
    image_id: str,
    question: QuestionOut = Depends(get_current_question_w_valid_editor),
) -> QuestionImageInDB:
    image_data = next(
        (image for image in question.images if image.image_id == image_id), None
    )
    if not image_data:
        raise HTTPException(
            status_code=404, detail=ExceptionQuestionImageNotFound().detail
        )
    return image_data


async def get_image_data_w_valid_editor(
    image_data: QuestionImageInDB = Depends(validate_image_by_id),
) -> QuestionImageInDB:
    return image_data


async def get_answer_data(
    plant: Plant = Depends(get_plant_from_science_name),
) -> AnswerPlantData:
    return AnswerPlantData(**plant.dict())
