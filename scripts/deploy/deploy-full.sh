#!/bin/bash
# ==============================================
#   Script de Despliegue Completo
#   Cloudflare News Project
# ==============================================

set -e

echo ""
echo "=============================================="
echo "   Despliegue Completo - Cloudflare"
echo "=============================================="
echo ""

RED='\033[0;31m'GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

status() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

! command -v wrangler &> /dev/null
then
error
"wrangler
no
esta
instalado"
exit
1fi
