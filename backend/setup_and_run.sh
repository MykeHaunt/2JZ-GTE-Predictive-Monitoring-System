#!/bin/bash

# Initialize project
git clone https://github.com/yourusername/2JZ-GTE-Turbo-Monitor.git
cd 2JZ-GTE-Turbo-Monitor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate initial data and train model
python3 -c "from turbo_monitor.core import TurboMonitorCore; core = TurboMonitorCore(); core.generate_data(); core.train_model()"

# Start dashboard
python3 -c "from turbo_monitor.dashboard import TurboMonitorDashboard; from turbo_monitor.core import TurboMonitorCore; dashboard = TurboMonitorDashboard(TurboMonitorCore()); dashboard.run()"