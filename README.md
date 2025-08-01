# 2JZ-GTE Predictive Monitoring System

[![GNU GPL v3](https://img.shields.io/badge/license-GPLv3-blue)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Docker Ready](https://img.shields.io/badge/docker-ready-blue)]()
[![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()
[![Status](https://img.shields.io/badge-status-active-success)]()

---

**WORK IN PROGRESS: H. PANDIT**  
Race Engine Fabricator | Automotive Diagnostics Educator | Embedded System Software Developer   
Dhaka, Bangladesh  
GitHub: [MykeHaunt](https://github.com/MykeHaunt)

---

## 📘 Overview

The **2JZ-GTE Predictive Monitoring System** is a comprehensive, real-time engine diagnostics and failure prediction platform built for Toyota’s iconic **2JZ-GTE turbocharged inline-six engine**. It is designed for high-performance scenarios such as drift cars, time attack builds, boosted street machines, and track cars. The system offers both **real-time anomaly detection** and **predictive fault classification**, using machine learning models trained on historical and simulated sensor data.

It integrates with actual hardware (OBD-II/CAN interfaces, ELM327 adapters), processes multiple sensor channels, and predicts engine health with statistical reliability — all through a modular backend architecture and a responsive, status-aware frontend dashboard.

---

## 🔬 Short Description

> Real-time diagnostic AI for 2JZ-GTE engines. Predicts turbo failure and operational anomalies via ML, using live sensor data or CSV logs. Dockerized, Flask-powered, and cross-platform.

---

## 🧱 Design Goals

- **Modular diagnostics**: Input sensor data, preprocess, model inference, real-time feedback.
- **Rolling fault prediction**: Not just fault detection after-the-fact, but ahead-of-time anomaly classification.
- **Transparency**: Fully visible ML training pipeline, traceable inputs, and clear operational logging.
- **Scalability**: Designed to integrate with future sensor extensions, embedded ECUs, and live dashboard feedback.
- **Portability**: Easily deployable on Raspberry Pi, laptops, or Docker containers.
- **Reproducibility**: Everything can be trained, simulated, tested, and re-deployed from a clean state.

---

## ⚙️ System Architecture

```mermaid
flowchart LR
    A[Live OBD-II or CSV Input] --> B[Sensor Ingestion Module]
    B --> C[Preprocessing]
    C --> D[Feature Vector Construction]
    D --> E[Predictive Model (RandomForestClassifier)]
    E --> F[Prediction Output (Normal/Anomaly/Fault)]
    F --> G[API Response (JSON)]
    G --> H[Frontend Dashboard (Status + Chart.js)]
```

---

## 📁 Directory Structure

```
2JZ-GTE-Predictive-Monitoring-System/
├── app.py                          # Flask app with API endpoints
├── config.py                       # Configuration using environment vars
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker build specification
├── docker-compose.yml              # Docker composition for production
├── README.md                       # ← This file
│
├── model/
│   ├── model.pkl                   # Trained RandomForest model
│   ├── train_model.py              # Model training pipeline
│   ├── retrain.py                  # Automatic retraining module
│   └── monitor.py                  # Model performance tracking
│
├── backend/
│   ├── ingestion.py                # Live/simulated sensor ingestion
│   ├── predictor.py                # Inference class
│   ├── validator.py                # Input validation and error handling
│   └── hardware_status.py          # Real-time OBD/CAN and logger health
│
├── data/
│   ├── engine_data.csv             # Structured logs for training/testing
│   └── sample_fault_data.csv       # Simulated turbo failure patterns
│
├── logs/
│   └── runtime.log                 # Inference and error logs
│
├── tests/
│   ├── test_predictor.py           # Unit test for model predictions
│   ├── test_ingestion.py           # Sensor integration tests
│   └── ...
│
├── frontend/
│   ├── index.html                  # Main HTML dashboard
│   ├── styles.css                  # UI styling
│   └── app.js                      # JS chart + API hooks
```

---

## 🔌 Input Data

### A. Real-Time Sensor Feed

This system is engineered to accept real-time data from either:
- OBD-II via ELM327 adapter (Bluetooth or USB)
- CAN bus modules over USB-CAN interfaces
- Simulated sensor streams from `.csv` logs

### Expected Sensor Inputs

| Signal Name   | Description                             |
|---------------|-----------------------------------------|
| rpm           | Engine speed in revolutions/minute      |
| boost         | Boost pressure in psi or kPa            |
| afr           | Air-Fuel Ratio (wideband or narrowband) |
| oil_temp      | Engine oil temperature in °C            |
| coolant_temp  | Radiator coolant temperature in °C      |
| knock         | Knock sensor output (0–100 scale)       |

---

## 🧠 Predictive Pipeline

### 🔹 Step 1: Ingestion

All incoming sensor data (either live from hardware or logs) is routed through the `SensorIngestionManager` class. This normalizes and timestamps input frames, then logs them if configured.

### 🔹 Step 2: Preprocessing

Handled in `validator.py`. Steps include:
- Removal of nulls
- Normalization of units
- Range validation:
  - Coolant temp: 30–120 °C
  - AFR: 11.0–16.0
  - Knock: 0–100

### 🔹 Step 3: Feature Construction

Raw input → Feature vector:
```python
X = [rpm, boost, afr, oil_temp, coolant_temp, knock]
```

### 🔹 Step 4: Inference

The trained `RandomForestClassifier` infers:
- `Normal` — Healthy operating condition
- `Anomaly` — Out-of-range or erratic sensor pattern
- `Fault` — Pattern matches pre-failure signature

### 🔹 Step 5: Output

- JSON response
- Logged in `runtime.log`
- Visualized via Chart.js on the frontend

---

## 🤖 Machine Learning Pipeline

Defined in `model/train_model.py`.

### Steps:

1. **Load & Clean**:
   - Load from `data/*.csv`
   - Remove outliers, scale, and impute

2. **Label Encoding**:
   - Targets: `{Normal, Anomaly, Fault}` → `{0, 1, 2}`

3. **Feature Selection**:
   - Manual now, planned: permutation importance

4. **Model Setup**:
   ```python
   RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
   ```

5. **Cross-Validation**:
   - Stratified 5-fold
   - Tracks accuracy, F1-score, recall

6. **Persistence**:
   - Model stored as `model.pkl`

---

## 🛠️ Retraining Pipeline

Handled by `model/retrain.py`.

Supports:
- Loading new logs
- Combining datasets
- Re-fitting from scratch
- Outputting model metadata (e.g., manifest.json)

---

## 🖥️ Frontend

Located in `/frontend`:
- Input form for live or simulated data
- System health (model + OBD/CAN status)
- Chart.js visualization (real-time predictions)
- Color-coded prediction history (green/yellow/red)

---

## 🔧 API Endpoints

| Route              | Method | Description                              |
|--------------------|--------|------------------------------------------|
| `/predict`         | POST   | Submit sensor frame, receive prediction  |
| `/update_model`    | POST   | Upload retrained model                   |
| `/health`          | GET    | Returns backend and model status         |
| `/sensor/ingest`   | POST   | Submit simulated CSV stream              |
| `/hardware/status` | GET    | Reports hardware/OBD availability        |

---

## 🐳 Docker & Deployment

### Build Image
```bash
docker build -t 2jz-monitor .
```

### Run Container
```bash
docker run -p 8000:8000 2jz-monitor
```

### Docker Compose
```bash
docker-compose up --build
```

#### Mount Volumes
- `data/` → `/app/data`
- `logs/` → `/app/logs`

---

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Covers:
- Validation of edge-case inputs
- CAN/OBD-II sensor simulation
- Model robustness under drift
- Retraining validation

---

## 🔒 License

This project is licensed under the **GNU GPL v3**.

### Permitted:
- Commercial and private use
- Distribution
- Modification

### Conditions:
- Derivatives must be under GPLv3
- Source disclosure on redistribution

Refer to [LICENSE](LICENSE) for legal text.

---

## 🔮 Future Features

- LSTM-based sequence modeling
- BLE-enabled sensor feeds
- Fault-alert via SMS/email
- Integration with ECU-specific CAN PIDs
- Cloud-based logging/visualizations

---

## 🎓 Educational Use

Recommended for:
- Teaching embedded ML systems
- Engine diagnostics coursework
- AI/ML workshops in automotive tech
- DIY racecar monitoring projects

---

## 👨‍💻 Author

H. Pandit  
Dhaka, Bangladesh  
Race Engine Fabricator | Automotive Diagnostics Educator | Software Developer  
GitHub: MykeHaunt