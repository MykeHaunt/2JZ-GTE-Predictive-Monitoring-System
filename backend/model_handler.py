import joblib
import config
import os

class ModelHandler:
    def __init__(self, model_path=config.Config.MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.model = joblib.load(model_path)

    def predict(self, features):
        return self.model.predict([features])[0]