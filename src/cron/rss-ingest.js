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
// runRSSIngest — Ingesta 1 artículo por sitio cada 30 minutos
// ============================================================
export async function runRSSIngest(env) {
  RSS_LOG('Starting RSS ingestion...');

  const FEEDS = [
    // Fuentes verificadas que funcionan desde Cloudflare Workers
    'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada',  // El País México
    'https://expansion.mx/rss',  // Expansión (negocios)
    'https://www.proceso.com.mx/rss/feed.html?id=12',  // Proceso (nacional)
    'https://www.sinembargo.mx/feed',  // SinEmbargo (general)
  ];

  let published = 0;

  for (const feedUrl of FEEDS) {
    if (published >= SITIOS_LIST.length) break; // Max 1 por sitio

    try {
      RSS_LOG(`Fetching feed: ${feedUrl}`);
      const res = await fetch(feedUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } });
      const xml = await res.text();
      
      // Normalizar XML (remover saltos de línea para el regex)
      const normalizedXml = xml.replace(/[\r\n]+/g, ' ');
      
      // Soportar tanto RSS 2.0 (<item>) como Atom (<entry>)
      const items = normalizedXml.match(/<(item|entry)>([\s\S]*?)<\/\1>/gi) || [];
      RSS_LOG(`Feed ${feedUrl} returned ${items.length} items.`);

      for (const item of items) {
        if (published >= SITIOS_LIST.length) break;

        // Parsear título y link
        const titleMatch =
          item.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/) ||
          item.match(/<title>([\s\S]*?)<\/title>/);
        const linkMatch =
          item.match(/<link[^>]+href=["']([^"']+)["']/) ||
          item.match(/<link>([\s\S]*?)<\/link>/);

        if (!titleMatch || !linkMatch) continue;

        let title = titleMatch[1].trim();
        title = title.replace(/^<!\[CDATA\[/, '').replace(/\]\]>$/, '').trim();
        const link = linkMatch[1].trim();

        // Verificar si URL ya existe (evitar duplicados)
        const urlExists = await env.DB.prepare(
          'SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE SOURCE_URL = ?'
        ).bind(link).first();

        if (urlExists) {
          RSS_LOG(`Skip: Already exists (${link})`);
        } else if (!imageUrl) {
          RSS_LOG('Skip: No OG Image, using fallback.');
        } else if (isPaywall) {
          RSS_LOG(`Skip: Paywall detected (${link})`);
            continue;
          }

          const pMatches = html.match(/<p>([\s\S]*?)<\/p>/g) || [];
          content = pMatches
            .map((p) => p.replace(/<[^>]*>/g, '').trim())
            .filter((p) => p.length > 40)
            .join('\n\n');

          // Limpieza profunda de contenido
          content = cleanArticleContent(content);
        } catch (e) {
          console.error(`[RSS INGEST] Error scraping ${link}:`, e.message);
          continue;
        }

        if (content.length < 300) {
          console.log(`[RSS INGEST] Skip: Content too short (${content.length} chars).`);
          continue;
        }

        // Verificar nuevamente que el contenido no sea de paywall
        if (
          content.toLowerCase().includes('suscripción') ||
          content.toLowerCase().includes('premium') ||
          content.toLowerCase().includes('compartir tu cuenta')
        ) {
          console.log('[RSS INGEST] Skip: Paywall content detected in parsed text');
          continue;
        }

        // Parafrasear con IA
        console.log('[RSS INGEST] Running AI proofread...');
        try {
          const aiTitle   = await proofreadTextAI(title, 'título', env);
          const aiContent = await proofreadTextAI(content, 'contenido', env);

          if (!aiTitle || !aiContent) {
            console.error('[RSS INGEST] AI returned empty results.');
            continue;
          }

          // Subir imagen a R2
          const r2ImageUrl = await uploadToR2(imageUrl, env);
          const finalImg   = r2ImageUrl || imageUrl;

          // Insertar en PARAFRASEADOS
          const now    = new Date().toISOString();
          const paraId = crypto.randomUUID();
          const slug   = slugify(aiTitle);

          await env.DB.prepare(`
            INSERT INTO ARTICULOS_PARAFRASEADOS
              (ID, TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA,
               CATEGORIA, AUTOR, FECHA_PUBLICACION, URL_IMAGEN, SOURCE_URL, ESTADO)
            VALUES (?, ?, ?, ?, ?, 'NACIONAL', ?, ?, ?, ?, 'PUBLICADO')
          `).bind(
            paraId, aiTitle, slug, aiContent,
            aiContent.substring(0, 200), 'Redacción NexoPress',
            now, finalImg, link
          ).run();

          // DISTRIBUCIÓN: Insertar en 1 sitio (round-robin)
          const siteSlug  = SITIOS_LIST[published % SITIOS_LIST.length];
          const siteId    = crypto.randomUUID();
          const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

          await env.DB.prepare(`
            INSERT INTO ${tableName} (
              ID, ID_PARAFRASEADO, FECHA_ASIGNACION,
              FB_PUBLICADO, FB_FECHA, FB_POST_ID
            ) VALUES (?, ?, datetime('now'), 0, NULL, NULL)
          `).bind(siteId, paraId).run();

          console.log(`[RSS INGEST] Published to ${siteSlug}: ${aiTitle.substring(0, 40)}...`);

          // El artículo queda disponible para Facebook Timer (se publica cuando el timer cumple 3 horas)

          published++;
        } catch (aiErr) {
          console.error('[RSS INGEST] AI Error:', aiErr.message);
          continue;
        }
      }
    } catch (e) {
      console.error(`[RSS INGEST] Feed error ${feedUrl}:`, e.message);
    }
  }

  console.log(`[RSS INGEST] Complete: ${published} articles published.`);
  return published;
}
