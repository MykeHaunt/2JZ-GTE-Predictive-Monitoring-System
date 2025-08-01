document.getElementById("sensor-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const sensorData = {
        rpm: parseFloat(document.getElementById("rpm").value),
        boost: parseFloat(document.getElementById("boost").value),
        afr: parseFloat(document.getElementById("afr").value),
        oil_temp: parseFloat(document.getElementById("oil_temp").value),
        coolant_temp: parseFloat(document.getElementById("coolant_temp").value),
        knock: parseFloat(document.getElementById("knock").value)
    };

    try {
        const response = await fetch("http://localhost:5000/api/update", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sensor_data: sensorData })
        });
        const updateStatus = await response.json();

        const predictionResponse = await fetch("http://localhost:5000/api/prediction");
        const predictionData = await predictionResponse.json();

        if (predictionData.prediction) {
            document.getElementById("result").style.display = "block";
            document.getElementById("prediction-text").textContent = `${predictionData.prediction} (Confidence: ${(predictionData.confidence * 100).toFixed(2)}%)`;
        }
    } catch (err) {
        console.error("Prediction failed", err);
    }
});

// Simulate OBD and CAN status
function updateSystemStatus() {
    // Simulated values – integrate with backend APIs if available
    document.getElementById("obd-status").innerHTML = 'OBD: <span class="badge bg-success">Connected</span>';
    document.getElementById("can-status").innerHTML = 'CAN: <span class="badge bg-success">Active</span>';
}

window.onload = updateSystemStatus;