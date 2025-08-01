document.getElementById("sensor-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    
    const data = {
        rpm: parseFloat(document.getElementById("rpm").value),
        boost: parseFloat(document.getElementById("boost").value),
        afr: parseFloat(document.getElementById("afr").value),
        oil_temp: parseFloat(document.getElementById("oil_temp").value),
        coolant_temp: parseFloat(document.getElementById("coolant_temp").value),
        knock: parseFloat(document.getElementById("knock").value),
    };

    const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    const predictionText = result.prediction !== undefined ? 
        `Engine Status: ${result.prediction}` : 
        `Error: ${result.error}`;

    document.getElementById("result").style.display = "block";
    document.getElementById("prediction-text").textContent = predictionText;
});