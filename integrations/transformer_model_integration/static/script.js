function fetchPrediction() {
    fetch('/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({data: latest60Data})
    })
    .then(response => response.json())
    .then(data => {
        updateDashboard(data.prediction);
    });
}

setInterval(fetchPrediction, 5000);