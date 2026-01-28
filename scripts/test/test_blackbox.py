#!/usr/bin/env python3
"""Test Blackbox API"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BLACKBOX_API_KEY')
API_URL = 'https://api.blackbox.ai/chat/completions'

print(f"API Key: {API_KEY[:20]}..." if API_KEY else "No API Key")
print(f"API URL: {API_URL}")

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

# Test 1: Modelo simple
print("\n🧪 Test 1: blackboxai-pro")
payload1 = {
    "model": "blackboxai-pro",
    "messages": [{"role": "user", "content": "Di hola en español"}],
    "max_tokens": 50
}

try:
    resp = requests.post(API_URL, headers=headers, json=payload1, timeout=10)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Sin system message
print("\n🧪 Test 2: Sin system message")
payload2 = {
    "model": "blackboxai-pro",
    "messages": [{"role": "user", "content": "Reescribe: México es un país"}],
    "temperature": 0.7,
    "max_tokens": 100
}

try:
    resp = requests.post(API_URL, headers=headers, json=payload2, timeout=10)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Modelo diferente
print("\n🧪 Test 3: Modelo blackboxai")
payload3 = {
    "model": "blackboxai",
    "messages": [{"role": "user", "content": "Test"}],
    "max_tokens": 50
}

try:
    resp = requests.post(API_URL, headers=headers, json=payload3, timeout=10)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
