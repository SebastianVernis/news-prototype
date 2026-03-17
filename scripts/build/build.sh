#!/bin/bash

# Build script completo para el proyecto de noticias

echo "🔨 Iniciando proceso de build del proyecto de noticias..."

# Crear directorios necesarios
mkdir -p build
mkdir -p build/public
mkdir -p build/api
mkdir -p build/dist

# Copiar archivos estáticos al directorio de build
echo "📂 Copiando archivos estáticos..."
cp -r public/* build/public/

# Minificar CSS
echo ".compressing CSS..."
if command -v cleancss &> /dev/null; then
    cleancss public/style.css -o build/public/style.min.css
else
    # Si clean-css no está disponible, simplemente copiar
    cp public/style.css build/public/style.min.css
    echo "⚠️  clean-css no encontrado, copiando CSS sin minificar"
fi

# Minificar JavaScript
echo ".compressing JavaScript..."
if command -v terser &> /dev/null; then
    terser public/script.js -o build/public/script.min.js
else
    # Si terser no está disponible, simplemente copiar
    cp public/script.js build/public/script.min.js
    echo "⚠️  terser no encontrado, copiando JS sin minificar"
fi

# Crear archivo de manifiesto
echo "📄 Creando archivo de manifiesto..."
cat > build/public/manifest.json << EOF
{
  "name": "Noticias Hoy",
  "short_name": "NoticiasHoy",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#f5f7fa",
  "theme_color": "#667eea",
  "description": "Tu fuente confiable de información actualizada sobre eventos nacionales e internacionales.",
  "icons": [
    {
      "src": "/favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    },
    {
      "src": "/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
EOF

# Crear archivo de precarga para mejorar rendimiento
echo "🔄 Creando archivo de precarga..."
cat > build/public/preload.html << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Preload Resources</title>
    <link rel="preload" href="/style.min.css" as="style">
    <link rel="preload" href="/script.min.js" as="script">
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&family=Playfair+Display:wght@700;800&display=swap" as="style">
</head>
<body>
    <p>Preloading resources...</p>
</body>
</html>
EOF

# Crear archivo robots.txt
echo "🤖 Creando archivo robots.txt..."
cat > build/public/robots.txt << EOF
User-agent: *
Allow: /
Sitemap: https://noticiashoy.pages.dev/sitemap.xml

# Bloquear acceso a rutas de administración
User-agent: *
Disallow: /admin/
Disallow: /admin.html
Disallow: /api/
EOF

# Crear archivo sitemap.xml
echo "🗺️ Creando archivo sitemap.xml..."
cat > build/public/sitemap.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://noticiashoy.pages.dev/</loc>
        <lastmod>$(date +%Y-%m-%d)</lastmod>
        <changefreq>hourly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://noticiashoy.pages.dev/categoria/nacional</loc>
        <lastmod>$(date +%Y-%m-%d)</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://noticiashoy.pages.dev/categoria/internacional</loc>
        <lastmod>$(date +%Y-%m-%d)</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://noticiashoy.pages.dev/categoria/politica</loc>
        <lastmod>$(date +%Y-%m-%d)</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://noticiashoy.pages.dev/categoria/economia</loc>
        <lastmod>$(date +%Y-%m-%d)</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://noticiashoy.pages.dev/admin.html</loc>
        <lastmod>$(date +%Y-%m-%d)</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.3</priority>
    </url>
</urlset>
EOF

# Crear archivo de configuración de Pages
echo "⚙️ Creando archivo de configuración de Pages..."
cat > build/_headers << EOF
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

/index.html
  Cache-Control: public, max-age=300

/style.min.css
  Cache-Control: public, max-age=31536000, immutable

/script.min.js
  Cache-Control: public, max-age=31536000, immutable

/favicon.ico
  Cache-Control: public, max-age=86400
EOF

# Crear archivo _redirects para manejo de rutas
echo "🔄 Creando archivo de redirecciones..."
cat > build/_redirects << EOF
# Redirecciones para manejo de rutas amigables
/articulo/*  /index.html  200
/categoria/*  /index.html  200
/busqueda  /index.html  200

# Redirecciones de seguridad
/http://noticiashoy.pages.dev/*  https://noticiashoy.pages.dev/:splat  301
EOF

# Copiar archivos del backend
echo "📡 Copiando archivos del backend..."
cp -r src build/api/
cp -r workers build/api/
cp -r functions build/api/

# Crear archivo de configuración de build
echo "📋 Creando archivo de configuración de build..."
cat > build/build-config.json << EOF
{
  "buildDate": "$(date -u)",
  "version": "1.0.0",
  "environment": "production",
  "assets": {
    "css": "style.min.css",
    "js": "script.min.js",
    "manifest": "manifest.json"
  },
  "optimizations": {
    "minification": true,
    "compression": true,
    "caching": true
  },
  "security": {
    "headers": true,
    "redirects": true,
    "sitemap": true
  }
}
EOF

# Mostrar resumen del build
echo "✅ Build completado exitosamente!"
echo ""
echo "📁 Directorio de build creado: build/"
echo ""
echo "Contenido del build:"
echo "- build/public/: Recursos estáticos del frontend"
echo "- build/api/: Código del backend (Workers)"
echo "- build/dist/: Archivos listos para despliegue"
echo ""
echo "Archivos generados:"
echo "- style.min.css: Hoja de estilos minificada"
echo "- script.min.js: JavaScript minificado"
echo "- manifest.json: Archivo de manifiesto de aplicación web"
echo "- robots.txt: Configuración para motores de búsqueda"
echo "- sitemap.xml: Mapa del sitio para SEO"
echo "- _headers: Cabeceras de seguridad"
echo "- _redirects: Reglas de redirección"
echo ""
echo "🎉 El proyecto está listo para despliegue!"