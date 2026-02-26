/**
 * Script de Revisión Exhaustiva Geográfica y Limpieza en D1 (Node.js)
 * - Purga artículos centrados en Argentina o España sin relevancia mexicana.
 * - Elimina referencias a canales/medios argentinos (Telefe, TN, C5N, etc.)
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_CONFIG = path.join(__dirname, '../../src/wrangler.toml');

function cleanTextExhaustive(text) {
  if (!text) return "";
  let cleaned = text;
  
  // 1. Canales y Medios Argentinos
  const argMedia = [
    /Telefe/gi, /C5N/gi, /TN\.com\.ar/gi, /Todo Noticias/gi, /El Trece/gi,
    /Crónica TV/gi, /América TV/gi, /Canal 9/gi, /TyC Sports/gi, /Directv Sports/gi,
    /La Nación \+/gi, /Radio Mitre/gi, /Radio 10/gi, /Infobae/gi, /Página\/12/gi
  ];
  
  // 2. Otros Bloques Residuales
  const badPatterns = [
    /¿Quiénes somos\? \| Contacto.*?Siguenos en:/gi,
    /La Jornada de Oriente.*?La Jornada Zacatecas/gi,
    /Medios asociados:.*?Radio Bilingüe/gi,
    /Haz clic aquí para leer más historias.*?(\n|$)/gi,
    /Suscríbete aquí a nuestro nuevo newsletter.*?(\n|$)/gi,
    /Y recuerda que puedes recibir notificaciones.*?(\n|$)/gi,
    /Descarga la última versión y actívalas.*?(\n|$)/gi,
    /Final de Más leídas/gi,
    /El nuevo podcast de BBC Mundo.*?(\n|$)/gi,
    /Episodios/gi,
    /Fin de Podcast/gi,
    /BBC News Mundo/g,
    /BBC Mundo/g,
    /Te puede interesar\s*[>:-].*?(\n|$)/gi,
    /Lee también\s*[>:-].*?(\n|$)/gi,
    /Según supo LA NACION,?/gi,
    /Como contó LA NACION,?/gi,
    /LA NACION/g,
    /La Jornada/g,
    /Copyright.*?\d{4}.*?(\n|$)/gi,
    /Los mejores comentarios:.*?Ver más vídeos/gis,
    /Tecnología Videojuegos Entretenimiento Gastronomía Motor Estilo de vida Economía/gi,
    /Ediciones Internacionales Suscribir Reciente/gi,
    /Ver más artículos Motorpasión México TV/gi
  ];
  
  for (const p of argMedia) { cleaned = cleaned.replace(p, ''); }
  for (const p of badPatterns) { cleaned = cleaned.replace(p, ''); }

  // 3. Normalización
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n');
  cleaned = cleaned.replace(/^[ |]+$/gm, '');
  cleaned = cleaned.replace(/  +/g, ' ');
  
  return cleaned.trim();
}

function shouldDeleteStrict(art) {
  const content = art.CONTENIDO || '';
  const title = art.TITULO_PARAFRASEADO || '';
  const text = (title + ' ' + content).toLowerCase();
  
  const hasMexico = text.includes('méxico') || text.includes('mexic') || text.includes('cdmx') || text.includes('sheinbaum') || text.includes('mencho');
  const isArgentina = text.includes('argentina') || text.includes('buenos aires') || text.includes('milei') || text.includes('casa rosada') || text.includes('fate');
  const isSpain = text.includes('españa') || text.includes('madrid') || text.includes('santander') || text.includes('barcelona') || text.includes('ayuntamiento de');

  // Si es fuertemente de otro país y no menciona a México
  if (isArgentina && !hasMexico) return "GEOGRAFIA_ARG";
  if (isSpain && !hasMexico) return "GEOGRAFIA_ESP";
  
  return null;
}

async function run() {
  const target = process.argv.includes('--remote') ? '--remote' : '--local';
  console.log(`🔍 Purga Geográfica y Medios Argentinos (${target})...`);
  try {
    const output = execSync(`npx wrangler d1 execute news_db ${target} --command="SELECT ID, TITULO_PARAFRASEADO, CONTENIDO FROM ARTICULOS_PARAFRASEADOS" --config=${WRANGLER_CONFIG} --json`, { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 });
    const articles = JSON.parse(output)[0]?.results || [];
    console.log(`📊 Analizando ${articles.length} artículos...`);
    
    let toDelete = [];
    let toUpdate = [];

    for (const art of articles) {
      const reason = shouldDeleteStrict(art);
      if (reason) {
        toDelete.push({ id: art.ID, reason });
        continue;
      }
      const cleaned = cleanTextExhaustive(art.CONTENIDO || '');
      if (cleaned !== (art.CONTENIDO || '')) {
        toUpdate.push({ id: art.ID, content: cleaned });
      }
    }

    if (toDelete.length > 0) {
      console.log(`🗑️ Eliminando ${toDelete.length} artículos por geografía...`);
      for (let i = 0; i < toDelete.length; i += 50) {
        const chunk = toDelete.slice(i, i + 50);
        const ids = chunk.map(item => `'${item.id}'`).join(',');
        const sql = `DELETE FROM METRICAS_CONTENIDO WHERE ID_ARTICULO_PARAFRASEADO IN (${ids}); DELETE FROM ARTICULOS_PARAFRASEADOS WHERE ID IN (${ids});`;
        const f = `del_geo_${Date.now()}.sql`;
        fs.writeFileSync(f, sql);
        execSync(`npx wrangler d1 execute news_db ${target} --file=${f} --config=${WRANGLER_CONFIG} --yes`);
        fs.unlinkSync(f);
      }
    }

    if (toUpdate.length > 0) {
      console.log(`📝 Saneando ${toUpdate.length} artículos...`);
      for (let i = 0; i < toUpdate.length; i += 20) {
        const chunk = toUpdate.slice(i, i + 20);
        const sql = chunk.map(art => `UPDATE ARTICULOS_PARAFRASEADOS SET CONTENIDO = '${art.content.replace(/'/g, "''")}' WHERE ID = '${art.id}';`).join('\n');
        const f = `upd_geo_${Date.now()}.sql`;
        fs.writeFileSync(f, sql);
        execSync(`npx wrangler d1 execute news_db ${target} --file=${f} --config=${WRANGLER_CONFIG} --yes`);
        fs.unlinkSync(f);
      }
    }
    console.log(`✨ Purga y saneamiento completado.`);
  } catch (err) { console.error('❌ Error:', err.message); }
}
run();
