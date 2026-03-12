#!/bin/bash
# Script para subir logos como foto de perfil en Facebook
# Solo para los 17 SITIOS NUEVOS
#
# Uso: ./scripts/upload_fb_profile_pics_manual.sh
#
# IMPORTANTE: Debes configurar tu TOKEN_DE_FACEBOOK abajo

# ═══════════════════════════════════════════════════════════════
# ⚙️  CONFIGURACIÓN - REEMPLAZA ESTE VALOR
# ═══════════════════════════════════════════════════════════════
TOKEN_DE_FACEBOOK="TU_TOKEN_AQUI"
# ═══════════════════════════════════════════════════════════════

# Verificar que el token fue configurado
if [ "$TOKEN_DE_FACEBOOK" == "TU_TOKEN_AQUI" ]; then
  echo "❌ ERROR: Debes configurar tu token de Facebook"
  echo ""
  echo "Instrucciones:"
  echo "1. Abre este archivo: nano scripts/upload_fb_profile_pics_manual.sh"
  echo "2. Reemplaza 'TU_TOKEN_AQUI' con tu token real"
  echo "3. Guarda el archivo (Ctrl+X, Y, Enter)"
  echo "4. Ejecuta el script nuevamente"
  echo ""
  echo "Cómo obtener tu token:"
  echo "1. Ve a: https://developers.facebook.com/tools/explorer/"
  echo "2. Click en 'Get Token' → 'Get User Access Token'"
  echo "3. Selecciona: pages_manage_posts, pages_read_engagement"
  echo "4. Click en 'Generate Access Token'"
  echo "5. Copia el token y pégalo arriba"
  echo ""
  exit 1
fi

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Subir Logos como Foto de Perfil - Facebook${NC}"
echo -e "${BLUE}   Solo 17 SITIOS NUEVOS${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

# Lista de sitios nuevos: slug:page_id:dominio
declare -a SITES=(
  "boominformativo:501728116348917:boominformativo.top"
  "capitalpress:458242550714232:capitalpress.lat"
  "diarioexpress:270142695517794:diarioexpress.click"
  "elpulsomexicano:253187761218980:elpulsomexicano.lat"
  "enfoquecapital:457328060805587:enfoquecapital.top"
  "enfoquedirecto:454841367704076:enfoquedirecto.lat"
  "formulacdmx:500033023189155:formulacdmx.top"
  "mexicantimes:578088192045850:mexicantimes.top"
  "mexico360noticias:286495644543503:mexico360noticias.click"
  "mradio:472254365974557:mradio.lat"
  "noticiashorizonte:403046706229851:noticiashorizonte.click"
  "pulsodiario:429372300256610:pulsodiario.lat"
  "puntoclave:497685936753403:puntoclave.lat"
  "puntonoticias:216140764924862:puntonoticias.website"
  "radarinformativo:405301062674763:radarinformativo.online"
  "reportediario:274537812414282:reportediario.online"
  "televisionabc:481562451709320:televisionabc.lat"
)

TOTAL=${#SITES[@]}
SUCCESS=0
FAILED=0
SKIPPED=0

echo -e "${YELLOW}📋 Total de sitios a procesar: ${TOTAL}${NC}"
echo ""
echo "Presiona Ctrl+C para cancelar en cualquier momento"
echo ""
read -p "Presiona ENTER para comenzar..."

echo ""

for i in "${!SITES[@]}"; do
  IFS=':' read -r slug pageid domain <<< "${SITES[$i]}"
  
  LOGO_URL="https://www.${domain}/logo.png"
  NUMERO=$((i + 1))
  
  echo -e "${BLUE}─────────────────────────────────────────────────────${NC}"
  echo -e "${BLUE} [${NUMERO}/${TOTAL}] ${slug}${NC}"
  echo -e "   Page ID: ${pageid}"
  echo -e "   Logo: ${LOGO_URL}"
  echo ""
  
  # Verificar que el logo sea accesible
  if ! curl -s --head --request GET "${LOGO_URL}" | grep "200 OK" > /dev/null; then
    echo -e "   ${RED}⚠️  Logo no accesible, saltando...${NC}"
    SKIPPED=$((SKIPPED + 1))
    echo ""
    continue
  fi
  
  # Subir foto de perfil
  RESPONSE=$(curl -s -X POST \
    "https://graph.facebook.com/v19.0/${pageid}/picture" \
    -d "url=${LOGO_URL}" \
    -d "access_token=${TOKEN_DE_FACEBOOK}")
  
  # Analizar respuesta
  if echo "$RESPONSE" | grep -q '"success"'; then
    echo -e "   ${GREEN}✅ Foto de perfil actualizada${NC}"
    SUCCESS=$((SUCCESS + 1))
  elif echo "$RESPONSE" | grep -q '"id"'; then
    echo -e "   ${GREEN}✅ Foto subida exitosamente${NC}"
    SUCCESS=$((SUCCESS + 1))
  else
    ERROR_MSG=$(echo "$RESPONSE" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    if [ -n "$ERROR_MSG" ]; then
      echo -e "   ${RED}❌ Error: ${ERROR_MSG}${NC}"
    else
      echo -e "   ${RED}❌ Error: ${RESPONSE}${NC}"
    fi
    FAILED=$((FAILED + 1))
  fi
  
  echo ""
  
  # Delay entre peticiones (evitar rate limiting)
  if [ $i -lt $((TOTAL - 1)) ]; then
    echo -e "   ${YELLOW}Esperando 3 segundos...${NC}"
    sleep 3
  fi
done

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Exitosos:  ${SUCCESS}${NC}"
echo -e "${RED}❌ Fallidos:   ${FAILED}${NC}"
echo -e "${YELLOW}⏭️  Saltados:   ${SKIPPED}${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

if [ $FAILED -gt 0 ]; then
  echo -e "${YELLOW}💡 Algunos sitios fallaron. Posibles causas:${NC}"
  echo "   - Token expirado o inválido"
  echo "   - Page ID incorrecto"
  echo "   - Permisos insuficientes"
  echo ""
  echo "   Genera un nuevo token en:"
  echo "   https://developers.facebook.com/tools/explorer/"
  echo ""
fi

echo "✅ Proceso completado"
