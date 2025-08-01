#!/bin/bash
echo "Starting 2JZ-GTE Predictive Monitoring System..."
conda env create -f environment.yml
conda activate 2jz-monitoring
python main.py