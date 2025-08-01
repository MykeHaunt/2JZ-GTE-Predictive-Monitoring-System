import logging
import time
from queue import Queue
from backend.ingestion_manager import SensorIngestionManager
from backend.model.predictor import Predictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    manager = SensorIngestionManager()
    predictor = Predictor()

    manager.start_all()

    try:
        while True:
            while not manager.data_queue.empty():
                sensor_data = manager.data_queue.get()
                prediction = predictor.predict(sensor_data)
                logger.info(f"Sensor Data: {sensor_data} -> Prediction: {prediction}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info("Stopping live prediction...")
    finally:
        manager.stop_all()

if __name__ == "__main__":
    main()