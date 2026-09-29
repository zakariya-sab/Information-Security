from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

analytics_log = []


@app.route("/")
def home():
    return "Analytics server is running"


@app.route("/collect")
def collect():
    visit = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analytics_id": request.args.get("id", "unknown"),
        
        "publisher": request.args.get("publisher", "unknown"),
        "page": request.args.get("page", "unknown")
    }

    analytics_log.append(visit)

    print("\n--- ANALYTICS PROFILE ---")

    for item in analytics_log:
        print(
            f'{item["time"]} | '
            f'ID={item["analytics_id"]} | '
            f'Publisher={item["publisher"]} | '
            f'Page={item["page"]}'
        )

    # A tiny transparent image response
    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9100, debug=True)