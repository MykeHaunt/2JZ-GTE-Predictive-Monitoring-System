// frontend/js/main.js

// Fetch intervals (ms)
const POLL_INTERVAL = 1000;

// Chart instance (defined in chart-config.js)
let sensorChart = null;

// Initialize after DOM load
document.addEventListener("DOMContentLoaded", () => {
  sensorChart = createSensorChart();  // from chart-config.js
  pollData();
});

// Recursive polling function
async function pollData() {
  try {
    // Fetch latest sensor data
    const sensorRes = await fetch("/api/sensor_data");
    const predRes = await fetch("/api/prediction");

    let sensorData = null, prediction = null;

    if (sensorRes.ok) {
      sensorData = await sensorRes.json();
      updateChart(sensorData);
    }

    if (predRes.ok) {
      prediction = await predRes.json();
      updatePrediction(prediction);
    }
  } catch (err) {
    console.error("Polling error:", err);
  } finally {
    setTimeout(pollData, POLL_INTERVAL);
  }
}

// Update textual prediction result
function updatePrediction(pred) {
  const resultDiv = document.getElementById("result");
  const textEl = document.getElementById("prediction-text");

  if (pred.error || pred.message) {
    textEl.textContent = pred.error || pred.message;
    textEl.classList.remove("alert-info");
    textEl.classList.add("alert-danger");
  } else {
    textEl.textContent = `Status: ${pred.prediction} (Confidence: ${(pred.confidence * 100).toFixed(1)}%)`;
    textEl.classList.remove("alert-danger");
    textEl.classList.add("alert-info");
  }
  resultDiv.style.display = "block";
}

// Push new data point(s) into Chart.js
function updateChart(data) {
  if (!sensorChart) return;

  const now = new Date().toLocaleTimeString();

  // Append new labels and data
  sensorChart.data.labels.push(now);
  sensorChart.data.datasets.forEach(dataset => {
    const key = dataset.label.toLowerCase().replace(/\s*\(.*?\)/, "").replace(/\s+/g, "_");
    dataset.data.push(data[key]);
  });

  // Keep last 20 points
  if (sensorChart.data.labels.length > 20) {
    sensorChart.data.labels.shift();
    sensorChart.data.datasets.forEach(ds => ds.data.shift());
  }

  sensorChart.update();
}