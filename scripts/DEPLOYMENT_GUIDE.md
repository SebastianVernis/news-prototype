# 🚀 Guía de Despliegue - Cloudflare News Project

## ✅ Sitios Listos para Desplegar

| # | Sitio | Layout | Estado |
|---|-------|--------|--------|
| 1 | **radiocinconoticias** | Carousel + Sidebar | ✅ Listo |
| 2 | **centralmexico** | Grid 4 Columnas | ✅ Listo |
| 3 | **tvmexico** | Classic | ✅ Listo |
| 4 | **cbnnoticias** | Horizontal List | ✅ Listo |
| 5 | **mexicoinformado** | Magazine | ✅ Listo |
| 6 | **nodoinformativo** | Masonry | ✅ Listo |
| 7 | **bitacoraurbana** | Masonry | ✅ Listo |
| 8 | **reportecentralmx** | Classic | ✅ Listo |
| 9 | **verticenoticias** | Masonry | ✅ Listo |
| 10 | **noticiasobjetivo** | Carousel + Sidebar | ✅ Listo |

---

## 📋 Opción 1: Despliegue con Wrangler CLI (Recomendado)

### Prerrequisitos

```bash
# Instalar wrangler
npm install -g wrangler

# Iniciar sesión
wrangler login
```

### Comandos de Despliegue

Ejecuta cada comando para desplegar un sitio:

```bash
# 1. Radio Cinco Noticias (Carousel + Sidebar)
wrangler pages deploy ./sites/radiocinconoticias --project-name=radiocinconoticias

# 2. Central México (Grid 4 Columnas)
wrangler pages deploy ./sites/centralmexico --project-name=centralmexico

# 3. TV México (Classic)
wrangler pages deploy ./sites/tvmexico --project-name=tvmexico

# 4. CBN Noticias (Horizontal List)
wrangler pages deploy ./sites/cbnnoticias --project-name=cbnnoticias

# 5. México Informado (Magazine)
wrangler pages deploy ./sites/mexicoinformado --project-name=mexicoinformado

# 6. Nodo Informativo (Masonry)
wrangler pages deploy ./sites/nodoinformativo --project-name=nodoinformativo

# 7. Bitácora Urbana (Masonry)
wrangler pages deploy ./sites/bitacoraurbana --project-name=bitacoraurbana

# 8. Reporte Central MX (Classic)
wrangler pages deploy ./sites/reportecentralmx --project-name=reportecentralmx

# 9. Vértice Noticias (Masonry)
wrangler pages deploy ./sites/verticenoticias --project-name=verticenoticias

# 10. Noticias Objetivo (Carousel + Sidebar)
wrangler pages deploy ./sites/noticiasobjetivo --project-name=noticiasobjetivo
```

### URLs de Producción

Cada sitio estará disponible en:
- `https://radiocinconoticias.pages.dev`
- `https://centralmexico.pages.dev`
- `https://tvmexico.pages.dev`
- `https://cbnnoticias.pages.dev`
- `https://mexicoinformado.pages.dev`
- `https://nodoinformativo.pages.dev`
- `https://bitacoraurbana.pages.dev`
- `https://reportecentralmx.pages.dev`
- `https://verticenoticias.pages.dev`
- `https://noticiasobjetivo.pages.dev`

---

## 📋 Opción 2: Despliegue desde Cloudflare Dashboard

### Pasos

1. **Ve a Cloudflare Dashboard**
   - https://dash.cloudflare.com/?to=/:account/pages

2. **Click en "Create a project"**

3. **Selecciona "Direct Upload"**

4. **Sube la carpeta del sitio**
   - Arrastra la carpeta `sites/radiocinconoticias` completa
   - O comprime en ZIP y sube

5. **Click en "Deploy"**

6. **Repite para cada sitio**

---

## 📋 Opción 3: Despliegue Automático con GitHub

### Configurar GitHub Repository

```bash
# Inicializar repo (si no existe)
git init
git add .
git commit -m "Initial commit - 10 news sites"

# Crear repo en GitHub y hacer push
git remote add origin https://github.com/tu-usuario/cloudflare-news.git
git push -u origin main
```

### Conectar con Cloudflare Pages

1. Ve a https://dash.cloudflare.com/?to=/:account/pages
2. Click "Create a project"
3. Selecciona "Connect to Git"
4. Selecciona tu repositorio
5. Configura:
   - **Production branch**: `main`
   - **Build command**: (dejar vacío)
   - **Build output directory**: `sites/radiocinconoticias`
6. Click "Save and Deploy"

### Deploy Automático

Cada push a `main` desplegará automáticamente.

---

## 🔧 Configuración Avanzada

### Dominio Personalizado

1. Ve al proyecto en Cloudflare Pages
2. Click en "Custom domains"
3. Agrega tu dominio (ej: `radiocinco.com`)
4. Cloudflare configura DNS automáticamente

### Variables de Entorno

Para cada sitio, puedes configurar:
- `SITE_TITLE` - Título del sitio
- `ADMIN_TOKEN` - Token para CMS

### Redirects

Crea `sites/[sitio]/_redirects`:
```
/articulo/* /articulo/informe-especial-tecnologia.html 200
/categoria/* /categoria/nacional.html 200
```

---

## 📊 Estructura de Archivos por Sitio

```
sites/[sitio]/
├── index.html              # Portada con layout personalizado
├── style.css               # Estilos únicos del sitio
├── script.js               # JavaScript (carousel, etc.)
├── article.css             # Estilos de artículos
├── legal.css               # Páginas legales
├── logo.png                # Logo del sitio
├── admin/                  # CMS de administración
│   ├── index.html
│   ├── login.html
│   ├── style.css
│   ├── script.js
│   └── login.js
├── articulo/               # 21 artículos individuales
│   ├── article-1.html
│   └── ...
├── categoria/              # 4 páginas de categoría
│   ├── nacional.html
│   ├── politica.html
│   ├── economia.html
│   └── deportes.html
└── assets/
    └── images/             # 21 imágenes descargadas
        ├── article_1.jpg
        └── ...
```

---

## 🎨 Layouts Disponibles

| Layout | Sitios | Características |
|--------|--------|----------------|
| **Carousel + Sidebar** | radiocinconoticias, noticiasobjetivo | 1 artículo principal + lista lateral |
| **Horizontal List** | cbnnoticias | Lista horizontal tipo blog |
| **Grid 4 Columnas** | centralmexico | Grid denso tipo Pinterest |
| **Masonry** | nodoinformativo, bitacoraurbana, verticenoticias | Columnas estilo Pinterest |
| **Magazine** | mexicoinformado | Hero grande + grid |
| **Classic** | tvmexico, reportecentralmx | Lista vertical tradicional |

---

## ✅ Verificación Post-Despliegue

Después de desplegar cada sitio:

1. ✅ Verificar que el logo carga
2. ✅ Verificar que las imágenes de artículos cargan
3. ✅ Probar navegación entre páginas
4. ✅ Probar CMS (`/admin/login.html`)
5. ✅ Verificar diseño responsivo (móvil)

---

## 🐛 Solución de Problemas

### Error: "Project not found"
```bash
# Crear proyecto primero en dashboard
# Luego hacer deploy
```

### Error: "Build failed"
```bash
# Verificar que la carpeta tiene index.html
ls sites/[sitio]/index.html
```

### Imágenes no cargan
```bash
# Verificar rutas en HTML
# Deben ser relativas: assets/images/article_1.jpg
```

---

## 📞 Soporte

- **Cloudflare Pages Docs**: https://developers.cloudflare.com/pages/
- **Wrangler Docs**: https://developers.cloudflare.com/workers/wrangler/

---

**Generado:** 2026-02-19  
**Total de sitios:** 10  
**Estado:** ✅ Listos para desplegar
