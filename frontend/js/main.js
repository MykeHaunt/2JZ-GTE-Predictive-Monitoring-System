// frontend/js/main.js

// Reference to the form and result elements
const sensorForm = document.getElementById('sensor-form');
const resultDiv = document.getElementById('result');
const predictionText = document.getElementById('prediction-text');

// Chart.js chart instance - assumed initialized in js/chart-config.js as sensorChart

// Function to fetch prediction from backend API using form data
async function fetchPrediction(sensorData) {
    try {
        const response = await fetch('http://localhost:5000/api/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sensor_data: sensorData })
        });
        if (!response.ok) {
            throw new Error(`Prediction request failed: ${response.statusText}`);
        }
        const data = await response.json();

        // After successful update, fetch latest prediction
        const predResponse = await fetch('http://localhost:5000/api/prediction');
        if (!predResponse.ok) {
            throw new Error('Failed to fetch prediction');
        }
        const predData = await predResponse.json();

        return predData;
    } catch (error) {
        console.error('Error during prediction fetch:', error);
        return null;
    }
}

// Handle form submission to send data and show prediction
sensorForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const sensorData = {
        rpm: parseFloat(document.getElementById('rpm').value),
        boost: parseFloat(document.getElementById('boost').value),
        afr: parseFloat(document.getElementById('afr').value),
        oil_temp: parseFloat(document.getElementById('oil_temp').value),
        coolant_temp: parseFloat(document.getElementById('coolant_temp').value),
        knock: parseFloat(document.getElementById('knock').value)
    };

    predictionText.textContent = 'Processing prediction...';
    resultDiv.style.display = 'block';

    const prediction = await fetchPrediction(sensorData);

    if (prediction && prediction.status) {
        predictionText.textContent = `Engine Status: ${prediction.status} (Confidence: ${(prediction.confidence * 100).toFixed(2)}%)`;
    } else {
        predictionText.textContent = 'Prediction unavailable.';
    }
});

// Function to update chart data dynamically from live sensor data endpoint
async function fetchAndUpdateChart() {
    try {
        const response = await fetch("http://localhost:5000/api/sensor_data");
        if (!response.ok) {
            console.warn("No sensor data available");
            return;
        }
        const data = await response.json();

        const maxLabels = 20; // Maximum number of points on chart

        const now = new Date();
        const timeLabel = now.toLocaleTimeString();

        if (sensorChart.data.labels.length >= maxLabels) {
            sensorChart.data.labels.shift();
            sensorChart.data.datasets.forEach(dataset => dataset.data.shift());
        }
        sensorChart.data.labels.push(timeLabel);

        // Update datasets with live sensor values (fallback to 0 if undefined)
        sensorChart.data.datasets[0].data.push(data.rpm ?? 0);
        sensorChart.data.datasets[1].data.push(data.boost ?? 0);
        sensorChart.data.datasets[2].data.push(data.knock ?? 0);

        sensorChart.update();

    } catch (error) {
        console.error("Failed to fetch sensor data for chart:", error);
    }
}

// Poll sensor data every 2 seconds for live updates
setInterval(fetchAndUpdateChart, 2000);

// Initial chart load
fetchAndUpdateChart();