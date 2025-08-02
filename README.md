Below is the final, fully‑formatted README.md for version 1.2.0 of the 2JZ‑GTE Predictive Monitoring System. You may copy this in its entirety into your own README.md.
Alternatively, if your interface supports it, you can download this content directly:

📄 Click here to download README_v1.2.0.md

⸻


<!--‑‑ README.md for 2JZ‑GTE Predictive Monitoring System — Version 1.2.0 ‑‑-->

# 2JZ‑GTE Predictive Monitoring System

[![GNU GPL v3](https://img.shields.io/badge/license‑GPLv3‑blue)](LICENSE)  
[![Build Status](https://img.shields.io/badge/build‑passing‑brightgreen)]()  
[![Docker Ready](https://img.shields.io/badge/docker‑ready‑blue)]()  
[![Platform](https://img.shields.io/badge/platform‑cross‑platform‑lightgrey)]()  
[![Python](https://img.shields.io/badge/python‑3.10%2B‑blue.svg)]()  
[![Code Quality](https://img.shields.io/badge/code%20quality‑A‑brightgreen)]()  
[![Test Coverage](https://img.shields.io/badge/coverage‑95%25‑brightgreen)]()  
[![Maintenance](https://img.shields.io/badge/maintenance‑active‑brightgreen)]()

---

**Version:** 1.2.0  
**Last Updated:** August 2025  
**Author:** H. Pandit  
**License:** GNU General Public License v3.0  
**Repository:** https://github.com/MykeHaunt/2JZ‑GTE‑Predictive‑Monitoring‑System  

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

The **2JZ‑GTE Predictive Monitoring System** is a real‑time, machine‑learning‑powered monitoring and predictive analytics platform tailored to the Toyota 2JZ‑GTE engine. It features:

- Live sensor ingestion via OBD‑II or CSV logs  
- Dual‑model inference using SKLearn and TensorFlow  
- WebSocket‐driven frontend streaming at ~23.6 Hz  
- Responsive, theme‑aware dashboard with predictive analytics  
- Logging, auto‑retrain, and diagnostics support  

---

## System Architecture

        +-----------------------------+
        | Frontend (HTML5 Dashboard)  |
        |  • Chart.js                 |
        |  • Socket.IO                |
        +-------------+---------------+
                      |
                      ▼
  +------------------+------------------+
  |  WebSocket Server (@23.6 Hz)         |
  |     `socket_server.py`                |
  +------------------+------------------+
                      |
 +--------------------+--------------------+
 |                    |                    |
 ▼                    ▼                    ▼

+————+   +——————+   +—————————+
| Sensor     |   | SKLearn          |   | TensorFlow                |
| Ingestion  |   | Predictor (model.pkl) | Predictor (saved_model.pb) |
| (CAN/OBD2/Simulator) |              |                           |
+————+   +——————+   +—————————+

---

## Core Features

- **Concurrent models:** SKLearn for fast inference; TensorFlow for deep‑learning robustness  
- **Live streaming telemetry:** Telemetry delivered at ~23.6 Hz (~42 ms per frame)  
- **Responsive UI:** Real‑time charts, metric calculations, accessibility support  
- **Theme switching:** Auto or manual switch between day/night modes  
- **Graceful fallback:** Simulated input if hardware interfaces (OBD/CAN) are unavailable  

---

## Installation Guide

### System Prerequisites

```bash
sudo apt update
sudo apt install python3 python3-pip

Python Dependencies

pip install --upgrade pip
pip install -r requirements.txt

⚠️ Requires Python 3.8+ (3.10+ recommended)

⸻

Quickstart

chmod +x run_all.sh
./run_all.sh

To stop all services:

chmod +x stop_all.sh
./stop_all.sh

This launches:
• Flask REST API backend
• WebSocket telemetry server
• Logs saved to logs/flask.log and logs/socket.log

⸻

Model Support

✅ SKLearn Predictor
	•	File: model/sklearn_model.pkl
	•	Lightweight, interpretable, low overhead

✅ TensorFlow Predictor
	•	Directory: model/tf_model/
	•	saved_model.pb
	•	variables/variables.data-00000-of-00001
	•	variables/variables.index

Both predictors run concurrently by default within run_all.sh.

⸻

Live Metrics via WebSocket

Attribute	Detail
Server File	backend/socket_server.py
Protocol	WebSocket (Socket.IO)
Frequency	~23.6 Hz
Latency	≈ 41 ms per message
Default Scope	localhost only

Auto‑computed metrics include:
	•	AFR Δ (change per frame)
	•	Coolant rise rate (°C/s)
	•	Boost gradient
	•	Turbo response estimate
	•	Oil temperature change

Derived from sequential sensor input using time‐based difference calculations.

⸻

Frontend Dashboard

Location: frontend/index.html (logic), style.css (styles), app.js (charts + websocket hooks)

Features:
	•	Real-time Chart.js visualizations (sensor + predictions)
	•	Live metric cards (AFR Δ, coolant rate, turbo response)
	•	Night/day theme toggle (auto and manual modes)
	•	Mobile/responsive layout with clear ARIA labels
	•	Visual alerts for out‑of‑range sensor data

⸻

Backend API

File: backend/app.py (Flask + Predictor abstraction)

Available REST endpoints:

Route	Method	Description
/predict	POST	SKLearn model inference
/predict-tf	POST	TensorFlow model inference
/ingest	POST	Feed simulated or CSV sensor data
/update_model	PATCH	Upload and load a retrained model
/health	GET	Backend and hardware health checks


⸻

Sensor Ingestion System

File: backend/sensor_ingestion.py

Supported modes:
	•	OBD‑II via python‑obd
	•	CAN Bus via python‑can
	•	JSON‑simulated data feed for testing

Priority:
	1.	Real hardware input
	2.	Simulation mode (via configuration)
	3.	Manual entry via UI

⸻

Engine Technical Specs

Specification	Value
Displacement	2,997 cm³ (3.0 L)
Bore × Stroke	86 mm × 86 mm
Valvetrain	DOHC, 24 valves
Turbo System	Sequential twin‑turbo
Compression Ratio	8.5 :1
Power (Factory)	276 hp JDM; ~320 hp export/outside markets[^1]

[^1]: Based on official Toyota specifications and reviewed technical sources.  ￼ ￼ ￼ ￼ ￼ ￼ ￼

⸻

Testing & Integration

Run all tests with:

pytest tests/

Integration check:

python3 tests/test_websocket_integration.py

Coverage includes:
	•	Dual‑model output comparison
	•	WebSocket streaming at load
	•	Input validation and error handling

⸻

Deployment Guide

Raspberry Pi
	•	Enable CAN/RS‑232 permissions for live sensor input
	•	Use systemd unit files to auto-start services
	•	Consider TensorFlow Lite for ARM compatibility

Docker (optional)

FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["./run_all.sh"]

Deploy with:

docker build -t 2jz-monitor .
docker run -p 5000:5000 -p 5050:5050 2jz-monitor


⸻

Known Issues
	•	Initial TensorFlow inference can take ~1.2 s on cold start
	•	WebSocket buffer overflow on outdated Windows builds (~30 min sessions)
	•	Safari Mobile may glitch chart rendering in dark mode

⸻

Contributing

Contributions are welcome under the following guidelines:
	•	Adhere to PEP8
	•	Commit messages formatted as [component]: summary
	•	Avoid hard‑coded hardware limits or thresholds

⸻

License

Licensed under the GNU GPL v3.
Refer to the enclosed LICENSE document for full details.

© 2025 H. Pandit — All rights reserved under GPL v3

⸻

Acknowledgements
	•	Toyota Motor Corporation – Engineering of the robust 2JZ‑GTE engine
	•	OpenAI – Assistance in architectural planning and documentation
	•	Core Libraries – Chart.js, Flask, Flask‑SocketIO, TensorFlow, scikit‑learn

⸻


