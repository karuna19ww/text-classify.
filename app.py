from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pickle

app = Flask(__name__)
CORS(app)

# Project folders
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FRONTEND_FOLDER = os.path.join(BASE_DIR, "frontend")
MODEL_FOLDER = os.path.join(BASE_DIR, "modell")


# Load trained model
with open(os.path.join(MODEL_FOLDER, "model.pkl"), "rb") as file:
    model = pickle.load(file)

# Load TF-IDF vectorizer
with open(os.path.join(MODEL_FOLDER, "vectorizer.pkl"), "rb") as file:
    vectorizer = pickle.load(file)


# Home page
@app.route("/")
def home():
    return send_from_directory(FRONTEND_FOLDER, "index.html")


# Frontend files
@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)


# Fake news prediction
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()
    news = data.get("news", "")

    # Check for empty input
    if not news.strip():
        return jsonify({
            "prediction": "Please enter some news.",
            "confidence": 0
        })

    # Convert text to TF-IDF features
    news_vector = vectorizer.transform([news])

    # Make prediction
    prediction = model.predict(news_vector)[0]

    # Get probabilities
    probabilities = model.predict_proba(news_vector)[0]

    # WELFake labels:
    # 0 = FAKE
    # 1 = REAL

    if prediction == 1:
        result = "REAL NEWS"
    else:
        result = "FAKE NEWS"

    # Highest probability
    confidence = max(probabilities) * 100

    return jsonify({
        "prediction": result,
        "confidence": round(confidence, 2)
    })


# Start Flask
if __name__ == "__main__":
    app.run(debug=True)