from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from endpoints.helpers_tools import detect_vision_api, detect_google_search
from endpoints.helpers_tools.storage import upload_to_gstorage
from core.config import get_settings
from pymongo.database import Database
from db import get_db
from models.helpers import gen_image_file_name
from datetime import datetime
from core.security import get_current_user_if_exists
from endpoints.helpers_tools.generic import get_today_str
from endpoints.helpers_tools.db import prepare_query_detect_image
from models.user import UserMinimalMetadataOut
import requests
from models.plant import PlantPrediction
from typing import List
from pathlib import Path
from models.exceptions import ExceptionImageDetectionServiceUnavailable

settings = get_settings()

router = APIRouter()

# TODO: set api limitter for this endpoint (by ip or user)


@router.post(
    "/image/",
    response_model=List[PlantPrediction],
    summary="Detect plant from image",
    description="Detect plant from image using the external service",
    responses={
        503: {
            "model": ExceptionImageDetectionServiceUnavailable,
            "description": ExceptionImageDetectionServiceUnavailable().detail,
        }
    },
)
async def images(
    file: UploadFile = File(...),
    user_data: UserMinimalMetadataOut = Depends(get_current_user_if_exists),
    db: Database = Depends(get_db),
) -> List[PlantPrediction]:
    # * send file to image recognition API
    try:
        api_response = requests.post(settings.DETECT_API_SRV, files={"file": file.file})
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail=ExceptionImageDetectionServiceUnavailable().detail,
        )

    # * prepare pipeline
    pipeline = prepare_query_detect_image(api_response)

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
    # TODO: move to background task (?)
    upload_to_gstorage(
        new_file_name, Path("image_api_files"), file.file.read(), file.content_type
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
            db_resaults=[x.dict() for x in plant_predictions],
        )
    )

    # * increase user usage counter of images detection if signed in
    if user_data:
        db.users.update_one(
            {"username": user_data.username},
            {"$inc": {f"counters.image_detection.{get_today_str()}": 1}},
        )

    return plant_predictions
