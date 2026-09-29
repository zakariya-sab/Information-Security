let analyticsId = null;

const cookies = document.cookie.split(";");

for (const cookie of cookies) {
    const [name, value] = cookie.trim().split("=");

    if (name === "analytics_id") {
        analyticsId = value;
    }
}

if (analyticsId === null) {
    const randomBytes = new Uint8Array(8);
    crypto.getRandomValues(randomBytes);

    analyticsId = Array.from(randomBytes)
        .map(byte => byte.toString(16).padStart(2, "0"))
        .join("");

    document.cookie =
        `analytics_id=${analyticsId}; Max-Age=2592000; Path=/; SameSite=Lax`;
}

console.log("Analytics ID:", analyticsId);
const publisher = window.location.hostname;
const page = window.location.pathname;

const collectUrl =
    `http://analytics.test:9100/collect` +
    `?id=${encodeURIComponent(analyticsId)}` +
    `&publisher=${encodeURIComponent(publisher)}` +
    `&page=${encodeURIComponent(page)}`;

fetch(collectUrl, {
    mode: "no-cors"
});

console.log("Analytics visit sent:", {
    analyticsId,
    publisher,
    page
});