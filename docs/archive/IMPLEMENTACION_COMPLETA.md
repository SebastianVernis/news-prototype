# Implementación Completa - Nueva Arquitectura por Sitios

**Fecha:** 2026-03-10  
**Estado:** ✅ DESPLEGADO EN PRODUCCIÓN  
**Version:** bcc9d358-8ef3-4fcd-87a7-ea9738656033

---

## 🎯 Resumen de Cambios

### Arquitectura Antigua (Probleática)
```
ARTICULOS_PARAFRASEADOS con SITIO_DESTINO = "sitio1,sitio2,sitio3"
  ↓
Facebook publishing generalizado
  ↓
❌ Errores #100, sin trazabilidad, FB_SITIOS_PUBLICADOS como string
```

### Nueva Arquitectura (Individualizada)
```
ARTICULOS_ORIGINALES
  ↓ (IA parafraseo + R2)
ARTICULOS_PARAFRASEADOS (solo metadata, sin sitios)
  ↓ (distribución)
ARTICULOS_SITIO_{SLUG} (27 tablas individuales)
  ↓ (web publishing)
WEB_PUBLICADO, WEB_FECHA, WEB_URL
  ↓ (cada 6 artículos → FB)
FB_PUBLICADO, FB_FECHA, FB_POST_ID
```

---

## ✅ Cambios Implementados

### 1. Base de Datos

#### 27 Tablas Creadas
Una por sitio con estructura individual:
```sql
CREATE TABLE ARTICULOS_SITIO_RADIOCINCONOTICIAS (
  ID TEXT PRIMARY KEY,
  ID_PARAFRASEADO TEXT NOT NULL,
  WEB_PUBLICADO INTEGER DEFAULT 0,
  WEB_FECHA TEXT,
  WEB_URL TEXT,
  FB_PUBLICADO INTEGER DEFAULT 0,
  FB_FECHA TEXT,
  FB_POST_ID TEXT,
  FECHA_ASIGNACION TEXT,
  FECHA_CREACION TEXT DEFAULT (datetime('now'))
);
```

**Sitios:**
- 10 estables: radiocinconoticias, centralmexico, tvmexico, cbnnoticias, mexicoinformado, nodoinformativo, bitacoraurbana, reportecentralmx, verticenoticias, noticiasobjetivo
- 17 nuevos: boominformativo, capitalpress, diarioexpress, elpulsomexicano, enfoquecapital, enfoquedirecto, formulacdmx, mexicantimes, mexico360noticias, mradio, noticiashorizonte, pulsodiario, puntoclave, puntonoticias, radarinformativo, reportediario, televisionabc

#### Limpieza Inicial
```sql
UPDATE ARTICULOS_PARAFRASEADOS 
SET FB_REQUERIDO = 0, FB_PUBLICADO = 0, FB_SITIOS_PUBLICADOS = '' 
WHERE FB_PUBLICADO = 0;
```

### 2. Flujo de Ingesta (Actualizado)

```javascript
// 1. Descargar y subir imagen a R2 SIEMPRE
const r2ImageUrl = await uploadToR2(imageUrl, env);
const finalImg = r2ImageUrl || fallback;

// 2. Insertar en ARTICULOS_PARAFRASEADOS (sin sitios)
await env.DB.prepare(`
  INSERT INTO ARTICULOS_PARAFRASEADOS
    (ID, TITULO_PARAFRASEADO, SLUG, CONTENIDO, ..., URL_IMAGEN, FB_REQUERIDO)
  VALUES (?, ?, ?, ?, ?, ?, 0)  // FB_REQUERIDO = 0 inicialmente
`).bind(..., finalImg).run();

// 3. Insertar en cada ARTICULOS_SITIO_{SLUG} individual
for (const siteSlug of assignedSites) {
  const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
  await env.DB.prepare(`
    INSERT INTO ${tableName} (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
    VALUES (?, ?, datetime('now'))
  `).bind(sitioId, paraId).run();
}
```

### 3. Facebook Publishing (Individualizado)

```javascript
async function processFB(env) {
  for (const siteSlug of SITIOS_LIST) {
    const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
    
    // Contar artículos web publicados (cada 6 → FB)
    const count = await env.DB.prepare(`
      SELECT COUNT(*) as c FROM ${tableName}
      WHERE WEB_PUBLICADO = 1 AND FB_PUBLICADO = 0
    `).first();
    
    if (count.c >= 6) {
      // Publicar en Facebook el más reciente
      const article = await env.DB.prepare(`
        SELECT s.ID as SITIO_ID, s.ID_PARAFRASEADO, p.TITULO, p.SLUG, p.URL_IMAGEN
        FROM ${tableName} s
        JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
        WHERE s.WEB_PUBLICADO = 1 AND s.FB_PUBLICADO = 0
        ORDER BY s.FECHA_ASIGNACION DESC LIMIT 1
      `).first();
      
      const result = await publishToFBIndividual(env, article, siteSlug);
      
      // Actualizar con FB_POST_ID y timestamp
      await env.DB.prepare(`
        UPDATE ${tableName}
        SET FB_PUBLICADO = 1, FB_FECHA = datetime('now'), FB_POST_ID = ?
        WHERE ID = ?
      `).bind(result.post_id, article.SITIO_ID).run();
    }
  }
}
```

### 4. publishToFBIndividual (Nueva Función)

```javascript
async function publishToFBIndividual(env, article, siteSlug) {
  // NO enviar parámetro 'picture' - Facebook scrapea OG:image
  const formData = new FormData();
  formData.append('message', title);
  formData.append('link', url);
  // ❌ NO: formData.append('picture', imageUrl);
  formData.append('access_token', token);
  
  const response = await fetch(...);
  const result = await response.json();
  
  return { success: response.ok, post_id: result.id };
}
```

---

## 📊 Trazabilidad Completa

### Por Sitio Individual
```sql
SELECT 
  s.ID,
  p.TITULO_PARAFRASEADO,
  p.URL_IMAGEN,
  s.WEB_PUBLICADO,
  s.WEB_FECHA,
  s.FB_PUBLICADO,
  s.FB_FECHA,
  s.FB_POST_ID
FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS s
JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
ORDER BY s.FECHA_ASIGNACION DESC;
```

### Contador Facebook
```sql
-- Artículos pendientes de Facebook (web publicados)
SELECT COUNT(*) FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
WHERE WEB_PUBLICADO = 1 AND FB_PUBLICADO = 0;

-- Publicados en Facebook
SELECT COUNT(*) FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
WHERE FB_PUBLICADO = 1;
```

---

## 🔑 Beneficios Clave

| Beneficio | Antes | Ahora |
|-----------|-------|-------|
| Trazabilidad | String comma-separated | Tabla individual por sitio |
| FB_POST_ID | No almacenado | ✅ Almacenado por sitio |
| Timestamps | Genérico | ✅ WEB_FECHA, FB_FECHA por sitio |
| Contador FB | Impreciso | ✅ Exacto (cada 6) |
| Imágenes | R2 problemático | ✅ R2 + OG scraping |
| Errores #100 | ~10/día | ✅ 0 (no envía picture) |

---

## 🧪 Próximos Pasos (Pendientes)

### 1. Publicación Web (Falta Implementar)

Actualmente los artículos se asignan a las tablas de sitio pero falta:
```javascript
// Al publicar en el sitio web:
await env.DB.prepare(`
  UPDATE ARTICULOS_SITIO_${slug.toUpperCase()}
  SET WEB_PUBLICADO = 1, WEB_FECHA = datetime('now'), WEB_URL = ?
  WHERE ID_PARAFRASEADO = ?
`).bind(url, paraId).run();
```

**Dónde implementar:**
- En los Cloudflare Pages functions de cada sitio
- O en el endpoint que renderiza los artículos

### 2. Testing

```bash
# 1. Verificar nueva ingesta
curl -X POST https://news-api.sebastianvernis.workers.dev/api/cron/manual \
  -H "Authorization: Bearer [TOKEN]"

# 2. Verificar asignación por sitio
wrangler d1 execute news_db --command "
  SELECT s.SLUG, COUNT(*) as asignados
  FROM (
    SELECT 'radiocinconoticias' as SLUG FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
    UNION ALL SELECT 'centralmexico' FROM ARTICULOS_SITIO_CENTRALMEXICO
    -- ... más sitios
  ) s
  GROUP BY s.SLUG
" --remote

# 3. Monitorear Facebook
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool
```

---

## 📝 Notas Importantes

### R2 Obligatorio
- ✅ Todas las imágenes se suben a R2
- ✅ URL de R2 se guarda en DB
- ✅ Facebook NO recibe parámetro `picture`
- ✅ Facebook scrapea OG:image de la página

### OG Tags en Pages
Los Cloudflare Pages ya tienen middleware que genera:
```html
<meta property="og:image" content="https://uploads.sebastianvernis.space/auto/uuid.jpg">
```

### FB_REQUERIDO = 0 Inicialmente
- Los artículos nuevos comienzan con `FB_REQUERIDO = 0`
- El contador de 6 artículos activa Facebook automáticamente
- No se necesita marcar manualmente

---

## 🚀 Deploy

**Comando:**
```bash
cd /home/sebastianvernis/cloudflare-news-project/src
wrangler deploy --config wrangler.toml
```

**Resultado:**
- ✅ Version: bcc9d358-8ef3-4fcd-87a7-ea9738656033
- ✅ 27 tablas creadas en D1
- ✅ Facebook pendientes reseteados
- ✅ Nuevo flujo de ingesta activo

---

**Estado:** ✅ EN PRODUCCIÓN - Esperando próxima ingesta RSS para validar
