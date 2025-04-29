from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Mapping van gemeenten naar provincies
plaats_naar_provincie = {
    "Someren": "Noord-Brabant",
    "Nieuwvliet": "Zeeland",
    "Oirschot": "Noord-Brabant",
    "Bunschoten-Spakenburg": "Utrecht",
    "Arnhem": "Gelderland",
    "Lunteren": "Gelderland",
    "Maastricht": "Limburg",
    "Bunde": "Limburg",
    "Elst Ut": "Utrecht",
    "Oost-Souburg": "Zeeland",
    "Workum": "Friesland",
    "Tilburg": "Noord-Brabant",
    "Oud-Beijerland": "Zuid-Holland",
    "Goedereede": "Zuid-Holland",
    "Beegden": "Limburg",
    "Hoorn": "Noord-Holland",
    "Sliedrecht": "Zuid-Holland",
    "Almere": "Flevoland",
    "Hoogeveen": "Drenthe",
    "Leiden": "Zuid-Holland",
    "Dordrecht": "Zuid-Holland",
    "Kapelle": "Zeeland",
    "Baexem": "Limburg",
    "Den Ham": "Overijssel",
    "Poortvliet": "Zeeland",
    "Ouddorp": "Zuid-Holland",
    "Zwolle": "Overijssel",
    "Hendrik-Ido-Ambacht": "Zuid-Holland",
    "Amsterdam": "Noord-Holland",
    "Leeuwarden": "Friesland",
    "Terneuzen": "Zeeland",
    "Rotterdam": "Zuid-Holland",
    "Venlo": "Limburg",
    "Puth": "Limburg",
    "Hallum": "Friesland",
    "Heerlen": "Limburg",
    "Apeldoorn": "Gelderland",
    "Beek en Donk": "Noord-Brabant",
    "Nijmegen": "Gelderland",
    "Hardinxveld-Giessendam": "Zuid-Holland",
    "Leerdam": "Zuid-Holland",
    "Arnhem": "Gelderland",
    "Venlo": "Limburg",
    # Voeg hier meer plaatsen toe als nodig
}

def bepaal_provincie(address):
    for plaats in plaats_naar_provincie:
        if plaats.lower() in address.lower():
            return plaats_naar_provincie[plaats]
    return "Onbekend"

@app.route("/")
def dashboard():
    with open("data.json", "r", encoding="utf-8") as f:
        houses = json.load(f)

    # Voeg provincie toe aan elk huis
    for h in houses:
        h['provincie'] = bepaal_provincie(h['address'])

    # Filters ophalen uit URL parameters
    selected_provincie = request.args.get('provincie')
    selected_sortering = request.args.get('sortering')

    # Filteren op provincie als gekozen
    if selected_provincie:
        houses = [h for h in houses if h['provincie'] == selected_provincie]

    # Sorteren op prijs
    if selected_sortering == "prijs_asc":
        houses.sort(key=lambda x: x['price'])
    elif selected_sortering == "prijs_desc":
        houses.sort(key=lambda x: x['price'], reverse=True)

    return render_template("dashboard.html", houses=houses, selected_provincie=selected_provincie, selected_sortering=selected_sortering)

if __name__ == "__main__":
    app.run(debug=True)
