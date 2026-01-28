# 🚀 Setup Rápido: APILayer WHOIS

## ⚡ Configuración en 3 pasos

### 1️⃣ Obtener API Key

1. Ve a https://apilayer.com/
2. Haz clic en "Sign Up" (registro gratuito)
3. Busca "WHOIS API" en el marketplace
4. Suscríbete al **Free Plan** (100 requests/mes)
5. Copia tu API key del dashboard

### 2️⃣ Configurar en .env

Abre el archivo `.env` en la raíz del proyecto:

```bash
nano .env
# o
code .env
# o
vim .env
```

Agrega esta línea (reemplaza con tu API key real):

```bash
APILAYER_API_KEY="TU_API_KEY_AQUI"
```

**Ejemplo completo del .env:**
```bash
NEWSAPI_KEY="3fe1ad82a95f462c802ebbacd88ce4db"
APITUBE_KEY="api_live_D1N0OMX931jbN50XqMSMdApafgJZ4RIHoOupbxZSa8NTkHRsqMXK22"
NEWSDATA_KEY="pub_34a911c383bb4a849b45816304852164"
WORLDNEWS_KEY="02384c82f02b48bb8c8e0c6fd51ad7e2"
BLACKBOX_API_KEY="sk-Pqln-11XRgKTb3PxUxKUfA"
APILAYER_API_KEY="AbC123xYz456DeF789..."
```

### 3️⃣ Verificar instalación

```bash
python scripts/test/test_apilayer_whois.py
```

**Output esperado:**
```
✅ api_key: PASS
✅ whois_api: PASS
🎉 ¡Todos los tests pasaron!
```

---

## 🎯 Uso

### Generar sitios con verificación de dominios

```bash
# Con APILayer API (recomendado)
python scripts/master_orchestrator.py --verificar-dominios --api-whois

# Con whois local (si lo tienes instalado)
python scripts/master_orchestrator.py --verificar-dominios
```

### Test rápido

```bash
# Test con API
python scripts/domain_verifier.py

# Test solo API (standalone)
python scripts/domain_verifier_apilayer.py
```

---

## 🆘 Problemas comunes

### "API key no encontrada"
- ✅ Verifica que agregaste `APILAYER_API_KEY="..."` en .env
- ✅ Verifica que el .env esté en la raíz del proyecto
- ✅ Verifica que no haya espacios extra alrededor del `=`

### "API key inválida"
- ✅ Copia la API key completa del dashboard de APILayer
- ✅ Asegúrate de estar usando comillas: `APILAYER_API_KEY="tu_key"`
- ✅ Verifica que la suscripción al WHOIS API esté activa

### "Rate limit excedido"
- ✅ Alcanzaste el límite de 100 requests/mes (free plan)
- ✅ Espera al siguiente mes o suscríbete a plan pago
- ✅ Alternativamente usa whois local: `--verificar-dominios` (sin `--api-whois`)

---

## 📖 Documentación completa

Para más detalles, ver: `docs/APILAYER-WHOIS.md`

---

**¿No tienes API key?** El sistema funciona igual sin ella, solo usa whois local si está instalado.
