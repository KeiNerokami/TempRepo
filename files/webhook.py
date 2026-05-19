import logging
from hmac import compare_digest

from flask import Flask, Response, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

VERIFY_TOKEN = "mybotsecret2026"


@app.route("/webhook", methods=["GET", "POST"], strict_slashes=False)
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode", "")
        token = request.args.get("hub.verify_token", "")
        challenge = request.args.get("hub.challenge", "")

        if mode == "subscribe" and compare_digest(token, VERIFY_TOKEN) and challenge:
            app.logger.info("Meta webhook verified successfully.")
            return Response(challenge, status=200, mimetype="text/plain")

        app.logger.warning("Meta webhook verification failed.")
        return Response("Forbidden", status=403, mimetype="text/plain")

    data = request.get_json(silent=True) or {}
    app.logger.info("Received Meta webhook event: %s", data)

    return Response("EVENT_RECEIVED", status=200, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
