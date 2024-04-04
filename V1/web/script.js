function predict() {
    var formData = new FormData(document.getElementById("predictionForm"));

    fetch("/predict", {
      method: "POST",
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        // Display prediction result
        document.getElementById("predictionResult").innerText = "Predicted rating: " + data.predicted_rating;
      })
      .catch(error => console.error("Error:", error));
  }