import os
from flask import Flask, request
import requests

app = Flask(__name__)

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

@app.route("/", methods=["POST"])
def handle_event():
    if not request.is_json:
        return "Bad Request", 400

    body = request.get_json()
    if body.get("token") != AUTH_TOKEN:
        return "Unauthorized", 403

    for event in body.get("events", []):
        name = event["name"]
        data = event.get("data", {})
        msg = ""

        if name == "serveradmintools_player_joined":
            msg = f"> 👤 Player Joined: **{data.get('player')}**"
        elif name == "serveradmintools_player_killed":
            msg = f"> 💀 Player Killed: **{data.get('player')}**"
        elif name == "serveradmintools_game_started":
            msg = "> ➡️ Game Started!"
        else:
            msg = f"📢 Event: `{name}`"

        requests.post(DISCORD_WEBHOOK, json={"content": msg})

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
