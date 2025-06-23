import logging
import os
import time

import numpy as np
import obd
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SEQ_LENGTH = 10
DATA_FILE = "data/synthetic_turbo_data.csv"
MODEL_DIR = "models/"
SCALER_FILE = os.path.join(MODEL_DIR, "scaler.pkl")
FAULT_MODEL = os.path.join(MODEL_DIR, "turbo_failure_predictor.h5")


class TurboMonitorCore:
    def __init__(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        self.connection = self._connect_obd2()
        self.scaler = MinMaxScaler()
        self.features = [
            "RPM", "AFR", "EGT", "MAP", "TurboEfficiency",
            "KnockIndex", "BoostPressure", "OilTemp", "Vibration"
        ]

    def _connect_obd2(self):
        for _ in range(3):
            try:
                connection = obd.OBD()
                if connection.is_connected():
                    logger.info("OBD-II connected successfully")
                    return connection
            except Exception as e:
                logger.error(f"OBD-II connection failed: {e}")
            time.sleep(2)
        logger.warning("Using synthetic data")
        return None

    def generate_data(self):
        if os.path.exists(DATA_FILE):
            return pd.read_csv(DATA_FILE)

        logger.info("Generating synthetic dataset...")
        total_samples = 36000
        timestamps = pd.date_range(start="2023-01-01", periods=total_samples, freq="10S")

        turbo_eff = np.linspace(1.0, 0.6, total_samples) + np.random.normal(0, 0.02, total_samples)
        boost_pressure = np.random.uniform(10, 25, total_samples) * turbo_eff

        dataset = pd.DataFrame({
            "Timestamp": timestamps,
            "RPM": np.random.randint(2000, 7000, total_samples),
            "AFR": np.random.uniform(11, 17, total_samples),
            "EGT": np.random.uniform(400, 950, total_samples),
            "MAP": np.random.uniform(50, 160, total_samples),
            "TurboEfficiency": turbo_eff,
            "KnockIndex": np.random.uniform(0.8, 1.5, total_samples),
            "BoostPressure": boost_pressure,
            "OilTemp": np.random.uniform(80, 120, total_samples),
            "Vibration": np.abs(np.random.normal(0, 1, total_samples) * (1 - turbo_eff))
        })

        dataset.to_csv(DATA_FILE, index=False)
        return dataset

    def build_model(self):
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(SEQ_LENGTH, len(self.features))),
            Dropout(0.3),
            LSTM(64),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer=Adam(0.001), loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train_model(self):
        data = pd.read_csv(DATA_FILE)
        X = data[self.features].values
        y = (data["TurboEfficiency"] < 0.7).astype(int)

        X_scaled = self.scaler.fit_transform(X)
        X_seq = np.array([X_scaled[i - SEQ_LENGTH:i] for i in range(SEQ_LENGTH, len(X_scaled))])
        y_seq = y[SEQ_LENGTH:]

        X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2)
        model = self.build_model()

        model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=64,
            validation_data=(X_test, y_test),
            callbacks=[
                tf.keras.callbacks.EarlyStopping(patience=10),
                tf.keras.callbacks.ModelCheckpoint(FAULT_MODEL, save_best_only=True)
            ]
        )

        pd.to_pickle(self.scaler, SCALER_FILE)
        return model