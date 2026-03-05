/**
 * Script para limpiar entidades HTML y referencias a medios
 * - Limpia &nbsp;, &amp;, &lt;, &gt;, etc.
 * - Elimina referencias a Revista Proceso
 * - Elimina otras referencias a medios no deseados
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_CONFIG = path.join(__dirname, '../../src/wrangler.toml');

// Entidades HTML a reemplazar
const HTML_ENTITIES = {
  '&nbsp;': ' ',
  '&amp;': '&',
  '&lt;': '<',
  '&gt;': '>',
  '&quot;': '"',
  '&#39;': "'",
  '&apos;': "'",
  '&copy;': '(c)',
  '&reg;': '(R)',
  '&trade;': '(TM)',
  '&mdash;': '-',
  '&ndash;': '-',
  '&hellip;': '...',
  '&lsquo;': "'",
  '&rsquo;': "'",
  '&ldquo;': '"',
  '&rdquo;': '"',
  '&laquo;': '"',
  '&raquo;': '"',
  '&euro;': 'EUR',
  '&pound;': 'GBP',
  '&yen;': 'JPY',
  '&cent;': 'c',
  '&plusmn;': '+/-',
  '&times;': 'x',
  '&divide;': '/',
};

// Referencias a medios a eliminar
const MEDIA_REFERENCES = [
  /Revista\s+Proceso/gi,
  /revista\s+Proceso/gi,
  /de\s+Proceso/gi,
  /en\s+Proceso/gi,
  /por\s+Proceso/gi,
  /según\s+Proceso/gi,
  /Proceso\.com/gi,
  /proceso\.com\.mx/gi,
  /www\.proceso\.com/gi,
  /Revista\s+Q/gi,
  /revista\s+Q/gi,
];

function cleanContent(text) {
  if (!text) return '';
  
  let cleaned = text;
  
  // 1. Reemplazar entidades HTML
  for (const [entity, replacement] of Object.entries(HTML_ENTITIES)) {
    const regex = new RegExp(entity.replace(';', '\\;?'), 'gi');
    cleaned = cleaned.replace(regex, replacement);
  }
  
  // 2. Eliminar referencias a medios
  MEDIA_REFERENCES.forEach(pattern => {
    cleaned = cleaned.replace(pattern, '');
  });
  
  // 3. Limpieza de espacios múltiples
  cleaned = cleaned.replace(/\s+/g, ' ');
  cleaned = cleaned.replace(/\s+\./g, '.');
  cleaned = cleaned.replace(/\s+,/g, ',');
  cleaned = cleaned.replace(/\s+:/g, ':');
  
  // 4. Eliminar espacios al inicio/fin
  cleaned = cleaned.trim();
  
  return cleaned;
}

async function run() {
  const isRemote = process.argv.includes('--remote');
  const target = isRemote ? '--remote' : '--local';
  
  console.log('🧹 Limpiando entidades HTML y referencias a medios...\n');
  console.log(`📍 Objetivo: ${target}\n`);
  
  try {
    // 1. Obtener artículos parafraseados
    console.log('📥 Obteniendo ARTICULOS_PARAFRASEADOS...');
    const output = execSync(
      `npx wrangler d1 execute news_db ${target} --command="SELECT ID, TITULO_PARAFRASEADO, DESCRIPCION_PARAFRASEADA, CONTENIDO FROM ARTICULOS_PARAFRASEADOS" --config=${WRANGLER_CONFIG} --json`,
      { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 }
    );
    
    const data = JSON.parse(output);
    const articles = data[0]?.results || [];
    console.log(`   📊 Artículos: ${articles.length}`);
    
    let updates = [];
    let cleanedCount = 0;
    
    for (const art of articles) {
      const nTitle = cleanContent(art.TITULO_PARAFRASEADO);
      const nDesc = cleanContent(art.DESCRIPCION_PARAFRASEADA);
      const nContent = cleanContent(art.CONTENIDO);
      
      if (nTitle !== art.TITULO_PARAFRASEADO || nDesc !== art.DESCRIPCION_PARAFRASEADA || nContent !== art.CONTENIDO) {
        cleanedCount++;
        updates.push(`UPDATE ARTICULOS_PARAFRASEADOS SET TITULO_PARAFRASEADO='${nTitle.replace(/'/g, "''")}', DESCRIPCION_PARAFRASEADA='${nDesc.replace(/'/g, "''")}', CONTENIDO='${nContent.replace(/'/g, "''")}' WHERE ID='${art.ID}';`);
      }
    }
    
    console.log(`   📝 A limpiar: ${cleanedCount}\n`);
    
    // 2. Ejecutar actualizaciones
    if (updates.length > 0) {
      console.log('🔄 Actualizando ARTICULOS_PARAFRASEADOS...');
      for (let i = 0; i < updates.length; i += 10) {
        const chunk = updates.slice(i, i + 10);
        const tempFile = `clean_html_${Date.now()}.sql`;
        fs.writeFileSync(tempFile, chunk.join('\n'));
        
        try {
          execSync(
            `npx wrangler d1 execute news_db ${target} --file=${tempFile} --config=${WRANGLER_CONFIG} --yes`,
            { encoding: 'utf-8', stdio: 'pipe' }
          );
          console.log(`   ✅ Lote ${Math.floor(i/10)+1}/${Math.ceil(updates.length/10)}`);
        } catch (err) {
          console.log(`   ❌ Error: ${err.message}`);
        } finally {
          if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);
        }
      }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('✨ LIMPIEZA COMPLETADA');
    console.log('='.repeat(60));
    console.log(`📰 Artículos limpiados: ${cleanedCount}`);
    console.log('='.repeat(60));
    
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

run();
