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
    Answer,
    AnswerInDB,
)
import models.user as user_model
from core.security import get_current_active_user, get_current_privilege_user
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
        images_ids=[x.image_id for x in questionInDB.images],
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

    images_metadata_for_db = [
        QuestionImageInDB(**x.dict()).dict() for x in images_metadata
    ]

    db.questions.update_one(
        {"question_id": question_id},
        {"$push": {"images": {"$each": images_metadata_for_db}}},
    )
    return ImagesInResponse(images_ids=[x["image_id"] for x in images_metadata_for_db])


@router.post("/{question_id}/images")
async def add_image_to_question(
    question_id: str,
    images_ids: List[str],
    images: List[UploadFile] = File(...),
    current_user: user_model.User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    # TODO: change ids array to image_ids
    question = db.questions.find_one({"question_id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if question["user_id"] != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this question")
    if len(images) != len(images_ids):
        raise HTTPException(status_code=400, detail="Images and ids mismatch")

    for image, image_id in zip(images, images_ids):
        # * each image must have a unique name
        # * TODO: fix error text and logic

        question = db.questions.find_one(
            {"images": {"$elemMatch": {"image_id": image_id, "uploaded": False}}}
        )
        # * check if image metadata exists and not been uploaded. before uploading image
        if not question:
            raise HTTPException(
                status_code=400,
                detail=f"Image not found or already been uploaded - {image_id}",
            )
        image_data = list(
            filter(lambda image: image["image_id"] == image_id, question["images"])
        )
        if not image_data:
            raise HTTPException(
                status_code=400,
                detail=f"Image metadata not found not found or already been uploaded - {image_id}",
            )
        file_name = image_data[0]["file_name"]
        blob = bucket.blob("questions/" + file_name)
        blob.upload_from_file(image.file, content_type=image.content_type)
        db.questions.update_one(
            {"question_id": question_id, "images.image_id": image_id},
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


# TODO: delete image from question
@router.delete("/{question_id}/images/{image_id}")
async def delete_image_from_question(
    question_id: str,
    image_id: str,
    current_user: user_model.User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    # * get question data from db
    question = db.questions.find_one({"question_id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if question["user_id"] != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this question")

    # * check if image metadata exists
    image_data = list(
        filter(lambda image: image["image_id"] == image_id, question["images"])
    )
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    image_data = image_data[0]

    # * delete image from storage
    blob = bucket.blob("questions/" + image_data["file_name"])
    blob.delete()

    # * delete image metadata from question
    db.questions.update_one(
        {"question_id": question_id},
        {"$pull": {"images": {"image_id": image_id, "uploaded": True}}},
    )
    return Response(status_code=200)


# TODO: answer question
@router.post("/{question_id}/answer")
async def answer_question(
    question_id: str,
    answer: Answer,
    current_user: user_model.User = Depends(get_current_privilege_user),
    db: MongoClient = Depends(db.get_db),
):
    question = db.questions.find_one({"question_id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if not db.plants.find_one({"plant_id": answer.plant_id}):
        raise HTTPException(status_code=404, detail="Plant not found")

    answerInDB = AnswerInDB(**answer.dict(), user_id=current_user.user_id)
    db.questions.update_one(
        {"question_id": question_id}, {"$set": {"answer": answerInDB.dict()}}
    )
    return Response(status_code=200)
