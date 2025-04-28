import time
import subprocess

def run_scraper():
    while True:
        print("🏠 Scraper gestart...")
        subprocess.run(["python", "scraper.py"])
        print("✅ Scraper afgerond. Wachten voor volgende run...")
        time.sleep(1800)  # 1800 seconden = 30 minuten
        

if __name__ == "__main__":
    run_scraper()
