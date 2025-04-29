from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Laad en verrijk de data
def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            houses = json.load(f)
            return houses
    except Exception as e:
        print(f"Fout bij laden van data.json: {e}")
        return []

@app.route("/")
def index():
    houses = load_data()

    # Vraag filters op uit de URL
    provincie = request.args.get("provincie")
    sort = request.args.get("sort")

    # Filter op provincie (als gekozen)
    if provincie:
        houses = [h for h in houses if h.get("province") == provincie]

    # Sorteer op prijs als gevraagd
    if sort == "prijs_hoog":
        houses.sort(key=lambda h: h.get("price", 0), reverse=True)
    elif sort == "prijs_laag":
        houses.sort(key=lambda h: h.get("price", 0))

    # Extract unieke provincies voor dropdown
    provincies = sorted(set(h.get("province", "Onbekend") for h in houses))

    return render_template("dashboard.html", houses=houses, provincies=provincies, selected_provincie=provincie)

if __name__ == "__main__":
    app.run(debug=True)
