// frontend/js/chart-config.js

const ctx = document.getElementById('sensorChart').getContext('2d');

const sensorChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],  // Time labels will be added dynamically
        datasets: [
            {
                label: 'RPM',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)', // Blue
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: true,
                tension: 0.3,
                pointRadius: 0,
                borderWidth: 2,
            },
            {
                label: 'Boost (psi)',
                data: [],
                borderColor: 'rgba(255, 159, 64, 1)', // Orange
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                fill: true,
                tension: 0.3,
                pointRadius: 0,
                borderWidth: 2,
            },
            {
                label: 'Knock Level',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)', // Red
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true,
                tension: 0.3,
                pointRadius: 0,
                borderWidth: 2,
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 0, // Disable animations for real-time responsiveness
        },
        scales: {
            x: {
                type: 'category',
                title: {
                    display: true,
                    text: 'Time'
                },
                ticks: {
                    maxRotation: 45,
                    minRotation: 45,
                    maxTicksLimit: 10,
                    autoSkip: true,
                },
                grid: {
                    display: false,
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Value'
                },
                grid: {
                    color: 'rgba(200, 200, 200, 0.2)'
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    boxWidth: 12,
                    padding: 15,
                    font: {
                        size: 14
                    }
                }
            },
            tooltip: {
                enabled: true,
                mode: 'nearest',
                intersect: false,
            }
        },
        interaction: {
            mode: 'nearest',
            intersect: false,
        }
    }
});