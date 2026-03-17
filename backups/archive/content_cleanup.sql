-- ============================================================
-- LIMPIEZA DE CONTENIDO - ORTOGRAFÍA Y RUBROS
-- Elimina contenido remanente, duplicados y problemas de formato
-- ============================================================

-- 1. Eliminar artículos con títulos que comienzan con espacios o caracteres especiales
DELETE FROM ARTICULOS_ORIGINALES 
WHERE TITULO LIKE ' %' 
   OR TITULO LIKE ' %'
   OR TITULO LIKE '%|%';

-- 2. Eliminar artículos con títulos que son solo boletines genéricos
DELETE FROM ARTICULOS_ORIGINALES 
WHERE TITULO LIKE '%BOLETÍN%' 
   AND DESCRIPCION IS NULL;

-- 3. Eliminar artículos con títulos vacíos o muy cortos (< 10 caracteres)
DELETE FROM ARTICULOS_ORIGINALES 
WHERE LENGTH(TRIM(TITULO)) < 10;

-- 4. Eliminar artículos con descripciones que contienen HTML no procesado
DELETE FROM ARTICULOS_ORIGINALES 
WHERE DESCRIPCION LIKE '%&lt;%' 
   OR DESCRIPCION LIKE '%&gt;%';

-- 5. Limpiar espacios dobles en títulos
UPDATE ARTICULOS_ORIGINALES 
SET TITULO = TRIM(REPLACE(TITULO, '  ', ' '))
WHERE TITULO LIKE '%  %';

-- 6. Limpiar títulos que comienzan con espacios
UPDATE ARTICULOS_ORIGINALES 
SET TITULO = TRIM(TITULO)
WHERE TITULO LIKE ' %';

-- 7. Eliminar artículos PARAFRASEADOS con títulos problemáticos
DELETE FROM ARTICULOS_PARAFRASEADOS 
WHERE LENGTH(TRIM(TITULO_PARAFRASEADO)) < 10
   OR TITULO_PARAFRASEADO LIKE '%|%';

-- 8. Limpiar descripciones parafraseadas con HTML
UPDATE ARTICULOS_PARAFRASEADOS 
SET DESCRIPCION_PARAFRASEADA = REPLACE(REPLACE(DESCRIPCION_PARAFRASEADA, '&lt;', '<'), '&gt;', '>')
WHERE DESCRIPCION_PARAFRASEADA LIKE '%&lt;%' OR DESCRIPCION_PARAFRASEADA LIKE '%&gt;%';

-- 9. Eliminar REVISION_CONTENIDO aprobados (ya fueron publicados)
DELETE FROM REVISION_CONTENIDO 
WHERE ESTADO = 'APROBADO';

-- 10. Eliminar REVISION_CONTENIDO con títulos vacíos
DELETE FROM REVISION_CONTENIDO 
WHERE LENGTH(TRIM(TITULO_PROPUESTO)) < 10;

-- 11. Verificar resultado
SELECT 'ARTICULOS_ORIGINALES' as tabla, COUNT(*) as registros FROM ARTICULOS_ORIGINALES
UNION ALL SELECT 'ARTICULOS_PARAFRASEADOS', COUNT(*) FROM ARTICULOS_PARAFRASEADOS
UNION ALL SELECT 'REVISION_CONTENIDO', COUNT(*) FROM REVISION_CONTENIDO;

-- 12. Mostrar artículos con posibles problemas restantes
SELECT ID, substr(TITULO, 1, 60) as TITULO, LENGTH(TITULO) as largo
FROM ARTICULOS_ORIGINALES 
WHERE LENGTH(TRIM(TITULO)) < 20
ORDER BY largo;
