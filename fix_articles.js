const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_CONFIG = path.join(__dirname, 'src/wrangler.toml');

function cleanContent(content) {
  if (!content) return content;
  let newContent = content;
  
  const stringsToCut = [
    '_____________________________________________',
    '#dailymotion-pip-large-viewport',
    'googletag.cmd.push',
    'Últimas noticias Deportes',
    'Más leídas'
  ];

  for (const str of stringsToCut) {
    const idx = newContent.indexOf(str);
    if (idx !== -1) {
      newContent = newContent.substring(0, idx);
    }
  }

  // Also clean up trailing whitespace
  return newContent.trim();
}

async function fixTable(tableName, idCol, contentCol) {
  console.log(`
--- Procesando tabla ${tableName} ---`);
  
  // 1. Obtener todos los IDs y Contenidos
  console.log(`Obteniendo datos de ${tableName}...`);
  const query = `SELECT ${idCol}, ${contentCol} FROM ${tableName} WHERE ${contentCol} LIKE '%dailymotion%' OR ${contentCol} LIKE '%googletag%' OR ${contentCol} LIKE '%_____________________________________________%'`;
  
  let output;
  try {
    output = execSync(
      `npx wrangler d1 execute news_db --remote --json --command="${query}"`,
      { encoding: 'utf-8', maxBuffer: 1024 * 1024 * 10 }
    );
  } catch (err) {
    console.error(`Error al consultar ${tableName}:`, err.message);
    return;
  }

  if (!output || !output.trim()) {
    console.log(`No hay datos a limpiar en ${tableName}`);
    return;
  }

  let rows;
  try {
    const results = JSON.parse(output);
    rows = results[0].results;
  } catch (err) {
    console.error(`Error al parsear JSON de ${tableName}:`, err.message);
    return;
  }

  console.log(`Se encontraron ${rows.length} registros para limpiar en ${tableName}.`);

  let count = 0;
  for (const row of rows) {
    const originalContent = row[contentCol];
    const cleanedContent = cleanContent(originalContent);
    
    if (originalContent !== cleanedContent) {
      // Update DB
      const id = row[idCol];
      // Escape single quotes for SQL
      const escapedContent = cleanedContent.replace(/'/g, "''");
      const updateQuery = `UPDATE ${tableName} SET ${contentCol} = '${escapedContent}' WHERE ${idCol} = '${id}'`;
      
      const tempFile = `temp_update_${tableName}_${count}.sql`;
      fs.writeFileSync(tempFile, updateQuery);
      
      try {
        execSync(`npx wrangler d1 execute news_db --remote --file=${tempFile}`, { encoding: 'utf-8' });
        count++;
        console.log(`✅ Registro limpiado en ${tableName}: ${id}`);
      } catch (err) {
        console.error(`❌ Error al actualizar ${id} en ${tableName}:`, err.message);
      } finally {
        if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);
      }
    }
  }
  console.log(`Total actualizados en ${tableName}: ${count}`);
}

async function main() {
  await fixTable('ARTICULOS_ORIGINALES', 'ID', 'CONTENIDO');
  await fixTable('ARTICULOS_PARAFRASEADOS', 'ID', 'CONTENIDO');
  await fixTable('ARTICULOS_CMS', 'ID', 'CONTENIDO');
  console.log('\\n--- LIMPIEZA COMPLETADA ---');
}

main().catch(console.error);
