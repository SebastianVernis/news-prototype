-- Script para asignar artículos huérfanos a sitios (round-robin)
-- Ejecutar: wrangler d1 execute news_db --file assign_orphans.sql --remote

-- Los artículos huérfanos se asignarán al sitio que corresponda por round-robin
-- Basado en el orden de fecha de publicación

-- Nota: Este script solo crea los registros en ARTICULOS_SITIO_*
-- No modifica ARTICULOS_PARAFRASEADOS

-- El script se ejecuta en 27 pasos (uno por sitio)
-- Cada artículo huérfano se asigna a UN solo sitio

-- Paso 1: Crear vista temporal de artículos huérfanos con número de fila
DROP VIEW IF EXISTS orphan_articles;
CREATE TEMP VIEW orphan_articles AS
SELECT 
  ap.ID,
  ap.TITULO_PARAFRASEADO,
  ap.FECHA_PUBLICACION,
  ROW_NUMBER() OVER (ORDER BY ap.FECHA_PUBLICACION DESC) as row_num
FROM ARTICULOS_PARAFRASEADOS ap
WHERE ap.ESTADO = 'PUBLICADO'
AND ap.ID NOT IN (
  SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_CENTRALMEXICO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_TVMEXICO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_CBNNOTICIAS
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_MEXICOINFORMADO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_NODOINFORMATIVO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_BITACORAURBANA
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_REPORTECENTRALMX
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_VERTICENOTICIAS
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_NOTICIASOBJETIVO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_BOOMINFORMATIVO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_CAPITALPRESS
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_DIARIOEXPRESS
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_ELPULSOMEXICANO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_ENFOQUECAPITAL
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_ENFOQUEDIRECTO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_FORMULACDMX
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_MEXICANTIMES
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_MEXICO360NOTICIAS
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_MRADIO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_NOTICIASHORIZONTE
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_PULSODIARIO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_PUNTOCLAVE
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_PUNTONOTICIAS
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_RADARINFORMATIVO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_REPORTEDIARIO
  UNION SELECT ID_PARAFRASEADO FROM ARTICULOS_SITIO_TELEVISIONABC
);

-- Contar huérfanos
SELECT 'Total orphan articles: ' || COUNT(*) FROM orphan_articles;

-- Asignar a radiocinconoticias (row_num % 27 = 1)
INSERT OR IGNORE INTO ARTICULOS_SITIO_RADIOCINCONOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-radio',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 1;

-- Asignar a centralmexico (row_num % 27 = 2)
INSERT OR IGNORE INTO ARTICULOS_SITIO_CENTRALMEXICO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-central',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 2;

-- Asignar a tvmexico (row_num % 27 = 3)
INSERT OR IGNORE INTO ARTICULOS_SITIO_TVMEXICO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-tv',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 3;

-- Asignar a cbnnoticias (row_num % 27 = 4)
INSERT OR IGNORE INTO ARTICULOS_SITIO_CBNNOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-cbn',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 4;

-- Asignar a mexicoinformado (row_num % 27 = 5)
INSERT OR IGNORE INTO ARTICULOS_SITIO_MEXICOINFORMADO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-mexinfo',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 5;

-- Asignar a nodoinformativo (row_num % 27 = 6)
INSERT OR IGNORE INTO ARTICULOS_SITIO_NODOINFORMATIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-nodo',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 6;

-- Asignar a bitacoraurbana (row_num % 27 = 7)
INSERT OR IGNORE INTO ARTICULOS_SITIO_BITACORAURBANA (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-bitacora',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 7;

-- Asignar a reportecentralmx (row_num % 27 = 8)
INSERT OR IGNORE INTO ARTICULOS_SITIO_REPORTECENTRALMX (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-reporte',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 8;

-- Asignar a verticenoticias (row_num % 27 = 9)
INSERT OR IGNORE INTO ARTICULOS_SITIO_VERTICENOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-vertice',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 9;

-- Asignar a noticiasobjetivo (row_num % 27 = 10)
INSERT OR IGNORE INTO ARTICULOS_SITIO_NOTICIASOBJETIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-objetivo',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 10;

-- Asignar a boominformativo (row_num % 27 = 11)
INSERT OR IGNORE INTO ARTICULOS_SITIO_BOOMINFORMATIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-boom',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 11;

-- Asignar a capitalpress (row_num % 27 = 12)
INSERT OR IGNORE INTO ARTICULOS_SITIO_CAPITALPRESS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-capital',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 12;

-- Asignar a diarioexpress (row_num % 27 = 13)
INSERT OR IGNORE INTO ARTICULOS_SITIO_DIARIOEXPRESS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-diario',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 13;

-- Asignar a elpulsomexicano (row_num % 27 = 14)
INSERT OR IGNORE INTO ARTICULOS_SITIO_ELPULSOMEXICANO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-pulso',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 14;

-- Asignar a enfoquecapital (row_num % 27 = 15)
INSERT OR IGNORE INTO ARTICULOS_SITIO_ENFOQUECAPITAL (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-enfocap',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 15;

-- Asignar a enfoquedirecto (row_num % 27 = 16)
INSERT OR IGNORE INTO ARTICULOS_SITIO_ENFOQUEDIRECTO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-enfocadir',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 16;

-- Asignar a formulacdmx (row_num % 27 = 17)
INSERT OR IGNORE INTO ARTICULOS_SITIO_FORMULACDMX (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-formula',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 17;

-- Asignar a mexicantimes (row_num % 27 = 18)
INSERT OR IGNORE INTO ARTICULOS_SITIO_MEXICANTIMES (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-mextimes',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 18;

-- Asignar a mexico360noticias (row_num % 27 = 19)
INSERT OR IGNORE INTO ARTICULOS_SITIO_MEXICO360NOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-mex360',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 19;

-- Asignar a mradio (row_num % 27 = 20)
INSERT OR IGNORE INTO ARTICULOS_SITIO_MRADIO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-mradio',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 20;

-- Asignar a noticiashorizonte (row_num % 27 = 21)
INSERT OR IGNORE INTO ARTICULOS_SITIO_NOTICIASHORIZONTE (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-horizonte',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 21;

-- Asignar a pulsodiario (row_num % 27 = 22)
INSERT OR IGNORE INTO ARTICULOS_SITIO_PULSODIARIO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-pulsodia',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 22;

-- Asignar a puntoclave (row_num % 27 = 23)
INSERT OR IGNORE INTO ARTICULOS_SITIO_PUNTOCLAVE (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-puntocla',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 23;

-- Asignar a puntonoticias (row_num % 27 = 24)
INSERT OR IGNORE INTO ARTICULOS_SITIO_PUNTONOTICIAS (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-punto',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 24;

-- Asignar a radarinformativo (row_num % 27 = 25)
INSERT OR IGNORE INTO ARTICULOS_SITIO_RADARINFORMATIVO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-radar',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 25;

-- Asignar a reportediario (row_num % 27 = 26)
INSERT OR IGNORE INTO ARTICULOS_SITIO_REPORTEDIARIO (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-repodia',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 26;

-- Asignar a televisionabc (row_num % 27 = 0)
INSERT OR IGNORE INTO ARTICULOS_SITIO_TELEVISIONABC (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
SELECT 
  'orphan-' || ID || '-teleabc',
  ID,
  datetime('now'),
  0,
  NULL,
  NULL
FROM orphan_articles
WHERE row_num % 27 = 0;

-- Limpiar vista temporal
DROP VIEW IF EXISTS orphan_articles;

-- Verificar resultado
SELECT 'Artículos asignados exitosamente!' as resultado;
