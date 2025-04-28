# 🏡 Woon Radar

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Welkom bij **Woon Radar** – een scraper en dashboard waarmee je woningen kunt zoeken en filteren!

---

## 🚀 Functionaliteiten
- Zoekt automatisch huizen van Funda (Noord-Brabant).
- Filter op stad, prijs, grootte, energielabel en tuin/terras.
- Automatische scraping elke 4 uur.
- Backups van de database worden automatisch gemaakt.
- Gemaakt met Flask, BeautifulSoup, SQLite en Pandas.

---

## 📋 Installatie (lokaal)

1. Installeer de vereiste libraries:

   ```bash
   pip install flask beautifulsoup4 pandas requests gunicorn
