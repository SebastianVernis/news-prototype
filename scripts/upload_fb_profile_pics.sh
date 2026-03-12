#!/bin/bash
# Script para subir logos como foto de perfil en Facebook
# Solo para los 17 SITIOS NUEVOS
#
# Uso: ./upload_fb_profile_pics.sh
#
# Requisitos:
# - Tener los tokens de Facebook (generar en Graph API Explorer)
# - curl instalado

echo "📋 Script para subir fotos de perfil a Facebook"
echo "   Solo para los 17 SITIOS NUEVOS"
echo ""
echo "⚠️  IMPORTANTE: Necesitas los tokens de acceso de Facebook"
echo "   Genera tokens en: https://developers.facebook.com/tools/explorer/"
echo "   Perfiles requeridos: pages_manage_posts, pages_read_engagement"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Lista de los 17 SITIOS NUEVOS con sus dominios y Page IDs
# NOTA: Debes verificar/actualizar los Page IDs y tokens
declare -A SITES=(
  ["boominformativo"]="boominformativo.top:61568203340617:TOKEN_AQUI"
  ["capitalpress"]="capitalpress.lat:PENDIENTE:TOKEN_AQUI"
  ["diarioexpress"]="diarioexpress.click:PENDIENTE:TOKEN_AQUI"
  ["elpulsomexicano"]="elpulsomexicano.lat:PENDIENTE:TOKEN_AQUI"
  ["enfoquecapital"]="enfoquecapital.top:PENDIENTE:TOKEN_AQUI"
  ["enfoquedirecto"]="enfoquedirecto.lat:PENDIENTE:TOKEN_AQUI"
  ["formulacdmx"]="formulacdmx.top:PENDIENTE:TOKEN_AQUI"
  ["mexicantimes"]="mexicantimes.top:PENDIENTE:TOKEN_AQUI"
  ["mexico360noticias"]="mexico360noticias.click:PENDIENTE:TOKEN_AQUI"
  ["mradio"]="mradio.lat:PENDIENTE:TOKEN_AQUI"
  ["noticiashorizonte"]="noticiashorizonte.click:PENDIENTE:TOKEN_AQUI"
  ["pulsodiario"]="pulsodiario.lat:PENDIENTE:TOKEN_AQUI"
  ["puntoclave"]="puntoclave.lat:PENDIENTE:TOKEN_AQUI"
  ["puntonoticias"]="puntonoticias.website:PENDIENTE:TOKEN_AQUI"
  ["radarinformativo"]="radarinformativo.online:PENDIENTE:TOKEN_AQUI"
  ["reportediario"]="reportediario.online:PENDIENTE:TOKEN_AQUI"
  ["televisionabc"]="televisionabc.lat:PENDIENTE:TOKEN_AQUI"
)

echo "Sitios a procesar: ${#SITES[@]}"
echo ""

for site in "${!SITES[@]}"; do
  IFS=':' read -r domain pageid token <<< "${SITES[$site]}"
  
  LOGO_URL="https://www.${domain}/logo.png"
  
  echo -e "${YELLOW}📤 ${site}${NC}"
  echo "   Logo: ${LOGO_URL}"
  echo "   Page ID: ${pageid}"
  
  if [ "$pageid" == "PENDIENTE" ]; then
    echo -e "   ${RED}⏭️  SKIP: Page ID pendiente${NC}"
    echo ""
    continue
  fi
  
  if [ "$token" == "TOKEN_AQUI" ]; then
    echo -e "   ${RED}⏭️  SKIP: Token no configurado${NC}"
    echo ""
    continue
  fi
  
  # Subir foto de perfil usando Graph API
  # Método: POST /{page-id}/picture con parámetro url
  RESPONSE=$(curl -s -X POST \
    "https://graph.facebook.com/v19.0/${pageid}/picture" \
    -d "url=${LOGO_URL}" \
    -d "access_token=${token}")
  
  # Verificar respuesta
  if echo "$RESPONSE" | grep -q '"success"'; then
    echo -e "   ${GREEN}✅ Foto de perfil actualizada${NC}"
  elif echo "$RESPONSE" | grep -q '"id"'; then
    echo -e "   ${GREEN}✅ Foto subida (ID: ${RESPONSE})${NC}"
  else
    echo -e "   ${RED}❌ Error: ${RESPONSE}${NC}"
  fi
  
  echo ""
  
  # Delay para no saturar API
  sleep 2
done

echo "─────────────────────────────────────────"
echo "✅ Proceso completado"
echo ""
echo "📌 Si algunos sitios fallaron:"
echo "   1. Verifica que el Page ID sea correcto"
echo "   2. Genera un nuevo token en Graph API Explorer"
echo "   3. Asegúrate que el logo sea accesible públicamente"
echo ""
