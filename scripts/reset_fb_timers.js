#!/usr/bin/env node
/**
 * Script de EMERGENCIA para resetear TODOS los timers de Facebook en KV
 * 
 * Uso: node reset_fb_timers.js
 * 
 * Este script:
 * 1. Obtiene TODOS los sitios de la tabla SITIOS
 * 2. Resetea el timer `last_fb_post_[site]` a 0 para cada sitio
 * 3. Opcionalmente: establece un timestamp antiguo para que todos publiquen inmediatamente
 */

const { execSync } = require('child_process');

// Lista completa de los 27 sitios
const SITES = [
  // Sitios Estables (10)
  'radiocinconoticias', 'centralmexico', 'tvmexico', 'cbnnoticias',
  'mexicoinformado', 'nodoinformativo', 'bitacoraurbana',
  'reportecentralmx', 'verticenoticias', 'noticiasobjetivo',
  // Nuevos Sitios (17)
  'boominformativo', 'capitalpress', 'diarioexpress', 'elpulsomexicano',
  'enfoquecapital', 'enfoquedirecto', 'formulacdmx', 'mexicantimes',
  'mexico360noticias', 'mradio', 'noticiashorizonte', 'pulsodiario',
  'puntoclave', 'puntonoticias', 'radarinformativo', 'reportediario',
  'televisionabc'
];

// Opciones
const RESET_TO_ZERO = process.argv.includes('--zero');
const RESET_TO_OLD = process.argv.includes('--old');

// Calcular timestamp
let timestampValue;
if (RESET_TO_ZERO) {
  timestampValue = '0';
  console.log('⚠️  MODO: Resetear timers a 0 (publicación inmediata)\n');
} else if (RESET_TO_OLD) {
  // Hace 4 horas - para que todos los sitios publiquen inmediatamente
  timestampValue = (Date.now() - 4 * 60 * 60 * 1000).toString();
  console.log('⚠️  MODO: Resetear timers a 4 horas atrás (publicación en próximo cron)\n');
} else {
  // Por defecto: hace 2 horas - algunos sitios publicarán, otros esperarán
  timestampValue = (Date.now() - 2 * 60 * 60 * 1000).toString();
  console.log('ℹ️  MODO: Resetear timers a 2 horas atrás (default)\n');
}

console.log(`📋 Sitios a resetear: ${SITES.length}`);
console.log(`⏰ Timestamp: ${timestampValue}\n`);

// Ejecutar comandos wrangler
let success = 0;
let failed = 0;

for (const site of SITES) {
  const kvKey = `last_fb_post_${site}`;
  // Sintaxis correcta wrangler 4.x: wrangler kv key put <key> <value> --namespace-id <ID> --remote
  const command = `wrangler kv key put "${kvKey}" "${timestampValue}" --namespace-id fbf21fb75f5647a8966858d199b44e0b --remote`;
  
  try {
    execSync(command, { 
      stdio: ['pipe', 'pipe', 'pipe'],
      cwd: __dirname
    });
    console.log(`✅ ${site}`);
    success++;
  } catch (error) {
    console.error(`❌ ${site}: ${error.message}`);
    failed++;
  }
}

console.log('\n─────────────────────────────────────────');
console.log(`✅ Exitosos: ${success}`);
console.log(`❌ Fallidos: ${failed}`);
console.log('─────────────────────────────────────────');

if (failed > 0) {
  console.log('\n⚠️  Algunos sitios fallaron. Verifica que wrangler esté autenticado.');
  process.exit(1);
} else {
  console.log('\n✅ ¡Todos los timers reseteados correctamente!');
  console.log('📌 El próximo cron ejecutará publicación para todos los sitios.');
}
