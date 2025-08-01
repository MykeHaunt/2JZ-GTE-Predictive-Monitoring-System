import joblib
import numpy as np
import logging
from config import Config

class Predictor:
    def __init__(self, model_path=None):
        """
        Loads the pre-trained model from the specified path.
        """
        self.model_path = model_path or Config.MODEL_PATH
        try:
            self.model = joblib.load(self.model_path)
            logging.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logging.error(f"Failed to load model from {self.model_path}: {e}")
            self.model = None

    def predict(self, sensor_data: dict) -> dict:
        """
        Predicts engine health from sensor input dictionary.

        Args:
            sensor_data (dict): {
                "rpm": int,
                "boost": float,
                "afr": float,
                "oil_temp": float,
                "coolant_temp": float,
                "knock": float
            }

        Returns:
            dict: {
                "prediction": str,
                "confidence": float
            }
        """
        if self.model is None:
            return {"error": "Model not loaded"}

        try:
            features = self._extract_features(sensor_data)
            proba = self.model.predict_proba([features])[0]
            label = self.model.predict([features])[0]

            return {
                "prediction": str(label),
                "confidence": round(float(np.max(proba)), 4)
            }

        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            return {"error": "Prediction error"}

    def _extract_features(self, data: dict) -> list:
        """
        Converts raw input dict to model-compatible feature list.

        Returns:
            list: [rpm, boost, afr, oil_temp, coolant_temp, knock]
        """
        keys = ["rpm", "boost", "afr", "oil_temp", "coolant_temp", "knock"]
        try:
            return [float(data[key]) for key in keys]
        except KeyError as ke:
            logging.error(f"Missing key in sensor data: {ke}")
            raise
        except ValueError as ve:
            logging.error(f"Invalid data format in sensor data: {ve}")
            raise