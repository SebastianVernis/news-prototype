// src/cron/rss-ingest.js — Ingesta automática de RSS y parafraseo con IA

import { slugify, decodeHTMLEntities } from '../utils/helpers.js';
import { getOGImage, uploadToR2 } from '../utils/html.js';
import { SITIOS_LIST, SITE_DOMAIN_MAP, log, error, warn, LOG_PREFIXES } from '../config.js';

const RSS_LOG = (...args) => log('[RSS INGEST]', ...args);
const RSS_ERR = (...args) => error('[RSS INGEST]', ...args);
const RSS_WARN = (...args) => warn('[RSS]', ...args);

// ============================================================
// cleanArticleContent — Limpieza profunda de contenido
// ============================================================
export function cleanArticleContent(text) {
  if (!text) return '';

  let cleaned = text;

  // 1. Decodificar entidades HTML
  cleaned = decodeHTMLEntities(cleaned);

  // 2. Eliminar scripts, estilos y elementos no deseados
  cleaned = cleaned.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
  cleaned = cleaned.replace(/<style[^>]*>[\s\S]*<\/style>/gi, '');
  cleaned = cleaned.replace(/<link[^>]*>/gi, '');
  cleaned = cleaned.replace(/<meta[^>]*>/gi, '');
  cleaned = cleaned.replace(/<noscript[^>]*>[\s\S]*?<\/noscript>/gi, '');
  cleaned = cleaned.replace(/<iframe[^>]*>[\s\S]*?<\/iframe>/gi, '');
  cleaned = cleaned.replace(/<object[^>]*>[\s\S]*?<\/object>/gi, '');
  cleaned = cleaned.replace(/<embed[^>]*>/gi, '');
  cleaned = cleaned.replace(/<form[^>]*>[\s\S]*?<\/form>/gi, '');
  cleaned = cleaned.replace(/<input[^>]*>/gi, '');
  cleaned = cleaned.replace(/<button[^>]*>[\s\S]*?<\/button>/gi, '');
  cleaned = cleaned.replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, '');
  cleaned = cleaned.replace(/<header[^>]*>[\s\S]*?<\/header>/gi, '');
  cleaned = cleaned.replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, '');
  cleaned = cleaned.replace(/<aside[^>]*>[\s\S]*?<\/aside>/gi, '');
  cleaned = cleaned.replace(/<sidebar[^>]*>[\s\S]*?<\/sidebar>/gi, '');

  // 3. Eliminar secciones de comentarios y noticias relacionadas (PATRONES ESPECIFICOS)
  cleaned = cleaned.replace(/Comentarios\s*$/gm, '');
  cleaned = cleaned.replace(/Más leídas\s*$/gm, '');
  cleaned = cleaned.replace(/Otras Noticias\s*$/gm, '');
  cleaned = cleaned.replace(/Últimas noticias\s*$/gm, '');
  cleaned = cleaned.replace(/te puede interesar/gi, '');
  cleaned = cleaned.replace(/lea también/gi, '');
  cleaned = cleaned.replace(/continuar leyendo/gi, '');
  cleaned = cleaned.replace(/Nacional\s+/gi, '');
  cleaned = cleaned.replace(/Internacional\s+/gi, '');
  cleaned = cleaned.replace(/Economía\s+/gi, '');
  cleaned = cleaned.replace(/Deportes\s+/gi, '');
  cleaned = cleaned.replace(/Cultura\s+/gi, '');
  cleaned = cleaned.replace(/Revista Proceso\s+/gi, '');

  // 4. Eliminar firmas, copyright y datos legales
  cleaned = cleaned.replace(/\d{4}\s*DERECHOS\s*RESERVADOS.*$/gim, '');
  cleaned = cleaned.replace(/©\s*\d{4}.*$/gim, '');
  cleaned = cleaned.replace(/todos los derechos reservados/gi, '');
  cleaned = cleaned.replace(/prohibida su reproducción/gi, '');
  cleaned = cleaned.replace(/comunicación e información/gi, '');
  cleaned = cleaned.replace(/EXPANSIÓN.*$/gim, '');
  cleaned = cleaned.replace(/fresas #\d+, col\..*$/gim, '');
  cleaned = cleaned.replace(/\(apro\)/gi, '');
  cleaned = cleaned.replace(/\(agencias\)/gi, '');
  cleaned = cleaned.replace(/\(ep\)/gi, '');

  // 5. Eliminar Google Tag Manager, Dailymotion y anuncios
  cleaned = cleaned.replace(/googletag\.cmd\.push\([^)]*\);/gi, '');
  cleaned = cleaned.replace(/googletag\.display\([^)]*\);/gi, '');
  cleaned = cleaned.replace(/div-gpt-ad-[\w()]+/gi, '');
  cleaned = cleaned.replace(/<script[^>]*googletag[^>]*>[\s\S]*?<\/script>/gi, '');
  cleaned = cleaned.replace(/#dailymotion-pip-large-viewport[^}]*\}[^}]*\}/gi, '');
  cleaned = cleaned.replace(/#dailymotion[^}]*\}/gi, '');

  // 6. Eliminar bloques JSON y datos estructurados
  cleaned = cleaned.replace(/\{\s*"locale"\s*:\s*"[^"]+"\s*\}/gi, '');
  cleaned = cleaned.replace(/\{\s*"@context".*?\}/gis, '');
  cleaned = cleaned.replace(/\{\s*"@type".*?\}/gis, '');

  // 7. Eliminar CSS y reglas de estilo
  cleaned = cleaned.replace(/#[\w-]+\{[^}]*\}/gi, '');
  cleaned = cleaned.replace(/\.[\w-]+\{[^}]*\}/gi, '');
  cleaned = cleaned.replace(/\{[^}]*--[\w-]+:[^}]*\}/gi, '');

  // 8. Eliminar caracteres corruptos y whitespace excesivo
  cleaned = cleaned.replace(/[\uFFFD]/g, ''); // Replacement character
  cleaned = cleaned.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F-\u009F]/g, '');
  cleaned = cleaned.replace(/\r\n/g, '\n');
  cleaned = cleaned.replace(/\n\s*\n\s*\n/g, '\n\n');
  cleaned = cleaned.replace(/^\s+|\s+$/g, '');

  // 9. Filtrar líneas por contenido (línea por línea)
  const lines = cleaned.split('\n');
  const filteredLines = lines.filter(line => {
    const lower = line.toLowerCase().trim();
    const len = line.trim().length;
    
    // Eliminar líneas muy cortas (< 30 chars) que no son contenido válido
    if (len < 30 && len > 0) return false;
    
    // Eliminar líneas que son solo categorías
    if (/^(nacional|internacional|economía|deportes|cultura|opinión)$/i.test(lower)) return false;
    
    // Eliminar líneas que parecen metadata de autor/editorial
    if (lower.includes('expansión') || lower.includes('proceso') || lower.includes('apro')) return false;
    
    // Eliminar líneas con puro copyright
    if (lower.includes('derechos reservados') || lower.includes('©')) return false;
    
    return true;
  });
  cleaned = filteredLines.join('\n');

  // 10. Limpieza final
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n'); // Máximo 2 saltos de línea
  cleaned = cleaned.trim();

  return cleaned;
}

// ============================================================
// proofreadTextAI — Parafrasea texto usando Workers AI
// ============================================================
async function proofreadTextAI(text, type, env) {
  try {
    if (!env.AI) {
      RSS_WARN('[AI] No AI binding available');
      return text;
    }

    const prompt = type === 'título'
      ? `Reescribe este titular de noticias en español mexicano, manteniendo el significado pero con palabras diferentes. Solo devuelve el titular reescrito, sin explicaciones:\n\n${text}`
      : `Reescribe este artículo de noticias en español mexicano con tus propias palabras, manteniendo todos los hechos importantes. Usa un estilo periodístico profesional. Solo devuelve el artículo reescrito:\n\n${text.substring(0, 2000)}`;

    const response = await env.AI.run('@cf/meta/llama-3-8b-instruct', {
      messages: [{ role: 'user', content: prompt }],
      max_tokens: type === 'título' ? 100 : 1000,
    });

    return response?.response?.trim() || text;
  } catch (e) {
    RSS_ERR(`Error paraphrasing ${type}:`, e.message);
    return text;
  }
}

// ============================================================
// shuffleArray — Mezcla un array aleatoriamente
// ============================================================
function shuffleArray(array) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// ============================================================
// runRSSIngest — Ingesta artículos y distribuye proporcionalmente
// ============================================================
export async function runRSSIngest(env) {
  console.log('[RSS INGEST] Starting RSS ingestion...');
  
  const FEEDS = [
    'https://www.jornada.com.mx/rss/edicion.xml?v=1',
    'https://www.informador.mx/rss/mexico.xml',
    'https://www.proceso.com.mx/rss/feed.html?id=12',
    'https://expansion.mx/rss',
  ];

  const totalSites = SITIOS_LIST.length;
  const MAX_ARTICLES = 3; // Artículos máximos a ingestar por ejecución
  
  // Calcular cuántos sitios por artículo para distribuir proporcionalmente
  // Si hay 27 sitios y 3 artículos, cada artículo va a 9 sitios (27/3 = 9)
  // Si hay 27 sitios y 1 artículo, el artículo va a todos los sitios (27/1 = 27)
  const sitesPerArticle = Math.ceil(totalSites / MAX_ARTICLES);
  
  console.log(`[RSS INGEST] Total sites: ${totalSites}, Articles: ${MAX_ARTICLES}, Sites per article: ${sitesPerArticle}`);

  let articlesPublished = 0;
  let sitesAssigned = 0;

  for (const feedUrl of FEEDS) {
    if (articlesPublished >= MAX_ARTICLES) break;
    
    try {
      console.log('Fetching feed:', feedUrl);
      const res = await fetch(feedUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } });
      const xml = await res.text();
      const normalizedXml = xml.replace(/[\r\n]+/g, ' ');
      const items = normalizedXml.match(/<(item|entry)>([\s\S]*?)<\/\1>/gi) || [];
      console.log('Items found:', items.length);

      for (const item of items) {
        if (articlesPublished >= MAX_ARTICLES) break;

        const titleMatch = item.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/) || item.match(/<title>([\s\S]*?)<\/title>/);
        const linkMatch = item.match(/<link[^>]+href=["']([^"']+)["']/) || item.match(/<link>([\s\S]*?)<\/link>/);

        if (!titleMatch || !linkMatch) continue;

        let title = titleMatch[1].trim();
        title = title.replace(/^<!\[CDATA\[/, '').replace(/\]\]>$/, '').trim();
        const link = linkMatch[1].trim();

        // Check duplicate
        const urlExists = await env.DB.prepare('SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE SOURCE_URL = ?').bind(link).first();
        if (urlExists) continue;

        // Fetch article
        const articleRes = await fetch(link, { headers: { 'User-Agent': 'Mozilla/5.0' } });
        const html = await articleRes.text();

        // OG Image
        const ogImageMatch = html.match(/<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["']/);
        const imageUrl = ogImageMatch ? ogImageMatch[1] : null;

        if (!imageUrl) continue;

        // Verificar que la imagen sea accesible antes de procesarla
        try {
          const imgCheck = await fetch(imageUrl, { method: 'HEAD', headers: { 'User-Agent': 'Mozilla/5.0' } });
          if (!imgCheck.ok || !imgCheck.headers.get('content-type')?.startsWith('image/')) {
            console.log('[RSS INGEST] Skip: Image not accessible or not image:', imageUrl.substring(0, 50));
            continue;
          }
        } catch (e) {
          console.log('[RSS INGEST] Skip: Image check failed:', e.message);
          continue;
        }

        // Paywall
        const isPaywall = html.toLowerCase().includes('suscripción') || html.toLowerCase().includes('premium');
        if (isPaywall) continue;

        // Content
        const pMatches = html.match(/<p>([\s\S]*?)<\/p>/g) || [];
        let content = pMatches.map(p => p.replace(/<[^>]*>/g, '').trim()).filter(p => p.length > 40).join('\n\n');
        content = cleanArticleContent(content);

        if (content.length < 300) continue;

        // Upload imagen a R2
        let finalImageUrl = imageUrl;
        try {
          console.log('[RSS INGEST] Attempting R2 upload for:', imageUrl.substring(0, 50));
          const r2Url = await uploadToR2(imageUrl, env);
          if (r2Url) {
            finalImageUrl = r2Url;
            console.log('[RSS INGEST] ✓ Image uploaded to R2:', finalImageUrl.substring(0, 50));
          } else {
            console.log('[RSS INGEST] ✗ R2 upload returned null, using original');
          }
        } catch (r2Err) {
          console.log('[RSS INGEST] ✗ R2 upload failed:', r2Err.message);
        }

        // Insert article into DB
        try {
          const now = new Date().toISOString();
          const paraId = crypto.randomUUID();
          const slug = slugify(title);

          await env.DB.prepare(`
            INSERT INTO ARTICULOS_PARAFRASEADOS
              (ID, TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA,
               CATEGORIA, AUTOR, FECHA_PUBLICACION, URL_IMAGEN, SOURCE_URL, ESTADO)
            VALUES (?, ?, ?, ?, ?, 'NACIONAL', ?, ?, ?, ?, 'PUBLICADO')
          `).bind(paraId, title, slug, content, content.substring(0, 200), 'NexoPress', now, finalImageUrl, link).run();

          // Seleccionar sitios aleatorios para este artículo
          const shuffledSites = shuffleArray(SITIOS_LIST);
          
          // Asignar a los sitios calculados (puede ser todos o una parte)
          const sitesToAssign = shuffledSites.slice(0, sitesPerArticle);
          
          console.log(`[RSS INGEST] Assigning article to ${sitesToAssign.length} sites: ${sitesToAssign.join(', ')}`);

          for (const siteSlug of sitesToAssign) {
            const siteId = crypto.randomUUID();
            const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

            await env.DB.prepare(`
              INSERT INTO ${tableName} (ID, ID_PARAFRASEADO, FECHA_ASIGNACION, FB_PUBLICADO, FB_FECHA, FB_POST_ID)
              VALUES (?, ?, datetime('now'), 0, NULL, NULL)
            `).bind(siteId, paraId).run();
            
            sitesAssigned++;
          }

          console.log(`[RSS INGEST] Published: "${title.substring(0, 40)}..." to ${sitesToAssign.length} sites`);
          articlesPublished++;
        } catch (dbErr) {
          console.error('[RSS INGEST] DB Error:', dbErr.message);
        }
      }
    } catch (e) {
      console.error(`[RSS INGEST] Feed error ${feedUrl}:`, e.message);
    }
  }

  console.log(`[RSS INGEST] Complete: ${articlesPublished} articles, ${sitesAssigned} site assignments.`);
  return articlesPublished;
}
