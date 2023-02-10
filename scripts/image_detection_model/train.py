import os

import numpy as np

import tensorflow as tf
assert tf.__version__.startswith('2')

from tflite_model_maker import model_spec
from tflite_model_maker import image_classifier
from tflite_model_maker.config import ExportFormat
from tflite_model_maker.config import QuantizationConfig
from tflite_model_maker.image_classifier import DataLoader

import matplotlib.pyplot as plt

tf.__version__

image_path = "/data/data"

data = DataLoader.from_folder(image_path)
train_data, test_data = data.split(0.8)

# model = image_classifier.create(train_data)
model = image_classifier.create(train_data, model_spec=model_spec.get('mobilenet_v2'), epochs=100)

loss, accuracy = model.evaluate(test_data)
print(loss, accuracy)

model.export(export_dir='.')
