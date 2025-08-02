#!/bin/bash

set -e

# Create logs directory if not present
mkdir -p logs

echo "====================================================="
echo "     2JZ-GTE Predictive Monitoring Quick Start"
echo "====================================================="
echo "Which model backends would you like to run?"
echo "1) sklearn only"
echo "2) tensorflow only"
echo "3) both (default)"
read -p "Enter your choice [1/2/3]: " choice

# Set environment variables
export FLASK_ENV=production
export MODEL_PATH="./models/sklearn_model.pkl"
export TF_MODEL_PATH="./models/tf_model"

run_sklearn() {
    echo ">> Starting SKLearn Predictor (app.py)"
    nohup python3 app.py > logs/sklearn.log 2>&1 &
    echo ">> SKLearn backend running in background (PID $!)"
}

run_tensorflow() {
    echo ">> Starting TensorFlow Predictor (run_with_tf.py)"
    nohup python3 run_with_tf.py > logs/tensorflow.log 2>&1 &
    echo ">> TensorFlow backend running in background (PID $!)"
}

case $choice in
    1)
        run_sklearn
        ;;
    2)
        run_tensorflow
        ;;
    *)
        run_sklearn
        run_tensorflow
        ;;
esac

echo "====================================================="
echo "Backends started. Logs: logs/sklearn.log & logs/tensorflow.log"
echo "You may now access the system through the frontend."
echo "====================================================="