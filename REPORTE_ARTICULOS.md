# 📊 Reporte de Artículos - Comparativa Originales vs Parafraseados

**Fecha de generación:** 2026-02-25  
**Archivo CSV:** `reporte_articulos_[timestamp].csv`  
**Tamaño:** ~140KB

---

## 📈 Resumen Ejecutivo

| Concepto | Cantidad |
|----------|----------|
| **Artículos Originales** | 171 |
| **Artículos Parafraseados** | 66 |
| **Originales sin Parafrasear** | 122 |
| **Total filas en CSV** | 188 |

---

## 📋 Estructura del CSV

El archivo CSV contiene las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| `TIPO` | "PARAFRASEADO" o "ORIGINAL_SIN_PARAFRASEAR" |
| `ID_PARAFRASEADO` | ID único del artículo parafraseado |
| `ID_ORIGINAL` | ID del artículo original relacionado |
| `TITULO_ORIGINAL` | Título del artículo original |
| `TITULO_PARAFRASEADO` | Título parafraseado |
| `DESCRIPCION_ORIGINAL` | Descripción/extracto original |
| `DESCRIPCION_PARAFRASEADA` | Descripción parafraseada |
| `URL_IMAGEN_ORIGINAL` | URL de imagen original |
| `URL_IMAGEN_PARAFRASEADO` | URL de imagen parafraseada |
| `FECHA_ORIGINAL` | Fecha de creación original |
| `FECHA_PUBLICACION` | Fecha de publicación |
| `CATEGORIA` | Categoría del artículo |
| `SITIO_DESTINO` | Sitios donde se publicó |
| `CONTENIDO_ORIGINAL_PREVIEW` | Primeros 200 caracteres del contenido original |
| `CONTENIDO_PARAFRASEADO_PREVIEW` | Primeros 200 caracteres del contenido parafraseado |
| `COINCIDE_IMAGEN` | SI/NO si la imagen es la misma |
| `COINCIDE_CATEGORIA` | SI/NO si la categoría coincide |

---

## 🎯 Estadísticas Clave

### Imágenes
- ✅ **Parafraseados con imagen:** 66 (100%)
- ❌ **Parafraseados sin imagen:** 0 (0%)

### Distribución
- **39%** de los originales han sido parafraseados (66 de 171)
- **61%** de los originales están sin parafrasear (122 de 171)

---

## 📁 Cómo Usar el CSV

### En Excel/Google Sheets:
```
1. Abrir Excel o Google Sheets
2. Archivo → Importar → Subir el CSV
3. Seleccionar codificación: UTF-8
4. Separador: Coma (,)
5. Aceptar
```

### En Python (pandas):
```python
import pandas as pd
df = pd.read_csv('reporte_articulos_[timestamp].csv')
print(df.head())
```

### Filtrar por tipo:
```
- Parafraseados: Filtrar columna TIPO = "PARAFRASEADO"
- Sin parafrasear: Filtrar columna TIPO = "ORIGINAL_SIN_PARAFRASEAR"
```

---

## 🔍 Comparaciones Útiles

### 1. Títulos Originales vs Parafraseados
Comparar columnas `TITULO_ORIGINAL` vs `TITULO_PARAFRASEADO` para ver cómo se transformaron.

### 2. Imágenes
- Columna `COINCIDE_IMAGEN` indica si se usó la misma imagen
- La mayoría de parafraseados tienen imágenes de R2 (`/api/images/news/...`)

### 3. Contenido
- Las columnas `CONTENIDO_*_PREVIEW` muestran los primeros 200 caracteres
- Útil para verificar calidad del parafraseo

---

## 📊 Próximos Pasos Sugeridos

1. **Revisar originales sin parafrasear** (122 artículos)
   - Identificar cuáles valen la pena parafrasear
   - Eliminar los que ya no sean relevantes

2. **Verificar calidad de parafraseo**
   - Muestreo aleatorio de 10-15 artículos
   - Comparar coherencia y ortografía

3. **Optimizar imágenes**
   - 100% de parafraseados tienen imagen ✅
   - Verificar que todas las URLs de R2 sean accesibles

---

**Generado por:** `scripts/fixes/export_article_comparison.js`  
**Comando:** `node scripts/fixes/export_article_comparison.js --remote`
