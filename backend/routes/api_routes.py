from flask import request, jsonify
from . import api_blueprint
from model_handler import ModelHandler
from preprocess import preprocess_input

model_handler = ModelHandler()

@api_blueprint.route("/predict", methods=["POST"])
def predict():
    try:
        json_data = request.get_json()
        features = preprocess_input(json_data)
        prediction = model_handler.predict(features)
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400