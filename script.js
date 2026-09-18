async function checkNews() {
    const newsText = document.getElementById("newsText").value;
    const result = document.getElementById("result");

    if (newsText.trim() === "") {
        result.innerText = "Please enter some news.";
        return;
    }

    result.innerText = "Checking...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                news: newsText
            })
        });

        const data = await response.json();

        result.innerText =
    data.prediction + " (" + data.confidence + "% confidence)";
    } catch (error) {
        result.innerText = "Could not connect to the backend.";
        console.error(error);
    }
}
