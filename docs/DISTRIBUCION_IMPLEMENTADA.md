# Código de Distribución Implementado

**Fecha:** 2026-03-10  
**Estado:** ✅ IMPLEMENTADO  
**Worker Version:** a5d5cb1d-d414-40c1-99e1-fe95ca638003

---

## ✅ Cambios Realizados

### 1. Endpoint `/cms/publish`

**Ubicación:** `src/index.js` línea ~1306

**Código agregado:**
```javascript
// DISTRIBUCIÓN: Insertar en cada tabla ARTICULOS_SITIO_{SLUG} con WEB_PUBLICADO = 1 por defecto
const siteDomainMap = {
  'radiocinconoticias': 'https://www.radiocinconoticias.click',
  'centralmexico': 'https://www.centralmexico.online',
  // ... 27 sitios
};

for (const siteSlug of sitios) {
  const siteId = crypto.randomUUID();
  const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
  const domain = siteDomainMap[siteSlug] || `https://${siteSlug}.pages.dev`;
  const articleUrl = `${domain}/articulo/?slug=${baseSlug}`;
  
  await c.env.DB.prepare(`
    INSERT INTO ${tableName} (
      ID, ID_PARAFRASEADO, FECHA_ASIGNACION,
      WEB_PUBLICADO, WEB_FECHA, WEB_URL,
      FB_PUBLICADO, FB_FECHA, FB_POST_ID
    ) VALUES (?, ?, datetime('now'), 1, datetime('now'), ?, 0, NULL, NULL)
  `).bind(siteId, paraId, articleUrl).run();
}
```

### 2. Endpoint `/revision/approve`

**Ubicación:** `src/index.js` línea ~1446

**Código agregado:** Mismo patrón que `/cms/publish` pero para artículos de revisión.

---

## 📊 Flujo Completo

### CMS Publishing
```
POST /cms/articles (crea artículo)
  ↓
POST /cms/publish (publica en sitios)
  ↓
1. INSERT INTO ARTICULOS_PARAFRASEADOS
  ↓
2. Para cada sitio en sitios[]:
   INSERT INTO ARTICULOS_SITIO_{SLUG}
   con WEB_PUBLICADO = 1 ✅
  ↓
3. Cron detecta (cada 30 min)
  ↓
4. Si count >= 6 → Facebook publish
```

### Revision Approval
```
POST /revision/approve/:id
  ↓
1. INSERT INTO ARTICULOS_PARAFRASEADOS
  ↓
2. Para cada sitio en SITIO_DESTINO:
   INSERT INTO ARTICULOS_SITIO_{SLUG}
   con WEB_PUBLICADO = 1 ✅
  ↓
3. Cron detecta (cada 30 min)
  ↓
4. Si count >= 6 → Facebook publish
```

---

## 🔑 Características Clave

### WEB_PUBLICADO = 1 por Defecto

```sql
INSERT INTO ARTICULOS_SITIO_{SLUG} (
  ID, ID_PARAFRASEADO, FECHA_ASIGNACION,
  WEB_PUBLICADO,  -- ✅ 1 por defecto
  WEB_FECHA,      -- ✅ datetime('now')
  WEB_URL,        -- ✅ URL completa del artículo
  FB_PUBLICADO,   -- 0 (pendiente)
  FB_FECHA,       -- NULL
  FB_POST_ID      -- NULL
) VALUES (?, ?, datetime('now'), 1, datetime('now'), ?, 0, NULL, NULL)
```

### Domain Mapping

```javascript
const siteDomainMap = {
  'radiocinconoticias': 'https://www.radiocinconoticias.click',
  'centralmexico': 'https://www.centralmexico.online',
  'tvmexico': 'https://www.tvmexiconews.site',
  // ... 27 sitios total
};
```

**Fallback:** Si el sitio no está en el map, usa `https://{slug}.pages.dev`

---

## 📊 Sitios Cubiertos (27)

### Sitios Estables (10)
1. radiocinconoticias
2. centralmexico
3. tvmexico
4. cbnnoticias
5. mexicoinformado
6. nodoinformativo
7. bitacoraurbana
8. reportecentralmx
9. verticenoticias
10. noticiasobjetivo

### Nuevos Sitios (17)
11. boominformativo
12. capitalpress
13. diarioexpress
14. elpulsomexicano
15. enfoquecapital
16. enfoquedirecto
17. formulacdmx
18. mexicantimes
19. mexico360noticias
20. mradio
21. noticiashorizonte
22. pulsodiario
23. puntoclave
24. puntonoticias
25. radarinformativo
26. reportediario
27. televisionabc

---

## 🧪 Testing

### Test 1: Crear Artículo CMS

```bash
# Crear artículo desde CMS
curl -X POST https://news-api.sebastianvernis.workers.dev/api/cms/articles \
  -H "Authorization: Bearer [TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test CMS Distribution",
    "content": "Contenido de prueba",
    "category": "TEST",
    "sites": ["radiocinconoticias", "centralmexico"]
  }'

# Verificar distribución
wrangler d1 execute news_db --command "
  SELECT s.slug, COUNT(*) as articles
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS r
  JOIN ARTICULOS_PARAFRASEADOS p ON r.ID_PARAFRASEADO = p.ID
  JOIN SITIOS s ON s.slug = 'radiocinconoticias'
  GROUP BY s.slug
" --remote
```

### Test 2: Aprobar Revisión

```bash
# Aprobar artículo de revisión
curl -X POST https://news-api.sebastianvernis.workers.dev/api/revision/approve/[ID] \
  -H "Authorization: Bearer [TOKEN]"

# Verificar distribución
wrangler d1 execute news_db --command "
  SELECT COUNT(*) as distributed
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  WHERE WEB_PUBLICADO = 1
" --remote
```

---

## 📝 Logs Esperados

```
[DISTRIBUTION] Article abc-123 assigned to radiocinconoticias with WEB_PUBLICADO=1
[DISTRIBUTION] Article abc-123 assigned to centralmexico with WEB_PUBLICADO=1
[DISTRIBUTION] Article abc-123 assigned to tvmexico with WEB_PUBLICADO=1
```

---

## ⚠️ Notas Importantes

### Faltan por Implementar

1. **RSS Ingest** - La ingesta automática de RSS aún no inserta en `ARTICULOS_SITIO_{SLUG}`
   - Los artículos RSS actuales se migraron manualmente
   - Futuro: Agregar distribución en `runRSSDirectIngest()`

2. **Bulk Import** - Si hay importación masiva, debe usar la misma lógica

### Error Handling

```javascript
try {
  await c.env.DB.prepare(`INSERT INTO ${tableName} ...`).bind(...).run();
  console.log(`[DISTRIBUTION] Article ${paraId} assigned to ${siteSlug} with WEB_PUBLICADO=1`);
} catch (e) {
  console.error(`[DISTRIBUTION] Error inserting into ${tableName}:`, e.message);
  // No falla el request completo, solo loggea el error
}
```

---

## ✅ Estado Actual

| Endpoint | Distribución | WEB_PUBLICADO | Estado |
|----------|--------------|---------------|--------|
| `/cms/publish` | ✅ Implementada | 1 por defecto | ✅ Listo |
| `/revision/approve` | ✅ Implementada | 1 por defecto | ✅ Listo |
| RSS Ingest | ⏳ Pendiente | N/A | Futuro |
| Migración manual | ✅ Completada | 1 actualizado | ✅ Listo |

---

## 🚀 Próximo Paso

**Esperar creación de artículo nuevo** (CMS o Revisión) para verificar:
1. INSERT en `ARTICULOS_PARAFRASEADOS`
2. INSERT en `ARTICULOS_SITIO_{SLUG}` × N sitios
3. `WEB_PUBLICADO = 1` por defecto
4. Cron detecta y cuenta artículos
5. Si ≥6 → Facebook publish

---

**Estado:** ✅ DISTRIBUCIÓN IMPLEMENTADA  
**Worker:** a5d5cb1d-d414-40c1-99e1-fe95ca638003  
**Próximo:** Test con artículo nuevo real
