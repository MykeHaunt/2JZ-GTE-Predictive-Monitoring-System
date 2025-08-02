# test/test_socket_stream.py

import socketio
import time

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print("Test connected to server.")

@sio.on('sensor_data')
def on_data(data):
    print("Received:", data)
    assert 'rpm' in data
    assert 'boost' in data
    assert 'afr' in data
    assert 'coolant_temp' in data
    assert 'knock' in data
    sio.disconnect()

def test_websocket():
    try:
        sio.connect('http://localhost:5050')
        time.sleep(2)
    except Exception as e:
        print("Connection failed:", e)
        assert False

if __name__ == "__main__":
    test_websocket()