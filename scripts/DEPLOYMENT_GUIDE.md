# Guía de Despliegue - Nuevos 17 Sitios

## 📋 Resumen

Esta guía cubre el despliegue de **17 nuevos sitios** a la red NexoPress, aumentando la capacidad de 10 a **27 sitios totales**.

### Nuevos Sitios

| # | Sitio | Slug | Dominio |
|---|-------|------|---------|
| 11 | Boominformativo | `boominformativo` | https://www.boominformativo.site |
| 12 | Capital Press | `capitalpress` | https://www.capitalpress.mx |
| 13 | Diario Express | `diarioexpress` | https://www.diarioexpress.news |
| 14 | El Pulso Mexicano | `elpulsomexicano` | https://www.elpulsomexicano.com |
| 15 | Enfoque Capital | `enfoquecapital` | https://www.enfoquecapital.mx |
| 16 | Enfoque Directo | `enfoquedirecto` | https://www.enfoquedirecto.news |
| 17 | Fórmula CDMX | `formulacdmx` | https://www.formulacdmx.mx |
| 18 | The Mexican Times | `mexicantimes` | https://www.mexicantimes.mx |
| 19 | México 360 Noticias | `mexico360noticias` | https://www.mexico360noticias.mx |
| 20 | M Radio | `mradio` | https://www.mradio.mx |
| 21 | Noticias Horizonte | `noticiashorizonte` | https://www.noticiashorizonte.mx |
| 22 | Pulso Diario | `pulsodiario` | https://www.pulsodiario.mx |
| 23 | Punto Clave | `puntoclave` | https://www.puntoclave.mx |
| 24 | Punto Noticias | `puntonoticias` | https://www.puntonoticias.mx |
| 25 | Radar Informativo | `radarinformativo` | https://www.radarinformativo.mx |
| 26 | Reporte Diario | `reportediario` | https://www.reportediario.mx |
| 27 | Televisión ABC | `televisionabc` | https://www.televisionabc.mx |

---

## 🚀 Pasos de Despliegue

### Paso 1: Actualizar el Worker (API)

El archivo `src/index.js` ya fue actualizado con los nuevos sitios en `SITES_CONFIG`.

```bash
# Deploy del Worker actualizado
cd /mnt/c/Users/soluc/cloudflare-news-project/src
wrangler deploy --config wrangler.toml
```

✅ **Verificación:**
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool
```

---

### Paso 2: Agregar Sitios a la Base de Datos

Ejecutar el script SQL para insertar los nuevos sitios en la tabla `SITIOS`:

```bash
# Opción A: Usando el archivo SQL
wrangler d1 execute news_db --file scripts/add_new_sites.sql --remote

# Opción B: Comando directo (copiar y pegar)
wrangler d1 execute news_db --command "
  INSERT OR IGNORE INTO SITIOS (ID, SLUG, NOMBRE, DOMINIO, TAGLINE, ACTIVO, FACEBOOK_ACTIVO) VALUES
    (lower(hex(randomblob(16))), 'boominformativo', 'Boominformativo', 'https://www.boominformativo.site', 'Información que impacta', 1, 1),
    (lower(hex(randomblob(16))), 'capitalpress', 'Capital Press', 'https://www.capitalpress.mx', 'Prensa independiente', 1, 1)
    -- ... (ver script completo en scripts/add_new_sites.sql)
" --remote
```

✅ **Verificación:**
```bash
wrangler d1 execute news_db --command "SELECT COUNT(*) as total FROM SITIOS" --remote
# Debería mostrar 27 (10 anteriores + 17 nuevos)
```

---

### Paso 3: Desplegar Sitios a Cloudflare Pages

Cada sitio debe desplegarse individualmente:

```bash
# Script automático (recomendado)
cd /mnt/c/Users/soluc/cloudflare-news-project
chmod +x scripts/deploy_new_sites.sh
./scripts/deploy_new_sites.sh
```

**O manualmente (uno por uno):**

```bash
cd sites/Nuevos/boominformativo
wrangler pages deploy . --project-name=boominformativo --branch=main

cd ../capitalpress
wrangler pages deploy . --project-name=capitalpress --branch=main

# ... repetir para cada sitio
```

✅ **Verificación:**
Visitar cualquier sitio:
- https://boominformativo.pages.dev
- https://capitalpress.pages.dev
- etc.

---

### Paso 4: Configurar Facebook Tokens (Opcional)

Si los nuevos sitios tendrán publicación automática en Facebook:

```bash
# Script interactivo (pide cada token)
python3 scripts/setup_new_sites_fb_tokens.py
```

**O manualmente (uno por uno):**

```bash
wrangler secret put FB_TOKEN_BOOMINFORMATIVO --name news-api
wrangler secret put FB_TOKEN_CAPITALPRESS --name news-api
wrangler secret put FB_TOKEN_DIARIOEXPRESS --name news-api
wrangler secret put FB_TOKEN_ENFOQUECAPITAL --name news-api
wrangler secret put FB_TOKEN_ENFOQUEDIRECTO --name news-api
wrangler secret put FB_TOKEN_FORMULACDMX --name news-api
wrangler secret put FB_TOKEN_MEXICANTIMES --name news-api
wrangler secret put FB_TOKEN_MEXICO360NOTICIAS --name news-api
wrangler secret put FB_TOKEN_MRADIO --name news-api
wrangler secret put FB_TOKEN_NOTICIASHORIZONTE --name news-api
wrangler secret put FB_TOKEN_PULSODIARIO --name news-api
wrangler secret put FB_TOKEN_PUNTOCLAVE --name news-api
wrangler secret put FB_TOKEN_PUNTONOTICIAS --name news-api
wrangler secret put FB_TOKEN_RADARINFORMATIVO --name news-api
wrangler secret put FB_TOKEN_REPORTEDIARIO --name news-api
wrangler secret put FB_TOKEN_TELEVISIONABC --name news-api
```

✅ **Verificación:**
```bash
wrangler secret list --name news-api
```

---

### Paso 5: Configurar Dominios Personalizados (Opcional)

Para cada sitio con dominio personalizado:

1. Ir a Cloudflare Dashboard → Pages → [sitio] → Custom Domains
2. Agregar dominio (ej: `www.boominformativo.site`)
3. Configurar DNS en Cloudflare

---

## 📊 Verificación Final

### 1. Verificar Worker
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status
```

### 2. Verificar Base de Datos
```bash
wrangler d1 execute news_db --command "SELECT SLUG, NOMBRE, DOMINIO FROM SITIOS ORDER BY NOMBRE" --remote
```

### 3. Verificar RSS Feeds
```bash
# Probar RSS de un nuevo sitio
curl -s "https://news-api.sebastianvernis.workers.dev/api/rss/boominformativo" | head -20
```

### 4. Verificar Facebook Tokens
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

### 5. Verificar Sitios Desplegados
Visitar las URLs de los nuevos sitios:
- https://boominformativo.pages.dev
- https://capitalpress.pages.dev
- https://diarioexpress.pages.dev
- etc.

---

## 🔧 Solución de Problemas

### Error: "Project already exists"
```bash
# El proyecto ya existe, usar --branch para actualizar
wrangler pages deploy . --project-name=[sitio] --branch=main
```

### Error: "UNIQUE constraint failed: SITIOS.SLUG"
```bash
# El sitio ya existe en la DB, es seguro ignorar este error
# O verificar con:
wrangler d1 execute news_db --command "SELECT * FROM SITIOS WHERE SLUG = 'boominformativo'" --remote
```

### Error: "Secret not found"
```bash
# El token de Facebook no está configurado
# Configurar con:
wrangler secret put FB_TOKEN_[SITIO] --name news-api
```

### RSS no muestra artículos
```bash
# Verificar que hay artículos para el sitio
wrangler d1 execute news_db --command "SELECT COUNT(*) FROM ARTICULOS_PARAFRASEADOS WHERE SITIO_DESTINO LIKE '%boominformativo%'" --remote
```

---

## 📝 Checklist de Despliegue

- [ ] Worker actualizado y desplegado
- [ ] Script SQL ejecutado (17 sitios en DB)
- [ ] 17 sitios desplegados a Pages
- [ ] Facebook tokens configurados (si aplica)
- [ ] Dominios personalizados configurados (si aplica)
- [ ] RSS feeds verificados
- [ ] Monitor de Facebook verificado

---

## 🎯 Próximos Pasos

1. **Configurar RSS Feeds** para ingesta automática de noticias
2. **Personalizar logos** de cada sitio
3. **Configurar Google Analytics** por sitio
4. **Habilitar Facebook Publishing** para cada sitio

---

**Documentación actualizada:** Marzo 2026
**Total de sitios:** 27 (10 estables + 17 nuevos)
