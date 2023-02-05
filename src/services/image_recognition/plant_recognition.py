import os

# * set env variables
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from tflite_support.task import vision
from tflite_support.task import core
from tflite_support.task import processor
from fastapi import FastAPI, File, UploadFile, Request
from pydantic import BaseModel
import numpy as np
from PIL import Image
from io import BytesIO
from typing import List
from time import time
from pathlib import Path


NUMBER_OF_RESULTS = 5


class Classification(BaseModel):
    class_name: str
    score: float


app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.post("/detect/", response_model=List[Classification])
async def detect(file: UploadFile = File(...)) -> List[Classification]:
    # * convert file to image (ndarray)
    image_bytes = np.array(Image.open(BytesIO(file.file.read())))
    # * load model
    model_file_path = Path(os.path.dirname(os.path.abspath(__file__))) / "PlantDetect.tflite"
    base_options = core.BaseOptions(file_name=str(model_file_path))
    classification_options = processor.ClassificationOptions(
        max_results=NUMBER_OF_RESULTS
    )
    options = vision.ImageClassifierOptions(
        base_options=base_options, classification_options=classification_options
    )
    # * create classifier
    classifier = vision.ImageClassifier.create_from_options(options)
    # * load image to classifier
    image = vision.TensorImage.create_from_array(image_bytes)
    # * classify image
    classification_result = classifier.classify(image)

    # * create response
    predictions = []
    for i in range(NUMBER_OF_RESULTS):
        predictions.append(
            Classification(
                class_name=classification_result.classifications[0]
                .classes[i]
                .class_name,
                score=round(
                    classification_result.classifications[0].classes[i].score, 5
                ),
            )
        )
    return predictions
