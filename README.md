# 2JZ-GTE Predictive Monitoring System

[![MIT License](https://img.shields.io/github/license/MykeHaunt/2JZ-GTE-Predictive-Monitoring-System?color=green)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Docker Ready](https://img.shields.io/badge/docker-ready-blue)]()
[![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()
[![Status](https://img.shields.io/badge/status-WIP-orange.svg)]()

---

**WORK IN PROGRESS BY: H. PANDIT**

---

## 📘 Technical Description

The **2JZ-GTE Predictive Monitoring System** is a diagnostic analytics engine developed to monitor and predict failure states in Toyota’s legendary **2JZ-GTE turbocharged inline-6 engine**. It uses machine learning to evaluate key engine parameters—RPM, coolant temperature, airflow, throttle position—and detects operational anomalies before catastrophic damage occurs.

It is engineered specifically for **rolling diagnostics** in high-performance environments such as track-day vehicles, drift builds, and boosted road cars. Data can be ingested via live OBD-II scanning or simulated from structured CSV logs.

This system currently employs:
- **RandomForestClassifier** for classification of engine condition (normal/anomaly/fault),
- A structured preprocessing pipeline,
- Realtime input/output management via a lightweight Flask interface,
- Containerized deployment using Docker and Docker Compose.

---

## 🧠 System Architecture

```
       +---------------------+        +--------------------+        +-----------------------+
       |    OBD-II Scanner   | ---->  |  Data Acquisition  | ---->  |   Preprocessing       |
       |  (Live or from CSV) |        | (ELM327 / pandas)  |        | (Cleaning / Selection)|
       +---------------------+        +--------------------+        +-----------------------+
                                                                        |
                                                                        v
       +-------------------------+      +-----------------------+      +---------------------+
       |     Feature Vector      | ---> |   Model Inference     | ---> | Prediction Output   |
       | (RPM, Temp, Throttle...)|      |  (RandomForestClassifier)   |  (Normal/Anomaly/Fail)|
       +-------------------------+      +-----------------------+      +---------------------+
```

**Target output**: `Condition` — one of `Normal`, `Anomaly`, or `Fault`.

---

## 🖥️ Input/Output Format

### 📥 Input CSV (`data/engine_data.csv`):
Structured CSV logs with sensor readings and labels. Required columns:

| RPM | Throttle | Load | CoolantTemp | IntakeAirTemp | Condition |
|-----|----------|------|-------------|----------------|-----------|
| 1200 | 10 | 30 | 75 | 32 | Normal |

### 📤 Output JSON (per processed row):

```json
{
  "RPM": 2000,
  "Throttle": 25,
  "CoolantTemp": 88,
  "Prediction": "Anomaly"
}
```

Logged to `logs/` if running under Docker Compose.

---

## ⚙️ Setup Guide

### 🧰 Prerequisites

- Python ≥ 3.10  
- pip (or Conda)
- git  
- Docker & Docker Compose (for containerized setup)

---

### 🔧 Local Setup (without Docker)

```bash
# Clone the repository
git clone https://github.com/MykeHaunt/2JZ-GTE-Predictive-Monitoring-System.git
cd 2JZ-GTE-Predictive-Monitoring-System

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # (use venv\Scripts\activate for Windows)

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

---

### 🐳 Docker Setup

#### Standalone:

```bash
docker build -t 2jz-monitor .
docker run -it --rm -p 8000:8000 2jz-monitor
```

#### With Docker Compose:

```bash
docker-compose up --build
```

This mounts:
- `data/` → `/app/data`
- `logs/` → `/app/logs`

Open your browser at: [http://localhost:8000](http://localhost:8000)

---

## 📂 Directory Structure

```
2JZ-GTE-Predictive-Monitoring-System/
├── data/                   # Sample or live log data
│   └── engine_data.csv
├── logs/                   # Logs (Docker-mapped volume)
├── model/
│   ├── model.pkl           # Trained model (RandomForest)
│   └── train_model.py
├── utils/
│   └── preprocess.py       # Data preprocessing functions
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── LICENSE
├── .dockerignore
├── environment.yml
├── pyproject.toml
├── setup.cfg
├── README-DOCKER.md
├── QUICK START GUIDE.txt
└── README.md               # ← this file
```

---

### 📄 License

This software is released under the **MIT License**.

You are permitted to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

- The original copyright notice and permission notice must be included.
- The Software is provided “as is”, without warranty of any kind—explicit or implied.

> The full text of the license is available in the [LICENSE](https://github.com/MykeHaunt/2JZ-GTE-Predictive-Monitoring-System/blob/main/LICENSE) file.

This license enables maximum reuse with minimal restriction—ideal for academic, personal, or commercial applications.

---

## 👤 Author

**H. Pandit**  
Embedded Systems Developer | Dhaka, Bangladesh  
Automotive Electronics Specialist | Turbo System Diagnostic Researcher  
GitHub: [MykeHaunt](https://github.com/MykeHaunt)

---

### **PREVIEW**


![IMG_0462](https://github.com/user-attachments/assets/efe5285d-b314-4299-b667-5d1a4b9245ca)



https://github.com/user-attachments/assets/dfc24c69-68da-409c-b24b-f509b82f2bbb

