# Facebook Publishing - Configuración de URLs

**Fecha:** 2026-03-11  
**Estado:** Configurado para usar `.pages.dev`

---

## Problema Resuelto

Los **dominios personalizados** NO ejecutan el middleware de Cloudflare Pages Functions, por lo que las OG tags no se inyectan y Facebook no puede leer las miniaturas.

### Solución Implementada

Facebook ahora usa los dominios `.pages.dev` que SÍ ejecutan el middleware correctamente.

---

## URLs que Facebook Usará

| Sitio | URL para Facebook |
|-------|-------------------|
| radiocinconoticias | `https://main.radiocinconoticias.pages.dev/articulo/?slug={slug}` |
| centralmexico | `https://main.centralmexico.pages.dev/articulo/?slug={slug}` |
| tvmexico | `https://main.tvmexico.pages.dev/articulo/?slug={slug}` |
| cbnnoticias | `https://main.cbnnoticias.pages.dev/articulo/?slug={slug}` |
| mexicoinformado | `https://main.mexicoinformado.pages.dev/articulo/?slug={slug}` |
| nodoinformativo | `https://main.nodoinformativo.pages.dev/articulo/?slug={slug}` |
| bitacoraurbana | `https://main.bitacoraurbana.pages.dev/articulo/?slug={slug}` |
| reportecentralmx | `https://main.reportecentralmx.pages.dev/articulo/?slug={slug}` |
| verticenoticias | `https://main.verticenoticias.pages.dev/articulo/?slug={slug}` |
| noticiasobjetivo | `https://main.noticiasobjetivo.pages.dev/articulo/?slug={slug}` |
| boominformativo | `https://main.boominformativo.pages.dev/articulo/?slug={slug}` |
| capitalpress | `https://main.capitalpress.pages.dev/articulo/?slug={slug}` |
| diarioexpress | `https://main.diarioexpress.pages.dev/articulo/?slug={slug}` |
| elpulsomexicano | `https://main.elpulsomexicano.pages.dev/articulo/?slug={slug}` |
| enfoquecapital | `https://main.enfoquecapital.pages.dev/articulo/?slug={slug}` |
| enfoquedirecto | `https://main.enfoquedirecto.pages.dev/articulo/?slug={slug}` |
| formulacdmx | `https://main.formulacdmx.pages.dev/articulo/?slug={slug}` |
| mexicantimes | `https://main.mexicantimes.pages.dev/articulo/?slug={slug}` |
| mexico360noticias | `https://main.mexico360noticias.pages.dev/articulo/?slug={slug}` |
| mradio | `https://main.mradio.pages.dev/articulo/?slug={slug}` |
| noticiashorizonte | `https://main.noticiashorizonte.pages.dev/articulo/?slug={slug}` |
| pulsodiario | `https://main.pulsodiario.pages.dev/articulo/?slug={slug}` |
| puntoclave | `https://main.puntoclave.pages.dev/articulo/?slug={slug}` |
| puntonoticias | `https://main.puntonoticias.pages.dev/articulo/?slug={slug}` |
| radarinformativo | `https://main.radarinformativo.pages.dev/articulo/?slug={slug}` |
| reportediario | `https://main.reportediario.pages.dev/articulo/?slug={slug}` |
| televisionabc | `https://main.televisionabc.pages.dev/articulo/?slug={slug}` |

---

## Cambios Realizados

### 1. `src/cron/facebook.js`

```javascript
// Construir URL del artículo - USAR .pages.dev para que OG tags funcionen
// Los dominios personalizados no ejecutan el middleware de OG tags
const pagesDomain = `${siteSlug}.pages.dev`;
const url = `https://main.${pagesDomain}/articulo/?slug=${article.SLUG}`;
```

### 2. OG Tags Verificadas

Ejemplo de OG tags que Facebook verá:

```html
<meta property="og:title" content="Entre guerra y futbol: Irán ve imposible disputar el Mundial 2026 en Estados Unidos" />
<meta property="og:description" content="La posibilidad de que Irán participe en el Mundial 2026 ha sido descartada..." />
<meta property="og:image" content="https://uploads.sebastianvernis.space/auto/7ae09aa0-7945-43ce-8440-27dcf516808f.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:type" content="article" />
<meta property="og:url" content="https://main.tvmexico.pages.dev/articulo/?slug=..." />
```

---

## Verificación

### ✅ Funciona (.pages.dev)
```bash
curl -s "https://main.tvmexico.pages.dev/articulo/?slug=..." | grep "og:title"
# Resultado: og:title content="..."
```

### ❌ No funciona (Custom Domain)
```bash
curl -s "https://tvmexiconews.site/articulo/?slug=..." | grep "og:title"
# Resultado: (vacío)
```

---

## Próximos Pasos

1. **Monitorear** las publicaciones en Facebook para asegurar que las miniaturas cargan
2. **Debug Facebook**: https://developers.facebook.com/tools/debug/
3. **Compartir** un artículo de prueba y verificar que la miniatura aparece

---

*Documentación creada: 2026-03-11*
