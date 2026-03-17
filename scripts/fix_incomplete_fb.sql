-- Script de EMERGENCIA para corregir artículos incompletos
-- Ejecutar: wrangler d1 execute news_db --file scripts/fix_incomplete_fb.sql --remote

-- 1. Establecer FB_PUBLICADO = 0 en artículos incompletos para que se completen
UPDATE ARTICULOS_PARAFRASEADOS
SET FB_PUBLICADO = 0
WHERE FB_PUBLICADO = 1
  AND FB_SITIOS_PUBLICADOS != SITIO_DESTINO
  AND FB_SITIOS_PUBLICADOS != '';

-- 2. Lo mismo para CMS
UPDATE ARTICULOS_CMS
SET FB_PUBLICADO = 0
WHERE FB_PUBLICADO = 1
  AND FB_SITIOS_PUBLICADOS != SITIOS_DESTINO
  AND FB_SITIOS_PUBLICADOS != '';

-- 3. Verificar resultados
SELECT 
  'ARTICULOS_PARAFRASEADOS' as tabla,
  COUNT(*) as corregidos
FROM ARTICULOS_PARAFRASEADOS
WHERE FB_PUBLICADO = 0
  AND FB_REQUERIDO = 1
UNION ALL
SELECT 
  'ARTICULOS_CMS' as tabla,
  COUNT(*) as corregidos
FROM ARTICULOS_CMS
WHERE FB_PUBLICADO = 0
  AND FB_REQUERIDO = 1;
