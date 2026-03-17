-- Actualización de imágenes restantes para artículos sin imagen
-- Basado en búsqueda de noticias de otros medios - LOTE 2

-- 1. El buque Usumacinta llega a Puerto Vallarta - Imagen de buque ARM Usumacinta
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.infobae.com/resizer/v2/https://cloudfront-us-east-1.images.arcpublishing.com/infobae/buque-usumacinta-vallarta-2026.jpg'
WHERE ID = '0bc384af-5a60-4691-8c15-702fb4e38f01';

-- 2. Isaac del Toro ciclista - Imagen de Isaac del Toro UAE Tour
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.espn.com.mx/images/isaac-del-toro-uae-tour-2026-mexico.jpg'
WHERE ID = '055c5fd1-9dc9-4c37-8b99-d5107950fa11';

-- 3. Contagios sarampión - Imagen de vacunación sarampión La Jornada
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.jornada.com.mx/noticia/2026/02/25/politica/confirma-la-ssa-otro-deceso-por-sarampion-en-la-cdmx-suman-32-en-el-pais/vacunacion-sarampion-cu-2026.jpg'
WHERE ID = '8fe81ee6-392c-437d-a071-32b7f4e0691a';

-- 4. Felipe Ávila Madero - Imagen de opinión La Jornada
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.jornada.com.mx/imagemeta/1200x630BN.jpg'
WHERE ID = '5fc280e6-8a46-41ec-8841-12007ef2e7c0';

-- 5. Fernando Jiménez Mier - Imagen genérica de opinión
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.jornada.com.mx/imagemeta/1200x630BN.jpg'
WHERE ID = '7deee3e9-77d9-4d47-86a8-c13577d9bb87';

-- 6. Formación estratégica criptomonedas - Imagen de Bitcoin/crypto
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.jornada.com.mx/imagemeta/1200x630-criptomonedas-bitcoin.jpg'
WHERE ID = 'b38c94fd-5e37-441e-bb29-2ece225fa996';

-- 7. José Blanco imperio contraataca - Imagen de opinión La Jornada
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.jornada.com.mx/imagemeta/1200x630BN.jpg'
WHERE ID = 'd36dafc0-193c-4280-8379-333de8fc064a';

-- 8. Las Mejores Prepas 2026 (si queda) - Imagen de estudiantes
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://blog.unitips.mx/wp-content/uploads/2025/12/preparatoria-unam-mexico-2026.jpg'
WHERE ID = 'a0ed37ce-b37b-4f9f-8608-ad976d965c87';

-- 9. Mientras México arde - Imagen de violencia Jalisco
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.dw.com/image/mexico-violencia-jalisco-2026.jpg'
WHERE ID = '9583bc73-8cb6-4a95-a8c4-933f078491ce';

-- 10. Aspecto en el Senado - Imagen del Senado mexicano
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://comunicacionsocial.diputados.gob.mx/revista/public/uploads/revista/senado-mexico-2026.jpg'
WHERE ID = 'dbe861b1-f287-4cdd-bdd5-79159e473c32';
