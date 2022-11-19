import os
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras
from skimage import io
from tensorflow.keras.preprocessing import image

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

vegmodel = tf.keras.models.load_model("VegetableModel.h5", compile=False)
fruitmodel = tf.keras.models.load_model("FruitModel.h5", compile=False)


def veg_model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    show_img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255
    preds = vegmodel.predict(x)
    return preds


def fruit_model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    show_img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255
    preds = fruitmodel.predict(x)
    return preds


@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/Predict", methods=["GET", "POST"])
def route():
    return render_template("predict.html")


@app.route("/predict", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        print
        f = request.files["file"]
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, "uploads", secure_filename(f.filename))
        f.save(file_path)
        plant = request.form["Plant"]

        disease_class = [
            "Apple Black Rot",
            "Apple Cedar Rust",
            "Apple Healthy",
            "Apple Scab",
            "Blueberry Healthy",
            "Cherry(Including_Sour) Healthy",
            "Cherry(Including_Sour) Powdery Mildew",
            "Corn(Maize) Cercospora Gray leaf spot",
            "Corn(Maize) Common Rust",
            "Corn(Maize) Northern Leaf Blight",
            "Corn(Maize) healthy",
            "Grape Black Rot",
            "Grape Esca (Black_Measles)",
            "Grape Healthy",
            "Grape Leaf Blight (Isariopsis_Leaf_Spot)",
            "Misc",
            "Orange Haunglongbing (Citrus_Greening)",
            "Peach Bacterial Spot",
            "Peach Healthy",
            "Pepper Bell Bacterial Spot",
            "Pepper Healthy",
            "Potato Early blight",
            "Potato Healthy",
            "Potato Late Blight",
            "Raspberry Healthy",
            "Soybean Healthy",
            "Squash Powdery Mildew",
            "Strawberry Healthy",
            "Strawberry Leaf Scorch",
            "Tomato Bacterial Spot",
            "Tomato Early Blight",
            "Tomato Healthy",
            "Tomato Late Blight",
            "Tomato Leaf Mold",
            "Tomato Mosaic Virus",
            "Tomato Septoria leaf Spot",
            "Tomato Spider Mite",
            "Tomato Target Spot",
            "Tomato Yellow Leaf Curl Virus",
        ]

        if plant == "Vegetable":
            preds = veg_model_predict(file_path, veg_model_predict)
        else:
            preds = fruit_model_predict(file_path, fruit_model_predict)

        a = preds[0]
        ind = np.argmax(a)
        result = disease_class[ind]
        df = pd.read_excel("Disease Fertilizer.xlsx")
        for row in range(len(df)):
            if df.loc[row, "Disease"] == result:
                fertilizer=df.loc[row, "Description"]
                result+=fertilizer
                break
        return result
    return None


if __name__ == "__main__":
    app.run()
