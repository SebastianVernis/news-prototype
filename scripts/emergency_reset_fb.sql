-- Script de EMERGENCIA para resetear TODOS los timers de Facebook
-- Ejecutar: wrangler d1 execute news_db --file scripts/emergency_reset_fb.sql --remote

-- Nota: Esto NO resetea los timers de KV, solo prepara la DB

-- 1. Verificar artículos con FB_PUBLICADO = 1 pero FB_SITIOS_PUBLICADOS incompleto
SELECT 
  ID,
  TITULO_PARAFRASEADO as TITULO,
  SITIO_DESTINO,
  FB_SITIOS_PUBLICADOS,
  CASE 
    WHEN FB_SITIOS_PUBLICADOS = SITIO_DESTINO THEN 'COMPLETO'
    ELSE 'INCOMPLETO'
  END as ESTADO
FROM ARTICULOS_PARAFRASEADOS
WHERE FB_PUBLICADO = 1
  AND FB_SITIOS_PUBLICADOS != SITIO_DESTINO
LIMIT 20;

-- 2. Contar artículos por estado
SELECT 
  CASE 
    WHEN FB_SITIOS_PUBLICADOS = SITIO_DESTINO THEN 'COMPLETOS'
    ELSE 'INCOMPLETOS'
  END as ESTADO,
  COUNT(*) as total
FROM ARTICULOS_PARAFRASEADOS
WHERE FB_PUBLICADO = 1
GROUP BY 1;
