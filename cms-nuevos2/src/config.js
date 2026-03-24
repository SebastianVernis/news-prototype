// src/config.js — CMS Nuevos2: Configuración de los 8 sitios nuevos (fase 2)

export const DEBUG = false;
export const log = DEBUG ? console.log.bind(console) : () => {};
export const error = DEBUG ? console.error.bind(console) : () => {};
export const warn = DEBUG ? console.warn.bind(console) : () => {};

export const LOG_PREFIXES = {
  FB: '[FB]', RSS: '[RSS INGEST]', CRON: '[CRON]',
  CACHE: '[CACHE]', AUTH: '[Auth]', DB: '[DB]',
};

// CORS — Dominios permitidos (8 sitios nuevos fase 2 + pages.dev + admin + nuevos dominios custom)
export const ALLOWED_ORIGINS = [
  // Dominios .click (originales)
  'https://www.centronews.click',
  'https://www.noticias123.click',
  'https://www.breakingcentermexico.click',
  'https://www.alavistanoticias.click',
  'https://www.socialmexiconews.click',
  'https://www.tmznews.click',
  'https://www.radioabc.click',
  'https://www.noticiasintegra.click',
  'https://centronews.click',
  'https://noticias123.click',
  'https://breakingcentermexico.click',
  'https://alavistanoticias.click',
  'https://socialmexiconews.click',
  'https://tmznews.click',
  'https://radioabc.click',
  'https://noticiasintegra.click',
  // Dominios pages.dev
  'https://centronews.pages.dev',
  'https://noticias123.pages.dev',
  'https://breakingcentermexico.pages.dev',
  'https://alavistanoticias.pages.dev',
  'https://socialmexiconews.pages.dev',
  'https://tmznews.pages.dev',
  'https://radioabc.pages.dev',
  'https://noticiasintegra.pages.dev',
  // Admin
  'https://cms.sebastianvernis.space',
  'https://cms-admin-nuevos2.pages.dev',
  // Nuevos dominios custom (HTTPS)
  'https://centronews.buzz',
  'https://noticias123.click',
  'https://breakingcenter.site',
  'https://alavistanoticias.online',
  'https://socialmexico.top',
  'https://tmznews.lat',
  'https://radioabc.space',
  'https://noticiasintegra.lat',
  // Nuevos dominios custom (HTTP)
  'http://centronews.buzz',
  'http://noticias123.click',
  'http://breakingcenter.site',
  'http://alavistanoticias.online',
  'http://socialmexico.top',
  'http://tmznews.lat',
  'http://radioabc.space',
  'http://noticiasintegra.lat',
];

// SITIOS_LIST — 8 sitios nuevos fase 2
export const SITIOS_LIST = [
  'centronews', 'noticias123', 'breakingcentermexico', 'alavistanoticias',
  'socialmexiconews', 'tmznews', 'radioabc', 'noticiasintegra',
];

// Admin UI URL para password reset links
export const ADMIN_UI_URL = 'https://cms-admin-nuevos2.pages.dev';

export const SITE_DOMAIN_MAP = {
  centronews:             'https://www.centronews.click',
  noticias123:            'https://www.noticias123.click',
  breakingcentermexico:   'https://www.breakingcentermexico.click',
  alavistanoticias:       'https://www.alavistanoticias.click',
  socialmexiconews:       'https://www.socialmexiconews.click',
  tmznews:                'https://www.tmznews.click',
  radioabc:               'https://www.radioabc.click',
  noticiasintegra:        'https://www.noticiasintegra.click',
};

export const SITES_CONFIG = {
  centronews:             { nombre: 'Centro News',                tagline: 'El centro de la noticia',             dominio: 'https://www.centronews.click'           },
  noticias123:            { nombre: 'Noticias 123',                tagline: 'Todas las noticias en un solo lugar', dominio: 'https://www.noticias123.click'          },
  breakingcentermexico:   { nombre: 'Breaking Center News Mexico', tagline: 'Breaking news en tiempo real',        dominio: 'https://www.breakingcentermexico.click'},
  alavistanoticias:       { nombre: 'A la Vista Noticias',         tagline: 'Noticias al alcance de tu vista',    dominio: 'https://www.alavistanoticias.click'    },
  socialmexiconews:       { nombre: 'Social Mexico News',          tagline: 'Noticias sociales de México',         dominio: 'https://www.socialmexiconews.click'   },
  tmznews:                { nombre: 'TMZ News México',             tagline: 'La guía de entretenimiento',          dominio: 'https://www.tmznews.click'            },
  radioabc:               { nombre: 'Radio ABC',                    tagline: 'Radio y noticias de México',           dominio: 'https://www.radioabc.click'           },
  noticiasintegra:        { nombre: 'Noticias Integra',             tagline: 'Periodismo integral',                  dominio: 'https://www.noticiasintegra.click'   },
};
