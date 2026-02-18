#!/usr/bin/env python3
"""
Test Blackbox API - Versión mejorada para nuevos flujos
Soporta múltiples API keys y modelos
"""

import os
import sys
import requests
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

# Colores ANSI
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

API_URL = 'https://api.blackbox.ai/chat/completions'

def get_available_keys() -> List[Dict]:
    """Obtiene todas las API keys disponibles"""
    keys = []

    key_configs = [
        ('BLACKBOX_API_KEY', 'DEFAULT'),
        ('BLACKBOX_API_KEY_PRO', 'PRO'),
        ('BLACKBOX_API_KEY_FREE', 'FREE'),
        ('BLACKBOX_API_KEY_ALT', 'ALT'),
        ('BLACKBOX_API_KEY_1', 'KEY_1'),
        ('BLACKBOX_API_KEY_2', 'KEY_2'),
    ]

    for env_name, key_id in key_configs:
        key_value = os.getenv(env_name)
        if key_value and 'PENDIENTE' not in str(key_value):
            keys.append({
                'id': key_id,
                'env_name': env_name,
                'key': key_value
            })

    return keys

def test_key(key_config: Dict, model: str = "blackboxai-pro") -> Dict:
    """Testea una API key específica"""
    result = {
        'key_id': key_config['id'],
        'model': model,
        'success': False,
        'status_code': None,
        'response': None,
        'error': None
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key_config["key"]}'
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Di 'Test OK' en español"}],
        "max_tokens": 50
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        result['status_code'] = resp.status_code

        if resp.status_code == 200:
            data = resp.json()
            if 'choices' in data and len(data['choices']) > 0:
                result['success'] = True
                result['response'] = data['choices'][0]['message']['content']
            else:
                result['error'] = "Respuesta sin choices"
        else:
            result['error'] = f"HTTP {resp.status_code}: {resp.text[:200]}"

    except Exception as e:
        result['error'] = str(e)

    return result

def main():
    """Ejecuta tests de Blackbox API"""
    print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🤖 TEST BLACKBOX API - Verificación de conectividad             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
""")

    # Obtener keys disponibles
    available_keys = get_available_keys()

    print(f"{Colors.BOLD}API Keys encontradas: {len(available_keys)}{Colors.ENDC}\n")

    if not available_keys:
        print(f"{Colors.RED}❌ No se encontraron API keys configuradas{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}Configura al menos una de estas variables en .env:{Colors.ENDC}")
        print("  - BLACKBOX_API_KEY")
        print("  - BLACKBOX_API_KEY_PRO")
        print("  - BLACKBOX_API_KEY_FREE")
        print("  - BLACKBOX_API_KEY_ALT")
        return 1

    # Mostrar keys encontradas
    for key_config in available_keys:
        masked = key_config['key'][:8] + '...' + key_config['key'][-4:]
        print(f"  ✅ {key_config['id']}: {masked}")

    print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}Testeando conexión con Blackbox API...{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

    # Testear cada key
    results = []
    models_to_test = ["blackboxai-pro", "blackboxai"]

    for key_config in available_keys:
        for model in models_to_test:
            print(f"  Testing {key_config['id']} con modelo {model}...", end=" ")
            result = test_key(key_config, model)
            results.append(result)

            if result['success']:
                print(f"{Colors.GREEN}✅ OK{Colors.ENDC}")
            else:
                print(f"{Colors.RED}❌ FAIL{Colors.ENDC}")
                if result['error']:
                    print(f"      Error: {result['error'][:80]}")

    # Resumen
    print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}📊 RESUMEN{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

    successful = sum(1 for r in results if r['success'])
    total = len(results)

    print(f"  Tests exitosos: {Colors.GREEN}{successful}{Colors.ENDC}/{total}")
    print(f"  Tests fallidos: {Colors.RED}{total - successful}{Colors.ENDC}/{total}")

    if successful > 0:
        print(f"\n  {Colors.GREEN}✅ Blackbox API está operativa{Colors.ENDC}")
        if len(available_keys) >= 2:
            print(f"  {Colors.GREEN}✅ Modo paralelo disponible ({len(available_keys)} keys){Colors.ENDC}")
        else:
            print(f"  {Colors.YELLOW}⚠️  Solo modo estándar disponible (1 key){Colors.ENDC}")
        return 0
    else:
        print(f"\n  {Colors.RED}❌ No se pudo conectar con Blackbox API{Colors.ENDC}")
        print(f"  {Colors.YELLOW}Verifica tus API keys y conexión a internet{Colors.ENDC}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
