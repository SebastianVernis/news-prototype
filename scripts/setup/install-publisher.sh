#!/bin/bash

# Script de instalación del sistema de publicación automática
# Configura cron jobs para publicar 1 noticia por hora

echo "🚀 INSTALANDO SISTEMA DE PUBLICACIÓN AUTOMÁTICA"
echo "================================================"
echo ""

# Determinar raíz del repo
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DATA_DIR="${NEWS_DATA_DIR:-$ROOT_DIR/data}"
RUNNER_PATH="$ROOT_DIR/scripts/run/run-publisher.sh"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado. Instalando..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip3 install requests beautifulsoup4 python-dotenv --break-system-packages 2>/dev/null || pip3 install requests beautifulsoup4 python-dotenv

# Crear archivo .env si no existe
if [ ! -f "$ROOT_DIR/.env" ]; then
    echo "📝 Creando archivo .env..."
    cat > "$ROOT_DIR/.env" << EOF
# API Keys
NEWSAPI_KEY=YOUR_NEWSAPI_KEY
BLACKBOX_API_KEY=

# Configuración
PUBLISHER_TOKEN=publisher_secret_token_2026
EOF
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p "$DATA_DIR/news_queue"
mkdir -p "$DATA_DIR/published_news"
mkdir -p "$DATA_DIR/logs"

# Configurar cron job
echo "⏰ Configurando cron job..."

# Crear script wrapper
cat > "$RUNNER_PATH" << 'EOF'
#!/bin/bash
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DATA_DIR="${NEWS_DATA_DIR:-$ROOT_DIR/data}"
LOGS_DIR="$DATA_DIR/logs"

mkdir -p "$LOGS_DIR"
cd "$ROOT_DIR"
python3 tools/news/news-publisher.py publish >> "$LOGS_DIR/cron_$(date +%Y%m%d).log" 2>&1
EOF

chmod +x "$RUNNER_PATH"

# Agregar cron job (publicar cada hora en el minuto 0)
CRON_JOB="0 * * * * $RUNNER_PATH"

# Verificar si ya existe el cron job
if crontab -l 2>/dev/null | grep -q "run-publisher.sh"; then
    echo "✅ Cron job ya existe"
else
    # Agregar cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job agregado: Publica cada hora"
fi

# Crear servicio systemd (opcional, para sistemas con systemd)
if [ -d "/etc/systemd/system" ]; then
    echo "🔧 Creando servicio systemd..."
    
    cat > /etc/systemd/system/news-publisher.service << EOF
[Unit]
Description=News Publisher Scheduler
After=network.target

[Service]
Type=simple
User=sebastianvernis
WorkingDirectory=$ROOT_DIR
ExecStart=/usr/bin/python3 $ROOT_DIR/tools/news/news-publisher.py run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Habilitar servicio
    systemctl daemon-reload
    systemctl enable news-publisher.service
    
    echo "✅ Servicio systemd creado"
    echo "   Comandos:"
    echo "   - Iniciar: sudo systemctl start news-publisher"
    echo "   - Detener: sudo systemctl stop news-publisher"
    echo "   - Estado: sudo systemctl status news-publisher"
    echo "   - Logs: sudo journalctl -u news-publisher -f"
fi

# Mostrar instrucciones
echo ""
echo "================================================"
echo "✅ INSTALACIÓN COMPLETADA"
echo "================================================"
echo ""
echo "📋 COMANDOS DISPONIBLES:"
echo ""
echo "1. Publicar noticia manualmente:"
echo "   cd $ROOT_DIR"
echo "   python3 tools/news/news-publisher.py publish"
echo ""
echo "2. Ver estado del sistema:"
echo "   python3 tools/news/news-publisher.py status"
echo ""
echo "3. Ver cola de noticias:"
echo "   python3 tools/news/news-publisher.py queue"
echo ""
echo "4. Agregar noticias a la cola:"
echo "   python3 tools/news/news-publisher.py add \"México\" 20"
echo ""
echo "5. Ejecutar scheduler continuo:"
echo "   python3 tools/news/news-publisher.py run"
echo ""
echo "⏰ CRON JOB CONFIGURADO:"
echo "   - Publica: Cada hora (minuto 0)"
echo "   - Logs: $DATA_DIR/logs/"
echo ""
echo "📊 ARCHIVOS DE CONTROL:"
echo "   - Cola: $DATA_DIR/news_queue/news_queue.json"
echo "   - Publicadas: $DATA_DIR/published_news/published_news.json"
echo "   - Config: $DATA_DIR/publisher_config.json"
echo ""
echo "🔧 PARA DESINSTALAR:"
echo "   crontab -e  # Remover la línea del cron job"
echo "   sudo systemctl stop news-publisher  # Si usas systemd"
echo "   sudo systemctl disable news-publisher"
echo ""
echo "================================================"
