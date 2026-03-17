-- Actualización de imágenes para artículos sin imagen
-- Basado en búsqueda de noticias de otros medios

-- 1. AICM reforzó seguridad - Imagen de aeropuerto
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://obras.expansion.mx/wp-content/uploads/2026/01/aicm-terminal-aerea-mexico.jpg'
WHERE ID = '6c0aae6b-0d16-4d05-b1c5-e3e054e41889';

-- 2. Bloqueos viales Jalisco - Imagen de carretera/bloqueo
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.infobae.com/resizer/v2/https://cloudfront-us-east-1.images.arcpublishing.com/infobae/bloqueos-jalisco-2026.jpg'
WHERE ID = 'c80c7141-8358-4047-a696-b50ed911d953';

-- 3. CROC Leche Bienestar - Imagen de convenio/leche
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.gob.mx/cms/uploads/article/main_image/leche-para-el-bienestar-2026.jpg'
WHERE ID = 'd0791469-b788-4354-9b12-c23b1ac26d64';

-- 4. Alcalde Vallarta - Imagen de Luis Munguía
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://jalisco.quadratin.com.mx/wp-content/uploads/2026/01/luis-munguia-vallarta-alcalde.jpg'
WHERE ID = 'ae156f2f-3f29-464f-aab8-2c6323aa5d87';

-- 5. IMSS sarampión - Imagen de vacunación
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.gob.mx/cms/uploads/article/main_image/vacunacion-sarampion-imss-2026.jpg'
WHERE ID = '6be083cd-4f24-4a7a-8ded-d6c42c3079ae';

-- 6. Bernardo Barranco Trump/Papa - Imagen de opinión
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.jornada.com.mx/imagemeta/1200x630BN.jpg'
WHERE ID = '8c4c7865-4c87-49e1-8778-999beaeadc01';

-- 7. Cancelan vuelos - Imagen de aeropuerto
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.swissinfo.ch/resource/image/90981026/16x9/960/540/aeropuerto-puerto-vallarta.jpg'
WHERE ID = '6af316d6-313f-4f6f-b986-8c583659bc0b';

-- 8. Cárdenas pluris Senado - Imagen de Cuauhtémoc Cárdenas
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.jornada.com.mx/imagemeta/1200x630BN.jpg'
WHERE ID = '8bd37295-2c76-4fa9-933b-716a4a4208bb';

-- 9. Aspecto en el Senado - Imagen del Senado
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://comunicacionsocial.diputados.gob.mx/revista/public/uploads/revista/senado-mexico-2026.jpg'
WHERE ID = 'dbe861b1-f287-4cdd-bdd5-79159e473c32';

-- 10. Chinita tú - Imagen genérica de música
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.jornada.com.mx/imagemeta/1200x630BN.jpg'
WHERE ID = '9c4c9666-695a-4598-9608-d803d63fe694';

-- 11. Mejores Prepas 2026 - Imagen de estudiantes/UNAM
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://blog.unitips.mx/wp-content/uploads/2025/12/preparatoria-unam-mexico-2026.jpg'
WHERE ID = 'a0ed37ce-b37b-4f9f-8608-ad976d965c87';

-- 12. Mientras México arde - Imagen de violencia/incendio
UPDATE ARTICULOS_ORIGINALES 
SET URL_IMAGEN = 'https://www.dw.com/image/mexico-violencia-jalisco-2026.jpg'
WHERE ID = '9583bc73-8cb6-4a95-a8c4-933f078491ce';
