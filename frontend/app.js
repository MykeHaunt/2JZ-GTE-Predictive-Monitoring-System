document.addEventListener('DOMContentLoaded', function() {
  // Sample data for demonstration; replace with dynamic API call if available.
  const engineData = {
    labels: ['0s', '1s', '2s', '3s', '4s', '5s'],
    datasets: [{
      label: 'Engine Temperature (°C)',
      data: [90, 92, 93, 95, 94, 96],
      borderColor: 'rgba(255, 99, 132, 1)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      fill: true,
      tension: 0.1
    }]
  };

  const ctx = document.getElementById('engineChart').getContext('2d');
  const engineChart = new Chart(ctx, {
    type: 'line',
    data: engineData,
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Time'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Temperature (°C)'
          }
        }
      }
    }
  });

  // Optional: Fetch live data from your predictive monitoring API endpoint.
  // Uncomment and modify the following code if you have an API endpoint to retrieve data.
  /*
  fetch('/api/engine-data')
    .then(response => response.json())
    .then(data => {
      // Assuming the API returns an object with `labels` and `data` arrays.
      engineChart.data.labels = data.labels;
      engineChart.data.datasets[0].data = data.data;
      engineChart.update();
    })
    .catch(error => console.error('Error fetching engine data:', error));
  */
});