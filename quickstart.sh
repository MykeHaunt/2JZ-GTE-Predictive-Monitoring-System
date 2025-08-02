#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(pwd)"
cd "$PROJECT_ROOT"

mkdir -p logs

echo "====================================================="
echo "     2JZ-GTE Predictive Monitoring Quick Start"
echo "====================================================="
echo "Choose which model backends to run:"
echo "1) SKLearn only"
echo "2) TensorFlow only"
echo "3) Both (default)"
read -rp "Enter your choice [1/2/3]: " choice
choice="${choice:-3}"
echo "====================================================="

# ------------------ Entrypoints ----------------------
ENTRY_SKLEARN="app.py"
ENTRY_TF="run_with_tf.py"

# ------------------ Run functions --------------------
run_sklearn() {
    if [ -f "$ENTRY_SKLEARN" ]; then
        export MODEL_PATH="${MODEL_PATH:-./model/sklearn_model.pkl}"
        echo "▶ Starting SKLearn backend using $ENTRY_SKLEARN"
        nohup python3 "$ENTRY_SKLEARN" > logs/sklearn.log 2>&1 &
        echo "   ↳ PID $! | Logs: logs/sklearn.log"
    else
        echo "❌ SKLearn entrypoint not found."
    fi
}

run_tensorflow() {
    if [ -f "$ENTRY_TF" ]; then
        export TF_MODEL_PATH="${TF_MODEL_PATH:-./model/tf_model}"
        echo "▶ Starting TensorFlow backend using $ENTRY_TF"
        nohup python3 "$ENTRY_TF" > logs/tensorflow.log 2>&1 &
        echo "   ↳ PID $! | Logs: logs/tensorflow.log"
    else
        echo "❌ TensorFlow entrypoint not found."
    fi
}

# ------------------ Execution ------------------------
case "$choice" in
    1) run_sklearn ;;
    2) run_tensorflow ;;
    3|*) run_sklearn; run_tensorflow ;;
esac

echo "====================================================="
echo "✅ Backends launched. Logs available in ./logs/"
echo "🛠 Use 'ps' or 'jobs -l' to monitor running processes"
echo "====================================================="