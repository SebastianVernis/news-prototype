#!/bin/bash

# Script principal de despliegue con opciones

echo "🚀 Asistente de Despliegue para el Sitio Web de Noticias"
echo "======================================================"
echo ""
echo "Seleccione una opción de despliegue:"
echo ""
echo "1) Despliegue interactivo (guía paso a paso para ingresar variables)"
echo "2) Despliegue automático (usa variables preconfiguradas)"
echo "3) Despliegue local para pruebas (sin Cloudflare)"
echo "4) Verificar estado del despliegue"
echo "5) Ayuda y documentación"
echo "6) Salir"
echo ""

read -p "Ingrese su opción (1-6): " option

case $option in
    1)
        echo ""
        echo "Iniciando despliegue interactivo..."
        echo "Este asistente le guiará paso a paso para ingresar todas las variables necesarias."
        echo ""
        ./deploy-interactive.sh
        ;;
    2)
        echo ""
        echo "Iniciando despliegue automático..."
        echo "Asegúrese de tener configuradas las variables en wrangler.toml y .dev.vars"
        echo ""
        ./full-deploy.sh
        ;;
    3)
        echo ""
        echo "Preparando despliegue local para pruebas..."
        echo ""
        echo "Opciones para pruebas locales:"
        echo ""
        echo "Opción A: Usando http-server"
        echo "  1. Instale http-server: npm install -g http-server"
        echo "  2. Navegue a la carpeta: cd public"
        echo "  3. Ejecute: http-server"
        echo "  4. Visite: http://localhost:8080"
        echo ""
        echo "Opción B: Usando Python"
        echo "  1. Navegue a la carpeta: cd public"
        echo "  2. Ejecute: python3 -m http.server 8080"
        echo "  3. Visite: http://localhost:8080"
        echo ""
        echo "Nota: Esta opción solo sirve para ver el frontend, no incluye el backend."
        ;;
    4)
        echo ""
        echo "Verificando estado del despliegue..."
        echo ""
        if command -v wrangler &> /dev/null; then
            echo "✅ Wrangler CLI está instalado"
            echo ""
            echo "Cuenta de Cloudflare:"
            wrangler whoami 2>/dev/null || echo "❌ No autenticado"
            echo ""
            echo "Proyectos de Pages:"
            wrangler pages project list 2>/dev/null || echo "No hay proyectos"
        else
            echo "❌ Wrangler CLI no está instalado"
        fi
        ;;
    5)
        echo ""
        echo "📖 Documentación y Ayuda"
        echo ""
        echo "Archivos de documentación disponibles:"
        echo "  - README.md: Documentación general del proyecto"
        echo "  - docs/README_DEPLOY.md: Instrucciones detalladas de despliegue"
        echo "  - docs/DOCUMENTACION.md: Documentación técnica completa en español"
        echo "  - docs/SUMMARY.md: Resumen del proyecto"
        echo ""
        echo "Recursos útiles:"
        echo "  - Cloudflare Dashboard: https://dash.cloudflare.com"
        echo "  - Documentation Pages: https://developers.cloudflare.com/pages/"
        echo "  - Documentation Workers: https://developers.cloudflare.com/workers/"
        echo ""
        echo "Para soporte adicional, revise los archivos de documentación mencionados."
        ;;
    6)
        echo ""
        echo "👋 ¡Hasta luego!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Opción inválida. Por favor, seleccione una opción del 1 al 6."
        exit 1
        ;;
esac
