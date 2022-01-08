from google.cloud import vision
from pydantic import BaseModel
from typing import Optional


class WebEntity(BaseModel):
    description: Optional[str]
    score: Optional[float]


class DetectResponse(BaseModel):
    labels: list[Optional[str]] = []
    web_entities: list[Optional[WebEntity]] = []


# * create vision client
client = vision.ImageAnnotatorClient()


def search_by_vision_api(content: bytes) -> DetectResponse:
    # * image to be analyzed
    image = vision.Image(content=content)

    # * Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # * Performs web detection on the image file
    response_web_detection = client.web_detection(image=image).web_detection
    response_web_detection.web_entities.sort(key=lambda x: x.score, reverse=True)

    detect_response = DetectResponse(
        labels=[x.description for x in labels],
        web_entities=[
            {"description": x.description, "score": x.score}
            for x in response_web_detection.web_entities
        ],
    )
    return detect_response
