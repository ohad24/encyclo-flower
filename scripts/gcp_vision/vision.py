from google.cloud import vision
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import base64
from fastapi import FastAPI, Body

load_dotenv()  # load path in GOOGLE_APPLICATION_CREDENTIALS from .env

client = vision.ImageAnnotatorClient()


app = FastAPI()


class WebEntity(BaseModel):
    description: Optional[str]
    score: Optional[float]


class DetectResponse(BaseModel):
    labels: list[Optional[str]] = []
    web_entities: list[Optional[WebEntity]] = []


def search_by_vision_api(encoded_image):
    # * convert base64 to bytes
    content = base64.b64decode(encoded_image)

    # * image to be analyzed
    image = vision.Image(content=content)

    # * Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # * Performs web detection on the image file
    response_web_detection = client.web_detection(image=image).web_detection
    response_web_detection.web_entities.sort(key=lambda x: x.score, reverse=True)

    response = dict(
        labels=[x.description for x in labels],
        web_entities=[
            {"description": x.description, "score": x.score}
            for x in response_web_detection.web_entities
        ],
    )

    return response


@app.post("/detect/", response_model=DetectResponse)
def detect(data: dict = Body(...)):
    encoded_image = data.get('encoded_image')
    return search_by_vision_api(encoded_image)


if __name__ == "__main__":
    test_images = ["I3YOFNKFFRVZOPN.jpg", "IWU8AAVDDDEEKRC.jpg", "58NY77V207Q7H06.jpg"]
    images_directory = "tests/assets/images/"

    for file in test_images:
        with open(images_directory + file, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            response = search_by_vision_api(encoded_image)
            print(response)
