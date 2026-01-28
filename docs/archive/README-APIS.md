# 📰 Guía Completa de APIs de Noticias

Sistema integrado con **4 APIs de noticias** para descarga automatizada de artículos de política en México.

## 🎯 APIs Disponibles

| API | URL | Plan Gratuito | Límite | Ventaja |
|-----|-----|---------------|--------|---------|
| **NewsAPI.org** | [newsapi.org](https://newsapi.org) | ✅ Sí | 100 req/día | Popular, bien documentada |
| **APITube.io** | [apitube.io](https://apitube.io) | ✅ Sí | 100 req/día | Body completo incluido |
| **Newsdata.io** | [newsdata.io](https://newsdata.io) | ✅ Sí | 200 créditos/día | Content completo incluido |
| **WorldNewsAPI** | [worldnewsapi.com](https://worldnewsapi.com) | ✅ Demo | 100 req/día | Búsqueda avanzada |

---

## 🚀 Inicio Rápido

### 1. Registrarse en las APIs

Obtén tus API keys registrándote en los siguientes enlaces:

```bash
# NewsAPI.org
https://newsapi.org/register

# APITube.io
https://apitube.io/register

# Newsdata.io
https://newsdata.io/register

# WorldNewsAPI
https://worldnewsapi.com/register
```

### 2. Configurar API Keys

Las API keys ya están configuradas en `.env`:

```env
NEWSAPI_KEY="3fe1ad82a95f462c802ebbacd88ce4db"
APITUBE_KEY="api_live_D1N0OMX931jbN50XqMSMdApafgJZ4RIHoOupbxZSa8NTkHRsqMXK22"
NEWSDATA_KEY="pub_34a911c383bb4a849b45816304852164"
WORLDNEWS_KEY="02384c82f02b48bb8c8e0c6fd51ad7e2"
```

### 3. Ejecutar

#### Opción A: Usar todas las APIs (recomendado)

```bash
# Modo prueba (5 artículos por API)
bash run_all_apis.sh test

# Modo normal (20 artículos por API)
bash run_all_apis.sh
```

#### Opción B: Usar una API específica

```bash
# Activar entorno virtual
source venv/bin/activate

# NewsAPI.org
python3 newsapi.py --size 20

# APITube.io
python3 apitube.py --size 20

# Newsdata.io
python3 newsdata.py --size 10  # Máx 10 en plan gratuito

# WorldNewsAPI
python3 worldnews.py --size 20
```

#### Opción C: Integrar con el sistema completo

```bash
# Usar NewsAPI.org (default)
python3 main.py --api newsapi --articles 5 --variations 40

# Usar APITube.io
python3 main.py --api apitube --articles 5 --variations 40

# Usar Newsdata.io
python3 main.py --api newsdata --articles 5 --variations 40

# Usar WorldNewsAPI
python3 main.py --api worldnews --articles 5 --variations 40

# Modo prueba
python3 main.py --api newsapi --test
```

---

## 📁 Estructura de Archivos

```
news-prototype/
├── utils.py                 # Funciones compartidas
├── newsapi.py              # NewsAPI.org scraper
├── apitube.py              # APITube.io scraper
├── newsdata.py             # Newsdata.io scraper
├── worldnews.py            # WorldNewsAPI scraper
├── main.py                 # Sistema integrado (con parafraseado + imágenes)
├── run_all_apis.sh         # Ejecutar todas las APIs
└── .env                    # API keys
```

---

## 🔧 Scripts Individuales

### NewsAPI.org (`newsapi.py`)

```bash
python3 newsapi.py --query "política México" --language es --size 20
```

**Parámetros:**
- `--query`: Términos de búsqueda (default: "política México")
- `--language`: Código de idioma (default: es)
- `--size`: Número de artículos (default: 20)
- `--no-enrich`: No extraer texto completo

**Salida:**
- `newsapi_YYYYMMDD_HHMM.json`
- `newsapi_YYYYMMDD_HHMM.csv`

### APITube.io (`apitube.py`)

```bash
python3 apitube.py --country mx --category politics --size 20
```

**Parámetros:**
- `--country`: Código de país (default: mx)
- `--category`: Categoría (default: politics)
- `--language`: Código de idioma (default: es)
- `--size`: Número de artículos (default: 20)

**Ventaja:** Incluye body completo sin scraping adicional.

**Salida:**
- `apitube_YYYYMMDD_HHMM.json`
- `apitube_YYYYMMDD_HHMM.csv`

### Newsdata.io (`newsdata.py`)

```bash
python3 newsdata.py --query "política México" --country mx --size 10
```

**Parámetros:**
- `--query`: Términos de búsqueda (default: "política México")
- `--country`: Código de país (default: mx)
- `--language`: Código de idioma (default: es)
- `--category`: Categoría (default: politics)
- `--size`: Número de artículos (default: 10, máx 10 en plan gratuito)

**Ventaja:** Incluye content completo sin scraping adicional.

**Salida:**
- `newsdata_YYYYMMDD_HHMM.json`
- `newsdata_YYYYMMDD_HHMM.csv`

### WorldNewsAPI (`worldnews.py`)

```bash
python3 worldnews.py --query "política México" --country mx --size 20
```

**Parámetros:**
- `--query`: Términos de búsqueda (default: "política México")
- `--country`: Código de país (default: mx)
- `--language`: Código de idioma (default: es)
- `--size`: Número de artículos (default: 20)
- `--from-date`: Fecha mínima YYYY-MM-DD (ej: 2024-01-01)

**Ventaja:** Búsqueda avanzada con filtros detallados.

**Salida:**
- `worldnews_YYYYMMDD_HHMM.json`
- `worldnews_YYYYMMDD_HHMM.csv`

---

## 📊 Normalización de Datos

Todos los scripts normalizan los artículos a una estructura común:

```json
{
  "source": "newsapi|apitube|newsdata|worldnews",
  "title": "Título del artículo",
  "description": "Descripción breve",
  "url": "https://...",
  "image_url": "https://...",
  "published_at": "2024-01-07T10:00:00Z",
  "content": "Contenido parcial",
  "full_text": "Texto completo del artículo",
  "author": "Nombre del autor",
  "source_name": "Nombre de la fuente"
}
```

---

## 🔄 Flujo Completo con Parafraseado + Imágenes

Para usar el sistema completo (descarga + parafraseado + generación de imágenes):

```bash
# NewsAPI.org
python3 main.py --api newsapi --articles 5 --variations 40

# APITube.io
python3 main.py --api apitube --articles 5 --variations 40

# Newsdata.io
python3 main.py --api newsdata --articles 5 --variations 40

# WorldNewsAPI
python3 main.py --api worldnews --articles 5 --variations 40

# Modo prueba (2 artículos, 5 variaciones)
python3 main.py --api newsapi --test
```

**Salidas:**
1. `noticias_{api}_{timestamp}.json` - Artículos originales
2. `noticias_paraphrased_{timestamp}.json` - Variaciones parafraseadas
3. `noticias_final_{timestamp}.json` - Con imágenes generadas
4. `images/news/article_*.jpg` - Imágenes generadas con IA

---

## 🛠️ Utilidades (`utils.py`)

Funciones compartidas entre todos los scrapers:

### `get_full_text(url)`

Extrae el texto completo de un artículo web usando BeautifulSoup.

```python
from utils import get_full_text

full_text = get_full_text('https://example.com/article')
```

### `save_articles(articles, prefix)`

Guarda artículos en JSON y CSV.

```python
from utils import save_articles

json_file, csv_file = save_articles(articles, 'newsapi')
```

### `normalize_article(article, source)`

Normaliza estructura de artículo según la fuente.

```python
from utils import normalize_article

normalized = normalize_article(raw_article, 'newsapi')
```

### `enrich_with_full_text(articles, source)`

Enriquece artículos con texto completo extraído.

```python
from utils import enrich_with_full_text

enriched = enrich_with_full_text(articles, 'newsapi')
```

---

## 📈 Comparación de APIs

| Característica | NewsAPI | APITube | Newsdata | WorldNews |
|----------------|---------|---------|----------|-----------|
| **Body completo** | ❌ No | ✅ Sí | ✅ Sí | ✅ Sí |
| **Scraping requerido** | ✅ Sí | ❌ No | ❌ No | ❌ No |
| **Límite gratuito** | 100/día | 100/día | 200/día | 100/día |
| **Max resultados** | 100 | 50 | 10 | 50 |
| **Filtro país** | ❌ No | ✅ Sí | ✅ Sí | ✅ Sí |
| **Filtro categoría** | ❌ No | ✅ Sí | ✅ Sí | ❌ No |
| **Búsqueda avanzada** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

**Recomendación:**
- **APITube.io**: Mejor para scraping sin complicaciones (body incluido)
- **Newsdata.io**: Mejor relación límite/calidad (200 créditos/día)
- **WorldNewsAPI**: Mejor para búsquedas avanzadas
- **NewsAPI.org**: Más popular y estable

---

## 🐛 Solución de Problemas

### Error: "API key no encontrada"

Verifica que `.env` contiene la API key correcta:

```bash
cat .env | grep NEWSAPI_KEY
```

### Error: "Rate limit exceeded"

Has superado el límite de requests diarios. Espera 24 horas o usa otra API.

### Error: "No articles found"

Ajusta los parámetros de búsqueda:

```bash
# Ampliar búsqueda
python3 newsapi.py --query "México" --size 50

# Cambiar categoría
python3 apitube.py --category business
```

### Error: "Connection timeout"

Aumenta el timeout en el código:

```python
response = requests.get(BASE_URL, params=params, timeout=60)
```

---

## 📝 Ejemplos de Uso

### Descarga masiva de todas las APIs

```bash
bash run_all_apis.sh
```

### Descarga + Parafraseado + Imágenes

```bash
# NewsAPI
python3 main.py --api newsapi --articles 5 --variations 40

# Resultado: 5 artículos × 40 variaciones = 200 artículos con imágenes
```

### Comparar resultados de múltiples APIs

```bash
# Descargar de todas
python3 newsapi.py --size 10
python3 apitube.py --size 10
python3 newsdata.py --size 10
python3 worldnews.py --size 10

# Comparar archivos JSON generados
ls -lth *.json | head -4
```

---

## 🔐 Seguridad

- **Nunca** compartas tu archivo `.env`
- Las API keys son personales e intransferibles
- Agrega `.env` a `.gitignore`
- Rota las API keys periódicamente

---

## 📚 Enlaces de Documentación

- [NewsAPI.org Docs](https://newsapi.org/docs)
- [APITube.io Docs](https://apitube.io/docs)
- [Newsdata.io Docs](https://newsdata.io/documentation)
- [WorldNewsAPI Docs](https://worldnewsapi.com/docs)

---

## 🎉 Próximos Pasos

1. ✅ Descarga de noticias con múltiples APIs
2. ✅ Parafraseado con IA (Blackbox API)
3. ✅ Generación de imágenes con IA (Flux Schnell)
4. 🚧 Publicación automática en redes sociales
5. 🚧 Base de datos para almacenamiento persistente
6. 🚧 Dashboard web para visualización

---

**Desarrollado con ❤️ usando Python + Multi-API Integration**
