@echo off
echo Starting Woon Radar...
python scraper.py
start http://localhost:5000
python dashboard.py
pause
