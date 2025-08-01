# backend/inference/predict.py

import numpy as np

def make_prediction(model, data: dict):
    input_array = np.array([
        data["rpm"],
        data["boost"],
        data["afr"],
        data["oil_temp"],
        data["coolant_temp"],
        data["knock"]
    ]).reshape(1, -1)
    
    prediction = model.predict(input_array)[0]
    if hasattr(model, "predict_proba"):
        confidence = max(model.predict_proba(input_array)[0])
    else:
        confidence = 1.0  # Fallback for models without probability
    
    return prediction, float(round(confidence, 4))