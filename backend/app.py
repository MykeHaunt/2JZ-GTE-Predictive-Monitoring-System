from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.ingestion_manager import SensorIngestionManager
from backend.model.predictor import Predictor
from threading import Lock

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

ingestion_manager = SensorIngestionManager()
predictor = Predictor()
data_lock = Lock()
latest_sensor_data = None
latest_prediction = None

@app.before_first_request
def start_ingestion():
    ingestion_manager.start_all()

@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    with data_lock:
        if latest_sensor_data is None:
            return jsonify({'message': 'No data available'}), 204
        return jsonify(latest_sensor_data)

@app.route('/api/prediction', methods=['GET'])
def get_prediction():
    with data_lock:
        if latest_prediction is None:
            return jsonify({'message': 'No prediction available'}), 204
        return jsonify(latest_prediction)

@app.route('/api/update', methods=['POST'])
def update_data():
    global latest_sensor_data, latest_prediction
    sensor_data = request.json.get('sensor_data')
    if not sensor_data:
        return jsonify({'error': 'No sensor data provided'}), 400
    with data_lock:
        latest_sensor_data = sensor_data
        latest_prediction = predictor.predict(sensor_data)
    return jsonify({'status': 'updated'}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)