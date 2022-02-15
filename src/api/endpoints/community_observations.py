from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Form,
    HTTPException,
    Response,
    Query,
)
from models.user_observations import (
    Observation,
    ObservationInDB,
    ObservationInResponse,
    ObservationImageInDB,
    ObservationImageInDB_w_oid,
    ObservationImageMeta,
    ObservationsPreview,
)
from models.user import User
from models.generic import (
    WhatInImage,
    ImageLocation,
    Comment,
    CommentInDB,
    RotateDirection,
)
from core.security import get_current_active_user, get_current_privilege_user
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
    get_image_exif_data,
    find_image_location,
    format_obj_image_preview,
    rotate_image,
)
from core.gstorage import bucket
from typing import List, Optional

router = APIRouter(prefix="/observations", tags=["observations"])

# TODO: delete observation
# TODO: format file


# TODO: get all observations (only submitted)
@router.get("/", response_model=List[Optional[ObservationsPreview]])
async def get_all_observations(
    skip: int = Query(0, ge=0, le=9),
    limit: int = Query(9, ge=0, le=9),
    db: MongoClient = Depends(db.get_db),
):
    db_query = dict(deleted=False, submitted=True)
    observations = (
        db.observations.find(
            db_query,
            {"_id": 0, "comments": 0},
        )
        .sort("created_dt", -1)
        .limit(limit)
        .skip(skip)
    )
    return list(map(format_obj_image_preview, observations))


# get one observation
@router.get("/{observation_id}")
async def get_observation_by_id(
    observation: ObservationInDB = Depends(get_current_observation),
):
    return observation


# TODO: create new observation
@router.post("/", response_model=ObservationInResponse)
async def add_observation(
    observation: Observation,
    user: User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    observationInDB = ObservationInDB(**observation.dict(), user_id=user.user_id)
    db.observations.insert_one(observationInDB.dict())
    return ObservationInResponse(observation_id=observationInDB.observation_id)


# TODO: edit observation (first and later). allow not submitted
@router.put("/{observation_id}", description="Edit observation header")
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


# TODO: submit observation. when not submitted
@router.put("/{observation_id}/submit")
async def submit_observation(
    observationInDB: ObservationInDB = Depends(get_current_observation_w_valid_owner),
    db: MongoClient = Depends(db.get_db),
):
    db.observations.update_one(
        {"observation_id": observationInDB.observation_id},
        {"$set": {"submitted": True}},
    )
    return Response(status_code=204)


# TODO: upload one image to observation. no metadata
@router.post(
    "/{observation_id}/image",
    response_model=ObservationImageInDB,
)
async def add_image_to_observation(
    observationInDB: str = Depends(get_current_observation_w_valid_owner),
    image: UploadFile = File(...),
    db: MongoClient = Depends(db.get_db),
):

    # * get image exif data
    # TODO: do in one function
    lon, lat, alt, image_dt = get_image_exif_data(image.file)
    il = find_image_location(lon, lat, alt)

    imageInDB = ObservationImageInDB(
        orig_file_name=image.filename,
        location_name=il.location_name,
        coordinates=il.coordinates,
        image_dt=image_dt,
    )

    # * seek 0 and upload image to storage
    image.file.seek(0)
    blob = bucket.blob("observations/" + imageInDB.file_name)
    blob.upload_from_file(image.file, content_type=image.content_type)

    # * update links from storage
    imageInDB.self_link = blob.self_link
    imageInDB.media_link = blob.media_link
    imageInDB.public_url = blob.public_url

    db.observations.update_one(
        {"observation_id": observationInDB.observation_id},
        {"$push": {"images": imageInDB.dict()}},
    )
    return imageInDB


# TODO: update image metadata
@router.put("/{observation_id}/image/{image_id}")
async def update_image_metadata(
    user_image_metadata: ObservationImageMeta,
    image_data: ObservationImageInDB_w_oid = Depends(get_image_data_oid_w_valid_editor),
    db: MongoClient = Depends(db.get_db),
):

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
                "images.$.what_in_image": user_image_metadata.what_in_image
                or image_data.image.what_in_image,
                "images.$.image_dt": user_image_metadata.image_dt
                or image_data.image.image_dt,
                "images.$.uploaded": True,
            }
        },
    )
    return Response(status_code=204)


# TODO: delete image from observation
@router.delete("/{observation_id}/image/{image_id}")
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


# TODO: add comment to observation
@router.post("/{observation_id}/comment")
async def add_comment(
    comment: Comment,
    observation_id: str = Depends(get_observation_id),
    user: User = Depends(get_current_active_user),
    db: MongoClient = Depends(db.get_db),
):
    comment_data = CommentInDB(user_id=user.user_id, **comment.dict())
    db.observations.update_one(
        {"observation_id": observation_id}, {"$push": {"comments": comment_data.dict()}}
    )
    return Response(status_code=201)


# TODO: rotate image
@router.post("/{observation_id}/images/{image_id}/rotate")
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
