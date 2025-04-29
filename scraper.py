import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

# Setup database
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


def scrape_funda():
    print("Scraping Funda...")
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

            garden_terrace = "Ja" if "tuin" in title.lower() or "terras" in title.lower() else "Nee"

            c.execute('''
                INSERT OR IGNORE INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, price, address, size, "Onbekend", garden_terrace, image, link))
            conn.commit()
        except Exception as e:
            print(f"[Funda] Fout bij scrapen: {e}")


def scrape_kin():
    print("Scraping KIN Makelaars...")
    url = "https://www.kinmakelaars.nl/nl/woningaanbod"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', class_='object-intro')

    for card in cards:
        try:
            title = card.find('a', class_='object-title').get_text(strip=True)
            address = card.find('div', class_='object-street').get_text(strip=True)
            link = card.find('a')['href']
            image = card.find_previous_sibling('div', class_='object-image').find('img')['src']
            price = 0
            size = 0.0

            c.execute('''
                INSERT OR IGNORE INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, price, address, size, "Onbekend", "Onbekend", image, link))
            conn.commit()
        except Exception as e:
            print(f"[KIN] Fout bij scrapen: {e}")


def scrape_boumij():
    print("Scraping Boumij Makelaars...")
    url = "https://boumij.nl/api/v1/property/list"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        for item in data.get("data", []):
            try:
                title = item.get("title", "Onbekend")
                address = item.get("street", "") + ", " + item.get("city", "")
                link = "https://boumij.nl/woningaanbod/" + str(item.get("slug", ""))
                price = int(item.get("price", 0))
                size = float(item.get("living_surface", 0) or 0)
                image = item.get("main_image", {}).get("url", "")
                energy_label = item.get("energy_label", "Onbekend")
                garden_terrace = "Ja" if "tuin" in title.lower() or "terras" in title.lower() else "Nee"

                c.execute('''
                    INSERT OR IGNORE INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, price, address, size, energy_label, garden_terrace, image, link))
                conn.commit()
            except Exception as e:
                print(f"[Boumij woning fout] {e}")
    except Exception as e:
        print(f"[Boumij API fout] {e}")


if __name__ == '__main__':
    scrape_funda()
    scrape_kin()
    scrape_boumij()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Scrapen compleet!")
    conn.close()
