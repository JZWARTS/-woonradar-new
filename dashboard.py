from flask import Flask, render_template, request
import json
import os
import re

app = Flask(__name__)

# 📍 Mapping plaats naar provincie
plaats_naar_provincie = {
    "Diessen": "Noord-Brabant",
    "Beek en Donk": "Noord-Brabant",
    "Tilburg": "Noord-Brabant",
    "Breda": "Noord-Brabant",
    "Eindhoven": "Noord-Brabant",
    "Amsterdam": "Noord-Holland",
    "Rotterdam": "Zuid-Holland",
    "Arnhem": "Gelderland",
    "Zwolle": "Overijssel",
    # Voeg zelf meer plaatsen toe als je wilt!
}

def extract_provincie(address):
    match = re.search(r"\((.*?)\)", address)
    plaats = match.group(1) if match else ""
    return plaats_naar_provincie.get(plaats, "Onbekend")

@app.route("/")
def dashboard():
    provincie_filter = request.args.get("provincie")
    sortering = request.args.get("sortering")

    # Laad huizen
    try:
        with open("static/data.json", encoding="utf-8") as f:
            houses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        houses = []

    # Voeg provincie toe per huis
    for house in houses:
        house["provincie"] = extract_provincie(house.get("address", ""))

    # Filteren op provincie
    if provincie_filter:
        houses = [h for h in houses if h.get("provincie") == provincie_filter]

    # Sorteren op prijs
    if sortering == "prijs_asc":
        houses.sort(key=lambda h: h.get("price") if h.get("price") else 0)

    return render_template("dashboard.html", houses=houses, selected_provincie=provincie_filter, selected_sortering=sortering)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
