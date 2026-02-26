/**
 * Script para exportar CSV comparativo de artículos
 * Originales vs Parafraseados
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_CONFIG = path.join(__dirname, '../../src/wrangler.toml');
const OUTPUT_FILE = path.join(__dirname, '../../reporte_articulos_' + Date.now() + '.csv');

function escapeCSV(text) {
  if (!text) return '';
  // Escapar comillas dobles y envolver en comillas si hay comas o saltos
  const escaped = String(text).replace(/"/g, '""');
  return `"${escaped}"`;
}

function run() {
  const target = process.argv.includes('--remote') ? '--remote' : '--local';
  console.log(`📊 Exportando reporte comparativo (${target})...\n`);
  
  try {
    // 1. Obtener artículos originales
    console.log('📥 Obteniendo ARTICULOS_ORIGINALES...');
    const origOutput = execSync(
      `npx wrangler d1 execute news_db ${target} --command="SELECT ID, TITULO, DESCRIPCION, URL_IMAGEN, FECHA, CATEGORIA, CONTENIDO FROM ARTICULOS_ORIGINALES ORDER BY FECHA DESC" --config=${WRANGLER_CONFIG} --json`,
      { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 }
    );
    const origData = JSON.parse(origOutput);
    const originales = origData[0]?.results || [];
    console.log(`   ✅ ${originales.length} artículos originales\n`);

    // 2. Obtener artículos parafraseados
    console.log('📥 Obteniendo ARTICULOS_PARAFRASEADOS...');
    const paraOutput = execSync(
      `npx wrangler d1 execute news_db ${target} --command="SELECT ID, ID_ARTICULO_ORIGINAL, TITULO_PARAFRASEADO, DESCRIPCION_PARAFRASEADA, URL_IMAGEN, FECHA_PUBLICACION, CATEGORIA, CONTENIDO, SITIO_DESTINO FROM ARTICULOS_PARAFRASEADOS ORDER BY FECHA_PUBLICACION DESC" --config=${WRANGLER_CONFIG} --json`,
      { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 }
    );
    const paraData = JSON.parse(paraOutput);
    const parafraseados = paraData[0]?.results || [];
    console.log(`   ✅ ${parafraseados.length} artículos parafraseados\n`);

    // 3. Crear mapa de originales por ID para comparar
    const origMap = new Map();
    originales.forEach(art => {
      origMap.set(art.ID, art);
    });

    // 4. Generar CSV
    console.log('📝 Generando CSV...');
    
    const headers = [
      'TIPO',
      'ID_PARAFRASEADO',
      'ID_ORIGINAL',
      'TITULO_ORIGINAL',
      'TITULO_PARAFRASEADO',
      'DESCRIPCION_ORIGINAL',
      'DESCRIPCION_PARAFRASEADA',
      'URL_IMAGEN_ORIGINAL',
      'URL_IMAGEN_PARAFRASEADO',
      'FECHA_ORIGINAL',
      'FECHA_PUBLICACION',
      'CATEGORIA',
      'SITIO_DESTINO',
      'CONTENIDO_ORIGINAL_PREVIEW',
      'CONTENIDO_PARAFRASEADO_PREVIEW',
      'COINCIDE_IMAGEN',
      'COINCIDE_CATEGORIA'
    ];

    let csvContent = headers.join(',') + '\n';
    let rowsWritten = 0;

    // 5. Escribir filas de parafraseados con su original correspondiente
    parafraseados.forEach(para => {
      const orig = origMap.get(para.ID_ARTICULO_ORIGINAL);
      
      const row = [
        'PARAFRASEADO',
        escapeCSV(para.ID),
        escapeCSV(para.ID_ARTICULO_ORIGINAL || 'N/A'),
        escapeCSV(orig?.TITULO || 'N/A'),
        escapeCSV(para.TITULO_PARAFRASEADO),
        escapeCSV(orig?.DESCRIPCION || 'N/A'),
        escapeCSV(para.DESCRIPCION_PARAFRASEADA),
        escapeCSV(orig?.URL_IMAGEN || 'N/A'),
        escapeCSV(para.URL_IMAGEN || ''),
        escapeCSV(orig?.FECHA || 'N/A'),
        escapeCSV(para.FECHA_PUBLICACION || ''),
        escapeCSV(para.CATEGORIA || ''),
        escapeCSV(para.SITIO_DESTINO || ''),
        escapeCSV((orig?.CONTENIDO || '').substring(0, 200)),
        escapeCSV((para.CONTENIDO || '').substring(0, 200)),
        orig?.URL_IMAGEN === para.URL_IMAGEN ? 'SI' : 'NO',
        orig?.CATEGORIA === para.CATEGORIA ? 'SI' : 'NO'
      ];

      csvContent += row.join(',') + '\n';
      rowsWritten++;
    });

    // 6. Agregar originales sin parafrasear
    const paraOriginalIds = new Set(parafraseados.map(p => p.ID_ARTICULO_ORIGINAL).filter(Boolean));
    const originalesSinParafrasear = originales.filter(o => !paraOriginalIds.has(o.ID));
    
    console.log(`   📊 Originales sin parafrasear: ${originalesSinParafrasear.length}`);

    originalesSinParafrasear.forEach(orig => {
      const row = [
        'ORIGINAL_SIN_PARAFRASEAR',
        'N/A',
        escapeCSV(orig.ID),
        escapeCSV(orig.TITULO),
        'N/A',
        escapeCSV(orig.DESCRIPCION),
        'N/A',
        escapeCSV(orig.URL_IMAGEN || ''),
        'N/A',
        escapeCSV(orig.FECHA || ''),
        'N/A',
        escapeCSV(orig.CATEGORIA || ''),
        'N/A',
        escapeCSV((orig.CONTENIDO || '').substring(0, 200)),
        'N/A',
        'N/A',
        'N/A'
      ];

      csvContent += row.join(',') + '\n';
      rowsWritten++;
    });

    // 7. Guardar archivo
    fs.writeFileSync(OUTPUT_FILE, csvContent, 'utf-8');
    
    console.log(`\n✅ CSV generado exitosamente!`);
    console.log(`📁 Archivo: ${OUTPUT_FILE}`);
    console.log(`📊 Total filas: ${rowsWritten}`);
    console.log(`   - Parafraseados: ${parafraseados.length}`);
    console.log(`   - Originales sin parafrasear: ${originalesSinParafrasear.length}`);
    
    // 8. Mostrar estadísticas adicionales
    console.log('\n📈 ESTADÍSTICAS:');
    const conImagen = parafraseados.filter(p => p.URL_IMAGEN && p.URL_IMAGEN !== 'N/A').length;
    const sinImagen = parafraseados.length - conImagen;
    console.log(`   - Parafraseados con imagen: ${conImagen} (${Math.round(conImagen/parafraseados.length*100)}%)`);
    console.log(`   - Parafraseados sin imagen: ${sinImagen} (${Math.round(sinImagen/parafraseados.length*100)}%)`);
    
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

run();
