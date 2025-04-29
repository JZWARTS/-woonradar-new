import sqlite3
import csv
import os
from datetime import datetime

# Verbind met database
conn = sqlite3.connect('listings.db')
cursor = conn.cursor()

# Haal alle data op uit 'houses' tabel
cursor.execute("SELECT * FROM houses")
rows = cursor.fetchall()

# Haal kolomnamen op
column_names = [description[0] for description in cursor.description]

# Maak map 'exports' aan als die niet bestaat
export_dir = "exports"
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

# Bestandsnaam met datum
filename = os.path.join(export_dir, f"woningen_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

# Schrijf naar CSV-bestand
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(column_names)
    writer.writerows(rows)

print(f"✅ Export succesvol naar: {filename}")

conn.close()
