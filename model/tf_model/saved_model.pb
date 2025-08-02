# train_and_export_tf_model.py
import tensorflow as tf
import numpy as np
import os

# Dummy model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(6,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy')

# Dummy training
X = np.random.rand(100, 6)
y = np.random.randint(0, 2, size=(100, 1))
model.fit(X, y, epochs=5, verbose=0)

# Export
os.makedirs("model", exist_ok=True)
model.save("model/tf_model")