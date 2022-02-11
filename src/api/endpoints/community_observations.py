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
)
from models.user import User
from models.generic import WhatInImage, ImageLocation, Comment, CommentInDB
from core.security import get_current_active_user, get_current_privilege_user
import db
from pymongo.mongo_client import MongoClient
from endpoints.helpers_tools.observation_dependencies import (
    get_current_observation,
    get_current_observation_w_valid_owner,
    get_image_data_oid_w_valid_editor,
    get_observation_id,
)
from endpoints.helpers_tools.generic import get_image_exif_data
from core.gstorage import bucket

router = APIRouter(prefix="/observations", tags=["observations"])

# TODO: edit observation
# TODO: delete observation
# TODO: delete image from observation
# TODO: rotate image
# TODO: format file


# TODO: get all observations
@router.get("/")
async def get_all_observations():
    return "Hello World"


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


# TODO: add image to observation
@router.post("/{observation_id}/image")
async def add_image_to_observation(
    observation: ObservationInDB = Depends(get_current_observation_w_valid_owner),
    image: UploadFile = File(...),
    description: str = Form(None),
    plant_id: str = Form(None),  # TODO: create validation if value not in db
    what_in_image: WhatInImage = Form(None),
    db: MongoClient = Depends(db.get_db),
):
    # * get image exif data
    lon, lat, alt, image_dt = get_image_exif_data(image.file)

    # * init image class
    image_metadata = ObservationImageInDB(
        orig_file_name=image.filename,
        description=description,
        plant_id=plant_id,
        what_in_image=what_in_image,
        image_dt=image_dt,
        location=ImageLocation(lat=lat, lon=lon, alt=alt) if lon and lat else None,
    )

    # * seek 0 and upload image to storage
    image.file.seek(0)
    blob = bucket.blob("observations/" + image_metadata.file_name)
    blob.upload_from_file(image.file, content_type=image.content_type)

    # * update links from storage
    image_metadata.self_link = blob.self_link
    image_metadata.media_link = blob.media_link
    image_metadata.public_url = blob.public_url

    # * add image to observation (db, push to images array)
    db.observations.update_one(
        {"observation_id": observation.observation_id},
        {"$push": {"images": image_metadata.dict()}},
    )
    return Response(status_code=201)


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
    db.questions.update_one(
        {"observation_id": image_data.observation_id},
        {
            "$pull": {
                "images": {"image_id": image_data.image.image_id, "uploaded": True}
            }
        },
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
