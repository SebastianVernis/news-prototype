# NexoPress - Guía Completa para Agentes de IA

## 📋 Índice

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura de Directorios](#estructura-de-directorios)
4. [Configuración y Despliegue](#configuración-y-despliegue)
5. [Base de Datos](#base-de-datos)
6. [API Endpoints](#api-endpoints)
7. [Flujo de Facebook](#flujo-de-facebook)
8. [Solución de Problemas Comunes](#solución-de-problemas-comunes)
9. [Comandos Útiles](#comandos-útiles)
10. [Variables de Entorno y Secrets](#variables-de-entorno-y-secrets)

---

## Descripción del Proyecto

**NexoPress** es una plataforma de noticias multi-sitio que gestiona 27 sitios de noticias independientes desde un único panel de administración y un núcleo centralizado en Cloudflare Workers y D1.

### Características Principales

- **27 Sitios de Noticias:** Cada uno con dominio personalizado
- **Ingesta Automática:** RSS y Atom feeds (El País, Proceso, Aristegui, etc.)
- **Parafraseo con IA:** OpenRouter (Gemini 2.0 Flash)
- **Publicación en Facebook:** Automática cada 3 horas por sitio
- **Cloudflare Stack:** Workers, D1, R2, KV, Pages

### Sitios de la Red

| # | Sitio | Dominio | Slug |
|---|-------|---------|------|
| 1 | Radio Cinco Noticias | https://www.radiocinconoticias.click | `radiocinconoticias` |
| 2 | Central México | https://www.centralmexico.online | `centralmexico` |
| 3 | TV México | https://www.tvmexiconews.site | `tvmexico` |
| 4 | CBN Noticias | https://www.cbnnoticias.click | `cbnnoticias` |
| 5 | México Informado | https://www.mexicoinformado.lat | `mexicoinformado` |
| 6 | Nodo Informativo | https://www.nodoinformativo.lat | `nodoinformativo` |
| 7 | Bitácora Urbana | https://www.bitacoraurbana.lat | `bitacoraurbana` |
| 8 | Reporte Central MX | https://www.reportecentral.site | `reportecentralmx` |
| 9 | Vértice Noticias | https://www.verticenoticias.today | `verticenoticias` |
| 10 | Noticias Objetivo | https://www.noticiasobjetivo.click | `noticiasobjetivo` |
| 11 | Boominformativo | https://www.boominformativo.lat | `boominformativo` |
| 12 | Capital Press | https://www.capitalpress.lat | `capitalpress` |
| 13 | Diario Express | https://www.diarioexpress.lat | `diarioexpress` |
| 14 | El Pulso Mexicano | https://www.elpulsomexicano.lat | `elpulsomexicano` |
| 15 | Enfoque Capital | https://www.enfoquecapital.lat | `enfoquecapital` |
| 16 | Enfoque Directo | https://www.enfoquedirecto.lat | `enfoquedirecto` |
| 17 | Fórmula CDMX | https://www.formulacdmx.lat | `formulacdmx` |
| 18 | Mexican Times | https://www.mexicantimes.lat | `mexicantimes` |
| 19 | México 360 Noticias | https://www.mexico360noticias.lat | `mexico360noticias` |
| 20 | MRadio | https://www.mradio.lat | `mradio` |
| 21 | Noticias Horizonte | https://www.noticiashorizonte.lat | `noticiashorizonte` |
| 22 | Pulso Diario | https://www.pulsodiario.lat | `pulsodiario` |
| 23 | Punto Clave | https://www.puntoclave.lat | `puntoclave` |
| 24 | Punto Noticias | https://www.puntonoticias.lat | `puntonoticias` |
| 25 | Radar Informativo | https://www.radarinformativo.lat | `radarinformativo` |
| 26 | Reporte Diario | https://www.reportediario.lat | `reportediario` |
| 27 | Television ABC | https://www.televisionabc.lat | `televisionabc` |

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cloudflare Workers                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              news-api (Worker Principal)                 │   │
│  │  - API REST (Hono framework)                            │   │
│  │  - Cron Jobs (cada 30 min)                              │   │
│  │  - Facebook Publishing (cada 3 horas por sitio)         │   │
│  │  - RSS Ingestion                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Cloudflare    │  │   Cloudflare    │  │   Cloudflare    │
│      D1         │  │      R2         │  │       KV        │
│  (SQLite DB)    │  │  (Imágenes)     │  │   (Caché)       │
│                 │  │                 │  │                 │
│ - ARTICULOS_    │  │ - uploads/      │  │ - cron_status   │
│ - SITIOS        │  │ - auto/         │  │ - last_fb_post_ │
│ - REVISION_     │  │                 │  │ - session_      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Cloudflare Pages (27 sitios)                    │
│  Cada sitio tiene:                                              │
│  - Frontend estático (HTML/CSS/JS)                              │
│  - Functions para SSR (middleware de artículos)                 │
│  - Open Graph meta tags dinámicas                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estructura de Directorios

```
/mnt/c/Users/soluc/cloudflare-news-project/
├── src/
│   ├── index.js                 # Worker principal (API + Cron + FB)
│   ├── index_append.js          # Funciones adicionales
│   ├── schema.sql               # Schema de D1
│   └── wrangler.toml            # Config del Worker
│
├── sites/                       # 27 sitios Cloudflare Pages
│   ├── radiocinconoticias/
│   ├── centralmexico/
│   ├── tvmexico/
│   ├── cbnnoticias/
│   ├── mexicoinformado/
│   ├── nodoinformativo/
│   ├── bitacoraurbana/
│   ├── reportecentralmx/
│   ├── verticenoticias/
│   └── noticiasobjetivo/
│       ├── index.html           # Homepage
│       ├── articulo/
│       │   └── index.html       # Página de artículo
│       ├── functions/
│       │   └── articulo/
│       │       └── _middleware.js  # SSR para OG tags
│       ├── components.js        # Componentes JS
│       ├── script.js            # Lógica principal
│       ├── style.css            # Estilos base
│       ├── style-custom.css     # Estilos personalizados
│       └── wrangler.toml        # Config de Pages
│
├── public/
│   └── admin/                   # Dashboard administrativo (CMS)
│       ├── index.html           # SPA principal del CMS
│       ├── generate-password-link.html  # Generador de links de setup
│       ├── setup-password.html  # Setup inicial de contraseña
│       ├── sw.js                # Service Worker para PWA
│       ├── css/
│       │   └── admin.css        # Estilos del dashboard
│       └── js/
│           ├── api.js           # Cliente HTTP para API
│           ├── auth.js          # Gestión de autenticación
│           ├── editor.js        # Editor universal de artículos
│           ├── articles.js      # Vista de lista de artículos
│           ├── cms.js           # Vista de artículos CMS
│           ├── revision.js      # Mesa de revisión
│           ├── monitor.js       # Monitor de sistema
│           ├── sites.js         # Gestión de sitios
│           ├── users.js         # Gestión de usuarios
│           ├── router.js        # Router SPA interno
│           ├── pwa-manager.js   # Gestión de PWA
│           └── theme.js         # Gestor de temas (claro/oscuro)
│
├── scripts/                     # Scripts de utilidad
│   ├── setup_fb_tokens.py       # Configurar tokens FB
│   ├── verify_fb_tokens.py      # Verificar tokens FB
│   └── cleanup_duplicates.sql   # Limpieza de duplicados
│
├── docs/                        # Documentación
│   ├── INDEX.md
│   ├── SYSTEM_MONITOR.md
│   └── ...
│
├── tools/                       # Herramientas de desarrollo
│   ├── site/
│   └── news/
│
├── backups/                     # Backups de DB
│   └── archive/
│
├── wrangler.toml                # Config raíz (referencia)
├── package.json                 # Dependencias Node
└── AGENTS.md                    # ESTE ARCHIVO
```

---

## Configuración y Despliegue

### Desplegar Worker (API)

```bash
cd /mnt/c/Users/soluc/cloudflare-news-project/src
wrangler deploy --config wrangler.toml
```

### Desplegar Sitio Pages

```bash
cd /mnt/c/Users/soluc/cloudflare-news-project/sites/[NOMBRE_SITIO]
wrangler pages deploy . --project-name=[NOMBRE_SITIO] --branch=master
```

### Desplegar Todos los Sitios

```bash
for site in radiocinconoticias centralmexico tvmexico cbnnoticias mexicoinformado nodoinformativo bitacoraurbana reportecentralmx verticenoticias noticiasobjetivo; do
  cd sites/$site && wrangler pages deploy . --project-name=$site --branch=master && cd ../..
done
```

---

## Base de Datos

### Tablas Principales

#### ARTICULOS_PARAFRASEADOS
Artículos procesados y listos para publicación.

```sql
CREATE TABLE ARTICULOS_PARAFRASEADOS (
  ID TEXT PRIMARY KEY,
  TITULO_PARAFRASEADO TEXT NOT NULL,
  SLUG TEXT,
  CONTENIDO TEXT,
  DESCRIPCION_PARAFRASEADA TEXT,
  CATEGORIA TEXT,
  AUTOR TEXT,
  FECHA_PUBLICACION TEXT,
  URL_IMAGEN TEXT,
  SITIO_DESTINO TEXT,        -- "sitio1,sitio2,sitio3"
  DESTACADO INTEGER DEFAULT 0,
  VISTAS INTEGER DEFAULT 0,
  ESTADO TEXT DEFAULT 'PUBLICADO',
  FB_REQUERIDO INTEGER DEFAULT 0,
  FB_PUBLICADO INTEGER DEFAULT 0,
  FB_FECHA TEXT,
  ES_BREVE INTEGER DEFAULT 0,
  SOURCE_URL TEXT
);
```

#### ARTICULOS_CMS
Artículos creados manualmente desde el CMS.

```sql
CREATE TABLE ARTICULOS_CMS (
  ID TEXT PRIMARY KEY,
  TITULO TEXT NOT NULL,
  SLUG TEXT NOT NULL UNIQUE,  -- ⚠️ UNIQUE constraint
  DESCRIPCION TEXT,
  CONTENIDO TEXT,
  CATEGORIA TEXT,
  URL_IMAGEN TEXT,
  SITIOS_DESTINO TEXT,
  ESTADO TEXT DEFAULT 'BORRADOR',
  DESTACADO INTEGER DEFAULT 0,
  FECHA_CREACION TEXT,
  FECHA_PUBLICACION TEXT,
  FB_PUBLICADO INTEGER DEFAULT 0,
  FB_FECHA TEXT,
  FB_REQUERIDO INTEGER DEFAULT 0
);
```

#### SITIOS
Configuración de cada sitio de la red.

```sql
CREATE TABLE SITIOS (
  ID TEXT PRIMARY KEY,
  SLUG TEXT NOT NULL UNIQUE,
  NOMBRE TEXT NOT NULL,
  DOMINIO TEXT NOT NULL,
  TAGLINE TEXT,
  LOGO_URL TEXT,
  FAVICON_URL TEXT,
  FACEBOOK_ACTIVO INTEGER DEFAULT 1,
  FACEBOOK_PAGE_ID TEXT,
  FACEBOOK_TOKEN_SECRET TEXT  -- Nombre del secret en Cloudflare
);
```

### Consultas Útiles

```bash
# Ver artículos duplicados por SLUG
wrangler d1 execute news_db --command "
  SELECT SLUG, COUNT(*) as count 
  FROM ARTICULOS_PARAFRASEADOS 
  WHERE ESTADO = 'PUBLICADO' 
  GROUP BY SLUG 
  HAVING count > 1
" --remote

# Ver artículos pendientes de Facebook
wrangler d1 execute news_db --command "
  SELECT ID, TITULO_PARAFRASEADO, SITIO_DESTINO, FB_PUBLICADO 
  FROM ARTICULOS_PARAFRASEADOS 
  WHERE FB_PUBLICADO = 0 
  LIMIT 10
" --remote

# Resetear FB_PUBLICADO para reintentar
wrangler d1 execute news_db --command "
  UPDATE ARTICULOS_PARAFRASEADOS 
  SET FB_PUBLICADO = 0, FB_FECHA = NULL 
  WHERE ID = '[ARTICLE_ID]'
" --remote
```

---

## API Endpoints

### Base URL
```
https://news-api.sebastianvernis.workers.dev/api
```

### Artículos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/articles?site=[slug]&limit=20` | Lista de artículos |
| `GET` | `/articles/:slug` | Artículo individual |
| `POST` | `/articles/bulk` | Insertar múltiples |
| `PUT` | `/articles/:id` | Actualizar artículo |
| `DELETE` | `/articles/:id` | Eliminar artículo |
| `POST` | `/articles/publish-fb/:id` | Publicar en FB manual |

### CMS

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/cms/articles` | Lista artículos CMS |
| `POST` | `/cms/articles` | Crear/Editar artículo |
| `POST` | `/cms/publish` | Publicar CMS → PARAFRASEADOS |
| `POST` | `/cms/generate-variations` | Generar variaciones IA |

### Facebook

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/facebook/monitor` | Monitor de publicaciones |
| `GET` | `/facebook/debug-tokens` | Debug de tokens |

### Cron

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/cron/status` | Estado del último cron |
| `POST` | `/cron/manual` | Ejecutar cron manual |
| `POST` | `/cron/ingest?force=true` | Forzar ingesta RSS |

---

## CMS Dashboard (Rutas y Vistas)

### URL de Acceso

| Entorno | URL |
|---------|-----|
| **Producción** | https://cms.sebastianvernis.space/admin/ |
| **Local** | http://localhost:8080/admin/ |

### Rutas del Dashboard (SPA Router)

El CMS usa un router SPA interno. Las rutas se manejan via hash (`#/ruta`).

| Ruta | Vista | Descripción | Archivo |
|------|-------|-------------|---------|
| `#/dashboard` | Dashboard | Vista principal con métricas | `index.html` |
| `#/articles` | Artículos | Lista de artículos parafraseados | `articles.js` |
| `#/cms` | CMS | Artículos creados manualmente | `cms.js` |
| `#/revision` | Revisión | Mesa de revisión de contenido | `revision.js` |
| `#/monitor` | Monitor | Estado del sistema en vivo | `monitor.js` |
| `#/sites` | Sitios | Gestión de los 27 sitios | `sites.js` |
| `#/users` | Usuarios | Gestión de usuarios y roles | `users.js` |
| `#/settings` | Configuración | Ajustes generales | `index.html` |

### Estructura del Router (`public/admin/js/router.js`)

```javascript
// Navegación
Router.navigate('articles');  // Cambia a #/articles
Router.navigate('cms');       // Cambia a #/cms

// Vistas disponibles
const views = {
  dashboard:  'Dashboard',
  articles:   'Artículos',
  cms:        'CMS',
  revision:   'Revisión',
  monitor:    'Monitor',
  sites:      'Sitios',
  users:      'Usuarios',
  settings:   'Configuración'
};
```

### Vistas Principales

#### 1. Dashboard (`#/dashboard`)
- Métricas generales
- Accesos rápidos
- Estado del sistema

#### 2. Artículos (`#/articles`)
- Lista de artículos parafraseados
- Filtros por sitio, categoría, estado
- Acciones: Editar, Publicar, Eliminar
- Botón: Publicar en Facebook

#### 3. CMS (`#/cms`)
- Lista de artículos CMS (manuales)
- Botón: Nuevo Artículo
- Acciones: Editar, Publicar, Generar Variaciones IA

#### 4. Revisión (`#/revision`)
- Artículos pendientes de aprobación
- Editor de correcciones
- Botones: Aprobar, Rechazar

#### 5. Monitor (`#/monitor`)
- Estado de crons en vivo
- Tokens de Facebook
- Historial de publicaciones
- Diagnóstico de errores

#### 6. Sitios (`#/sites`)
- Lista de los 27 sitios
- Configurar Facebook por sitio
- Activar/Desactivar sitio

#### 7. Usuarios (`#/users`)
- Lista de usuarios
- Roles: Admin, Editor
- Generar link de setup

### Editor Universal (`public/admin/js/editor.js`)

El editor se usa en múltiples vistas:

```javascript
// Abrir editor para nuevo artículo CMS
openUniversalEditor('cms', {
  title: '',
  content: '',
  excerpt: '',
  category: 'NACIONAL',
  imageUrl: '',
  featured: false
});

// Abrir editor para revisión
openUniversalEditor('revision', {
  id: rev.ID,
  title: rev.TITULO_PROPUESTO,
  content: rev.CONTENIDO_PROPUESTO,
  excerpt: rev.DESCRIPCION_PROPUESTA,
  imageUrl: rev.URL_IMAGEN
});

// Abrir editor para artículo publicado
openUniversalEditor('live', {
  id: article.ID,
  title: article.title,
  content: article.content,
  ...
});
```

### Funciones del Editor

| Función | Descripción |
|---------|-------------|
| `insertImage()` | Inserta imagen desde URL |
| `insertYouTube()` | Inserta video de YouTube |
| `insertTwitter()` | Inserta tweet embed |
| `insertInstagram()` | Inserta post de Instagram |
| `autoParagraph()` | Auto-formatea párrafos |
| `uploadUniversalImage(input)` | Sube imagen a R2 |
| `saveUniversal(action)` | Guarda artículo |

### Acciones del Editor

| Acción | Modo | Descripción |
|--------|------|-------------|
| `draft` | CMS | Guardar como borrador |
| `publish` | CMS | Publicar en sitios |
| `revision_save` | Revisión | Guardar cambios en revisión |
| `revision_approve` | Revisión | Aprobar y publicar |
| `live_update` | Live | Actualizar artículo publicado |

### Autenticación del CMS

```javascript
// Archivo: public/admin/js/auth.js

// Login
await apiFetch('/auth/login', {
  method: 'POST',
  body: JSON.stringify({ username, password })
});

// Verificar sesión
const session = await apiFetch('/auth/session');

// Logout
await apiFetch('/auth/logout', { method: 'POST' });
```

### PWA del CMS

El CMS es una Progressive Web App:

```javascript
// Service Worker: public/admin/sw.js
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('cms-v1').then((cache) => {
      return cache.addAll([
        '/admin/',
        '/admin/index.html',
        '/admin/css/admin.css',
        '/admin/js/api.js',
        // ... más archivos
      ]);
    })
  );
});
```

### Endpoints del CMS (Admin API)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/auth/login` | Iniciar sesión |
| `POST` | `/auth/logout` | Cerrar sesión |
| `GET` | `/auth/session` | Verificar sesión |
| `POST` | `/auth/users` | Crear usuario |
| `GET` | `/auth/setup/:token` | Setup con token |
| `POST` | `/auth/generate-password-link` | Generar link de setup |

---

## Flujo de Facebook

### Proceso Automático (Cron cada 30 min)

1. **Verifica timers:** Cada sitio publica cada 3 horas
2. **Selecciona artículo:** El más reciente con `FB_PUBLICADO = 0`
3. **Filtra imágenes:** Solo artículos con imagen original (no fallback)
4. **Publica en Facebook:** Usa Graph API v19.0
5. **Actualiza DB:** Marca `FB_PUBLICADO = 1`

### Función `publishToFB`

```javascript
async function publishToFB(env, article, type) {
  // 1. Obtener datos del artículo
  const targetSites = article.SITIOS_DESTINO || article.SITIO_DESTINO;
  const title = decodeHTMLEntities(article.TITULO || article.TITULO_PARAFRASEADO);
  const slug = article.SLUG || article.slug;
  const imageUrl = article.URL_IMAGEN || '';

  // 2. Para cada sitio destino
  for (const siteSlug of slugs) {
    // a. Obtener config del sitio
    const site = await env.DB.prepare(
      "SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1"
    ).bind(siteSlug).first();

    // b. Obtener token desde secrets
    const token = env[site.FACEBOOK_TOKEN_SECRET];

    // c. Construir URL del artículo
    const domain = site.DOMINIO || `${siteSlug}.pages.dev`;
    const url = `https://${domain}/articulo/?slug=${slug}`;

    // d. Publicar en Facebook
    const formData = new URLSearchParams();
    formData.append('message', title);
    formData.append('link', url);
    formData.append('picture', imageUrl);  // ✅ Miniatura
    formData.append('access_token', token);

    const response = await fetch(
      `https://graph.facebook.com/v19.0/${site.FACEBOOK_PAGE_ID}/feed`,
      { method: "POST", body: formData }
    );

    // e. Marcar como publicado si éxito
    if (response.ok) {
      await env.DB.prepare(
        `UPDATE ${table} SET FB_PUBLICADO = 1, FB_FECHA = datetime('now') 
         WHERE ID = ?`
      ).bind(article.ID).run();
    }
  }
}
```

### Configurar Tokens de Facebook

```bash
# Ejecutar script de configuración
cd /mnt/c/Users/soluc/cloudflare-news-project
python3 scripts/setup_fb_tokens.py

# O manualmente (uno por uno)
wrangler secret put FB_TOKEN_RADIOCINCONOTICIAS --name news-api
wrangler secret put FB_TOKEN_CENTRALMEXICO --name news-api
wrangler secret put FB_TOKEN_TVMEXICO --name news-api
wrangler secret put FB_TOKEN_CBNNOTICIAS --name news-api
wrangler secret put FB_TOKEN_MEXICOINFORMADO --name news-api
wrangler secret put FB_TOKEN_NODOINFORMATIVO --name news-api
wrangler secret put FB_TOKEN_BITACORAURBANA --name news-api
wrangler secret put FB_TOKEN_REPORTECENTRALMX --name news-api
wrangler secret put FB_TOKEN_VERTICENOTICIAS --name news-api
wrangler secret put FB_TOKEN_NOTICIASOBJETIVO --name news-api
```

### Verificar Tokens

```bash
# Ver lista de secrets
wrangler secret list --name news-api

# Test manual de token
curl -s "https://graph.facebook.com/v19.0/[PAGE_ID]?access_token=[TOKEN]&fields=name"
```

---

## Solución de Problemas Comunes

### 1. Error: `UNIQUE constraint failed: ARTICULOS_CMS.SLUG`

**Causa:** Dos artículos con el mismo título (mismo SLUG generado).

**Solución:** El código ahora detecta duplicados y agrega timestamp:
```javascript
// En src/index.js - app.post('/cms/articles')
if (existingSlug) {
  slug = `${slugify(titulo)}-${Date.now()}`;
}
```

### 2. Error: `D1_ERROR: UNIQUE constraint failed: ARTICULOS_PARAFRASEADOS`

**Causa:** Publicar dos veces el mismo artículo CMS.

**Solución:** El endpoint `/cms/publish` ahora verifica por SLUG:
```javascript
const existingPara = await env.DB.prepare(
  'SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? AND ESTADO = "PUBLICADO"'
).bind(baseSlug).first();

if (existingPara) {
  // UPDATE en lugar de INSERT
}
```

### 3. Facebook no muestra miniaturas

**Causas posibles:**
- Imagen es `/logo.png` o fallback
- Imagen no es URL absoluta
- Falta parámetro `picture` en POST a Facebook

**Solución:**
```javascript
// ✅ Verificar imagen válida
if (imageUrl && imageUrl.trim() !== '' && !imageUrl.includes('logo.png')) {
  formData.append('picture', imageUrl);
}

// ✅ Forzar URL absoluta
if (image.startsWith('/')) {
  image = `${url.origin}${image}`;
}
```

### 4. Entidades HTML escapadas (`&nbsp;`, `&amp;`, etc.)

**Causa:** Contenido scrapeado viene con entidades HTML.

**Solución:** Decodificar en `parseArticleRow()`:
```javascript
const decodedContent = decodeHTMLEntities(rawContent);

function decodeHTMLEntities(text) {
  return text
    .replace(/&quot;/g, '"')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>');
}
```

### 5. Functions de Pages no se ejecutan

**Causa:** Deploy a rama incorrecta o functions no están en el bundle.

**Solución:**
```bash
# Verificar que existe functions/
ls -la sites/[sitio]/functions/articulo/_middleware.js

# Desplegar a rama master
wrangler pages deploy . --project-name=[sitio] --branch=master

# Verificar deployment
curl -s "https://www.[sitio].lat/articulo/?slug=[slug]" | grep "og:image"
```

### 6. Cron no ejecuta

**Causa:** Cron trigger no está configurado o Worker no está activo.

**Solución:**
```bash
# Verificar triggers
wrangler deploy --dry-run --config wrangler.toml

# Verificar crons en dashboard de Cloudflare
# https://dash.cloudflare.com/[ACCOUNT]/workers/services/view/news-api/triggers

# Ejecutar manual
curl -X POST https://news-api.sebastianvernis.workers.dev/api/cron/manual

# Ver estado
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status
```

### 7. Artículos no se publican en Facebook

**Causas:**
- Tokens expirados
- `FB_REQUERIDO = 0`
- Timer de 3 horas no ha vencido
- Imagen es fallback

**Solución:**
```bash
# 1. Verificar tokens
python3 scripts/verify_fb_tokens.py

# 2. Resetear timers en KV
# (Se hace automático, pero se puede forzar)

# 3. Verificar artículos pendientes
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor

# 4. Forzar publicación manual
curl -X POST https://news-api.sebastianvernis.workers.dev/api/articles/publish-fb/[ARTICLE_ID]
```

---

## Comandos Útiles

### Desarrollo Local

```bash
# Worker local
cd src
wrangler dev --config wrangler.toml

# Pages local
cd sites/[sitio]
wrangler pages dev .
```

### Producción

```bash
# Deploy Worker
cd src && wrangler deploy

# Deploy Pages
cd sites/[sitio] && wrangler pages deploy . --project-name=[sitio] --branch=master

# Ver logs
wrangler tail --name news-api

# Ver KV
wrangler kv:key get --binding ARTICLES_KV cron_status
```

### Base de Datos

```bash
# Query directa
wrangler d1 execute news_db --command "SELECT COUNT(*) FROM ARTICULOS_PARAFRASEADOS" --remote

# Backup
wrangler d1 export news_db --output backup.sql --remote

# Restaurar
wrangler d1 execute news_db --file backup.sql --remote
```

### Facebook

```bash
# Configurar tokens
python3 scripts/setup_fb_tokens.py

# Verificar tokens
python3 scripts/verify_fb_tokens.py

# Ver estado
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool

# Monitor
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

---

## Variables de Entorno y Secrets

### Worker Secrets (news-api)

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `OPENROUTER_API_KEY` | API key para IA | `sk-or-...` |
| `ADMIN_TOKEN` | Token maestro admin | `admin-12345` |
| `FB_TOKEN_RADIOCINCONOTICIAS` | Token FB Radio Cinco | `[REDACTED_FB_TOKEN]` |
| `FB_TOKEN_CENTRALMEXICO` | Token FB Central México | `[REDACTED_FB_TOKEN]` |
| `FB_TOKEN_TVMEXICO` | Token FB TV México | `[REDACTED_FB_TOKEN]` |
| `FB_TOKEN_CBNNOTICIAS` | Token FB CBN Noticias | `[REDACTED_FB_TOKEN]` |
| `FB_TOKEN_MEXICOINFORMADO` | Token FB México Informado | `[REDACTED_FB_TOKEN]` |
| `FB_TOKEN_NODOINFORMATIVO` | Token FB Nodo Informativo | `[REDACTED_FB_TOKEN]` |
| `FB_TOKEN_BITACORAURBANA` | Token FB Bitácora Urbana | `[REDACTED_FB_TOKEN]` |
| `FB_TOKEN_REPORTECENTRALMX` | Token FB Reporte Central | `[REDACTED_FB_TOKEN]` |
| `FB_TOKEN_VERTICENOTICIAS` | Token FB Vértice Noticias | `[REDACTED_FB_TOKEN]` |
| `FB_TOKEN_NOTICIASOBJETIVO` | Token FB Noticias Objetivo | `[REDACTED_FB_TOKEN]` |

### Worker Variables (wrangler.toml)

```toml
[vars]
ENVIRONMENT = "production"
NEWSAPI_KEY = "..."  # Opcional, para NewsAPI
```

### Bindings

```toml
[[d1_databases]]
binding = "DB"
database_name = "news_db"
database_id = "039ec6ab-8f14-4e79-8f02-021df67a6c18"

[[kv_namespaces]]
binding = "ARTICLES_KV"
id = "fbf21fb75f5647a8966858d199b44e0b"

[[r2_buckets]]
binding = "UPLOADS"
bucket_name = "cms-news"
```

---

## Checklist de Despliegue

### Antes de Desplegar

- [ ] Verificar que no hay cambios sin commit
- [ ] Ejecutar tests locales si existen
- [ ] Verificar variables de entorno

### Deploy Worker

```bash
cd src
wrangler deploy --config wrangler.toml
# ✅ Verificar: https://news-api.sebastianvernis.workers.dev/api/cron/status
```

### Deploy Pages (cada sitio)

```bash
cd sites/[sitio]
wrangler pages deploy . --project-name=[sitio] --branch=master
# ✅ Verificar: https://www.[sitio].lat/
```

### Post-Deploy

- [ ] Verificar API responde
- [ ] Verificar sitios cargan
- [ ] Verificar OG tags en artículos
- [ ] Verificar cron status
- [ ] Verificar Facebook tokens

---

## Contacto y Soporte

- **Dashboard Admin:** https://cms.sebastianvernis.space/
- **API Base:** https://news-api.sebastianvernis.workers.dev/api
- **Monitor de Sistema:** https://cms.sebastianvernis.space/admin/#/monitor

---

*Última actualización: 2026-03-03*

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **cloudflare-news-project** (5337 symbols, 10458 relationships, 300 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## When Debugging

1. `gitnexus_query({query: "<error or symptom>"})` — find execution flows related to the issue
2. `gitnexus_context({name: "<suspect function>"})` — see all callers, callees, and process participation
3. `READ gitnexus://repo/cloudflare-news-project/process/{processName}` — trace the full execution flow step by step
4. For regressions: `gitnexus_detect_changes({scope: "compare", base_ref: "main"})` — see what your branch changed

## When Refactoring

- **Renaming**: MUST use `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` first. Review the preview — graph edits are safe, text_search edits need manual review. Then run with `dry_run: false`.
- **Extracting/Splitting**: MUST run `gitnexus_context({name: "target"})` to see all incoming/outgoing refs, then `gitnexus_impact({target: "target", direction: "upstream"})` to find all external callers before moving code.
- After any refactor: run `gitnexus_detect_changes({scope: "all"})` to verify only expected files changed.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Tools Quick Reference

| Tool | When to use | Command |
|------|-------------|---------|
| `query` | Find code by concept | `gitnexus_query({query: "auth validation"})` |
| `context` | 360-degree view of one symbol | `gitnexus_context({name: "validateUser"})` |
| `impact` | Blast radius before editing | `gitnexus_impact({target: "X", direction: "upstream"})` |
| `detect_changes` | Pre-commit scope check | `gitnexus_detect_changes({scope: "staged"})` |
| `rename` | Safe multi-file rename | `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` |
| `cypher` | Custom graph queries | `gitnexus_cypher({query: "MATCH ..."})` |

## Impact Risk Levels

| Depth | Meaning | Action |
|-------|---------|--------|
| d=1 | WILL BREAK — direct callers/importers | MUST update these |
| d=2 | LIKELY AFFECTED — indirect deps | Should test |
| d=3 | MAY NEED TESTING — transitive | Test if critical path |

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/cloudflare-news-project/context` | Codebase overview, check index freshness |
| `gitnexus://repo/cloudflare-news-project/clusters` | All functional areas |
| `gitnexus://repo/cloudflare-news-project/processes` | All execution flows |
| `gitnexus://repo/cloudflare-news-project/process/{name}` | Step-by-step execution trace |

## Self-Check Before Finishing

Before completing any code modification task, verify:
1. `gitnexus_impact` was run for all modified symbols
2. No HIGH/CRITICAL risk warnings were ignored
3. `gitnexus_detect_changes()` confirms changes match expected scope
4. All d=1 (WILL BREAK) dependents were updated

## Keeping the Index Fresh

After committing code changes, the GitNexus index becomes stale. Re-run analyze to update it:

```bash
npx gitnexus analyze
```

If the index previously included embeddings, preserve them by adding `--embeddings`:

```bash
npx gitnexus analyze --embeddings
```

To check whether embeddings exist, inspect `.gitnexus/meta.json` — the `stats.embeddings` field shows the count (0 means no embeddings). **Running analyze without `--embeddings` will delete any previously generated embeddings.**

> Claude Code users: A PostToolUse hook handles this automatically after `git commit` and `git merge`.

## CLI

- Re-index: `npx gitnexus analyze`
- Check freshness: `npx gitnexus status`
- Generate docs: `npx gitnexus wiki`

<!-- gitnexus:end -->
