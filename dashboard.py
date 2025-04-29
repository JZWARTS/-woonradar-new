from flask import Flask, render_template, request
import json

app = Flask(__name__)

def bepaal_provincie(adres):
    plaats_provincie = {
        "Amsterdam": "Noord-Holland",
        "Rotterdam": "Zuid-Holland",
        "Utrecht": "Utrecht",
        "Eindhoven": "Noord-Brabant",
        "Arnhem": "Gelderland",
        "Tilburg": "Noord-Brabant",
        "Maastricht": "Limburg",
        "Groningen": "Groningen",
        "Leeuwarden": "Friesland",
        "Zwolle": "Overijssel",
        "Nijmegen": "Gelderland",
        "Den Haag": "Zuid-Holland",
        "Breda": "Noord-Brabant",
        "Almere": "Flevoland",
        "Haarlem": "Noord-Holland",
        "Enschede": "Overijssel",
        "Apeldoorn": "Gelderland"
    }
    for plaats, provincie in plaats_provincie.items():
        if plaats.lower() in adres.lower():
            return provincie
    return "Onbekend"

@app.route("/")
def dashboard():
    with open("data.json", "r", encoding="utf-8") as file:
        houses = json.load(file)

    for h in houses:
        h["province"] = bepaal_provincie(h.get("address", ""))

    geselecteerde_provincie = request.args.get("provincie")
    sort = request.args.get("sortering")

    if geselecteerde_provincie:
        houses = [h for h in houses if h.get("province") == geselecteerde_provincie]

    if sort == "prijs_asc":
        houses.sort(key=lambda h: h.get("price", 0))
    elif sort == "prijs_desc":
        houses.sort(key=lambda h: h.get("price", 0), reverse=True)

    provincies = sorted(set(h.get("province", "Onbekend") for h in houses))

    return render_template("dashboard.html", houses=houses, provincies=provincies, selected_provincie=geselecteerde_provincie)

if __name__ == "__main__":
    app.run(debug=True)
