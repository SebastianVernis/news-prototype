# Migración: Eliminación de WEB_PUBLICADO y FACEBOOK_QUEUE

**Fecha:** 2026-03-11  
**Estado:** Completado

## Resumen

Se eliminó la columna `WEB_PUBLICADO` de todas las tablas `ARTICULOS_SITIO_*` y se eliminó completamente la tabla `FACEBOOK_QUEUE`. El nuevo flujo usa un timer en KV para publicar 1 artículo aleatorio con imagen R2 cada 3 horas por sitio.

## Cambios Principales

### 1. Schema Simplificado

```sql
CREATE TABLE ARTICULOS_SITIO_{SLUG} (
  ID TEXT PRIMARY KEY,
  ID_PARAFRASEADO TEXT NOT NULL,
  FB_PUBLICADO INTEGER DEFAULT 0,
  FB_FECHA TEXT,
  FB_POST_ID TEXT,
  FECHA_ASIGNACION TEXT,
  FECHA_CREACION TEXT DEFAULT (datetime('now'))
);
```

**Eliminado:**
- `WEB_PUBLICADO` → Todos los artículos en estas tablas están publicados
- `FACEBOOK_QUEUE` → Reemplazada por timer en KV

### 2. Nuevo Flujo de Facebook

#### Timer de 3 Horas (KV)
Cada sitio tiene un timer almacenado en KV: `last_fb_post_{slug}`

```javascript
// processFBTimer en src/cron/facebook.js
const THREE_HOURS_MS = 3 * 60 * 60 * 1000;
const lastPostTime = await env.ARTICLES_KV.get(`last_fb_post_${siteSlug}`);
const elapsed = Date.now() - lastPostTime;

if (elapsed < THREE_HOURS_MS) {
  // Skip - timer no cumplido
  return;
}
```

#### Selección Aleatoria con Filtro R2

```javascript
// Solo artículos con imagen R2 válida
const randomArticle = await env.DB.prepare(`
  SELECT s.ID, p.TITULO_PARAFRASEADO, p.SLUG, p.URL_IMAGEN
  FROM ${tableName} s
  JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
  WHERE s.FB_PUBLICADO = 0
    AND p.URL_IMAGEN IS NOT NULL
    AND p.URL_IMAGEN != ''
    AND p.URL_IMAGEN NOT LIKE '%logo.png'
    AND p.URL_IMAGEN NOT LIKE '%fallback%'
  ORDER BY RANDOM()
  LIMIT 1
`).first();
```

### 3. Publicación Inmediata

| Origen | Flujo |
|--------|-------|
| **RSS** | Espera timer de 3 horas → 1 artículo aleatorio |
| **CMS** | Publicación INMEDIATA (sin espera) |
| **Manual** | Publicación INMEDIATA (botón en dashboard) |

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `src/schema_sitios_tables.sql` | Eliminar `WEB_PUBLICADO` |
| `src/cron/facebook.js` | Nuevo `processFBTimer()`, eliminar `processFacebookQueue()` |
| `src/cron/master.js` | Usar `processFBTimer` |
| `src/cron/rss-ingest.js` | Eliminar insert en `FACEBOOK_QUEUE` |
| `src/routes/facebook.js` | Queries sin `WEB_PUBLICADO`, `/queue` muestra pendientes |
| `src/routes/cms.js` | INSERT sin `WEB_PUBLICADO` |
| `src/routes/revision.js` | INSERT sin `WEB_PUBLICADO` |
| `src/routes/stats.js` | Conteos desde `ARTICULOS_SITIO_*` |
| `src/routes/sites.js` | Eliminar conteo `web` |
| `src/migrate_all_sites.sh` | Actualizar creación de tablas |
| `src/migrate_remove_web_columns.sql` | Script para migrar tablas existentes |

## Migración en Producción

### Opción 1: Recrear tablas (recomendado)

```bash
cd src && ./migrate_all_sites.sh
```

### Opción 2: Preservar datos

```bash
wrangler d1 execute news_db --file migrate_remove_web_columns.sql --remote
```

## Verificación

```bash
# Ver timer de un sitio
wrangler kv:key get --binding ARTICLES_KV last_fb_post_radiocinconoticias

# Ver artículos pendientes con R2
wrangler d1 execute news_db --command "
  SELECT COUNT(*) as pendientes_con_r2
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS s
  JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
  WHERE s.FB_PUBLICADO = 0
    AND p.URL_IMAGEN IS NOT NULL
    AND p.URL_IMAGEN NOT LIKE '%logo.png'
" --remote

# Ver estado del cron
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool
```

---

*Documentación creada: 2026-03-11*
