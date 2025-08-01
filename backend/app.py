from flask import Flask, request, jsonify
from model_handler import load_model, predict_engine_status
from utils.preprocessing import preprocess_input

app = Flask(__name__)

# Load model at startup
model = load_model("model.pkl")

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        input_data = request.get_json()
        processed = preprocess_input(input_data)
        prediction = predict_engine_status(model, processed)
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)