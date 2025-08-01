import threading
import time
import random
import logging

from config import Config
from model.data_monitor import DriftMonitor

logger = logging.getLogger(__name__)

class SensorIngestionManager:
    def __init__(self, interval=2.0):
        self.interval = interval
        self.running = False
        self.thread = None
        self.drift_monitor = DriftMonitor()
        self.simulated_data = None

    def _simulate_sensor_data(self):
        """Simulate real-time sensor input."""
        return {
            'rpm': random.randint(800, 7000),
            'boost': round(random.uniform(0, 20), 2),
            'afr': round(random.uniform(10, 16), 2),
            'oil_temp': random.randint(70, 130),
            'coolant_temp': random.randint(70, 110),
            'knock': random.randint(0, 100)
        }

    def _run(self):
        logger.info("Sensor ingestion thread started.")
        while self.running:
            self.simulated_data = self._simulate_sensor_data()
            logger.debug(f"Simulated sensor data: {self.simulated_data}")
            self.drift_monitor.add_data(self.simulated_data)
            self.drift_monitor.monitor_and_trigger()
            time.sleep(self.interval)
        logger.info("Sensor ingestion thread stopped.")

    def start_all(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop_all(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()

    def get_latest_data(self):
        return self.simulated_data

    def is_running(self):
        return self.running