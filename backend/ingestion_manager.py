# backend/ingestion_manager.py

import logging
from queue import Queue
from backend.obd.ingestion import OBDIngestion
from backend.can.ingestion import CANIngestion

class SensorIngestionManager:
    """
    Manages live sensor ingestion from OBD-II and CAN.
    Provides a queue of sensor-data dicts to consuming code.
    """

    def __init__(self, polling_interval=1.0):
        self.data_queue = Queue()
        self.logger = logging.getLogger(__name__)

        # initialize ingestion modules
        self.obd_ingester = OBDIngestion(self.data_queue, polling_interval)
        self.can_ingester = CANIngestion(self.data_queue, polling_interval / 10)

    def start_all(self):
        """
        Start both OBD and CAN ingestion threads.
        """
        self.logger.info("Starting OBD ingestion...")
        self.obd_ingester.start()
        self.logger.info("Starting CAN ingestion...")
        self.can_ingester.start()

    def stop_all(self):
        """
        Stop ingestion threads gracefully.
        """
        self.logger.info("Stopping OBD ingestion...")
        self.obd_ingester.stop()
        self.logger.info("Stopping CAN ingestion...")
        self.can_ingester.stop()

    def get_latest(self):
        """
        Retrieve the most recent sensor data dict from the queue.
        Non-blocking. Returns None if no new data.
        """
        try:
            # drain entire queue, but return only last
            latest = None
            while True:
                latest = self.data_queue.get_nowait()
        except Exception:
            return latest