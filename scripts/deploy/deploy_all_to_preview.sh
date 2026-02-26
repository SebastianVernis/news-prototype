#!/bin/bash

SITES="cbnnoticias centralmexico mexicoinformado nodoinformativo noticiasobjetivo radiocinconoticias reportecentralmx tvmexico verticenoticias"

echo "============================================================"
echo "Desplegando todos los sitios a PREVIEW"
echo "============================================================"

for site in $SITES; do
    echo ""
    echo "=== Desplegando $site ==="
    npx wrangler pages deploy sites/$site --project-name=$site --branch=preview --commit-dirty=true
    if [ $? -eq 0 ]; then
        echo "✅ $site desplegado correctamente"
    else
        echo "❌ Error desplegando $site"
    fi
done

echo ""
echo "============================================================"
echo "Despliegue completado"
echo "============================================================"
