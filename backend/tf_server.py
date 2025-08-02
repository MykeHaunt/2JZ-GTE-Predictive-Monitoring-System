from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the saved model
MODEL_PATH = "model/tf_model"
model = tf.keras.models.load_model(MODEL_PATH)

@app.route("/predict-tf", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = np.array([
            data["rpm"],
            data["boost"],
            data["afr"],
            data["oil_temp"],
            data["coolant_temp"],
            data["knock"]
        ]).reshape(1, -1)

        prediction = model.predict(features)
        result = float(prediction[0][0])
        return jsonify({"confidence": result, "failure_likely": result > 0.5})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/health-tf")
def health():
    return jsonify({"status": "TensorFlow model online"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)