-- Script para limpiar artículos corruptos en la base de datos
-- Elimina: Google Tag scripts, CSS corrupto, caracteres especiales ()

-- 1. Limpiar ARTICULOS_PARAFRASEADOS
-- Eliminar Google Tag Manager scripts
UPDATE ARTICULOS_PARAFRASEADOS 
SET CONTENIDO = REPLACE(
  REPLACE(
    REPLACE(
      REPLACE(CONTENIDO, 
        'googletag.cmd.push(function() { googletag.display(', ''),
      '});', ''),
    'googletag.display(', ''),
  '});', '')
WHERE CONTENIDO LIKE '%googletag%';

-- 2. Limpiar ARTICULOS_CMS
UPDATE ARTICULOS_CMS 
SET CONTENIDO = REPLACE(
  REPLACE(
    REPLACE(
      REPLACE(CONTENIDO, 
        'googletag.cmd.push(function() { googletag.display(', ''),
      '});', ''),
    'googletag.display(', ''),
  '});', '')
WHERE CONTENIDO LIKE '%googletag%';

-- Verificar limpieza
SELECT COUNT(*) as corruptos_restantes_para 
FROM ARTICULOS_PARAFRASEADOS 
WHERE CONTENIDO LIKE '%googletag%' 
   OR CONTENIDO LIKE '%div-gpt-ad%';

SELECT COUNT(*) as corruptos_restantes_cms 
FROM ARTICULOS_CMS 
WHERE CONTENIDO LIKE '%googletag%' 
   OR CONTENIDO LIKE '%div-gpt-ad%';
