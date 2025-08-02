#!/bin/bash

echo "=============================================="
echo "2JZ-GTE Predictive Monitoring System - Launcher"
echo "=============================================="
echo
echo "Choose model serving option:"
echo "1) SKLearn model only"
echo "2) TensorFlow model only"
echo "3) Both models (run in background)"
echo

read -p "Enter choice [1-3]: " CHOICE

# Check Python installation
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is not installed or not in PATH."
    exit 1
fi

# Check pip installation
if ! command -v pip &>/dev/null; then
    echo "❌ pip is not installed."
    exit 1
fi

# Uninstall TensorFlow to ensure clean install
echo "♻️  Uninstalling any existing TensorFlow installations..."
pip uninstall -y tensorflow tensorflow-cpu tensorflow-gpu || true

# Install dependencies
echo "🔧 Installing required Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create logs directory if not exists
mkdir -p logs

# Start model servers
case "$CHOICE" in
    1)
        echo "🚀 Starting SKLearn server (port 5000)..."
        python3 backend/app.py
        ;;
    2)
        echo "🚀 Starting TensorFlow server (port 5001)..."
        python3 backend/tf_server.py
        ;;
    3)
        echo "🚀 Starting both SKLearn and TensorFlow servers in background..."
        echo "  • SKLearn server → http://localhost:5000"
        nohup python3 backend/app.py > logs/sklearn_server.log 2>&1 &

        echo "  • TensorFlow server → http://localhost:5001"
        nohup python3 backend/tf_server.py > logs/tf_server.log 2>&1 &

        echo
        echo "✅ Both servers are now running in the background."
        echo "🗂️  Logs:"
        echo "   - logs/sklearn_server.log"
        echo "   - logs/tf_server.log"
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac