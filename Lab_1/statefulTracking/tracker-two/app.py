from flask import Flask, request, make_response
import secrets

app = Flask(__name__)


@app.route("/")
def home():
    bid = request.cookies.get("bid")
    is_new = bid is None

    if is_new:
        bid = secrets.token_hex(8)

    response = make_response(
        f"Tracker 2 identifier: {bid}"
    )

    if is_new:
        response.set_cookie(
            key="bid",
            value=bid,
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            path="/"
        )

    return response
sync_log = []


@app.route("/sync")
def sync():
    # Identifier received from Tracker 1 through the URL
    aid = request.args.get("aid")

    # Tracker 2 reads only its own cookie
    bid = request.cookies.get("bid")
    is_new = bid is None

    if is_new:
        bid = secrets.token_hex(8)

    if aid is None:
        return "Missing Tracker 1 identifier", 400

    pair = {
        "tracker_one_id": aid,
        "tracker_two_id": bid
    }

    sync_log.append(pair)

    print("\n--- COOKIE SYNCING ---")
    print(f"Tracker 1 ID: {aid}")
    print(f"Tracker 2 ID: {bid}")
    print(f"Association: {aid} <-> {bid}")

    response = make_response(
        f"Identifiers synchronized: {aid} <-> {bid}"
    )

    if is_new:
        response.set_cookie(
            key="bid",
            value=bid,
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            path="/"
        )

    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9200, debug=True)