import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

PARARIUS_URL = "https://www.pararius.nl/koopwoningen/nederland/bestaande-bouw/bouwjaar-1950-2025/0-450000/50m2/50-perceel-m2/page-"
HUISLIJN_URL = "https://www.huislijn.nl/koopwoning/nederland?order=relevance&c-maxPrice=450000&c-livingArea=49&c-buildDate=1960%251970&page="
MAX_PAGES = 5

def clean_price(text):
    digits = ''.join(filter(str.isdigit, text))
    return int(digits) if digits else None

def scrape_pararius():
    print("\n🔎 Scrapen van Pararius gestart...")
    woningen = []

    for page in range(1, MAX_PAGES + 1):
        url = f"{PARARIUS_URL}{page}"
        print(f"🌍 Pararius pagina {page}: {url}")
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
        except Exception as e:
            print(f"❌ Fout bij ophalen Pararius pagina {page}: {e}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        listings = soup.find_all("section", class_="listing-search-item")
        if not listings:
            break

        for item in listings:
            try:
                title = item.find("a", class_="listing-search-item__link--title").get_text(strip=True)
                price = clean_price(item.find("div", class_="listing-search-item__price").get_text(strip=True))
                if not price:
                    continue
                address = item.find("div", class_="listing-search-item__sub-title").get_text(strip=True)
                link = "https://www.pararius.nl" + item.find("a")["href"]
                image = item.find("img")["src"] if item.find("img") else ""
                size = 50.0
                garden_terrace = "Ja" if any(word in title.lower() for word in ["tuin", "terras"]) else "Nee"
                woningen.append({
                    "title": title,
                    "price": price,
                    "address": address,
                    "size": size,
                    "energy_label": "Onbekend",
                    "garden_terrace": garden_terrace,
                    "image_url": image,
                    "link": link,
                    "provider": "Pararius",
                    "date_scraped": datetime.today().strftime('%Y-%m-%d')
                })
            except Exception as e:
                print(f"⚠️ Fout bij Pararius listing op pagina {page}: {e}")
    return woningen

def scrape_huislijn():
    print("\n🔎 Scrapen van Huislijn gestart...")
    woningen = []

    for page in range(1, MAX_PAGES + 1):
        url = f"{HUISLIJN_URL}{page}"
        print(f"🌍 Huislijn pagina {page}: {url}")
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
        except Exception as e:
            print(f"❌ Fout bij ophalen Huislijn pagina {page}: {e}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        listings = soup.find_all("article", class_="property-list-item")
        if not listings:
            break

        for item in listings:
            try:
                title = item.find("h2").get_text(strip=True)
                price = clean_price(item.find(class_="price").get_text(strip=True))
                if not price:
                    continue
                address = item.find(class_="address").get_text(strip=True)
                size = 50.0
                image = item.find("img")["src"] if item.find("img") else ""
                link = "https://www.huislijn.nl" + item.find("a")["href"]
                garden_terrace = "Ja" if any(word in title.lower() for word in ["tuin", "terras"]) else "Nee"
                woningen.append({
                    "title": title,
                    "price": price,
                    "address": address,
                    "size": size,
                    "energy_label": "Onbekend",
                    "garden_terrace": garden_terrace,
                    "image_url": image,
                    "link": link,
                    "provider": "Huislijn",
                    "date_scraped": datetime.today().strftime('%Y-%m-%d')
                })
            except Exception as e:
                print(f"⚠️ Fout bij Huislijn listing op pagina {page}: {e}")
    return woningen

def save_data(woningen):
    os.makedirs("static", exist_ok=True)
    output_path = os.path.join("static", "data.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(woningen, f, indent=2, ensure_ascii=False)
        print(f"\n✅ {len(woningen)} woningen opgeslagen in {output_path}")
    except Exception as e:
        print(f"❌ Fout bij opslaan van data: {e}")

if __name__ == "__main__":
    woningen = scrape_pararius() + scrape_huislijn()
    save_data(woningen)
