from fastapi import APIRouter, File, UploadFile
from endpoints.helpers_tools import detect_vision_api, detect_google_search

router = APIRouter()


@router.post("/image/")
async def images(file: UploadFile = File(...)):
    # TODO: add response model (list of plants)
    apis_result = dict(google_search_by_image=None, search_by_vision_api=None)
    apis_result["google_search_by_image"] = detect_google_search.search_by_image(
        file.filename, file.file, file.content_type
    )
    await file.seek(0)
    apis_result["search_by_vision_api"] = detect_vision_api.search_by_vision_api(
        await file.read()
    )

    # TODO: DB cross data against apis_result - with Shahar
    return apis_result  # TODO: replace with final response model
