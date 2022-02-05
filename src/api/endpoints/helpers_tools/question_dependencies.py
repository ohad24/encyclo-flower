import db
from pymongo.mongo_client import MongoClient
from fastapi import HTTPException, Depends
import models.user as user_model
from models.user_questions import QuestionInDB, QuestionImageInDB
from core.security import get_current_active_user, check_privilege_user


async def validate_question_by_id(
    question_id: str, db: MongoClient = Depends(db.get_db)
) -> QuestionInDB:
    question = db.questions.find_one({"question_id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
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
    user: user_model.User = Depends(get_current_active_user),
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
    user: user_model.User = Depends(get_current_active_user),
) -> QuestionInDB:
    """
    valid editor is the question owner or an admin/editor
    """
    if not user.user_id == question.user_id and not check_privilege_user(user):
        raise HTTPException(
            status_code=403, detail="User is not owner or editor of this question"
        )
    return question


async def get_image_data_from_question(
    image_id: str,
    question: QuestionInDB = Depends(get_current_question_w_valid_editor),
) -> QuestionImageInDB:
    image_data = list(filter(lambda image: image.image_id == image_id, question.images))
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    return image_data[0]
