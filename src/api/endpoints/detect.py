from fastapi import APIRouter, File, UploadFile, Depends, Request
from endpoints.helpers_tools import detect_vision_api, detect_google_search
from core.config import get_settings
from pymongo.mongo_client import MongoClient
from db import get_db
from models.helpers import gen_image_file_name
from datetime import datetime
from core.security import ALGORITHM
from endpoints.helpers_tools.generic import get_today_str
from endpoints.helpers_tools.db import prepare_query_detect_image
from core.gstorage import bucket
from jose import jwt, JWTError

settings = get_settings()

router = APIRouter()


def extract_user_from_token(
    token: str | None, db: MongoClient
) -> dict:
    """
    Local function to extract user from token.

    If exists, return user (username and user_id as dict).
    If not, return empty dict
    """
    try:
        payload = jwt.decode(
            token.split("Bearer ")[-1], settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("username")
    except (JWTError, AttributeError):
        return {}

    user_data = db.users.find_one(
        {"username": username}, {"_id": 0, "username": 1, "user_id": 1}
    )
    return user_data


@router.post("/image/")
async def images(
    request: Request,
    file: UploadFile = File(...),
    db: MongoClient = Depends(get_db),
):
    # TODO: add response model (list of plants)
    # * init respose model
    apis_result = dict(google_search_by_image=None, search_by_vision_api=None)

    # * detect with google search by image
    result_google_search_by_image = detect_google_search.search_by_image(
        file.filename, file.file, file.content_type
    )
    apis_result["google_search_by_image"] = result_google_search_by_image
    await file.seek(0)

    # * detect with google vision api
    result_search_by_vision_api = detect_vision_api.search_by_vision_api(
        await file.read()
    )
    apis_result["search_by_vision_api"] = result_search_by_vision_api

    # TODO: DB cross data against apis_result - with Shahar
    # * search in db
    query_or = prepare_query_detect_image(
        result_google_search_by_image, result_search_by_vision_api
    )
    # print(query_or)
    db_result = db.plants.find(
        query_or,
        {"_id": 0, "heb_name": 1, "science_name": 1},
    )

    # * upload image to cloud storage
    await file.seek(0)
    new_file_name = gen_image_file_name(file.filename)
    blob = bucket.blob("image_api_files/" + new_file_name)
    blob.upload_from_file(file.file, content_type=file.content_type)

    # * check in auth headers
    user_data = extract_user_from_token(token=request.headers.get("Authorization"), db=db)

    # * save apis_result to DB
    additional_data = dict(
        user_data=user_data,
        self_link=blob.self_link,
        media_link=blob.media_link,
        public_url=blob.public_url,
        orig_file_name=file.filename,
        file_name=new_file_name,
        content_type=file.content_type,
        ts=datetime.utcnow(),
    )
    result_data = dict(
        google_search_by_image=apis_result["google_search_by_image"].dict(),
        search_by_vision_api=apis_result["search_by_vision_api"].dict(),
    )
    db.images_detections.insert_one(
        dict(result_data=result_data, additional_data=additional_data)
    )

    # * increase user usage counter of images detection if signed in
    if user_data:
        db.users.update_one(
            {"username": user_data.get("username")},
            {"$inc": {f"counters.image_detection.{get_today_str()}": 1}},
        )

    return apis_result | {
        "db_result": list(db_result)
    }  # TODO: replace with final response model
