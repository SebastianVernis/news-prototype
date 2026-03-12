// src/config.js — Constantes compartidas de la red de sitios

// ============================================================
// ENTORNO
// ============================================================
export const DEBUG = false; // Cambiar a true para ver logs en desarrollo

// Helper de logging: solo muestra en modo DEBUG
export const log = DEBUG ? console.log.bind(console) : () => {};
export const error = DEBUG ? console.error.bind(console) : () => {};
export const warn = DEBUG ? console.warn.bind(console) : () => {};

export const LOG_PREFIXES = {
  FB: '[FB]',
  RSS: '[RSS INGEST]',
  CRON: '[CRON]',
  CACHE: '[CACHE]',
  AUTH: '[Auth]',
  DB: '[DB]',
};
// CORS — Dominios permitidos
// ============================================================
export const ALLOWED_ORIGINS = [
  // Con www
  'https://www.noticiasobjetivo.click',
  'https://www.mexicoinformado.lat',
  'https://www.bitacoraurbana.lat',
  'https://www.nodoinformativo.lat',
  'https://www.cbnnoticias.click',
  'https://www.centralmexico.online',
  'https://www.verticenoticias.today',
  'https://www.radiocinconoticias.click',
  'https://www.reportecentral.site',
  'https://www.tvmexiconews.site',
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
  'https://www.noticiashorizonte.click',
  'https://www.pulsodiario.lat',
  'https://www.puntoclave.lat',
  'https://www.puntonoticias.website',
  'https://www.radarinformativo.online',
  'https://www.reportediario.online',
  'https://www.televisionabc.lat',
  // Sin www (root domains)
  'https://noticiasobjetivo.click',
  'https://mexicoinformado.lat',
  'https://bitacoraurbana.lat',
  'https://nodoinformativo.lat',
  'https://cbnnoticias.click',
  'https://centralmexico.online',
  'https://verticenoticias.today',
  'https://radiocinconoticias.click',
  'https://reportecentral.site',
  'https://tvmexiconews.site',
  'https://cms.sebastianvernis.space',
  'https://nexopress.sebastianvernis.space',
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
];

// ============================================================
// SITIOS_LIST — Lista canónica de slugs de sitios activos
// ============================================================
export const SITIOS_LIST = [
  // Sitios Estables (10)
  'radiocinconoticias', 'centralmexico', 'tvmexico', 'cbnnoticias',
  'mexicoinformado', 'nodoinformativo', 'bitacoraurbana',
  'reportecentralmx', 'verticenoticias', 'noticiasobjetivo',
  // Nuevos Sitios (17)
  'boominformativo', 'capitalpress', 'diarioexpress', 'elpulsomexicano',
  'enfoquecapital', 'enfoquedirecto', 'formulacdmx', 'mexicantimes',
  'mexico360noticias', 'mradio', 'noticiashorizonte', 'pulsodiario',
  'puntoclave', 'puntonoticias', 'radarinformativo', 'reportediario',
  'televisionabc',
];

// ============================================================
// SITE_DOMAIN_MAP — slug → dominio canónico
// ============================================================
export const SITE_DOMAIN_MAP = {
  radiocinconoticias: 'https://www.radiocinconoticias.click',
  centralmexico:      'https://www.centralmexico.online',
  tvmexico:           'https://www.tvmexiconews.site',
  cbnnoticias:        'https://www.cbnnoticias.click',
  mexicoinformado:    'https://www.mexicoinformado.lat',
  nodoinformativo:    'https://www.nodoinformativo.lat',
  bitacoraurbana:     'https://www.bitacoraurbana.lat',
  reportecentralmx:   'https://www.reportecentral.site',
  verticenoticias:    'https://www.verticenoticias.today',
  noticiasobjetivo:   'https://www.noticiasobjetivo.click',
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
  televisionabc:      'https://www.televisionabc.lat',
};

// ============================================================
// SITES_CONFIG — slug → { nombre, tagline, dominio } (para RSS)
// ============================================================
export const SITES_CONFIG = {
  // Sitios Estables (10) - Con dominio personalizado
  noticiasobjetivo:   { nombre: 'Noticias Objetivo',       tagline: 'La Verdad Sin Filtros',                dominio: 'https://www.noticiasobjetivo.click'  },
  mexicoinformado:    { nombre: 'México Informado',         tagline: 'Periodismo con Perspectiva',           dominio: 'https://www.mexicoinformado.lat'      },
  bitacoraurbana:     { nombre: 'Bitácora Urbana',          tagline: 'Crónicas de la ciudad',                dominio: 'https://www.bitacoraurbana.lat'       },
  nodoinformativo:    { nombre: 'Nodo Informativo',         tagline: 'El Centro de las Noticias',            dominio: 'https://www.nodoinformativo.lat'      },
  cbnnoticias:        { nombre: 'CBN Noticias',             tagline: 'Noticias con credibilidad',            dominio: 'https://www.cbnnoticias.click'        },
  centralmexico:      { nombre: 'Central México',           tagline: 'Noticias del Centro del País',         dominio: 'https://www.centralmexico.online'     },
  verticenoticias:    { nombre: 'Vértice Noticias',         tagline: 'Perspectivas Únicas',                  dominio: 'https://www.verticenoticias.today'    },
  radiocinconoticias: { nombre: 'Radio Cinco Noticias',     tagline: 'Información en Tiempo Real',           dominio: 'https://www.radiocinconoticias.click' },
  reportecentralmx:   { nombre: 'Reporte Central MX',       tagline: 'Periodismo de Investigación',          dominio: 'https://www.reportecentral.site'      },
  tvmexico:           { nombre: 'TV México',                tagline: 'Noticias y Entretenimiento',           dominio: 'https://www.tvmexiconews.site'        },
  // Nuevos Sitios (17) - Con dominio temporal .pages.dev
  boominformativo:    { nombre: 'Boominformativo',          tagline: 'Información que impacta',              dominio: 'https://boominformativo.pages.dev'    },
  capitalpress:       { nombre: 'Capital Press',            tagline: 'Prensa independiente',                 dominio: 'https://capitalpress.pages.dev'       },
  diarioexpress:      { nombre: 'Diario Express',           tagline: 'Noticias al instante',                 dominio: 'https://diarioexpress.pages.dev'      },
  elpulsomexicano:    { nombre: 'El Pulso Mexicano',        tagline: 'El latir de las noticias',             dominio: 'https://elpulsomexicano.pages.dev'    },
  enfoquecapital:     { nombre: 'Enfoque Capital',          tagline: 'La noticia con enfoque',               dominio: 'https://enfoquecapital.pages.dev'     },
  enfoquedirecto:     { nombre: 'Enfoque Directo',          tagline: 'Sin rodeos, directo al punto',         dominio: 'https://enfoquedirecto.pages.dev'     },
  formulacdmx:        { nombre: 'Fórmula CDMX',             tagline: 'La voz de la capital',                 dominio: 'https://formulacdmx.pages.dev'        },
  mexicantimes:       { nombre: 'The Mexican Times',        tagline: 'News from Mexico',                     dominio: 'https://mexicantimes.pages.dev'       },
  mexico360noticias:  { nombre: 'México 360 Noticias',      tagline: 'Cobertura completa',                   dominio: 'https://mexico360noticias.pages.dev'  },
  mradio:             { nombre: 'M Radio',                  tagline: 'Radio en línea',                       dominio: 'https://mradio.pages.dev'             },
  noticiashorizonte:  { nombre: 'Noticias Horizonte',       tagline: 'Mirando hacia el futuro',              dominio: 'https://noticiashorizonte.pages.dev'  },
  pulsodiario:        { nombre: 'Pulso Diario',             tagline: 'El pulso de la noticia',               dominio: 'https://pulsodiario.pages.dev'        },
  puntoclave:         { nombre: 'Punto Clave',              tagline: 'El punto exacto de la noticia',        dominio: 'https://puntoclave.pages.dev'         },
  puntonoticias:      { nombre: 'Punto Noticias',           tagline: 'Noticias en el punto',                 dominio: 'https://puntonoticias.pages.dev'      },
  radarinformativo:   { nombre: 'Radar Informativo',        tagline: 'Rastreando la verdad',                 dominio: 'https://radarinformativo.pages.dev'   },
  reportediario:      { nombre: 'Reporte Diario',           tagline: 'Tu reporte diario de noticias',        dominio: 'https://reportediario.pages.dev'      },
  televisionabc:      { nombre: 'Televisión ABC',           tagline: 'Televisión informativa',               dominio: 'https://televisionabc.pages.dev'      },
};
