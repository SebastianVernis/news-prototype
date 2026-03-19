// src/utils/helpers.js — Utilidades compartidas del worker

// ============================================================
// sleep — Pausa asíncrona (ms)
// ============================================================
export const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// ============================================================
// slugify — Convierte texto a slug URL-friendly
// ============================================================
export const slugify = (text) => {
  return text.toString().toLowerCase().trim()
    .replace(/[áàäâã]/g, 'a').replace(/[éèëê]/g, 'e').replace(/[íìïî]/g, 'i')
    .replace(/[óòöôõ]/g, 'o').replace(/[úùüû]/g, 'u').replace(/[ñ]/g, 'n')
    .replace(/[ç]/g, 'c').replace(/[ý]/g, 'y')
    .replace(/\s+/g, '-').replace(/[^\w\-]+/g, '').replace(/\-\-+/g, '-')
    .replace(/^-+/, '').replace(/-+$/, '').substring(0, 100);
};

const ARTICLE_TITLE_PREFIXES = [
  /^la\s+jornada:\s*/i,
  /^el\s+informador:\s*/i,
  /^proceso:\s*/i,
  /^el\s+universal:\s*/i,
  /^milenio:\s*/i,
  /^excelsior:\s*/i,
  /^excélsior:\s*/i,
  /^expansion:\s*/i,
  /^expansion:\s*/i,
  /^expansión:\s*/i,
  /^publimetro:\s*/i,
  /^azteca\s+noticias:\s*/i,
  /^tv\s+azteca:\s*/i,
];

export const normalizeArticleTitleForSlug = (text) => {
  let cleaned = decodeHTMLEntities(text || '').trim();

  for (const prefix of ARTICLE_TITLE_PREFIXES) {
    cleaned = cleaned.replace(prefix, '');
  }

  cleaned = cleaned.replace(/\s*[|\-]\s*(la\s+jornada|el\s+informador|proceso|el\s+universal|milenio|excelsior|excélsior|expansion|expansión|publimetro|azteca\s+noticias|tv\s+azteca)\s*$/i, '');

  return cleaned.trim();
};

export const articleSlugify = (text) => slugify(normalizeArticleTitleForSlug(text));

// ============================================================
// decodeHTMLEntities — Decodifica entidades HTML y limpia contenido
// ============================================================
export const decodeHTMLEntities = (text) => {
  if (!text) return '';

  // 1. Decodificar entidades HTML básicas
  let cleaned = text
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/&#39;/g, "'")
    .replace(/&ldquo;/g, '"')
    .replace(/&rdquo;/g, '"')
    .replace(/&lsquo;/g, "'")
    .replace(/&rsquo;/g, "'")
    .replace(/&iexcl;/g, '¡')
    .replace(/&iquest;/g, '¿')
    .replace(/&mdash;/g, '—')
    .replace(/&ndash;/g, '–')
    .replace(/&hellip;/g, '…')
    .replace(/&laquo;/g, '«')
    .replace(/&raquo;/g, '»');

  // 2. Eliminar Google Tag Manager y scripts de anuncios
  cleaned = cleaned.replace(/googletag\.cmd\.push\([^)]*\);/g, '');
  cleaned = cleaned.replace(/googletag\.display\([^)]*\);/g, '');
  cleaned = cleaned.replace(/googletag\.display\(['"][^'"]*['"]\);/g, '');
  cleaned = cleaned.replace(/div-gpt-ad-[\w()]+/g, '');
  cleaned = cleaned.replace(/<script[^>]*googletag[^>]*>[\s\S]*?<\/script>/g, '');

  // 3. Eliminar CSS variables corruptas y bloques de estilo
  cleaned = cleaned.replace(/\s*--[\w-]+:\s*[^;]*;\s*/g, '');
  cleaned = cleaned.replace(/\{[^}]*--[\w-]+:[^}]*\}/g, '');
  cleaned = cleaned.replace(/#[\w-]+\{[^}]*\}/g, '');

  // 4. Eliminar caracteres corruptos y especiales
  cleaned = cleaned.replace(/[\uFFFD]/g, ''); // Replacement character
  cleaned = cleaned.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F-\u009F]/g, '');

  // 5. Eliminar marcas de agua y créditos
  const watermarks = [
    /LEA TAMBIÉN[:\s]*/gi,
    /LEA ADEMÁS[:\s]*/gi,
    /TE PUEDE INTERESAR[:\s]*/gi,
    /MÁS INFORMACIÓN[:\s]*/gi,
    /VER TAMBIÉN[:\s]*/gi,
    /PUBLICIDAD/gi,
    /ANUNCIO/gi,
    /SPONSORED/gi,
    /PATROCINADO/gi,
    /\[.*?PUBLICIDAD.*?\]/gi,
    /\[.*?ANUNCIO.*?\]/gi,
    /Suscríbete/gi,
    /Suscríbete aquí/gi,
    /Suscríbase/gi,
    /Síguenos/gi,
    /Síguenos en/gi,
    /Comparte esta nota/gi,
    /Compartir en Facebook/gi,
    /Compartir en Twitter/gi,
  ];

  for (const watermark of watermarks) {
    cleaned = cleaned.replace(watermark, '');
  }

  // 6. Eliminar saltos de línea repetidos
  cleaned = cleaned.replace(/\n\s*\n\s*\n/g, '\n\n');

  return cleaned.trim();
};

// ============================================================
// parseArticleRow — Normaliza una fila de DB a objeto artículo
// ============================================================
export const parseArticleRow = (row) => {
  if (!row) return null;
  const category = row.CATEGORIA || row.category || 'General';

  const title   = decodeHTMLEntities(row.TITULO_PARAFRASEADO || row.TITULO || row.title || '');
  const content = decodeHTMLEntities(row.CONTENIDO || row.content || '');
  const excerpt = decodeHTMLEntities(row.DESCRIPCION_PARAFRASEADA || row.DESCRIPCION || row.excerpt || '');

  return {
    id:          row.ID || row.id,
    title,
    slug:        row.slug || row.SLUG || articleSlugify(row.TITULO_PARAFRASEADO || row.TITULO || 'articulo'),
    content,
    excerpt,
    category,
    author:      'Redacción ' + category,
    publishedAt: row.FECHA_PUBLICACION || row.published_at || null,
    imageUrl:    row.URL_IMAGEN || row.image_url || '',
    featured:    Boolean(row.DESTACADO || row.featured || 0),
    site:        row.SITIO_DESTINO || row.SITIOS_DESTINO || row.site || '',
    fb_published: Boolean(row.FB_PUBLICADO || 0),
  };
};
