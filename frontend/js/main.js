// frontend/js/main.js

document.getElementById("sensor-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const payload = {
        rpm: parseInt(document.getElementById("rpm").value),
        boost: parseFloat(document.getElementById("boost").value),
        afr: parseFloat(document.getElementById("afr").value),
        oil_temp: parseFloat(document.getElementById("oil_temp").value),
        coolant_temp: parseFloat(document.getElementById("coolant_temp").value),
        knock: parseFloat(document.getElementById("knock").value)
    };

    try {
        const res = await fetch("http://localhost:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        const resultDiv = document.getElementById("result");
        const predText = document.getElementById("prediction-text");

        if (res.ok) {
            predText.textContent = `Prediction: ${data.prediction} (Confidence: ${(data.confidence * 100).toFixed(2)}%)`;
        } else {
            predText.textContent = `Error: ${data.error}`;
        }

        resultDiv.style.display = "block";
    } catch (err) {
        console.error(err);
        alert("API request failed. Check server.");
    }
});