from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import requests
import os

app = Flask(__name__)
CORS(app)

TOKEN = "7094792264:AAEH-QrZhteAOaFoHoCZEk54iyzhud1Tck4"
TELEGRAM_CHAT_ID = "5949257717"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

MODEL = tf.keras.models.load_model("D:\code of hackathon\plant-deasese-project\2-20240209T113751Z-001\2")

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

DISEASE_SOLUTIONS = {
    "Early Blight": "Apply fungicide and increase watering.",
    "Late Blight": "Isolate infected plants and use fungicide Y.",
    "Healthy": "No disease detected. Keep monitoring for any changes.",
}

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data))
    image = image.resize((256, 256))
    image = np.array(image)
    return image

def predict_disease(image_data):
    image = read_file_as_image(image_data)
    img_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]))
    return predicted_class, confidence

def send_to_telegram(message, image_data):
    files = {'photo': ('image.jpg', image_data)}
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'caption': message}
    requests.post(TELEGRAM_API_URL, files=files, data=payload)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No image selected"}), 400

    image_data = image_file.read()

    predicted_class, confidence = predict_disease(image_data)
    disease_solution = DISEASE_SOLUTIONS.get(predicted_class, "No solution available.")

    message = f"Prediction: {predicted_class}\nConfidence: {confidence}\nSolution: {disease_solution}"
    send_to_telegram(message, image_data)

    return jsonify({"message": "Image uploaded and processed successfully"}), 200

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video provided"}), 400

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No video selected"}), 400

    video_data = video_file.read()

    # Process the video (you need to implement this)

    return jsonify({"message": "Video uploaded and processed successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
