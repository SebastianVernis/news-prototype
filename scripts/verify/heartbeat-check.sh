#!/bin/bash
# Verificación de heartbeat para cloudflare-news-project
# Revisa estado de publicaciones y envía alerta por Telegram si hay errores

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DATA_DIR="${NEWS_DATA_DIR:-$ROOT_DIR/data}"
LOGS_DIR="$DATA_DIR/logs"
mkdir -p "$LOGS_DIR"

# Configuración
API_URL="https://news-api.sebastianvernis.workers.dev/api"
TOKEN="17f616e5c86c4988d2f6a6955ba9a98bc3c7ddda4c3557286ba3b80f8aa76291"
TELEGRAM_CHAT_ID="-1002508776650"  # Canal/Chat de alertas
BOT_TOKEN="8050461185:AAF91pG2ugi5ij2235Y2fl6cKQ6nd9LehTM"

ERRORS=()
WARNINGS=()

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

send_telegram_alert() {
    local message="$1"
    local url="https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"
    
    curl -s -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\":\"${TELEGRAM_CHAT_ID}\",\"text\":\"${message}\",\"parse_mode\":\"Markdown\"}" > /dev/null
}

log "=== Verificación Cloudflare News Project ==="

# 1. Verificar health del API
log "Verificando health del API..."
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/health" 2>/dev/null || echo "000")
HEALTH_CODE=$(echo "$HEALTH_RESPONSE" | tail -1)
HEALTH_BODY=$(echo "$HEALTH_RESPONSE" | head -n -1)

if [ "$HEALTH_CODE" != "200" ]; then
    ERRORS+=("❌ API no responde (HTTP $HEALTH_CODE)")
    log "ERROR: API health falló con código $HEALTH_CODE"
else
    log "✓ API saludable"
fi

# 2. Verificar estado de cron jobs
log "Verificando estado de cron jobs..."
CRON_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/cron/status" \
    -H "Authorization: Bearer ${TOKEN}" 2>/dev/null || echo "000")
CRON_CODE=$(echo "$CRON_RESPONSE" | tail -1)

if [ "$CRON_CODE" != "200" ]; then
    WARNINGS+=("⚠️ No se pudo obtener estado de cron jobs")
    log "WARNING: No se pudo obtener estado de cron"
else
    log "✓ Estado de cron obtenido"
fi

# 3. Verificar últimas publicaciones de Facebook
log "Verificando publicaciones recientes en Facebook..."
FB_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/facebook/monitor" \
    -H "Authorization: Bearer ${TOKEN}" 2>/dev/null || echo "000")
FB_CODE=$(echo "$FB_RESPONSE" | tail -1)

if [ "$FB_CODE" != "200" ]; then
    WARNINGS+=("⚠️ No se pudo obtener monitor de Facebook")
    log "WARNING: No se pudo obtener monitor de Facebook"
else
    # Verificar si hay errores recientes en la respuesta
    if echo "$FB_RESPONSE" | grep -q '"error"'; then
        WARNINGS+=("⚠️ Errores detectados en publicaciones de Facebook")
        log "WARNING: Errores en publicaciones de Facebook"
    else
        log "✓ Publicaciones de Facebook sin errores"
    fi
fi

# 4. Verificar artículos pendientes de revisión
log "Verificando artículos pendientes de revisión..."
PENDING_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/revision/pending" \
    -H "Authorization: Bearer ${TOKEN}" 2>/dev/null || echo "000")
PENDING_CODE=$(echo "$PENDING_RESPONSE" | tail -1)

if [ "$PENDING_CODE" != "200" ]; then
    WARNINGS+=("⚠️ No se pudo obtener artículos pendientes")
    log "WARNING: No se pudo obtener artículos pendientes"
else
    PENDING_COUNT=$(echo "$PENDING_RESPONSE" | head -n -1 | grep -o '"count":[0-9]*' | cut -d: -f2 || echo "0")
    log "✓ Artículos pendientes: ${PENDING_COUNT:-0}"
fi

# Resumen
log "=== Resumen ==="
log "Errores: ${#ERRORS[@]}"
log "Warnings: ${#WARNINGS[@]}"

if [ ${#ERRORS[@]} -gt 0 ]; then
    log "❌ HAY ERRORES CRÍTICOS"
    
    # Construir mensaje de alerta
    ALERT_MSG="🚨 *ALERTA CRÍTICA - Cloudflare News Project*\n\n"
    ALERT_MSG+="*Errores detectados:*\n"
    for error in "${ERRORS[@]}"; do
        ALERT_MSG+="$error\n"
    done
    
    if [ ${#WARNINGS[@]} -gt 0 ]; then
        ALERT_MSG+="\n*Warnings:*\n"
        for warning in "${WARNINGS[@]}"; do
            ALERT_MSG+="$warning\n"
        done
    fi
    
    ALERT_MSG+="\n_Fecha: $(date '+%Y-%m-%d %H:%M:%S CST')_"
    
    log "Enviando alerta por Telegram..."
    send_telegram_alert "$ALERT_MSG"
    log "✓ Alerta enviada"
    
    exit 1
elif [ ${#WARNINGS[@]} -gt 0 ]; then
    log "⚠️ HAY WARNINGS (sin errores críticos)"
    # Opcional: enviar warning por Telegram también
    exit 0
else
    log "✓ Todo operativo"
    exit 0
fi
