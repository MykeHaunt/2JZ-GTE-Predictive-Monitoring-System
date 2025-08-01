import time
import threading
import random
from backend.schema.sensor_data import SensorDataInput
from backend.status.status_flags import SystemStatus

class SimulatedSensorIngestor:
    def __init__(self, update_callback, interval=2.0):
        self.update_callback = update_callback
        self.interval = interval  # Seconds between data updates
        self.running = False
        self.thread = None

    def _generate_sensor_data(self):
        return SensorDataInput(
            rpm=random.randint(800, 7200),
            boost=round(random.uniform(-1.0, 20.0), 2),
            afr=round(random.uniform(10.0, 16.0), 2),
            oil_temp=random.randint(60, 120),
            coolant_temp=random.randint(70, 110),
            knock=random.uniform(0.0, 5.0)
        )

    def _run(self):
        SystemStatus.update_status('simulated_ingestion', True)
        while self.running:
            data = self._generate_sensor_data()
            self.update_callback(data.dict())
            time.sleep(self.interval)
        SystemStatus.update_status('simulated_ingestion', False)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()