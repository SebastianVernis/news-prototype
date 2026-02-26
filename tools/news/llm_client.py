# NOTA: No ejecutamos load_dotenv() aquí porque el script principal
# (ai_multi_source_publish_flow.py) ya carga las variables de entorno
# correctamente antes de importar este módulo.

import os
import requests
import json

def chat(provider, model, messages, temperature=0.7, max_tokens=4000):
    if provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("Falta OPENROUTER_API_KEY en las variables de entorno.")
            
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8888", # Opcional para OpenRouter
            "X-Title": "News CMS"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Error OpenRouter: {response.status_code} - {response.text}")
            
    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Falta GEMINI_API_KEY en las variables de entorno.")
            
        # Ensure model name is correct for the API
        model_name = model or "gemini-2.0-flash"
        if not model_name.startswith("models/"):
            full_model_name = f"models/{model_name}"
        else:
            full_model_name = model_name
            
        url = f"https://generativelanguage.googleapis.com/v1beta/{full_model_name}:generateContent?key={api_key}"
        
        # Convert messages to Gemini format (merging system prompt if present for v1 compatibility)
        contents = []
        system_content = ""
        
        for msg in messages:
            if msg['role'] == "system":
                system_content = msg['content'] + "\n\n"
            else:
                role = "user" if msg['role'] == "user" else "model"
                text = msg['content']
                if role == "user" and system_content:
                    text = system_content + text
                    system_content = "" # Only apply once
                
                contents.append({
                    "role": role,
                    "parts": [{"text": text}]
                })
            
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        
        response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        if response.status_code == 200:
            res_json = response.json()
            try:
                return res_json['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError):
                if 'promptFeedback' in res_json:
                    raise Exception(f"Gemini bloqueó el contenido: {res_json['promptFeedback']}")
                raise Exception(f"Estructura de respuesta inesperada de Gemini: {json.dumps(res_json)}")
        else:
            raise Exception(f"Error Gemini: {response.status_code} - {response.text}")

    # Fallback para otros proveedores si existieran
    raise ValueError(f"Proveedor {provider} no soportado.")
