from flask import Flask, render_template, request
import json
import os
import re

app = Flask(__name__)

# 📍 Grote plaats naar provincie mapping
plaats_naar_provincie = {
    "Amsterdam": "Noord-Holland",
    "Rotterdam": "Zuid-Holland",
    "Utrecht": "Utrecht",
    "Groningen": "Groningen",
    "Den Haag": "Zuid-Holland",
    "Eindhoven": "Noord-Brabant",
    "Tilburg": "Noord-Brabant",
    "Breda": "Noord-Brabant",
    "Nijmegen": "Gelderland",
    "Arnhem": "Gelderland",
    "Haarlem": "Noord-Holland",
    "Enschede": "Overijssel",
    "Zwolle": "Overijssel",
    "Leeuwarden": "Friesland",
    "Maastricht": "Limburg",
    "Venlo": "Limburg",
    "Middelburg": "Zeeland",
    "Assen": "Drenthe",
    "Almere": "Flevoland",
    "Apeldoorn": "Gelderland",
    "Helmond": "Noord-Brabant",
    "Dordrecht": "Zuid-Holland",
    "Leiden": "Zuid-Holland",
    "Amersfoort": "Utrecht",
    "Zaanstad": "Noord-Holland",
    "Roosendaal": "Noord-Brabant",
    "Oss": "Noord-Brabant",
    "Heerlen": "Limburg",
    "Sittard-Geleen": "Limburg",
    "Emmen": "Drenthe",
    "Gouda": "Zuid-Holland",
    "Hengelo": "Overijssel",
    "Vlissingen": "Zeeland",
    "Hoorn": "Noord-Holland",
    "Delft": "Zuid-Holland",
    "Tiel": "Gelderland",
    "Weert": "Limburg",
    "Ede": "Gelderland",
    "Nieuwegein": "Utrecht",
    "Zeist": "Utrecht",
    "Harderwijk": "Gelderland",
    "Heerenveen": "Friesland",
    "Hilversum": "Noord-Holland",
    "Goes": "Zeeland",
    "Hoogeveen": "Drenthe",
    "Schiedam": "Zuid-Holland",
    "Capelle aan den IJssel": "Zuid-Holland",
    "Purmerend": "Noord-Holland",
    "Veenendaal": "Utrecht",
    "Houten": "Utrecht",
    "Woerden": "Utrecht"
    # ➔ Hier kun je later altijd nog meer plaatsen aan toevoegen
}

# 🧠 Functie om provincie te bepalen uit adres
def extract_provincie(address):
    if not address:
        return "Onbekend"
    # Eerst zoeken naar haakjes (bijv: (Tilburg))
    match = re.search(r"\((.*?)\)", address)
    if match:
        plaats = match.group(1).strip()
    else:
        # Als geen haakjes, pak alles na laatste komma
        delen = address.split(',')
        plaats = delen[-1].strip() if len(delen) > 1 else address.strip()

    return plaats_naar_provincie.get(plaats, "Onbekend")

# 🌐 Route voor dashboard
@app.route("/")
def dashboard():
    provincie_filter = request.args.get("provincie")
    sortering = request.args.get("sortering")

    try:
        with open("static/data.json", encoding="utf-8") as f:
            houses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        houses = []

    # Provincie toevoegen per woning
    for house in houses:
        house["provincie"] = extract_provincie(house.get("address", ""))

    # Filteren op provincie
    if provincie_filter:
        houses = [h for h in houses if h.get("provincie") == provincie_filter]

    # Sorteren op prijs
    if sortering == "prijs_asc":
        houses.sort(key=lambda h: h.get("price") if h.get("price") else 0)
    elif sortering == "prijs_desc":
        houses.sort(key=lambda h: h.get("price") if h.get("price") else 0, reverse=True)

    return render_template("dashboard.html", houses=houses, selected_provincie=provincie_filter, selected_sortering=sortering)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
