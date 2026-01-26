# 🚀 Comandos para Flujo Completo - News Prototype

## 📋 Guía de Ejecución Paso a Paso

---

## 🔄 Flujo Completo Automatizado

### **Opción 1: Flujo Completo con Un Comando**

```bash
# Navegar al directorio de scripts
cd /home/sebastianvernis/news-prototype/scripts

# Ejecutar flujo completo (descarga + parafraseo + imágenes + sitios)
python3 main.py --api newsapi --articles 5
```

**¿Qué hace?**
1. ✅ Descarga 5 noticias de NewsAPI
2. ✅ Parafrasea automáticamente (40 variaciones cada una = 200 noticias)
3. ✅ Genera imágenes con IA (200 imágenes)
4. ✅ Listo para generar sitios

**Duración estimada:** 10-20 minutos

---

## 🎯 Flujo Paso a Paso (Control Manual)

### **PASO 1: Descargar Noticias**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Opción A: NewsAPI (recomendado)
python3 main.py --api newsapi --articles 5

# Opción B: Newsdata.io
python3 main.py --api newsdata --articles 5

# Opción C: WorldNewsAPI
python3 main.py --api worldnews --articles 5
```

**Output esperado:**
- Archivo: `data/noticias_newsapi_[fecha].json`
- 5 noticias originales con contenido completo

---

### **PASO 2: Parafrasear Noticias (40 variaciones)**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Parafraseo con Blackbox AI
python3 paraphrase.py
```

**¿Qué hace?**
- Lee el último archivo de noticias
- Genera 40 variaciones por cada noticia
- Total: 5 × 40 = 200 noticias únicas

**Output esperado:**
- Archivo: `data/noticias_paraphrased_[fecha].json`
- 200 noticias únicas

**Duración estimada:** 5-10 minutos

---

### **PASO 3: Generar Imágenes con IA**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Generar imágenes con Flux Schnell
python3 generate-images-ai.py
```

**¿Qué hace?**
- Lee noticias parafraseadas
- Genera 1 imagen por cada variación (200 imágenes)
- Modelo: Flux Schnell 1024×1024 PNG

**Output esperado:**
- Imágenes en: `images/news/article_[id]_[var].jpg`
- Archivo actualizado: `data/noticias_final_[fecha].json`

**Duración estimada:** 5-10 minutos (depende de API)

---

### **PASO 4: Generar Sitios HTML**

#### **Modo Interactivo (Recomendado para Primera Vez)**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Ejecutar generador interactivo
python3 generate-sites.py
```

**Preguntas que hará:**
1. ¿Cuántos sitios generar? (1-100)
2. ¿Verificar disponibilidad de dominios? (s/n)
3. ¿Usar metadatos existentes o generar nuevos? (1/2)
4. Confirmación final

---

#### **Modo No-Interactivo (Rápido)**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Generar 10 sitios sin preguntas
python3 generate-sites.py --cantidad 10 --no-interactivo

# Generar 40 sitios con verificación de dominios
python3 generate-sites.py --cantidad 40 --verificar-dominios --no-interactivo

# Generar 5 sitios usando metadatos específicos
python3 generate-sites.py --cantidad 5 \
  --metadata-file ../data/sites_metadata/sites_metadata_20260108.json \
  --no-interactivo
```

**Output esperado:**
- Sitios HTML en: `sites/site1.html`, `site2.html`, etc.
- Metadatos en: `data/sites_metadata/sites_metadata_[fecha].json`

**Duración estimada:** 20-40 segundos

---

## ⚡ Comandos Rápidos

### **Flujo Completo Express (5 noticias → 10 sitios)**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# 1. Descargar, parafrasear y generar imágenes (todo incluido)
python3 main.py --api newsapi --articles 5

# 2. Generar 10 sitios
python3 generate-sites.py --cantidad 10 --no-interactivo
```

**Tiempo total:** 15-25 minutos

---

### **Flujo Producción (10 noticias → 100 sitios)**

```bash
cd /home/sebastianvernis/news-prototype/scripts

# 1. Descargar 10 noticias (400 variaciones)
python3 main.py --api newsapi --articles 10

# 2. Generar 100 sitios
python3 generate-sites.py --cantidad 100 --no-interactivo
```

**Tiempo total:** 30-45 minutos

---

## 🔧 Comandos Útiles

### **Ver Noticias Disponibles**

```bash
cd /home/sebastianvernis/news-prototype/data

# Ver archivos de noticias
ls -lh noticias_*.json

# Ver última versión final
cat noticias_final_*.json | jq length
# Output: 200 (si tienes 5 noticias × 40 variaciones)
```

---

### **Ver Imágenes Generadas**

```bash
cd /home/sebastianvernis/news-prototype/images/news

# Contar imágenes
ls -1 *.jpg | wc -l

# Ver peso total
du -sh .
```

---

### **Ver Sitios Generados**

```bash
cd /home/sebastianvernis/news-prototype/sites

# Listar sitios
ls -lh *.html

# Abrir sitio específico en navegador (ejemplo para Linux)
xdg-open site1.html

# O simplemente navegar a:
# file:///home/sebastianvernis/news-prototype/sites/site1.html
```

---

### **Ver Metadatos de Sitios**

```bash
cd /home/sebastianvernis/news-prototype/data/sites_metadata

# Ver metadatos generados
cat sites_metadata_*.json | jq '.[0]'
# Muestra el primer sitio con toda su configuración
```

---

### **Limpiar Todo y Empezar de Cero**

```bash
cd /home/sebastianvernis/news-prototype

# Eliminar sitios
rm -f sites/*.html

# Eliminar imágenes antiguas (CUIDADO)
# rm -rf images/news/*.jpg

# Eliminar noticias antiguas (CUIDADO)
# rm -f data/noticias_*.json

# Eliminar metadatos antiguos (CUIDADO)
# rm -f data/sites_metadata/sites_metadata_*.json

echo "✅ Limpieza completada"
```

---

## 📊 Parámetros y Opciones

### **main.py (Descarga de Noticias)**

```bash
python3 main.py [opciones]

Opciones:
  --api [newsapi|newsdata|worldnews]  # API a utilizar (default: newsapi)
  --articles N                        # Número de noticias (default: 5)
  --country CÓDIGO                    # País (default: mx)
  --language CÓDIGO                   # Idioma (default: es)
  --category CATEGORÍA                # Categoría específica
```

**Ejemplos:**
```bash
# 10 noticias de tecnología
python3 main.py --api newsapi --articles 10 --category technology

# Noticias de Argentina
python3 main.py --api newsapi --articles 5 --country ar

# Noticias en inglés de USA
python3 main.py --api newsapi --articles 5 --country us --language en
```

---

### **generate-sites.py (Generación de Sitios)**

```bash
python3 generate-sites.py [opciones]

Opciones:
  --cantidad N                # Número de sitios (1-100)
  --no-interactivo           # Modo sin preguntas
  --verificar-dominios       # Verificar disponibilidad de dominios
  --metadata-file RUTA       # Usar metadatos existentes
  --max-templates N          # Máximo de templates CSS (default: 40)
```

**Ejemplos:**
```bash
# 20 sitios rápido
python3 generate-sites.py --cantidad 20 --no-interactivo

# 50 sitios con dominios verificados
python3 generate-sites.py --cantidad 50 --verificar-dominios --no-interactivo

# Usar metadatos específicos
python3 generate-sites.py --cantidad 10 \
  --metadata-file ../data/sites_metadata/sites_metadata_20260108_162552.json
```

---

### **paraphrase.py (Parafraseo Manual)**

```bash
python3 paraphrase.py [opciones]

Opciones:
  --input ARCHIVO           # Archivo de entrada (default: último noticias_*.json)
  --output ARCHIVO          # Archivo de salida (default: auto)
  --variations N            # Variaciones por noticia (default: 40)
```

**Ejemplo:**
```bash
# 20 variaciones por noticia
python3 paraphrase.py --variations 20
```

---

### **generate-images-ai.py (Imágenes Manual)**

```bash
python3 generate-images-ai.py [opciones]

Opciones:
  --input ARCHIVO           # Archivo con noticias parafraseadas
  --output-dir DIRECTORIO   # Directorio para imágenes
  --model MODELO            # Modelo de IA (default: flux-schnell)
```

---

## 🎨 Variaciones de Configuración

### **Generar Sitios con Diferentes Estilos**

El generador usa configuraciones aleatorias, pero puedes regenerar para obtener diferentes combinaciones:

```bash
cd /home/sebastianvernis/news-prototype/scripts

# Generar 10 sitios (iteración 1)
python3 generate-sites.py --cantidad 10 --no-interactivo

# Ver resultados en sites/

# Eliminar y regenerar con nuevos estilos
rm -f ../sites/*.html
python3 generate-sites.py --cantidad 10 --no-interactivo

# Cada ejecución genera combinaciones diferentes de:
# - 21 tipos de layouts
# - 12 estilos de header
# - 12 estilos de navegación
# - 15 layouts destacados
# - 6 paletas de colores
```

---

## 📈 Checklist de Ejecución

### **Primera Vez (Setup Completo)**

```bash
# 1. Verificar que estás en el directorio correcto
cd /home/sebastianvernis/news-prototype

# 2. Verificar estructura de directorios
ls -la data/ images/ scripts/ sites/ templates/

# 3. Ejecutar flujo completo
cd scripts
python3 main.py --api newsapi --articles 5

# 4. Generar sitios
python3 generate-sites.py --cantidad 10 --no-interactivo

# 5. Verificar resultados
ls -lh ../sites/*.html

# 6. Abrir un sitio en navegador
xdg-open ../sites/site1.html
```

---

### **Ejecución Rápida (Ya Configurado)**

```bash
# Desde cualquier lugar, ir al proyecto
cd /home/sebastianvernis/news-prototype/scripts

# Flujo completo en 2 comandos
python3 main.py --api newsapi --articles 5
python3 generate-sites.py --cantidad 10 --no-interactivo

# Listo en 15-20 minutos
```

---

## 🐛 Troubleshooting

### **Error: No se encuentran noticias**

```bash
# Verificar archivo de noticias existe
ls -lh /home/sebastianvernis/news-prototype/data/noticias_final_*.json

# Si no existe, ejecutar:
cd /home/sebastianvernis/news-prototype/scripts
python3 main.py --api newsapi --articles 5
```

---

### **Error: Faltan imágenes**

```bash
# Verificar imágenes
ls /home/sebastianvernis/news-prototype/images/news/*.jpg | wc -l

# Si faltan, regenerar:
cd /home/sebastianvernis/news-prototype/scripts
python3 generate-images-ai.py
```

---

### **Error: API Key no configurada**

```bash
# Editar archivo .env
nano /home/sebastianvernis/news-prototype/.env

# Agregar keys:
NEWSAPI_KEY=tu_key_aqui
BLACKBOX_API_KEY=tu_key_aqui
```

---

## 📚 Documentación Adicional

- **Flujo completo:** `PRESENTACION-FLUJO.md`
- **Optimización de imágenes:** `OPTIMIZACION-IMAGENES.md`
- **README principal:** `README.md`

---

## 🎯 Resumen de Comandos Clave

```bash
# ============================================
# FLUJO COMPLETO RÁPIDO (LO MÁS USADO)
# ============================================

cd /home/sebastianvernis/news-prototype/scripts

# 1. Descargar + Parafrasear + Generar Imágenes
python3 main.py --api newsapi --articles 5

# 2. Generar sitios
python3 generate-sites.py --cantidad 10 --no-interactivo

# 3. Ver resultados
ls -lh ../sites/*.html

# ============================================
# FIN - Sitios listos en ~/news-prototype/sites/
# ============================================
```

---

*Última actualización: 8 de enero de 2026*
*Sistema verificado y funcional ✅*
