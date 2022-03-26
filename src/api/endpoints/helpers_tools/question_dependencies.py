import db
from pymongo.mongo_client import MongoClient
from fastapi import HTTPException, Depends
from models.user import UserInDB
from models.user_questions import (
    QuestionInDB,
    QuestionImageInDB,
    QuestionImageInDB_w_qid,
)
from core.security import get_current_active_user, check_privilege_user
from endpoints.helpers_tools.db import prepare_aggregate_pipeline_w_users


async def validate_question_by_id(
    question_id: str, db: MongoClient = Depends(db.get_db)
) -> QuestionInDB:
    query_filter = dict(question_id=question_id, deleted=False)
    pipeline = prepare_aggregate_pipeline_w_users(query_filter, 0, 1)
    question = next(db.questions.aggregate(pipeline), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if question["user_data"]:
        # TODO: this if because TestQuestion::test_delete_image_as_editor isn't configured correctly, remove after fixing
        question["user_data"] = question["user_data"][0]
    else:
        question["user_data"] = None
    return QuestionInDB(**question)


async def get_question_id(
    question: QuestionInDB = Depends(validate_question_by_id),
) -> str:
    return question.question_id


async def get_current_question(
    question: QuestionInDB = Depends(validate_question_by_id),
) -> QuestionInDB:
    return question


async def validate_user_is_question_owner(
    question: QuestionInDB = Depends(get_current_question),
    user: UserInDB = Depends(get_current_active_user),
) -> QuestionInDB:
    if user.user_id != question.user_id:
        raise HTTPException(
            status_code=403, detail="User is not owner of this question"
        )
    return question


async def get_current_question_w_valid_owner(
    question: QuestionInDB = Depends(validate_user_is_question_owner),
) -> QuestionInDB:
    return question


async def get_current_question_w_valid_editor(
    question: QuestionInDB = Depends(get_current_question),
    user: UserInDB = Depends(get_current_active_user),
) -> QuestionInDB:
    """
    valid editor is the question owner or an admin/editor
    """
    if not user.user_id == question.user_id and not check_privilege_user(user):
        raise HTTPException(
            status_code=403, detail="User is not owner or editor of this question"
        )
    return question


async def validate_image_by_id(
    image_id: str,
    question: QuestionInDB = Depends(get_current_question_w_valid_editor),
) -> QuestionImageInDB_w_qid:
    image_data = list(filter(lambda image: image.image_id == image_id, question.images))
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    return QuestionImageInDB_w_qid(
        question_id=question.question_id, image=image_data[0]
    )


async def get_image_data_qid_w_valid_editor(
    image_data: QuestionImageInDB_w_qid = Depends(validate_image_by_id),
) -> QuestionImageInDB_w_qid:
    return image_data


async def get_image_data_w_valid_editor(
    image_data: QuestionImageInDB = Depends(validate_image_by_id),
) -> QuestionImageInDB:
    return image_data.image
