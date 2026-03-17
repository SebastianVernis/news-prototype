-- Script para agregar los 17 nuevos sitios a la tabla SITIOS
-- Ejecutar con: wrangler d1 execute news_db --command "SQL" --remote

-- Nuevos Sitios (17)
INSERT OR IGNORE INTO SITIOS (ID, SLUG, NOMBRE, DOMINIO, TAGLINE, ACTIVO, FACEBOOK_ACTIVO) VALUES
  (lower(hex(randomblob(16))), 'boominformativo', 'Boominformativo', 'https://www.boominformativo.site', 'Información que impacta', 1, 1),
  (lower(hex(randomblob(16))), 'capitalpress', 'Capital Press', 'https://www.capitalpress.mx', 'Prensa independiente', 1, 1),
  (lower(hex(randomblob(16))), 'diarioexpress', 'Diario Express', 'https://www.diarioexpress.news', 'Noticias al instante', 1, 1),
  (lower(hex(randomblob(16))), 'elpulsomexicano', 'El Pulso Mexicano', 'https://www.elpulsomexicano.com', 'El latir de las noticias', 1, 1),
  (lower(hex(randomblob(16))), 'enfoquecapital', 'Enfoque Capital', 'https://www.enfoquecapital.mx', 'La noticia con enfoque', 1, 1),
  (lower(hex(randomblob(16))), 'enfoquedirecto', 'Enfoque Directo', 'https://www.enfoquedirecto.news', 'Sin rodeos, directo al punto', 1, 1),
  (lower(hex(randomblob(16))), 'formulacdmx', 'Fórmula CDMX', 'https://www.formulacdmx.mx', 'La voz de la capital', 1, 1),
  (lower(hex(randomblob(16))), 'mexicantimes', 'The Mexican Times', 'https://www.mexicantimes.mx', 'News from Mexico', 1, 1),
  (lower(hex(randomblob(16))), 'mexico360noticias', 'México 360 Noticias', 'https://www.mexico360noticias.mx', 'Cobertura completa', 1, 1),
  (lower(hex(randomblob(16))), 'mradio', 'M Radio', 'https://www.mradio.mx', 'Radio en línea', 1, 1),
  (lower(hex(randomblob(16))), 'noticiashorizonte', 'Noticias Horizonte', 'https://www.noticiashorizonte.mx', 'Mirando hacia el futuro', 1, 1),
  (lower(hex(randomblob(16))), 'pulsodiario', 'Pulso Diario', 'https://www.pulsodiario.mx', 'El pulso de la noticia', 1, 1),
  (lower(hex(randomblob(16))), 'puntoclave', 'Punto Clave', 'https://www.puntoclave.mx', 'El punto exacto de la noticia', 1, 1),
  (lower(hex(randomblob(16))), 'puntonoticias', 'Punto Noticias', 'https://www.puntonoticias.mx', 'Noticias en el punto', 1, 1),
  (lower(hex(randomblob(16))), 'radarinformativo', 'Radar Informativo', 'https://www.radarinformativo.mx', 'Rastreando la verdad', 1, 1),
  (lower(hex(randomblob(16))), 'reportediario', 'Reporte Diario', 'https://www.reportediario.mx', 'Tu reporte diario de noticias', 1, 1),
  (lower(hex(randomblob(16))), 'televisionabc', 'Televisión ABC', 'https://www.televisionabc.mx', 'Televisión informativa', 1, 1);

-- Verificar sitios agregados
SELECT SLUG, NOMBRE, DOMINIO, ACTIVO FROM SITIOS WHERE SLUG IN (
  'boominformativo', 'capitalpress', 'diarioexpress', 'elpulsomexicano',
  'enfoquecapital', 'enfoquedirecto', 'formulacdmx', 'mexicantimes',
  'mexico360noticias', 'mradio', 'noticiashorizonte', 'pulsodiario',
  'puntoclave', 'puntonoticias', 'radarinformativo', 'reportediario',
  'televisionabc'
);
