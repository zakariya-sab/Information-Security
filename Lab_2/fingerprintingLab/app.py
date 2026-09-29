from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/")
def home():
    print("\n========== NEW VISIT ==========")
    # Information about the request and network connection
    #print("IP address :", request.remote_addr)
    #print("HTTP method :", request.method)
    # Examples of passive HTTP features
    #print("User-Agent :", request.headers.get("User-Agent"))
    #print("Accept-Language :", request.headers.get("Accept-Language"))

    # TODO: Add the other passive features identified in Task 0.
    # Example:
    #print("Host             :", request.headers.get("Host"))
    #print("Accept           :", request.headers.get("Accept"))
    #print("Sec-Fetch-Mode   :", request.headers.get("Sec-Fetch-Mode"))
    #print("Sec-CH-UA-Platform:", request.headers.get("Sec-CH-UA-Platform"))
    #print("Sec-Fetch-Site   :", request.headers.get("Sec-Fetch-Site"))


    




    
    
    #print("From :", request.headers.get("From "))
    print("================================\n")
    return render_template("index.html")

@app.route("/collect", methods=["POST"])
def collect():
    features = request.get_json()

    print("\n=== ACTIVE FEATURES RECEIVED ===")
    for name, value in features.items():
        print(f"{name}: {value}")

    return {"status": "received"}

@app.route("/collect-typing", methods=["POST"])
def collect_typing():
    data = request.get_json()

    print("\n=== TYPING RESULTS RECEIVED ===")
    print("Time (seconds):", data.get("typing_time_seconds"))
    print("Speed (characters/second):",
          data.get("typing_speed_chars_per_second"))
    print("Backspace corrections:", data.get("corrections"))

    return {"status": "received"}

@app.route("/collect-fingerprint", methods=["POST"])
def collect_fingerprint():
    data = request.get_json()
    print("Fingerprint:", data.get("fp"))
    return {"status": "received"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)