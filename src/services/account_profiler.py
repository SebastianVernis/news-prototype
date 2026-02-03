```python
import sys
import json
import os
import requests
from dotenv import load_dotenv

sys.path.append('../..')
from src.database import SessionLocal
from src.models import Account

load_dotenv()

def call_gemini_api(prompt, api_key):
    """
    Wrapper para Gemini 3 Pro API
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(
        f"{url}?key={api_key}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        return text
    else:
        raise Exception(f"Gemini API Error: {response.text}")

def profile_account(account_id):
    """
    Analiza una cuenta y genera su perfil con Gemini 3 Pro
    """
    session = SessionLocal()
    account = session.query(Account).filter_by(id=account_id).first()

    if not account:
        print(f"❌ Account {account_id} not found")
        return

    api_key = os.getenv('GEMINI_API_KEY')

    prompt = f"""
Eres un analista de redes sociales. Analiza esta cuenta:

```
Nombre: {account.account_name}
Plataforma: {account.platform}
Últimos posts: [Aquí integrarías datos reales de la API de la plataforma]
```
Responde SOLO con JSON válido en este formato:
{{
"interests": ["política", "tecnología", "deportes"],
"tone": "formal",
"activity_pattern": {{
"best_hours": [9, 14, 18, 21],
"frequency_per_day": 3
}},
"writing_style": "profesional con emojis ocasionales"
}}
"""

    try:
        response_text = call_gemini_api(prompt, api_key)

        # Extraer JSON de la respuesta
        # Gemini a veces envuelve JSON en ```json ... ```
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()

        profile_data = json.loads(json_str)

        # Guardar perfil
        account.profile = profile_data
        session.commit()

        print(f"✅ Profiled account: {account.account_name}")
        print(f" Interests: {profile_data.get('interests', [])}")
        print(f" Tone: {profile_data.get('tone', 'N/A')}")

    except Exception as e:
        print(f"❌ Error profiling account: {e}")

    session.close()

def profile_all_accounts(campaign_id):
    """
    Profile todas las cuentas de una campaña
    """
    session = SessionLocal()
    accounts = session.query(Account).filter_by(campaign_id=campaign_id).all()
    session.close()

    print(f" Profiling {len(accounts)} accounts...")
    for account in accounts:
        profile_account(account.id)

    print("✅ All accounts profiled")

if __name__ == "__main__":
    # Test con account de ejemplo
    session = SessionLocal()

    # Obtener primera campaign
    from src.models import Campaign
    campaign = session.query(Campaign).first()

    if not campaign:
        print("❌ No campaign found. Run scripts/init_db.py first")
        exit()

    # Crear account de prueba
    account = Account(
        campaign_id=campaign.id,
        platform="facebook",
        account_name="Tech News Daily",
        warmup_status="ready"
    )

    session.add(account)
    session.commit()

    account_id = account.id
    session.close()

    print(f"Testing with account: {account_id}")
    profile_account(account_id)
