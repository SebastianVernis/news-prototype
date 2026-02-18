#!/bin/bash
# Launcher para el menú interactivo
# Soporta flujos con Blackbox AI (paralelo y estándar)

cd "$(dirname "$0")"

# Verificar si se pasó algún argumento
if [ $# -eq 0 ]; then
    # Sin argumentos: lanzar menú interactivo
    python3 menu.py
else
    # Con argumentos: ejecutar comando directo
    python3 menu.py "$@"
fi
