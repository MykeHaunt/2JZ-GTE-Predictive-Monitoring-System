import pandas as pd
import joblib
from sklearn.metrics import classification_report
from backend.config import Config

def validate_model(model_path: str, validation_data_path: str):
    model = joblib.load(model_path)
    df = pd.read_csv(validation_data_path)

    X = df.drop(columns=['failure'])
    y = df['failure']

    y_pred = model.predict(X)
    report = classification_report(y, y_pred, output_dict=True)
    
    print("Validation Report:\n", classification_report(y, y_pred))
    return report