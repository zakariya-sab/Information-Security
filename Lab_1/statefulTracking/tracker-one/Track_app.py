from flask import Flask, render_template, request, make_response, redirect
from datetime import datetime
import secrets

app = Flask(__name__)

# Temporary server-side log
visit_log = []


@app.route("/")
def track():
    # Read the tracker cookie
    aid = request.cookies.get("aid")
    is_new = aid is None

    # Create an identifier for a new browser
    if is_new:
        aid = secrets.token_hex(8)

    # Read information from the iframe URL
    publisher = request.args.get("publisher", "unknown")
    page = request.args.get("page", "unknown")

    # Record this visit
    visit = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aid": aid,
        "publisher": publisher,
        "page": page
    }

    visit_log.append(visit)

    # Print every received request
    print("\n--- TRACKER REQUEST ---")
    print(request.headers)

    # Print the reconstructed profile chronologically
    print("--- RECONSTRUCTED PROFILE ---")

    for item in visit_log:
        print(
            f'{item["time"]} | '
            f'AID={item["aid"]} | '
            f'Publisher={item["publisher"]} | '
            f'Page={item["page"]}'
        )

    response = make_response(
        render_template(
            "index.html",
            aid=aid,
            publisher=publisher,
            page=page
        )
    )

    # Create a persistent tracker cookie
    if is_new:
        response.set_cookie(
            key="aid",
            value=aid,
            httponly=True,
            max_age=3600,
            #samesite="None",
            #path="/"
        )

    return response

@app.route("/sync-start")
def sync_start():
    # Tracker 1 reads only its own cookie
    aid = request.cookies.get("aid")
    is_new = aid is None

    if is_new:
        aid = secrets.token_hex(8)

    # Send Tracker 1's identifier to Tracker 2 through the URL
    tracker_two_url = (
        f"http://tracker-two.test:9200/sync?aid={aid}"
    )

    response = make_response(redirect(tracker_two_url))

    if is_new:
        response.set_cookie(
            key="aid",
            value=aid,
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            path="/"
        )

    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9000, debug=True)