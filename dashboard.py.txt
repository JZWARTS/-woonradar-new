from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_filtered_houses(filters):
    conn = sqlite3.connect('listings.db')
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

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    filters = {}
    if request.method == 'POST':
        filters['city'] = request.form.get('city')
        filters['min_price'] = request.form.get('min_price')
        filters['max_price'] = request.form.get('max_price')
        filters['min_size'] = request.form.get('min_size')
        filters['energy_label'] = request.form.get('energy_label')
        filters['garden_terrace'] = request.form.get('garden_terrace')

    houses = get_filtered_houses(filters)
    return render_template('dashboard.html', houses=houses)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
