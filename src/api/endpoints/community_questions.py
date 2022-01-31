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
    QuestionImageInDB,
    Question,
    QuestionInDB,
    QuestionInResponse,
    ImagesInResponse,
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


# TODO: delete image from question
# TODO: answer question
# TODO: delete question ?
# TODO: rotate image
# TODO: format file


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
    for image in question.images:
        image.file_name = gen_image_file_name(image.orig_file_name)
    questionInDB = QuestionInDB(**question.dict(), user_id=current_user.user_id)
    db.questions.insert_one(questionInDB.dict())
    return QuestionInResponse(
        question_id=questionInDB.question_id,
        images_gen_names=[x.file_name for x in question.images],
    )


# TODO: add image to question
@router.post("/{question_id}/images_metadata", response_model=ImagesInResponse)
async def add_image_metadata_to_question(
    question_id: str,
    images_metadata: List[QuestionImage],
    db: MongoClient = Depends(db.get_db),
    user: user_model.User = Depends(get_current_active_user),
):
    question = db.questions.find_one({"question_id": question_id})
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    if question["user_id"] != user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    for image in images_metadata:
        image.file_name = gen_image_file_name(image.orig_file_name)

    db.questions.update_one(
        {"question_id": question_id},
        {
            "$push": {
                "images": {
                    "$each": [
                        QuestionImageInDB(**x.dict()).dict() for x in images_metadata
                    ]
                }
            }
        },
    )
    return ImagesInResponse(images_gen_names=[x.file_name for x in images_metadata])


@router.post("/{question_id}/images")
async def add_image_to_question(
    question_id: str,
    images_gen_names: List[str],
    images: List[UploadFile] = File(...),
    current_user: user_model.User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    question = db.questions.find_one({"question_id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if question["user_id"] != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this question")
    if len(images) != len(images_gen_names):
        raise HTTPException(status_code=400, detail="Images and names mismatch")

    for image, file_name in zip(images, images_gen_names):
        # * each image must have a unique name

        # * check if image metadata exists and not been uploaded. before uploading image
        if not db.questions.find_one(
            {"images": {"$elemMatch": {"file_name": file_name, "uploaded": False}}}
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Image not found or already been uploaded - {file_name}",
            )

        blob = bucket.blob("questions/" + file_name)
        blob.upload_from_file(image.file, content_type=image.content_type)
        db.questions.update_one(
            {"question_id": question_id, "images.file_name": file_name},
            {
                "$set": {
                    "images.$.uploaded": True,
                    "images.$.self_link": blob.self_link,
                    "images.$.media_link": blob.media_link,
                    "images.$.public_url": blob.public_url,
                }
            },
        )
    return Response(status_code=200)
