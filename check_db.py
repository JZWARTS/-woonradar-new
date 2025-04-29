import sqlite3

try:
    conn = sqlite3.connect("listings.db")
    c = conn.cursor()

    # Controleer of de tabel bestaat
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print("Gevonden tabellen:", tables)

    if ('houses',) not in tables:
        print("⚠️  De tabel 'houses' bestaat niet.")
    else:
        # Toon aantal rijen
        c.execute("SELECT COUNT(*) FROM houses")
        count = c.fetchone()[0]
        print(f"✅ Aantal woningen in database: {count}")

        # Toon de eerste 3 resultaten
        if count > 0:
            c.execute("SELECT title, price, address FROM houses LIMIT 3")
            rows = c.fetchall()
            print("\nVoorbeeld resultaten:")
            for row in rows:
                print(row)
        else:
            print("⚠️  Geen woningen gevonden in de database.")
            
except Exception as e:
    print("❌ Fout tijdens openen of uitlezen van de database:", e)
finally:
    conn.close()
