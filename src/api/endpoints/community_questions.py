from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Form,
    Body,
    Request,
    HTTPException,
    Response,
)
from typing import List, Any, Union
import db
from pymongo.mongo_client import MongoClient
from google.cloud import storage
from models.user_questions import (
    QuestionImage,
    Question,
    QuestionInDB,
    QuestionInResponse,
)
import models.user as user_model
from core.security import get_current_active_user
from endpoints.helpers_tools.generic import gen_image_file_name
from core.gstorage import bucket

router = APIRouter()

storage_client = storage.Client()

# TODO: get one question
# TODO: get all questions
# TODO: add image to question
# TODO: delete image from question
# TODO: answer question
# TODO: delete question ?
# TODO: add comment to question


@router.post("/questions", response_model=QuestionInResponse)
async def ask_question(
    question: Question,
    current_user: user_model.User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    questionInDB = QuestionInDB(**question.dict(), user_id=current_user.user_id)
    db.questions.insert_one(questionInDB.dict())
    return {"question_id": questionInDB.question_id}


@router.post("/questions/{question_id}/images")
async def add_image_to_question(
    question_id: str,
    images: List[UploadFile] = File(...),
    current_user: user_model.User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    question = db.questions.find_one({"question_id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if question["user_id"] != current_user.user_id:
        raise HTTPException(status_code=400, detail="Not allowed to edit this question")

    for image in images:
        # * each image must have a unique name
        new_file_name = gen_image_file_name(image.filename)
        db.questions.update_one(
            {"question_id": question_id, "images.orig_file_name": image.filename},
            {"$set": {"images.$.file_name": new_file_name}},
        )
        blob = bucket.blob("questions/" + new_file_name)
        blob.upload_from_file(image.file, content_type=image.content_type)
    return Response(status_code=200)
