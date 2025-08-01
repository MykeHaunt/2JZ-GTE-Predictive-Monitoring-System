import os
import pandas as pd
import joblib
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from datetime import datetime
from config import Config

logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

REQUIRED_COLUMNS = ["rpm", "boost", "afr", "oil_temp", "coolant_temp", "knock", "label"]

def load_training_data(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        logging.error(f"Training data file not found: {file_path}")
        raise FileNotFoundError(f"Data file not found: {file_path}")
    data = pd.read_csv(file_path)
    if not all(col in data.columns for col in REQUIRED_COLUMNS):
        logging.error("Missing required columns in training data.")
        raise ValueError("Training data missing required columns.")
    return data

def preprocess_data(df: pd.DataFrame):
    X = df[["rpm", "boost", "afr", "oil_temp", "coolant_temp", "knock"]]
    y = df["label"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def retrain_model(data_path: str = "data/training_data.csv", save_path: str = Config.MODEL_PATH):
    try:
        logging.info("Retraining initiated.")
        df = load_training_data(data_path)
        X_train, X_test, y_train, y_test = preprocess_data(df)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        joblib.dump(model, save_path)

        logging.info(f"Model retrained and saved to {save_path}")
        logging.info(f"Retraining Accuracy: {acc:.4f}")
        logging.info(f"Classification Report:\n{report}")

        return {
            "status": "success",
            "accuracy": acc,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logging.exception("Retraining failed.")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    result = retrain_model()
    print(result)