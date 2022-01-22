from fastapi import APIRouter, Depends, File, UploadFile, Form, Body, Request
from typing import List, Any, Union
import db
from pymongo.mongo_client import MongoClient
from google.cloud import storage
from models.user_questions import QuestionImage, Question, QuestionInDB
import models.user as user_model
from core.security import get_current_active_user

router = APIRouter()

storage_client = storage.Client()

# TODO: get one question
# TODO: get all questions
# TODO: add image to question
# TODO: delete image from question
# TODO: answer question
# TODO: delete question ?
# TODO: add comment to question

@router.post("/questions")
async def ask_question(
    question: Question,
    current_user: user_model.User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    questionInDB = QuestionInDB(**question.dict(), user_id=current_user.user_id)
    db.questions.insert_one(questionInDB.dict())
    return {"question_id": questionInDB.question_id}
