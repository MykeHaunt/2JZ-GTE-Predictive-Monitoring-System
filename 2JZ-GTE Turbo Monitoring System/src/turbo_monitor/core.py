import logging
import os
import time
import threading
import queue
from datetime import datetime

import numpy as np
import obd
import pandas as pd
import joblib
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TurboMonitorCore:
    """
    Core class for turbocharger predictive monitoring with enhanced
    wireless latency handling and data smoothing.
    """
    SEQ_LENGTH = 10
    DATA_FILE = "data/synthetic_turbo_data.csv"
    MODEL_DIR = "models"
    SCALER_FILE = os.path.join(MODEL_DIR, "scaler.pkl")
    FAULT_MODEL = os.path.join(MODEL_DIR, "turbo_failure_predictor.h5")

    def __init__(self):
        os.makedirs(self.MODEL_DIR, exist_ok=True)
        self.features = [
            "RPM", "AFR", "EGT", "MAP", "TurboEfficiency",
            "KnockIndex", "BoostPressure", "OilTemp", "Vibration"
        ]
        self.scaler = MinMaxScaler()
        self.connection = self._connect_obd2()
        # For streaming data
        self._data_queue = queue.Queue(maxsize=100)
        self._stop_event = threading.Event()
        # Exponential moving average for smoothing and latency
        self.alpha = 0.2
        self._last_values = {feat: None for feat in self.features}
        self.latency_ema = None
        if self.connection:
            self._start_streaming_reader()

    def _connect_obd2(self, retries: int = 3, delay: float = 2.0):
        """Attempt to connect to the OBD-II interface, otherwise fall back to synthetic data."""
        for attempt in range(1, retries + 1):
            try:
                conn = obd.OBD()  # works over USB, Bluetooth, or WiFi ELM327
                if conn.is_connected():
                    logger.info("OBD-II connected successfully on attempt %d", attempt)
                    return conn
            except Exception as e:
                logger.error("OBD-II connection attempt %d failed: %s", attempt, e)
            time.sleep(delay)
        logger.warning("OBD-II not available – using synthetic data.")
        return None

    def _start_streaming_reader(self):
        """
        Launch a background thread to read sensor values continuously,
        measure latency, and apply exponential smoothing.
        """
        def reader():
            while not self._stop_event.is_set():
                start = datetime.utcnow()
                readings = {}
                for pid in self.features:
                    try:
                        # Map feature to OBD PID if configured; using watch() would be ideal
                        res = self.connection.query(getattr(obd.commands, pid.lower()), force=True)
                        value = float(res.value) if res.value is not None else np.nan
                    except Exception:
                        value = np.nan
                    # Smoothing
                    prev = self._last_values[pid]
                    if prev is None or np.isnan(prev):
                        smoothed = value
                    else:
                        smoothed = self.alpha * value + (1 - self.alpha) * prev
                    self._last_values[pid] = smoothed
                    readings[pid] = smoothed
                end = datetime.utcnow()
                latency = (end - start).total_seconds()
                # Update EMA of latency
                if self.latency_ema is None:
                    self.latency_ema = latency
                else:
                    self.latency_ema = self.alpha * latency + (1 - self.alpha) * self.latency_ema
                # Put in queue, dropping oldest if full
                try:
                    self._data_queue.put_nowait(readings)
                except queue.Full:
                    _ = self._data_queue.get_nowait()
                    self._data_queue.put_nowait(readings)
                # Adaptive sleep based on latency EMA
                interval = max(0.1, min(1.0, self.latency_ema * 2))
                time.sleep(interval)
        thread = threading.Thread(target=reader, daemon=True)
        thread.start()
        logger.info("Started background reader thread with adaptive interval.")

    def stop(self):
        """Stop the background reader."""
        self._stop_event.set()

    def get_latest_window(self) -> np.ndarray:
        """
        Retrieve the latest SEQ_LENGTH readings from the queue and
        return as a numpy array shaped (SEQ_LENGTH, n_features).
        """
        buffer = []
        while len(buffer) < self.SEQ_LENGTH:
            try:
                buffer.append(self._data_queue.get(timeout=1.0))
            except queue.Empty:
                break
        if len(buffer) < self.SEQ_LENGTH:
            raise RuntimeError("Insufficient data for prediction window.")
        arr = np.array([[d[feat] for feat in self.features] for d in buffer[-self.SEQ_LENGTH:]])
        return arr

    # ... existing methods build_model, train_model, predict remain unchanged ...
