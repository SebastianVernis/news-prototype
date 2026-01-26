# Configuración de Gemini API para Placeholders

**Objetivo:** Generar artículos placeholder de forma rápida usando Gemini API con rotación de keys

---

## 🔑 Obtener API Keys de Gemini

### Paso 1: Acceder a Google AI Studio

1. Ve a: https://aistudio.google.com/apikey
2. Inicia sesión con tu cuenta de Google
3. Click en "Get API Key" o "Create API Key"

### Paso 2: Crear 3 API Keys

Necesitas crear **3 API keys** para rotación automática:

```
Key 1: Para evitar rate limiting en requests paralelos
Key 2: Backup cuando Key 1 alcance límite
Key 3: Tercera opción para máxima velocidad
```

**Nota:** Con 3 keys puedes hacer hasta 45-60 requests/minuto (15-20 por key)

### Paso 3: Agregar Keys al .env

Abre `.env` y agrega las keys:

```bash
# Gemini API Keys (rotación automática)
GEMINI_API_KEY_1="AIzaSyAD_nK5WV5M-xaamQCwDfQJL4iCEDRLLKg"
GEMINI_API_KEY_2="TU_SEGUNDA_KEY_AQUI"
GEMINI_API_KEY_3="TU_TERCERA_KEY_AQUI"
```

**Estado actual:**
- ✅ KEY_1: Configurada (de tu ejemplo)
- ⏳ KEY_2: Pendiente (agregar cuando la generes)
- ⏳ KEY_3: Pendiente (agregar cuando la generes)

---

## 🔄 Sistema de Rotación de Keys

### Funcionamiento

```python
# El sistema rota automáticamente entre las keys disponibles
Request 1  → usa KEY_1
Request 2  → usa KEY_2
Request 3  → usa KEY_3
Request 4  → usa KEY_1 (reinicia ciclo)
Request 5  → usa KEY_2
...
```

### Ventajas

✅ **Evita rate limiting**
- Distribuye la carga entre múltiples keys
- Cada key maneja ~33% de los requests

✅ **Mayor velocidad**
- 10-15 workers paralelos
- ~3-5 segundos para 20 artículos
- ~30-60 segundos para 200 placeholders

✅ **Tolerancia a fallos**
- Si una key falla, las otras siguen funcionando
- Sistema thread-safe con locks

---

## 📊 Límites de Gemini API

### Free Tier (sin pago)

| Modelo | RPM (Requests/Min) | TPM (Tokens/Min) | RPD (Requests/Day) |
|--------|-------------------|------------------|-------------------|
| gemini-2.0-flash-exp | 15 | 1,000,000 | 1,500 |
| gemini-1.5-flash | 15 | 1,000,000 | 1,500 |

**Con 3 keys:**
- RPM efectivo: ~45 requests/minuto
- Suficiente para generar ~200 placeholders en ~4-5 minutos

---

## 🚀 Uso del Sistema

### Test Básico (con 1 key)

```bash
# Asegúrate de tener al menos GEMINI_API_KEY_1 en .env
python3 scripts/gemini_paraphraser.py
```

### Test con Rotación (3 keys)

```bash
# Agrega las 3 keys al .env
# Ejecuta el test
python3 scripts/gemini_paraphraser.py
```

Salida esperada:
```
🔑 Keys cargadas: 3
🚀 PARAFRASEO PARALELO CON GEMINI
Workers paralelos: 5
Tiempo estimado: ~2s

  [1/5] ✅ Artículo parafraseado...
  [2/5] ✅ Artículo parafraseado...
  ...

🔑 Uso de Keys:
  Total requests: 5
  Keys disponibles: 3
  Requests por key: ~1.7
```

### Generar Placeholders

```bash
python3 scripts/placeholder_generator.py
```

Generará:
- 20 placeholders por categoría
- Parafraseo simple (título + descripción)
- En paralelo con rotación de keys
- ~5 minutos para 200 placeholders

---

## ⚙️ Configuración Avanzada

### Ajustar Número de Workers

En `gemini_paraphraser.py`:

```python
# Más workers = más rápido, pero mayor riesgo de rate limiting
results = paraphraser.parafrasear_lote_paralelo(
    articles,
    max_workers=15  # Ajusta según tus needs
)
```

**Recomendaciones:**
- Con 1 key: max_workers=5
- Con 2 keys: max_workers=10
- Con 3 keys: max_workers=15

### Cambiar Modelo de Gemini

En `gemini_paraphraser.py` línea 18:

```python
# Más rápido (recomendado para placeholders)
GEMINI_API_URL_BASE = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent'

# Alternativas:
# gemini-1.5-flash:generateContent (más rápido)
# gemini-1.5-pro:generateContent (mejor calidad, más lento)
```

---

## 🧪 Testing

### Test 1: Verificar Keys

```bash
cd /home/sebastianvernis/Proyectos/news-prototype/Politica

# Test simple
python3 << 'EOF'
import os
from dotenv import load_dotenv
load_dotenv()

keys = [
    os.getenv('GEMINI_API_KEY_1'),
    os.getenv('GEMINI_API_KEY_2'),
    os.getenv('GEMINI_API_KEY_3')
]

for i, key in enumerate(keys, 1):
    if key and key != "PENDIENTE_KEY_2" and key != "PENDIENTE_KEY_3":
        print(f"✅ KEY_{i}: {key[:20]}...")
    else:
        print(f"⏳ KEY_{i}: No configurada")
EOF
```

### Test 2: Request Simple

```bash
# Test con curl (usando la key del archivo paste_1.txt)
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=AIzaSyAD_nK5WV5M-xaamQCwDfQJL4iCEDRLLKg" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [{
      "parts": [{"text": "Di hola en español"}]
    }]
  }'
```

### Test 3: Parafraseo Paralelo

```bash
python3 scripts/gemini_paraphraser.py
```

---

## 🔧 Solución de Problemas

### Error: 429 Too Many Requests

**Causa:** Rate limiting alcanzado

**Soluciones:**
1. Agrega más keys al .env
2. Reduce `max_workers` (de 15 a 10 o 5)
3. Espera 1 minuto y reintenta
4. Verifica límites en: https://ai.google.dev/pricing

### Error: 401 Unauthorized

**Causa:** API key inválida

**Soluciones:**
1. Verifica que la key esté bien copiada
2. Regenera la key en Google AI Studio
3. Asegúrate de que no tenga espacios extras

### Error: 400 Bad Request

**Causa:** Formato de request incorrecto

**Soluciones:**
1. Verifica que el modelo esté disponible
2. Revisa la estructura del payload
3. Consulta docs: https://ai.google.dev/api/rest

---

## 📈 Performance Esperado

### Con 1 Key

```
5 artículos:    ~5-10 segundos
20 artículos:   ~30-40 segundos
100 artículos:  ~3-4 minutos
```

### Con 3 Keys (Rotación)

```
5 artículos:    ~2-3 segundos
20 artículos:   ~8-12 segundos
100 artículos:  ~45-60 segundos
200 artículos:  ~2-3 minutos
```

---

## 🎯 Uso en Producción

### Generar Sitio con Placeholders

```bash
# El master_orchestrator usará automáticamente:
# 1. Parafraseo completo (Blackbox) para artículos principales
# 2. Parafraseo simple (Gemini paralelo) para placeholders

python3 scripts/master_orchestrator.py
```

Flujo:
1. Descarga 20 noticias principales
2. Parafraseo completo con Blackbox (~40 min)
3. Descarga 200 noticias para placeholders
4. Parafraseo simple con Gemini paralelo (~3 min)
5. Categorización de todo
6. Generación del sitio

**Tiempo total:** ~45-50 minutos (vs ~2 horas sin paralelización)

---

## 📚 Referencias

- **Gemini API Docs:** https://ai.google.dev/docs
- **Get API Key:** https://aistudio.google.com/apikey
- **Pricing & Limits:** https://ai.google.dev/pricing
- **Models:** https://ai.google.dev/models/gemini

---

## ✅ Checklist de Configuración

- [ ] Obtener 3 API keys de Google AI Studio
- [ ] Agregar keys al .env (GEMINI_API_KEY_1, 2, 3)
- [ ] Verificar keys con test simple
- [ ] Ejecutar test de parafraseo paralelo
- [ ] Confirmar que no hay errores 429
- [ ] Generar placeholders de prueba
- [ ] Integrar en master_orchestrator

---

**Última actualización:** 2026-01-20
**Estado:** ⏳ Pendiente agregar KEY_2 y KEY_3
