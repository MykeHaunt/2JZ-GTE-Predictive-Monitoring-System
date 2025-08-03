import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import joblib

app = Flask(__name__)
model = load_model('model/transformer_model.h5')
scaler = joblib.load('model/scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['data']
    scaled_data = scaler.transform(data)
    prediction = model.predict(np.array([scaled_data]))
    predicted_values = scaler.inverse_transform(prediction)[0]
    return jsonify(prediction=predicted_values.tolist())

if __name__ == '__main__':
    app.run(debug=True)