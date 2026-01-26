#!/usr/bin/env python3
"""List available Blackbox models"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BLACKBOX_API_KEY')
MODELS_URL = 'https://api.blackbox.ai/v1/models'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

try:
    resp = requests.get(MODELS_URL, headers=headers, timeout=10)
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"\n📋 Modelos disponibles:\n")
        
        if 'data' in data:
            for model in data['data']:
                print(f"  • {model.get('id', model)}")
        else:
            print(data)
    else:
        print(f"Error: {resp.text}")
        
except Exception as e:
    print(f"Error: {e}")
