// Site definitions and constants
const path = require('path');

const SITES = [
    { num: 1,  slug: 'puntoclave',        name: 'PuntoClave',           style: 'Neobrutalismo' },
    { num: 2,  slug: 'diarioexpress',      name: 'DiarioExpress',        style: 'Swiss Design' },
    { num: 3,  slug: 'enfoquedirecto',     name: 'EnfoqueDirecto',       style: 'Editorial Cinematico' },
    { num: 4,  slug: 'noticiashorizonte',  name: 'NoticiasHorizonte',    style: 'Revista Lifestyle' },
    { num: 5,  slug: 'mexico360noticias',  name: 'Mexico360Noticias',    style: 'Corporate Standard' },
    { num: 6,  slug: 'capitalpress',       name: 'CapitalPress',         style: 'Minimalismo Escandinavo' },
    { num: 7,  slug: 'boominformativo',    name: 'BoomInformativo',      style: 'Asimetria Dinamica' },
    { num: 8,  slug: 'puntonoticias',      name: 'PuntoNoticias',        style: 'Card-Based Magazine' },
    { num: 9,  slug: 'reportediario',      name: 'ReporteDiario',        style: 'Modern Broadsheet' },
    { num: 10, slug: 'pulsodiario',        name: 'PulsoDiario',          style: 'Horizontal Storytelling' },
    { num: 11, slug: 'radarinformativo',   name: 'RadarInformativo',     style: 'Tech Dark Mode' },
    { num: 12, slug: 'formulacdmx',        name: 'FormulaCDMX',          style: 'Frosted Glass' },
    { num: 13, slug: 'enfoquecapital',     name: 'EnfoqueCapital',       style: 'Split Screen Magazine' },
    { num: 14, slug: 'mexicantimes',       name: 'MexicanTimes',         style: 'Timeline Feed' },
    { num: 15, slug: 'elpulsomexicano',    name: 'ElPulsoMexicano',      style: 'Cartel Maximalista' },
    { num: 16, slug: 'mradio',             name: 'MRadio',               style: 'Neumorphic Tech' },
    { num: 17, slug: 'televisionabc',      name: 'TelevisionABC',        style: 'Premium Financial' },
];

const BASE_DIR = path.resolve(__dirname, '..');
const TITULARES_DIR = path.join(BASE_DIR, 'Titulares');
const SITES_DIR = path.join(BASE_DIR, 'sites');
const METADATA_DIR = path.join(BASE_DIR, 'data', 'sites_metadata');
const API_BASE = 'https://news-api.sebastianvernis.workers.dev';
const CATEGORIES = ['nacional', 'politica', 'economia', 'deportes', 'cultura', 'tecnologia'];
const CAT_LABELS = {
    nacional: 'Nacional', politica: 'Politica', economia: 'Economia',
    deportes: 'Deportes', cultura: 'Cultura', tecnologia: 'Tecnologia'
};

module.exports = { SITES, BASE_DIR, TITULARES_DIR, SITES_DIR, METADATA_DIR, API_BASE, CATEGORIES, CAT_LABELS };
