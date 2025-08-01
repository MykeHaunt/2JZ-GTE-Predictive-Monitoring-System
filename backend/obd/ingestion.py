import threading
import time
from queue import Queue

class OBDIngestion:
    """
    Simulates or interfaces with an OBD-II sensor stream.
    Reads real-time OBD data and pushes parsed sensor readings to a queue for processing.
    """

    def __init__(self, data_queue: Queue, polling_interval: float = 1.0):
        """
        :param data_queue: Queue to push sensor data dictionaries
        :param polling_interval: Time in seconds between reads
        """
        self.data_queue = data_queue
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
            sensor_data = self.read_obd_data()
            if sensor_data:
                self.data_queue.put(sensor_data)
            time.sleep(self.polling_interval)

    def read_obd_data(self):
        """
        Stub for actual OBD-II data reading.
        Replace with real OBD interface code.
        Returns a dict of sensor values, e.g.:
        {
            'rpm': 3000,
            'throttle_pos': 45.6,
            'engine_temp': 92.3,
            ...
        }
        """
        # Simulated data for demonstration
        import random
        return {
            'rpm': random.randint(700, 6000),
            'throttle_pos': random.uniform(0, 100),
            'engine_temp': random.uniform(70, 110),
            'maf': random.uniform(0.1, 5.0)
        }