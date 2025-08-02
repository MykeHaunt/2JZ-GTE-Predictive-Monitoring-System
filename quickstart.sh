#!/bin/bash

echo "===================================="
echo "2JZ-GTE Predictive Monitoring System"
echo "===================================="
echo
echo "Choose model serving option:"
echo "1) SKLearn model only"
echo "2) TensorFlow model only"
echo "3) Both models (run in background)"
echo

read -p "Enter choice [1-3]: " CHOICE

# Python environment check
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is not installed."
    exit 1
fi

# Install dependencies
echo "🔧 Installing dependencies..."
pip install -r requirements.txt

# Activate model server(s)
case "$CHOICE" in
    1)
        echo "🚀 Launching SKLearn server (Flask)..."
        python3 backend/app.py
        ;;
    2)
        echo "🚀 Launching TensorFlow server (Flask)..."
        python3 backend/tf_server.py
        ;;
    3)
        echo "🚀 Launching both servers in background..."

        echo "  • SKLearn server on port 5000"
        nohup python3 backend/app.py > logs/sklearn_server.log 2>&1 &

        echo "  • TensorFlow server on port 5001"
        nohup python3 backend/tf_server.py > logs/tf_server.log 2>&1 &

        echo "✅ Both servers running in background."
        echo "   Logs: logs/sklearn_server.log | logs/tf_server.log"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac