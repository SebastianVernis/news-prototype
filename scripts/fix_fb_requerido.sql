-- Script para actualizar FB_REQUERIDO = 1 en artículos recientes
-- Ejecutar: wrangler d1 execute news_db --file scripts/fix_fb_requerido.sql --remote

-- Actualizar artículos PARAFRASEADOS de los últimos 7 días
UPDATE ARTICULOS_PARAFRASEADOS
SET FB_REQUERIDO = 1
WHERE FB_REQUERIDO = 0
  AND ESTADO = 'PUBLICADO'
  AND URL_IMAGEN NOT LIKE '%unsplash.com%'
  AND FECHA_PUBLICACION >= datetime('now', '-7 days');

-- Actualizar artículos CMS de los últimos 7 días
UPDATE ARTICULOS_CMS
SET FB_REQUERIDO = 1
WHERE FB_REQUERIDO = 0
  AND ESTADO = 'PUBLICADO'
  AND URL_IMAGEN NOT LIKE '%unsplash.com%'
  AND FECHA_CREACION >= datetime('now', '-7 days');

-- Verificar resultados
SELECT 
  'ARTICULOS_PARAFRASEADOS' as tabla,
  COUNT(*) as actualizados,
  'Ultimos 7 dias' as periodo
FROM ARTICULOS_PARAFRASEADOS
WHERE FB_REQUERIDO = 1
  AND FECHA_PUBLICACION >= datetime('now', '-7 days')
UNION ALL
SELECT 
  'ARTICULOS_CMS' as tabla,
  COUNT(*) as actualizados,
  'Ultimos 7 dias' as periodo
FROM ARTICULOS_CMS
WHERE FB_REQUERIDO = 1
  AND FECHA_CREACION >= datetime('now', '-7 days');
