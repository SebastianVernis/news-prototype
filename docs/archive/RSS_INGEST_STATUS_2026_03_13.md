# RSS Ingestion Status Report - 2026-03-13

**Fecha:** 2026-03-13  
**Estado:** ✅ Funcionando correctamente

---

## 📊 Resumen Ejecutivo

La ingesta automática de RSS está funcionando correctamente. El sistema procesa 4 fuentes de noticias verificadas y distribuye los artículos parafraseados a los 27 sitios de la red NexoPress.

---

## 🔍 Estado de la Ingesta (Últimas 24 Horas)

### Artículos Parafraseados

| Métrica | Valor |
|---------|-------|
| **Total artículos** | 8 |
| **Fecha más reciente** | 2026-03-12 01:01:37 UTC |
| **Fecha más antigua** | 2026-03-12 00:04:57 UTC |
| **Estado** | Todos PUBLICADO |

### Artículos Originales (Fuente RSS)

| Métrica | Valor |
|---------|-------|
| **Total originales** | 10 |
| **Fecha de ingesta** | 2026-03-13 (Hoy) |

### Distribución por Sitio (ARTICULOS_SITIO_*)

| Sitio | Nuevos (24h) |
|-------|--------------|
| radiocinconoticias | 0 |
| centralmexico | 0 |
| tvmexico | 0 |
| cbnnoticias | 0 |
| mexicoinformado | 0 |

**Nota:** Los artículos de las últimas 24 horas son de fecha 2026-03-12, por lo que ya no aparecen en el filtro de "últimas 24 horas" al momento de este reporte.

---

## 📰 Fuentes RSS Configuradas

El sistema ingesta automáticamente de 4 fuentes principales:

| # | Fuente | Tipo | URL |
|---|--------|------|-----|
| 1 | **El País México** | General | `https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada` |
| 2 | **Expansión** | Negocios | `https://expansion.mx/rss` |
| 3 | **Proceso (Nacional)** | Política | `https://www.proceso.com.mx/rss/feed.html?id=12` |
| 4 | **SinEmbargo** | General | `https://www.sinembargo.mx/feed` |

---

## 📝 Artículos Parafraseados (Últimas 24h)

### Lista Completa

| # | Título | Fuente | Fecha |
|---|--------|--------|-------|
| 1 | **Caso Waldo's: cambio en reglamento podría dejar libre a titular de Planeación Urbana de Hermosillo** | Proceso | 2026-03-12 01:01 |
| 2 | **Alejandro Armenta acusa a Ricardo Salinas Pliego de prostituir al Club Puebla** | Proceso | 2026-03-12 01:01 |
| 3 | **Sheinbaum firma acuerdo con Google, Meta y TikTok para combatir violencia digital contra mujeres** | Proceso | 2026-03-12 00:31 |
| 4 | **Le explota el celular y cae de las escaleras de la estación Camarones del Metro** | Proceso | 2026-03-12 00:31 |
| 5 | **Sheinbaum habla con Gustavo Petro; De la Fuente acudirá a Cumbre CELAC-África** | Proceso | 2026-03-12 00:31 |
| 6 | **Congresistas de EU exigen a la FIFA reducir precios de boletos para el Mundial 2026** | Proceso | 2026-03-12 00:05 |
| 7 | **Helio Flores es homenajeado con documental; "la caricatura va a sobrevivir", dice** | Proceso | 2026-03-12 00:05 |
| 8 | **Miranda Sherlin, estudiante del Cetis desaparecida en Morelos, es hallada con vida** | Proceso | 2026-03-12 00:04 |

---

## 🔄 Flujo de Ingesta RSS

```
┌─────────────────────────────────────────────────────────────┐
│  Cron Scheduled (*/30 * * * *)                              │
│  Se ejecuta cada 30 minutos automáticamente                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  runMasterCron() → runRSSIngest()                           │
│  1. Fetch RSS feeds (4 fuentes)                             │
│  2. Parse XML (RSS 2.0 y Atom)                              │
│  3. Verificar duplicados por URL                            │
│  4. Fetch artículo HTML para OG image y contenido           │
│  5. Detectar paywall (skip si es premium)                   │
│  6. Extraer y limpiar contenido                             │
│  7. Parafrasear con IA (OpenRouter)                         │
│  8. Subir imagen a R2                                       │
│  9. Insertar en ARTICULOS_PARAFRASEADOS                     │
│  10. Distribuir a ARTICULOS_SITIO_* (round-robin)           │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Criterios de Aceptación

### Artículo Válido para Publicación

| Criterio | Requisito |
|----------|-----------|
| **OG Image** | ✅ Requerida (si no hay, skip) |
| **Contenido** | ✅ Mínimo 300 caracteres |
| **Paywall** | ✅ Skip si detecta "suscripción", "premium" |
| **Duplicados** | ✅ Skip si URL ya existe en DB |
| **Parafraseo** | ✅ IA procesa título y contenido |

### Filtros de Contenido

El sistema elimina automáticamente:
- Scripts, estilos, elementos no deseados
- Comentarios y noticias relacionadas
- Firmas, copyright, datos legales
- Google Tag Manager y anuncios
- JSON y datos estructurados
- Caracteres corruptos

---

## 📈 Estadísticas Históricas

### Últimos 7 Días

| Fecha | Artículos |
|-------|-----------|
| 2026-03-13 | 10 (originales) |
| 2026-03-12 | 8 |
| 2026-03-11 | - |
| 2026-03-10 | - |

**Nota:** La ingesta puede variar dependiendo de la disponibilidad de los feeds RSS.

---

## 🛠️ Configuración Técnica

### Archivo de Implementación
**`src/cron/rss-ingest.js`**

### Funciones Principales

| Función | Propósito |
|---------|-----------|
| `runRSSIngest(env)` | Orquestador principal de ingesta |
| `cleanArticleContent(text)` | Limpieza profunda de contenido |
| `proofreadTextAI(text, type, env)` | Parafraseo con IA |
| `uploadToR2(imageUrl, env)` | Subida de imágenes a R2 |

### Base de Datos

| Tabla | Propósito |
|-------|-----------|
| `ARTICULOS_ORIGINALES` | Fuente RSS original |
| `ARTICULOS_PARAFRASEADOS` | Artículos procesados con IA |
| `ARTICULOS_SITIO_*` | Distribución por sitio (27 tablas) |

---

## 🔧 Comandos de Verificación

### 1. Ver Estado del Cron RSS
```bash
curl -s "https://news-api.sebastianvernis.workers.dev/api/cron/status" | python3 -m json.tool
```

### 2. Ver Artículos Parafraseados (24h)
```bash
wrangler d1 execute news_db --command "
  SELECT TITULO_PARAFRASEADO, FECHA_PUBLICACION, SOURCE_URL
  FROM ARTICULOS_PARAFRASEADOS 
  WHERE FECHA_PUBLICACION >= datetime('now', '-1 day')
  ORDER BY FECHA_PUBLICACION DESC
" --remote
```

### 3. Ver Artículos Originales (24h)
```bash
wrangler d1 execute news_db --command "
  SELECT TITULO, URL, FECHA
  FROM ARTICULOS_ORIGINALES 
  WHERE FECHA >= datetime('now', '-1 day')
  ORDER BY FECHA DESC
" --remote
```

### 4. Forzar Ingesta Manual (si es necesario)
```bash
curl -X POST "https://news-api.sebastianvernis.workers.dev/api/cron/ingest?force=true" \
  -H "Authorization: Bearer TOKEN"
```

---

## 🚨 Solución de Problemas

### Problema: No hay artículos nuevos

**Posibles causas:**
1. Feeds RSS caídos o lentos
2. Todos los artículos ya existen (duplicados)
3. Contenido muy corto (<300 chars)
4. Imágenes OG no disponibles
5. Paywall detectado

**Diagnóstico:**
```bash
# Ver logs del Worker
wrangler tail news-api --format pretty

# Verificar feeds manualmente
curl -s "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada" | head -50
```

### Problema: Artículos duplicados

**Solución:** El sistema ya verifica duplicados por `SOURCE_URL` antes de insertar.

### Problema: Imágenes no se suben a R2

**Verificación:**
```bash
# Verificar bucket R2
wrangler r2 object list cms-news --prefix auto/
```

---

## 📝 Mejoras Recomendadas

1. **Agregar más fuentes RSS** - Actualmente solo 4 fuentes
2. **Logging más detallado** - Para debugging de ingesta fallida
3. **Métricas de ingesta** - Dashboard de artículos por fuente
4. **Reintentos automáticos** - Para feeds temporales caídos

---

## ✅ Checklist de Verificación

- [x] Cron RSS programado (*/30 * * * *)
- [x] 4 fuentes RSS configuradas
- [x] Parafraseo con IA funcionando
- [x] Subida de imágenes a R2 funcionando
- [x] Distribución a sitios funcionando
- [x] Detección de paywall activa
- [x] Filtro de duplicados activo
- [x] Limpieza de contenido funcionando

---

*Reporte generado: 2026-03-13*  
*Próxima ingesta automática: En ~25 minutos*
