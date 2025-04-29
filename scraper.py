import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import os
import json

# === DATABASE AANMAKEN ===
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

def clean_price(text):
    digits = ''.join(filter(str.isdigit, text))
    return int(digits) if digits else None

# === FUNDA ===
def scrape_funda(c):
    print("🔎 Scraping Funda...")
    url = "https://www.funda.nl/zoeken/koop/?selected_area=[%22provincie-noord-brabant%22]&availability=[%22available%22]&object_type=[%22house%22,%22apartment%22]&floor_area=%2250-%22&energy_label=[%22A%2B%2B%2B%2B%2B%22,%22A%2B%2B%2B%2B%22,%22A%2B%2B%2B%22,%22A%2B%2B%22,%22A%2B%22,%22A%22,%22B%22,%22C%22,%22D%22]&exterior_space_type=[%22garden%22,%22balcony%22,%22terrace%22]&construction_type=[%22resale%22]&construction_period=[%22after_2020%22,%22from_2011_to_2020%22,%22from_2001_to_2010%22,%22from_1991_to_2000%22,%22from_1981_to_1990%22,%22from_1971_to_1980%22,%22from_1960_to_1970%22]&price=%22-450000%22&zoom=11&centerLat=51.6051&centerLng=5.3398"
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        listings = soup.find_all("div", class_="search-result-content")

        for item in listings:
            try:
                title = item.find("h2", class_="search-result-title").get_text(strip=True)
                price_raw = item.find("span", class_="search-result-price").get_text(strip=True)
                price = clean_price(price_raw)
                if not price:
                    continue
                address = item.find("div", class_="search-result-subtitle").get_text(strip=True)
                link_tag = item.find("a", class_="search-result__header-title-container")
                link = "https://www.funda.nl" + link_tag["href"] if link_tag else "https://www.funda.nl"
                image = item.find("img")["src"] if item.find("img") else ""
                size = 50.0  # placeholder
                garden_terrace = "Ja" if any(w in title.lower() for w in ["tuin", "terras"]) else "Nee"
                energy_label = "Onbekend"
                date_scraped = datetime.now().strftime('%Y-%m-%d')

                c.execute('''
                    INSERT OR IGNORE INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link, provider, date_scraped)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, price, address, size, energy_label, garden_terrace, image, link, "Funda", date_scraped))
            except Exception as e:
                print("[Funda item error]", e)
        print("✅ Funda scraping klaar.")
    except Exception as e:
        print("[Funda] Failed:", e)

# === PARARIUS ===
def scrape_pararius(c):
    print("🔎 Scraping Pararius...")
    url = "https://www.pararius.nl/koopwoningen/noord-brabant"
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        listings = soup.find_all("section", class_="listing-search-item")

        for item in listings:
            try:
                title = item.find("a", class_="listing-search-item__link--title").get_text(strip=True)
                price_raw = item.find("div", class_="listing-search-item__price").get_text(strip=True)
                price = clean_price(price_raw)
                if not price:
                    continue
                address = item.find("div", class_="listing-search-item__sub-title").get_text(strip=True)
                link = "https://www.pararius.nl" + item.find("a")["href"]
                image = item.find("img")["src"] if item.find("img") else ""
                size = 50.0  # placeholder
                garden_terrace = "Ja" if any(w in title.lower() for w in ["tuin", "terras"]) else "Nee"
                energy_label = "Onbekend"
                date_scraped = datetime.now().strftime('%Y-%m-%d')

                c.execute('''
                    INSERT OR IGNORE INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link, provider, date_scraped)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, price, address, size, energy_label, garden_terrace, image, link, "Pararius", date_scraped))
            except Exception as e:
                print("[Pararius item error]", e)
        print("✅ Pararius scraping klaar.")
    except Exception as e:
        print("[Pararius] Failed:", e)

# === VBO via vastgoednederland.nl ===
def scrape_vbo(c):
    print("🔎 Scraping VBO via VastgoedNederland...")
    url = "https://aanbod.vastgoednederland.nl/koopwoningen?q=&straal=&koopprijs_van=&koopprijs_tot=450000&oppervlakte=50%2B+m%26sup2%3B&bouwperiode=1960-1970&energielabel=D-label"
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        listings = soup.find_all("div", class_="listing")

        for item in listings:
            try:
                title = item.find("div", class_="listing-title").get_text(strip=True)
                address = item.find("div", class_="listing-address").get_text(strip=True)
                price_raw = item.find("div", class_="listing-price").get_text(strip=True)
                price = clean_price(price_raw)
                if not price:
                    continue
                link_tag = item.find("a", href=True)
                link = "https://aanbod.vastgoednederland.nl" + link_tag["href"] if link_tag else "#"
                image = item.find("img")["src"] if item.find("img") else ""
                size = 50.0  # placeholder
                garden_terrace = "Onbekend"
                energy_label = "D"
                date_scraped = datetime.now().strftime('%Y-%m-%d')

                c.execute('''
                    INSERT OR IGNORE INTO houses (title, price, address, size, energy_label, garden_terrace, image_url, link, provider, date_scraped)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, price, address, size, energy_label, garden_terrace, image, link, "VBO", date_scraped))
            except Exception as e:
                print("[VBO item error]", e)
        print("✅ VBO scraping klaar.")
    except Exception as e:
        print("[VBO] Failed:", e)

# === EXPORT NAAR JSON VOOR RENDER DASHBOARD ===
def export_to_json(c):
    c.execute("SELECT title, price, address, size, energy_label, garden_terrace, image_url, link, provider, date_scraped FROM houses")
    rows = c.fetchall()
    columns = ["title", "price", "address", "size", "energy_label", "garden_terrace", "image_url", "link", "provider", "date_scraped"]
    data = [dict(zip(columns, row)) for row in rows]

    if not os.path.exists("static"):
        os.makedirs("static")

    with open("static/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("📦 JSON-export voltooid: static/data.json")

# === MAIN ===
if __name__ == '__main__':
    conn, c = setup_database()

    scrape_funda(c)
    time.sleep(2)
    scrape_pararius(c)
    time.sleep(2)
    scrape_vbo(c)

    conn.commit()

    if not os.path.exists("backups"):
        os.makedirs("backups")
    backup_name = f"backups/listings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    conn.backup(sqlite3.connect(backup_name))

    export_to_json(c)

    conn.close()
    print("🎉 Scraping afgerond op", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
