# 🚀 Guía Rápida de Inicio

## Configuración Inicial (Solo una vez)

### 1. Obtener API Key de Blackbox

1. Ve a https://www.blackbox.ai
2. Crea una cuenta o inicia sesión
3. Ve a Settings → API Keys
4. Copia tu API key

### 2. Configurar el archivo .env

Edita el archivo `.env` y reemplaza `tu_api_key_aqui` con tu API key real:

```bash
nano .env
```

Debe verse así:
```env
NEWSAPI_KEY="3fe1ad82a95f462c802ebbacd88ce4db"
BLACKBOX_API_KEY="tu_api_key_real_aqui"
```

Guarda con `Ctrl+O`, Enter, `Ctrl+X`

## Ejecución

### Modo Prueba (Recomendado primero)

```bash
bash run-generator.sh test
```

Esto procesará:
- 2 artículos de noticias
- 5 variaciones por artículo
- 10 imágenes generadas con Flux Schnell
- Tiempo: ~2-3 minutos
- Costo estimado: ~$0.03 (10 imágenes × $0.003)

### Modo Completo

```bash
bash run-generator.sh
```

Esto procesará:
- 5 artículos de noticias
- 40 variaciones por artículo
- 200 imágenes generadas con Flux Schnell
- Tiempo: ~30-45 minutos
- Costo estimado: ~$0.60 (200 imágenes × $0.003)

## Verificar Resultados

### Archivos JSON generados:

```bash
ls -lh noticias_*.json
```

Verás:
- `noticias_mx_TIMESTAMP.json` - Artículos originales
- `noticias_paraphrased_TIMESTAMP.json` - Con variaciones
- `noticias_final_TIMESTAMP.json` - Con imágenes

### Imágenes generadas:

```bash
ls images/news/
```

## Solución Rápida de Problemas

### ❌ Error: "BLACKBOX_API_KEY no encontrada"

**Solución**: Edita `.env` y agrega tu API key real

```bash
nano .env
# Reemplaza "tu_api_key_aqui" con tu key real
```

### ❌ Error: "No module named 'requests'"

**Solución**: El script instalará automáticamente las dependencias. Si falla:

```bash
source venv/bin/activate
pip install -r core/requirements.txt
```

### ❌ Error: "Permission denied"

**Solución**: Da permisos de ejecución al script:

```bash
chmod +x run-generator.sh
```

### ❌ Las imágenes no se generan

**Posibles causas**:
1. API key inválida → Verifica tu key en .env
2. Límite de API alcanzado → Espera o usa modo prueba
3. Modelo no disponible → Verifica logs de error

## Comandos Útiles

### Ver logs en tiempo real:

```bash
bash run-generator.sh test 2>&1 | tee output.log
```

### Limpiar archivos generados:

```bash
rm noticias_*.json
rm images/news/*.jpg
```

### Ver estadísticas:

```bash
echo "Artículos JSON: $(ls noticias_*.json 2>/dev/null | wc -l)"
echo "Imágenes: $(ls images/news/*.jpg 2>/dev/null | wc -l)"
```

## Próximos Pasos

1. ✅ Ejecuta modo prueba
2. ✅ Verifica que se generaron archivos
3. ✅ Revisa las imágenes en `images/news/`
4. ✅ Ejecuta modo completo si todo funciona
5. ✅ Integra con tus plantillas HTML

## Personalización

### Cambiar número de artículos:

```bash
source venv/bin/activate
python3 core/main.py --articles 10 --variations 20
```

### Solo descargar noticias (sin IA):

```bash
source venv/bin/activate
python3 news.py
```

### Solo parafrasear (sin imágenes):

```bash
source venv/bin/activate
python3 paraphrase.py
```

## Ayuda

Para más información detallada, consulta `README.md`

```bash
cat README.md
```

---

**¿Listo? Ejecuta:**

```bash
bash run-generator.sh test
```
