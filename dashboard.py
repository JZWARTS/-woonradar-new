from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    print("🔍 Route '/' werd opgevraagd")  # Debug
    try:
        with open("static/data.json", encoding="utf-8") as f:
            houses = json.load(f)
            print(f"✅ {len(houses)} woningen geladen uit data.json")  # Debug
    except FileNotFoundError:
        print("⚠️ Bestand data.json niet gevonden")
        houses = []
    except json.JSONDecodeError:
        print("⚠️ JSON fout in data.json")
        houses = []

    if not houses:
        return render_template("loading.html")

    return render_template("dashboard.html", houses=houses)

if __name__ == "__main__":
    print("🚀 dashboard.py gestart")
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Start server op poort {port}...")
    app.run(host="0.0.0.0", port=port)
