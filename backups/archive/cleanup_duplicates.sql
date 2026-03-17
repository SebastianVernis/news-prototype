-- Script para eliminar duplicados en ARTICULOS_ORIGINALES
-- Prioriza conservar artículos con URL_IMAGEN válida

-- 1. Ver duplicados existentes
SELECT 
    TITULO, 
    COUNT(*) as cantidad,
    GROUP_CONCAT(ID) as ids,
    GROUP_CONCAT(URL_IMAGEN) as imagenes
FROM ARTICULOS_ORIGINALES
GROUP BY TITULO
HAVING COUNT(*) > 1
ORDER BY cantidad DESC;

-- 2. Identificar qué IDs eliminar (mantener el que tiene imagen válida)
-- Selecciona los IDs a eliminar: duplicados sin imagen o con imagen inválida
SELECT 
    a.ID,
    a.TITULO,
    a.URL_IMAGEN,
    a.FECHA
FROM ARTICULOS_ORIGINALES a
WHERE EXISTS (
    SELECT 1 FROM ARTICULOS_ORIGINALES b
    WHERE b.TITULO = a.TITULO
    AND b.ID != a.ID
    AND (
        -- El otro tiene imagen válida y este no
        (b.URL_IMAGEN IS NOT NULL AND b.URL_IMAGEN != '' AND b.URL_IMAGEN != '/logo.png'
         AND (a.URL_IMAGEN IS NULL OR a.URL_IMAGEN = '' OR a.URL_IMAGEN = '/logo.png'))
        OR
        -- Ambos tienen imagen inválida, mantener el más reciente
        ((a.URL_IMAGEN IS NULL OR a.URL_IMAGEN = '' OR a.URL_IMAGEN = '/logo.png')
         AND (b.URL_IMAGEN IS NULL OR b.URL_IMAGEN = '' OR b.URL_IMAGEN = '/logo.png')
         AND a.FECHA < b.FECHA)
        OR
        -- Ambos tienen imagen válida, mantener el más reciente
        (a.URL_IMAGEN IS NOT NULL AND a.URL_IMAGEN != '' AND a.URL_IMAGEN != '/logo.png'
         AND b.URL_IMAGEN IS NOT NULL AND b.URL_IMAGEN != '' AND b.URL_IMAGEN != '/logo.png'
         AND a.FECHA < b.FECHA)
    )
)
ORDER BY a.TITULO, a.FECHA;

-- 3. Eliminar duplicados (manteniendo el que tiene imagen válida o el más reciente)
DELETE FROM ARTICULOS_ORIGINALES
WHERE ID IN (
    SELECT a.ID
    FROM ARTICULOS_ORIGINALES a
    WHERE EXISTS (
        SELECT 1 FROM ARTICULOS_ORIGINALES b
        WHERE b.TITULO = a.TITULO
        AND b.ID != a.ID
        AND (
            -- El otro tiene imagen válida y este no
            (b.URL_IMAGEN IS NOT NULL AND b.URL_IMAGEN != '' AND b.URL_IMAGEN != '/logo.png'
             AND (a.URL_IMAGEN IS NULL OR a.URL_IMAGEN = '' OR a.URL_IMAGEN = '/logo.png'))
            OR
            -- Ambos tienen imagen inválida, mantener el más reciente
            ((a.URL_IMAGEN IS NULL OR a.URL_IMAGEN = '' OR a.URL_IMAGEN = '/logo.png')
             AND (b.URL_IMAGEN IS NULL OR b.URL_IMAGEN = '' OR b.URL_IMAGEN = '/logo.png')
             AND a.FECHA < b.FECHA)
            OR
            -- Ambos tienen imagen válida, mantener el más reciente
            (a.URL_IMAGEN IS NOT NULL AND a.URL_IMAGEN != '' AND a.URL_IMAGEN != '/logo.png'
             AND b.URL_IMAGEN IS NOT NULL AND b.URL_IMAGEN != '' AND b.URL_IMAGEN != '/logo.png'
             AND a.FECHA < b.FECHA)
        )
    )
);

-- 4. Verificar resultado
SELECT 
    TITULO, 
    COUNT(*) as cantidad,
    URL_IMAGEN
FROM ARTICULOS_ORIGINALES
GROUP BY TITULO
HAVING COUNT(*) > 1;

-- 5. Contar registros restantes
SELECT COUNT(*) as total_registros FROM ARTICULOS_ORIGINALES;
