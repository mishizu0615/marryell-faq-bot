from flask import Flask, request, jsonify
from faq import handle_faq_event

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "Mariel FAQ Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json(silent=True) or {}
    events = body.get("events", [])
    for event in events:
        try:
            handle_faq_event(event)
        except Exception as e:
            print(f"Error: {e}")
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
