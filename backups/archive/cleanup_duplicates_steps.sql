-- Limpieza de duplicados en ARTICULOS_ORIGINALES
-- Ejecutar en pasos para evitar errores de foreign keys

-- PASO 1: Ver duplicados
SELECT 
    TITULO, 
    COUNT(*) as cantidad,
    GROUP_CONCAT(ID || ':' || CASE WHEN URL_IMAGEN IS NOT NULL AND URL_IMAGEN != '' AND URL_IMAGEN NOT LIKE '%/logo.png' THEN 'CON_IMAGEN' ELSE 'SIN_IMAGEN' END) as estado
FROM ARTICULOS_ORIGINALES
GROUP BY TITULO
HAVING COUNT(*) > 1
ORDER BY cantidad DESC
LIMIT 20;

-- PASO 2: Identificar IDs a eliminar (los que NO tienen imagen o son más antiguos)
-- Guardar estos IDs en una tabla temporal
CREATE TEMP TABLE IF NOT EXISTS ids_a_eliminar AS
SELECT a.ID
FROM ARTICULOS_ORIGINALES a
WHERE EXISTS (
    SELECT 1 FROM ARTICULOS_ORIGINALES b
    WHERE b.TITULO = a.TITULO
    AND b.ID != a.ID
    AND (
        -- El otro tiene imagen válida y este no
        (b.URL_IMAGEN IS NOT NULL AND b.URL_IMAGEN != '' AND b.URL_IMAGEN NOT LIKE '%/logo.png'
         AND (a.URL_IMAGEN IS NULL OR a.URL_IMAGEN = '' OR a.URL_IMAGEN LIKE '%/logo.png'))
        OR
        -- Ambos sin imagen válida, mantener el más reciente
        ((a.URL_IMAGEN IS NULL OR a.URL_IMAGEN = '' OR a.URL_IMAGEN LIKE '%/logo.png')
         AND (b.URL_IMAGEN IS NULL OR b.URL_IMAGEN = '' OR b.URL_IMAGEN LIKE '%/logo.png')
         AND a.FECHA < b.FECHA)
        OR
        -- Ambos con imagen válida, mantener el más reciente
        (a.URL_IMAGEN IS NOT NULL AND a.URL_IMAGEN != '' AND a.URL_IMAGEN NOT LIKE '%/logo.png'
         AND b.URL_IMAGEN IS NOT NULL AND b.URL_IMAGEN != '' AND b.URL_IMAGEN NOT LIKE '%/logo.png'
         AND a.FECHA < b.FECHA)
    )
);

-- Ver cuántos IDs se van a eliminar
SELECT COUNT(*) as ids_a_eliminar FROM ids_a_eliminar;

-- PASO 3: Eliminar referencias en REVISION_CONTENIDO
DELETE FROM REVISION_CONTENIDO WHERE ID_ORIGEN IN (SELECT ID FROM ids_a_eliminar);

-- PASO 4: Eliminar duplicados en ARTICULOS_ORIGINALES
DELETE FROM ARTICULOS_ORIGINALES WHERE ID IN (SELECT ID FROM ids_a_eliminar);

-- PASO 5: Limpiar tabla temporal
DROP TABLE IF EXISTS ids_a_eliminar;

-- PASO 6: Verificar resultado
SELECT 
    TITULO, 
    COUNT(*) as cantidad
FROM ARTICULOS_ORIGINALES
GROUP BY TITULO
HAVING COUNT(*) > 1
LIMIT 10;

-- Total final
SELECT COUNT(*) as total_articulos FROM ARTICULOS_ORIGINALES;
