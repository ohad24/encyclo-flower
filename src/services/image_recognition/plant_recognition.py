from tflite_support.task import vision
from tflite_support.task import core
from tflite_support.task import processor
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import numpy as np
from PIL import Image
from io import BytesIO

NUMBER_OF_RESULTS = 5


class Classification(BaseModel):
    class_name: str
    score: float


app = FastAPI()


@app.post("/detect/")
async def detect(file: UploadFile = File(...)):
    # * convert file to image (ndarray)
    image_bytes = np.array(Image.open(BytesIO(file.file.read())))
    # * load model
    base_options = core.BaseOptions(file_name="model.tflite")
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
                score=classification_result.classifications[0].classes[i].score,
            )
        )
    return {"predictions": predictions}
