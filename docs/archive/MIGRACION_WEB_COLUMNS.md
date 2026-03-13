# Migración: Eliminación de columnas WEB_FECHA y WEB_URL

**Fecha:** 2026-03-11  
**Estado:** Completado

## Resumen

Se eliminaron las columnas `WEB_FECHA` y `WEB_URL` de todas las tablas `ARTICULOS_SITIO_*` para centralizar los datos en la tabla principal `ARTICULOS_PARAFRASEADOS` y construir las URLs de Facebook dinámicamente al momento de la publicación.

## Cambios Realizados

### 1. Schema de Base de Datos

**Archivo:** `src/schema_sitios_tables.sql`

Las tablas `ARTICULOS_SITIO_*` ahora tienen la siguiente estructura:

```sql
CREATE TABLE ARTICULOS_SITIO_{SLUG} (
  ID TEXT PRIMARY KEY,
  ID_PARAFRASEADO TEXT NOT NULL,
  WEB_PUBLICADO INTEGER DEFAULT 0,
  FB_PUBLICADO INTEGER DEFAULT 0,
  FB_FECHA TEXT,
  FB_POST_ID TEXT,
  FECHA_ASIGNACION TEXT,
  FECHA_CREACION TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (ID_PARAFRASEADO) REFERENCES ARTICULOS_PARAFRASEADOS(ID)
);
```

**Columnas eliminadas:**
- `WEB_FECHA TEXT` → Ahora se obtiene de `ARTICULOS_PARAFRASEADOS.FECHA_PUBLICACION`
- `WEB_URL TEXT` → Ahora se construye dinámicamente usando el SLUG + dominio del sitio

### 2. Archivos de Código Actualizados

#### `src/routes/facebook.js`
- **Cambio:** Query en `/facebook/monitor` ahora obtiene `FECHA_PUBLICACION` de `ARTICULOS_PARAFRASEADOS`
- **Antes:** `s.WEB_FECHA` de la tabla de sitio
- **Ahora:** `p.FECHA_PUBLICACION` del JOIN con `ARTICULOS_PARAFRASEADOS`

#### `src/routes/cms.js`
- **Cambio:** INSERT en tablas de sitio ya no incluye `WEB_FECHA` ni `WEB_URL`
- **Antes:** 
  ```sql
  INSERT INTO ${tableName} (..., WEB_PUBLICADO, WEB_FECHA, WEB_URL, FB_PUBLICADO, ...)
  VALUES (?, ?, datetime('now'), 1, datetime('now'), ?, 0, NULL, NULL)
  ```
- **Ahora:**
  ```sql
  INSERT INTO ${tableName} (..., WEB_PUBLICADO, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
  VALUES (?, ?, datetime('now'), 1, 0, NULL, NULL)
  ```
- **Import eliminado:** `SITE_DOMAIN_MAP` (ya no se necesita)

#### `src/routes/revision.js`
- **Cambio:** Mismo que `cms.js` - INSERT sin `WEB_FECHA` ni `WEB_URL`
- **Import eliminado:** `SITE_DOMAIN_MAP`

#### `src/cron/rss-ingest.js`
- **Cambio:** INSERT en tablas de sitio sin `WEB_FECHA` ni `WEB_URL`
- **Nota:** `SITE_DOMAIN_MAP` se mantiene para otros usos en el archivo

#### `src/routes/stats.js`
- **Cambio:** Query para artículos publicados hoy ahora usa JOIN
- **Antes:**
  ```sql
  SELECT COUNT(*) FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  WHERE WEB_PUBLICADO = 1 AND DATE(WEB_FECHA) = DATE('now')
  ```
- **Ahora:**
  ```sql
  SELECT COUNT(*) FROM ARTICULOS_PARAFRASEADOS ap
  JOIN ARTICULOS_SITIO_RADIOCINCONOTICIAS s ON s.ID_PARAFRASEADO = ap.ID
  WHERE ap.ESTADO = 'PUBLICADO' AND s.WEB_PUBLICADO = 1 
    AND DATE(ap.FECHA_PUBLICACION) = DATE('now')
  ```

### 3. Scripts de Migración

#### `src/migrate_all_sites.sh`
- Actualizado para crear tablas sin `WEB_FECHA` y `WEB_URL`

#### `src/migrate_remove_web_columns.sql` (NUEVO)
- Script SQL para migrar tablas existentes en producción
- Usa el patrón: DROP → CREATE → INSERT → DROP BACKUP
- Incluye migración para los 10 sitios estables

## Construcción Dinámica de URLs para Facebook

La función `publishToFBIndividual` en `src/cron/facebook.js` construye la URL dinámicamente:

```javascript
// Obtener configuración del sitio desde la tabla SITIOS
const site = await env.DB.prepare(
  'SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1'
).bind(siteSlug).first();

// Construir URL usando dominio del sitio + SLUG del artículo
const domain = site.DOMINIO || `${siteSlug}.pages.dev`;
const url = `https://${domain}/articulo/?slug=${article.SLUG}`;
```

**Ventajas:**
1. ✅ Los datos están centralizados en `ARTICULOS_PARAFRASEADOS`
2. ✅ Las URLs se construyen al momento de publicar (siempre actualizadas)
3. ✅ Si cambia el dominio, no hay que migrar datos
4. ✅ Menos almacenamiento en D1
5. ✅ Facebook scrapeará las OG tags directamente del Pages

## Cómo Ejecutar la Migración en Producción

### Opción 1: Recrear todas las tablas (recomendado)

```bash
cd /home/sebastianvernis/cloudflare-news-project/src
./migrate_all_sites.sh
```

**Nota:** Esto borrará las tablas existentes y las recreará. Los datos de `WEB_FECHA` y `WEB_URL` se pierden, pero ya no son necesarios.

### Opción 2: Migración preservando datos

```bash
wrangler d1 execute news_db --file migrate_remove_web_columns.sql --remote
```

**Nota:** Este script preserva los datos existentes eliminando solo las columnas `WEB_FECHA` y `WEB_URL`.

## Verificación Post-Migración

```bash
# Verificar que las tablas no tienen las columnas
wrangler d1 execute news_db --command "
  PRAGMA table_info(ARTICULOS_SITIO_RADIOCINCONOTICIAS)
" --remote

# Verificar que los artículos tienen FECHA_PUBLICACION
wrangler d1 execute news_db --command "
  SELECT ID, TITULO_PARAFRASEADO, FECHA_PUBLICACION, SITIO_DESTINO 
  FROM ARTICULOS_PARAFRASEADOS 
  WHERE ESTADO = 'PUBLICADO' 
  LIMIT 5
" --remote

# Verificar el monitor de Facebook
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

## Impacto en el Flujo de Facebook

El flujo de publicación en Facebook **NO se ve afectado**:

1. ✅ La URL se construye dinámicamente al momento de publicar
2. ✅ El SLUG del artículo ya está en `ARTICULOS_PARAFRASEADOS`
3. ✅ El dominio se obtiene de la tabla `SITIOS`
4. ✅ Facebook scrapeará las OG tags del Cloudflare Pages

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `src/schema_sitios_tables.sql` | Eliminar columnas de todas las tablas |
| `src/routes/facebook.js` | Query usa `FECHA_PUBLICACION` del JOIN |
| `src/routes/cms.js` | INSERT sin columnas, eliminar import |
| `src/routes/revision.js` | INSERT sin columnas, eliminar import |
| `src/cron/rss-ingest.js` | INSERT sin columnas |
| `src/routes/stats.js` | Query usa JOIN con `ARTICULOS_PARAFRASEADOS` |
| `src/migrate_all_sites.sh` | Actualizar creación de tablas |
| `src/migrate_remove_web_columns.sql` | **NUEVO** - Script de migración |

## Notas Adicionales

- La fecha de publicación ahora se centraliza en `ARTICULOS_PARAFRASEADOS.FECHA_PUBLICACION`
- La URL se construye usando: `{dominio}/articulo/?slug={slug}`
- Los Cloudflare Pages Functions siguen generando OG tags dinámicas
- Facebook usa las OG tags para obtener título, descripción e imagen

---

*Documentación creada: 2026-03-11*
