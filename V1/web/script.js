function predict() {
    var episodes = document.getElementById("episodes").value;
    var members = document.getElementById("members").value;
    var timespan = document.getElementById("timespan").value;

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ episode: episodes, member: members, timespan: timespan }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert("Predicted rating: " + data.prediction);
    })
    .catch(error => {
        console.error('Error predicting:', error);
    });
}
