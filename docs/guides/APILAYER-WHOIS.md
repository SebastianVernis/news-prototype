# 🔍 Integración APILayer WHOIS

## 📋 Resumen

El sistema ahora soporta **dos métodos** para verificación de dominios:

1. **whois local** - Comando del sistema (original)
2. **APILayer WHOIS API** - Servicio en la nube (nuevo)

## 🎯 ¿Por qué APILayer?

### Ventajas sobre whois local:
- ✅ **No requiere instalación** de whois en el sistema
- ✅ **Respuestas estructuradas** en JSON (más confiables)
- ✅ **Funciona en cualquier OS** (Windows, Linux, macOS)
- ✅ **Rate limiting integrado** por el servicio
- ✅ **Datos consistentes** de múltiples TLDs (.com, .net, .org, etc.)
- ✅ **Compatible con whois local** (mismo API)

### Free Plan:
- 100 requests/mes gratuitas
- Suficiente para pruebas y desarrollo
- No requiere tarjeta de crédito

## 🔑 Configuración

### 1. Obtener API Key

1. Regístrate en [APILayer](https://apilayer.com/)
2. Suscríbete al [WHOIS API](https://apilayer.com/marketplace/whois-api)
3. Copia tu API key del dashboard

### 2. Configurar en .env

Abre el archivo `.env` en la raíz del proyecto y agrega:

```bash
APILAYER_API_KEY="tu_api_key_aqui"
```

**Ejemplo:**
```bash
NEWSAPI_KEY="3fe1ad82a95f462c802ebbacd88ce4db"
BLACKBOX_API_KEY="sk-Pqln-11XRgKTb3PxUxKUfA"
APILAYER_API_KEY="AbC123xYz456..."
```

### 3. Verificar instalación

```bash
# Test completo de integración
python core/scripts/test/test_apilayer_whois.py

# Test rápido con script dedicado
python core/scripts/domain_verifier_apilayer.py
```

## 📚 Uso

### CLI - Master Orchestrator

```bash
# Con APILayer WHOIS API (recomendado)
python core/scripts/master_orchestrator.py --verificar-dominios --api-whois

# Con whois local (método original)
python core/scripts/master_orchestrator.py --verificar-dominios

# Sin verificación (más rápido)
python core/scripts/master_orchestrator.py
```

### Python - Código

```python
from domain_verifier import DomainVerifier

# Usar APILayer API
verifier = DomainVerifier(usar_api=True)

# Usar whois local
verifier = DomainVerifier(usar_api=False)

# Verificar dominio
resultado = verifier.verificar_dominio("ejemplo.com")

print(resultado)
# {
#   'dominio': 'ejemplo.com',
#   'estado': 'registrado' | 'disponible' | 'error',
#   'disponible': True/False,
#   'registrado': True/False,
#   'info_adicional': {...},
#   'metodo': 'api' | 'local'
# }
```

### Verificación por lotes

```python
verifier = DomainVerifier(usar_api=True)

dominios = [
    "google.com",
    "ejemplo-no-existe-123.com",
    "microsoft.com"
]

resultados = verifier.verificar_dominios_batch(dominios)

for r in resultados:
    print(f"{r['dominio']}: {r['estado']}")
```

## 🔄 Compatibilidad

Los dos métodos son **100% compatibles**:

```python
# Mismo código, diferentes backends
verifier_api = DomainVerifier(usar_api=True)
verifier_local = DomainVerifier(usar_api=False)

# Ambos retornan la misma estructura
resultado_api = verifier_api.verificar_dominio("google.com")
resultado_local = verifier_local.verificar_dominio("google.com")

# Ambos tienen:
# - resultado['dominio']
# - resultado['estado']
# - resultado['disponible']
# - resultado['registrado']
# - resultado['info_adicional']
```

**Diferencia clave:** Campo `metodo`
- APILayer: `'metodo': 'api'`
- Local: `'metodo': 'local'`

## 📊 Comparación de métodos

| Característica | whois local | APILayer API |
|----------------|-------------|--------------|
| **Instalación** | Requiere `whois` | Solo API key |
| **Plataformas** | Linux/macOS | Todas |
| **Rate Limit** | Manual | Automático |
| **Formato** | Texto plano | JSON |
| **Parsing** | Regex | Estructurado |
| **Costo** | Gratis | 100 req/mes gratis |
| **Confiabilidad** | Variable | Alta |
| **Setup** | `apt install whois` | Copiar API key |

## 🚀 Recomendaciones

### Para desarrollo:
✅ **APILayer API** - Más consistente y fácil de debuggear

### Para producción:
- **APILayer API** si:
  - Generas < 100 sitios/mes (free plan)
  - Necesitas máxima compatibilidad
  - Trabajas en Windows

- **whois local** si:
  - Generas > 100 sitios/mes
  - Tienes servidor Linux/macOS
  - Prefieres no depender de servicios externos

### Modo híbrido (fallback):
```python
try:
    verifier = DomainVerifier(usar_api=True)
    resultado = verifier.verificar_dominio(dominio)
except Exception:
    # Fallback a whois local
    verifier = DomainVerifier(usar_api=False)
    resultado = verifier.verificar_dominio(dominio)
```

## 🧪 Testing

### Test completo
```bash
python core/scripts/test/test_apilayer_whois.py
```

**Output esperado:**
```
🧪 TEST DE INTEGRACIÓN: APILayer WHOIS
======================================================================

🔍 Test 1: Verificar API key en .env
✅ API key encontrada: AbC123xYz4...

🖥️ Test 2: Verificar con whois local
✅ whois local disponible
✅ Verificación exitosa - Estado: registrado

🌐 Test 3: Verificar con APILayer WHOIS API
   Probando: google.com
   ✅ Estado: registrado
   📊 Disponible: False
   🔧 Método: api

🔄 Test 4: Compatibilidad entre métodos
   ✅ Ambos métodos funcionan
   ✅ Resultados coinciden

📊 RESUMEN DE TESTS
✅ api_key: PASS
✅ whois_local: PASS
✅ whois_api: PASS
✅ compatibilidad: PASS

📈 Tasa de éxito: 4/4 (100%)
🎉 ¡Todos los tests pasaron!
```

### Test específico de API
```bash
python core/scripts/domain_verifier_apilayer.py
```

### Test de domain_verifier unificado
```bash
# Con API key configurada → usa API
python core/scripts/domain_verifier.py

# Sin API key → usa whois local
unset APILAYER_API_KEY
python core/scripts/domain_verifier.py
```

## 📖 Referencia de API

### APILayer WHOIS Endpoint

**URL:** `https://api.apilayer.com/whois/query?domain={domain}`

**Headers:**
```json
{
  "apikey": "tu_api_key_aqui"
}
```

**Response:**
```json
{
  "domain_name": "example.com",
  "registrar": "Example Registrar Inc.",
  "creation_date": "1995-08-13",
  "expiration_date": "2025-08-12",
  "name_servers": ["ns1.example.com", "ns2.example.com"],
  "status": ["clientTransferProhibited"],
  "emails": ["admin@example.com"],
  "dnssec": "unsigned",
  "registrant_name": "Example Organization",
  "registrant_organization": "Example Org",
  "registrant_country": "US"
}
```

**Error response:**
```json
{
  "error": "Domain not found"
}
```

## ⚠️ Límites y consideraciones

### Free Plan (100 req/mes):
- **Suficiente para:** ~3 sitios/día con verificación
- **No suficiente para:** Verificación masiva diaria

### Paid Plans:
- **Starter:** $9.99/mes - 5,000 requests
- **Pro:** $49.99/mes - 50,000 requests
- **Ultra:** $149.99/mes - 500,000 requests

### Rate Limiting:
- APILayer: 1 req/segundo (free), más en planes pagos
- whois local: Manual (configurado a 1-2 seg entre requests)

## 🐛 Troubleshooting

### Error: "API key inválida"
```bash
# Verificar que la API key esté en .env
cat .env | grep APILAYER

# Verificar que esté cargada
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('APILAYER_API_KEY'))"
```

### Error: "Rate limit excedido"
- Espera al siguiente mes (free plan)
- O cambia a whois local temporalmente
- O suscríbete a plan pago

### API key no se carga
```bash
# Asegúrate de tener python-dotenv instalado
pip install python-dotenv

# Verifica que .env esté en la raíz del proyecto
ls -la .env
```

### Ambos métodos fallan
```bash
# Verificar conexión a internet
ping -c 3 api.apilayer.com

# Verificar whois local
which whois

# Ver logs detallados
python core/scripts/domain_verifier.py -vv
```

## 📝 Archivos involucrados

```
core/scripts/
├── domain_verifier.py              # Verificador unificado (soporta ambos)
├── domain_verifier_apilayer.py     # Solo API (standalone)
├── master_orchestrator.py          # CLI con --api-whois flag
└── test/
    └── test_apilayer_whois.py      # Tests de integración

.env                                 # API keys (no commitear)
docs/
└── APILAYER-WHOIS.md               # Esta documentación
```

## 🔗 Enlaces útiles

- **APILayer Dashboard:** https://apilayer.com/account
- **WHOIS API Docs:** https://apilayer.com/marketplace/whois-api#documentation
- **Pricing:** https://apilayer.com/marketplace/whois-api#pricing
- **Support:** https://apilayer.com/support

## 🎓 Ejemplos de uso

### Ejemplo 1: Verificar un dominio específico
```bash
python -c "from scripts.domain_verifier import DomainVerifier; \
v = DomainVerifier(usar_api=True); \
r = v.verificar_dominio('google.com'); \
print(f\"Estado: {r['estado']}, Registrado: {r['registrado']}\")"
```

### Ejemplo 2: Generar sitio con verificación API
```bash
python core/scripts/master_orchestrator.py \
  --verificar-dominios \
  --api-whois \
  --output-dir ./sitios_verificados
```

### Ejemplo 3: Script personalizado
```python
#!/usr/bin/env python3
from scripts.domain_verifier import DomainVerifier

def verificar_lista_dominios(archivo):
    with open(archivo) as f:
        dominios = [line.strip() for line in f if line.strip()]
    
    verifier = DomainVerifier(usar_api=True)
    
    disponibles = []
    for dominio in dominios:
        resultado = verifier.verificar_dominio(dominio)
        if resultado.get('disponible'):
            disponibles.append(dominio)
            print(f"✅ {dominio} - DISPONIBLE")
        else:
            print(f"❌ {dominio} - {resultado['estado']}")
    
    return disponibles

# Uso
dominios_disponibles = verificar_lista_dominios('dominios.txt')
print(f"\n{len(dominios_disponibles)} dominios disponibles")
```

---

**Última actualización:** 2026-01-18  
**Versión:** 1.0  
**Autor:** Sistema automatizado de generación de sitios
