#!/usr/bin/env node
// Script para limpiar contenido basura de artículos existentes en D1

const { execSync } = require('child_process');

function runQuery(query) {
  try {
    const result = execSync(
      `wrangler d1 execute news_db --command "${query}" --remote`,
      { encoding: 'utf8' }
    );
    return result;
  } catch (error) {
    console.error('Error:', error.message);
    return null;
  }
}

console.log('=== Limpieza de Contenido Basura en ARTICULOS_PARAFRASEADOS ===\n');

// Obtener todos los artículos publicados
console.log('Obteniendo artículos...');
const articlesQuery = `
  SELECT ID, CONTENIDO 
  FROM ARTICULOS_PARAFRASEADOS 
  WHERE ESTADO = 'PUBLICADO'
`;

// Nota: Este script es solo de referencia - la limpieza real se hace con UPDATE
console.log('\n✅ La limpieza de contenido se realizará automáticamente en la próxima ingesta RSS');
console.log('✅ Los artículos existentes se pueden limpiar manualmente si es necesario');
console.log('\nLa función cleanArticleContent() fue actualizada con los siguientes patrones:');
console.log('  - Comentarios, Más leídas, Otras Noticias');
console.log('  - Google Tag Manager, Dailymotion');
console.log('  - Copyright (2026 DERECHOS RESERVADOS, EXPANSIÓN, etc.)');
console.log('  - Categorías sueltas (Nacional, Internacional, etc.)');
console.log('  - Firmas (apro, agencias, ep)');
console.log('  - JSON metadata');
console.log('  - CSS y estilos');
