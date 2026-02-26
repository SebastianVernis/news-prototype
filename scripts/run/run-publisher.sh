#!/bin/bash
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DATA_DIR="${NEWS_DATA_DIR:-$ROOT_DIR/data}"
LOGS_DIR="$DATA_DIR/logs"

mkdir -p "$LOGS_DIR"
cd "$ROOT_DIR"
python3 tools/news/news-publisher.py publish >> "$LOGS_DIR/cron_$(date +%Y%m%d).log" 2>&1
