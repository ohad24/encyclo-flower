from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Response,
    Query,
)
from models.user_observations import (
    Observation,
    ObservationOut,
    ObservationInDB,
    ObservationInResponse,
    ObservationImageInDB,
    ObservationImageOut,
    ObservationImageInDB_w_oid,
    ObservationImageMeta,
    ObservationsPreview,
)
from models.user import User
from models.generic import (
    Comment,
    CommentInDB,
    RotateDirection,
    CommentOut,
)
from core.security import get_current_active_user
import db
from pymongo.mongo_client import MongoClient
from endpoints.helpers_tools.observation_dependencies import (
    get_current_observation,
    get_current_observation_w_valid_owner,
    get_image_data_oid_w_valid_editor,
    get_observation_id,
    get_current_observation_w_valid_editor,
    get_image_data_w_valid_editor,
)
from endpoints.helpers_tools.generic import (
    get_image_metadata,
    format_obj_image_preview,
    rotate_image,
)
from core.gstorage import bucket
from typing import List
from endpoints.helpers_tools.db import (
    prepare_aggregate_pipeline_w_users,
    prepare_aggregate_pipeline_comments_w_users,
)

router = APIRouter(prefix="/observations", tags=["observations"])


@router.get("/", response_model=List[ObservationsPreview])
async def get_all_observations(
    skip: int = Query(0, ge=0),
    limit: int = Query(9, ge=1, le=9),
    db: MongoClient = Depends(db.get_db),
):
    query_filter = dict(deleted=False, submitted=True)
    pipeline = prepare_aggregate_pipeline_w_users(query_filter, skip, limit)
    observations = db.observations.aggregate(pipeline)
    return list(map(format_obj_image_preview, observations))


@router.get("/{observation_id}", response_model=ObservationOut)
async def get_observation_by_id(
    observation: ObservationOut = Depends(get_current_observation),
):
    return observation


@router.post("/", response_model=ObservationInResponse)
async def add_observation(
    observation: Observation,
    user: User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    observationInDB = ObservationInDB(**observation.dict(), user_id=user.user_id)
    db.observations.insert_one(observationInDB.dict())
    return ObservationInResponse(observation_id=observationInDB.observation_id)


@router.put("/{observation_id}", description="Edit observation header", status_code=204)
async def edit_observation(
    observation_data: Observation,
    observationInDB: ObservationInDB = Depends(get_current_observation_w_valid_editor),
    db: MongoClient = Depends(db.get_db),
):
    db.observations.update_one(
        {"observation_id": observationInDB.observation_id},
        {"$set": observation_data.dict()},
    )
    return Response(status_code=204)


@router.put("/{observation_id}/submit", status_code=204)
async def submit_observation(
    observationInDB: ObservationInDB = Depends(get_current_observation_w_valid_owner),
    db: MongoClient = Depends(db.get_db),
):
    db.observations.update_one(
        {"observation_id": observationInDB.observation_id},
        {"$set": {"submitted": True}},
    )
    return Response(status_code=204)


@router.post("/{observation_id}/image", response_model=ObservationImageOut)
async def add_image_to_observation(
    observationInDB: str = Depends(get_current_observation_w_valid_owner),
    image: UploadFile = File(...),
    db: MongoClient = Depends(db.get_db),
):

    # * get image metadata from exif
    image_location, image_heb_month_taken = get_image_metadata(image.file)

    imageInDB = ObservationImageInDB(
        orig_file_name=image.filename,
        month_taken=image_heb_month_taken,
        **image_location.dict(),
    )

    # * seek 0 and upload image to storage
    image.file.seek(0)
    blob = bucket.blob("observations/" + imageInDB.file_name)
    blob.upload_from_file(image.file, content_type=image.content_type)

    # * update links from storage
    imageInDB.self_link = blob.self_link
    imageInDB.media_link = blob.media_link
    imageInDB.public_url = blob.public_url

    # * add image to observation
    db.observations.update_one(
        {"observation_id": observationInDB.observation_id},
        {"$push": {"images": imageInDB.dict()}},
    )
    return imageInDB


@router.put("/{observation_id}/image/{image_id}", status_code=204)
async def update_image_metadata(
    user_image_metadata: ObservationImageMeta,
    image_data: ObservationImageInDB_w_oid = Depends(get_image_data_oid_w_valid_editor),
    db: MongoClient = Depends(db.get_db),
):
    # * check if plant_id is valid
    plant = db.plants.find_one({"plant_id": user_image_metadata.plant_id})
    if plant:
        plant_id = plant["plant_id"]
    else:
        plant_id = None

    db.observations.update_one(
        {
            "observation_id": image_data.observation_id,
            "images.image_id": image_data.image.image_id,
        },
        {
            "$set": {
                "images.$.description": user_image_metadata.description
                or image_data.image.description,
                "images.$.location_name": user_image_metadata.location_name
                or image_data.image.location_name,
                "images.$.content_category": user_image_metadata.content_category
                or image_data.image.content_category,
                "images.$.month_taken": user_image_metadata.month_taken
                or image_data.image.month_taken,
                "images.$.plant_id": plant_id,
                "images.$.uploaded": True,
            }
        },
    )
    return Response(status_code=204)


@router.delete("/{observation_id}/image/{image_id}", status_code=204)
async def delete_image_from_observation(
    image_data: ObservationImageInDB_w_oid = Depends(get_image_data_oid_w_valid_editor),
    db: MongoClient = Depends(db.get_db),
):
    # * delete image from storage
    blob = bucket.blob("observations/" + image_data.image.file_name)
    blob.delete()

    # * delete image metadata from question
    db.observations.update_one(
        {"observation_id": image_data.observation_id},
        {"$pull": {"images": {"image_id": image_data.image.image_id}}},
    )
    return Response(status_code=204)


@router.post("/{observation_id}/comment", status_code=201)
async def add_comment(
    comment: Comment,
    user: User = Depends(get_current_active_user),
    observation_id: str = Depends(get_observation_id),
    db: MongoClient = Depends(db.get_db),
):
    comment_data = CommentInDB(
        user_id=user.user_id,
        type="observation",
        object_id=observation_id,
        **comment.dict(),
    )
    db.comments.insert_one(comment_data.dict())
    return Response(status_code=201)


@router.get("/{observation_id}/comments", response_model=List[CommentOut])
async def get_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(9, ge=1, le=9),
    observation_id: str = Depends(get_observation_id),
    db: MongoClient = Depends(db.get_db),
):
    query_filter = dict(
        type="observation",
        object_id=observation_id,
    )
    pipeline = prepare_aggregate_pipeline_comments_w_users(query_filter, skip, limit)
    comments = list(db.comments.aggregate(pipeline))
    return comments


@router.post("/{observation_id}/images/{image_id}/rotate", status_code=204)
async def rotate_image_in_observation(
    direction: RotateDirection,
    image_data: ObservationImageInDB = Depends(get_image_data_w_valid_editor),
):
    # * download image
    blob = bucket.blob("observations/" + image_data.file_name)
    image = blob.download_as_bytes()
    # * rotate image
    rotated_image = rotate_image(image, direction.angle)
    # * upload image to gstorage
    blob.upload_from_string(rotated_image, content_type=blob.content_type)

    return Response(status_code=204)


@router.delete("/{observation_id}", status_code=204)
async def delete_observation(
    observation: ObservationInDB = Depends(get_current_observation_w_valid_owner),
    db: MongoClient = Depends(db.get_db),
):
    """
    Only set deleted flag to true in DB
    """
    db.observations.update_one(
        {"observation_id": observation.observation_id}, {"$set": {"deleted": True}}
    )
    return Response(status_code=204)
