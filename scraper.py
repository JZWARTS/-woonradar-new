import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import os

# === Database Setup ===
def setup_database():
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
            link TEXT UNIQUE,
            provider TEXT,
            date_scraped TEXT
        )
    ''')
    conn.commit()
    return conn, c

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# === Scraper Functions ===
def scrape_funda(c):
    print("Scraping Funda...")
    url = "https://www.funda.nl/koop/noord-brabant/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
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
                energy_label = "Onbekend"
                date_scraped = datetime.now().strftime('%Y-%m-%d')

                if size >= 50:
                    c.execute('''
                        INSERT OR IGNORE INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link, provider, date_scraped)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (title, price, address, size, energy_label, garden_terrace, image, link, 'Funda', date_scraped))
            except Exception as e:
                print(f"[Funda] Error in listing: {e}")
        print("Funda scraping completed.")
    except Exception as e:
        print(f"[Funda] Failed to scrape: {e}")

def scrape_pararius(c):
    print("Scraping Pararius...")
    url = "https://www.pararius.nl/koopwoningen/noord-brabant"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all('section', class_='listing-search-item')

        for listing in listings:
            try:
                title = listing.find('a', class_='listing-search-item__link--title').get_text(strip=True)
                price_text = listing.find('div', class_='listing-search-item__price').get_text(strip=True).replace('€', '').replace('.', '').replace(',', '')
                price = int(''.join(filter(str.isdigit, price_text)))
                address = listing.find('div', class_='listing-search-item__sub-title').get_text(strip=True)
                size_info = listing.find('li', class_='illustrated-features__item--surface-area')
                size = float(''.join(filter(str.isdigit, size_info.get_text(strip=True).split('m²')[0]))) if size_info else 0
                image = listing.find('img')['src'] if listing.find('img') else ''
                link = "https://www.pararius.nl" + listing.find('a', class_='listing-search-item__link--title')['href']

                garden_terrace = "Ja" if "tuin" in title.lower() or "terras" in title.lower() else "Nee"
                energy_label = "Onbekend"
                date_scraped = datetime.now().strftime('%Y-%m-%d')

                if size >= 50:
                    c.execute('''
                        INSERT OR IGNORE INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link, provider, date_scraped)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (title, price, address, size, energy_label, garden_terrace, image, link, 'Pararius', date_scraped))
            except Exception as e:
                print(f"[Pararius] Error in listing: {e}")
        print("Pararius scraping completed.")
    except Exception as e:
        print(f"[Pararius] Failed to scrape: {e}")

def scrape_vbo(c):
    print("Scraping VBO...")
    url = "https://www.vbo.nl/koopwoningen/noord-brabant"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all('div', class_='property-list-item')

        for listing in listings:
            try:
                title = listing.find('a', class_='property-title').get_text(strip=True)
                price_text = listing.find('div', class_='property-price').get_text(strip=True).replace('€', '').replace('.', '').replace(',', '')
                price = int(''.join(filter(str.isdigit, price_text)))
                address = listing.find('div', class_='property-address').get_text(strip=True)
                size_info = listing.find('div', class_='property-size')
                size = float(''.join(filter(str.isdigit, size_info.get_text(strip=True).split('m²')[0]))) if size_info else 0
                image = listing.find('img')['src'] if listing.find('img') else ''
                link = "https://www.vbo.nl" + listing.find('a', class_='property-title')['href']

                garden_terrace = "Ja" if "tuin" in title.lower() or "terras" in title.lower() else "Nee"
                energy_label = "Onbekend"
                date_scraped = datetime.now().strftime('%Y-%m-%d')

                if size >= 50:
                    c.execute('''
                        INSERT OR IGNORE INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link, provider, date_scraped)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (title, price, address, size, energy_label, garden_terrace, image, link, 'VBO', date_scraped))
            except Exception as e:
                print(f"[VBO] Error in listing: {e}")
        print("VBO scraping completed.")
    except Exception as e:
        print(f"[VBO] Failed to scrape: {e}")

# === Main Run ===
if __name__ == '__main__':
    conn, c = setup_database()

    scrape_funda(c)
    time.sleep(2)
    scrape_pararius(c)
    time.sleep(2)
    scrape_vbo(c)

    conn.commit()

    # Backup database
    if not os.path.exists("backups"):
        os.makedirs("backups")
    backup_name = f"backups/listings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    conn.backup(sqlite3.connect(backup_name))

    conn.close()
    print("All scraping completed at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
