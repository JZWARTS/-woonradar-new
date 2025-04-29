from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Vaste lijst met plaats → provincie
def bepaal_provincie(adres):
    plaats_provincie = {
        "Amsterdam": "Noord-Holland",
        "Haarlem": "Noord-Holland",
        "Den Helder": "Noord-Holland",
        "Rotterdam": "Zuid-Holland",
        "Den Haag": "Zuid-Holland",
        "Delft": "Zuid-Holland",
        "Utrecht": "Utrecht",
        "Nieuwegein": "Utrecht",
        "Amersfoort": "Utrecht",
        "Eindhoven": "Noord-Brabant",
        "Tilburg": "Noord-Brabant",
        "Breda": "Noord-Brabant",
        "Den Bosch": "Noord-Brabant",
        "Arnhem": "Gelderland",
        "Nijmegen": "Gelderland",
        "Apeldoorn": "Gelderland",
        "Zwolle": "Overijssel",
        "Enschede": "Overijssel",
        "Deventer": "Overijssel",
        "Leeuwarden": "Friesland",
        "Drachten": "Friesland",
        "Groningen": "Groningen",
        "Delfzijl": "Groningen",
        "Assen": "Drenthe",
        "Emmen": "Drenthe",
        "Middelburg": "Zeeland",
        "Goes": "Zeeland",
        "Maastricht": "Limburg",
        "Heerlen": "Limburg",
        "Sittard": "Limburg",
        "Almere": "Flevoland",
        "Lelystad": "Flevoland"
    }

    adres = adres.lower()
    for plaats, provincie in plaats_provincie.items():
        if plaats.lower() in adres:
            return provincie
    return "Onbekend"

@app.route("/")
def dashboard():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            houses = json.load(file)
    except Exception as e:
        print(f"❌ Kan data.json niet openen: {e}")
        houses = []

    for h in houses:
        h["province"] = bepaal_provincie(h.get("address", ""))

    # Filters ophalen
    geselecteerde_provincie = request.args.get("provincie")
    sort = request.args.get("sortering")

    # Filter toepassen
    if geselecteerde_provincie:
        houses = [h for h in houses if h.get("province") == geselecteerde_provincie]

    # Sortering toepassen
    if sort == "prijs_asc":
        houses.sort(key=lambda h: h.get("price", 0))
    elif sort == "prijs_desc":
        houses.sort(key=lambda h: h.get("price", 0), reverse=True)

    # Vaste lijst met alle provincies
    alle_provincies = [
        "Drenthe", "Flevoland", "Friesland", "Gelderland", "Groningen",
        "Limburg", "Noord-Brabant", "Noord-Holland", "Overijssel",
        "Utrecht", "Zeeland", "Zuid-Holland"
    ]

    return render_template(
        "dashboard.html",
        houses=houses,
        provincies=alle_provincies,
        selected_provincie=geselecteerde_provincie,
        selected_sortering=sort
    )

if __name__ == "__main__":
    app.run(debug=True)
