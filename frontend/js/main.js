// frontend/js/main.js

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('sensor-form');
  const predictionText = document.getElementById('prediction-text');
  const resultDiv = document.getElementById('result');

  // Status indicators elements (create them dynamically or assume present in HTML)
  // Let's assume you have a div with id="status-container" for these:
  const statusContainer = document.createElement('div');
  statusContainer.className = 'status-container';
  document.querySelector('.container').insertBefore(statusContainer, form);

  // Create status indicators for OBD and CAN
  const obdStatus = createStatusIndicator('OBD');
  const canStatus = createStatusIndicator('CAN');

  statusContainer.appendChild(obdStatus.element);
  statusContainer.appendChild(canStatus.element);

  // Chart setup using Chart.js (assuming chartConfig is defined in chart-config.js)
  const ctx = document.getElementById('sensorChart').getContext('2d');
  const sensorChart = new Chart(ctx, chartConfig);

  // Function to create a status indicator
  function createStatusIndicator(name) {
    const div = document.createElement('div');
    div.className = 'status-indicator disconnected'; // Default disconnected
    div.textContent = `${name}: Disconnected`;
    return { element: div, setConnected: (connected) => {
      if (connected) {
        div.classList.remove('disconnected');
        div.classList.add('connected');
        div.textContent = `${name}: Connected`;
      } else {
        div.classList.remove('connected');
        div.classList.add('disconnected');
        div.textContent = `${name}: Disconnected`;
      }
    }};
  }

  // Simulated or real-time update of connection statuses from backend
  async function updateComponentStatus() {
    try {
      // Call backend health or status endpoint for real status
      const response = await fetch('/health');
      if (response.ok) {
        // For demonstration, toggle statuses randomly (replace with real data)
        const obdConnected = Math.random() > 0.2;  // 80% chance connected
        const canConnected = Math.random() > 0.3;  // 70% chance connected
        obdStatus.setConnected(obdConnected);
        canStatus.setConnected(canConnected);
      } else {
        obdStatus.setConnected(false);
        canStatus.setConnected(false);
      }
    } catch (error) {
      obdStatus.setConnected(false);
      canStatus.setConnected(false);
    }
  }

  // Initial status update
  updateComponentStatus();

  // Periodically refresh status every 5 seconds
  setInterval(updateComponentStatus, 5000);

  // Handle sensor form submission for prediction
  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Collect sensor inputs
    const sensorData = {
      rpm: Number(document.getElementById('rpm').value),
      boost: Number(document.getElementById('boost').value),
      afr: Number(document.getElementById('afr').value),
      oil_temp: Number(document.getElementById('oil_temp').value),
      coolant_temp: Number(document.getElementById('coolant_temp').value),
      knock: Number(document.getElementById('knock').value),
    };

    try {
      const response = await fetch('/api/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sensor_data: sensorData }),
      });

      if (!response.ok) {
        throw new Error('Failed to update sensor data');
      }

      // Get prediction
      const predResponse = await fetch('/api/prediction');
      if (!predResponse.ok) {
        throw new Error('Failed to fetch prediction');
      }

      const predJson = await predResponse.json();

      predictionText.textContent = `Prediction: ${predJson.status} (Confidence: ${(predJson.confidence * 100).toFixed(2)}%)`;
      resultDiv.style.display = 'block';

      // Update chart with new sensor values
      updateChart(sensorChart, sensorData);

    } catch (error) {
      predictionText.textContent = `Error: ${error.message}`;
      resultDiv.style.display = 'block';
    }
  });

  // Function to update Chart.js with new data
  function updateChart(chart, sensorData) {
    if (!chart) return;

    // Example: Update datasets with new sensor data points
    // Assuming your chartConfig datasets have labels matching sensor keys
    Object.entries(sensorData).forEach(([key, value]) => {
      const dataset = chart.data.datasets.find(ds => ds.label.toLowerCase() === key.toLowerCase());
      if (dataset) {
        dataset.data.push(value);
        // Limit to last 20 points
        if (dataset.data.length > 20) {
          dataset.data.shift();
        }
      }
    });

    // Add new label (timestamp)
    chart.data.labels.push(new Date().toLocaleTimeString());
    if (chart.data.labels.length > 20) {
      chart.data.labels.shift();
    }

    chart.update();
  }
});