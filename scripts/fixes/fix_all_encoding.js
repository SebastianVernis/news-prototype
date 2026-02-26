/**
 * Script completo para corregir encoding en TODA la base de datos
 * - ARTICULOS_ORIGINALES
 * - ARTICULOS_PARAFRASEADOS
 * - ARTICULOS_CMS
 * - REVISION_CONTENIDO
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_CONFIG = path.join(__dirname, '../../src/wrangler.toml');

// Mapa completo de encoding ISO-8859-1 a UTF-8
const ENCODING_MAP = {
  'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
  'Ã': 'Á', 'Ã‰': 'É', 'Ã': 'Í', 'Ã“': 'Ó', 'Ãš': 'Ú',
  'Ã±': 'ñ', 'Ã‘': 'Ñ',
  'Â¡': '¡', 'Â¿': '¿',
  'â€œ': '"', 'â€': '"', 'â€': '"',
  'â€˜': "'", 'â€™': "'",
  'â€"': '–', 'â€"': '—',
  'â€¦': '...',
  'Â': '',
  'Ã': '',
  'Â°': '°',
  'Â±': '±',
  'Â©': '©',
  'Â®': '®',
  'â€¢': '•',
  'â€º': '›',
  'â€¹': '‹',
  'Ã¼': 'ü', 'Ãœ': 'Ü',
  'Ã¶': 'ö', 'Ã–': 'Ö',
  'Ã¤': 'ä', 'Ã„': 'Ä',
  'ÃŸ': 'ß',
  'Ã¨': 'è', 'Ã©': 'é', 'Ãª': 'ê', 'Ã«': 'ë',
  'Ã ': 'à', 'Ã¢': 'â', 'Ã´': 'ô', 'Ã»': 'û',
  'Ã§': 'ç', 'Ã': 'Ç',
  'Ãµ': 'õ', 'Ã•': 'Õ',
  'Ã£': 'ã', 'Ã': 'Ã',
  '\u0000': '' // Eliminar caracteres nulos
};

function fixEncoding(text) {
  if (!text) return "";
  let fixed = text;
  
  // Aplicar mapa de encoding
  for (const [bad, good] of Object.entries(ENCODING_MAP)) {
    fixed = fixed.split(bad).join(good);
  }
  
  // Correcciones específicas comunes
  fixed = fixed.replace(/MÃ©xico/g, 'México');
  fixed = fixed.replace(/MÃ©jico/g, 'México');
  fixed = fixed.replace(/JalÃ­sco/g, 'Jalisco');
  fixed = fixed.replace(/MÃ©xicano/g, 'Mexicano');
  fixed = fixed.replace(/AmÃ©rica/g, 'América');
  fixed = fixed.replace(/Ãšltimas/g, 'Últimas');
  fixed = fixed.replace(/PÃºblico/g, 'Público');
  fixed = fixed.replace(/GobiÃ©rno/g, 'Gobierno');
  fixed = fixed.replace(/elecciÃ³n/g, 'elección');
  fixed = fixed.replace(/elecciÃ³nes/g, 'elecciones');
  fixed = fixed.replace(/naÃ§Ã£o/g, 'nação');
  
  // Corregir espacios antes de puntuación
  fixed = fixed.replace(/\s+([,.!?;:])/g, '$1');
  
  // Corregir falta de espacio después de puntuación
  fixed = fixed.replace(/([,.!?;:])([a-zA-ZáéíóúÁÉÍÓÚñÑ])/g, '$1 $2');
  
  // Corregir puntos suspensivos múltiples
  fixed = fixed.replace(/\.\.+/g, '...');
  
  // Corregir espacios múltiples
  fixed = fixed.replace(/\s\s+/g, ' ');
  
  // Eliminar líneas vacías múltiples
  fixed = fixed.replace(/\n{3,}/g, '\n\n');
  
  return fixed.trim();
}

function processTable(tableName, idField, textFields) {
  console.log(`\n🔧 Procesando ${tableName}...`);
  
  try {
    // Obtener todos los registros
    const fields = [idField, ...textFields].join(', ');
    const output = execSync(
      `npx wrangler d1 execute news_db --remote --command="SELECT ${fields} FROM ${tableName}" --config=${WRANGLER_CONFIG} --json`,
      { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 }
    );
    
    const data = JSON.parse(output);
    const records = data[0]?.results || data.results || data;
    console.log(`   📊 Registros: ${records.length}`);
    
    let updates = [];
    let updatedCount = 0;
    
    for (const record of records) {
      const updatesForRecord = {};
      let hasChanges = false;
      
      // Revisar cada campo de texto
      for (const field of textFields) {
        if (record[field]) {
          const fixed = fixEncoding(record[field]);
          if (fixed !== record[field]) {
            updatesForRecord[field] = fixed;
            hasChanges = true;
          }
        }
      }
      
      if (hasChanges) {
        updatedCount++;
        // Construir UPDATE
        const setClauses = Object.entries(updatesForRecord)
          .map(([field, value]) => `${field} = '${value.replace(/'/g, "''")}'`)
          .join(', ');
        
        updates.push(`UPDATE ${tableName} SET ${setClauses} WHERE ${idField} = '${record[idField]}';`);
      }
    }
    
    console.log(`   📝 A corregir: ${updatedCount}`);
    
    if (updates.length === 0) {
      console.log(`   ✅ Sin cambios necesarios`);
      return 0;
    }
    
    // Ejecutar actualizaciones en lotes
    console.log(`   🔄 Ejecutando actualizaciones...`);
    let totalUpdated = 0;
    
    for (let i = 0; i < updates.length; i += 10) {
      const chunk = updates.slice(i, i + 10);
      const tempFile = `fix_enc_${Date.now()}.sql`;
      fs.writeFileSync(tempFile, chunk.join('\n'));
      
      try {
        execSync(
          `npx wrangler d1 execute news_db --remote --file=${tempFile} --config=${WRANGLER_CONFIG} --yes`,
          { encoding: 'utf-8', stdio: 'pipe' }
        );
        totalUpdated += chunk.length;
        console.log(`      ✅ Lote ${Math.floor(i/10)+1}/${Math.ceil(updates.length/10)}`);
      } catch (err) {
        console.error(`      ❌ Error en lote: ${err.message}`);
      } finally {
        if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);
      }
    }
    
    console.log(`   ✅ Actualizados: ${totalUpdated}`);
    return totalUpdated;
    
  } catch (err) {
    console.error(`   ❌ Error: ${err.message}`);
    return 0;
  }
}

async function run() {
  console.log('🔧 CORRECCIÓN DE ENCODING COMPLETA\n');
  console.log('📍 Objetivo: Todas las tablas con contenido de texto\n');
  
  const startTime = Date.now();
  let totalUpdated = 0;
  
  // Procesar cada tabla
  totalUpdated += processTable('ARTICULOS_ORIGINALES', 'ID', ['TITULO', 'DESCRIPCION', 'CONTENIDO']);
  totalUpdated += processTable('ARTICULOS_PARAFRASEADOS', 'ID', ['TITULO_PARAFRASEADO', 'DESCRIPCION_PARAFRASEADA', 'CONTENIDO']);
  totalUpdated += processTable('ARTICULOS_CMS', 'ID', ['TITULO', 'DESCRIPCION', 'CONTENIDO']);
  totalUpdated += processTable('REVISION_CONTENIDO', 'ID', ['TITULO_PROPUESTO', 'DESCRIPCION_PROPUESTA', 'CONTENIDO_PROPUESTO']);
  
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
  
  console.log('\n' + '='.repeat(60));
  console.log('✨ CORRECCIÓN DE ENCODING COMPLETADA');
  console.log('='.repeat(60));
  console.log(`⏱️  Tiempo total: ${elapsed}s`);
  console.log(`📝 Total registros actualizados: ${totalUpdated}`);
  console.log('='.repeat(60));
}

run();
