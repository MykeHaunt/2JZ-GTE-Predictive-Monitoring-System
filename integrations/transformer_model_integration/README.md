# Transformer Model Integration

This directory contains all necessary components to integrate a Transformer-based prediction model into the **2JZ‑GTE Predictive Monitoring System**.

## Contents
- `data_preparation.py`: Sequence generation from raw engine data.
- `model/transformer_model.py`: Transformer architecture definition.
- `train_transformer.py`: Training script for the Transformer model.
- `app.py`: Flask endpoint for serving Transformer predictions.
- `static/script.js`: Frontend hook to fetch and display predictions.
- `requirements.txt`: Required Python packages.
- `Dockerfile`: Containerization config.
- `.github/workflows/transformer_ci.yml`: CI workflow for testing and linting.

## Prerequisites
- Python 3.10+
- Git
- Docker (optional)

## Installation & Integration

1. **Merge Code**  
   Copy the following files into your main repo under `backend/` and `frontend/` respectively:
   ```
   backend/data_preparation.py
   backend/model/transformer_model.py
   backend/train_transformer.py
   backend/app.py           # or merge with existing app.py endpoints
   frontend/static/script.js
   ```
2. **Dependencies**  
   Add to your `backend/requirements.txt`:
   ```
   flask
   tensorflow
   scikit-learn
   pandas
   joblib
   ```
3. **Train Model**  
   ```bash
   cd backend
   python train_transformer.py
   ```
4. **Serve Predictions**  
   Ensure your Flask app loads `transformer_model.h5` and `scaler.pkl`.  
   Start server:
   ```bash
   python app.py
   ```
5. **Frontend**  
   Include `script.js` in your HTML to fetch from `/predict-transformer` every 5s.

## Docker

Build and run:
```bash
docker build -t 2jz-transformer .
docker run -p 5000:5000 2jz-transformer
```

## CI/CD

A sample GitHub Actions workflow `.github/workflows/transformer_ci.yml` is provided to:
- Lint Python code with `flake8`
- Run unit tests with `pytest`

Paste it into your main repo’s workflows directory.
