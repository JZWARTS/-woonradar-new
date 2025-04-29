import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

BASE_URL = "https://www.pararius.nl/koopwoningen/nederland/bestaande-bouw/bouwjaar-1950-2025/0-450000/50m2/50-perceel-m2/page-"
MAX_PAGES = 5  # Aantal pagina's om te scrapen

def clean_price(text):
    digits = ''.join(filter(str.isdigit, text))
    return int(digits) if digits else None

def scrape_pararius():
    print("🔎 Scrapen van Pararius gestart...")
    woningen = []

    for page in range(1, MAX_PAGES + 1):
        url = f"{BASE_URL}{page}"
        print(f"🌍 Bezig met pagina {page}: {url}")
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
        except Exception as e:
            print(f"❌ Fout bij ophalen pagina {page}: {e}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        listings = soup.find_all("section", class_="listing-search-item")

        if not listings:
            print(f"ℹ️ Geen resultaten op pagina {page}, stoppen...")
            break

        for item in listings:
            try:
                title = item.find("a", class_="listing-search-item__link--title").get_text(strip=True)
                price_text = item.find("div", class_="listing-search-item__price").get_text(strip=True)
                price = clean_price(price_text)
                if not price:
                    continue

                address = item.find("div", class_="listing-search-item__sub-title").get_text(strip=True)
                link = "https://www.pararius.nl" + item.find("a")["href"]
                image = item.find("img")["src"] if item.find("img") else ""
                size = 50.0  # Standaard als niet vermeld
                garden_terrace = "Ja" if any(word in title.lower() for word in ["tuin", "terras"]) else "Nee"
                energy_label = "Onbekend"
                date_scraped = datetime.today().strftime('%Y-%m-%d')

                woningen.append({
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
                })

            except Exception as e:
                print(f"[⚠️ Fout bij listing op pagina {page}]: {e}")

    # Schrijf naar static/data.json
    output_path = os.path.join("static", "data.json")
    os.makedirs("static", exist_ok=True)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(woningen, f, indent=2, ensure_ascii=False)
        print(f"✅ {len(woningen)} woningen opgeslagen in {output_path}")
    except Exception as e:
        print(f"❌ Fout bij opslaan van data: {e}")

if __name__ == "__main__":
    scrape_pararius()
