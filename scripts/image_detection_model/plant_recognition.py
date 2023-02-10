# Coomand for recognition:
# python plant_recognition.py img_name.jpg

# Imports
from tflite_support.task import vision
from tflite_support.task import core
from tflite_support.task import processor
import sys, os

img_path = sys.argv[1]

# Initialization
base_options = core.BaseOptions(file_name="PlantDetect.tflite")
classification_options = processor.ClassificationOptions(max_results=1)
options = vision.ImageClassifierOptions(base_options=base_options, classification_options=classification_options)
classifier = vision.ImageClassifier.create_from_options(options)

# Alternatively, you can create an image classifier in the following manner:
# classifier = vision.ImageClassifier.create_from_file(model_path)

# Run inference
image = vision.TensorImage.create_from_file(img_path)
classification_result = classifier.classify(image)
print(classification_result)
