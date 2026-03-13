# Test de Facebook Publishing - Artículo de Prueba

**Fecha:** 2026-03-10 05:25 UTC  
**Estado:** ✅ ARTÍCULO CREADO - Esperando cron automático

---

## 📊 Artículo de Prueba Creado

### Datos del Artículo
```
ID: test-article-001
Título: "TEST: Artículo de prueba para verificar flujo Facebook"
Slug: test-articulo-prueba-flujo-facebook
URL Imagen: https://images.unsplash.com/photo-1504711434969-e33886168f5c
```

### Sitios Asignados (6 artículos web)
| Sitio | ID Sitio | WEB_PUBLICADO | FB_PUBLICADO |
|-------|----------|---------------|--------------|
| radiocinconoticias | test-site-001-radio | ✅ 1 | ⏰ 0 |
| centralmexico | test-site-001-central | ✅ 1 | ⏰ 0 |
| tvmexico | test-site-001-tv | ✅ 1 | ⏰ 0 |
| cbnnoticias | test-site-001-cbn | ✅ 1 | ⏰ 0 |
| mexicoinformado | test-site-001-mexinfo | ✅ 1 | ⏰ 0 |
| nodoinformativo | test-site-001-nodo | ✅ 1 | ⏰ 0 |

---

## 🔄 Flujo Esperado

### Estado Actual (Pre-Cron)
```
6 sitios con WEB_PUBLICADO = 1
0 sitios con FB_PUBLICADO = 1
```

### Después del Cron (Post-Cron)
```
Cron ejecuta processFB()
  ↓
Para cada sitio:
  - COUNT(*) WHERE WEB=1 AND FB=0
  - count = 1 (≥ 6 umbral)
  ↓
Publica en Facebook el artículo más reciente
  ↓
UPDATE ARTICULOS_SITIO_{SLUG}
  SET FB_PUBLICADO = 1, 
      FB_FECHA = datetime('now'), 
      FB_POST_ID = '[FB_POST_ID]'
```

**Resultado Esperado:**
- 6 sitios con `FB_PUBLICADO = 1`
- 6 sitios con `FB_POST_ID` (ID de post de Facebook)
- 6 sitios con `FB_FECHA` (timestamp de publicación)

---

## 🧪 Cómo Verificar

### 1. Verificar Estado en DB
```bash
wrangler d1 execute news_db --command "
  SELECT ID, WEB_PUBLICADO, FB_PUBLICADO, FB_POST_ID, FB_FECHA
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  WHERE ID_PARAFRASEADO = 'test-article-001'
" --remote
```

**Resultado esperado (después del cron):**
```
ID: test-site-001-radio
WEB_PUBLICADO: 1
FB_PUBLICADO: 1
FB_POST_ID: 123456789012345 (ID real de Facebook)
FB_FECHA: 2026-03-10 05:30:00
```

### 2. Verificar Monitor de Facebook
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

**Buscar:**
- Artículo con título "TEST: Artículo de prueba..."
- `WEB_PUBLICADO: 1`
- `FB_PUBLICADO: 1`
- `FB_POST_ID: [ID real]`

### 3. Verificar en Facebook (Opcional)
Visitar las páginas de Facebook de los sitios:
- https://www.facebook.com/radiocinconoticias
- https://www.facebook.com/centralmexico
- etc.

**Buscar:**
- Post con el título del artículo de prueba
- Link a `https://www.[sitio].click/articulo/?slug=test-articulo-prueba-flujo-facebook`

---

## ⏰ Próxima Ejecución del Cron

**Última ejecución:** 2026-03-10T05:00:55.447Z  
**Próxima ejecución:** ~5-10 minutos (cron cada 30 min)

**Qué esperar:**
1. Cron ejecuta `processFB()` automáticamente
2. Para cada sitio con ≥6 artículos web, publica 1 en Facebook
3. Actualiza `FB_PUBLICADO = 1`, `FB_POST_ID`, `FB_FECHA`

---

## ✅ Criterios de Éxito

| Criterio | Antes | Después (Esperado) |
|----------|-------|-------------------|
| WEB_PUBLICADO (6 sitios) | 1 | 1 (sin cambios) |
| FB_PUBLICADO (6 sitios) | 0 | 1 ✅ |
| FB_POST_ID (6 sitios) | NULL | ID real ✅ |
| FB_FECHA (6 sitios) | NULL | Timestamp ✅ |
| Error #100 en Facebook | N/A | 0 ✅ |

---

## 🐛 Troubleshooting

### Si FB_PUBLICADO sigue en 0 después del cron

**Posibles causas:**
1. **Token de Facebook expirado** - Verificar con `/facebook/debug-tokens`
2. **Sitio inactivo** - Verificar `FACEBOOK_ACTIVO = 1` en SITIOS
3. **Error en publishToFBIndividual** - Revisar logs del Worker

**Comandos de diagnóstico:**
```bash
# Verificar tokens
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/debug-tokens

# Verificar estado del cron
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status

# Ver logs del Worker
wrangler tail --name news-api
```

### Si hay Error #100

**Causa:** Facebook rechaza la imagen

**Solución:** El código ya NO envía parámetro `picture`, Facebook scrapea OG:image

---

## 📝 Notas

- **Artículo de prueba:** Se puede eliminar después del test
- **Limpieza:** `DELETE FROM ARTICULOS_SITIO_{SLUG} WHERE ID_PARAFRASEADO = 'test-article-001'`
- **Seguro:** El test no afecta artículos reales

---

**Estado:** ✅ ESPERANDO CRON AUTOMÁTICO  
**Próximo cron:** ~5-10 minutos  
**Acción requerida:** Ninguna (automático)
