from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet
import time
import random

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "SocketIO running."

@socketio.on('connect')
def on_connect():
    print("Client connected.")

def emit_sensor_data():
    while True:
        data = {
            "timestamp": time.time(),
            "rpm": random.randint(700, 7200),
            "boost": round(random.uniform(-0.5, 2.5), 2),
            "afr": round(random.uniform(11.5, 15.5), 2),
            "oil_temp": round(random.uniform(80, 120), 1),
            "coolant_temp": round(random.uniform(70, 110), 1),
            "knock": round(random.uniform(0, 2), 2)
        }
        socketio.emit('sensor_data', data)
        socketio.sleep(1/23.5999)  # ~42ms interval

if __name__ == '__main__':
    socketio.start_background_task(emit_sensor_data)
    socketio.run(app, port=5050)