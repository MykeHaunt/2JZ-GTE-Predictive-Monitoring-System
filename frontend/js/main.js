document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('sensor-form');
    const resultDiv = document.getElementById('result');
    const predictionText = document.getElementById('prediction-text');

    const obdStatusBadge = document.getElementById('obd-status');
    const canStatusBadge = document.getElementById('can-status');
    const ingestionStatusBadge = document.getElementById('ingestion-status');

    // Function to update system status badges
    async function fetchSystemStatus() {
        try {
            const response = await fetch('/api/monitor_status');
            if (!response.ok) throw new Error('Network response was not ok');
            const status = await response.json();

            // Update badges with colors and text
            updateBadge(obdStatusBadge, status.obd_connected);
            updateBadge(canStatusBadge, status.can_active);
            updateBadge(ingestionStatusBadge, status.sensor_ingestion_active);
        } catch (error) {
            console.error('Error fetching system status:', error);
            obdStatusBadge.textContent = 'Error';
            canStatusBadge.textContent = 'Error';
            ingestionStatusBadge.textContent = 'Error';

            obdStatusBadge.className = 'badge bg-danger';
            canStatusBadge.className = 'badge bg-danger';
            ingestionStatusBadge.className = 'badge bg-danger';
        }
    }

    function updateBadge(badgeElement, status) {
        if (status === true) {
            badgeElement.textContent = 'Connected';
            badgeElement.className = 'badge bg-success';
        } else if (status === false) {
            badgeElement.textContent = 'Disconnected';
            badgeElement.className = 'badge bg-danger';
        } else {
            badgeElement.textContent = 'Unknown';
            badgeElement.className = 'badge bg-warning';
        }
    }

    // Initial fetch of system status and then every 10 seconds
    fetchSystemStatus();
    setInterval(fetchSystemStatus, 10000);

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const sensorData = {
            rpm: parseFloat(document.getElementById('rpm').value),
            boost: parseFloat(document.getElementById('boost').value),
            afr: parseFloat(document.getElementById('afr').value),
            oil_temp: parseFloat(document.getElementById('oil_temp').value),
            coolant_temp: parseFloat(document.getElementById('coolant_temp').value),
            knock: parseFloat(document.getElementById('knock').value),
        };

        try {
            const response = await fetch('/api/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sensor_data: sensorData }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Prediction failed');
            }

            const predictionResponse = await fetch('/api/prediction');
            if (!predictionResponse.ok) throw new Error('Failed to get prediction');

            const prediction = await predictionResponse.json();

            predictionText.textContent = JSON.stringify(prediction, null, 2);
            resultDiv.style.display = 'block';
        } catch (error) {
            predictionText.textContent = `Error: ${error.message}`;
            resultDiv.style.display = 'block';
        }
    });
});