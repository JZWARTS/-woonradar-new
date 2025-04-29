from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    try:
        with open("static/data.json", encoding="utf-8") as f:
            houses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        houses = []

    if not houses:
        return render_template("loading.html")

    return render_template("dashboard.html", houses=houses)

if __name__ == "__main__":
    app.run(debug=True)
