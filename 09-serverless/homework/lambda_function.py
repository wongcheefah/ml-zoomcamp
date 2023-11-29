import numpy as np

import tflite_runtime.interpreter as tflite

from io import BytesIO
from urllib import request

from PIL import Image


interpreter = tflite.Interpreter(model_path="bees-wasps-v2.tflite")
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]


def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(target_size, Image.NEAREST)
    return img


# Pre-processing in homework 8 was rescaling by dividing by 255
def preprocess_input(x):
    x /= 255.0
    return x


def predict(url):
    img = prepare_image(download_image(url), (150, 150))

    x = np.array(img, dtype="float32")
    X = np.array([x])
    X = preprocess_input(X)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()

    preds = interpreter.get_tensor(output_index)

    float_prediction = float(preds[0, 0])

    return float_prediction


def lambda_handler(event, context):
    url = event["url"]
    result = predict(url)
    return result
