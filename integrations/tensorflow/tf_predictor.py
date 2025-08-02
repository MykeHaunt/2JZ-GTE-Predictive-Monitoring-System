import os
import numpy as np
import tensorflow as tf
from backend.predictor import Predictor  # existing Predictor interface

class TensorFlowPredictor(Predictor):
    """
    A drop-in replacement for the existing Predictor, using a TensorFlow SavedModel.
    Expects six sensor inputs in the same order: rpm, boost, afr, oil_temp,
    coolant_temp, knock.
    """

    def __init__(self, model_path: str = None):
        """
        Load a TensorFlow SavedModel from disk.
        If model_path is not provided, defaults to environment variable TF_MODEL_PATH.
        """
        path = model_path or os.getenv("TF_MODEL_PATH")
        if not path:
            raise ValueError("TF_MODEL_PATH must be set to your SavedModel directory or .pb file")
        self.model = tf.saved_model.load(path)

    def predict(self, sensor_values: dict) -> dict:
        """
        sensor_values: dict with keys ['rpm','boost','afr','oil_temp','coolant_temp','knock']
        Returns: { 'failure_probability': float, 'confidence_score': float }
        """
        # Prepare input array in correct order
        inputs = np.array([[
            sensor_values['rpm'],
            sensor_values['boost'],
            sensor_values['afr'],
            sensor_values['oil_temp'],
            sensor_values['coolant_temp'],
            sensor_values['knock']
        ]], dtype=np.float32)

        # Assume the SavedModel has a 'serving_default' signature returning a single tensor
        infer = self.model.signatures["serving_default"]
        output = infer(tf.constant(inputs))

        # Extract prediction; adapt keys if your model uses different signature names
        # Here we assume output contains 'probabilities' and 'confidence'
        probs = output.get('probabilities') or output.get('output_0')
        confs = output.get('confidence') or output.get('output_1')

        failure_prob = float(probs.numpy().squeeze())
        confidence_score = float(confs.numpy().squeeze()) if confs is not None else 1.0

        return {
            'failure_probability': failure_prob,
            'confidence_score': confidence_score
        }