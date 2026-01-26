# 🚀 Comandos Actualizados - Flujo Completo

## ✅ Problema de Imports Resuelto

Se corrigieron los imports en los scripts de API para usar rutas correctas.

---

## 🎯 Flujo Completo Automático

### **Opción 1: Script Bash Automatizado (RECOMENDADO)**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Flujo completo con configuración por defecto
# (5 noticias → 200 artículos → 10 sitios)
./flujo-completo.sh

# Flujo completo personalizado
# Sintaxis: ./flujo-completo.sh [noticias] [sitios]
./flujo-completo.sh 10 40
```

**¿Qué hace?**
1. ✅ Descarga noticias de NewsAPI
2. ✅ Parafrasea (40 variaciones cada una)
3. ✅ Genera imágenes con IA (Flux Schnell)
4. ✅ Genera sitios HTML con layouts

**Duración:** 15-25 minutos (5 noticias)

---

## 🔧 Flujo Manual Paso a Paso

### **PASO 1: Descargar Noticias**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# NewsAPI (recomendado)
python3 api/newsapi.py --size 5

# O usar otras APIs
python3 api/newsdata.py --size 5
python3 api/worldnews.py --size 5
python3 api/apitube.py --size 5
```

**Output:** `newsapi_YYYYMMDD_HHMM.json` (5 noticias)

---

### **PASO 2: Parafrasear Noticias**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Parafraseo completo (40 variaciones)
python3 -c "
import json
from paraphrase import NewsParaphraser
import glob

# Encontrar último archivo
patterns = ['newsapi_*.json', 'newsdata_*.json', 'worldnews_*.json', 'apitube_*.json']
files = []
for p in patterns:
    files.extend(glob.glob(p))
latest = sorted(files)[-1]

# Cargar y procesar
with open(latest, 'r', encoding='utf-8') as f:
    articles = json.load(f)

paraphraser = NewsParaphraser()
variations = paraphraser.process_articles(articles, variations_per_article=40)

# Guardar
with open('noticias_paraphrased.json', 'w', encoding='utf-8') as f:
    json.dump(variations, f, ensure_ascii=False, indent=2)

print(f'✅ {len(variations)} variaciones guardadas')
"
```

**Output:** `noticias_paraphrased.json` (200 artículos si usaste 5 noticias)

---

### **PASO 3: Generar Imágenes con IA**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Generar imágenes para todos los artículos
python3 generate-images-ai.py
```

**Output:** 
- Imágenes en `../images/news/article_*.jpg`
- Archivo actualizado: `noticias_final_YYYYMMDD.json`

---

### **PASO 4: Generar Sitios HTML**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Generar 10 sitios
python3 generate-sites.py --cantidad 10 --no-interactivo

# O más sitios
python3 generate-sites.py --cantidad 40 --no-interactivo
```

**Output:** `../sites/site1.html` hasta `site10.html`

---

## ⚡ Comandos Rápidos

### **Flujo Express (5→10)**

```bash
cd /home/sebastianvernis/news-prototype/scripts
./flujo-completo.sh 5 10
```

### **Flujo Producción (10→100)**

```bash
cd /home/sebastianvernis/news-prototype/scripts
./flujo-completo.sh 10 100
```

---

## 🔍 Verificar Resultados

```bash
# Ver noticias descargadas
cd /home/sebastianvernis/news-prototype/scripts
ls -lh newsapi_*.json

# Ver artículos parafraseados
cat noticias_paraphrased.json | jq length

# Ver imágenes generadas
ls -1 ../images/news/*.jpg | wc -l

# Ver sitios generados
ls -lh ../sites/*.html
```

---

## 🐛 Solución de Problemas

### **Error: ModuleNotFoundError: No module named 'utils'**
✅ **RESUELTO** - Se agregaron `__init__.py` y rutas correctas

### **Error: No se encontraron archivos de noticias**
```bash
# Descargar noticias primero
cd /home/sebastianvernis/news-prototype/scripts
python3 api/newsapi.py --size 5
```

### **Error: BLACKBOX_API_KEY no encontrada**
```bash
# Configurar en .env
nano /home/sebastianvernis/news-prototype/.env

# Agregar:
BLACKBOX_API_KEY=tu_key_aqui
NEWSAPI_KEY=tu_key_aqui
```

---

## 📊 Archivos Generados por Paso

| Paso | Archivo | Ubicación | Cantidad |
|------|---------|-----------|----------|
| 1. Descarga | `newsapi_*.json` | `scripts/` | 5 noticias |
| 2. Parafraseo | `noticias_paraphrased.json` | `scripts/` | 200 artículos |
| 3. Imágenes | `article_*.jpg` | `images/news/` | 200 imágenes |
| 4. Sitios | `site*.html` | `sites/` | 10 sitios |

---

## 🎯 Resumen del Flujo

```
📥 NewsAPI (5 noticias)
    ↓
✍️  Parafraseo (40 variaciones × 5 = 200 artículos)
    ↓
🎨 Generación de Imágenes (200 imágenes con Flux Schnell)
    ↓
🏗️  Generación de Sitios (10 sitios HTML con layouts únicos)
    ↓
✅ 10 sitios completos con 200 artículos y 200 imágenes
```

---

## 💡 Notas Importantes

### **Lo que SÍ hace automáticamente:**
- ✅ Genera nombres de sitios con IA
- ✅ Verifica disponibilidad de dominios
- ✅ Descarga y enriquece noticias
- ✅ Parafrasea con múltiples estilos
- ✅ Genera imágenes con IA (Flux Schnell)
- ✅ Crea layouts HTML únicos
- ✅ Aplica paletas de colores
- ✅ Optimiza dimensiones de imágenes

### **Lo que NO hace:**
- ❌ No genera logos visuales (solo metadatos)
- ❌ No crea favicons
- ❌ No hace deploy automático

---

## 🚀 Comando Único Recomendado

```bash
cd /home/sebastianvernis/news-prototype/scripts && ./flujo-completo.sh
```

**Eso es todo.** 15-20 minutos después tendrás 10 sitios HTML completos.

---

*Última actualización: 8 de enero de 2026*
*Flujo verificado y funcional ✅*
