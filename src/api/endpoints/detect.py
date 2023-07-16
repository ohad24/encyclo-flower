from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, BackgroundTasks
from endpoints.helpers_tools.storage import upload_to_gstorage
from core.config import get_settings
from pymongo.database import Database
from db import get_db
from models.helpers import gen_image_file_name
from datetime import datetime
from core.security import get_current_user_if_exists, validate_detection_usage
from endpoints.helpers_tools.generic import get_today_str, get_image_metadata
from endpoints.helpers_tools.db import prepare_query_detect_image
from models.user import UserMinimalMetadataOut
import requests
from models.plant import PlantPrediction
from typing import List
from pathlib import Path
from models.exceptions import (
    ExceptionImageDetectionServiceUnavailable,
    ExceptionTooManyRequests,
)
import google.auth.transport.requests
import google.oauth2.id_token

settings = get_settings()

router = APIRouter()


@router.post(
    "/image/",
    response_model=List[PlantPrediction],
    summary="Detect plant from image",
    description="Detect plant from image using the external service",
    responses={
        503: {
            "model": ExceptionImageDetectionServiceUnavailable,
            "description": ExceptionImageDetectionServiceUnavailable().detail,
        },
        429: {
            "model": ExceptionTooManyRequests,
            "description": ExceptionTooManyRequests().detail,
        },
    },
    dependencies=[Depends(validate_detection_usage)],
)
async def images(
    file: UploadFile = File(...),
    user_data: UserMinimalMetadataOut = Depends(get_current_user_if_exists),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Database = Depends(get_db),
) -> List[PlantPrediction]:
    # * send file to image recognition API
    try:
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(
            auth_req, settings.DETECT_API_SRV
        )
        headers = {"Authorization": f"Bearer {id_token}"}
        api_response = requests.post(
            settings.DETECT_API_SRV + "/detect/",
            headers=headers,
            files={"file": file.file},
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail=ExceptionImageDetectionServiceUnavailable().detail,
        )

    # * get image bytes
    await file.seek(0)
    image_bytes = file.file.read()
    # * get image metadata from exif
    image_location, _ = get_image_metadata(image_bytes)

    # * prepare pipeline
    pipeline = prepare_query_detect_image(
        api_response.json(), image_location.location_name
    )

    # * search in db and convert to PlantPrediction
    plant_predictions = list(
        PlantPrediction(**x) for x in db.plants.aggregate(pipeline)
    )

    # * merge score from api to db result
    for idx, db_item in enumerate(plant_predictions):
        for api_item in api_response.json():
            if db_item.science_name == api_item["class_name"]:
                plant_predictions[idx].score = api_item["score"]
                break

    # * sort by score
    plant_predictions = sorted(plant_predictions, key=lambda x: x.score, reverse=True)

    # * generate image file name
    new_file_name = gen_image_file_name(file.filename)

    # * upload image to cloud storage
    background_tasks.add_task(
        upload_to_gstorage,
        new_file_name,
        Path("image_api_files"),
        image_bytes,
        file.content_type,
    )

    # * save all data in DB (image_detections collection)
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
        dict(
            metadata=metadata,
            api_response=api_response.json(),
            db_results=[x.dict() for x in plant_predictions],
        )
    )

    # * increase user usage counter of images detection if signed in
    if user_data:
        db.users.update_one(
            {"username": user_data.username},
            {"$inc": {f"counters.image_detection.{get_today_str()}": 1}},
        )

    return plant_predictions
