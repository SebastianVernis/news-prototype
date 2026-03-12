#!/bin/bash
# Migración completa de artículos existentes a tablas ARTICULOS_SITIO_{SLUG}
# Ejecutar en lotes para evitar timeouts

DB="news_db"

echo "=== Migración de artículos existentes ==="
echo "Fecha: $(date)"
echo ""

# Función para ejecutar migración de un sitio
migrate_site() {
  local slug=$1
  local short_name=$2

  echo "Migrando $slug..."

  wrangler d1 execute $DB --command "
PRAGMA foreign_keys = OFF;

-- Drop existing table
DROP TABLE IF EXISTS ARTICULOS_SITIO_${slug^^};

-- Recreate: todos los artículos están publicados, solo rastrea Facebook
CREATE TABLE ARTICULOS_SITIO_${slug^^} (
  ID TEXT PRIMARY KEY,
  ID_PARAFRASEADO TEXT NOT NULL,
  FB_PUBLICADO INTEGER DEFAULT 0,
  FB_FECHA TEXT,
  FB_POST_ID TEXT,
  FECHA_ASIGNACION TEXT,
  FECHA_CREACION TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sitio_${slug^^}_fb ON ARTICULOS_SITIO_${slug^^}(FB_PUBLICADO);

-- Migrate from PARAFRASEADOS (todos como publicados en web)
INSERT OR IGNORE INTO ARTICULOS_SITIO_${slug^^} (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 'para-' || ID || '-${short_name}', ID, FECHA_PUBLICACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO' AND SITIO_DESTINO LIKE '%${slug}%';

-- Migrate from CMS
INSERT OR IGNORE INTO ARTICULOS_SITIO_${slug^^} (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 'cms-' || ID || '-${short_name}', ID, FECHA_PUBLICACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO' AND SITIOS_DESTINO LIKE '%${slug}%';

-- Count
SELECT '${slug}' as sitio, COUNT(*) as migrados FROM ARTICULOS_SITIO_${slug^^};
" --remote 2>&1 | grep -E "migrados|ERROR" || echo "  ✓ $slug completado"
}

# Sitios estables (10)
echo "=== Migrando sitios estables ==="
migrate_site "radiocinconoticias" "radio"
migrate_site "centralmexico" "central"
migrate_site "tvmexico" "tv"
migrate_site "cbnnoticias" "cbn"
migrate_site "mexicoinformado" "mexinfo"
migrate_site "nodoinformativo" "nodo"
migrate_site "bitacoraurbana" "bitacora"
migrate_site "reportecentralmx" "reporte"
migrate_site "verticenoticias" "vertice"
migrate_site "noticiasobjetivo" "objetivo"

# Nuevos sitios (17)
echo ""
echo "=== Migrando nuevos sitios ==="
migrate_site "boominformativo" "boom"
migrate_site "capitalpress" "capital"
migrate_site "diarioexpress" "diario"
migrate_site "elpulsomexicano" "pulso"
migrate_site "enfoquecapital" "enfocap"
migrate_site "enfoquedirecto" "enfocadir"
migrate_site "formulacdmx" "formula"
migrate_site "mexicantimes" "mextimes"
migrate_site "mexico360noticias" "mex360"
migrate_site "mradio" "mradio"
migrate_site "noticiashorizonte" "horizonte"
migrate_site "pulsodiario" "pulsodia"
migrate_site "puntoclave" "puntocla"
migrate_site "puntonoticias" "punto"
migrate_site "radarinformativo" "radar"
migrate_site "reportediario" "repodia"
migrate_site "televisionabc" "teleabc"

echo ""
echo "=== Migración completada ==="
echo "Fecha: $(date)"
