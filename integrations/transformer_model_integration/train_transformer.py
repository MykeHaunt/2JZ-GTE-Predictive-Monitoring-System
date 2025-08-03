import numpy as np
import joblib
from data_preparation import create_sequences, scaler, scaled_data
from model.transformer_model import build_transformer

X, y = create_sequences(scaled_data, 60)
train_split = int(0.8 * len(X))
X_train, y_train = X[:train_split], y[:train_split]
X_test, y_test = X[train_split:], y[train_split:]

model = build_transformer(
    input_shape=(60, X_train.shape[2]),
    head_size=32,
    num_heads=4,
    ff_dim=64,
    num_layers=2
)
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)

model.save('model/transformer_model.h5')
joblib.dump(scaler, 'model/scaler.pkl')