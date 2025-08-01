import joblib
import numpy as np

def load_model(path: str):
    try:
        model = joblib.load(path)
        return model
    except FileNotFoundError:
        raise RuntimeError(f"Model file not found at: {path}")

def predict_engine_status(model, features: np.ndarray) -> str:
    result = model.predict(features.reshape(1, -1))[0]
    return "FAILURE LIKELY" if result == 1 else "NORMAL"