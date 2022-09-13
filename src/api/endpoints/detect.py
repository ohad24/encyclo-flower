from fastapi import APIRouter, File, UploadFile, Depends
from endpoints.helpers_tools import detect_vision_api, detect_google_search
from core.config import get_settings
from pymongo.database import Database
from db import get_db
from models.helpers import gen_image_file_name
from datetime import datetime
from core.security import get_current_user_if_exists
from endpoints.helpers_tools.generic import get_today_str
from endpoints.helpers_tools.db import prepare_query_detect_image
from core.gstorage import bucket
from models.user import UserMinimalMetadataOut
import os
import requests

settings = get_settings()

router = APIRouter()

# TODO: set api limitter for this endpoint (by ip or user)


@router.post("/image/")
async def images(
    file: UploadFile = File(...),
    user_data: UserMinimalMetadataOut = Depends(get_current_user_if_exists),
    db: Database = Depends(get_db),
):
    # * send file to image recognition API
    # TODO: add this to global config/vars
    DETECT_API_SRV = os.environ.get("API_SRV", "http://localhost:5001/detect/")
    api_response = requests.post(DETECT_API_SRV, files={"file": file.file})

    # * prepare pipeline
    pipeline = prepare_query_detect_image(api_response)

    # * search in db
    db_result = list(db.plants.aggregate(pipeline))

    # * merge score from api to db result
    for idx, db_item in enumerate(db_result):
        for api_item in api_response.json():
            if api_item["class_name"] == db_item["science_name"]:
                db_result[idx]["score"] = api_item["score"]
                break

    # * sort by score
    db_result = sorted(db_result, key=lambda x: x["score"], reverse=True)

    # * upload image to cloud storage
    # TODO: move to background task
    await file.seek(0)
    new_file_name = gen_image_file_name(file.filename)
    blob = bucket.blob("image_api_files/" + new_file_name)
    blob.upload_from_file(file.file, content_type=file.content_type)

    # * save apis_result to DB
    metadata = dict(
        user_data=user_data.dict(include={"username", "user_id"}),
        orig_file_name=file.filename,
        file_name=new_file_name,
        content_type=file.content_type,
        ts=datetime.utcnow(),
        detection_service_response_time_sec=round(
            float(api_response.headers["x-process-time"]), 5
        ),
    )
    db.images_detections.insert_one(
        dict(metadata=metadata, api_response=api_response.json(), db_result=db_result)
    )

    # * increase user usage counter of images detection if signed in
    if user_data:
        db.users.update_one(
            {"username": user_data.username},
            {"$inc": {f"counters.image_detection.{get_today_str()}": 1}},
        )

    return db_result  # TODO: replace with final response model
