// frontend/js/chart-config.js

function createSensorChart() {
  const ctx = document.getElementById("sensorChart").getContext("2d");
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        { label: "RPM", data: [], fill: false, tension: 0.1 },
        { label: "Boost (psi)", data: [], fill: false, tension: 0.1 },
        { label: "AFR", data: [], fill: false, tension: 0.1 },
        { label: "Oil Temp (°C)", data: [], fill: false, tension: 0.1 },
        { label: "Coolant Temp (°C)", data: [], fill: false, tension: 0.1 },
        { label: "Knock", data: [], fill: false, tension: 0.1 }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" }
      },
      scales: {
        x: { display: true, title: { display: true, text: "Time" } },
        y: { beginAtZero: true }
      }
    }
  });
}