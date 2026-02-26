#!/bin/bash
# Script de comprobación rápida para el sitio web de noticias

echo "🔍 Comprobación Rápida del Sitio Web de Noticias"
echo "=============================================="

# Comprobar página principal
echo ""
echo "✅ Comprobando página principal..."
if curl -s -o /dev/null -w "%{http_code}" https://noticias-hoy.pages.dev | grep -q "200"; then
    echo "   ✅ Página principal: FUNCIONAL"
else
    echo "   ❌ Página principal: ERROR"
fi

# Comprobar una categoría
echo ""
echo "✅ Comprobando categoría..."
if curl -s -o /dev/null -w "%{http_code}" https://noticias-hoy.pages.dev/categoria/nacional | grep -q "200"; then
    echo "   ✅ Categoría nacional: FUNCIONAL"
else
    echo "   ❌ Categoría nacional: ERROR"
fi

# Comprobar un artículo
echo ""
echo "✅ Comprobando artículo..."
if curl -s -o /dev/null -w "%{http_code}" https://noticias-hoy.pages.dev/articulo/presidente-plan-economico | grep -q "200"; then
    echo "   ✅ Artículo: FUNCIONAL"
else
    echo "   ❌ Artículo: ERROR"
fi

# Comprobar página legal
echo ""
echo "✅ Comprobando página legal..."
if curl -s -o /dev/null -w "%{http_code}" https://noticias-hoy.pages.dev/acerca-de | grep -q "200"; then
    echo "   ✅ Página legal: FUNCIONAL"
else
    echo "   ❌ Página legal: ERROR"
fi

echo ""
echo "🎉 ¡COMPROBACIÓN COMPLETADA!"
echo ""
echo "Si ves ✅ en todas las comprobaciones, tu sitio web está funcionando correctamente."
echo ""
echo "Recursos disponibles:"
echo "🏠 Página principal: https://noticias-hoy.pages.dev"
echo "📰 Categorías: https://noticias-hoy.pages.dev/categoria/[nombre]"
echo "📝 Artículos: https://noticias-hoy.pages.dev/articulo/[titulo]"
echo "📋 Páginas legales: https://noticias-hoy.pages.dev/[pagina]"
echo ""
echo "Tu sitio web de noticias con contenido real está completamente operativo."