import sqlite3

conn = sqlite3.connect('listings.db')
c = conn.cursor()

c.execute("SELECT * FROM houses LIMIT 10")
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()
