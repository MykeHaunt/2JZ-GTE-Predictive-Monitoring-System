#!/usr/bin/env bash

set -euo pipefail

# ------------------ Configuration ------------------
PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
cd "$PROJECT_ROOT"
mkdir -p logs

# ------------------ Header -------------------------
echo "====================================================="
echo "       2JZ-GTE Predictive Monitoring Launcher"
echo "====================================================="
echo "Choose which backend(s) to run:"
echo "1) SKLearn only"
echo "2) TensorFlow only"
echo "3) Both (default)"
read -rp "Enter your choice [1/2/3]: " choice
choice="${choice:-3}"
echo "====================================================="

# ------------------ Search for Entrypoints -------------------------

# Find app.py or file that contains 'Flask' definition
ENTRY_SKLEARN=$(grep -Rl --include='*.py' -E 'Flask|app = Flask' . | grep -v 'run_with_tf' | head -n1 || true)
[ -n "$ENTRY_SKLEARN" ] || { echo "❌ Could not find SKLearn Flask entrypoint."; exit 1; }

# Find run_with_tf.py
ENTRY_TF=$(find . -type f -name 'run_with_tf.py' | head -n1 || true)
[ -n "$ENTRY_TF" ] || echo "⚠️ Warning: TensorFlow runner not found. Skipping TF launch."

# ------------------ Backend Launch Functions ----------------------

run_sklearn() {
    echo "▶ Starting SKLearn backend: $ENTRY_SKLEARN"
    nohup python3 "$ENTRY_SKLEARN" > logs/sklearn.log 2>&1 &
    echo "   ↳ PID $! | Logs: logs/sklearn.log"
}

run_tensorflow() {
    if [ -n "$ENTRY_TF" ]; then
        echo "▶ Starting TensorFlow backend: $ENTRY_TF"
        export TF_MODEL_PATH="${TF_MODEL_PATH:-./models/tf_model}"
        nohup python3 "$ENTRY_TF" > logs/tensorflow.log 2>&1 &
        echo "   ↳ PID $! | Logs: logs/tensorflow.log"
    else
        echo "⚠️ Skipping TensorFlow backend (file not found)."
    fi
}

# ------------------ Execution -----------------------

case "$choice" in
    1) run_sklearn ;;
    2) run_tensorflow ;;
    3|*) run_sklearn; run_tensorflow ;;
esac

# ------------------ Footer --------------------------

echo "====================================================="
echo "🟢 Backends launched. View logs in the ./logs/ folder."
echo "🛠 Use 'ps' or 'jobs -l' to manage running services."
echo "====================================================="