import logging
import numpy as np
import pandas as pd
import joblib
from backend.config import Config

logger = logging.getLogger(__name__)

class Predictor:
    def __init__(self, model_path=Config.MODEL_PATH):
        """
        Load the pre-trained predictive model.

        :param model_path: Path to the serialized model file
        """
        try:
            self.model = joblib.load(model_path)
            logger.info(f"Loaded model from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model from {model_path}: {e}")
            raise e

    def preprocess(self, sensor_data: dict) -> np.ndarray:
        """
        Preprocess raw sensor data dictionary to model input feature vector.

        :param sensor_data: Dictionary of sensor readings, e.g.,
            {
                'rpm': 3500,
                'throttle_pos': 45.6,
                'engine_temp': 90.1,
                ...
            }
        :return: numpy array of features aligned with the model's expected input shape
        """
        # Define feature order consistent with training
        feature_order = ['rpm', 'throttle_pos', 'engine_temp', 'maf']

        # Extract features in order, use 0 or NaN for missing features
        features = []
        for feat in feature_order:
            val = sensor_data.get(feat, np.nan)
            features.append(val)
        features_array = np.array(features, dtype=np.float32)

        # Example: fill missing values with mean or zero
        features_array = np.nan_to_num(features_array, nan=0.0)

        logger.debug(f"Preprocessed features: {features_array}")
        return features_array.reshape(1, -1)  # Model expects 2D input

    def predict(self, sensor_data: dict) -> dict:
        """
        Perform prediction on live sensor data.

        :param sensor_data: Raw sensor data dict
        :return: Prediction dict, e.g., {'failure_probability': 0.75, 'alert': True}
        """
        features = self.preprocess(sensor_data)

        # Predict probability or regression value
        try:
            prob = self.model.predict_proba(features)[:, 1][0]
            alert = prob > 0.7  # Threshold for alert, adjustable
            result = {
                'failure_probability': float(prob),
                'alert': alert
            }
            logger.info(f"Prediction result: {result}")
            return result
        except AttributeError:
            # Model does not support predict_proba (e.g., regression)
            val = self.model.predict(features)[0]
            alert = val > 0.7
            result = {
                'prediction_value': float(val),
                'alert': alert
            }
            logger.info(f"Regression prediction result: {result}")
            return result
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {'error': str(e)}