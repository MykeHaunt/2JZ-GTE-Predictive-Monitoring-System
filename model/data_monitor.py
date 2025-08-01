import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime
from sklearn.metrics import mean_squared_error
from model.predictor import Predictor
from model.train_model import train_model
from config import Config

logger = logging.getLogger(__name__)

class DriftMonitor:
    def __init__(self, threshold=0.05):
        self.threshold = threshold
        self.predictor = Predictor()
        self.recent_data = []
        self.window_size = 100

    def add_data(self, data: dict):
        if len(self.recent_data) >= self.window_size:
            self.recent_data.pop(0)
        self.recent_data.append(data)

    def detect_drift(self):
        if len(self.recent_data) < self.window_size:
            return False

        df = pd.DataFrame(self.recent_data)
        preds = [self.predictor.predict(row.to_dict())['prediction'] for _, row in df.iterrows()]

        predicted_mean = np.mean(preds)
        actual_mean = df.mean(numeric_only=True).mean()

        drift_value = abs(predicted_mean - actual_mean)
        logger.info(f"Drift value: {drift_value}")

        return drift_value > self.threshold

    def monitor_and_trigger(self):
        if self.detect_drift():
            logger.warning("Drift detected! Triggering retraining.")
            try:
                train_model(Config.DEFAULT_TRAINING_DATA, Config.MODEL_PATH)
                logger.info("Model retrained successfully after drift.")
            except Exception as e:
                logger.error(f"Retraining failed: {str(e)}")