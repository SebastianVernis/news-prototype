// src/config.js — CMS Originales: Configuración de los 10 sitios originales

export const DEBUG = false;
export const log = DEBUG ? console.log.bind(console) : () => {};
export const error = DEBUG ? console.error.bind(console) : () => {};
export const warn = DEBUG ? console.warn.bind(console) : () => {};

export const LOG_PREFIXES = {
  FB: '[FB]', RSS: '[RSS INGEST]', CRON: '[CRON]',
  CACHE: '[CACHE]', AUTH: '[Auth]', DB: '[DB]',
};

// CORS — Dominios permitidos (10 sitios originales + pages.dev + admin)
export const ALLOWED_ORIGINS = [
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
  'https://radiocinconoticias.pages.dev',
  'https://centralmexico.pages.dev',
  'https://tvmexico.pages.dev',
  'https://cbnnoticias.pages.dev',
  'https://mexicoinformado.pages.dev',
  'https://nodoinformativo.pages.dev',
  'https://bitacoraurbana.pages.dev',
  'https://reportecentralmx.pages.dev',
  'https://verticenoticias.pages.dev',
  'https://noticiasobjetivo.pages.dev',
  'https://cms.sebastianvernis.space',
  'https://cms-admin-originaux.pages.dev',
];

// SITIOS_LIST — 10 sitios originales
export const SITIOS_LIST = [
  'radiocinconoticias', 'centralmexico', 'tvmexico', 'cbnnoticias',
  'mexicoinformado', 'nodoinformativo', 'bitacoraurbana',
  'reportecentralmx', 'verticenoticias', 'noticiasobjetivo',
];

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
};

export const SITES_CONFIG = {
  noticiasobjetivo:   { nombre: 'Noticias Objetivo',       tagline: 'La Verdad Sin Filtros',         dominio: 'https://www.noticiasobjetivo.click' },
  mexicoinformado:    { nombre: 'México Informado',         tagline: 'Periodismo con Perspectiva',    dominio: 'https://www.mexicoinformado.lat'     },
  bitacoraurbana:     { nombre: 'Bitácora Urbana',           tagline: 'Crónicas de la ciudad',         dominio: 'https://www.bitacoraurbana.lat'      },
  nodoinformativo:    { nombre: 'Nodo Informativo',         tagline: 'El Centro de las Noticias',    dominio: 'https://www.nodoinformativo.lat'     },
  cbnnoticias:        { nombre: 'CBN Noticias',              tagline: 'Noticias con credibilidad',     dominio: 'https://www.cbnnoticias.click'       },
  centralmexico:      { nombre: 'Central México',            tagline: 'Noticias del Centro del País',  dominio: 'https://www.centralmexico.online'    },
  verticenoticias:    { nombre: 'Vértice Noticias',          tagline: 'Perspectivas Únicas',          dominio: 'https://www.verticenoticias.today'  },
  radiocinconoticias: { nombre: 'Radio Cinco Noticias',      tagline: 'Información en Tiempo Real',    dominio: 'https://www.radiocinconoticias.click'},
  reportecentralmx:   { nombre: 'Reporte Central MX',        tagline: 'Periodismo de Investigación',   dominio: 'https://www.reportecentral.site'    },
  tvmexico:           { nombre: 'TV México',                 tagline: 'Noticias y Entretenimiento',    dominio: 'https://www.tvmexiconews.site'      },
};
