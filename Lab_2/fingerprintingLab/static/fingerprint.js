// ---- Collect browser/environment info ----
const browserLanguage = navigator.language;
const screenAvailWidth = screen.availWidth;
const windowInnerWidth = window.innerWidth;
const intlTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
const intlLocale = new Intl.Locale(navigator.language).toString();
const documentVisibilityState = document.visibilityState;

// ---- Bundle it ----
const features = {
    "Browser language": browserLanguage,
    "Screen available width": screenAvailWidth,
    "Window inner width": windowInnerWidth,
    "Intl timezone": intlTimezone,
    "Intl locale": intlLocale,
    "Document visibility state": documentVisibilityState
};

// ---- Print to console ----
console.log("=== Active Feature Collection ===");
for (const [key, value] of Object.entries(features)) {
    console.log(`${key}: ${value}`);
}
console.table(features); // nice tabular view in DevTools

// ---- Display on the page ----
const outputElement = document.getElementById("feature-output");
outputElement.innerHTML = Object.entries(features)
    .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
    .join("<br>");
fetch("/collect", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(features)
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }
        console.log("Features sent to Flask");
    })
    .catch(error => console.error("Could not send features:", error));






