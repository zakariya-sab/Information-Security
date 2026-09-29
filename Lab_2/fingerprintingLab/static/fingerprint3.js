async function buildFingerprint() {
    // Always keep the features in the same order.
    const values = [
        navigator.language,
        screen.availWidth,
        Intl.DateTimeFormat().resolvedOptions().timeZone,
        new Intl.Locale(navigator.language).toString()
    ];

    const combined = values.join(" | ");
    const bytes = new TextEncoder().encode(combined);

    // SHA-256 returns bytes; convert them to a readable hexadecimal string.
    const hashBuffer = await crypto.subtle.digest("SHA-256", bytes);
    const hash = Array.from(new Uint8Array(hashBuffer))
        .map(byte => byte.toString(16).padStart(2, "0"))
        .join("");
    const message = "Browser fingerprint: " + hash;
    document.getElementById("fingerprint-output").textContent = message;
    console.log("Browser fingerprint:", hash);

    // Send only the hash for this mission.
    const response = await fetch("/collect-fingerprint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fp: hash })
    });

    if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
    }
}

buildFingerprint().catch(error => {
    console.error("Fingerprint failed:", error);
    document.getElementById("fingerprint-output").textContent =
        "Could not calculate fingerprint.";
});