from flask import Blueprint, jsonify, current_app

status_bp = Blueprint('status', __name__)

@status_bp.route('/api/monitor_status', methods=['GET'])
def monitor_status():
    try:
        ingestion_manager = current_app.config['INGESTION_MANAGER']
        drift_monitor = ingestion_manager.drift_monitor

        status_report = {
            'ingestion_running': ingestion_manager.is_running(),
            'latest_data': ingestion_manager.get_latest_data(),
            'drift_detected': drift_monitor.drift_detected,
            'drift_score': drift_monitor.last_drift_score,
            'retraining_triggered': drift_monitor.retraining_triggered
        }
        return jsonify(status_report), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve monitor status: {str(e)}'}), 500