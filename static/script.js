function generatePrompt() {
    const role = document.getElementById("role").value;
    const goal = document.getElementById("issue").value;
    const model = document.getElementById("model").value;
    const adjective = document.getElementById("adjective").value;
    const platform = document.getElementById("platform").value;
    const area = document.getElementById("area").value;
    const prompts = document.getElementById("noPrompts").value;
    const issue = document.getElementById("issue").value;
    const Tokens = document.getElementById("Tokens").value;
    const temperature = document.getElementById("temperature").value;
    const language = document.getElementById("language").value;
    const like = document.getElementById("like").value;
    const dislike = document.getElementById("dislike").value;

    const generateBtn = document.getElementById("generateBtn");
    const loadingText = document.getElementById("loadingText");
    
    generateBtn.style.display = "none";
    loadingText.style.display = "inline-block";

    fetch("/generate_prompt", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ role, goal, model, adjective, platform, area, prompts, issue, Tokens, temperature, language, like, dislike }),
    })
    .then((response) => response.json())
    .then((data) => {
        // Display the response
        document.getElementById("response").innerText = data.response;
        document.getElementById("responseSuggestions").innerText = data.response_suggestions;
        document.getElementById("responsePrompt").innerText = data.first_prompt;

        loadingText.style.display = "none";
        generateBtn.style.display = "inline-block";
    })
    .catch((error) => {
        console.error("Error:", error);
        loadingText.style.display = "none";
        generateBtn.style.display = "inline-block";
    });
}

function likeSuggestion() {
    // Mark the like button as active and dislike button as inactive
    document.querySelector(".like-button").classList.add("active");
    document.querySelector(".dislike-button").classList.remove("active");

    // Show the input prompt for like action
    const userInput = prompt("You liked the response! Please provide your feedback:");
    if (userInput) {
        // Process the user input (you can perform any action with the input here)
        console.log("User Feedback (Liked):", userInput);
    }
}

function dislikeSuggestion() {
    // Mark the dislike button as active and like button as inactive
    document.querySelector(".dislike-button").classList.add("active");
    document.querySelector(".like-button").classList.remove("active");

    // Show the input prompt for dislike action
    const userInput = prompt("You disliked the response! Please provide your feedback to improve");
    if (userInput) {
        // Process the user input (you can perform any action with the input here)
        console.log("User Feedback (Disliked):", userInput);
    }
}
