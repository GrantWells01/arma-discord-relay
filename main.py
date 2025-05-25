import os
from flask import Flask, request
import requests

app = Flask(__name__)

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

def build_discord_message(event):
    name = event.get("name")
    data = event.get("data", {})

    if name == "serveradmintools_player_joined":
        return f"> 👤 **{data.get('player')}** joined the game."

    elif name == "serveradmintools_player_killed":
        player = data.get("player")
        instigator = data.get("instigator")

        if instigator == "AI":
            return f"> 🤖 **{player}** was killed by AI."
        elif instigator and instigator != player:
            return f"> 💥 **{player}** was killed by **{instigator}**."
        else:
            return f"> ☠️ **{player}** died."

    elif name == "serveradmintools_game_started":
        return "> 🚀 Game has started!"

    # Fallback for unhandled events
    return f"📢 Unhandled event: `{name}`"

@app.route("/", methods=["POST"])
def handle_event():
    if not request.is_json:
        return "Bad Request", 400

    body = request.get_json()
    if body.get("token") != AUTH_TOKEN:
        return "Unauthorized", 403

    events = body.get("events", [])
    for event in events:
        msg = build_discord_message(event)
        if msg:
            requests.post(DISCORD_WEBHOOK, json={"content": msg})

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
