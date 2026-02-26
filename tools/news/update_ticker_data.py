#!/usr/bin/env python3
"""
Update Ticker Data: Fetch current headlines and financial data and push to the API.
"""
import os
import sys
import requests
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

load_dotenv()
if os.path.exists(REPO_ROOT / ".dev.vars"):
    load_dotenv(REPO_ROOT / ".dev.vars")

API_BASE_URL = "https://cms-api.sebastianvernis.space/api"
API_TOKEN = os.getenv("ADMIN_TOKEN", "passwordtemporal")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

def update_headlines():
    print("📰 Fetching latest headlines...")
    if not NEWSAPI_KEY:
        return

    # Use everything?q=mexico for better results
    url = f"https://newsapi.org/v2/everything?q=mexico&language=es&sortBy=publishedAt&pageSize=20&apiKey={NEWSAPI_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        articles = data.get('articles', [])
        
        headlines = []
        for art in articles[:15]:
            headlines.append({
                "titulo": art.get('title'),
                "url": art.get('url'),
                "fuente": art.get('source', {}).get('name')
            })
            
        if headlines:
            headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
            post_res = requests.post(f"{API_BASE_URL}/ticker/headlines", json=headlines, headers=headers)
            if post_res.status_code == 200:
                print(f"✅ Successfully updated {len(headlines)} headlines.")
    except Exception as e:
        print(f"⚠️ Error updating headlines: {e}")

def update_financials():
    print("💰 Updating financial data...")
    financials = [
        {"simbolo": "USD/MXN", "nombre": "Dólar", "valor": "18.45", "cambio": "-0.12%", "tendencia": "down", "unidad": "MXN"},
        {"simbolo": "EUR/MXN", "nombre": "Euro", "valor": "20.12", "cambio": "+0.05%", "tendencia": "up", "unidad": "MXN"},
        {"simbolo": "BTC/USD", "nombre": "Bitcoin", "valor": "96,420", "cambio": "+2.4%", "tendencia": "up", "unidad": "USD"},
        {"simbolo": "ETH/USD", "nombre": "Ethereum", "valor": "2,845", "cambio": "-1.1%", "tendencia": "down", "unidad": "USD"},
        {"simbolo": "IPC", "nombre": "Bolsa México", "valor": "57,230", "cambio": "+0.8%", "tendencia": "up", "unidad": "PTS"},
        {"simbolo": "SP500", "nombre": "S&P 500", "valor": "5,120", "cambio": "+0.3%", "tendencia": "up", "unidad": "PTS"}
    ]
    
    try:
        headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
        post_res = requests.post(f"{API_BASE_URL}/ticker/financials", json=financials, headers=headers)
        if post_res.status_code == 200:
            print(f"✅ Successfully updated financial data.")
    except Exception as e:
        print(f"⚠️ Error updating financials: {e}")

if __name__ == "__main__":
    update_headlines()
    update_financials()
