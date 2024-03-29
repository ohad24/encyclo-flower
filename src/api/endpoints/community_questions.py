from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    Response,
    Query,
    BackgroundTasks,
)
from typing import List, Union
from db import get_db
from pymongo.database import Database
from models.user_questions import (
    QuestionImageMetadata,
    Question,
    QuestionInDB,
    QuestionImageInDB,
    QuestionInResponse,
    QuestionOut,
    AnswerInDB,
    QuestionPreview,
    GetQuestionsFilterPreviewQuery,
    AnswerFilterLiteral,
    ObservationImageOut,
    AnswerPlantData,
)
from models.user import UserInDB
from models.generic import RotateDirection, Comment, CommentInDB, CommentOut
from core.security import get_current_active_user, get_current_privilege_user
from endpoints.helpers_tools.question_dependencies import (
    get_question_id,
    get_current_question,
    get_current_question_w_valid_owner,
    get_image_data_w_valid_editor,
    get_answer_data,
    get_current_question_w_valid_editor,
)
from endpoints.helpers_tools.generic import (
    format_obj_image_preview,
    get_image_metadata,
    rotate_storage_image,
    create_thumbnail,
)
from endpoints.helpers_tools.db import (
    prepare_aggregate_pipeline_w_users,
    prepare_aggregate_pipeline_comments_w_users,
)
from endpoints.helpers_tools.common_dependencies import QuerySearchPageParams
from pathlib import Path
from endpoints.helpers_tools.storage import (
    upload_to_gstorage,
    delete_from_gstorage,
)
from models.exceptions import (
    ExceptionQuestionImageCountLimit,
    ExceptionQuestionNotFound,
    ExceptionQuestionUserIsNotOwner,
    ExceptionQuestionImageNotFound,
    ExceptionQuestionUserIsNotValidEditor,
    ExceptionUserNotPrivilege,
    ExceptionPlantNotFound,
)

router = APIRouter()

QUESTIONS_IMAGES_PATH = Path("questions")
QUESTION_THUMBNAILS_PATH = QUESTIONS_IMAGES_PATH / "thumbnails"


@router.get("/", response_model=List[QuestionPreview])
async def get_all_questions(
    answer_filter: AnswerFilterLiteral = Query(
        "all",
        description="Filter questions by answer status",
    ),
    search_params: QuerySearchPageParams = Depends(QuerySearchPageParams),
    db: Database = Depends(get_db),
):
    qp = GetQuestionsFilterPreviewQuery(answer_filter_value=answer_filter)
    query_filter = dict(deleted=False, submitted=True, **qp.answer_query)
    pipeline = prepare_aggregate_pipeline_w_users(
        query_filter, search_params.skip, search_params.limit
    )
    questions = db.questions.aggregate(pipeline)
    return list(map(format_obj_image_preview, questions))


@router.get(
    "/{question_id}",
    response_model=QuestionOut,
    responses={
        404: {
            "model": ExceptionQuestionNotFound,
            "description": ExceptionQuestionNotFound().detail,
        }
    },
)
async def get_question(
    question: QuestionOut = Depends(get_current_question),
):
    return question


@router.post(
    "/{question_id}/comments",
    status_code=201,
    responses={
        404: {
            "model": ExceptionQuestionNotFound,
            "description": ExceptionQuestionNotFound().detail,
        }
    },
)
def add_comment(
    comment: Comment,
    question_id: str = Depends(get_question_id),
    user: UserInDB = Depends(get_current_active_user),
    db: Database = Depends(get_db),
):
    comment_data = CommentInDB(
        user_id=user.user_id,
        type="question",
        object_id=question_id,
        **comment.dict(),
    )
    db.comments.insert_one(comment_data.dict())
    return Response(status_code=201)


@router.get(
    "/{question_id}/comments",
    response_model=List[CommentOut],
    responses={
        404: {
            "model": ExceptionQuestionNotFound,
            "description": ExceptionQuestionNotFound().detail,
        }
    },
)
async def get_comments(
    search_params: QuerySearchPageParams = Depends(QuerySearchPageParams),
    question_id: str = Depends(get_question_id),
    db: Database = Depends(get_db),
):
    query_filter = dict(
        type="question",
        object_id=question_id,
    )
    pipeline = prepare_aggregate_pipeline_comments_w_users(
        query_filter, search_params.skip, search_params.limit
    )
    comments = list(db.comments.aggregate(pipeline))
    return comments


@router.post("/", response_model=QuestionInResponse)
async def ask_question(
    question: Question,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Database = Depends(get_db),
):
    questionInDB = QuestionInDB(**question.dict(), user_id=current_user.user_id)
    db.questions.insert_one(questionInDB.dict())
    return QuestionInResponse(question_id=questionInDB.question_id)


@router.put(
    "/{question_id}",
    description="Edit question header",
    status_code=204,
    responses={
        403: {
            "model": ExceptionQuestionUserIsNotValidEditor,
            "description": ExceptionQuestionUserIsNotValidEditor().detail,
        },
        404: {
            "model": ExceptionQuestionNotFound,
            "description": ExceptionQuestionNotFound().detail,
        },
    },
)
async def edit_question(
    question_data: Question,
    questionInDB: QuestionInDB = Depends(get_current_question_w_valid_editor),
    db: Database = Depends(get_db),
):
    db.questions.update_one(
        {"question_id": questionInDB.question_id},
        {"$set": question_data.dict()},
    )
    return Response(status_code=204)


@router.put(
    "/{question_id}/submit",
    status_code=204,
    responses={
        403: {
            "model": ExceptionQuestionUserIsNotOwner,
            "description": ExceptionQuestionUserIsNotOwner().detail,
        },
        404: {
            "model": ExceptionQuestionNotFound,
            "description": ExceptionQuestionNotFound().detail,
        },
    },
)
async def submit_question(
    question: QuestionOut = Depends(get_current_question_w_valid_owner),
    db: Database = Depends(get_db),
):
    db.questions.update_one(
        {"question_id": question.question_id},
        {"$set": {"submitted": True}},
    )
    return Response(status_code=204)


@router.post(
    "/{question_id}/image",
    response_model=ObservationImageOut,
    responses={
        403: {
            "model": ExceptionQuestionUserIsNotOwner,
            "description": ExceptionQuestionUserIsNotOwner().detail,
        },
        404: {
            "model": ExceptionQuestionNotFound,
            "description": ExceptionQuestionNotFound().detail,
        },
    },
)
async def add_image_to_question(
    question: QuestionOut = Depends(get_current_question_w_valid_owner),
    image: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Database = Depends(get_db),
):
    if len(question.images) >= 10:
        raise HTTPException(
            status_code=400,
            detail=ExceptionQuestionImageCountLimit().detail,
        )

    # * setup image variables
    image_bytes = image.file.read()
    content_type = image.content_type

    # * get image metadata from exif
    image_location, image_heb_month_taken = get_image_metadata(image_bytes)

    # * set model
    imageInDB = QuestionImageInDB(
        orig_file_name=image.filename,
        month_taken=image_heb_month_taken,
        **image_location.dict(),
    )

    # * create thumbnail and upload to gstorage
    thumbnail_bytes = create_thumbnail(image_bytes)
    upload_to_gstorage(
        imageInDB.file_name, QUESTION_THUMBNAILS_PATH, thumbnail_bytes, content_type
    )

    # * upload image to gstorage as background task
    background_tasks.add_task(
        upload_to_gstorage,
        imageInDB.file_name,
        QUESTIONS_IMAGES_PATH,
        image_bytes,
        content_type,
    )

    # * add image to question
    db.questions.update_one(
        {"question_id": question.question_id},
        {"$push": {"images": imageInDB.dict()}},
    )
    return imageInDB


@router.put(
    "/{question_id}/image/{image_id}",
    status_code=204,
    responses={
        403: {
            "model": ExceptionQuestionUserIsNotValidEditor,
            "description": ExceptionQuestionUserIsNotValidEditor().detail,
        },
        404: {
            "description": "Not Found",
            "model": Union[ExceptionQuestionNotFound, ExceptionQuestionImageNotFound],
        },
    },
)
async def update_image_metadata(
    question_id: str,
    user_image_metadata: QuestionImageMetadata,
    image_data: QuestionImageInDB = Depends(get_image_data_w_valid_editor),
    db: Database = Depends(get_db),
):
    db.questions.update_one(
        {
            "question_id": question_id,
            "images.image_id": image_data.image_id,
        },
        {
            "$set": {
                "images.$.description": user_image_metadata.description
                or image_data.description,
                "images.$.location_name": user_image_metadata.location_name
                or image_data.location_name,
                "images.$.content_category": user_image_metadata.content_category
                or image_data.content_category,
                "images.$.month_taken": user_image_metadata.month_taken
                or image_data.month_taken,
            }
        },
    )
    return Response(status_code=204)


@router.delete(
    "/{question_id}/images/{image_id}",
    status_code=204,
    responses={
        403: {
            "model": ExceptionQuestionUserIsNotValidEditor,
            "description": ExceptionQuestionUserIsNotValidEditor().detail,
        },
        404: {
            "description": "Not Found",
            "model": Union[ExceptionQuestionNotFound, ExceptionQuestionImageNotFound],
        },
    },
)
async def delete_image_from_question(
    question_id: str,
    image_data: QuestionImageInDB = Depends(get_image_data_w_valid_editor),
    db: Database = Depends(get_db),
):
    # * delete image and thumbnail from storage
    delete_from_gstorage(image_data.file_name, QUESTIONS_IMAGES_PATH)
    delete_from_gstorage(image_data.file_name, QUESTION_THUMBNAILS_PATH)

    # * delete image metadata from question
    db.questions.update_one(
        {"question_id": question_id},
        {"$pull": {"images": {"image_id": image_data.image_id}}},
    )
    return Response(status_code=204)


@router.put(
    "/{question_id}/answer",
    status_code=204,
    responses={
        403: {
            "model": ExceptionUserNotPrivilege,
            "description": ExceptionUserNotPrivilege().detail,
        },
        404: {
            "description": "Not Found",
            "model": Union[ExceptionQuestionNotFound, ExceptionPlantNotFound],
        },
    },
)
async def answer_question(
    current_user: UserInDB = Depends(get_current_privilege_user),
    question_id: str = Depends(get_question_id),
    answer: AnswerPlantData = Depends(get_answer_data),
    db: Database = Depends(get_db),
):
    answerInDB = AnswerInDB(**answer.dict(), user_id=current_user.user_id)
    db.questions.update_one(
        {"question_id": question_id}, {"$set": {"answer": answerInDB.dict()}}
    )
    return Response(status_code=204)


@router.delete(
    "/{question_id}/answer",
    status_code=204,
    responses={
        403: {
            "model": ExceptionUserNotPrivilege,
            "description": ExceptionUserNotPrivilege().detail,
        },
        404: {
            "model": ExceptionQuestionNotFound,
            "description": ExceptionQuestionNotFound().detail,
        },
    },
    dependencies=[Depends(get_current_privilege_user)],
)
async def remove_answer(
    question_id: str = Depends(get_question_id),
    db: Database = Depends(get_db),
):
    db.questions.update_one({"question_id": question_id}, {"$set": {"answer": None}})
    return Response(status_code=204)


@router.post(
    "/{question_id}/images/{image_id}/rotate",
    responses={
        403: {
            "model": ExceptionQuestionUserIsNotValidEditor,
            "description": ExceptionQuestionUserIsNotValidEditor().detail,
        },
        404: {
            "description": "Not Found",
            "model": Union[ExceptionQuestionNotFound, ExceptionQuestionImageNotFound],
        },
    },
)
async def rotate_image_in_question(
    direction: RotateDirection,
    image_data: QuestionImageInDB = Depends(get_image_data_w_valid_editor),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    # * thumbnail
    rotate_storage_image(
        image_data.file_name, QUESTION_THUMBNAILS_PATH, direction.angle
    )

    # * image as background task
    background_tasks.add_task(
        rotate_storage_image,
        image_data.file_name,
        QUESTIONS_IMAGES_PATH,
        direction.angle,
    )
    return Response(status_code=204)


@router.delete(
    "/{question_id}",
    status_code=204,
    responses={
        403: {
            "model": ExceptionQuestionUserIsNotOwner,
            "description": ExceptionQuestionUserIsNotOwner().detail,
        },
        404: {
            "model": ExceptionQuestionNotFound,
            "description": ExceptionQuestionNotFound().detail,
        },
    },
)
async def delete_question(
    question: QuestionOut = Depends(get_current_question_w_valid_owner),
    db: Database = Depends(get_db),
):
    """
    Only set deleted flag to true in DB
    """
    db.questions.update_one(
        {"question_id": question.question_id}, {"$set": {"deleted": True}}
    )
    return Response(status_code=204)
