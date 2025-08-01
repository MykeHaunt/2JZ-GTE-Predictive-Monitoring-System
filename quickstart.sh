#!/bin/bash
echo "Setting up 2JZ-GTE Predictive Monitoring System..."

# Step 1: Create virtual environment
python3 -m venv env
source env/bin/activate

# Step 2: Install requirements
pip install --upgrade pip
pip install -r backend/requirements.txt

# Step 3: Start backend server
echo "Launching Flask API..."
python backend/app.py