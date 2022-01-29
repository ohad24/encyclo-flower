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
    Query,
)
from typing import List, Any, Union
import db
from pymongo.mongo_client import MongoClient
from google.cloud import storage
from models.user_questions import (
    CommentInDB,
    QuestionImage,
    Question,
    QuestionInDB,
    QuestionInResponse,
    Comment,
    CommentInDB,
)
import models.user as user_model
from core.security import get_current_active_user
from endpoints.helpers_tools.generic import gen_image_file_name
from core.gstorage import bucket

router = APIRouter(prefix="/questions", tags=["questions"])

storage_client = storage.Client()


# TODO: get all questions from db
@router.get("/", response_model=List[QuestionInDB])
async def get_all_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(9, le=9),
    db: MongoClient = Depends(db.get_db),
):
    # TODO: SET MORE RELEVANT FIELDS (NO COMMENTS, ONE IMAGE)
    questions = (
        db.questions.find({}, {"comments": 0})
        .sort("created_dt", -1)
        .limit(limit)
        .skip(skip)
    )
    return list(questions)


# TODO: get one question
@router.get("/{question_id}", response_model=QuestionInDB)
async def get_question(
    question_id: str,
    db: MongoClient = Depends(db.get_db),
):
    question = db.questions.find_one({"question_id": question_id})
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return QuestionInDB(**question)


# TODO: add image to question
# TODO: delete image from question
# TODO: answer question
# TODO: delete question ?
# TODO: rotate image


# TODO: add comment to question
@router.post("/{question_id}/comments", response_model=Comment)
def add_comment(
    question_id: str,
    comment: Comment,
    db: MongoClient = Depends(db.get_db),
    user: user_model.User = Depends(get_current_active_user),
):
    question = db.questions.find_one({"question_id": question_id})
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    data = CommentInDB(user_id=user.user_id, **comment.dict())
    db.questions.update_one(
        {"question_id": question_id}, {"$push": {"comments": data.dict()}}
    )
    return Response(status_code=200)


@router.post("/", response_model=QuestionInResponse)
async def ask_question(
    question: Question,
    current_user: user_model.User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    questionInDB = QuestionInDB(**question.dict(), user_id=current_user.user_id)
    db.questions.insert_one(questionInDB.dict())
    return {"question_id": questionInDB.question_id}


@router.post("/{question_id}/images")
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
