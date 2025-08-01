import threading
import time
from backend.status.status_flags import SystemStatus
from backend.schema.sensor_data import SensorDataInput

class HardwareSensorIngestor:
    def __init__(self, update_callback, interval=1.5):
        self.update_callback = update_callback
        self.interval = interval
        self.running = False
        self.thread = None

    def _read_from_hardware(self):
        # TODO: Replace with real hardware reading logic (e.g., via python-can or OBD2)
        try:
            # Dummy placeholder for example
            return SensorDataInput(
                rpm=2200,
                boost=5.6,
                afr=13.2,
                oil_temp=85,
                coolant_temp=90,
                knock=0.15
            )
        except Exception as e:
            SystemStatus.update_status("hardware_ingestion_error", str(e))
            return None

    def _run(self):
        SystemStatus.update_status("hardware_ingestion", True)
        while self.running:
            data = self._read_from_hardware()
            if data:
                self.update_callback(data.dict())
            time.sleep(self.interval)
        SystemStatus.update_status("hardware_ingestion", False)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()