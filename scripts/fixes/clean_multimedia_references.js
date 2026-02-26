/**
 * Script para eliminar referencias a multimedia de títulos y contenido
 * Elimina: (VIDEO), (FOTOS), [VIDEO], [FOTOS], etc.
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_CONFIG = path.join(__dirname, '../../src/wrangler.toml');

// Patrones a eliminar
const PATTERNS_TO_REMOVE = [
  /\(VIDEO\)/gi,
  /\(VIDEOS\)/gi,
  /\(FOTO\)/gi,
  /\(FOTOS\)/gi,
  /\(IMAGEN\)/gi,
  /\(IMÁGENES\)/gi,
  /\(AUDIO\)/gi,
  /\(GALERÍA\)/gi,
  /\(GALERIA\)/gi,
  /\[VIDEO\]/gi,
  /\[VIDEOS\]/gi,
  /\[FOTO\]/gi,
  /\[FOTOS\]/gi,
  /\[IMAGEN\]/gi,
  /\[IMÁGENES\]/gi,
  /\[AUDIO\]/gi,
  /\[GALERÍA\]/gi,
  /\[GALERIA\]/gi,
  /\| VIDEO/gi,
  /\| FOTOS/gi,
  /\| FOTO/gi,
  /VIDEO:/gi,
  /FOTOS:/gi,
  /FOTO:/gi,
  /IMAGEN:/gi,
  /IMÁGENES:/gi,
  /— VIDEO/gi,
  /— FOTOS/gi,
  /– VIDEO/gi,
  /– FOTOS/gi,
];

function cleanText(text) {
  if (!text) return '';
  
  let cleaned = text;
  
  // Eliminar patrones
  PATTERNS_TO_REMOVE.forEach(pattern => {
    cleaned = cleaned.replace(pattern, '');
  });
  
  // Limpiar espacios múltiples resultantes
  cleaned = cleaned.replace(/\s+/g, ' ');
  cleaned = cleaned.replace(/\s+\./g, '.');
  cleaned = cleaned.replace(/\s+,/g, ',');
  cleaned = cleaned.replace(/\s+:/g, ':');
  
  // Eliminar espacios al inicio/fin
  cleaned = cleaned.trim();
  
  return cleaned;
}

async function run() {
  const isRemote = process.argv.includes('--remote');
  const target = isRemote ? '--remote' : '--local';
  
  console.log('🧹 Limpiando referencias a multimedia (VIDEO, FOTOS, etc.)...\n');
  console.log(`📍 Objetivo: ${target}\n`);
  
  try {
    // 1. Obtener artículos para limpiar
    console.log('📥 Obteniendo ARTICULOS_PARAFRASEADOS...');
    const paraOutput = execSync(
      `npx wrangler d1 execute news_db ${target} --command="SELECT ID, TITULO_PARAFRASEADO, DESCRIPCION_PARAFRASEADA, CONTENIDO FROM ARTICULOS_PARAFRASEADOS" --config=${WRANGLER_CONFIG} --json`,
      { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 }
    );
    
    const paraData = JSON.parse(paraOutput);
    const paraArticles = paraData[0]?.results || [];
    console.log(`   📊 Artículos: ${paraArticles.length}`);
    
    let paraUpdates = [];
    let paraCleaned = 0;
    
    for (const art of paraArticles) {
      const nTitle = cleanText(art.TITULO_PARAFRASEADO);
      const nDesc = cleanText(art.DESCRIPCION_PARAFRASEADA);
      const nContent = cleanText(art.CONTENIDO);
      
      if (nTitle !== art.TITULO_PARAFRASEADO || nDesc !== art.DESCRIPCION_PARAFRASEADA || nContent !== art.CONTENIDO) {
        paraCleaned++;
        paraUpdates.push(`UPDATE ARTICULOS_PARAFRASEADOS SET TITULO_PARAFRASEADO='${nTitle.replace(/'/g, "''")}', DESCRIPCION_PARAFRASEADA='${nDesc.replace(/'/g, "''")}', CONTENIDO='${nContent.replace(/'/g, "''")}' WHERE ID='${art.ID}';`);
      }
    }
    
    console.log(`   📝 A limpiar: ${paraCleaned}\n`);
    
    // 2. Obtener artículos originales
    console.log('📥 Obteniendo ARTICULOS_ORIGINALES...');
    const origOutput = execSync(
      `npx wrangler d1 execute news_db ${target} --command="SELECT ID, TITULO, DESCRIPCION, CONTENIDO FROM ARTICULOS_ORIGINALES" --config=${WRANGLER_CONFIG} --json`,
      { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 }
    );
    
    const origData = JSON.parse(origOutput);
    const origArticles = origData[0]?.results || [];
    console.log(`   📊 Artículos: ${origArticles.length}`);
    
    let origUpdates = [];
    let origCleaned = 0;
    
    for (const art of origArticles) {
      const nTitle = cleanText(art.TITULO);
      const nDesc = cleanText(art.DESCRIPCION);
      const nContent = cleanText(art.CONTENIDO);
      
      if (nTitle !== art.TITULO || nDesc !== art.DESCRIPCION || nContent !== art.CONTENIDO) {
        origCleaned++;
        origUpdates.push(`UPDATE ARTICULOS_ORIGINALES SET TITULO='${nTitle.replace(/'/g, "''")}', DESCRIPCION='${nDesc.replace(/'/g, "''")}', CONTENIDO='${nContent.replace(/'/g, "''")}' WHERE ID='${art.ID}';`);
      }
    }
    
    console.log(`   📝 A limpiar: ${origCleaned}\n`);
    
    // 3. Ejecutar actualizaciones parafraseados
    if (paraUpdates.length > 0) {
      console.log('🔄 Actualizando ARTICULOS_PARAFRASEADOS...');
      for (let i = 0; i < paraUpdates.length; i += 10) {
        const chunk = paraUpdates.slice(i, i + 10);
        const tempFile = `clean_media_${Date.now()}.sql`;
        fs.writeFileSync(tempFile, chunk.join('\n'));
        
        try {
          execSync(
            `npx wrangler d1 execute news_db ${target} --file=${tempFile} --config=${WRANGLER_CONFIG} --yes`,
            { encoding: 'utf-8', stdio: 'pipe' }
          );
          console.log(`   ✅ Lote ${Math.floor(i/10)+1}/${Math.ceil(paraUpdates.length/10)}`);
        } catch (err) {
          console.log(`   ❌ Error: ${err.message}`);
        } finally {
          if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);
        }
      }
    }
    
    // 4. Ejecutar actualizaciones originales
    if (origUpdates.length > 0) {
      console.log('\n🔄 Actualizando ARTICULOS_ORIGINALES...');
      for (let i = 0; i < origUpdates.length; i += 10) {
        const chunk = origUpdates.slice(i, i + 10);
        const tempFile = `clean_media_${Date.now()}.sql`;
        fs.writeFileSync(tempFile, chunk.join('\n'));
        
        try {
          execSync(
            `npx wrangler d1 execute news_db ${target} --file=${tempFile} --config=${WRANGLER_CONFIG} --yes`,
            { encoding: 'utf-8', stdio: 'pipe' }
          );
          console.log(`   ✅ Lote ${Math.floor(i/10)+1}/${Math.ceil(origUpdates.length/10)}`);
        } catch (err) {
          console.log(`   ❌ Error: ${err.message}`);
        } finally {
          if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);
        }
      }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('✨ LIMPIEZA DE MULTIMEDIA COMPLETADA');
    console.log('='.repeat(60));
    console.log(`📰 ARTICULOS_PARAFRASEADOS limpiados: ${paraCleaned}`);
    console.log(`📰 ARTICULOS_ORIGINALES limpiados: ${origCleaned}`);
    console.log('='.repeat(60));
    
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

run();
