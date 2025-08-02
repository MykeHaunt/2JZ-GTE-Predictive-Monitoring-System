#!/bin/bash

# === Configuration ===
FLASK_APP="backend/app.py"
SOCKET_SERVER="backend/socket_server.py"
LOG_DIR="logs"
FLASK_LOG="$LOG_DIR/flask.log"
SOCKET_LOG="$LOG_DIR/socket.log"

# === Create log directory if not exists ===
mkdir -p "$LOG_DIR"

echo "🔧 Starting Flask API..."
nohup python3 "$FLASK_APP" > "$FLASK_LOG" 2>&1 &
FLASK_PID=$!
echo "✅ Flask running with PID $FLASK_PID (log: $FLASK_LOG)"

echo "🔧 Starting WebSocket server..."
nohup python3 "$SOCKET_SERVER" > "$SOCKET_LOG" 2>&1 &
SOCKET_PID=$!
echo "✅ Socket server running with PID $SOCKET_PID (log: $SOCKET_LOG)"

# === Save PIDs for later control ===
echo "$FLASK_PID" > .flask.pid
echo "$SOCKET_PID" > .socket.pid

echo "📡 Both services are now running in the background."