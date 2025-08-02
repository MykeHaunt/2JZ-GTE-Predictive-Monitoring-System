
# 2JZ‑GTE Predictive Monitoring System

[![GNU GPL v3](https://img.shields.io/badge/license-GPLv3-blue)](LICENSE)  
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()  
[![Docker Ready](https://img.shields.io/badge/docker-ready-blue)]()  
[![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)]()  
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()  
[![Code Quality](https://img.shields.io/badge/code%20quality-A-brightgreen)]()  
[![Test Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)]()  
[![Maintenance](https://img.shields.io/badge/maintenance-active-brightgreen)]()

---

**Version:** 1.2.0  
**Last Updated:** August 2025  
**Author:** H. Pandit  
**License:** GNU General Public License v3.0  
**Repository:** [https://github.com/MykeHaunt/2JZ‑GTE‑Predictive‑Monitoring‑System](https://github.com/MykeHaunt/2JZ‑GTE‑Predictive‑Monitoring‑System)

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
11. [Engine Technical Specs](#engine-technical-specs)  
12. [Testing & Integration](#testing--integration)  
13. [Deployment Guide](#deployment-guide)  
14. [Known Issues](#known-issues)  
15. [Contributing](#contributing)  
16. [License](#license)  
17. [Acknowledgements](#acknowledgements)

---

## Overview

The **2JZ‑GTE Predictive Monitoring System** is a real‑time, machine learning–powered monitoring and predictive analytics platform tailored to the Toyota 2JZ‑GTE engine. It features:

- Live sensor ingestion via OBD‑II or CSV logs  
- Dual-model inference using `scikit-learn` and `TensorFlow`  
- WebSocket-driven frontend streaming at ~23.6 Hz  
- Responsive, theme-aware dashboard with predictive analytics  
- Logging, auto-retrain, and diagnostics support  

---

## System Architecture

```
+-----------------------------+
| Frontend (HTML5 Dashboard) |
|  • Chart.js                |
|  • Socket.IO               |
+-------------+-------------+
              |
              ▼
+-----------------------------+
| WebSocket Server (@23.6 Hz)|
|  • socket_server.py        |
+-------------+-------------+
              |
     +--------+--------+
     |                 |
     ▼                 ▼
+-----------+    +-------------------+
| SKLearn   |    | TensorFlow        |
| model.pkl |    | saved_model.pb    |
+-----------+    +-------------------+
     ▲                 ▲
     |                 |
     +--------+--------+
              |
              ▼
+-----------------------------+
| Sensor Ingestion System     |
|  • OBD2 / CAN / Simulator   |
+-----------------------------+
```

---

## Core Features

- **Concurrent Models**: `scikit-learn` for fast inference; `TensorFlow` for robust deep learning  
- **Live Streaming Telemetry**: ~23.6 Hz (≈42 ms per frame)  
- **Responsive UI**: Real-time charts and accessibility support  
- **Theme Switching**: Auto/manual night/day mode  
- **Graceful Fallback**: Simulated input if hardware is unavailable  

---

## Installation Guide

### System Prerequisites

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ Requires Python 3.8+ (Python 3.10+ recommended)

---

## Quickstart

```bash
chmod +x run_all.sh
./run_all.sh
```

To stop all services:

```bash
chmod +x stop_all.sh
./stop_all.sh
```

This launches:

- Flask REST API backend  
- WebSocket telemetry server  
- Logs saved to `logs/flask.log` and `logs/socket.log`  

---

## Model Support

### ✅ SKLearn Predictor

- File: `model/sklearn_model.pkl`  
- Lightweight, interpretable, low overhead  

### ✅ TensorFlow Predictor

- Directory: `model/tf_model/`  
  - `saved_model.pb`  
  - `variables/variables.data-00000-of-00001`  
  - `variables/variables.index`  

Both models run concurrently within `run_all.sh`.

---

## Live Metrics via WebSocket

| Attribute       | Detail                        |
|----------------|-------------------------------|
| Server File     | `backend/socket_server.py`    |
| Protocol        | WebSocket (Socket.IO)         |
| Frequency       | ~23.6 Hz                      |
| Latency         | ≈ 41 ms per message           |
| Default Scope   | Localhost only                |

Auto-computed metrics include:

- AFR Δ (change per frame)  
- Coolant rise rate (°C/s)  
- Boost gradient  
- Turbo response estimate  
- Oil temperature change  

Derived from sequential sensor input using time-based difference calculations.

---

## Frontend Dashboard

- **Location**: `frontend/index.html`, `style.css`, `app.js`  
- **Features**:  
  - Real-time `Chart.js` visualizations  
  - Live metric cards (AFR Δ, turbo response, coolant rate)  
  - Theme toggle (auto/manual)  
  - Responsive layout (mobile support, ARIA labels)  
  - Alerts for out-of-range sensor data  

---

## Backend API

- **File**: `backend/app.py`  

| Route         | Method | Description                        |
|---------------|--------|------------------------------------|
| `/predict`     | POST   | SKLearn model inference            |
| `/predict-tf`  | POST   | TensorFlow model inference         |
| `/ingest`      | POST   | Simulated/CSV sensor input         |
| `/update_model`| PATCH  | Upload and reload new model        |
| `/health`      | GET    | Backend and hardware health check  |

---

## Sensor Ingestion System

- **File**: `backend/sensor_ingestion.py`  
- **Supported Modes**:
  - OBD‑II via `python‑obd`  
  - CAN Bus via `python‑can`  
  - JSON-simulated feed for testing  

**Priority Order:**

1. Real hardware  
2. Simulation mode (configurable)  
3. Manual input (UI)

---

## Engine Technical Specs

| Specification      | Value                               |
|--------------------|-------------------------------------|
| Displacement       | 2,997 cm³ (3.0 L)                   |
| Bore × Stroke      | 86 mm × 86 mm                       |
| Valvetrain         | DOHC, 24 valves                     |
| Turbo System       | Sequential twin-turbo              |
| Compression Ratio  | 8.5 : 1                             |
| Power (Factory)    | 276 hp JDM; ~320 hp export markets  |

> [^1]: Based on official Toyota specifications and reviewed technical sources.

---

## Testing & Integration

Run all tests:

```bash
pytest tests/
```

Integration test:

```bash
python3 tests/test_websocket_integration.py
```

Coverage includes:

- Dual-model output consistency  
- WebSocket streaming under load  
- Input validation and error handling  

---

## Deployment Guide

### ✅ Raspberry Pi

- Enable CAN/RS-232 permissions  
- Use `systemd` for service auto-start  
- Consider TensorFlow Lite for ARM optimization  

### ✅ Docker (optional)

**Dockerfile:**

```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["./run_all.sh"]
```

Build and deploy:

```bash
docker build -t 2jz-monitor .
docker run -p 5000:5000 -p 5050:5050 2jz-monitor
```

---

## Known Issues

- Initial TensorFlow inference may take ~1.2 s on cold start  
- WebSocket buffer overflow on legacy Windows (~30 min sessions)  
- Chart rendering glitch in Safari Mobile dark mode  

---

## Contributing

Contributions are welcome under the following guidelines:

- Follow [PEP8](https://peps.python.org/pep-0008/)  
- Commit messages: `[component]: summary`  
- Avoid hard-coded thresholds or hardware-specific constants  

---

## License

Licensed under the **GNU GPL v3**.  
Refer to the enclosed `LICENSE` file for full terms.

© 2025 H. Pandit — All rights reserved under GPL v3.

---

## Acknowledgements

- **Toyota Motor Corporation** – Engineering of the 2JZ‑GTE engine  
- **OpenAI** – Architectural and documentation assistance  
- **Core Libraries** – `Chart.js`, `Flask`, `Flask‑SocketIO`, `TensorFlow`, `scikit-learn`  