from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
from backend.ingestion_manager import SensorIngestionManager
from backend.model.predictor import Predictor
from backend.api.routes.status import status_bp
from threading import Lock

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend access

# Initialize components
ingestion_manager = SensorIngestionManager()
predictor = Predictor()
data_lock = Lock()

# Shared state for latest data and predictions
latest_sensor_data = None
latest_prediction = None

# Register ingestion manager globally for use in blueprints
app.config['INGESTION_MANAGER'] = ingestion_manager

# Register the status blueprint
app.register_blueprint(status_bp)


@app.before_first_request
def start_ingestion():
    """
    Starts all sensor ingestion threads before handling the first request.
    """
    ingestion_manager.start_all()


@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    """
    Returns the latest ingested sensor data.
    """
    with data_lock:
        if latest_sensor_data is None:
            return jsonify({'message': 'No sensor data available'}), 204
        return jsonify(latest_sensor_data), 200


@app.route('/api/prediction', methods=['GET'])
def get_prediction():
    """
    Returns the latest prediction result based on sensor data.
    """
    with data_lock:
        if latest_prediction is None:
            return jsonify({'message': 'No prediction available'}), 204
        return jsonify(latest_prediction), 200


@app.route('/api/update', methods=['POST'])
def update_data():
    """
    Accepts JSON sensor data, validates it, updates the global state,
    and triggers prediction using the ML model.
    """
    global latest_sensor_data, latest_prediction

    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415

    sensor_data = request.json.get('sensor_data')
    if not sensor_data:
        return jsonify({'error': 'No sensor data provided'}), 400

    # Validate sensor_data keys and types (basic)
    expected_keys = {'rpm', 'boost', 'afr', 'oil_temp', 'coolant_temp', 'knock'}
    if not expected_keys.issubset(sensor_data.keys()):
        return jsonify({'error': f'Missing keys in sensor_data. Required keys: {expected_keys}'}), 400

    try:
        # Typecast and validate each input
        sensor_data_validated = {
            'rpm': int(sensor_data['rpm']),
            'boost': float(sensor_data['boost']),
            'afr': float(sensor_data['afr']),
            'oil_temp': float(sensor_data['oil_temp']),
            'coolant_temp': float(sensor_data['coolant_temp']),
            'knock': int(sensor_data['knock'])
        }
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid sensor data types: {str(e)}'}), 400

    # Update state and predict
    with data_lock:
        latest_sensor_data = sensor_data_validated
        try:
            latest_prediction = predictor.predict(sensor_data_validated)
        except Exception as e:
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

    return jsonify({'status': 'updated'}), 200


@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint.
    """
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    # Production deployment should use a WSGI server such as Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=False)