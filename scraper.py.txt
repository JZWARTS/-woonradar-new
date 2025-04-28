import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

conn = sqlite3.connect('listings.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS houses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price INTEGER,
    address TEXT,
    size REAL,
    energy_label TEXT,
    garden_terrace TEXT,
    image_url TEXT,
    link TEXT UNIQUE
)
''')
conn.commit()

def scrape_houses():
    url = "https://www.funda.nl/koop/noord-brabant/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    listings = soup.find_all('div', class_='search-result-content')

    for listing in listings:
        try:
            title = listing.find('h2', class_='search-result-title').get_text(strip=True)
            price_text = listing.find('span', class_='search-result-price').get_text(strip=True).replace('€', '').replace('.', '').replace(',', '')
            price = int(''.join(filter(str.isdigit, price_text)))
            address = listing.find('div', class_='search-result-subtitle').get_text(strip=True)
            size_text = listing.find('ul', class_='search-result-kenmerken').get_text(strip=True)
            size = float(''.join(filter(lambda x: x.isdigit() or x == '.', size_text.split('m²')[0])))
            image = listing.find('img')['src'] if listing.find('img') else ''
            link = "https://www.funda.nl" + listing.find('a', class_='search-result__header-title-container')['href']

            energy_label = "Unknown"
            garden_terrace = "Yes" if "tuin" in title.lower() or "terras" in title.lower() else "No"

            try:
                c.execute('''
                INSERT INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, price, address, size, energy_label, garden_terrace, image, link))
                conn.commit()
            except sqlite3.IntegrityError:
                continue  # Dubbel link? Skip.

        except Exception as e:
            print(f"Fout bij scrapen: {e}")

if __name__ == '__main__':
    scrape_houses()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Scrapen klaar!")
    conn.close()
