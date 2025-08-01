import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from pathlib import Path
import os

from backend.config import Config

def load_data(csv_path):
    return pd.read_csv(csv_path)

def preprocess_data(df):
    X = df.drop(columns=['failure'])  # assuming 'failure' is the label
    y = df['failure']
    return X, y

def train_and_save_model(csv_path: str, model_path: str = None):
    df = load_data(csv_path)
    X, y = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Model Evaluation:\n", classification_report(y_test, y_pred))

    output_path = model_path or Config.MODEL_PATH
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)

    print(f"Model saved to: {output_path}")

if __name__ == "__main__":
    data_path = os.getenv("TRAINING_DATA", "data/engine_data.csv")
    train_and_save_model(data_path)