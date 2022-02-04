from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    Response,
    Query,
)
from typing import List
import db
from pymongo.mongo_client import MongoClient
from models.user_questions import (
    CommentInDB,
    QuestionImage,
    Question,
    QuestionInDB,
    QuestionImageInDB,
    QuestionInResponse,
    ImagesInResponse,
    Comment,
    Answer,
    AnswerInDB,
)
import models.user as user_model
from core.security import get_current_active_user, get_current_privilege_user
from core.gstorage import bucket

router = APIRouter(prefix="/questions", tags=["questions"])


# * questions dependencies
async def validate_question_by_id(
    question_id: str, db: MongoClient = Depends(db.get_db)
) -> str:
    if not db.questions.find_one({"question_id": question_id}, {"question_id": 1}):
        raise HTTPException(status_code=404, detail="Question not found")
    return question_id


async def get_current_question(
    question_id: str = Depends(validate_question_by_id),
    db: MongoClient = Depends(db.get_db),
) -> dict:
    question = db.questions.find_one({"question_id": question_id})
    return QuestionInDB(**question)


async def validate_user_is_question_owner(
    question: QuestionInDB = Depends(get_current_question),
    user: user_model.User = Depends(get_current_active_user),
):
    if user.user_id != question.user_id:
        raise HTTPException(
            status_code=403, detail="User is not owner of this question"
        )
    return user


# * end of questions dependencies


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
    question: QuestionInDB = Depends(get_current_question),
):
    return question


# TODO: delete question ?
# TODO: rotate image
# TODO: format file


# TODO: add comment to question
@router.post("/{question_id}/comments", response_model=Comment)
def add_comment(
    comment: Comment,
    question_id: str = Depends(validate_question_by_id),
    db: MongoClient = Depends(db.get_db),
    user: user_model.User = Depends(get_current_active_user),
):
    comment_data = CommentInDB(user_id=user.user_id, **comment.dict())
    db.questions.update_one(
        {"question_id": question_id}, {"$push": {"comments": comment_data.dict()}}
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
    return QuestionInResponse(
        question_id=questionInDB.question_id,
        images_ids=list(map(lambda x: x.image_id, questionInDB.images)),
    )


# TODO: add image to question
@router.post("/{question_id}/images_metadata", response_model=ImagesInResponse)
async def add_image_metadata_to_question(
    images_metadata: List[QuestionImage],
    question: QuestionInDB = Depends(get_current_question),
    db: MongoClient = Depends(db.get_db),
    user: user_model.User = Depends(validate_user_is_question_owner),
):
    images_metadata_for_db = [
        QuestionImageInDB(**x.dict()).dict() for x in images_metadata
    ]

    db.questions.update_one(
        {"question_id": question.question_id},
        {"$push": {"images": {"$each": images_metadata_for_db}}},
    )
    return ImagesInResponse(images_ids=[x["image_id"] for x in images_metadata_for_db])


@router.post("/{question_id}/images")
async def add_image_to_question(
    # question_id: str,
    images_ids: List[str],
    question: QuestionInDB = Depends(get_current_question),
    images: List[UploadFile] = File(...),
    current_user: user_model.User = Depends(validate_user_is_question_owner),
    db: MongoClient = Depends(db.get_db),
):
    if len(images) != len(images_ids):
        raise HTTPException(status_code=400, detail="Images and ids mismatch")

    for image, image_id in zip(images, images_ids):
        # * get image metadata
        image_data = list(
            filter(
                lambda image: image.image_id == image_id and not image.uploaded,
                question.images,
            )
        )

        # * check if image metadata exists and not been uploaded
        if not image_data:
            raise HTTPException(
                status_code=400,
                detail=f"Image metadata not found or already been uploaded - {image_id}",
            )

        # * upload image to gstorage
        file_name = image_data[0].file_name
        blob = bucket.blob("questions/" + file_name)
        blob.upload_from_file(image.file, content_type=image.content_type)

        # * update image metadata
        db.questions.update_one(
            {"question_id": question.question_id, "images.image_id": image_id},
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


@router.delete("/{question_id}/images/{image_id}")
async def delete_image_from_question(
    image_id: str,
    question: str = Depends(get_current_question),
    current_user: user_model.User = Depends(validate_user_is_question_owner),
    db: MongoClient = Depends(db.get_db),
):
    # TODO: also admin and editor should be able to delete image
    # * get image metadata
    image_data = list(filter(lambda image: image.image_id == image_id, question.images))

    # * check if image metadata exists
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    image_data = image_data[0]

    # * delete image from storage
    blob = bucket.blob("questions/" + image_data.file_name)
    blob.delete()

    # * delete image metadata from question
    db.questions.update_one(
        {"question_id": question.question_id},
        {"$pull": {"images": {"image_id": image_id, "uploaded": True}}},
    )
    return Response(status_code=200)


@router.post("/{question_id}/answer")
async def answer_question(
    answer: Answer,
    question_id: str = Depends(validate_question_by_id),
    current_user: user_model.User = Depends(get_current_privilege_user),
    db: MongoClient = Depends(db.get_db),
):
    # TODO: replace with dependency
    if not db.plants.find_one({"plant_id": answer.plant_id}):
        raise HTTPException(status_code=404, detail="Plant not found")

    answerInDB = AnswerInDB(**answer.dict(), user_id=current_user.user_id)
    db.questions.update_one(
        {"question_id": question_id}, {"$set": {"answer": answerInDB.dict()}}
    )
    return Response(status_code=200)
