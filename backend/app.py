from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.ingestion_manager import SensorIngestionManager
from backend.model.predictor import Predictor
from threading import Lock
import logging
from config import Config

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Logging configuration
logging.basicConfig(filename=Config.LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Core components
ingestion_manager = SensorIngestionManager()
predictor = Predictor(model_path=Config.MODEL_PATH)

# Thread-safe global data
data_lock = Lock()
latest_sensor_data = None
latest_prediction = None

@app.before_first_request
def start_ingestion():
    """
    Starts all sensor data ingestion threads before serving the first request.
    """
    ingestion_manager.start_all()
    app.logger.info("Sensor ingestion threads started.")

@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    """
    Returns the latest sensor data ingested.
    """
    with data_lock:
        if latest_sensor_data is None:
            return jsonify({'message': 'No data available'}), 204
        return jsonify(latest_sensor_data)

@app.route('/api/prediction', methods=['GET'])
def get_prediction():
    """
    Returns the latest prediction result from ingested data.
    """
    with data_lock:
        if latest_prediction is None:
            return jsonify({'message': 'No prediction available'}), 204
        return jsonify(latest_prediction)

@app.route('/api/update', methods=['POST'])
def update_data():
    """
    Accepts sensor data from frontend and computes a new prediction.
    """
    global latest_sensor_data, latest_prediction

    try:
        payload = request.get_json()
        sensor_data = payload.get('sensor_data')

        if not sensor_data:
            return jsonify({'error': 'Missing sensor_data'}), 400

        with data_lock:
            latest_sensor_data = sensor_data
            latest_prediction = predictor.predict(sensor_data)

        return jsonify({'status': 'updated'}), 200

    except Exception as e:
        app.logger.error(f"Error in /api/update: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check for API uptime.
    """
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)