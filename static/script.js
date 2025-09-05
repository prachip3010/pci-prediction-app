async function makePrediction() {
    const form = document.getElementById("predictionForm");
    const formData = new FormData(form);
    let data = {};

    formData.forEach((value, key) => {
        data[key] = value;
    });

    document.getElementById("loading").style.display = "block";
    document.getElementById("resultSection").style.display = "none";
    document.getElementById("errorMessage").style.display = "none";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        document.getElementById("loading").style.display = "none";

        if (response.ok) {
            document.getElementById("resultValue").innerText = result.prediction.toFixed(2);
            document.getElementById("resultSection").style.display = "block";
        } else {
            document.getElementById("errorMessage").innerText = "Prediction failed: " + result.error;
            document.getElementById("errorMessage").style.display = "block";
        }
    } catch (error) {
        document.getElementById("loading").style.display = "none";
        document.getElementById("errorMessage").innerText = "Error: " + error.message;
        document.getElementById("errorMessage").style.display = "block";
    }
}
