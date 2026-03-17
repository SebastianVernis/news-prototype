-- Script para actualizar SITIO_DESTINO en todos los artículos
-- Agrega los 17 nuevos sitios a TODOS los artículos existentes
-- Ejecutar con: wrangler d1 execute news_db --file scripts/add_all_sites_to_articles.sql --remote

-- Lista de los 17 nuevos sitios
-- boominformativo, capitalpress, diarioexpress, elpulsomexicano, enfoquecapital, enfoquedirecto, formulacdmx, mexicantimes, mexico360noticias, mradio, noticiashorizonte, pulsodiario, puntoclave, puntonoticias, radarinformativo, reportediario, televisionabc

-- 1. Actualizar ARTICULOS_PARAFRASEADOS
-- Agregar los 17 sitios a cada artículo existente
UPDATE ARTICULOS_PARAFRASEADOS 
SET SITIO_DESTINO = SITIO_DESTINO || ',boominformativo,capitalpress,diarioexpress,elpulsomexicano,enfoquecapital,enfoquedirecto,formulacdmx,mexicantimes,mexico360noticias,mradio,noticiashorizonte,pulsodiario,puntoclave,puntonoticias,radarinformativo,reportediario,televisionabc'
WHERE ESTADO = 'PUBLICADO';

-- 2. Actualizar ARTICULOS_CMS
-- Agregar los 17 sitios a cada artículo publicado existente
UPDATE ARTICULOS_CMS 
SET SITIOS_DESTINO = SITIOS_DESTINO || ',boominformativo,capitalpress,diarioexpress,elpulsomexicano,enfoquecapital,enfoquedirecto,formulacdmx,mexicantimes,mexico360noticias,mradio,noticiashorizonte,pulsodiario,puntoclave,puntonoticias,radarinformativo,reportediario,televisionabc'
WHERE ESTADO = 'PUBLICADO';

-- Verificar cambios
SELECT 'PARAFRASEADOS' as TABLA, COUNT(*) as CANTIDAD, SITIO_DESTINO 
FROM ARTICULOS_PARAFRASEADOS 
WHERE ESTADO = 'PUBLICADO' 
LIMIT 5;

SELECT 'CMS' as TABLA, COUNT(*) as CANTIDAD, SITIOS_DESTINO 
FROM ARTICULOS_CMS 
WHERE ESTADO = 'PUBLICADO' 
LIMIT 5;

-- Contar total actualizado
SELECT 'Total PARAFRASEADOS actualizados' as INFO, COUNT(*) as TOTAL 
FROM ARTICULOS_PARAFRASEADOS 
WHERE ESTADO = 'PUBLICADO' AND SITIO_DESTINO LIKE '%boominformativo%';

SELECT 'Total CMS actualizados' as INFO, COUNT(*) as TOTAL 
FROM ARTICULOS_CMS 
WHERE ESTADO = 'PUBLICADO' AND SITIOS_DESTINO LIKE '%boominformativo%';
