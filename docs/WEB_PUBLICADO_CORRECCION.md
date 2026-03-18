# WEB_PUBLICADO - Lógica Corregida

**Fecha:** 2026-03-10  
**Estado:** ✅ LÓGICA CORREGIDA

---

## 🐛 Problema Detectado

**Lógica anterior (INCORRECTA):**
```
Artículo se asigna a sitio → WEB_PUBLICADO = 0
  ↓
Usuario visita artículo
  ↓
Middleware: UPDATE SET WEB_PUBLICADO = 1
```

**Problema:**
- Los artículos NO aparecen en el index ni como destacados
- Nadie los visita → nunca se marcan como `WEB_PUBLICADO = 1`
- Facebook nunca publica (espera 6 artículos web)
- **Círculo vicioso**

---

## ✅ Lógica Corregida

### 1. Al Insertar Artículo en Sitio (DEFAULT)

```sql
INSERT INTO ARTICULOS_SITIO_{SLUG} (
  ID, ID_PARAFRASEADO, FECHA_ASIGNACION,
  WEB_PUBLICADO,  -- ✅ 1 por defecto
  WEB_FECHA,
  WEB_URL
) VALUES (
  'unique-id',
  'article-id',
  datetime('now'),
  1,  -- ✅ WEB_PUBLICADO = 1 por defecto
  datetime('now'),
  'https://sitio.com/articulo/?slug=...'
);
```

### 2. Middleware (Solo Actualiza WEB_URL)

```javascript
// Middleware en sites/{sitio}/functions/articulo/_middleware.js
await env.DB.prepare(`
  UPDATE ${tableName}
  SET WEB_URL = ?, 
      WEB_FECHA = CASE 
        WHEN WEB_FECHA IS NULL THEN datetime('now') 
        ELSE WEB_FECHA 
      END
  WHERE ID_PARAFRASEADO = ?
`).bind(url.href, article.para_id).run();
```

**Nota:** `WEB_PUBLICADO` ya es 1, solo actualizamos `WEB_URL` y `WEB_FECHA` si es necesario.

---

## 📊 Flujo Correcto

```
1. RSS/IA crea artículo en PARAFRASEADOS
   ↓
2. Distribución asigna a 3 sitios
   ↓
3. INSERT en ARTICULOS_SITIO_{SLUG} con WEB_PUBLICADO = 1
   ↓
4. Cron detecta: COUNT(*) WHERE WEB=1 AND FB=0
   ↓
5. Si count >= 6 → Publicar en Facebook
   ↓
6. UPDATE SET FB_PUBLICADO = 1, FB_POST_ID, FB_FECHA
```

---

## 🔧 Cambios Realizados

### 1. Middleware Actualizado

**Antes:**
```javascript
UPDATE ${tableName}
SET WEB_PUBLICADO = 1, WEB_FECHA = datetime('now'), WEB_URL = ?
WHERE ID_PARAFRASEADO = ? AND WEB_PUBLICADO = 0
```

**Después:**
```javascript
UPDATE ${tableName}
SET WEB_URL = ?, 
    WEB_FECHA = CASE WHEN WEB_FECHA IS NULL THEN datetime('now') ELSE WEB_FECHA END
WHERE ID_PARAFRASEADO = ?
```

### 2. Datos de Prueba Actualizados

```sql
UPDATE ARTICULOS_SITIO_{SLUG} 
SET WEB_PUBLICADO = 1 
WHERE ID_PARAFRASEADO = 'test-article-001';
```

**Sitios actualizados:**
- radiocinconoticias ✅
- centralmexico ✅
- tvmexico ✅
- cbnnoticias ✅
- mexicoinformado ✅
- nodoinformativo ✅

---

## 📝 Próximos Pasos (Falta Implementar)

### 1. Código de Distribución (Ingesta RSS)

Cuando se crea un artículo nuevo, el código de ingesta debe:

```javascript
// En el código de ingesta RSS (FALTA IMPLEMENTAR)
for (const siteSlug of assignedSites) {
  const siteId = crypto.randomUUID();
  const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
  
  await env.DB.prepare(`
    INSERT INTO ${tableName} (
      ID, ID_PARAFRASEADO, FECHA_ASIGNACION,
      WEB_PUBLICADO, WEB_FECHA, WEB_URL
    ) VALUES (?, ?, datetime('now'), 1, datetime('now'), ?)
  `).bind(siteId, paraId, `https://${siteSlug}.pages.dev/articulo/?slug=${slug}`).run();
}
```

### 2. CMS Publishing

Cuando se publica un artículo CMS, debe insertar en las tablas de sitio:

```javascript
// En /cms/publish endpoint (FALTA IMPLEMENTAR)
for (const siteSlug of sitios) {
  const siteId = crypto.randomUUID();
  const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
  
  await env.DB.prepare(`
    INSERT INTO ${tableName} (
      ID, ID_PARAFRASEADO, FECHA_ASIGNACION,
      WEB_PUBLICADO, WEB_FECHA, WEB_URL
    ) VALUES (?, ?, datetime('now'), 1, datetime('now'), ?)
  `).bind(siteId, paraId, `https://${siteSlug}.pages.dev/articulo/?slug=${slug}`).run();
}
```

---

## ✅ Estado Actual

| Componente | Estado | Notas |
|------------|--------|-------|
| Middleware | ✅ Actualizado | Solo actualiza WEB_URL |
| Datos de prueba | ✅ WEB_PUBLICADO = 1 | 6 sitios listos |
| Código de distribución | ⏳ Falta implementar | En ingesta RSS y CMS |
| Cron FB | ✅ Listo | Espera WEB_PUBLICADO = 1 |

---

## 🧪 Verificación

### Test Artículo de Prueba

```bash
# Verificar estado
wrangler d1 execute news_db --command "
  SELECT ID, WEB_PUBLICADO, FB_PUBLICADO
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  WHERE ID_PARAFRASEADO = 'test-article-001'
" --remote
```

**Resultado esperado:**
```
ID: test-site-001-radio
WEB_PUBLICADO: 1 ✅
FB_PUBLICADO: 0 ⏰ (esperando cron)
```

---

**Estado:** ✅ LÓGICA CORREGIDA  
**Próximo:** Implementar código de distribución en ingesta RSS y CMS
