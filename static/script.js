function getPrediction() {
    let selectedSymptoms = $("#symptoms").val(); // Fetch selected values using jQuery

    if (selectedSymptoms.length === 0) {
        alert("Please select at least one symptom!");
        return;
    }

    $("#result").html("<p style='color: gray;'>Predicting...</p>");

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: selectedSymptoms })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
        } else {
            document.getElementById("result").innerHTML = `
                <p class="disease"><strong>Predicted Disease:</strong> ${data.prediction}</p>
                <p class="score"><strong>Confidence Score:</strong> ${data.confidence.toFixed(2)}%</p>
                <p class="description"><strong>Description:</strong> ${data.description}</p>
                <p class="precaution-title"><strong>Precautions:</strong></p>
                <ul class="precautions">
                    ${data.precautions.map(p => `<li>${p}</li>`).join("")}
                </ul>
            `;
        }
    })
    .catch(error => console.error("Error:", error));
}
