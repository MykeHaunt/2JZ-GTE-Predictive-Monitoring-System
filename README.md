# 2JZ-GTE Predictive Monitoring System – Frontend

## Project Overview

The 2JZ-GTE Predictive Monitoring System is an open-source automotive platform designed for Toyota 2JZ-GTE engines. It captures real-time vehicle telemetry and applies predictive algorithms to monitor engine health and performance. This project includes both a backend analytics engine and an updated frontend interface. The backend trains machine learning models on historical sensor data to predict component wear and failures. The new frontend provides users with a graphical interface for visualizing live and historical engine data, viewing predictive model outputs, and configuring system settings.

## Features

- **Real-time Dashboard**: Displays live engine parameters (RPM, boost pressure, EGT, coolant temperature, oil pressure, etc.)
- **Historical Data Visualization**: Time-series graphs for trend analysis and anomaly detection.
- **Predictive Alerts**: Visual warnings based on forecasted component failure.
- **Diagnostic Overview**: Health summaries and maintenance recommendations.
- **Customizable Layout**: Users can configure display panels and metric visibility.
- **Responsive Design**: Works seamlessly across desktops, tablets, and mobile devices.
- **Multi-Language Support**: Configurable localization system.
- **Secure Access**: Optional authentication and user-role support.
- **Theming and Branding**: Customizable dark/light themes and logos.
- **API Integration**: Pulls data and predictions via backend REST API.
- **Data Logging Control**: UI-based toggling of telemetry logging.

## Improvements Since Previous Version

- Replaced minimal or absent frontend with a complete graphical interface.
- Built with a modern JavaScript framework for modularity and performance.
- Interactive charts, responsive layout, and mobile support.
- Gauge and graph widgets for real-time and historical data visualization.
- Streamlined backend API integration.
- Reduced frontend-backend latency with efficient polling.
- Frontend-configurable settings and thresholds.
- Added integrated help, documentation, and developer hints.
- Simplified dependency tree and environment setup.
- Fully documented and maintainable codebase.

## Installation

```bash
git clone https://github.com/MykeHaunt/2JZ-GTE-Predictive-Monitoring-System.git
cd 2JZ-GTE-Predictive-Monitoring-System/frontend
npm install