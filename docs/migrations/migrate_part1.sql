-- Migración de artículos existentes a nuevas tablas ARTICULOS_SITIO_{SLUG}
-- Fecha: 2026-03-10
-- Objetivo: Migrar artículos existentes de ARTICULOS_PARAFRASEADOS y ARTICULOS_CMS
-- a las 27 tablas ARTICULOS_SITIO_{SLUG} individuales

-- ============================================================
-- 1. ARTICULOS_PARAFRASEADOS → ARTICULOS_SITIO_{SLUG}
-- ============================================================

-- Para cada artículo en PARAFRASEADOS, crear entradas en las tablas de sitio correspondientes
-- Usamos una función auxiliar para parsear el string SITIO_DESTINO

-- Nota: SQLite no tiene split nativo, usamos un approach diferente
-- Primero obtenemos todos los sitios únicos

-- Crear tabla temporal para mapeo de sitios
CREATE TEMPORARY TABLE IF NOT EXISTS TEMP_SITIOS (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL
);

-- Limpiar tabla temporal
DELETE FROM TEMP_SITIOS;

-- Insertar sitios conocidos
INSERT INTO TEMP_SITIOS (slug) VALUES 
  ('radiocinconoticias'), ('centralmexico'), ('tvmexico'), ('cbnnoticias'),
  ('mexicoinformado'), ('nodoinformativo'), ('bitacoraurbana'), ('reportecentralmx'),
  ('verticenoticias'), ('noticiasobjetivo'), ('boominformativo'), ('capitalpress'),
  ('diarioexpress'), ('elpulsomexicano'), ('enfoquecapital'), ('enfoquedirecto'),
  ('formulacdmx'), ('mexicantimes'), ('mexico360noticias'), ('mradio'),
  ('noticiashorizonte'), ('pulsodiario'), ('puntoclave'), ('puntonoticias'),
  ('radarinformativo'), ('reportediario'), ('televisionabc');

-- ============================================================
-- Migración para cada sitio individualmente
-- ============================================================

-- 1. RADIOCINCONOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_RADIOCINCONOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%radiocinconoticias%';

-- 2. CENTRALMEXICO
INSERT OR IGNORE INTO ARTICULOS_SITIO_CENTRALMEXICO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%centralmexico%';

-- 3. TVMEXICO
INSERT OR IGNORE INTO ARTICULOS_SITIO_TVMEXICO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%tvmexico%';

-- 4. CBNNOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_CBNNOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%cbnnoticias%';

-- 5. MEXICOINFORMADO
INSERT OR IGNORE INTO ARTICULOS_SITIO_MEXICOINFORMADO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%mexicoinformado%';

-- 6. NODOINFORMATIVO
INSERT OR IGNORE INTO ARTICULOS_SITIO_NODOINFORMATIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%nodoinformativo%';

-- 7. BITACORAURBANA
INSERT OR IGNORE INTO ARTICULOS_SITIO_BITACORAURBANA (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
