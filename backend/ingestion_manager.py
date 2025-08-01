from queue import Queue
import time
from backend.obd.ingestion import OBDIngestion
from backend.can.ingestion import CANIngestion

class SensorIngestionManager:
    def __init__(self):
        self.data_queue = Queue()
        self.obd_ingestion = OBDIngestion(self.data_queue)
        self.can_ingestion = CANIngestion(self.data_queue)

    def start_all(self):
        self.obd_ingestion.start()
        self.can_ingestion.start()

    def stop_all(self):
        self.obd_ingestion.stop()
        self.can_ingestion.stop()

    def run(self, duration_seconds=60):
        self.start_all()
        start_time = time.time()
        try:
            while time.time() - start_time < duration_seconds:
                while not self.data_queue.empty():
                    sensor_data = self.data_queue.get()
                    print("Received sensor data:", sensor_data)
                time.sleep(0.1)
        finally:
            self.stop_all()

if __name__ == "__main__":
    manager = SensorIngestionManager()
    manager.run()