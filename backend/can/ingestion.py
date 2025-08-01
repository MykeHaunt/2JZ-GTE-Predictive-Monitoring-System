import threading
import time
from queue import Queue

class CANIngestion:
    """
    Handles ingestion of live CAN Bus frames and decodes sensor information.
    Data is parsed and pushed to a queue for downstream processing.
    """

    def __init__(self, data_queue: Queue, interface: str = "can0", polling_interval: float = 0.1):
        """
        :param data_queue: Queue to push sensor data dictionaries
        :param interface: CAN interface name
        :param polling_interval: Time between polls
        """
        self.data_queue = data_queue
        self.interface = interface
        self.polling_interval = polling_interval
        self._running = False
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()

    def _poll_loop(self):
        while self._running:
            can_frame = self.read_can_frame()
            if can_frame:
                sensor_data = self.decode_can_frame(can_frame)
                if sensor_data:
                    self.data_queue.put(sensor_data)
            time.sleep(self.polling_interval)

    def read_can_frame(self):
        """
        Stub for reading CAN frames from interface.
        Replace with actual python-can or socketcan code.
        Returns a raw CAN frame.
        """
        # Simulated CAN frame data
        import random
        frame_id = 0x100
        data = [random.randint(0, 255) for _ in range(8)]
        return {'id': frame_id, 'data': data}

    def decode_can_frame(self, frame):
        """
        Decode CAN frame data into sensor values.
        Returns dict of sensor readings or None if not recognized.
        """
        # Example decoding logic, to be customized per vehicle CAN protocol
        if frame['id'] == 0x100:
            rpm = frame['data'][0] * 256 + frame['data'][1]
            throttle = frame['data'][2] * 100 / 255
            engine_temp = frame['data'][3] - 40  # Example offset
            return {
                'rpm': rpm,
                'throttle_pos': throttle,
                'engine_temp': engine_temp
            }
        return None