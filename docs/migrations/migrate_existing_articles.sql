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
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%bitacoraurbana%';

-- 8. REPORTECENTRALMX
INSERT OR IGNORE INTO ARTICULOS_SITIO_REPORTECENTRALMX (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%reportecentralmx%';

-- 9. VERTICENOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_VERTICENOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%verticenoticias%';

-- 10. NOTICIASOBJETIVO
INSERT OR IGNORE INTO ARTICULOS_SITIO_NOTICIASOBJETIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%noticiasobjetivo%';

-- 11. BOOMINFORMATIVO
INSERT OR IGNORE INTO ARTICULOS_SITIO_BOOMINFORMATIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%boominformativo%';

-- 12. CAPITALPRESS
INSERT OR IGNORE INTO ARTICULOS_SITIO_CAPITALPRESS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%capitalpress%';

-- 13. DIARIOEXPRESS
INSERT OR IGNORE INTO ARTICULOS_SITIO_DIARIOEXPRESS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%diarioexpress%';

-- 14. ELPULSOMEXICANO
INSERT OR IGNORE INTO ARTICULOS_SITIO_ELPULSOMEXICANO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%elpulsomexicano%';

-- 15. ENFOQUECAPITAL
INSERT OR IGNORE INTO ARTICULOS_SITIO_ENFOQUECAPITAL (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%enfoquecapital%';

-- 16. ENFOQUEDIRECTO
INSERT OR IGNORE INTO ARTICULOS_SITIO_ENFOQUEDIRECTO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%enfoquedirecto%';

-- 17. FORMULACDMX
INSERT OR IGNORE INTO ARTICULOS_SITIO_FORMULACDMX (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%formulacdmx%';

-- 18. MEXICANTIMES
INSERT OR IGNORE INTO ARTICULOS_SITIO_MEXICANTIMES (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%mexicantimes%';

-- 19. MEXICO360NOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_MEXICO360NOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%mexico360noticias%';

-- 20. MRADIO
INSERT OR IGNORE INTO ARTICULOS_SITIO_MRADIO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%mradio%';

-- 21. NOTICIASHORIZONTE
INSERT OR IGNORE INTO ARTICULOS_SITIO_NOTICIASHORIZONTE (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%noticiashorizonte%';

-- 22. PULSODIARIO
INSERT OR IGNORE INTO ARTICULOS_SITIO_PULSODIARIO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%pulsodiario%';

-- 23. PUNTOCLAVE
INSERT OR IGNORE INTO ARTICULOS_SITIO_PUNTOCLAVE (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%puntoclave%';

-- 24. PUNTONOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_PUNTONOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%puntonoticias%';

-- 25. RADARINFORMATIVO
INSERT OR IGNORE INTO ARTICULOS_SITIO_RADARINFORMATIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%radarinformativo%';

-- 26. REPORTEDIARIO
INSERT OR IGNORE INTO ARTICULOS_SITIO_REPORTEDIARIO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%reportediario%';

-- 27. TELEVISIONABC
INSERT OR IGNORE INTO ARTICULOS_SITIO_TELEVISIONABC (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_PARAFRASEADOS
WHERE ESTADO = 'PUBLICADO'
  AND SITIO_DESTINO LIKE '%televisionabc%';

-- ============================================================
-- 2. ARTICULOS_CMS → ARTICULOS_SITIO_{SLUG}
-- ============================================================

-- 1. RADIOCINCONOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_RADIOCINCONOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%radiocinconoticias%';

-- 2. CENTRALMEXICO
INSERT OR IGNORE INTO ARTICULOS_SITIO_CENTRALMEXICO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%centralmexico%';

-- 3. TVMEXICO
INSERT OR IGNORE INTO ARTICULOS_SITIO_TVMEXICO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%tvmexico%';

-- 4. CBNNOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_CBNNOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%cbnnoticias%';

-- 5. MEXICOINFORMADO
INSERT OR IGNORE INTO ARTICULOS_SITIO_MEXICOINFORMADO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%mexicoinformado%';

-- 6. NODOINFORMATIVO
INSERT OR IGNORE INTO ARTICULOS_SITIO_NODOINFORMATIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%nodoinformativo%';

-- 7. BITACORAURBANA
INSERT OR IGNORE INTO ARTICULOS_SITIO_BITACORAURBANA (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%bitacoraurbana%';

-- 8. REPORTECENTRALMX
INSERT OR IGNORE INTO ARTICULOS_SITIO_REPORTECENTRALMX (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%reportecentralmx%';

-- 9. VERTICENOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_VERTICENOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%verticenoticias%';

-- 10. NOTICIASOBJETIVO
INSERT OR IGNORE INTO ARTICULOS_SITIO_NOTICIASOBJETIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%noticiasobjetivo%';

-- 11. BOOMINFORMATIVO
INSERT OR IGNORE INTO ARTICULOS_SITIO_BOOMINFORMATIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%boominformativo%';

-- 12. CAPITALPRESS
INSERT OR IGNORE INTO ARTICULOS_SITIO_CAPITALPRESS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%capitalpress%';

-- 13. DIARIOEXPRESS
INSERT OR IGNORE INTO ARTICULOS_SITIO_DIARIOEXPRESS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%diarioexpress%';

-- 14. ELPULSOMEXICANO
INSERT OR IGNORE INTO ARTICULOS_SITIO_ELPULSOMEXICANO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%elpulsomexicano%';

-- 15. ENFOQUECAPITAL
INSERT OR IGNORE INTO ARTICULOS_SITIO_ENFOQUECAPITAL (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%enfoquecapital%';

-- 16. ENFOQUEDIRECTO
INSERT OR IGNORE INTO ARTICULOS_SITIO_ENFOQUEDIRECTO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%enfoquedirecto%';

-- 17. FORMULACDMX
INSERT OR IGNORE INTO ARTICULOS_SITIO_FORMULACDMX (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%formulacdmx%';

-- 18. MEXICANTIMES
INSERT OR IGNORE INTO ARTICULOS_SITIO_MEXICANTIMES (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%mexicantimes%';

-- 19. MEXICO360NOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_MEXICO360NOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%mexico360noticias%';

-- 20. MRADIO
INSERT OR IGNORE INTO ARTICULOS_SITIO_MRADIO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%mradio%';

-- 21. NOTICIASHORIZONTE
INSERT OR IGNORE INTO ARTICULOS_SITIO_NOTICIASHORIZONTE (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%noticiashorizonte%';

-- 22. PULSODIARIO
INSERT OR IGNORE INTO ARTICULOS_SITIO_PULSODIARIO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%pulsodiario%';

-- 23. PUNTOCLAVE
INSERT OR IGNORE INTO ARTICULOS_SITIO_PUNTOCLAVE (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%puntoclave%';

-- 24. PUNTONOTICIAS
INSERT OR IGNORE INTO ARTICULOS_SITIO_PUNTONOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%puntonoticias%';

-- 25. RADARINFORMATIVO
INSERT OR IGNORE INTO ARTICULOS_SITIO_RADARINFORMATIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%radarinformativo%';

-- 26. REPORTEDIARIO
INSERT OR IGNORE INTO ARTICULOS_SITIO_REPORTEDIARIO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%reportediario%';

-- 27. TELEVISIONABC
INSERT OR IGNORE INTO ARTICULOS_SITIO_TELEVISIONABC (ID, ID_PARAFRASEADO, FECHA_ASIGNACION)
SELECT 
  lower(hex(randomblob(16))) || '-' || lower(hex(randomblob(4))) || '-' || '4' || substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab',abs(random())%4+1,1) || substr(lower(hex(randomblob(6))), 2) as ID,
  ID as ID_PARAFRASEADO,
  FECHA_PUBLICACION as FECHA_ASIGNACION
FROM ARTICULOS_CMS
WHERE ESTADO = 'PUBLICADO'
  AND SITIOS_DESTINO LIKE '%televisionabc%';

-- ============================================================
-- 3. Verificación final
-- ============================================================

-- Contar registros migrados por sitio
SELECT 'ARTICULOS_SITIO_*' as tabla, COUNT(*) as total_migrados
FROM (
  SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_CENTRALMEXICO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_TVMEXICO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_CBNNOTICIAS
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_MEXICOINFORMADO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_NODOINFORMATIVO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_BITACORAURBANA
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_REPORTECENTRALMX
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_VERTICENOTICIAS
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_NOTICIASOBJETIVO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_BOOMINFORMATIVO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_CAPITALPRESS
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_DIARIOEXPRESS
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_ELPULSOMEXICANO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_ENFOQUECAPITAL
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_ENFOQUEDIRECTO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_FORMULACDMX
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_MEXICANTIMES
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_MEXICO360NOTICIAS
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_MRADIO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_NOTICIASHORIZONTE
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_PULSODIARIO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_PUNTOCLAVE
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_PUNTONOTICIAS
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_RADARINFORMATIVO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_REPORTEDIARIO
  UNION ALL SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_TELEVISIONABC
);

-- Limpiar tabla temporal
DROP TABLE IF EXISTS TEMP_SITIOS;
