# 🔧 Reporte de Errores - Tokens de Facebook Inválidos

**Fecha:** 2026-03-11 01:25 UTC

---

## ❌ SITIOS CON TOKENS INVÁLIDOS

### 1. noticiashorizonte
- **Estado:** ❌ Inválido
- **Token:** ✅ Existe
- **Page ID:** ✅ 403046706229851
- **Error:** "This Page access token belongs to a Page that is not accessible"
- **Causa probable:** Token expirado o página desconectada

### 2. enfoquedirecto
- **Estado:** ❌ Inválido
- **Token:** ✅ Existe
- **Page ID:** ✅ 122124424060548904
- **Error:** "This Page access token belongs to a Page that is not accessible"
- **Causa probable:** Token expirado o página desconectada

### 3. diarioexpress
- **Estado:** ❌ Inválido
- **Token:** ✅ Existe
- **Page ID:** ✅ 122116728060548904
- **Error:** "This Page access token belongs to a Page that is not accessible"
- **Causa probable:** Token expirado o página desconectada

### 4. reportediario
- **Estado:** ❌ Inválido
- **Token:** ✅ Existe
- **Page ID:** ✅ 274537812414282
- **Error:** "This Page access token belongs to a Page that is not accessible"
- **Causa probable:** Token expirado o página desconectada

---

## ✅ SITIOS CON TOKENS VÁLIDOS

| Sitio | Page ID | Estado |
|-------|---------|--------|
| noticiasobjetivo | 591610227368886 | ✅ Válido |

---

## 🔍 CAUSAS PROBABLES

### Error: "This Page access token belongs to a Page that is not accessible"

**Posibles causas:**

1. **Token expirado** (más común)
   - Los tokens de Facebook expiran después de ~60 días
   - Solución: Generar nuevos tokens de larga duración

2. **Página eliminada**
   - La página de Facebook fue eliminada
   - Solución: Crear nueva página y actualizar Page ID

3. **Página desconectada del app**
   - La página fue desconectada de la app de Facebook
   - Solución: Reconectar página en Facebook Developers

4. **Permisos revocados**
   - Los permisos de la página fueron revocados
   - Solución: Re-autorizar la página

---

## 🛠️ SOLUCIONES

### Opción 1: Generar Nuevos Tokens (Recomendado)

**Pasos:**

1. Ir a [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/)

2. Seleccionar la app de NexoPress

3. Generar token con permisos:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`

4. Seleccionar cada página y obtener el token

5. Actualizar secrets en Cloudflare:
   ```bash
   wrangler secret put FB_TOKEN_NOTICIASHORIZONTE --name news-api
   wrangler secret put FB_TOKEN_ENFOQUEDIRECTO --name news-api
   wrangler secret put FB_TOKEN_DIARIOEXPRESS --name news-api
   wrangler secret put FB_TOKEN_REPORTEDIARIO --name news-api
   ```

### Opción 2: Verificar Páginas en Facebook

**URLs de las páginas:**

- noticiashorizonte: https://www.facebook.com/403046706229851
- enfoquedirecto: https://www.facebook.com/122124424060548904
- diarioexpress: https://www.facebook.com/122116728060548904
- reportediario: https://www.facebook.com/274537812414282

**Verificar:**
- ✅ La página existe y es accesible
- ✅ La página está publicada (no en borrador)
- ✅ La página está conectada a la app de NexoPress

---

## 📊 IMPACTO

| Métrica | Valor |
|---------|-------|
| Sitios afectados | 4/27 (15%) |
| Publicaciones fallidas | ~8 artículos |
| Solución requerida | Generar nuevos tokens |

---

## ✅ PRÓXIMOS PASOS

1. **Verificar páginas en Facebook** - Confirmar que existen
2. **Generar nuevos tokens** - Usar Graph API Explorer
3. **Actualizar secrets** - En Cloudflare Workers
4. **Reintentar publicaciones** - Ejecutar force-publish nuevamente
5. **Monitorear** - Verificar que se publiquen correctamente

---

**Estado:** ⚠️ **REQUIERE ACCIÓN**  
**Prioridad:** Alta  
**Tiempo estimado de solución:** 30 minutos
