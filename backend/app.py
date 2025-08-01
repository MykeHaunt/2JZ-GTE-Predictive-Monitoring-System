from flask import Flask, request, jsonify
import pandas as pd
import joblib
import logging
from datetime import datetime

app = Flask(__name__)
model = joblib.load('model.pkl')

logging.basicConfig(filename='logs/api.log', level=logging.INFO)

@app.route('/')
def home():
    return jsonify({"message": "2JZ-GTE Predictive Monitoring API v1.0"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]
        status = 'Potential Failure' if prediction else 'Normal'
        logging.info(f"{datetime.now()} | Prediction: {status} | Input: {data}")
        return jsonify({'status': status}), 200
    except Exception as e:
        logging.error(f"{datetime.now()} | Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)