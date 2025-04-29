import json
import re

# 🗺️ Vereenvoudigde plaats→provincie mapping
plaats_provincie_map = {
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
    "Nieuwvliet": "Zeeland",
    "Rotterdam": "Zuid-Holland",
    "Westknollendam": "Noord-Holland",
    "Diessen": "Noord-Brabant",
    "Hoorn": "Noord-Holland",
    "Almere": "Flevoland",
    "Einighausen": "Limburg",
    "Vaals": "Limburg",
    "Leek": "Groningen",
    "Sint Jansteen": "Zeeland",
    "Grubbenvorst": "Limburg",
    "Beek en Donk": "Noord-Brabant",
    "Nijmegen": "Gelderland",
    "Hardinxveld-Giessendam": "Zuid-Holland",
    "Leerdam": "Zuid-Holland",
    "Arnhem": "Gelderland",
    "Venlo": "Limburg",
    "Puth": "Limburg",
    "Dordrecht": "Zuid-Holland",
}

# 📄 Lees het data.json bestand
with open("static/data.json", encoding="utf-8") as f:
    houses = json.load(f)

# 🔍 Haal plaatsnaam uit haakjes en koppel aan provincie
for h in houses:
    address = h.get("address", "")
    match = re.search(r"\((.*?)\)", address)
    plaats = match.group(1) if match else None
    provincie = plaats_provincie_map.get(plaats, "Onbekend")
    h["provincie"] = provincie

# 💾 Schrijf terug naar data.json
with open("static/data.json", "w", encoding="utf-8") as f:
    json.dump(houses, f, indent=2, ensure_ascii=False)

print("✅ Provincies toegevoegd aan data.json.")
