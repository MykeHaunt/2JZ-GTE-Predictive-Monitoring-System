# 2JZ-GTE Predictive Monitoring System

[![GNU GPL v3 License](https://img.shields.io/badge/License-GNU%20GPL%20v3-green.svg)](LICENSE)

**Version:** 1.0.0  
**Last Updated:** August 2025  
**Author:** H. Pandit  
**License:** GNU General Public License v3.0  
**Repository:** https://github.com/MykeHaunt/2JZ-GTE-Predictive-Monitoring-System  

---

## Table of Contents

1. [Overview](#overview)  
2. [System Architecture](#system-architecture)  
3. [Core Features](#core-features)  
4. [Installation Guide](#installation-guide)  
5. [Quickstart](#quickstart)  
6. [Model Support](#model-support)  
7. [Live Metrics via WebSocket](#live-metrics-via-websocket)  
8. [Frontend Dashboard](#frontend-dashboard)  
9. [Backend API](#backend-api)  
10. [Sensor Ingestion System](#sensor-ingestion-system)  
11. [Testing & Integration](#testing--integration)  
12. [Deployment Guide](#deployment-guide)  
13. [Known Issues](#known-issues)  
14. [Contributing](#contributing)  
15. [License](#license)  

---

## Overview

The **2JZ-GTE Predictive Monitoring System** is a real-time, machine-learning-powered failure prediction and health analytics platform built around the legendary Toyota 2JZ-GTE engine. Designed for enthusiasts, engineers, and tuners, it uses both statistical and deep learning models to forecast failure trends, optimize engine health, and support diagnostics.

Key components include:
- Live sensor ingestion
- WebSocket-based metric broadcasting
- Dual model inference (SKLearn + TensorFlow)
- Adaptive frontend with night/day theming
- Auto-retraining and performance logging

---

## System Architecture

            +-----------------------------+
            |       Frontend (HTML5)      |
            |  - Chart.js, Socket.IO      |
            +-------------+---------------+
                          |
                          ▼
      +------------------+------------------+
      |         WebSocket Server            |
      |    socket_server.py (23.6Hz)        |
      +------------------+------------------+
                          |
     +--------------------+--------------------+
     |                     |                    |
     ▼                     ▼                    ▼

SensorIngestion      SKLearn Predictor     TensorFlow Predictor
(CAN/OBD2/Simulator)     (model.pkl)          (model/saved_model.pb)

---

## Core Features

- **Dual ML Backend:** Runs both SKLearn (for fast inference) and TensorFlow (for deep-learning prediction).
- **Live WebSocket Streaming:** 23.5999 Hz bi-directional streaming.
- **Frontend Dashboard:** Accessible in-browser real-time data visualization and health monitoring.
- **Auto Theme Switch:** Night and day modes based on system or manual input.
- **Hardware Status Interface:** OBD-II/CAN interface status shown live.

---

## Installation Guide

### 🔧 Dependencies

Install system-level dependencies:

```bash
sudo apt install python3 python3-pip

Install Python packages:

pip install -r requirements.txt

Ensure your environment uses Python ≥ 3.8.

⸻

Quickstart

Use the bundled script:

chmod +x run_all.sh
./run_all.sh

To stop:

./stop_all.sh

This launches:
	•	Flask API backend
	•	WebSocket streaming server
	•	Logs saved to logs/flask.log and logs/socket.log

⸻

Model Support

✅ SKLearn Predictor
	•	Location: model/sklearn_model.pkl
	•	Fast, low-memory usage
	•	Used for basic inference

✅ TensorFlow Model
	•	Location: model/tf_model/
	•	Structured SavedModel format with:
	•	saved_model.pb
	•	variables/variables.data-00000-of-00001
	•	variables/variables.index
	•	Requires tensorflow==2.15.0

Both models are run concurrently in background inference servers.

⸻

Live Metrics via WebSocket
	•	Server: backend/socket_server.py
	•	Protocol: WebSocket (via websockets)
	•	Frequency: 23.5999 Hz
	•	Latency: ~41ms (avg)
	•	Security: Localhost only by default

Metrics include:
	•	AFR delta
	•	Coolant Temp Rise Rate
	•	Boost Gradient
	•	Turbo Deviation Factor
	•	Oil Temp Swing

Auto-computed using streaming buffer with differential time derivatives.

⸻

Frontend Dashboard

Location: frontend/index.html
Styles: frontend/style.css

Features:
	•	Realtime sensor graphing (Chart.js)
	•	Component status (OBD2, CAN, Socket)
	•	Engine health prediction display
	•	Theme toggle (auto/manual)
	•	Form validation for inputs

Live Updating:
	•	Metrics update at 23.5999Hz
	•	Broadcast via WebSocket
	•	Dynamic color cues for abnormal states

⸻

Backend API

Location: backend/app.py
Framework: Flask

Endpoints:
	•	/predict — POST: inference from JSON sensor data
	•	/ingest — POST: accept live values
	•	/update_model — PATCH: load new models
	•	/health — GET: backend and hardware status

Uses Predictor class that abstracts both ML backends.

⸻

Sensor Ingestion System

Location: backend/sensor_ingestion.py

Modes:
	•	OBD-II via pyOBD or python-OBD
	•	CAN Bus via python-can
	•	Simulated Ingestion for testing

Supports fallback hierarchy:
	1.	Real hardware
	2.	Simulated profiles
	3.	Manual input via dashboard

⸻

Testing & Integration

Unit Tests

Located in: tests/
Run with:

pytest tests/

Integration Test

python3 tests/test_websocket_integration.py

Covers:
	•	Model predictions
	•	Socket broadcast latency
	•	API consistency
	•	Error handling for malformed input

⸻

Deployment Guide

Raspberry Pi
	1.	Ensure GPIO permissions for CAN
	2.	Install python-can, socket, and TensorFlow Lite
	3.	Use systemd unit to keep backend running

Docker (Optional)

Create Dockerfile:

FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["./run_all.sh"]

Then:

docker build -t 2jz-monitor .
docker run -p 5000:5000 -p 8765:8765 2jz-monitor


⸻

Known Issues
	•	TensorFlow model takes ~1.2s on first inference (cold start)
	•	Socket drops on Windows after ~30 mins (buffer overflow)
	•	Chart.js rendering bug on Safari mobile under dark mode

⸻

Contributing

Pull requests are welcome. Please follow:
	•	Python PEP8
	•	Commit message format: [component]: short desc
	•	Avoid hardcoding sensor limits

⸻

License

This project is licensed under the GNU GPL v3 License — see the LICENSE file for details.

© 2025 H. Pandit
All rights reserved under GNU General Public License v3

⸻

Acknowledgements
	•	[Toyota Motor Corporation] – for engineering the 2JZ-GTE
	•	[OpenAI] – assistance in architecture and documentation
	•	[Chart.js, Flask, TensorFlow] – backbone of this stack

---

Would you like this as a downloadable PDF or Markdown file as well?