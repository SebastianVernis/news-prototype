// src/config.js — CMS Nuevos: Configuración de los 17 sitios nuevos

export const DEBUG = false;
export const log = DEBUG ? console.log.bind(console) : () => {};
export const error = DEBUG ? console.error.bind(console) : () => {};
export const warn = DEBUG ? console.warn.bind(console) : () => {};

export const LOG_PREFIXES = {
  FB: '[FB]', RSS: '[RSS INGEST]', CRON: '[CRON]',
  CACHE: '[CACHE]', AUTH: '[Auth]', DB: '[DB]',
};

// CORS — Dominios permitidos (17 sitios nuevos)
export const ALLOWED_ORIGINS = [
  'https://www.boominformativo.top',
  'https://www.capitalpress.lat',
  'https://www.diarioexpress.click',
  'https://www.elpulsomexicano.lat',
  'https://www.enfoquecapital.top',
  'https://www.enfoquedirecto.lat',
  'https://www.formulacdmx.top',
  'https://www.mradio.lat',
  'https://www.mexicantimes.top',
  'https://www.mexico360noticias.click',
  'https://www.noticiashoronte.click',
  'https://www.pulsodiario.lat',
  'https://www.puntoclave.lat',
  'https://www.puntonoticias.website',
  'https://www.radarinformativo.online',
  'https://www.reportediario.online',
  'https://www.televisionabc.lat',
  'https://boominformativo.top',
  'https://capitalpress.lat',
  'https://diarioexpress.click',
  'https://elpulsomexicano.lat',
  'https://enfoquecapital.top',
  'https://enfoquedirecto.lat',
  'https://formulacdmx.top',
  'https://mradio.lat',
  'https://mexicantimes.top',
  'https://mexico360noticias.click',
  'https://noticiashorizonte.click',
  'https://pulsodiario.lat',
  'https://puntoclave.lat',
  'https://puntonoticias.website',
  'https://radarinformativo.online',
  'https://reportediario.online',
  'https://televisionabc.lat',
  'https://cms.sebastianvernis.space',
];

// SITIOS_LIST — 17 sitios nuevos
export const SITIOS_LIST = [
  'boominformativo', 'capitalpress', 'diarioexpress', 'elpulsomexicano',
  'enfoquecapital', 'enfoquedirecto', 'formulacdmx', 'mexicantimes',
  'mexico360noticias', 'mradio', 'noticiashorizonte', 'pulsodiario',
  'puntoclave', 'puntonoticias', 'radarinformativo', 'reportediario',
  'televisionabc',
];

export const SITE_DOMAIN_MAP = {
  boominformativo:    'https://www.boominformativo.top',
  capitalpress:       'https://www.capitalpress.lat',
  diarioexpress:      'https://www.diarioexpress.click',
  elpulsomexicano:    'https://www.elpulsomexicano.lat',
  enfoquecapital:     'https://www.enfoquecapital.top',
  enfoquedirecto:     'https://www.enfoquedirecto.lat',
  formulacdmx:        'https://www.formulacdmx.top',
  mexicantimes:       'https://www.mexicantimes.top',
  mexico360noticias:  'https://www.mexico360noticias.click',
  mradio:             'https://www.mradio.lat',
  noticiashorizonte:  'https://www.noticiashorizonte.click',
  pulsodiario:        'https://www.pulsodiario.lat',
  puntoclave:         'https://www.puntoclave.lat',
  puntonoticias:      'https://www.puntonoticias.website',
  radarinformativo:   'https://www.radarinformativo.online',
  reportediario:      'https://www.reportediario.online',
  televisionabc:       'https://www.televisionabc.lat',
};

export const SITES_CONFIG = {
  boominformativo:    { nombre: 'Boominformativo',       tagline: 'Información que impacta',        dominio: 'https://www.boominformativo.top'   },
  capitalpress:       { nombre: 'Capital Press',          tagline: 'Prensa independiente',         dominio: 'https://www.capitalpress.lat'      },
  diarioexpress:      { nombre: 'Diario Express',         tagline: 'Noticias al instante',          dominio: 'https://www.diarioexpress.click'    },
  elpulsomexicano:    { nombre: 'El Pulso Mexicano',      tagline: 'El latir de las noticias',     dominio: 'https://www.elpulsomexicano.lat'    },
  enfoquecapital:     { nombre: 'Enfoque Capital',        tagline: 'La noticia con enfoque',        dominio: 'https://www.enfoquecapital.top'    },
  enfoquedirecto:     { nombre: 'Enfoque Directo',        tagline: 'Sin rodeos, directo al punto',  dominio: 'https://www.enfoquedirecto.lat'   },
  formulacdmx:        { nombre: 'Fórmula CDMX',           tagline: 'La voz de la capital',          dominio: 'https://www.formulacdmx.top'       },
  mexicantimes:       { nombre: 'The Mexican Times',       tagline: 'News from Mexico',              dominio: 'https://www.mexicantimes.top'     },
  mexico360noticias:  { nombre: 'México 360 Noticias',    tagline: 'Cobertura completa',           dominio: 'https://www.mexico360noticias.click'},
  mradio:             { nombre: 'M Radio',                 tagline: 'Radio en línea',                dominio: 'https://www.mradio.lat'            },
  noticiashorizonte:  { nombre: 'Noticias Horizonte',      tagline: 'Mirando hacia el futuro',       dominio: 'https://www.noticiashorizonte.click'},
  pulsodiario:        { nombre: 'Pulso Diario',            tagline: 'El pulso de la noticia',         dominio: 'https://www.pulsodiario.lat'      },
  puntoclave:         { nombre: 'Punto Clave',             tagline: 'El punto exacto de la noticia',  dominio: 'https://www.puntoclave.lat'       },
  puntonoticias:      { nombre: 'Punto Noticias',          tagline: 'Noticias en el punto',          dominio: 'https://www.puntonoticias.website'},
  radarinformativo:   { nombre: 'Radar Informativo',       tagline: 'Rastreando la verdad',          dominio: 'https://www.radarinformativo.online'},
  reportediario:      { nombre: 'Reporte Diario',          tagline: 'Tu reporte diario de noticias', dominio: 'https://www.reportediario.online'  },
  televisionabc:       { nombre: 'Televisión ABC',          tagline: 'Televisión informativa',        dominio: 'https://www.televisionabc.lat'    },
};
