import tensorflow as tf
import numpy as np
import os

# Simulated sensor data: rpm, boost, afr, oil_temp, coolant_temp, knock
X_dummy = np.random.rand(100, 6).astype(np.float32)
y_dummy = np.random.randint(0, 2, size=(100, 1)).astype(np.float32)

# Define a minimal binary classification model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(6,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_dummy, y_dummy, epochs=5, batch_size=10, verbose=1)

# Create target directory if not exists
export_path = 'model/tf_model'
os.makedirs(export_path, exist_ok=True)

# Save in SavedModel format
model.save(export_path)
print(f"Model saved to {export_path}")