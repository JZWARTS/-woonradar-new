from flask import Flask, render_template, request
import json
import os
import re

app = Flask(__name__)

# Mapping plaats naar provincie
plaats_naar_provincie = {
    "Diessen": "Noord-Brabant",
    "Beek en Donk": "Noord-Brabant",
    # Voeg hier meer plaatsnamen toe als je wilt uitbreiden
}

@app.route("/")
def dashboard():
    filter_provincie = request.args.get("provincie")
    try:
        with open("static/data.json", encoding="utf-8") as f:
            houses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        houses = []

    # Extract plaats en koppel provincie
    for house in houses:
        match = re.search(r"\((.*?)\)", house.get("address", ""))
        plaats = match.group(1) if match else ""
        house["provincie"] = plaats_naar_provincie.get(plaats, "Onbekend")

    if filter_provincie:
        houses = [h for h in houses if h.get("provincie") == filter_provincie]

    return render_template("dashboard.html", houses=houses)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
