const target = document.getElementById("target-sentence").textContent.trim();
const typingInput = document.getElementById("typing-input");
const restartButton = document.getElementById("restart-button");
const results = document.getElementById("typing-results");

let startTime = null;
let corrections = 0;
let finished = false;

// Count Backspace presses during the experiment.
typingInput.addEventListener("keydown", (event) => {
    if (event.key === "Backspace" && startTime !== null && !finished) {
        corrections++;
    }
});

// The input event runs whenever the text changes.
typingInput.addEventListener("input", () => {
    if (finished) return;

    // Start timing when the first character appears.
    if (startTime === null && typingInput.value.length > 0) {
        startTime = performance.now();
    }

    // Stop only when the entire sentence matches exactly.
    if (typingInput.value === target) {
        finished = true;
        const endTime = performance.now();

        const timeSeconds = (endTime - startTime) / 1000;
        const speed = target.length / timeSeconds; // characters per second

        results.innerHTML = `
            <p>Total time: ${timeSeconds.toFixed(2)} seconds</p>
            <p>Typing speed: ${speed.toFixed(2)} characters/second</p>
            <p>Backspace corrections: ${corrections}</p>
        `;

        typingInput.disabled = true;

        fetch("/collect-typing", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                typing_time_seconds: Number(timeSeconds.toFixed(2)),
                typing_speed_chars_per_second: Number(speed.toFixed(2)),
                corrections: corrections
            })
        })
            .then((response) => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                console.log("Typing results sent to Flask");
            })
            .catch((error) => console.error("Sending failed:", error));
    }
});

// Restart all measurements, not only the text.
restartButton.addEventListener("click", () => {
    startTime = null;
    corrections = 0;
    finished = false;

    typingInput.disabled = false;
    typingInput.value = "";
    results.textContent = "";
    typingInput.focus();
});