#!/bin/bash
# Quickstart Script for 2JZ-GTE Predictive Monitoring System
# This script sets up the Python environment, launches the backend service,
# and serves the frontend web application.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Initializing the environment..."

# Check for Python dependencies and install them if requirements.txt is present.
if [ -f "requirements.txt" ]; then
  echo "Installing Python dependencies from requirements.txt..."
  pip install -r requirements.txt
else
  echo "No requirements.txt found; skipping dependency installation."
fi

# Start the backend main script in the background.
if [ -f "main.py" ]; then
  echo "Starting backend service (main.py)..."
  python main.py &
  BACKEND_PID=$!
else
  echo "main.py not found. Please ensure your backend script is in the main directory."
fi

# Serve the frontend directory using Python's built-in HTTP server.
if [ -d "frontend" ]; then
  echo "Starting frontend server from the 'frontend' directory on port 8000..."
  cd frontend
  python -m http.server 8000 &
  FRONTEND_PID=$!
  cd ..
else
  echo "Frontend directory not found. Please ensure the 'frontend' folder exists."
fi

echo "Both backend and frontend services are running."
echo "Access the frontend at http://localhost:8000"
echo "Press [CTRL+C] to stop both services."

# Trap interrupt signals to gracefully terminate the background processes.
trap "echo 'Stopping services...'; kill ${BACKEND_PID} ${FRONTEND_PID}; exit 0" SIGINT SIGTERM

# Wait indefinitely until an interrupt signal is received.
wait