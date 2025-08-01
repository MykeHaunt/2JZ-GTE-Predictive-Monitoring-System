// main.js

// Existing sensor form submission and prediction logic
document.getElementById('sensor-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    // Gather input values with validation
    const rpm = Number(document.getElementById('rpm').value);
    const boost = Number(document.getElementById('boost').value);
    const afr = Number(document.getElementById('afr').value);
    const oil_temp = Number(document.getElementById('oil_temp').value);
    const coolant_temp = Number(document.getElementById('coolant_temp').value);
    const knock = Number(document.getElementById('knock').value);

    // Basic input validation (can be expanded)
    if (
        isNaN(rpm) || rpm < 0 ||
        isNaN(boost) ||
        isNaN(afr) || afr <= 0 ||
        isNaN(oil_temp) || oil_temp < -40 || oil_temp > 150 ||
        isNaN(coolant_temp) || coolant_temp < -40 || coolant_temp > 150 ||
        isNaN(knock) || knock < 0 || knock > 10
    ) {
        alert('Please enter valid sensor data within allowed ranges.');
        return;
    }

    const sensorData = { rpm, boost, afr, oil_temp, coolant_temp, knock };

    try {
        const response = await fetch('/api/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sensor_data: sensorData }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        if (result.status === 'updated') {
            // Fetch the latest prediction
            const predResponse = await fetch('/api/prediction');
            if (predResponse.ok) {
                const predData = await predResponse.json();
                displayPrediction(predData);
                addDataToChart(sensorData);
            }
        }
    } catch (error) {
        console.error('Error submitting sensor data:', error);
        alert('Failed to submit sensor data. Please try again.');
    }
});

function displayPrediction(prediction) {
    const resultDiv = document.getElementById('result');
    const predictionText = document.getElementById('prediction-text');
    predictionText.textContent = prediction.message || 'No prediction message.';
    resultDiv.style.display = 'block';
}

// Chart.js setup (basic example)
const ctx = document.getElementById('sensorChart').getContext('2d');
const sensorChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // time or count
        datasets: [
            {
                label: 'RPM',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false,
                tension: 0.1,
            },
            {
                label: 'Boost (psi)',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false,
                tension: 0.1,
            },
            {
                label: 'AFR',
                data: [],
                borderColor: 'rgba(255, 206, 86, 1)',
                fill: false,
                tension: 0.1,
            },
            {
                label: 'Oil Temp (°C)',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
                tension: 0.1,
            },
            {
                label: 'Coolant Temp (°C)',
                data: [],
                borderColor: 'rgba(153, 102, 255, 1)',
                fill: false,
                tension: 0.1,
            },
            {
                label: 'Knock Level',
                data: [],
                borderColor: 'rgba(255, 159, 64, 1)',
                fill: false,
                tension: 0.1,
            },
        ],
    },
    options: {
        responsive: true,
        animation: false,
        scales: {
            x: {
                title: { display: true, text: 'Sample Count' },
            },
            y: {
                beginAtZero: true,
            },
        },
    },
});

let sampleCount = 0;

function addDataToChart(sensorData) {
    sampleCount++;
    sensorChart.data.labels.push(sampleCount.toString());
    sensorChart.data.datasets[0].data.push(sensorData.rpm);
    sensorChart.data.datasets[1].data.push(sensorData.boost);
    sensorChart.data.datasets[2].data.push(sensorData.afr);
    sensorChart.data.datasets[3].data.push(sensorData.oil_temp);
    sensorChart.data.datasets[4].data.push(sensorData.coolant_temp);
    sensorChart.data.datasets[5].data.push(sensorData.knock);

    // Limit data points to last 20 samples for readability
    if (sensorChart.data.labels.length > 20) {
        sensorChart.data.labels.shift();
        sensorChart.data.datasets.forEach(dataset => dataset.data.shift());
    }
    sensorChart.update();
}

// --- System Status Section ---

// Function to fetch and update system status badges
async function updateSystemStatus() {
    try {
        const response = await fetch('/api/monitor_status');
        if (!response.ok) throw new Error('Network response was not ok');
        const statusData = await response.json();

        function updateBadge(id, isActive) {
            const badge = document.getElementById(id);
            if (!badge) return;
            if (isActive === true) {
                badge.textContent = 'Connected';
                badge.className = 'badge rounded-pill bg-success';
            } else if (isActive === false) {
                badge.textContent = 'Disconnected';
                badge.className = 'badge rounded-pill bg-danger';
            } else {
                badge.textContent = 'Unknown';
                badge.className = 'badge rounded-pill bg-secondary';
            }
        }

        updateBadge('obd-status', statusData.obd_connected);
        updateBadge('can-status', statusData.can_active);
        updateBadge('sensor-ingestion-status', statusData.sensor_ingestion_active);
    } catch (error) {
        console.error('Failed to fetch system status:', error);
        ['obd-status', 'can-status', 'sensor-ingestion-status'].forEach(id => {
            const badge = document.getElementById(id);
            if (badge) {
                badge.textContent = 'Error';
                badge.className = 'badge rounded-pill bg-danger';
            }
        });
    }
}

// Initial call and polling every 5 seconds
updateSystemStatus();
setInterval(updateSystemStatus, 5000);