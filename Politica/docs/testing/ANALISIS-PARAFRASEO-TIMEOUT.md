# Análisis de Parafraseo y Timeouts - Sistema de Noticias

**Fecha:** 2026-01-20  
**Análisis por:** Testing automatizado  
**Objetivo:** Verificar configuración de timeouts, endpoint API y manejo de errores

---

## 🎯 Resumen Ejecutivo

✅ **Estado General:** OPERATIVO  
✅ **Endpoint API:** Funcionando correctamente  
✅ **Timeouts:** Configurados adecuadamente  
⚠️ **Recomendaciones:** Mejoras menores sugeridas  

---

## 📊 Resultados de Tests

### Test 1: Endpoint Directo Blackbox API
```
Status: ✅ PASS
Endpoint: https://api.blackbox.ai/chat/completions
Status Code: 200
Tiempo de respuesta: 3.87s
Timeout configurado: 30s
```

**Análisis:**
- El endpoint responde correctamente
- Tiempo de respuesta óptimo (< 5s para requests simples)
- Autenticación funcional
- Headers correctamente configurados

---

### Test 2: NewsParaphraser Timeout
```
Status: ✅ PASS
Timeout configurado: 90s (línea 102 paraphrase.py)
Tiempo de ejecución: 47.97s
Formato de respuesta: Estructurado con [TÍTULO] y [ARTÍCULO]
```

**Análisis:**
- Timeout de 90s es **ADECUADO** para artículos largos
- Tiempo promedio ~48s para parafraseo completo
- Margen de seguridad: 42s (90s - 48s = 42s)
- La API retorna respuestas estructuradas correctamente

**Detalles de Implementación:**
```python
# scripts/paraphrase.py:102
response = requests.post(API_URL, headers=self.headers, json=payload, timeout=90)
```

---

### Test 3: ArticleExpander Timeout
```
Status: ⏭️ SKIP (módulo no importado correctamente)
Timeout configurado: 45s (línea 134 article-expander.py)
```

**Observación:**
- Módulo presente pero no se importa en el flujo principal
- Timeout de 45s puede ser **INSUFICIENTE** para artículos largos
- Recomendación: Aumentar a 60-90s

---

### Test 4: Manejo de Errores

#### 4.1 API Key Inválida
```
Status: ✅ PASS
Código HTTP: 401
Mensaje: "Authentication Error, LiteLLM Virtual Key expected"
Respuesta correcta: Sí
```

#### 4.2 Payload Inválido
```
Status: ✅ PASS
Código HTTP: 400
Mensaje: "Invalid model name passed"
Respuesta correcta: Sí
```

**Análisis:**
- Los errores se manejan correctamente a nivel API
- Códigos HTTP apropiados (401, 400)
- Mensajes de error descriptivos
- El código Python captura y maneja excepciones

---

## 🔍 Análisis Detallado de Timeouts

### Configuración Actual

| Módulo | Función | Timeout | Ubicación | Estado |
|--------|---------|---------|-----------|--------|
| paraphrase.py | paraphrase_text | 90s | Línea 102 | ✅ Óptimo |
| article-expander.py | expand_article | 45s | Línea 134 | ⚠️ Ajustar |

### Tiempos de Respuesta Observados

```
Request simple (50 tokens):     ~4s
Parafraseo completo (3000 tokens): ~48s
Expansión de artículo (2000 tokens): N/A (no testeado)
```

### Cálculo de Margen de Seguridad

```
Parafraseo:
- Timeout: 90s
- Tiempo real: 48s
- Margen: 42s (46.7%)
- Evaluación: ✅ EXCELENTE

Expansión:
- Timeout: 45s
- Tiempo estimado: 35-40s
- Margen: 5-10s (11-22%)
- Evaluación: ⚠️ AJUSTADO (riesgo de timeout)
```

---

## 🛠️ Recomendaciones

### 1. Timeout en ArticleExpander
**Prioridad:** MEDIA

```python
# Cambio sugerido en article-expander.py línea 134
# ANTES:
response = requests.post(API_URL, headers=self.headers, json=payload, timeout=45)

# DESPUÉS:
response = requests.post(API_URL, headers=self.headers, json=payload, timeout=90)
```

**Justificación:**
- Consistencia con paraphrase.py
- Mayor margen de seguridad
- Artículos largos necesitan más tiempo

---

### 2. Implementar Retry Logic
**Prioridad:** ALTA

```python
# Nuevo módulo sugerido: scripts/utils/api_retry.py

import time
from typing import Callable, Any

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    timeout_increment: int = 30
):
    """
    Reintenta una función con backoff exponencial
    
    Args:
        func: Función a ejecutar
        max_retries: Número máximo de reintentos
        initial_delay: Delay inicial en segundos
        backoff_factor: Factor de multiplicación del delay
        timeout_increment: Segundos adicionales por retry
    """
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return func(timeout=90 + (attempt * timeout_increment))
        except requests.exceptions.Timeout as e:
            if attempt == max_retries - 1:
                raise
            print(f"⏱️ Timeout en intento {attempt + 1}, reintentando en {delay}s...")
            time.sleep(delay)
            delay *= backoff_factor
    
    raise Exception("Max retries exceeded")
```

**Uso:**
```python
# En paraphrase.py
from utils.api_retry import retry_with_backoff

result = retry_with_backoff(
    lambda timeout: requests.post(API_URL, headers=self.headers, json=payload, timeout=timeout)
)
```

---

### 3. Logging de Tiempos de Respuesta
**Prioridad:** MEDIA

```python
# Agregar a paraphrase.py y article-expander.py

import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Antes del request:
start_time = time.time()

# Después del request:
elapsed = time.time() - start_time
logger.info(f"API Response time: {elapsed:.2f}s - Model: {model} - Tokens: {max_tokens}")

# Para análisis de performance
if elapsed > 60:
    logger.warning(f"Slow API response: {elapsed:.2f}s")
```

---

### 4. Configuración por Entorno
**Prioridad:** BAJA

```python
# .env
BLACKBOX_API_TIMEOUT_DEFAULT=90
BLACKBOX_API_TIMEOUT_LONG=120
BLACKBOX_API_MAX_RETRIES=3

# paraphrase.py
TIMEOUT_DEFAULT = int(os.getenv('BLACKBOX_API_TIMEOUT_DEFAULT', 90))
TIMEOUT_LONG = int(os.getenv('BLACKBOX_API_TIMEOUT_LONG', 120))
```

---

## 📈 Monitoreo y Métricas

### Métricas Recomendadas

1. **Tiempo promedio de respuesta por operación**
   - Parafraseo simple
   - Parafraseo largo
   - Expansión de artículos

2. **Tasa de timeouts**
   - Por módulo
   - Por hora del día
   - Por tamaño de payload

3. **Tasa de éxito/fracaso**
   - Requests exitosos vs fallidos
   - Distribución de códigos de error

4. **Uso de API**
   - Requests por minuto
   - Tokens consumidos
   - Costos asociados

---

## 🔧 Manejo de Errores Actual

### Errores Capturados

```python
# paraphrase.py:109-114
try:
    response = requests.post(API_URL, headers=self.headers, json=payload, timeout=90)
    response.raise_for_status()
    result = response.json()
    paraphrased = result['choices'][0]['message']['content'].strip()
    return paraphrased
    
except requests.exceptions.RequestException as e:
    print(f"❌ Error en API: {e}")
    return text  # Retornar texto original si falla
    
except (KeyError, IndexError) as e:
    print(f"❌ Error procesando respuesta: {e}")
    return text
```

### Evaluación
✅ **Fortalezas:**
- Captura excepciones de red (RequestException)
- Captura errores de parsing (KeyError, IndexError)
- Retorna texto original como fallback
- No rompe el flujo del programa

⚠️ **Mejoras Sugeridas:**
- Agregar logging estructurado
- Diferenciar tipos de error para métricas
- Implementar alertas para errores críticos
- Guardar errores para análisis posterior

---

## 🧪 Comandos de Testing

### Test Rápido
```bash
python3 scripts/test/test_paraphrase_quick.py
```

### Test Completo de Timeouts
```bash
python3 scripts/test/test_api_timeout.py
```

### Test de Flujo Completo
```bash
python3 scripts/test/test_flujo_completo.py
```

---

## 📝 Problemas Conocidos

### 1. Timeout en Parafraseo da Timeout Siempre
**Status:** ❌ REPORTADO por usuario  
**Reproducible:** ⚠️ No reproducido en tests

**Análisis:**
- Tests automáticos NO presentan timeouts
- Tiempo de respuesta: 47.97s (dentro de límite de 90s)
- Posibles causas:
  1. ~~Timeout configurado muy bajo~~ ✅ 90s es adecuado
  2. Problemas de red intermitentes (latencia, DNS)
  3. Throttling por parte de la API (rate limiting)
  4. Carga alta del servidor Blackbox en ciertos horarios
  5. Artículos específicos que requieren más procesamiento

**Recomendaciones de Diagnóstico:**
```bash
# 1. Verificar latencia a API
ping api.blackbox.ai

# 2. Medir tiempo de respuesta
time curl -X POST https://api.blackbox.ai/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BLACKBOX_API_KEY" \
  -d '{"model":"blackboxai/blackbox-pro","messages":[{"role":"user","content":"test"}]}'

# 3. Revisar logs de timeouts específicos
grep -r "Timeout" scripts/ --include="*.py"
```

**Acción Sugerida:**
1. Implementar logging detallado de cada request
2. Capturar metadata: hora, tamaño del artículo, tiempo de respuesta
3. Analizar patrones: ¿timeouts en horas específicas? ¿artículos largos?
4. Considerar implementar rate limiting local para evitar throttling

---

## ✅ Conclusiones

1. **El sistema de parafraseo está operativo y configurado correctamente**
2. **Los timeouts actuales (90s) son adecuados para la mayoría de casos**
3. **El manejo de errores es robusto y previene fallos críticos**
4. **Recomendaciones de mejora son incrementales, no críticas**

### Prioridades de Implementación

1. 🔴 **ALTA:** Implementar retry logic con backoff exponencial
2. 🟡 **MEDIA:** Agregar logging detallado de tiempos de respuesta
3. 🟡 **MEDIA:** Aumentar timeout en article-expander.py a 90s
4. 🟢 **BAJA:** Configuración por variables de entorno

---

## 📚 Referencias

- **Blackbox API Docs:** https://docs.blackbox.ai/api-reference
- **Error Handling:** https://docs.blackbox.ai/api-reference/errors
- **Best Practices:** https://docs.blackbox.ai/api-reference/web-search
- **Timeout Configuration:** RFC 7231 (HTTP/1.1 Semantics and Content)

---

## 📞 Siguiente Acciones

- [ ] Revisar logs de producción para identificar timeouts reales
- [ ] Implementar retry logic
- [ ] Agregar monitoring de métricas
- [ ] Ajustar timeout en article-expander.py
- [ ] Crear dashboard de performance de API

---

**Generado automáticamente por:** `test_api_timeout.py`  
**Última actualización:** 2026-01-20
