-- Script para actualizar dominios de los 17 nuevos sitios
-- Ejecutar cuando tengas los dominios personalizados listados
-- Uso: wrangler d1 execute news_db --file update_domains.sql --remote

-- Actualizar dominios (ejemplos - editar con tus dominios reales)
UPDATE SITIOS SET DOMINIO = 'https://www.boominformativo.site' WHERE SLUG = 'boominformativo';
UPDATE SITIOS SET DOMINIO = 'https://www.capitalpress.mx' WHERE SLUG = 'capitalpress';
UPDATE SITIOS SET DOMINIO = 'https://www.diarioexpress.news' WHERE SLUG = 'diarioexpress';
UPDATE SITIOS SET DOMINIO = 'https://www.elpulsomexicano.com' WHERE SLUG = 'elpulsomexicano';
UPDATE SITIOS SET DOMINIO = 'https://www.enfoquecapital.mx' WHERE SLUG = 'enfoquecapital';
UPDATE SITIOS SET DOMINIO = 'https://www.enfoquedirecto.news' WHERE SLUG = 'enfoquedirecto';
UPDATE SITIOS SET DOMINIO = 'https://www.formulacdmx.mx' WHERE SLUG = 'formulacdmx';
UPDATE SITIOS SET DOMINIO = 'https://www.mexicantimes.mx' WHERE SLUG = 'mexicantimes';
UPDATE SITIOS SET DOMINIO = 'https://www.mexico360noticias.mx' WHERE SLUG = 'mexico360noticias';
UPDATE SITIOS SET DOMINIO = 'https://www.mradio.mx' WHERE SLUG = 'mradio';
UPDATE SITIOS SET DOMINIO = 'https://www.noticiashorizonte.mx' WHERE SLUG = 'noticiashorizonte';
UPDATE SITIOS SET DOMINIO = 'https://www.pulsodiario.mx' WHERE SLUG = 'pulsodiario';
UPDATE SITIOS SET DOMINIO = 'https://www.puntoclave.mx' WHERE SLUG = 'puntoclave';
UPDATE SITIOS SET DOMINIO = 'https://www.puntonoticias.mx' WHERE SLUG = 'puntonoticias';
UPDATE SITIOS SET DOMINIO = 'https://www.radarinformativo.mx' WHERE SLUG = 'radarinformativo';
UPDATE SITIOS SET DOMINIO = 'https://www.reportediario.mx' WHERE SLUG = 'reportediario';
UPDATE SITIOS SET DOMINIO = 'https://www.televisionabc.mx' WHERE SLUG = 'televisionabc';

-- Habilitar Facebook para los nuevos sitios (opcional, cuando tengas los tokens)
UPDATE SITIOS SET FACEBOOK_ACTIVO = 1 WHERE SLUG IN (
  'boominformativo', 'capitalpress', 'diarioexpress', 'elpulsomexicano',
  'enfoquecapital', 'enfoquedirecto', 'formulacdmx', 'mexicantimes',
  'mexico360noticias', 'mradio', 'noticiashorizonte', 'pulsodiario',
  'puntoclave', 'puntonoticias', 'radarinformativo', 'reportediario',
  'televisionabc'
);

-- Verificar cambios
SELECT SLUG, NOMBRE, DOMINIO, FACEBOOK_ACTIVO FROM SITIOS ORDER BY NOMBRE;
