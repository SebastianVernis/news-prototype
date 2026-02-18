# 🚀 Inicio Rápido - 5 Minutos

## ⚡ Lo Más Rápido

```bash
# 1. Activar entorno
source venv/bin/activate

# 2. Ejecutar flujo completo de prueba (2 artículos, 5 variaciones)
python3 core/main.py --api newsapi --test

# Resultado: 10 artículos con imágenes en ~3 minutos
```

---

## 📋 Opciones Comunes

### Opción 1: Descarga Simple (sin parafraseado ni imágenes)

```bash
# NewsAPI - 20 artículos
python3 core/scripts/api/newsapi.py --size 20

# WorldNews - 20 artículos
python3 worldnews.py --size 20

# Todas las APIs - modo test
bash run_all_apis.sh test
```

**Salida:** Archivos JSON y CSV con artículos descargados

### Opción 2: Flujo Completo (descarga + parafraseado + imágenes)

```bash
# Modo test: 2 artículos, 5 variaciones = 10 posts
python3 core/main.py --api newsapi --test

# Modo normal: 5 artículos, 40 variaciones = 200 posts
python3 core/main.py --api newsapi --articles 5 --variations 40
```

**Salida:**
- Artículos originales JSON
- Variaciones parafraseadas JSON
- Imágenes en `images/news/`
- Resultado final JSON con todo

### Opción 3: Todas las APIs Simultáneas

```bash
# Ejecuta todas las APIs disponibles
bash run_all_apis.sh
```

**Salida:** Artículos de cada API (NewsAPI, Newsdata, WorldNews)

---

## 🎯 Casos de Uso Específicos

### Para Redes Sociales (10 posts únicos)

```bash
python3 core/main.py --api worldnews --articles 2 --variations 5
```

**Tiempo:** ~3 minutos  
**Resultado:** 10 posts con imágenes

### Para Blog (50 artículos variados)

```bash
python3 core/main.py --api newsapi --articles 5 --variations 10
```

**Tiempo:** ~8 minutos  
**Resultado:** 50 artículos con imágenes

### Para Campaña Masiva (200 posts)

```bash
python3 core/main.py --api newsapi --articles 5 --variations 40
```

**Tiempo:** ~45 minutos  
**Resultado:** 200 artículos únicos con imágenes

---

## 🔧 Verificar Instalación

```bash
# Probar todos los componentes
python3 test_integration.py

# Probar solo parafraseado
python3 test_paraphrase_quick.py

# Ver modelos de Blackbox disponibles
python3 list_blackbox_models.py
```

---

## 📊 Archivos Generados

### Estructura de Salida

```
news-prototype/
├── noticias_newsapi_20260107_2251.json      # Artículos originales
├── noticias_paraphrased_20260107_2251.json  # Variaciones parafraseadas
├── noticias_final_20260107_2251.json        # Resultado final con imágenes
└── images/news/
    ├── article_1.jpg
    ├── article_2.jpg
    └── ...
```

---

## 🆘 Solución Rápida de Problemas

### Error: "API key not found"

```bash
# Verifica que .env existe
cat .env | grep API_KEY

# Si falta alguna, agrégala
echo 'NEWSAPI_KEY="tu_api_key"' >> .env
```

### Error: "Module not found"

```bash
# Reinstala dependencias
source venv/bin/activate
pip install -r core/requirements.txt
```

### Error: "Blackbox API 400"

El modelo ya está corregido en `paraphrase.py`. Si persiste:

```bash
# Ver modelos disponibles
python3 list_blackbox_models.py
```

---

## 📖 Documentación Completa

- **README.md** - Guía principal del sistema
- **README-APIS.md** - Detalles de las 4 APIs
- **RESUMEN-IMPLEMENTACION.md** - Resumen técnico completo
- **INTEGRATION-STATUS.md** - Estado actual

---

## 💡 Tips Rápidos

1. **Empezar con `--test`** siempre para verificar
2. **Usar WorldNews** si NewsAPI da problemas
3. **Revisar** `images/news/` para ver imágenes generadas
4. **Leer** archivos JSON para ver estructura de datos

---

## 🎉 Comando Más Usado

```bash
# El comando que usarás el 90% del tiempo
python3 core/main.py --api newsapi --articles 5 --variations 40
```

**¿Por qué?**
- 5 artículos: suficiente variedad sin saturar
- 40 variaciones: máxima diversidad de contenido
- NewsAPI: más estable y confiable
- Total: 200 posts únicos listos para publicar

---

**¡Listo para empezar!** 🚀
