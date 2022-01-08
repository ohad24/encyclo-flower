from fastapi import APIRouter, File, UploadFile, Depends, Request
from endpoints.helpers_tools import detect_vision_api, detect_google_search
from google.cloud import storage
from core.config import get_settings
from pymongo.mongo_client import MongoClient
import db
import uuid
import datetime
from core.security import verify_user_in_token

settings = get_settings()

router = APIRouter()

storage_client = storage.Client()


@router.post("/image/")
async def images(
    request: Request,
    file: UploadFile = File(...),
    db: MongoClient = Depends(db.get_db),
):
    # TODO: add response model (list of plants)
    # * init respose model
    apis_result = dict(google_search_by_image=None, search_by_vision_api=None)

    # * detect with google search by image
    apis_result["google_search_by_image"] = detect_google_search.search_by_image(
        file.filename, file.file, file.content_type
    )
    await file.seek(0)

    # * detect with google vision api
    apis_result["search_by_vision_api"] = detect_vision_api.search_by_vision_api(
        await file.read()
    )

    # TODO: DB cross data against apis_result - with Shahar

    # * upload image to cloud storage
    await file.seek(0)
    bucket = storage_client.bucket(settings.CLOUD_BUCKET)
    new_file_name = str(uuid.uuid4()) + "." + file.filename.split(".")[-1]
    blob = bucket.blob("image_api_files/" + new_file_name)
    blob.upload_from_file(file.file, content_type=file.content_type)

    # * save apis_result to DB
    additional_data = dict(
        user_data=verify_user_in_token(request.headers.get("Authorization")),
        self_link=blob.self_link,
        media_link=blob.media_link,
        public_url=blob.public_url,
        orig_file_name=file.filename,
        file_name=new_file_name,
        content_type=file.content_type,
        ts=datetime.datetime.utcnow(),
    )
    result_data = dict(
        google_search_by_image=apis_result["google_search_by_image"].dict(),
        search_by_vision_api=apis_result["search_by_vision_api"].dict(),
    )
    db.images_detections.insert_one(
        dict(result_data=result_data, additional_data=additional_data)
    )

    # TODO: increase user usage counter of images detections if signed in
    # get username from header

    return apis_result  # TODO: replace with final response model
