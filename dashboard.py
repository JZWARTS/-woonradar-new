from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# --- Functie om woningen op te halen ---
def get_filtered_houses(filters):
    try:
        conn = sqlite3.connect('data/houses.db')
        c = conn.cursor()

        query = "SELECT * FROM houses WHERE 1=1"
        params = []

        if filters.get('city'):
            query += " AND address LIKE ?"
            params.append(f"%{filters['city']}%")
        if filters.get('min_price'):
            query += " AND price >= ?"
            params.append(filters['min_price'])
        if filters.get('max_price'):
            query += " AND price <= ?"
            params.append(filters['max_price'])
        if filters.get('min_size'):
            query += " AND size >= ?"
            params.append(filters['min_size'])
        if filters.get('energy_label'):
            query += " AND energy_label = ?"
            params.append(filters['energy_label'])
        if filters.get('garden_terrace') == 'Yes':
            query += " AND garden_terrace = 'Yes'"

        query += " ORDER BY price ASC"

        c.execute(query, params)
        houses = c.fetchall()
        conn.close()
        return houses

    except sqlite3.OperationalError:
        # Als database of tabel niet bestaat ➔ geef lege lijst terug
        return []

# --- Homepagina route ---
@app.route('/')
def dashboard():
    filters = request.args
    houses = get_filtered_houses(filters)

    if len(houses) == 0:
        return render_template('loading.html')

    return render_template('dashboard.html', houses=houses)

# --- Geen data gevonden pagina ---
@app.route('/no-data')
def no_data():
    return render_template('no_data.html')

# --- App starten als script ---
if __name__ == "__main__":
    app.run(debug=True)
