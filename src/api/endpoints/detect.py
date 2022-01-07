from fastapi import APIRouter, File
from typing import List
import requests
import base64

router = APIRouter()


# @app.post("/image/")
# async def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}


@router.post("/images/")
async def images(files: List[bytes] = File(...)):
    # convert first file to base64
    file = files[0]
    encoded_image = base64.b64encode(file).decode("utf-8")
    r = requests.post(
        "http://localhost:5001/detect/",
        json={"encoded_image": encoded_image}
    )
    print(r.json())
    return {"file_sizes": [len(file) for file in files]}
