# backend/socket_server.py

import time
from flask import Flask
from flask_socketio import SocketIO
import eventlet
import random  # Replace with real data source in production

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "2JZ-GTE Predictive Monitoring WebSocket Server is active."

@socketio.on('connect')
def handle_connect():
    print(f"[{time.strftime('%X')}] Client connected.")

def generate_sensor_data():
    """
    Replace this function with actual sensor input pipeline.
    """
    return {
        "timestamp": time.time(),
        "rpm": random.randint(700, 7200),
        "boost": round(random.uniform(-0.3, 2.2), 2),
        "afr": round(random.uniform(11.2, 15.1), 2),
        "oil_temp": round(random.uniform(80, 125), 1),
        "coolant_temp": round(random.uniform(70, 108), 1),
        "knock": round(random.uniform(0, 2.0), 2)
    }

def emit_data_loop():
    while True:
        data = generate_sensor_data()
        socketio.emit('sensor_data', data)
        socketio.sleep(1 / 23.5999)

if __name__ == '__main__':
    print("Starting WebSocket telemetry server...")
    socketio.start_background_task(emit_data_loop)
    socketio.run(app, host='0.0.0.0', port=5050)