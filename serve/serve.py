import NLP
import pickle
import sklearn
from rating import default_user, predict_rating_for_user
import pandas as pd
from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    text = data["text"]
    user_profile = data.get("user", default_user)

    model = NLP.load_model("Model.keras")
    vectorizer = NLP.Load_Vectorizer("Model.ftz")
    rating_regressor = pickle.load(open("rating_regressor.pkl", "rb"))
    print("Model loaded")

    output = NLP.Predict([data["text"]], model, vectorizer)[0]
    categories = NLP.Decode_Genre(output)
    rating = predict_rating_for_user(rating_regressor, categories, user_profile)

    return jsonify({"categories": categories, "rating": rating})


app.run(
    host="0.0.0.0",
    port=5000,
    debug=True,
)

"""
COMMAND TO TEST THE API:
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text": "Angela Basset was good as expected, but Whitney has no Range as an actress. The screenplay also neglected to portray, on film, the greatness of this novel.  Instead of promoting sisterhood, they emphasized the canine-qualities of men.  Read the book; rent Soul Food instead!"}'
"""
