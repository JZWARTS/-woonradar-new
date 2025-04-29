import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import os

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def clean_price(text):
    digits = ''.join(filter(str.isdigit, text))
    return int(digits) if digits else None

def scrape_pararius():
    print("🔎 Scraping Pararius...")
    houses = []

    base_url = "https://www.pararius.nl/koopwoningen/nederland/bestaande-bouw/bouwjaar-1950-2025/0-450000/50m2/50-perceel-m2/page-"

    try:
        for page in range(1, 4):  # scrape 3 pagina's
            url = f"{base_url}{page}"
            print(f"🌐 Bezig met pagina {page}: {url}")
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
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
                    size = 50.0
                    garden_terrace = "Ja" if "tuin" in title.lower() or "terras" in title.lower() else "Nee"
                    energy_label = "Onbekend"
                    date_scraped = datetime.now().strftime('%Y-%m-%d')

                    house = {
                        "title": title,
                        "price": price,
                        "address": address,
                        "size": size,
                        "energy_label": energy_label,
                        "garden_terrace": garden_terrace,
                        "image_url": image,
                        "link": link,
                        "provider": "Pararius",
                        "date_scraped": date_scraped
                    }

                    houses.append(house)
                except Exception as e:
                    print(f"[⚠️ Fout bij listing op pagina {page}]:", e)

    except Exception as e:
        print("❌ Fout bij ophalen pagina's:", e)

    # Opslaan van resultaten
    output_dir = "static"
    output_file = os.path.join(output_dir, "data.json")
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(houses if houses else [], f, indent=2, ensure_ascii=False)
        print(f"✅ {len(houses)} woningen opgeslagen in {output_file}")
    except Exception as e:
        print("❌ Fout bij opslaan van data.json:", e)

if __name__ == "__main__":
    scrape_pararius()
