import numpy as np

def preprocess_input(data: dict) -> np.ndarray:
    try:
        return np.array([
            data["rpm"],
            data["boost"],
            data["afr"],
            data["oil_temp"],
            data["coolant_temp"],
            data["knock"]
        ])
    except KeyError as e:
        raise ValueError(f"Missing required input: {str(e)}")