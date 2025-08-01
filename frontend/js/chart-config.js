const ctx = document.getElementById("sensorChart").getContext("2d");
const sensorChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [
            {
                label: "RPM",
                borderColor: "red",
                data: [],
                fill: false,
            },
            {
                label: "Boost (psi)",
                borderColor: "blue",
                data: [],
                fill: false,
            },
        ],
    },
    options: {
        responsive: true,
        animation: false,
        scales: {
            x: { display: false },
            y: { beginAtZero: true }
        }
    }
});