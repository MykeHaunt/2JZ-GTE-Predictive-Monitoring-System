"""
Entry-point script to launch the Flask app with TensorFlow integration.
It monkey-patches backend.Predictor to use TensorFlowPredictor.
"""

import os
import sys

# Ensure project root is on PYTHONPATH
sys.path.insert(0, os.path.dirname(__file__))

# Import the TF predictor
from integrations.tensorflow.tf_predictor import TensorFlowPredictor

# Monkey-patch the existing Predictor class
import backend.predictor as pred_mod
pred_mod.Predictor = TensorFlowPredictor

# Now import and run the existing Flask app
from app import app  # existing Flask app in project root or backend/app.py

if __name__ == "__main__":
    # Optionally read host/port from env variables
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)